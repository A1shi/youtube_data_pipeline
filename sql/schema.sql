CREATE TABLE IF NOT EXISTS channels (
    channel_id VARCHAR(50) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL
);


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


CREATE INDEX IF NOT EXISTS idx_videos_channel_id
ON videos(channel_id);


CREATE INDEX IF NOT EXISTS idx_videos_published_at
ON videos(published_at);


CREATE INDEX IF NOT EXISTS idx_videos_views
ON videos(views);