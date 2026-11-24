import os
import docx
from pdfminer.high_level import extract_text

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
        raise ValueError("Unsupported file format")

if __name__ == "__main__":
    file_path = input("Enter path to resume file (.pdf/.docx): ")
    text = extract_text_from_file(file_path)
    print("\n=== Resume Text Extracted ===\n")
    print(text[:1500])  # Print first 1500 chars
    
with open("extracted_resume.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("\nResume text saved to extracted_resume.txt")
