import json
from pathlib import Path


INPUT_FILE = Path("data/raw/youtube_raw.json")


def load_raw_data():
    """Load the raw YouTube data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {INPUT_FILE}"
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_videos(videos):
    """Validate YouTube video records."""

    required_fields = [
        "id",
        "snippet",
        "statistics"
    ]

    valid_videos = []
    invalid_videos = []

    seen_video_ids = set()

    for video in videos:

        video_id = video.get("id")

        # Check required top-level fields
        missing_fields = [
            field for field in required_fields
            if field not in video
        ]

        if missing_fields:
            invalid_videos.append({
                "video_id": video_id,
                "reason": f"Missing fields: {missing_fields}"
            })
            continue

        # Check duplicate video IDs
        if video_id in seen_video_ids:
            invalid_videos.append({
                "video_id": video_id,
                "reason": "Duplicate video ID"
            })
            continue

        seen_video_ids.add(video_id)

        statistics = video.get("statistics", {})

        # Convert numeric fields safely
        try:
            views = int(statistics.get("viewCount", 0))
            likes = int(statistics.get("likeCount", 0))
            comments = int(statistics.get("commentCount", 0))
        except (ValueError, TypeError):
            invalid_videos.append({
                "video_id": video_id,
                "reason": "Invalid numeric statistics"
            })
            continue

        # Check for negative values
        if views < 0 or likes < 0 or comments < 0:
            invalid_videos.append({
                "video_id": video_id,
                "reason": "Negative statistics"
            })
            continue

        valid_videos.append(video)

    return valid_videos, invalid_videos


def save_validation_report(valid_videos, invalid_videos,channel):
    """Save validation results."""

    output_dir = Path("data/validated")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "validated_youtube_data.json"

    result = {
        "valid_records": len(valid_videos),
        "invalid_records": len(invalid_videos),
        "channel": channel,
        "videos": valid_videos,
        "invalid_details": invalid_videos
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(f"Validated data saved to: {output_file}")


def main():
    print("Starting data validation...")

    raw_data = load_raw_data()

    videos = raw_data.get("videos", [])
    channel = raw_data.get("channel", {})

    print(f"Records received: {len(videos)}")

    valid_videos, invalid_videos = validate_videos(videos)

    print(f"Valid records: {len(valid_videos)}")
    print(f"Invalid records: {len(invalid_videos)}")

    if invalid_videos:
        print("\nValidation issues:")

        for item in invalid_videos[:10]:
            print(
                f"- Video {item['video_id']}: "
                f"{item['reason']}"
            )

    save_validation_report(
        valid_videos,
        invalid_videos,
        channel
    )

    print("\nValidation completed successfully.")


if __name__ == "__main__":
    main()