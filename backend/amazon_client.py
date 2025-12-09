from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

# Base directory and local fallback data file
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sample_amazon_reviews.csv"

# Headers to look more like a browser (helps a bit with blocking)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _to_reviews_url(url: str) -> str:
    """Convert a /dp/ URL into a /product-reviews/ URL on amazon.ca."""
    if "product-reviews" in url:
        return url

    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if not match:
        return url

    asin = match.group(1)
    return f"https://www.amazon.ca/product-reviews/{asin}"


def _scrape_amazon_reviews(url: str, max_reviews: int) -> Tuple[str | None, List[str]]:
    """Try to scrape reviews directly from Amazon with a short timeout."""
    reviews_url = _to_reviews_url(url)

    try:
        # Short timeout so we never hang the API for too long
        resp = requests.get(reviews_url, headers=HEADERS, timeout=8)
    except Exception:
        return None, []

    if resp.status_code != 200:
        # Blocked / captcha / slow / etc.
        return None, []

    soup = BeautifulSoup(resp.text, "lxml")

    # Product title (may or may not be present on reviews page)
    title_tag = soup.select_one("#productTitle")
    product_title = title_tag.get_text(strip=True) if title_tag else None

    # Review bodies
    review_spans = soup.select('span[data-hook="review-body"]')

    reviews: List[str] = []
    for span in review_spans:
        text = span.get_text(" ", strip=True)
        if text:
            reviews.append(text)
        if len(reviews) >= max_reviews:
            break

    return product_title, reviews


def _load_local_reviews(max_reviews: int) -> Tuple[str | None, List[str]]:
    """Fallback: load reviews from a local CSV so the demo always works."""
    if not DATA_FILE.exists():
        return None, []

    reviews: List[str] = []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = (row.get("text") or "").strip()
                if text:
                    reviews.append(text)
                if len(reviews) >= max_reviews:
                    break
    except Exception:
        return None, []

    if not reviews:
        return None, []

    return "Sample Amazon Product (local dataset)", reviews


def fetch_amazon_reviews(url: str, max_reviews: int = 50) -> Tuple[str | None, List[str]]:
    """
    Main function used by FastAPI.

    1. Try to scrape live Amazon reviews with a fast timeout.
    2. If that fails or returns nothing, fall back to the local CSV.
    """
    title, reviews = _scrape_amazon_reviews(url, max_reviews=max_reviews)
    if reviews:
        return title, reviews

    # Fallback: local synthetic dataset
    return _load_local_reviews(max_reviews)
