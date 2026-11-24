# test_visuals.py
from ml_visualization import plot_role_prediction_confidence
from visualization import plot_skill_match_radar

import torch

# Fake data
roles = ['SDE', 'Data Scientist', 'DevOps']
probs = torch.tensor([0.7, 0.4, 0.1])

resume_skills = ['Python', 'Git', 'Django', 'REST']
jd_keywords = ['python', 'django', 'flask', 'aws', 'git']

# Run both plots
plot_role_prediction_confidence(roles, probs)
plot_skill_match_radar(resume_skills, jd_keywords)
