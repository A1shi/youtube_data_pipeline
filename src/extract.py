import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

BASE_URL = "https://www.googleapis.com/youtube/v3"


def validate_config():
    """Check that required environment variables are available."""

    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY is missing from .env")

    if not CHANNEL_ID:
        raise ValueError("YOUTUBE_CHANNEL_ID is missing from .env")


def get_channel_details():
    """Extract basic channel information."""

    url = f"{BASE_URL}/channels"

    params = {
        "part": "snippet,contentDetails,statistics",
        "id": CHANNEL_ID,
        "key": API_KEY,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not data.get("items"):
        raise ValueError("Channel not found. Check your CHANNEL_ID.")

    return data["items"][0]


def get_video_ids(upload_playlist_id):
    """Get video IDs from the channel's upload playlist."""

    url = f"{BASE_URL}/playlistItems"

    video_ids = []
    next_page_token = None

    while True:

        params = {
            "part": "contentDetails",
            "playlistId": upload_playlist_id,
            "maxResults": 50,
            "key": API_KEY,
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        for item in data.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            video_ids.append(video_id)

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids


def get_video_details(video_ids):
    """Extract video metadata and statistics."""

    if not video_ids:
        return []

    url = f"{BASE_URL}/videos"

    videos = []

    # YouTube API accepts up to 50 IDs per request
    for i in range(0, len(video_ids), 50):

        batch = video_ids[i:i + 50]

        params = {
            "part": "snippet,contentDetails,statistics",
            "id": ",".join(batch),
            "key": API_KEY,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        videos.extend(data.get("items", []))

    return videos


def save_raw_data(channel, videos):
    """Save raw extracted data for the next pipeline stages."""

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "youtube_raw.json"

    raw_data = {
        "channel": channel,
        "videos": videos
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, indent=2, ensure_ascii=False)

    print(f"Raw data saved to: {output_file}")


def extract_youtube_data():

    validate_config()

    print("Starting YouTube data extraction...")

    # Get channel information
    channel = get_channel_details()

    channel_name = channel["snippet"]["title"]

    print(f"Channel: {channel_name}")

    # Get upload playlist
    upload_playlist_id = (
        channel["contentDetails"]
        ["relatedPlaylists"]
        ["uploads"]
    )

    print("Finding uploaded videos...")

    video_ids = get_video_ids(upload_playlist_id)

    print(f"Found {len(video_ids)} videos.")

    # Get video information
    videos = get_video_details(video_ids)

    print(f"Extracted {len(videos)} video records.")

    # Save raw API response
    save_raw_data(channel, videos)

    return channel, videos


if __name__ == "__main__":
    extract_youtube_data()