import re

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving", "adaptability",
    "critical thinking", "time management", "creativity", "collaboration", "empathy"
]

def extract_soft_skills(text):
    text = text.lower()
    found = []
    for skill in SOFT_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.append(skill.title())
    return list(set(found))
