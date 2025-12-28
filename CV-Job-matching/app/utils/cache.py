# app/utils/cache.py
import hashlib
import json
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
