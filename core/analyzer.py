import math
from datetime import datetime

AVG_TIME_PER_VIDEO_SEC = 3.81
MAX_RESULTS = 20


def niche_opportunity_score(avg_seo, avg_views, avg_duration_sec, max_possible_views=50000):
    log_views = math.log10(max(avg_views, 1))
    norm_views = min(1.0, log_views / math.log10(max_possible_views))
    norm_seo = min(1.0, avg_seo / 100.0)
    duration_min = avg_duration_sec / 60
    if duration_min < 2:
        norm_duration = 0.3
    elif duration_min < 5:
        norm_duration = 0.6
    elif duration_min <= 15:
        norm_duration = 1.0
    else:
        norm_duration = 0.8
    score = 0.5 * norm_seo + 0.3 * norm_views + 0.2 * norm_duration
    return min(100.0, score * 100)


def seo_score(entry, subscribers, today_str="20251012"):
    views = entry.get("views", 0)
    likes = entry.get("likes", 0)
    comments = entry.get("comments", 0)
    duration = entry.get("duration", 0)
    upload_date_str = entry.get("date", "0")
    try:
        upload_date = datetime.strptime(str(upload_date_str), "%Y%m%d")
    except ValueError:
        return None
    today = datetime.strptime(today_str, "%Y%m%d")
    age_days = max(1, (today - upload_date).days)
    engagement_raw = (likes + 2 * comments) / (views + 1)
    base_score = min(80, 100 * engagement_raw * 10)
    views_per_day = views / age_days
    expected_views = max(100, subscribers * 0.1)
    viral_ratio = views_per_day / expected_views
    viral_multiplier = min(2.0, 0.8 + math.log10(1 + viral_ratio))
    length_minutes = duration / 60.0
    engagement_rate = (likes + comments) / (views + 1)
    if length_minutes < 3:
        length_bonus = 1.0
    else:
        duration_factor = min(3, length_minutes / 10)
        engagement_factor = min(1.0, engagement_rate / 0.05)
        length_bonus = 1.0 + 0.2 * duration_factor * engagement_factor
    score = base_score * viral_multiplier * length_bonus
    return min(100.0, score)
