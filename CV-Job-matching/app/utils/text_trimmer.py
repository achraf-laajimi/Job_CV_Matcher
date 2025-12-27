# app/utils/text_trimmer.py
import re

def trim_cv(text: str, max_chars: int = 3000) -> str:
    """
    Trim CV to only relevant sections to reduce LLM processing time.
    Keeps: skills, experience, education, projects, tools, technologies
    """
    # Keywords to identify relevant sections
    keywords = [
        "skill", "experience", "education", "project", "tool",
        "technology", "framework", "language", "work", "job",
        "developer", "engineer", "programming", "software",
        "responsibility", "achievement", "certification"
    ]
    
    lines = text.split("\n")
    relevant_lines = []
    
    for line in lines:
        line_lower = line.lower()
        # Keep lines that contain keywords or look like bullet points
        if any(keyword in line_lower for keyword in keywords) or \
           line.strip().startswith(('-', '•', '*', '▪')) or \
           re.search(r'\d{4}', line):  # Keep lines with years
            relevant_lines.append(line)
    
    # Join and truncate to max_chars
    trimmed = "\n".join(relevant_lines)
    
    if len(trimmed) > max_chars:
        trimmed = trimmed[:max_chars]
    
    return trimmed


def trim_jd(text: str, max_chars: int = 2000) -> str:
    """
    Trim job description to essential requirements.
    Keeps: requirements, skills, experience, qualifications
    """
    keywords = [
        "require", "skill", "experience", "must", "should",
        "qualifications", "responsibilities", "looking for",
        "ideal candidate", "years", "knowledge", "proficient"
    ]
    
    lines = text.split("\n")
    relevant_lines = []
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in keywords) or \
           line.strip().startswith(('-', '•', '*', '▪')):
            relevant_lines.append(line)
    
    trimmed = "\n".join(relevant_lines)
    
    if len(trimmed) > max_chars:
        trimmed = trimmed[:max_chars]
    
    return trimmed
