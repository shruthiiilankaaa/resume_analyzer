# heuristic_feedback.py

def heuristic_resume_feedback(resume_text):
    feedback = []
    text_lower = resume_text.lower()

    if len(resume_text.split()) < 200:
        feedback.append("Resume looks too short, add more details.")

    if "summary" not in text_lower:
        feedback.append("Add a professional summary at the top.")

    if "linkedin" not in text_lower:
        feedback.append("Include LinkedIn profile link.")

    if "email" not in text_lower:
        feedback.append("Add an email address for contact.")

    if "experience" not in text_lower:
        feedback.append("Include your professional experience section.")

    return feedback


if __name__ == "__main__":
    path = input("Enter path to resume file (.pdf/.docx): ").strip().replace('"', '')
    from analyze_resume import extract_text_from_file
    try:
        resume_text = extract_text_from_file(path)
        feedback = heuristic_resume_feedback(resume_text)
        print("\n=== Heuristic Resume Feedback ===\n")
        if feedback:
            for f in feedback:
                print(f"- {f}")
        else:
            print("No issues found! Resume looks good.")
    except Exception as e:
        print(f"Error: {e}")
