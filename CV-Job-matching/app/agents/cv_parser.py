# app/agents/cv_parser.py
import ollama

def parse_cv(cv_text: str):
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

    res = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 400}
    )

    return res["message"]["content"]
