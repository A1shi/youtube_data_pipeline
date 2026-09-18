-- ============================================================
-- YouTube Content Performance Analytics
-- ============================================================


-- 1. Top 10 videos by views
SELECT
    video_id,
    video_title,
    views
FROM videos
ORDER BY views DESC
LIMIT 10;


-- 2. Top 10 videos by engagement rate
SELECT
    video_id,
    video_title,
    views,
    likes,
    comments,
    engagement_rate
FROM videos
ORDER BY engagement_rate DESC
LIMIT 10;


-- 3. Average performance of the channel
SELECT
    COUNT(*) AS total_videos,
    ROUND(AVG(views), 2) AS avg_views,
    ROUND(AVG(likes), 2) AS avg_likes,
    ROUND(AVG(comments), 2) AS avg_comments,
    ROUND(AVG(engagement_rate), 2) AS avg_engagement_rate
FROM videos;


-- 4. Videos by year
SELECT
    EXTRACT(YEAR FROM published_at) AS publish_year,
    COUNT(*) AS video_count,
    SUM(views) AS total_views,
    ROUND(AVG(views), 2) AS avg_views
FROM videos
GROUP BY EXTRACT(YEAR FROM published_at)
ORDER BY publish_year;


-- 5. Highly engaging videos
SELECT
    video_title,
    views,
    likes,
    comments,
    engagement_rate,
    CASE
        WHEN engagement_rate >= 10 THEN 'Very High'
        WHEN engagement_rate >= 5 THEN 'High'
        WHEN engagement_rate >= 2 THEN 'Medium'
        ELSE 'Low'
    END AS engagement_category
FROM videos
ORDER BY engagement_rate DESC;


-- 6. Rank videos by views
SELECT
    video_title,
    views,
    RANK() OVER (ORDER BY views DESC) AS view_rank
FROM videos
ORDER BY view_rank
LIMIT 20;


-- 7. Top 3 videos within each year
WITH ranked_videos AS (
    SELECT
        video_title,
        published_at,
        views,
        EXTRACT(YEAR FROM published_at) AS publish_year,
        RANK() OVER (
            PARTITION BY EXTRACT(YEAR FROM published_at)
            ORDER BY views DESC
        ) AS yearly_rank
    FROM videos
)
SELECT
    publish_year,
    video_title,
    views,
    yearly_rank
FROM ranked_videos
WHERE yearly_rank <= 3
ORDER BY publish_year, yearly_rank;


-- 8. Videos with above-average views
WITH average_views AS (
    SELECT AVG(views) AS avg_views
    FROM videos
)
SELECT
    video_title,
    views
FROM videos
WHERE views > (SELECT avg_views FROM average_views)
ORDER BY views DESC;


-- 9. Most liked videos
SELECT
    video_title,
    views,
    likes,
    comments
FROM videos
ORDER BY likes DESC
LIMIT 10;


-- 10. Most commented videos
SELECT
    video_title,
    views,
    likes,
    comments
FROM videos
ORDER BY comments DESC
LIMIT 10;