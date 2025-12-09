import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000"


def call_analyze_api(text: str) -> dict:
    """Send text to backend /analyze endpoint."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"text": text},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def call_youtube_api(url: str, limit: int) -> dict:
    """Send YouTube URL to backend /youtube/analyze endpoint."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/youtube/analyze",
            json={"url": url, "max_comments": limit},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def call_amazon_api(url: str, limit: int) -> dict:
    """Send Amazon product URL to backend /amazon/analyze endpoint."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/amazon/analyze",
            json={"url": url, "max_reviews": limit},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}


def render_single_text_section() -> None:
    """Render UI for single text sentiment analysis."""
    st.subheader("Analyze a single review/comment")

    user_text = st.text_area("Enter text to analyze:", height=150)

    if st.button("Analyze Sentiment"):
        if not user_text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Analyzing..."):
                result = call_analyze_api(user_text)

            st.write("### Result:")
            st.json(result)


def render_youtube_section() -> None:
    """Render UI for YouTube comments sentiment analysis."""
    st.subheader("Analyze YouTube video comments")

    url = st.text_input(
        "YouTube video URL:",
        placeholder="https://www.youtube.com/watch?v=...",
    )

    limit = st.slider(
        "Maximum number of comments to analyze:",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
    )

    if st.button("Analyze YouTube"):
        if not url.strip():
            st.warning("Please enter a YouTube video URL.")
        else:
            with st.spinner("Fetching comments and analyzing sentiment..."):
                result = call_youtube_api(url, limit)

            if "error" in result:
                st.error(result["error"])
                return

            df = pd.DataFrame(result.get("comments", []))
            if df.empty:
                st.info("No comments returned.")
                return

            st.success(
                f"Analyzed {result.get('total_fetched', 0)} comments from video ID: "
                f"{result.get('video_id', '')}"
            )

            st.write("### Sample of analyzed comments")
            st.dataframe(df.head(50), use_container_width=True)

            st.write("### Sentiment distribution")
            st.bar_chart(df["label"].value_counts())


def render_amazon_section() -> None:
    """Render UI for Amazon product reviews sentiment analysis."""
    st.subheader("Analyze Amazon product reviews")

    url = st.text_input(
        "Amazon product URL:",
        placeholder="https://www.amazon.ca/...",
    )

    limit = st.slider(
        "Maximum number of reviews to analyze:",
        min_value=10,
        max_value=100,
        value=20,
        step=10,
    )

    if st.button("Analyze Amazon"):
        if not url.strip():
            st.warning("Please enter an Amazon URL.")
        else:
            with st.spinner("Fetching reviews and analyzing sentiment..."):
                result = call_amazon_api(url, limit)

            if "error" in result:
                st.error(result["error"])
                return

            product_title = result.get("product_title") or "Unknown product"
            st.success(
                f"Analyzed {result.get('total_fetched', 0)} reviews for: {product_title}"
            )

            df = pd.DataFrame(result.get("reviews", []))
            if df.empty:
                st.info("No reviews returned.")
                return

            st.write("### Sample of analyzed reviews")
            st.dataframe(df.head(50), use_container_width=True)

            st.write("### Sentiment distribution")
            st.bar_chart(df["label"].value_counts())


def main() -> None:
    """Render the main Streamlit app layout."""
    st.title("Sentiment Fullstack Dashboard")

    render_single_text_section()
    st.markdown("---")
    render_youtube_section()
    st.markdown("---")
    render_amazon_section()


if __name__ == "__main__":
    main()
