"""Manual channel mode: pick today's TikTok video from the links you entered.

Reads channels/links.json. Each channel has a list of {"url": ..., "views": ...}.
1. Chooses one channel at random among channels that still have an unused link.
2. Inside it takes the unused link with the most views (ties: the first one listed).
3. Writes work/trend.json (source "tiktok_manual") and adds the video id to used.json.

The pipeline does not browse TikTok: it only uses the links you put in channels/links.json.
"""
from __future__ import annotations

import random
import re

from common import TREND_FILE, USED_FILE, ROOT, ensure_work_dir, fail, load_json, save_json

LINKS_FILE = ROOT / "channels" / "links.json"
VIDEO_RE = re.compile(r"tiktok\.com/@([\w.]+)/video/(\d+)")


def parse(url: str) -> tuple[str, str] | None:
    m = VIDEO_RE.search(url or "")
    return (m.group(1), m.group(2)) if m else None


def main() -> None:
    ensure_work_dir()
    data = load_json(LINKS_FILE, None)
    if not data or "channels" not in data:
        fail("channels/links.json не найден или пуст")
    used = set(load_json(USED_FILE, {"used": []}).get("used", []))

    options: dict[str, dict] = {}
    for handle, items in data["channels"].items():
        best = None
        for item in items or []:
            parsed = parse(item.get("url", ""))
            if not parsed:
                print(f"Пропущена некорректная ссылка для {handle}: {item.get('url', '')!r}")
                continue
            channel, video_id = parsed
            if video_id in used:
                continue
            views = int(item.get("views") or 0)
            if best is None or views > best["view_count"]:
                best = {"video_id": video_id, "url": item["url"], "channel": f"@{channel}",
                        "view_count": views}
        if best:
            options[handle] = best

    if not options:
        fail("Нет непубликованных ссылок ни в одном канале. Добавьте ссылки в channels/links.json")

    handle = random.choice(sorted(options))
    pick = options[handle]
    trend = {"source": "tiktok_manual", "title": None, "description": None,
             "published_at": None, "duration_sec": None, "channel_handle": handle, **pick}
    save_json(TREND_FILE, trend)
    used.add(pick["video_id"])
    save_json(USED_FILE, {"used": sorted(used)})
    print(f"Выбран канал {handle}: {pick['url']} ({pick['view_count']} просмотров)")


if __name__ == "__main__":
    main()
