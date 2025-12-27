# app/embedding/similarity.py
import ollama
import numpy as np
from typing import List

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def embedding_score(cv_text: str, jd_text: str) -> float:
    """
    Legacy method: Full document embedding (not recommended for large CVs).
    Consider using embedding_score_rag() for better performance.
    """
    cv_emb = ollama.embeddings(
        model="nomic-embed-text",
        prompt=cv_text
    )["embedding"]

    jd_emb = ollama.embeddings(
        model="nomic-embed-text",
        prompt=jd_text
    )["embedding"]

    return round(cosine(cv_emb, jd_emb) * 100, 1)


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
        cosine(cv_emb, jd_embedding)
        for cv_emb in cv_embeddings
    ]
    
    # Aggregate based on pooling strategy
    if pooling == "max":
        # Best matching chunk
        score = max(similarities)
    elif pooling == "mean":
        # Average across all chunks
        score = np.mean(similarities)
    elif pooling == "weighted":
        # Weighted by top 3 chunks
        top_3 = sorted(similarities, reverse=True)[:3]
        weights = [0.5, 0.3, 0.2]
        score = sum(s * w for s, w in zip(top_3, weights[:len(top_3)]))
    else:
        score = max(similarities)
    
    return round(score * 100, 1)
