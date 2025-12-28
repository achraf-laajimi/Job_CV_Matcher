# app/pipeline.py
import asyncio
import logging
import time
from app.extract.pdf_extractor import extract_pdf_text
from app.extract.cleaner import clean_text
from app.agents.cv_parser import parse_cv_async
from app.agents.jd_parser import parse_jd_async
from app.embedding.transformer_embedder import embedding_score_rag
from app.agents.scorer import score_cv_rag_async
from app.utils.cache import CVCache
from app.utils.text_trimmer import trim_cv, trim_jd
from app.embedding.rag_embedder import get_rag_embedder
from app.utils.rag import chunk_jd, retrieve_relevant_chunks
from app.embedding.transformer_embedder import embed_chunks_async, embed_text_async

# Setup logger with proper configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler if not already present
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Global cache instance
_cache = CVCache()

# Global RAG embedder
_rag_embedder = get_rag_embedder()


def clear_cache():
    """Clear all cached CV data"""
    _cache.clear()


async def run_pipeline_rag_async(cv_path, jd_text, top_k=5):
    """
    FULLY ASYNC RAG pipeline - MAXIMUM PERFORMANCE.
    
    Optimizations:
    - Parallel chunk embedding (all chunks at once)
    - Concurrent CV+JD parsing
    - RAG retrieval (70-90% context reduction)
    - No ThreadPoolExecutor overhead
    
    RECOMMENDED: Use this for production.
    
    Args:
        cv_path: Path to CV PDF
        jd_text: Job description text
        top_k: Number of CV chunks to retrieve (default: 5)
        
    Returns:
        Scoring result as JSON string
    """
    start_total = time.time()
    logger.info("="*60)
    logger.info(f"🚀 Starting RAG Pipeline | CV: {cv_path}")
    
    # 1. Extract and clean (fast sync operations)
    logger.info("📄 Step 1: Extracting PDF text...")
    t1 = time.time()
    cv_raw = extract_pdf_text(cv_path)
    cv_clean = clean_text(cv_raw)
    jd_clean = clean_text(jd_text)
    logger.info(f"   ✓ Extracted & cleaned | CV: {len(cv_clean)} chars, JD: {len(jd_clean)} chars ({time.time()-t1:.2f}s)")
    
    # 2. Check if CV chunks are cached
    logger.info("💾 Step 2: Checking cache...")
    cached_cv_data = _rag_embedder.get_cached_cv(cv_clean)
    
    if cached_cv_data:
        logger.info(f"   ✓ Cache HIT! Using {cached_cv_data['num_chunks']} cached chunks")
        cv_data = cached_cv_data
    else:
        logger.info("   ⚠ Cache MISS - Processing CV...")
        # Chunk CV
        from app.utils.rag import chunk_cv
        t2 = time.time()
        chunks = chunk_cv(cv_clean)
        logger.info(f"   ✓ Chunked CV into {len(chunks)} chunks")
        
        # ASYNC: Embed all chunks in PARALLEL using fast transformers
        logger.info("🔢 Step 3: Embedding CV chunks (async)...")
        t3 = time.time()
        embeddings = await embed_chunks_async(chunks)
        logger.info(f"   ✓ Embedded {len(chunks)} chunks in {time.time()-t3:.2f}s")
        
        cv_data = {
            "chunks": chunks,
            "embeddings": embeddings,
            "num_chunks": len(chunks)
        }
        
        # Cache for future use
        cv_hash = _rag_embedder.get_cv_hash(cv_clean)
        _rag_embedder._cache[cv_hash] = cv_data
        logger.info("   ✓ Cached embeddings for reuse")
    
    # 3. ASYNC: Embed JD using fast transformer
    logger.info("🔢 Step 4: Embedding job description (async)...")
    t4 = time.time()
    jd_embedding = await embed_text_async(jd_clean)
    logger.info(f"   ✓ Embedded JD in {time.time()-t4:.2f}s")
    
    # 4. Retrieve relevant CV chunks (fast, synchronous)
    logger.info(f"🔍 Step 5: Retrieving top {top_k} relevant chunks...")
    t5 = time.time()
    from app.utils.rag import retrieve_relevant_chunks
    relevant_chunks, chunk_scores = retrieve_relevant_chunks(
        cv_data["chunks"],
        cv_data["embeddings"],
        jd_embedding,
        top_k=top_k
    )
    logger.info(f"   ✓ Retrieved {len(relevant_chunks)} chunks in {time.time()-t5:.2f}s")
    logger.info(f"   📊 Scores: {[f'{s:.2f}' for s in chunk_scores]}")
    
    # 5. Calculate overall similarity score
    sim_score = embedding_score_rag(
        cv_data["embeddings"],
        jd_embedding,
        pooling="max"
    )
    logger.info(f"   📈 Overall similarity: {sim_score:.1f}/100")
    
    # 6. Prepare text for parsing
    logger.info("✂️ Step 6: Trimming text for LLM...")
    cv_trimmed = trim_cv(cv_clean)
    jd_trimmed = trim_jd(jd_clean)
    logger.info(f"   ✓ Trimmed | CV: {len(cv_trimmed)} chars, JD: {len(jd_trimmed)} chars")
    
    # Optional: chunk JD for even more optimization
    jd_chunks = chunk_jd(jd_clean, max_chars=400)
    top_jd_chunks = jd_chunks[:3] if len(jd_chunks) > 3 else jd_chunks
    
    # 7. ASYNC: Parse CV and JD in PARALLEL (KEY OPTIMIZATION!)
    logger.info("🤖 Step 7: Parsing CV & JD with LLM (parallel async)...")
    t7 = time.time()
    cv_json, jd_json = await asyncio.gather(
        parse_cv_async(cv_trimmed),
        parse_jd_async(jd_trimmed)
    )
    logger.info(f"   ✓ Parsed both in {time.time()-t7:.2f}s")
    
    # 8. ASYNC: Score using RAG
    logger.info("🎯 Step 8: Scoring match with LLM...")
    t8 = time.time()
    result = await score_cv_rag_async(
        cv_json=cv_json,
        jd_json=jd_json,
        relevant_cv_chunks=relevant_chunks,
        chunk_scores=chunk_scores,
        similarity_score=sim_score,
        jd_chunks=top_jd_chunks
    )
    logger.info(f"   ✓ Scored in {time.time()-t8:.2f}s")
    
    total_time = time.time() - start_total
    logger.info(f"✅ Pipeline Complete | Total: {total_time:.2f}s")
    logger.info("="*60)
    
    return result


# Legacy sync version with ThreadPoolExecutor (not recommended)

