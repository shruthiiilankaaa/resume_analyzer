# matcher.py
import re

from analyze_resume import extract_text_from_file, extract_skills

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def extract_jd_skills(jd_text):
    # This function assumes JD skills are comma-separated or line-separated
    # You can customize this parsing logic as needed
    lines = jd_text.split('\n')
    skills = []
    for line in lines:
        # Split by commas and strip whitespace
        parts = [s.strip() for s in line.split(',')]
        skills.extend(parts)
    # Filter out empty strings and lowercase
    skills = [skill.lower() for skill in skills if skill]
    return set(skills)

def match_resume_to_jd_with_recommendations(resume_text, jd_text):
    resume_skills = set(skill.lower() for skill in extract_skills(resume_text))
    jd_skills = extract_jd_skills(jd_text)

    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)

    score = (len(matched_skills) / max(1, len(jd_skills))) * 100

    recommendations = []
    if score < 60:
        if missing_skills:
            recommendations.append(f"Consider adding or emphasizing these skills: {', '.join(missing_skills)}")
        if "project" not in resume_text.lower():
            recommendations.append("Add detailed projects section highlighting relevant experience.")

    return {
        "score_percent": round(score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "recommendations": recommendations
    }

if __name__ == "__main__":
    resume_path = input("Enter path to resume file (.pdf/.docx): ").strip().replace('"', '')
    jd_path = input("Enter path to job description file (.txt): ").strip().replace('"', '')

    try:
        resume_text = extract_text_from_file(resume_path)
        with open(jd_path, "r", encoding="utf-8") as f:
            jd_text = f.read()

        result = match_resume_to_jd_with_recommendations(resume_text, jd_text)

        print("\n=== Resume to JD Matching Results ===\n")
        print(f"Fit Score: {result['score_percent']}%")
        print(f"Matched Skills: {result['matched_skills']}")
        print(f"Missing Skills: {result['missing_skills']}")
        if result['recommendations']:
            print("\nRecommendations:")
            for rec in result['recommendations']:
                print(f"- {rec}")
        else:
            print("\nGreat fit! No recommendations.")
    except Exception as e:
        print(f"Error: {e}")
