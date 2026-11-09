"""Shared paths and helpers for the finance Shorts pipeline."""
from __future__ import annotations

import json
import os
import re
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
WORDS_FILE = WORK / "words.json"
SCENE_FILE = WORK / "scene" / "index.html"
VIDEO_FILE = WORK / "video.mp4"


def load_local_env() -> None:
    """Load KEY=VALUE pairs from a local env file into os.environ (never overrides real env vars).

    Lookup order: $FINANCE_SHORTS_ENV, then ~/.finance-shorts.env, then ROOT/.env. In the cloud routine the variables
    are set in the routine settings and this file does not exist.
    """
    candidates = [
        os.environ.get("FINANCE_SHORTS_ENV", ""),
        str(Path.home() / ".finance-shorts.env"),
        str(ROOT / ".env"),
    ]
    for raw in candidates:
        if not raw:
            continue
        path = Path(raw).expanduser()
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        return


load_local_env()


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        fail(f"Не задана переменная окружения {name}")
    return value


def scrub(text: str) -> str:
    """Remove anything that looks like a secret from text before it is printed or sent."""
    text = re.sub(r"bot\d+:[\w-]+", "bot<redacted>", text)
    text = re.sub(r"AIza[\w-]{20,}", "<redacted>", text)
    text = re.sub(r"AQ\.[\w-]{20,}", "<redacted>", text)
    for name in ("TG_TOKEN", "YOUTUBE_API_KEY", "GEMINI_API_KEY"):
        value = os.environ.get(name, "")
        if value:
            text = text.replace(value, "<redacted>")
    return text


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
    """Print an error (secrets scrubbed) to stderr and exit with status 1."""
    print(f"ERROR: {scrub(message)}", file=sys.stderr)
    sys.exit(1)
