import os
import tempfile
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import nltk
import spacy
from openai import OpenAI


def get_default_openai_key() -> str:
    """Safely fetch OPENAI_API_KEY from environment variables or Streamlit secrets."""
    env_key = os.getenv("OPENAI_API_KEY", "").strip()
    if env_key:
        return env_key
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return str(st.secrets["OPENAI_API_KEY"]).strip()
    except Exception:
        pass
    return ""


# Ensure NLTK stopwords and spaCy model are available on Streamlit Cloud
@st.cache_resource
def setup_nlp():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)
    return spacy.load("en_core_web_sm")


nlp = setup_nlp()

from analyze_resume import (
    extract_text_from_file,
    extract_name,
    extract_email,
    extract_phone,
    extract_education,
    extract_skills,
)
from ats_checker import check_ats_score
from heuristic_feedback import heuristic_resume_feedback
from jd_matcher import match_resume_to_jd
from extra_features import (
    get_word_count,
    get_readability_score,
    compare_keyword_density,
    extract_experience_periods,
)
from role_classifier import classify_job_role
from salary_estimator import estimate_salary
from soft_skills import extract_soft_skills
from interview_questions import generate_interview_questions
from summary_generator import generate_resume_summary
import ai_feedback

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Job Description Matcher")
st.markdown(
    "Upload a resume (`.pdf` or `.docx`) and paste a target job description to analyze "
    "ATS compatibility, skill gaps, career insights, and AI feedback."
)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    default_key = get_default_openai_key()
    openai_api_key = st.text_input(
        "OpenAI API Key (optional)",
        value=default_key,
        type="password",
        help="Required only for AI Summary & GPT Resume Critique.",
    )
    st.info("All rule-based NLP, ATS scoring, role prediction, and visualizations work without an API key.")

col1, col2 = st.columns(2)
with col1:
    uploaded_resume = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])
with col2:
    default_jd = ""
    if os.path.exists("jd_sample.txt"):
        with open("jd_sample.txt", "r", encoding="utf-8") as f:
            default_jd = f.read()
    jd_text = st.text_area("Paste Job Description", value=default_jd, height=220)

