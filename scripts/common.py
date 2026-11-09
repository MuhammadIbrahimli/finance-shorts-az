"""Shared paths and helpers for the finance Shorts pipeline."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Console encoding can be cp1252 on Windows; Azerbaijani/Russian output must not crash.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
USED_FILE = ROOT / "used.json"
TREND_FILE = WORK / "trend.json"
TRANSCRIPT_FILE = WORK / "transcript.txt"
TRANSCRIPT_META_FILE = WORK / "transcript_meta.json"
SCRIPT_FILE = WORK / "script.json"
NARRATION_RAW = WORK / "narration.wav"
NARRATION_TRIM = WORK / "narration_trim.wav"
SCENE_FILE = WORK / "scene" / "index.html"
VIDEO_FILE = WORK / "video.mp4"
MUSIC_FILE = ROOT / "assets" / "music.mp3"  # optional, supplied by you (royalty-free)


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        fail(f"Не задана переменная окружения {name}")
    return value


def ensure_work_dir() -> None:
    WORK.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fail(message: str) -> None:
    """Print an error to stderr and exit with status 1."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)
