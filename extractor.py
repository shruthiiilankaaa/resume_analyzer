import re
import spacy
from nltk.corpus import stopwords

# Load English tokenizer, POS tagger, etc.
nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words('english'))

# -----------------------------
# Contact Info Extractors
# -----------------------------
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){2}\d{4}', text)
    return match.group(0) if match else None

# -----------------------------
# Name Extraction
# -----------------------------
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

# -----------------------------
# Education Keywords
# -----------------------------
EDUCATION_KEYWORDS = [
    "bachelor", "master", "b.sc", "m.sc", "b.tech", "m.tech", "phd", "mba", 
    "degree", "university", "college", "school"
]

def extract_education(text):
    lines = text.lower().split('\n')
    education_lines = [line for line in lines if any(keyword in line for keyword in EDUCATION_KEYWORDS)]
    return education_lines[:3]  # Return top 3 education lines

# -----------------------------
# Skill Extraction (basic version)
# -----------------------------
SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "sql", "html", "css",
    "machine learning", "data science", "tensorflow", "pandas", "numpy",
    "react", "node", "django", "flask", "aws", "docker", "git"
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()
    for skill in SKILL_KEYWORDS:
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)

# -----------------------------
# Full Extraction Function
# -----------------------------
def extract_candidate_info(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": extract_skills(text)
    }

# Test it (optional)
if __name__ == "__main__":
    with open("extracted_resume.txt", "r", encoding="utf-8") as f:
        resume_text = f.read()

    extracted = extract_candidate_info(resume_text)
    print("\n=== Extracted Candidate Info ===\n")
    for key, value in extracted.items():
        print(f"{key.capitalize()}: {value}")
