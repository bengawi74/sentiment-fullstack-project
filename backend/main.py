from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    YouTubeAnalyzeRequest,
    YouTubeAnalyzeResponse,
    CommentSentiment,
    AmazonAnalyzeRequest,
    AmazonAnalyzeResponse,
)
from .model_loader import SentimentModel
from .youtube_client import extract_video_id, fetch_youtube_comments
from .amazon_client import fetch_amazon_reviews


class HealthResponse(BaseModel):
    """Response model for API health check."""
    status: str
    message: str


# -------------------------------------------------
# FastAPI app + load sentiment model once
# -------------------------------------------------
app = FastAPI(
    title="Sentiment Fullstack API",
    description="Backend API for product review sentiment project.",
    version="0.2.0",
)

# DistilBERT sentiment model (loaded once)
sentiment_model = SentimentModel()


# -------------------------------------------------
# Health endpoint
# -------------------------------------------------
@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return simple API health status."""
    return HealthResponse(status="ok", message="API is running")


# -------------------------------------------------
# Single-text sentiment endpoint
# -------------------------------------------------
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze sentiment of a single text using DistilBERT model."""
    label, score = sentiment_model.predict(request.text)

    return AnalyzeResponse(
        label=label,
        score=score,
        model=sentiment_model.model_name,
    )


# -------------------------------------------------
# YouTube comments endpoint
# -------------------------------------------------
@app.post("/youtube/analyze", response_model=YouTubeAnalyzeResponse)
def analyze_youtube_comments(request: YouTubeAnalyzeRequest) -> YouTubeAnalyzeResponse:
    """
    Fetch comments from a YouTube video and analyze their sentiment.

    Uses the helper functions in youtube_client.py:
    - extract_video_id(url) -> video_id
    - fetch_youtube_comments(video_id, max_comments) -> List[str]
    """
    video_id = extract_video_id(request.url)
    comments = fetch_youtube_comments(video_id, request.max_comments)

    if not comments:
        return YouTubeAnalyzeResponse(
            video_id=video_id,
            total_fetched=0,
            comments=[],
        )

    results: List[CommentSentiment] = []
    for text in comments:
        label, score = sentiment_model.predict(text)
        results.append(
            CommentSentiment(
                text=text,
                label=label,
                score=score,
            )
        )

    return YouTubeAnalyzeResponse(
        video_id=video_id,
        total_fetched=len(results),
        comments=results,
    )


# -------------------------------------------------
# Amazon reviews endpoint
# -------------------------------------------------
@app.post("/amazon/analyze", response_model=AmazonAnalyzeResponse)
def analyze_amazon_reviews(request: AmazonAnalyzeRequest) -> AmazonAnalyzeResponse:
    """
    Fetch reviews from an Amazon product reviews page and analyze sentiment.

    Uses fetch_amazon_reviews(url, max_reviews) from amazon_client.py.
    If no reviews can be fetched (blocked, captcha, etc.), returns an
    empty but well-formed response.
    """
    product_title, reviews = fetch_amazon_reviews(
        request.url, max_reviews=request.max_reviews
    )

    # If nothing was fetched, return a graceful empty response
    if not reviews:
        return AmazonAnalyzeResponse(
            product_title=product_title or "Unknown Amazon Product",
            total_fetched=0,
            reviews=[],
        )

    results: List[CommentSentiment] = []
    for text in reviews:
        label, score = sentiment_model.predict(text)
        results.append(
            CommentSentiment(
                text=text,
                label=label,
                score=score,
            )
        )

    return AmazonAnalyzeResponse(
        product_title=product_title or "Unknown Amazon Product",
        total_fetched=len(results),
        reviews=results,
    )
