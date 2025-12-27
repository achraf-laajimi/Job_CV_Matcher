# app/agents/jd_parser.py
import ollama



def parse_jd(jd_text: str):
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

    res = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 400}
    )

    return res["message"]["content"]
