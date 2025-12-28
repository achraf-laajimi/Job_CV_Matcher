# app/agents/jd_parser.py
from app.utils.ollama_async import chat_async


async def parse_jd_async(jd_text: str):
    """
    Extract structured job requirements using LLM.
    
    Args:
        jd_text: Clean JD text
        
    Returns:
        JSON string with structured JD requirements
    """
    prompt = f"""
Extract structured job requirements.
Return ONLY valid JSON.

Fields:
- required_skills (list)
- nice_to_have (list)
- min_years_experience (number)
- domain (list)
- seniority (junior | mid | senior | lead)

Job Description:
{jd_text}
"""

    res = await chat_async(
        model="mistral:7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 400}
    )

    return res["message"]["content"]
