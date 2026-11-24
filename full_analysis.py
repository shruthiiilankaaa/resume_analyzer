import os
from getpass import getpass
import torch

from analyze_resume import extract_text_from_file, extract_skills
from extra_features import extract_experience_periods
from interview_questions import generate_interview_questions
from salary_estimator import estimate_salary
from summary_generator import generate_resume_summary
from ats_checker import check_ats_score
from soft_skills import extract_soft_skills
from role_classifier import classify_job_role
from visualization import plot_skill_match_radar
from ml_visualization import plot_role_prediction_confidence


def load_jd_text(jd_path: str) -> str:
    """Load job description text from a .txt or .pdf file."""
    if not os.path.exists(jd_path):
        raise FileNotFoundError(f"Job description file not found: {jd_path}")
    if jd_path.lower().endswith(".pdf"):
        return extract_text_from_file(jd_path)
    with open(jd_path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    resume_path = input("Enter resume path (.pdf/.docx): ").strip().replace('"', "")
    jd_path = input("Enter job description file (.txt/.pdf): ").strip().replace('"', "")

    try:
        # Load and parse text
        resume_text = extract_text_from_file(resume_path)
        jd_text = load_jd_text(jd_path)

        # Extract skills & experience
        years, months = extract_experience_periods(resume_text)
        total_exp_years = round(years + months / 12, 1)
        skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        jd_keywords = [w.strip(".,:;()[]") for w in jd_text.lower().split() if w.strip(".,:;()[]")]

        # Interview questions
        questions = generate_interview_questions(skills, jd_keywords)

        # Salary estimate
        level, salary = estimate_salary(total_exp_years, skills)

        # Generate summary (optional if no API key is entered)
        print("\nGenerating AI-based resume summary...")
        env_key = os.getenv("OPENAI_API_KEY", "").strip()
        entered_key = getpass("Enter your OpenAI API Key (press Enter to skip): ").strip()
        api_key = entered_key or env_key

        if api_key:
            try:
                summary = generate_resume_summary(resume_text, model="gpt-4o-mini", api_key=api_key)
            except Exception as e:
                summary = f"Error generating summary: {e}"
        else:
            summary = "Skipped (no OpenAI API key provided)."

        # Output Summary
        print("\n=== AI-Generated Resume Summary ===")
        print(summary)

        print("\n=== Career Insights ===")
        print(f"Candidate Experience: {total_exp_years} years")
        print(f"Estimated Level: {level}")
        print(f"Estimated Salary: ${salary}")

        print("\n=== Suggested Interview Questions ===")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")

        # ATS Compatibility
        ats_score, ats_feedback = check_ats_score(resume_text)
        print("\n=== ATS Compatibility Score ===")
        print(f"Score: {ats_score}/100")
        for fb in ats_feedback:
            print(f"- {fb}")

        # Soft Skills
        soft_skills = extract_soft_skills(resume_text)
        print("\n=== Detected Soft Skills ===")
        print(", ".join(soft_skills) if soft_skills else "No soft skills explicitly mentioned.")

        # Job Role Prediction + Confidence Visualization
        role, matched_count, confidence_dict = classify_job_role(skills, return_confidences=True)
        print("\n=== Predicted Job Role ===")
        print(f"{role} (matched {matched_count} core skills)")

        print("\nRendering visualizations...")

        # ML Visualization: Job Role Confidence (PyTorch-based)
        roles = list(confidence_dict.keys())
        scores_tensor = torch.tensor(list(confidence_dict.values()), dtype=torch.float32)
        plot_role_prediction_confidence(roles, scores_tensor)

        # Visualization: Skill Match Radar Chart (using extracted skills for readability)
        radar_jd_items = jd_skills if jd_skills else jd_keywords[:10]
        if skills or radar_jd_items:
            plot_skill_match_radar(skills, radar_jd_items)
        else:
            print("Skipping radar chart: no skills or keywords detected.")

        print("✅ Visualizations rendered successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()