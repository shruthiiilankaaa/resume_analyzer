import matplotlib.pyplot as plt
import torch


def plot_role_prediction_confidence(roles, probs: torch.Tensor):
    """
    Bar chart of job role prediction confidence scores.

    Args:
        roles (list[str]): Job role labels.
        probs (torch.Tensor): Confidence scores, floats between 0 and 1.
    """
    plt.figure(figsize=(9, 5))
    probs_np = probs.numpy()

    bars = plt.bar(roles, probs_np, color='skyblue')
    plt.ylim(0, 1)
    plt.ylabel('Confidence Score')
    plt.title('Job Role Prediction Confidence')
    plt.xticks(rotation=45, ha='right')

    for bar, score in zip(bars, probs_np):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{score:.2f}",
            ha='center',
            va='bottom',
            fontsize=10,
        )

    plt.tight_layout()
    plt.show()
