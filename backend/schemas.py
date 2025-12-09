from typing import List

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Model representing the input for single-text sentiment analysis."""
    text: str = Field(..., description="The review or comment text to analyze.")


class AnalyzeResponse(BaseModel):
    """Model representing the output from sentiment analysis."""
    label: str = Field(..., description="Predicted sentiment label.")
    score: float = Field(..., description="Confidence score of the prediction.")
    model: str = Field(..., description="Name of the model used.")


# ---------- YouTube models ----------

class YouTubeAnalyzeRequest(BaseModel):
    """Request model for analyzing a YouTube video's comments."""
    url: str = Field(..., description="Full YouTube video URL.")
    max_comments: int = Field(
        50,
        ge=1,
        le=500,
        description="Maximum number of comments to fetch and analyze.",
    )


class CommentSentiment(BaseModel):
    """Sentiment result for a single text item (comment/review)."""
    text: str
    label: str
    score: float


class YouTubeAnalyzeResponse(BaseModel):
    """Response model for YouTube comments sentiment analysis."""
    video_id: str
    total_fetched: int
    comments: List[CommentSentiment]


# ---------- Amazon models ----------

class AmazonAnalyzeRequest(BaseModel):
    """Request model for analyzing Amazon product reviews."""
    url: str = Field(..., description="Amazon product or reviews URL.")
    max_reviews: int = Field(
        50,
        ge=1,
        le=200,
        description="Maximum number of reviews to fetch and analyze.",
    )


class AmazonAnalyzeResponse(BaseModel):
    """Response model for Amazon reviews sentiment analysis."""
    product_title: str | None
    total_fetched: int
    reviews: List[CommentSentiment]
