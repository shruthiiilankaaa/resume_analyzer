import torch
from ml_visualization import plot_role_prediction_confidence

# Sample data
roles = ['SDE', 'Data Scientist', 'DevOps Engineer', 'QA Engineer']
# Example confidence scores as PyTorch tensor (values between 0 and 1)
confidence_scores = torch.tensor([0.75, 0.60, 0.40, 0.30])

# Call the plot function
plot_role_prediction_confidence(roles, confidence_scores)
