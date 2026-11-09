"""Get the spoken text of the chosen Short.

Order of sources:
1. vidIQ transcript, if Claude already fetched it with the vidIQ connector
   (video_transcript tool) and saved it to --vidiq-file. The connector is only
   reachable from Claude's session, not from Python, so Claude does this step.
2. YouTube captions via youtube-transcript-api (no API key needed for reading
   public captions; YouTube may block cloud IP addresses, see README).

Writes work/transcript.txt and work/transcript_meta.json.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    TRANSCRIPT_FILE,
    TRANSCRIPT_META_FILE,
    TREND_FILE,
    ensure_work_dir,
    fail,
    load_json,
    save_json,
)

LANGUAGES = ["en", "ru", "tr", "az"]


def from_vidiq(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None


def from_youtube_captions(video_id: str) -> str | None:
    from youtube_transcript_api import YouTubeTranscriptApi

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=LANGUAGES)
    except Exception as exc:  # library raises many subclasses; report and move on
        print(f"YouTube captions недоступны: {type(exc).__name__}: {exc}")
        return None
    text = " ".join(snippet.text.strip() for snippet in fetched if snippet.text.strip())
    return text or None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", help="YouTube video id (default: from work/trend.json)")
    parser.add_argument(
        "--vidiq-file",
        type=Path,
        default=Path("work/vidiq_transcript.txt"),
        help="Plain-text transcript saved by Claude from the vidIQ connector",
    )
    args = parser.parse_args()

    ensure_work_dir()
    video_id = args.video_id or load_json(TREND_FILE, {}).get("video_id")
    if not video_id:
        fail("Нет video_id: запустите find_trend.py или передайте --video-id")

    text = from_vidiq(args.vidiq_file)
    source = "vidiq"
    if text is None:
        text = from_youtube_captions(video_id)
        source = "youtube_captions"
    if text is None:
        fail(
            f"Транскрипт для {video_id} не получен ни через vidIQ, ни через YouTube captions. "
            "Видео пропущено; отправьте отчёт об ошибке."
        )

    TRANSCRIPT_FILE.write_text(text, encoding="utf-8")
    save_json(TRANSCRIPT_META_FILE, {"video_id": video_id, "source": source, "chars": len(text)})
    print(f"Транскрипт ({source}): {len(text)} символов")


if __name__ == "__main__":
    main()
