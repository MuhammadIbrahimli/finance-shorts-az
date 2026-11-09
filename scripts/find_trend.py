"""Find the most-viewed finance YouTube Shorts from the last 14 days that are not in used.json.

Writes the chosen video to work/trend.json and adds its id to used.json.
Requires: YOUTUBE_API_KEY (YouTube Data API v3).
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

import requests

from common import (
    TREND_FILE,
    USED_FILE,
    ensure_work_dir,
    fail,
    load_json,
    require_env,
    save_json,
)

API = "https://www.googleapis.com/youtube/v3"
QUERIES = [
    "personal finance tips",
    "investing for beginners",
    "money saving tips",
    "stock market explained",
    "budgeting tips",
]
MAX_DURATION_SEC = 90
MAX_AGE_DAYS = 14


def parse_duration(iso: str) -> int:
    """Convert an ISO 8601 duration such as PT45S or PT1M30S to seconds."""
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 10**6
    h, mins, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mins * 60 + s


def search_ids(api_key: str, published_after: str) -> set[str]:
    ids: set[str] = set()
    for query in QUERIES:
        resp = requests.get(
            f"{API}/search",
            params={
                "key": api_key,
                "part": "id",
                "type": "video",
                "videoDuration": "short",
                "q": query,
                "order": "viewCount",
                "publishedAfter": published_after,
                "maxResults": 50,
            },
            timeout=30,
        )
        if resp.status_code != 200:
            fail(f"YouTube search.list вернул {resp.status_code}: {resp.text[:300]}")
        ids.update(item["id"]["videoId"] for item in resp.json().get("items", []))
    return ids


def video_details(api_key: str, ids: list[str]) -> list[dict]:
    results: list[dict] = []
    for i in range(0, len(ids), 50):
        chunk = ids[i : i + 50]
        resp = requests.get(
            f"{API}/videos",
            params={
                "key": api_key,
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(chunk),
            },
            timeout=30,
        )
        if resp.status_code != 200:
            fail(f"YouTube videos.list вернул {resp.status_code}: {resp.text[:300]}")
        results.extend(resp.json().get("items", []))
    return results


def main() -> None:
    api_key = require_env("YOUTUBE_API_KEY")
    ensure_work_dir()

    now = datetime.now(timezone.utc)
    published_after = (now - timedelta(days=MAX_AGE_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cutoff = now - timedelta(days=MAX_AGE_DAYS)

    used = set(load_json(USED_FILE, {"used": []}).get("used", []))
    candidates = search_ids(api_key, published_after) - used
    if not candidates:
        fail("Нет новых кандидатов: все найденные видео уже в used.json. Расширьте QUERIES.")

    best = None
    for item in video_details(api_key, sorted(candidates)):
        vid = item["id"]
        published = datetime.strptime(
            item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=timezone.utc)
        duration = parse_duration(item["contentDetails"]["duration"])
        if published < cutoff or duration > MAX_DURATION_SEC:
            continue
        views = int(item.get("statistics", {}).get("viewCount", 0))
        if best is None or views > best["view_count"]:
            best = {
                "video_id": vid,
                "url": f"https://www.youtube.com/shorts/{vid}",
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "published_at": item["snippet"]["publishedAt"],
                "duration_sec": duration,
                "view_count": views,
                "description": item["snippet"].get("description", ""),
            }

    if best is None:
        fail("Нет подходящих Shorts (≤90 с, не старше 14 дней, не использованных).")

    save_json(TREND_FILE, best)
    used.add(best["video_id"])
    save_json(USED_FILE, {"used": sorted(used)})
    print(f"Выбрано: {best['url']} | {best['view_count']} просмотров | {best['title']}")


if __name__ == "__main__":
    main()
