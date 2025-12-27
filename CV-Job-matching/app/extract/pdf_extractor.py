# app/extract/pdf_extractor.py
import pdfplumber

def extract_pdf_text(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
