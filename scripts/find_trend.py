"""Find an animated, general-audience finance Short from a channel that is about a month old.

Criteria (owner's brief):
- the CHANNEL was created at most CHANNEL_MAX_AGE_DAYS ago (a new channel);
- the video was published at most VIDEO_MAX_AGE_DAYS ago;
- the video is animated (title or description says so) and is finance education or
  stories for a general audience, not market news;
- news-style videos are excluded by keyword;
- length <= 90 s, captions usable (en/ru/tr/az), not already in used.json.
Among the matches the most-viewed one is chosen.

Writes work/trend.json and adds the video id to used.json (unless --dry-run).
Requires: YOUTUBE_API_KEY (YouTube Data API v3).
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta, timezone

import requests

from common import TREND_FILE, USED_FILE, ensure_work_dir, fail, load_json, require_env, save_json

API = "https://www.googleapis.com/youtube/v3"
CHANNEL_MAX_AGE_DAYS = 31
VIDEO_MAX_AGE_DAYS = 31
MAX_DURATION_SEC = 90
TRANSCRIPT_LANGS = ["en", "ru", "tr", "az"]

# Animated, educational/story finance for a general audience.
QUERIES = [
    "animated money story for beginners",
    "animated personal finance explained",
    "2D animation how money works",
    "animated budgeting story",
    "animated investing for beginners",
    "cartoon explains saving money",
    "animated financial literacy",
    "animated debt explained story",
]
# Required: the title or description shows that the video is animated.
ANIMATION_RE = re.compile(
    r"animat|cartoon|2d|motion graphic|whiteboard|animasiya|анимац|мультик", re.IGNORECASE)
# Excluded: news and market-report style.
NEWS_RE = re.compile(
    r"\bnews\b|breaking|crash|today|this week|live\b|market update|daily update|xəbər|"
    r"новост|сегодня|обвал|рынок сегодня|прогноз на",
    re.IGNORECASE)


def get(url: str, params: dict) -> requests.Response:
    """GET wrapper: the API key sits in the query string, so never let an exception print the URL."""
    try:
        return requests.get(url, params=params, timeout=30)
    except requests.RequestException as exc:
        fail(f"YouTube API: сетевая ошибка {type(exc).__name__}")


def parse_duration(iso: str) -> int:
    """Convert an ISO 8601 duration such as PT45S or PT1M30S to seconds."""
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 10**6
    h, mins, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mins * 60 + s


def parse_ts(value: str) -> datetime:
    """YouTube timestamps may or may not have fractional seconds."""
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def has_transcript(video_id: str) -> bool:
    """True if YouTube has captions in a language the pipeline can use."""
    from youtube_transcript_api import YouTubeTranscriptApi

    try:
        YouTubeTranscriptApi().list(video_id).find_transcript(TRANSCRIPT_LANGS)
        return True
    except Exception:  # no captions, captions disabled, blocked, etc.
        return False


def search_video_ids(api_key: str, published_after: str) -> set[str]:
    ids: set[str] = set()
    for query in QUERIES:
        resp = get(f"{API}/search", params={
            "key": api_key, "part": "id", "type": "video", "videoDuration": "short",
            "q": query, "order": "viewCount", "publishedAfter": published_after,
            "relevanceLanguage": "en", "maxResults": 50,
        })
        if resp.status_code != 200:
            fail(f"YouTube search.list вернул {resp.status_code}: {resp.text[:300]}")
        ids.update(item["id"]["videoId"] for item in resp.json().get("items", []) if "videoId" in item["id"])
    return ids


def video_details(api_key: str, ids: list[str]) -> list[dict]:
    results: list[dict] = []
    for i in range(0, len(ids), 50):
        resp = get(f"{API}/videos", params={
            "key": api_key, "part": "snippet,statistics,contentDetails",
            "id": ",".join(ids[i:i + 50]),
        })
        if resp.status_code != 200:
            fail(f"YouTube videos.list вернул {resp.status_code}: {resp.text[:300]}")
        results.extend(resp.json().get("items", []))
    return results


def channel_created(api_key: str, channel_ids: list[str]) -> dict[str, datetime]:
    """Map channel id -> channel creation time (snippet.publishedAt)."""
    created: dict[str, datetime] = {}
    ids = sorted(channel_ids)
    for i in range(0, len(ids), 50):
        resp = get(f"{API}/channels", params={
            "key": api_key, "part": "snippet", "id": ",".join(ids[i:i + 50]),
        })
        if resp.status_code != 200:
            fail(f"YouTube channels.list вернул {resp.status_code}: {resp.text[:300]}")
        for ch in resp.json().get("items", []):
            created[ch["id"]] = parse_ts(ch["snippet"]["publishedAt"])
    return created


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    api_key = require_env("YOUTUBE_API_KEY")
    ensure_work_dir()

    now = datetime.now(timezone.utc)
    published_after = (now - timedelta(days=VIDEO_MAX_AGE_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    channel_cutoff = now - timedelta(days=CHANNEL_MAX_AGE_DAYS)
    video_cutoff = now - timedelta(days=VIDEO_MAX_AGE_DAYS)

    used = set(load_json(USED_FILE, {"used": []}).get("used", []))
    candidate_ids = search_video_ids(api_key, published_after) - used
    if not candidate_ids:
        fail("Нет кандидатов в поиске. Расширьте QUERIES или проверьте used.json.")

    videos = video_details(api_key, sorted(candidate_ids))
    created = channel_created(api_key, [v["snippet"]["channelId"] for v in videos])

    ranked: list[dict] = []
    for item in videos:
        snip = item["snippet"]
        text = f"{snip.get('title', '')}\n{snip.get('description', '')}"
        published = parse_ts(snip["publishedAt"])
        duration = parse_duration(item["contentDetails"]["duration"])
        channel_id = snip["channelId"]
        if published < video_cutoff or duration > MAX_DURATION_SEC:
            continue
        if channel_id not in created or created[channel_id] < channel_cutoff:
            continue  # the channel is older than a month
        if not ANIMATION_RE.search(text):
            continue  # not animated
        if NEWS_RE.search(text):
            continue  # news / market-report style
        ranked.append({
            "video_id": item["id"],
            "url": f"https://www.youtube.com/shorts/{item['id']}",
            "title": snip["title"],
            "channel": snip["channelTitle"],
            "channel_id": channel_id,
            "channel_created_at": created[channel_id].isoformat(),
            "published_at": snip["publishedAt"],
            "duration_sec": duration,
            "view_count": int(item.get("statistics", {}).get("viewCount", 0)),
            "description": snip.get("description", ""),
        })

    if not ranked:
        fail("Нет анимированных финансовых Shorts от каналов не старше 31 дня (после фильтров).")

    ranked.sort(key=lambda r: r["view_count"], reverse=True)
    best = None
    for cand in ranked:
        if has_transcript(cand["video_id"]):
            best = cand
            break
        print(f"Пропущено (нет субтитров en/ru/tr/az): {cand['video_id']}")
    if best is None:
        fail("Подходящих видео с субтитрами не найдено.")

    if dry_run:
        print(f"[dry-run] {best['url']} | {best['view_count']} просмотров | канал {best['channel']} "
              f"создан {best['channel_created_at'][:10]} | {best['title']}")
        return
    save_json(TREND_FILE, best)
    used.add(best["video_id"])
    save_json(USED_FILE, {"used": sorted(used)})
    print(f"Выбрано: {best['url']} | {best['view_count']} просмотров | {best['title']}")


if __name__ == "__main__":
    main()
