# app/agents/cv_parser.py
from app.utils.ollama_async import chat_async


async def parse_cv_async(cv_text: str):
    """
    Extract structured information from CV using LLM.
    
    Args:
        cv_text: Clean CV text
        
    Returns:
        JSON string with structured CV data
    """
    prompt = f"""
Extract structured information from the CV.
Return ONLY valid JSON.

Fields:
- skills (list)
- years_experience (number)
- job_titles (list)
- domains (list)
- seniority (junior | mid | senior | lead)

CV:
{cv_text}
"""

    res = await chat_async(
        model="mistral:7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 400}
    )

    return res["message"]["content"]
