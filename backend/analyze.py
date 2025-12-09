import random
from typing import Tuple


def simple_sentiment(text: str) -> Tuple[str, float]:
    """Temporary sentiment predictor until the ML model is integrated.

    Args:
        text (str): Input review text.

    Returns:
        Tuple[str, float]: A simple label and simulated confidence value.
    """
    labels = ["positive", "neutral", "negative"]
    label = random.choice(labels)
    score = round(random.uniform(0.50, 0.99), 3)
    return label, score
