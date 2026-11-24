# interview_questions.py

skill_question_map = {
    "python": [
        "Explain the difference between lists and tuples in Python.",
        "How do you manage memory in Python?",
        "What are Python decorators and how do you use them?"
    ],
    "machine learning": [
        "What is overfitting and how do you prevent it?",
        "Explain the difference between supervised and unsupervised learning.",
        "What is a confusion matrix?"
    ],
    "sql": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How do you optimize SQL queries?",
        "Explain normalization and denormalization."
    ],
    "javascript": [
        "What are closures in JavaScript?",
        "Explain event delegation.",
        "How does prototypal inheritance work?"
    ],
    # Add more skills and questions as needed
}

def generate_interview_questions(skills, jd_keywords):
    questions = []
    combined = set(skills).union(set(jd_keywords))
    for skill in combined:
        skill_lower = skill.lower()
        if skill_lower in skill_question_map:
            questions.extend(skill_question_map[skill_lower])
    return questions if questions else ["No specific interview questions found for the extracted skills."]

if __name__ == "__main__":
    skills = input("Enter comma-separated extracted skills: ").lower().split(",")
    jd_keywords = input("Enter comma-separated job description keywords: ").lower().split(",")
    interview_qs = generate_interview_questions([s.strip() for s in skills], [k.strip() for k in jd_keywords])
    print("\n=== Suggested Interview Questions ===")
    for i, q in enumerate(interview_qs, 1):
        print(f"{i}. {q}")
