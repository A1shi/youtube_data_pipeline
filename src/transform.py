import json
from pathlib import Path
from datetime import datetime


INPUT_FILE = Path("data/validated/validated_youtube_data.json")
OUTPUT_FILE = Path("data/transformed/clean_youtube_data.json")


def load_validated_data():
    """Load validated YouTube data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Validated data not found: {INPUT_FILE}"
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_engagement_rate(views, likes, comments):
    """Calculate video engagement rate."""

    if views == 0:
        return 0.0

    return round(
        ((likes + comments) / views) * 100,
        2
    )


def transform_video(video, channel):
    """Convert one raw YouTube video into a clean record."""

    snippet = video.get("snippet", {})
    statistics = video.get("statistics", {})
    content_details = video.get("contentDetails", {})

    video_id = video.get("id")

    views = int(statistics.get("viewCount", 0))
    likes = int(statistics.get("likeCount", 0))
    comments = int(statistics.get("commentCount", 0))

    transformed_video = {
        "video_id": video_id,
        "channel_id": channel.get("id"),
        "channel_name": channel.get("snippet", {}).get("title"),
        "video_title": snippet.get("title"),
        "published_at": snippet.get("publishedAt"),
        "category_id": snippet.get("categoryId"),
        "duration": content_details.get("duration"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "engagement_rate": calculate_engagement_rate(
            views,
            likes,
            comments
        )
    }

    return transformed_video


def transform_data(data):
    """Transform all validated videos."""

    channel = data.get("channel", {})
    videos = data.get("videos", [])

    transformed_videos = []

    for video in videos:
        transformed_video = transform_video(
            video,
            channel
        )

        transformed_videos.append(transformed_video)

    return transformed_videos


def save_transformed_data(videos):
    """Save clean transformed data."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_data = {
        "record_count": len(videos),
        "transformed_at": datetime.now().isoformat(),
        "videos": videos
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output_data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Transformed data saved to: {OUTPUT_FILE}"
    )


def main():

    print("Starting data transformation...")

    data = load_validated_data()

    transformed_videos = transform_data(data)

    print(
        f"Records transformed: {len(transformed_videos)}"
    )

    save_transformed_data(transformed_videos)

    print("Transformation completed successfully.")


if __name__ == "__main__":
    main()