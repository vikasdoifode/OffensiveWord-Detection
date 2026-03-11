"""
YouTube Chat Fetcher Utility

Fetches comments from YouTube live chat or video comments.

Note: For a production system, you would need a valid YouTube Data API key.
This module provides both real API integration and a simulation mode
for testing/demonstration purposes.
"""

import re
import httpx
import os


def _get_api_key() -> str:
    """Get YouTube API key at runtime (not import time)."""
    return os.getenv("YOUTUBE_API_KEY", "")


def extract_video_id(url: str) -> str | None:
    """Extract video ID from various YouTube URL formats."""
    # Clean the input — strip whitespace, newlines, quotes
    url = url.strip().strip('"').strip("'")

    patterns = [
        # Standard watch URL: youtube.com/watch?v=VIDEO_ID
        r"(?:youtube\.com|youtube-nocookie\.com)/watch\?.*v=([a-zA-Z0-9_-]{11})",
        # Shortened URL: youtu.be/VIDEO_ID
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        # Embed URL: youtube.com/embed/VIDEO_ID
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})",
        # Live URL: youtube.com/live/VIDEO_ID
        r"youtube\.com/live/([a-zA-Z0-9_-]{11})",
        # Shorts URL: youtube.com/shorts/VIDEO_ID
        r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
        # /v/ URL: youtube.com/v/VIDEO_ID
        r"youtube\.com/v/([a-zA-Z0-9_-]{11})",
        # Live chat popup URL: youtube.com/live_chat?v=VIDEO_ID
        r"youtube\.com/live_chat\?.*v=([a-zA-Z0-9_-]{11})",
        # Generic fallback: v= or /v/ anywhere
        r"(?:v=|/v/)([a-zA-Z0-9_-]{11})",
        # Bare video ID (exactly 11 chars)
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


async def fetch_youtube_comments(url: str) -> list[dict]:
    """
    Fetch comments from a YouTube video.

    If YOUTUBE_API_KEY is set, uses the real YouTube Data API.
    Otherwise, returns simulated comments for demonstration.

    Args:
        url: YouTube video URL or live chat URL

    Returns:
        List of dicts with 'user' and 'comment' keys
    """
    video_id = extract_video_id(url)

    if not video_id:
        # Try to extract from live chat URL (legacy pattern)
        match = re.search(r"live_chat.*v=([a-zA-Z0-9_-]{11})", url)
        if match:
            video_id = match.group(1)

    api_key = _get_api_key()
    print(f"[YouTube] Received URL: '{url}'")
    print(f"[YouTube] Video ID: {video_id}")
    print(f"[YouTube] API Key present: {'YES' if api_key else 'NO'}")

    if not video_id:
        print("[YouTube] Could not extract video ID from URL, using simulated data")
        return _get_simulated_comments(), "simulated"

    if not api_key:
        print("[YouTube] No API key configured, using simulated data")
        return _get_simulated_comments(), "simulated"

    comments = await _fetch_real_comments(video_id, api_key)
    if comments:
        return comments, "youtube_api"
    return _get_simulated_comments(), "simulated_fallback"


async def _fetch_real_comments(video_id: str, api_key: str) -> list[dict]:
    """Fetch real comments using YouTube Data API v3."""
    comments = []
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": 50,
        "order": "relevance",
        "textFormat": "plainText",
    }

    try:
        async with httpx.AsyncClient() as client:
            print(f"[YouTube] Fetching comments for video: {video_id}")
            response = await client.get(url, params=params, timeout=15.0)
            print(f"[YouTube] API Response Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                print(f"[YouTube] Fetched {len(items)} comments from YouTube API")

                if not items:
                    print("[YouTube] API returned 0 items — video may have comments disabled")
                    return _get_simulated_comments()

                for item in items:
                    snippet = item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        "user": snippet.get("authorDisplayName", "Unknown"),
                        "comment": snippet.get("textDisplay", ""),
                    })
            elif response.status_code == 403:
                error_data = response.json()
                error_reason = error_data.get("error", {}).get("errors", [{}])[0].get("reason", "unknown")
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                print(f"[YouTube] API 403 Forbidden — Reason: {error_reason}")
                print(f"[YouTube] Error Message: {error_message}")

                if error_reason == "commentsDisabled":
                    print("[YouTube] Comments are disabled on this video")
                elif error_reason in ("quotaExceeded", "dailyLimitExceeded"):
                    print("[YouTube] API quota exceeded — try again tomorrow or use a new key")
                elif error_reason == "forbidden":
                    print("[YouTube] YouTube Data API v3 may not be enabled. Go to:")
                    print("         https://console.cloud.google.com/apis/library/youtube.googleapis.com")
                    print("         and click 'Enable'")

                comments = _get_simulated_comments()
            elif response.status_code == 400:
                error_data = response.json()
                print(f"[YouTube] API 400 Bad Request: {error_data}")
                comments = _get_simulated_comments()
            else:
                print(f"[YouTube] API error: {response.status_code} - {response.text}")
                comments = _get_simulated_comments()
    except httpx.ConnectError as e:
        print(f"[YouTube] Connection error (no internet?): {e}")
        comments = _get_simulated_comments()
    except httpx.TimeoutException as e:
        print(f"[YouTube] Request timed out: {e}")
        comments = _get_simulated_comments()
    except Exception as e:
        print(f"[YouTube] Unexpected error: {type(e).__name__}: {e}")
        comments = _get_simulated_comments()

    return comments


def _get_simulated_comments() -> list[dict]:
    """
    Return simulated YouTube chat comments for demonstration.
    Includes a mix of safe and offensive comments to showcase detection.
    """
    return [
        {"user": "GamerPro99", "comment": "This stream is amazing! Love the content!"},
        {"user": "TrollMaster", "comment": "You are so stup1d, why do you even try?"},
        {"user": "NiceViewer", "comment": "Great gameplay, keep it up!"},
        {"user": "Hater_42", "comment": "What an id10t, learn to play the game"},
        {"user": "FanGirl", "comment": "You're my favorite streamer!"},
        {"user": "Toxic_User", "comment": "This is complete bullshit, you suck"},
        {"user": "Chill_Dude", "comment": "Wow nice move there! Well played!"},
        {"user": "AngryKid", "comment": "You're such a l0ser and a m0r0n"},
        {"user": "SupportiveFan", "comment": "Don't listen to the haters, you're great!"},
        {"user": "ObfuscatedTroll", "comment": "You are a f00l and @$$hole"},
        {"user": "HappyViewer", "comment": "This is the best stream today!"},
        {"user": "SneakyHater", "comment": "s.t.u.p.i.d people like you should quit"},
        {"user": "RegularUser", "comment": "Can you play that level again?"},
        {"user": "BadMouth", "comment": "What a damn idiot, go away"},
        {"user": "PositiveVibes", "comment": "Sending love from Brazil! 🇧🇷"},
        {"user": "SymbolUser", "comment": "You are $tup!d and should leave"},
    ]
