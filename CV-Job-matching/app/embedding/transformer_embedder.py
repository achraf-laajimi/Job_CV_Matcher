# app/embedding/transformer_embedder.py
"""
Fast transformer-based embeddings without Ollama overhead.
Uses sentence-transformers for efficient local embedding generation.
"""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
import asyncio
from functools import lru_cache

# Global model instance (loaded once, reused everywhere)
_model = None


@lru_cache(maxsize=1)
def get_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Get or create the global embedding model.
    
    Recommended models:
    - "all-MiniLM-L6-v2" (90MB, FAST, recommended)
    - "all-mpnet-base-v2" (420MB, best quality)
    - "paraphrase-multilingual-MiniLM-L12-v2" (420MB, multilingual)
    
    Args:
        model_name: HuggingFace model name
    
    Returns:
        SentenceTransformer model
    """
    global _model
    if _model is None:
        print(f"Loading embedding model: {model_name}...")
        _model = SentenceTransformer(model_name)
        print(f"✓ Model loaded successfully ({model_name})")
    return _model


def embed_text_sync(text: str, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Embed single text (synchronous).
    
    Args:
        text: Text to embed
        model_name: Model to use
        
    Returns:
        Embedding vector (numpy array)
    """
    model = get_embedding_model(model_name)
    embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    return embedding


def embed_chunks_sync(chunks: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[np.ndarray]:
    """
    Embed multiple chunks (synchronous, batched for speed).
    
    This is MUCH faster than one-by-one encoding because
    sentence-transformers optimizes batch processing.
    
    Args:
        chunks: List of text chunks
        model_name: Model to use
        
    Returns:
        List of embedding vectors
    """
    if not chunks:
        return []
    
    model = get_embedding_model(model_name)
    
    # Batch encoding is much faster than one-by-one
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        batch_size=32,  # Process 32 chunks at once
        show_progress_bar=False
    )
    
    return [emb for emb in embeddings]


async def embed_text_async(text: str, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Embed single text (async wrapper).
    
    Args:
        text: Text to embed
        model_name: Model to use
        
    Returns:
        Embedding vector
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, embed_text_sync, text, model_name)


async def embed_chunks_async(chunks: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[np.ndarray]:
    """
    Embed multiple chunks (async wrapper with batching).
    
    Args:
        chunks: List of text chunks
        model_name: Model to use
        
    Returns:
        List of embedding vectors
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, embed_chunks_sync, chunks, model_name)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity (0-1)
    """
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def embedding_score_rag(
    cv_embeddings: List[np.ndarray],
    jd_embedding: np.ndarray,
    pooling: str = "max"
) -> float:
    """
    RAG-optimized similarity score using CV chunks.
    
    Args:
        cv_embeddings: List of CV chunk embeddings
        jd_embedding: Single JD embedding
        pooling: How to aggregate chunk scores ('max', 'mean', or 'weighted')
        
    Returns:
        Similarity score (0-100)
    """
    if not cv_embeddings:
        return 0.0
    
    # Calculate similarity for each chunk
    similarities = [
        cosine_similarity(cv_emb, jd_embedding)
        for cv_emb in cv_embeddings
    ]
    
    # Aggregate based on pooling strategy
    if pooling == "max":
        score = max(similarities)
    elif pooling == "mean":
        score = float(np.mean(similarities))
    elif pooling == "weighted":
        top_3 = sorted(similarities, reverse=True)[:3]
        weights = [0.5, 0.3, 0.2]
        score = sum(s * w for s, w in zip(top_3, weights[:len(top_3)]))
    else:
        score = max(similarities)
    
    return round(float(score * 100), 1)
