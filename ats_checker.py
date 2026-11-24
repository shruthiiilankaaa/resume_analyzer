import re

def check_ats_score(resume_text):
    score = 0
    feedback = []

    sections = ['education', 'experience', 'projects', 'skills', 'achievements', 'certifications']
    for section in sections:
        if section in resume_text.lower():
            score += 10
        else:
            feedback.append(f"Missing section: {section.capitalize()}")

    if re.search(r'\b(github|linkedin|portfolio)\b', resume_text.lower()):
        score += 10
    else:
        feedback.append("Missing professional links (GitHub, LinkedIn, Portfolio)")

    word_count = len(re.findall(r'\w+', resume_text))
    if word_count < 300:
        feedback.append("Resume is too short for ATS (should be 300+ words)")
    elif word_count > 1000:
        feedback.append("Resume is too long (try to keep it under 1000 words)")
    else:
        score += 10

    final_score = min(score, 100)
    return final_score, feedback
