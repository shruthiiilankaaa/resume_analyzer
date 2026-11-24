import re
from analyze_resume import extract_text_from_file, extract_skills

# Define the same skill keywords used in analyze_resume
SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "sql", "html", "css",
    "machine learning", "data science", "tensorflow", "pandas", "numpy",
    "react", "node", "django", "flask", "aws", "docker", "git",
    "github", "figma", "php"
]

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def extract_jd_keywords(jd_text):
    return set(clean_text(jd_text).split())

def match_resume_to_jd(resume_text, jd_text):
    resume_keywords = set(clean_text(resume_text).split())
    jd_keywords = extract_jd_keywords(jd_text)
    common_keywords = resume_keywords.intersection(jd_keywords)

    resume_skills = set(extract_skills(resume_text))
    jd_skills = {kw for kw in jd_keywords if kw in SKILL_KEYWORDS}
    matched_skills = jd_skills.intersection(resume_skills)

    # Fit score
    score = (len(matched_skills) / max(1, len(jd_skills))) * 100

    # Recommendations if score is low
    recommendations = None
    if score < 60:
        missing_skills = jd_skills - resume_skills
        if missing_skills:
            recommendations = {
                "missing_skills": list(missing_skills),
                "advice": f"Consider adding more experience or training in: {', '.join(missing_skills)}"
            }

    return {
        "matched_keywords": list(common_keywords)[:10],
        "matched_skills": list(matched_skills),
        "score_percent": round(score, 2),
        "recommendations": recommendations
    }

if __name__ == "__main__":
    resume_path = input("Enter resume path (.pdf/.docx): ").strip().replace('"', '')
    jd_path = input("Enter job description file (.txt): ").strip().replace('"', '')

    try:
        resume_text = extract_text_from_file(resume_path)
        with open(jd_path, "r", encoding="utf-8") as f:
            jd_text = f.read()

        result = match_resume_to_jd(resume_text, jd_text)

        print("\n=== Resume to JD Matching Results ===\n")
        print(f"Matched Skills: {result['matched_skills']}")
        print(f"Sample Overlapping Keywords: {result['matched_keywords']}")
        print(f"Fit Score: {result['score_percent']}%")

        if result['recommendations']:
            print("\n🚧 Recommendations to Improve Fit:")
            print(f"- Missing Skills: {result['recommendations']['missing_skills']}")
            print(f"- Advice: {result['recommendations']['advice']}")

    except Exception as e:
        print(f"Error: {e}")
