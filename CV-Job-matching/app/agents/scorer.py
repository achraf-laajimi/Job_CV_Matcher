# app/agents/scorer.py
import ollama
from typing import List, Optional

def score_cv(cv_json, jd_json, similarity_score):
    """
    Legacy scorer using full CV/JD (not recommended).
    Use score_cv_rag() for better performance.
    """
    prompt = f"""
You are an ATS scoring agent.

Use:
- Skills match (40%)
- Experience (30%)
- Domain relevance (20%)
- Penalties (10%)

Embedding similarity score: {similarity_score}/100

CV:
{cv_json}

JOB:
{jd_json}

Return JSON:
{{
  "final_score": number,
  "strengths": [],
  "gaps": [],
  "recommendation": "reject | maybe | shortlist"
}}
"""

    res = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 500}
    )

    return res["message"]["content"]


def score_cv_rag(
    cv_json: str,
    jd_json: str,
    relevant_cv_chunks: List[str],
    chunk_scores: List[float],
    similarity_score: float,
    jd_chunks: Optional[List[str]] = None
):
    """
    RAG-optimized scorer: uses only retrieved CV chunks instead of full CV.
    
    Args:
        cv_json: Parsed CV (structured info only - skills, experience, etc.)
        jd_json: Parsed JD (structured requirements)
        relevant_cv_chunks: Top K relevant CV chunks
        chunk_scores: Similarity scores for each chunk
        similarity_score: Overall similarity score
        jd_chunks: Optional top JD requirement chunks
        
    Returns:
        Scoring result as JSON string
    """
    # Format relevant CV information
    cv_context = "\n\n".join([
        f"[Relevant CV Section {i+1}] (relevance: {score:.2f})\n{chunk}"
        for i, (chunk, score) in enumerate(zip(relevant_cv_chunks, chunk_scores))
    ])
    
    # Format JD context (use chunks if available, otherwise full JD)
    if jd_chunks:
        jd_context = "\n\n".join([
            f"[Requirement {i+1}]\n{chunk}"
            for i, chunk in enumerate(jd_chunks)
        ])
    else:
        jd_context = jd_json
    
    prompt = f"""
You are an ATS scoring agent.

Use these weights:
- Skills match (40%)
- Experience (30%)
- Domain relevance (20%)
- Penalties (10%)

Overall embedding similarity: {similarity_score}/100

STRUCTURED CV DATA:
{cv_json}

RELEVANT CV EXCERPTS (filtered by RAG):
{cv_context}

JOB REQUIREMENTS:
{jd_context}

Analyze ONLY the relevant excerpts above. Score the match (0-100).

Return JSON only:
{{
  "final_score": number,
  "strengths": [],
  "gaps": [],
  "recommendation": "reject | maybe | shortlist"
}}
"""

    res = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 500}
    )

    return res["message"]["content"]
