# app/utils/cache.py
import hashlib
import json
import pickle
import numpy as np
from pathlib import Path

class CVCache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache = {}
    
    def get_hash(self, text: str) -> str:
        """Generate SHA-256 hash of text"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def get(self, cv_hash: str):
        """Get cached CV data"""
        # Check memory first
        if cv_hash in self.memory_cache:
            return self.memory_cache[cv_hash]
        
        # Check disk
        cache_file = self.cache_dir / f"{cv_hash}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.memory_cache[cv_hash] = data
                return data
        
        return None
    
    def set(self, cv_hash: str, data: dict):
        """Cache CV data"""
        # Store in memory
        self.memory_cache[cv_hash] = data
        
        # Store on disk
        cache_file = self.cache_dir / f"{cv_hash}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear(self):
        """Clear all caches"""
        self.memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()


class RAGCache(CVCache):
    """
    Extended cache for storing CV chunks and embeddings.
    Uses pickle for numpy array serialization.
    """
    
    def __init__(self, cache_dir=".cache/rag"):
        super().__init__(cache_dir)
        self.embeddings_dir = self.cache_dir / "embeddings"
        self.embeddings_dir.mkdir(exist_ok=True)
    
    def get_rag_data(self, cv_hash: str):
        """
        Get cached RAG data (chunks + embeddings).
        
        Returns:
            Dict with 'chunks' and 'embeddings' or None
        """
        # Check memory first
        if cv_hash in self.memory_cache:
            return self.memory_cache[cv_hash]
        
        # Check disk
        chunks_file = self.cache_dir / f"{cv_hash}_chunks.json"
        embeddings_file = self.embeddings_dir / f"{cv_hash}_emb.pkl"
        
        if chunks_file.exists() and embeddings_file.exists():
            # Load chunks
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            # Load embeddings
            with open(embeddings_file, 'rb') as f:
                embeddings = pickle.load(f)
            
            data = {
                "chunks": chunks,
                "embeddings": embeddings,
                "num_chunks": len(chunks)
            }
            
            self.memory_cache[cv_hash] = data
            return data
        
        return None
    
    def set_rag_data(self, cv_hash: str, chunks: list, embeddings: list):
        """
        Cache RAG data (chunks + embeddings).
        
        Args:
            cv_hash: Hash of the CV text
            chunks: List of text chunks
            embeddings: List of numpy arrays (embeddings)
        """
        data = {
            "chunks": chunks,
            "embeddings": embeddings,
            "num_chunks": len(chunks)
        }
        
        # Store in memory
        self.memory_cache[cv_hash] = data
        
        # Store chunks as JSON
        chunks_file = self.cache_dir / f"{cv_hash}_chunks.json"
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        
        # Store embeddings as pickle (handles numpy arrays)
        embeddings_file = self.embeddings_dir / f"{cv_hash}_emb.pkl"
        with open(embeddings_file, 'wb') as f:
            pickle.dump(embeddings, f)
    
    def clear(self):
        """Clear all caches including embeddings"""
        super().clear()
        for emb_file in self.embeddings_dir.glob("*.pkl"):
            emb_file.unlink()
