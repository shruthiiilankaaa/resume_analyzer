# resume_jd_analyzer.py
from matcher import match_resume_to_jd_with_recommendations
from heuristic_feedback import heuristic_resume_feedback
from analyze_resume import extract_text_from_file

def run_analysis(resume_path, jd_path):
    resume_text = extract_text_from_file(resume_path)
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    match_result = match_resume_to_jd_with_recommendations(resume_text, jd_text)
    heuristic_result = heuristic_resume_feedback(resume_text)

    print("\n=== Resume to JD Matching Results ===\n")
    print(f"Fit Score: {match_result['score_percent']}%")
    print(f"Matched Skills: {match_result['matched_skills']}")
    print(f"Missing Skills: {match_result['missing_skills']}")

    if match_result['recommendations']:
        print("\nRecommendations:")
        for rec in match_result['recommendations']:
            print(f"- {rec}")
    else:
        print("\nGreat fit! No recommendations.")

    print("\n=== Heuristic Resume Feedback ===\n")
    if heuristic_result:
        for f in heuristic_result:
            print(f"- {f}")
    else:
        print("No heuristic issues found! Resume looks good.")

if __name__ == "__main__":
    resume_path = input("Enter path to resume file (.pdf/.docx): ").strip().replace('"', '')
    jd_path = input("Enter path to job description file (.txt): ").strip().replace('"', '')
    try:
        run_analysis(resume_path, jd_path)
    except Exception as e:
        print(f"Error: {e}")
