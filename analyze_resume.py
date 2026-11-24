import re
import docx
import spacy
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords

# ----------------- Load NLP & Stopwords -----------------
nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words('english'))

# ----------------- File Parsers -----------------
def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use .pdf or .docx")

# ----------------- Info Extractors -----------------
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){2}\d{4}', text)
    return match.group(0) if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

EDUCATION_KEYWORDS = [
    "bachelor", "master", "b.sc", "m.sc", "b.tech", "m.tech", "phd", "mba", 
    "degree", "university", "college", "school"
]

def extract_education(text):
    lines = text.lower().split('\n')
    return [line.strip() for line in lines if any(keyword in line for keyword in EDUCATION_KEYWORDS)]

SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "sql", "html", "css",
    "machine learning", "data science", "tensorflow", "pandas", "numpy",
    "react", "node", "django", "flask", "aws", "docker", "git",
    "github", "figma", "php"
]

def extract_skills(text):
    text = text.lower()
    return list({skill for skill in SKILL_KEYWORDS if skill in text})

# ----------------- Main Analyzer -----------------
def analyze_resume(file_path):
    try:
        text = extract_text_from_file(file_path)
        info = {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "education": extract_education(text),
            "skills": extract_skills(text)
        }

        print("\n=== Candidate Information Extracted ===\n")
        for key, value in info.items():
            print(f"{key.capitalize()}: {value}")

    except Exception as e:
        print(f"Error: {e}")

# ----------------- Run Script -----------------
if __name__ == "__main__":
    file_path = input("Enter path to resume file (.pdf/.docx): ").strip().replace('"', '')
    analyze_resume(file_path)
