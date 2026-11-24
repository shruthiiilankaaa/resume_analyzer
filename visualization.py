import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import re


def plot_skill_match_radar(resume_skills, jd_keywords):
    """
    Radar chart comparing skill presence in resume and JD.
    Skills presence is binary (0 or 100%) for clarity.
    """
    all_skills = list(set(resume_skills) | set(jd_keywords))
    resume_scores = [100 if skill in resume_skills else 0 for skill in all_skills]
    jd_scores = [100 if skill in jd_keywords else 0 for skill in all_skills]

    labels = all_skills
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Close the radar chart
    resume_scores += resume_scores[:1]
    jd_scores += jd_scores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    ax.plot(angles, resume_scores, color='blue', linewidth=2, label='Resume Skills')
    ax.fill(angles, resume_scores, color='blue', alpha=0.25)

    ax.plot(angles, jd_scores, color='red', linewidth=2, label='JD Keywords')
    ax.fill(angles, jd_scores, color='red', alpha=0.25)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    ax.set_ylim(0, 100)
    ax.set_yticklabels([])  # Hide radial labels for clarity

    ax.set_title('Skill Match Radar Chart', size=20, y=1.05)
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.1))

    plt.tight_layout()
    plt.show()


def plot_keyword_density(resume_text, jd_text):
    """
    Bar chart showing frequency of JD keywords found in resume.
    """
    jd_keywords = jd_text.lower().split()
    resume_words = re.findall(r'\b\w+\b', resume_text.lower())

    resume_counter = Counter(resume_words)
    jd_counter = Counter(jd_keywords)

    keywords_in_resume = {k: resume_counter[k] for k in jd_counter if k in resume_counter}

    if not keywords_in_resume:
        print("No JD keywords found in resume for keyword density plot.")
        return

    keywords = list(keywords_in_resume.keys())
    counts = list(keywords_in_resume.values())

    plt.figure(figsize=(10, 6))
    plt.bar(keywords, counts, color='purple')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Frequency in Resume')
    plt.title('Keyword Density in Resume vs Job Description')
    plt.tight_layout()
    plt.show()
