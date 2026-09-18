import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(".env"), override=True)


INPUT_FILE = Path("data/transformed/clean_youtube_data.json")


def get_db_connection():
    """Create a PostgreSQL database connection."""

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_transformed_data():
    """Load transformed JSON data."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Transformed data not found: {INPUT_FILE}"
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def create_tables(connection):
    """Create database tables if they don't already exist."""

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            channel_id VARCHAR(50) PRIMARY KEY,
            channel_name VARCHAR(255) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id VARCHAR(50) PRIMARY KEY,
            channel_id VARCHAR(50) NOT NULL,
            video_title TEXT NOT NULL,
            published_at TIMESTAMP,
            category_id INTEGER,
            duration VARCHAR(50),
            views BIGINT DEFAULT 0,
            likes BIGINT DEFAULT 0,
            comments BIGINT DEFAULT 0,
            engagement_rate DECIMAL(10, 2),

            CONSTRAINT fk_videos_channel
                FOREIGN KEY (channel_id)
                REFERENCES channels(channel_id)
        );
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_videos_channel_id
        ON videos(channel_id);
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_videos_published_at
        ON videos(published_at);
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_videos_views
        ON videos(views);
    """)

    connection.commit()
    cursor.close()


def load_channel(connection, channel_id, channel_name):
    """Insert or update channel information."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO channels (
            channel_id,
            channel_name
        )
        VALUES (%s, %s)
        ON CONFLICT (channel_id)
        DO UPDATE SET
            channel_name = EXCLUDED.channel_name;
    """, (channel_id, channel_name))

    connection.commit()
    cursor.close()


def load_videos(connection, videos):
    """Insert or update video records."""

    cursor = connection.cursor()

    for video in videos:

        cursor.execute("""
            INSERT INTO videos (
                video_id,
                channel_id,
                video_title,
                published_at,
                category_id,
                duration,
                views,
                likes,
                comments,
                engagement_rate
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )

            ON CONFLICT (video_id)
            DO UPDATE SET
                video_title = EXCLUDED.video_title,
                views = EXCLUDED.views,
                likes = EXCLUDED.likes,
                comments = EXCLUDED.comments,
                engagement_rate = EXCLUDED.engagement_rate;
        """, (
            video["video_id"],
            video["channel_id"],
            video["video_title"],
            video["published_at"],
            video["category_id"],
            video["duration"],
            video["views"],
            video["likes"],
            video["comments"],
            video["engagement_rate"]
        ))

    connection.commit()
    cursor.close()


def main():

    print("Starting data loading...")

    data = load_transformed_data()

    videos = data.get("videos", [])

    if not videos:
        raise ValueError("No transformed video data found.")

    # Get channel information from first video
    channel_id = videos[0]["channel_id"]
    channel_name = videos[0]["channel_name"]

    connection = None

    try:

        connection = get_db_connection()

        print("Connected to PostgreSQL.")

        create_tables(connection)

        print("Database tables ready.")

        load_channel(
            connection,
            channel_id,
            channel_name
        )

        print("Channel loaded successfully.")

        load_videos(
            connection,
            videos
        )

        print(
            f"Loaded {len(videos)} videos successfully."
        )

    except Exception as error:

        if connection:
            connection.rollback()

        print(f"Loading failed: {error}")
        raise

    finally:

        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()