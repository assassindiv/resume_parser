import pdfplumber
import docx

def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        try:
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        except:
            return None
    elif file_path.endswith(".docx"):
        try:
            doc = docx.Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        except:
            return None
    return None