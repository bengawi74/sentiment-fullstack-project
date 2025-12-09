from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class SentimentModel:
    """Wrapper for the HuggingFace DistilBERT sentiment model."""

    def __init__(self) -> None:
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self._load_pipeline()

    def _load_pipeline(self) -> None:
        """Load tokenizer + model into a HuggingFace pipeline."""
        self.pipe = pipeline(
            "sentiment-analysis",
            model=self.model_name,
            tokenizer=self.model_name
        )

    def predict(self, text: str) -> tuple[str, float]:
        """Predict sentiment for a given text.

        Args:
            text (str): Input comment or review.

        Returns:
            tuple[str, float]: Label and score.
        """
        result = self.pipe(text)[0]
        return result["label"].lower(), float(result["score"])
