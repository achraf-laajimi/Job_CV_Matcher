# app/utils/rag.py
"""
RAG (Retrieval Augmented Generation) utilities for CV-Job matching.
Uses fast transformer embeddings instead of Ollama.
"""

import numpy as np
import re
from typing import List, Tuple, Dict

from app.embedding.transformer_embedder import (
    embed_text_sync,
    embed_chunks_sync,
    embed_text_async,
    embed_chunks_async,
    cosine_similarity
)


def chunk_cv(text: str, max_chars: int = 500) -> List[str]:
    """
    Chunk CV into logical sections using section headers and character limits.
    
    Prioritizes:
    - Skills sections
    - Each job experience
    - Education
    - Projects
    - Certifications
    
    Args:
        text: Clean CV text
        max_chars: Maximum characters per chunk
        
    Returns:
        List of CV chunks
    """
    chunks = []
    
    # First, try to split by common section headers
    section_patterns = [
        r'\n\s*(?:SKILLS?|TECHNICAL SKILLS?|CORE COMPETENCIES)\s*\n',
        r'\n\s*(?:EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE)\s*\n',
        r'\n\s*(?:EDUCATION|ACADEMIC BACKGROUND)\s*\n',
        r'\n\s*(?:PROJECTS?|KEY PROJECTS?)\s*\n',
        r'\n\s*(?:CERTIFICATIONS?|CERTIFICATES?)\s*\n',
    ]
    
    # Split by sections first
    sections = [text]
    for pattern in section_patterns:
        new_sections = []
        for section in sections:
            parts = re.split(pattern, section, flags=re.IGNORECASE)
            new_sections.extend([p.strip() for p in parts if p.strip()])
        sections = new_sections
    
    # Now chunk each section by character limit
    for section in sections:
        if len(section) <= max_chars:
            if section.strip():
                chunks.append(section.strip())
        else:
            # Split long sections by paragraphs/lines
            current = ""
            for line in section.split("\n"):
                if len(current) + len(line) + 1 > max_chars:
                    if current.strip():
                        chunks.append(current.strip())
                    current = line
                else:
                    current += "\n" + line if current else line
            
            if current.strip():
                chunks.append(current.strip())
    
    return chunks


def chunk_jd(text: str, max_chars: int = 500) -> List[str]:
    """
    Chunk Job Description into logical sections.
    
    Args:
        text: Clean JD text
        max_chars: Maximum characters per chunk
        
    Returns:
        List of JD chunks
    """
    chunks = []
    
    # Split by common JD sections
    section_patterns = [
        r'\n\s*(?:REQUIREMENTS?|QUALIFICATIONS?|REQUIRED SKILLS?)\s*\n',
        r'\n\s*(?:RESPONSIBILITIES|JOB DUTIES|ROLE)\s*\n',
        r'\n\s*(?:NICE TO HAVE|PREFERRED|BONUS)\s*\n',
        r'\n\s*(?:ABOUT|COMPANY|OVERVIEW)\s*\n',
    ]
    
    sections = [text]
    for pattern in section_patterns:
        new_sections = []
        for section in sections:
            parts = re.split(pattern, section, flags=re.IGNORECASE)
            new_sections.extend([p.strip() for p in parts if p.strip()])
        sections = new_sections
    
    # Chunk by size
    for section in sections:
        if len(section) <= max_chars:
            if section.strip():
                chunks.append(section.strip())
        else:
            current = ""
            for line in section.split("\n"):
                if len(current) + len(line) + 1 > max_chars:
                    if current.strip():
                        chunks.append(current.strip())
                    current = line
                else:
                    current += "\n" + line if current else line
            
            if current.strip():
                chunks.append(current.strip())
    
    return chunks


# Embedding functions now use transformers (imported from transformer_embedder)
# embed_text_sync, embed_chunks_sync, embed_text_async, embed_chunks_async
# are all available and MUCH faster than Ollama


def retrieve_relevant_chunks(
    chunks: List[str],
    chunk_embeddings: List[np.ndarray],
    query_embedding: np.ndarray,
    top_k: int = 5
) -> Tuple[List[str], List[float]]:
    """
    Retrieve top K most relevant chunks using cosine similarity.
    
    Args:
        chunks: Original text chunks
        chunk_embeddings: Embeddings for each chunk
        query_embedding: Query embedding (e.g., JD embedding)
        top_k: Number of top chunks to retrieve
        
    Returns:
        Tuple of (top chunks, similarity scores)
    """
    # Calculate similarity scores
    scores = [
        cosine_similarity(chunk_emb, query_embedding)
        for chunk_emb in chunk_embeddings
    ]
    
    # Get top K indices
    top_k = min(top_k, len(chunks))
    top_indices = np.argsort(scores)[-top_k:][::-1]
    
    # Return top chunks and their scores
    top_chunks = [chunks[i] for i in top_indices]
    top_scores = [scores[i] for i in top_indices]
    
    return top_chunks, top_scores
