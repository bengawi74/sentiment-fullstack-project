import os
import re
from typing import List

import requests


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from a URL.

    Args:
        url (str): Full YouTube video URL.

    Returns:
        str: Extracted video ID.

    Raises:
        ValueError: If no video ID can be found.
    """
    # Common patterns: https://www.youtube.com/watch?v=VIDEO_ID or youtu.be/VIDEO_ID
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Could not extract video ID from URL.")


def fetch_youtube_comments(video_id: str, max_comments: int = 50) -> List[str]:
    """Fetch top-level comments from a YouTube video using the Data API.

    Args:
        video_id (str): YouTube video ID.
        max_comments (int): Maximum number of comments to fetch.

    Returns:
        List[str]: List of comment texts.

    Raises:
        RuntimeError: If the API key is missing or the API call fails.
    """
    if not YOUTUBE_API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY environment variable is not set.")

    comments: List[str] = []
    page_token = None

    while len(comments) < max_comments:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "key": YOUTUBE_API_KEY,
            "maxResults": 50,
            "textFormat": "plainText",
        }
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            "https://www.googleapis.com/youtube/v3/commentThreads",
            params=params,
            timeout=10,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"YouTube API error: {response.status_code} {response.text}"
            )

        data = response.json()
        items = data.get("items", [])
        for item in items:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            text = snippet.get("textDisplay", "")
            if text:
                comments.append(text)
                if len(comments) >= max_comments:
                    break

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return comments
