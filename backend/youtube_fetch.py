# youtube_fetch.py
import os
import requests

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_top_videos(query: str, max_results: int = 5):
    """
    Fetch top YouTube videos for a given query.
    Requires YOUTUBE_API_KEY in environment.
    """
    if not YOUTUBE_KEY:
        raise RuntimeError("ERROR: Set YOUTUBE_API_KEY in your .env file")

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "key": YOUTUBE_KEY,
        "maxResults": max_results,
    }

    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()

    items = response.json().get("items", [])

    videos = []
    for it in items:
        video_id = it["id"]["videoId"]
        videos.append({
            "title": it["snippet"]["title"],
            "channel": it["snippet"]["channelTitle"],
            "thumbnail": it["snippet"]["thumbnails"]["default"]["url"],
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return videos


if __name__ == "__main__":
    print(fetch_top_videos("sliding window leetcode"))
