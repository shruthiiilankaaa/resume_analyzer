# 📄 AI Resume Analyzer & Job Description Matcher

An end-to-end Python NLP and AI-powered application that parses resumes (`.pdf` and `.docx`), evaluates ATS compatibility, matches candidate profiles against job descriptions, predicts best-fit job roles, estimates salary ranges, generates tailored interview questions, and provides AI-driven improvement feedback.

---

## ✨ Features

* **Resume Parsing (`parser.py`, `extractor.py`, `analyze_resume.py`):** Extracts raw text, candidate name (via `spaCy` NER), email, phone number, education history, and technical skills from PDF and DOCX files.
* **Job Description Matching (`jd_matcher.py`, `matcher.py`, `resume_jd_analyzer.py`):** Compares resume skills and keywords against a target job description, computes a **Fit Score (%)**, identifies missing skills, and provides actionable recommendations.
* **ATS Compatibility Checker (`ats_checker.py`):** Evaluates resumes out of 100 based on standard section presence (`Education`, `Experience`, `Projects`, `Skills`, `Achievements`, `Certifications`), professional profile links (GitHub, LinkedIn, Portfolio), and optimal word count (300–1000 words).
* **Heuristic & AI Feedback (`heuristic_feedback.py`, `ai_feedback.py`, `summary_generator.py`):**
  * Rule-based structural checks (word count, summary presence, contact details).
  * OpenAI (`gpt-3.5-turbo`) powered candidate fit analysis, strengths/weaknesses breakdown, improvement tips, and 3–4 line executive summary generation.
* **Career & Role Insights (`role_classifier.py`, `salary_estimator.py`, `soft_skills.py`, `interview_questions.py`):**
  * Predicts best-fit technical role (`SDE`, `Data Scientist`, `DevOps`) with confidence scores.
  * Estimates candidate seniority level (`Junior`, `Mid-level`, `Senior`) and approximate annual salary based on extracted experience duration and premium skills.
  * Detects soft skills and generates tailored technical interview questions.
* **Readability & Keyword Analytics (`extra_features.py`):** Computes Flesch Reading Ease score, keyword density percentages, and resume-vs-JD keyword gap analysis.
* **Visualizations (`visualization.py`, `ml_visualization.py`):** Generates Skill Match Radar Charts, Keyword Density Bar Charts, and PyTorch-backed Job Role Prediction Confidence Charts.

---

## 📁 Project Structure

```text
resume_analyzer_py-main/
├── app.py                      # Streamlit web application (for cloud deployment)
├── requirements.txt            # Python dependencies
├── packages.txt                # System-level dependencies for Streamlit Cloud
├── full_analysis.py            # Main CLI orchestrator running all analysis modules
├── analyze_resume.py           # Core PDF/DOCX text & entity extraction
├── parser.py                   # Standalone resume parser saving to extracted_resume.txt
├── extractor.py                # spaCy & regex candidate info extractor
├── jd_matcher.py               # Keyword & skill matcher against job descriptions
├── matcher.py                  # Line/comma-separated JD skill matcher
├── resume_jd_analyzer.py       # Combined JD matching + heuristic feedback CLI
├── ats_checker.py              # 100-point ATS compatibility scorer
├── heuristic_feedback.py       # Rule-based resume feedback generator
├── ai_feedback.py              # OpenAI GPT-based deep resume vs. JD critique
├── summary_generator.py        # OpenAI GPT-based 3-4 line professional summary
├── role_classifier.py          # Rule-based job role & confidence scorer
├── salary_estimator.py         # Experience & skill-based compensation estimator
├── soft_skills.py              # Soft skill regex detector
├── interview_questions.py      # Skill-mapped technical interview question generator
├── extra_features.py           # Word count, Flesch readability, keyword density & experience parser
├── visualization.py            # Matplotlib radar & keyword density plots
├── ml_visualization.py         # Matplotlib + PyTorch role confidence bar chart
├── test_visualization.py       # Unit test for radar visualization
├── test_ml_visualization.py    # Unit test for ML confidence visualization
├── test_visuals.py             # Combined visualization test script
├── jd_sample.txt               # Sample job description text file
├── jd.pdf                      # Sample job description PDF
├── resume.pdf                  # Sample resume PDF
└── extracted_resume.txt        # Sample extracted resume text
```

---

## 🚀 Local Installation & CLI Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/resume_analyzer_py.git
   cd resume_analyzer_py
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies & NLP models:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('stopwords')"
   ```

4. **Configure environment variables (optional, for OpenAI features):**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key
   ```

5. **Run the full CLI analysis:**
   ```bash
   python full_analysis.py
   ```

---

## 🌐 Deploying to Streamlit Community Cloud

Because this repository is originally structured as a CLI toolkit, deploying it to Streamlit requires adding `app.py`, `requirements.txt`, and `packages.txt` to your GitHub repository root:

1. Push your code (including `app.py` and `requirements.txt`) to a public or private GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **New app**, select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. *(Optional)* Under **Advanced settings → Secrets**, add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "sk-your-openai-api-key"
   ```
5. Click **Deploy!**