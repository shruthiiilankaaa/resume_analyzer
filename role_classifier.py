# role_classifier.py
from collections import Counter

ROLE_SKILLS = {
    'SDE': {'python', 'javascript', 'react', 'node', 'django', 'rest', 'git'},
    'Data Scientist': {'python', 'pandas', 'numpy', 'sklearn', 'ml', 'data'},
    'DevOps': {'docker', 'kubernetes', 'jenkins', 'aws', 'ci/cd', 'linux'}
}

def classify_job_role(skills, return_confidences=False):
    skill_set = set([s.lower() for s in skills])
    role_scores = {}

    for role, required_skills in ROLE_SKILLS.items():
        match_count = len(skill_set & required_skills)
        role_scores[role] = match_count / len(required_skills)

    best_role = max(role_scores, key=role_scores.get)
    confidence = round(role_scores[best_role] * len(ROLE_SKILLS[best_role]), 2)

    if return_confidences:
        return best_role, confidence, role_scores
    else:
        return best_role, confidence