if uploaded_resume is not None:
    suffix = os.path.splitext(uploaded_resume.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_resume.read())
        tmp_path = tmp.name

    try:
        resume_text = extract_text_from_file(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    if not resume_text.strip():
        st.error("Could not extract text from the uploaded file. Please ensure it is not a scanned image-only PDF.")
        st.stop()

    # Extract core details
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    education = extract_education(resume_text)
    skills = extract_skills(resume_text)
    soft_skills = extract_soft_skills(resume_text)
    ats_score, ats_feedback = check_ats_score(resume_text)
    heuristics = heuristic_resume_feedback(resume_text)
    word_count = get_word_count(resume_text)
    readability = get_readability_score(resume_text)
    years, months = extract_experience_periods(resume_text)
    total_exp_years = round(years + months / 12, 1)
    level, est_salary = estimate_salary(total_exp_years, skills)
    best_role, _, role_scores = classify_job_role(skills, return_confidences=True)

    # Top KPI Metrics
    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ATS Score", f"{ats_score} / 100")
    m2.metric("Predicted Role", best_role)
    m3.metric("Estimated Level", f"{level} ({total_exp_years} yrs)")
    m4.metric("Est. Annual Salary", f"${est_salary:,.0f}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Profile & ATS",
        "🎯 JD Match & Visuals",
        "💼 Career & Interview Prep",
        "🤖 AI Feedback (GPT)",
        "📝 Raw Extracted Text",
    ])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Candidate Information")
            st.write(f"**Name:** {name or 'Not detected'}")
            st.write(f"**Email:** {email or 'Not detected'}")
            st.write(f"**Phone:** {phone or 'Not detected'}")
            st.write(f"**Word Count:** {word_count} words")
            st.write(f"**Flesch Reading Ease:** {readability:.2f}")
            st.write("**Technical Skills:**", ", ".join(skills) if skills else "None detected")
            st.write("**Soft Skills:**", ", ".join(soft_skills) if soft_skills else "None detected")
            if education:
                st.write("**Education Lines:**")
                for line in education:
                    st.markdown(f"- {line}")

        with c2:
            st.subheader("ATS & Heuristic Feedback")
            if ats_feedback:
                st.warning("**ATS Improvements:**")
                for fb in ats_feedback:
                    st.markdown(f"- {fb}")
            else:
                st.success("Great ATS structure! All core sections and links detected.")

            if heuristics:
                st.info("**Heuristic Checks:**")
                for h in heuristics:
                    st.markdown(f"- {h}")

    with tab2:
        if jd_text.strip():
            match_res = match_resume_to_jd(resume_text, jd_text)
            st.subheader(f"JD Skill Fit Score: {match_res['score_percent']}%")
            st.progress(min(int(match_res["score_percent"]), 100))

            mc1, mc2 = st.columns(2)
            with mc1:
                st.write("**Matched Skills:**", ", ".join(match_res["matched_skills"]) or "None")
                st.write("**Overlapping Keywords:**", ", ".join(match_res["matched_keywords"]) or "None")
                if match_res["recommendations"]:
                    st.error(f"**Missing Skills:** {', '.join(match_res['recommendations']['missing_skills'])}")
                    st.write(match_res["recommendations"]["advice"])

            with mc2:
                jd_skills_set = set(extract_skills(jd_text))
                all_skills = sorted(list(set(skills) | jd_skills_set))
                if len(all_skills) >= 3:
                    res_scores = [100 if s in skills else 0 for s in all_skills]
                    jd_scores = [100 if s in jd_skills_set else 0 for s in all_skills]
                    angles = np.linspace(0, 2 * np.pi, len(all_skills), endpoint=False).tolist()
                    res_scores += res_scores[:1]
                    jd_scores += jd_scores[:1]
                    angles += angles[:1]

                    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
                    ax.plot(angles, res_scores, color="blue", linewidth=2, label="Resume")
                    ax.fill(angles, res_scores, color="blue", alpha=0.25)
                    ax.plot(angles, jd_scores, color="red", linewidth=2, label="Job Description")
                    ax.fill(angles, jd_scores, color="red", alpha=0.25)
                    ax.set_theta_offset(np.pi / 2)
                    ax.set_theta_direction(-1)
                    ax.set_thetagrids(np.degrees(angles[:-1]), all_skills)
                    ax.set_ylim(0, 100)
                    ax.set_yticklabels([])
                    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
                    st.pyplot(fig)
                else:
                    st.info("Add more technical skills in the JD to render the radar chart.")

            st.subheader("Top JD Keyword Gap Analysis")
            comp = compare_keyword_density(resume_text, jd_text, top_n=10)
            st.dataframe(comp, use_container_width=True)
        else:
            st.warning("Paste a job description above to run skill gap analysis.")

    with tab3:
        rc1, rc2 = st.columns(2)
        with rc1:
            st.subheader("Job Role Prediction Confidence")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            roles = list(role_scores.keys())
            probs = list(role_scores.values())
            bars = ax2.bar(roles, probs, color="#4F8BF9")
            ax2.set_ylim(0, 1.05)
            ax2.set_ylabel("Confidence Score")
            for bar, score in zip(bars, probs):
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f"{score:.2f}", ha="center")
            st.pyplot(fig2)

        with rc2:
            st.subheader("Suggested Interview Questions")
            jd_kw = jd_text.lower().split() if jd_text else []
            questions = generate_interview_questions(skills, jd_kw)
            for idx, q in enumerate(questions, 1):
                st.markdown(f"**{idx}.** {q}")

    with tab4:
        if not openai_api_key:
            st.warning("Enter your OpenAI API Key in the sidebar to generate AI summaries and tailored feedback.")
        else:
            if st.button("✨ Generate AI Summary & Deep Critique"):
                with st.spinner("Analyzing resume with OpenAI..."):
                    summary = generate_resume_summary(
                        resume_text, model="gpt-4o-mini", api_key=openai_api_key
                    )
                    st.subheader("AI Executive Summary")
                    st.write(summary)

                    if jd_text.strip():
                        ai_feedback.client = OpenAI(api_key=openai_api_key)
                        critique = ai_feedback.get_ai_resume_feedback(resume_text, jd_text)
                        st.subheader("AI Hiring Expert Critique")
                        st.write(critique)

    with tab5:
        st.text_area("Extracted Resume Text", value=resume_text, height=350)
else:
    st.info("👆 Upload a PDF or DOCX resume to get started.")