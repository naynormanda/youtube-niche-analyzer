import yt_dlp
from urllib.parse import urlencode


def search_youtube_detailed(query, max_results=20, last_week_only=False):
    base_url = "https://www.youtube.com/results"
    params = {"search_query": query}
    if last_week_only:
        params["sp"] = "EgIIAw"
    url = base_url + "?" + urlencode(params)

    ydl_opts_flat = {
        "quiet": True,
        "extract_flat": True,
        "playlistend": max_results,
    }
    with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
        info = ydl.extract_info(url, download=False)

    video_ids = []
    for entry in info.get("entries", [])[:max_results]:
        if entry and entry.get("id"):
            video_ids.append(entry["id"])

    results = []
    ydl_opts_full = {
        "quiet": True,
        "skip_download": True,
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts_full) as ydl:
        for vid in video_ids:
            try:
                full_info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
                if not full_info:
                    continue
                results.append({
                    "title": full_info.get("title"),
                    "author": full_info.get("uploader"),
                    "duration": full_info.get("duration"),
                    "views": full_info.get("view_count"),
                    "likes": full_info.get("like_count"),
                    "comments": full_info.get("comment_count"),
                    "date": full_info.get("upload_date"),
                    "followers": full_info.get("channel_follower_count") or 1000
                })
            except Exception:
                continue
    return results
