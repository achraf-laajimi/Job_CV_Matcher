# app/embedding/rag_embedder.py
"""
RAG-optimized CV embedder with caching.
Uses fast transformer embeddings (NOT Ollama).
"""

import hashlib
import numpy as np
from typing import List, Dict, Tuple, Optional
from app.embedding.transformer_embedder import embed_chunks_sync, embed_text_sync, cosine_similarity
from app.utils.rag import chunk_cv


class RAGEmbedder:
    """
    Manages chunk-based embeddings for CVs with caching support.
    Now uses sentence-transformers for 5-6x faster embeddings!
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG embedder with in-memory cache.
        
        Args:
            model_name: Transformer model for embeddings
                - "all-MiniLM-L6-v2" (90MB, FAST, recommended)
                - "all-mpnet-base-v2" (420MB, best quality)
        """
        self._cache: Dict[str, Dict] = {}
        self.model_name = model_name
    
    def get_cv_hash(self, cv_text: str) -> str:
        """
        Generate hash for CV text.
        
        Args:
            cv_text: Clean CV text
            
        Returns:
            SHA256 hash of the CV
        """
        return hashlib.sha256(cv_text.encode()).hexdigest()
    
    def embed_cv(
        self,
        cv_text: str,
        force_recompute: bool = False
    ) -> Dict:
        """
        Chunk and embed a CV, with caching.
        NOW USES FAST TRANSFORMERS (not Ollama).
        
        Args:
            cv_text: Clean CV text
            force_recompute: If True, bypass cache and recompute
            
        Returns:
            Dictionary with chunks, embeddings, and metadata
        """
        cv_hash = self.get_cv_hash(cv_text)
        
        # Check cache
        if not force_recompute and cv_hash in self._cache:
            return self._cache[cv_hash]
        
        # Chunk the CV
        chunks = chunk_cv(cv_text)
        
        # Embed chunks using fast transformer (NOT Ollama)
        embeddings = embed_chunks_sync(chunks, self.model_name)
        
        # Store in cache
        result = {
            "cv_hash": cv_hash,
            "chunks": chunks,
            "embeddings": embeddings,
            "num_chunks": len(chunks),
            "cv_text": cv_text
        }
        
        self._cache[cv_hash] = result
        
        return result
    
    def get_cached_cv(self, cv_text: str) -> Optional[Dict]:
        """
        Get cached CV embeddings if available.
        
        Args:
            cv_text: Clean CV text
            
        Returns:
            Cached CV data or None
        """
        cv_hash = self.get_cv_hash(cv_text)
        return self._cache.get(cv_hash)
    
    def retrieve_for_jd(
        self,
        cv_data: Dict,
        jd_text: str,
        top_k: int = 5
    ) -> Tuple[List[str], List[float], np.ndarray]:
        """
        Retrieve top K CV chunks relevant to a job description.
        
        Args:
            cv_data: CV data from embed_cv()
            jd_text: Job description text
            top_k: Number of chunks to retrieve
            
        Returns:
            Tuple of (relevant chunks, scores, jd_embedding)
        """
        from app.utils.rag import retrieve_relevant_chunks
        
        # Embed JD using fast transformer (NOT Ollama)
        jd_embedding = embed_text_sync(jd_text, self.model_name)
        
        # Retrieve relevant chunks
        relevant_chunks, scores = retrieve_relevant_chunks(
            cv_data["chunks"],
            cv_data["embeddings"],
            jd_embedding,
            top_k=top_k
        )
        
        return relevant_chunks, scores, jd_embedding
    
    def clear_cache(self):
        """Clear the embedding cache."""
        self._cache.clear()
    
    def cache_size(self) -> int:
        """Get number of cached CVs."""
        return len(self._cache)


# Global instance for use across the application
_rag_embedder = RAGEmbedder()


def get_rag_embedder() -> RAGEmbedder:
    """
    Get the global RAG embedder instance.
    
    Returns:
        Global RAGEmbedder instance
    """
    return _rag_embedder
