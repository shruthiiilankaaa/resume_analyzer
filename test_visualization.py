import torch
from visualization import plot_skill_match_radar

resume_skills = ['python', 'sql', 'docker', 'aws']
jd_keywords = ['python', 'java', 'sql', 'kubernetes', 'docker']

plot_skill_match_radar(resume_skills, jd_keywords)
