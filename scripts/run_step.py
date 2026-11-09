"""Run one pipeline step. Called by n8n (Execute Command) on the local machine.

usage: python scripts/run_step.py <step>

Python steps run a script. Claude steps run the local Claude Code CLI headless
(`claude -p --model sonnet`) with a prompt file on stdin. Those steps may use only the
tools listed in ALLOWED_TOOLS for that step (vidIQ connector, read/write files).
On failure the output tail is sent to Telegram (notify.py --error) and the process exits 1.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from common import ROOT, TREND_FILE, USED_FILE, WORK, ensure_work_dir, load_json, save_json, scrub

PY = sys.executable
CLAUDE_MODEL = "sonnet"
VIDIQ_SEARCH = "mcp__claude_ai_vidIQ__vidiq_instagram_tiktok_outlier_search"
VIDIQ_WATCH = "mcp__claude_ai_vidIQ__vidiq_watch_shortform_content"
VIDIQ_POLL = "mcp__claude_ai_vidIQ__vidiq_job_poll"
CANDIDATE_MAX_AGE_DAYS = 31

STEPS: dict[str, list[str]] = {
    "pick_channel": [PY, "scripts/pick_channel.py"],
    "transcript": [PY, "scripts/transcript.py"],
    "tts": [PY, "scripts/tts.py"],
    "trim": [PY, "scripts/trim.py"],
    "align": [PY, "scripts/align_words.py"],
    "render": [PY, "scripts/render.py"],
    "notify": [PY, "scripts/notify.py"],
}
# Claude steps: prompt file (sent on stdin) and the only tools that step may use.
CLAUDE_STEPS: dict[str, tuple[str, str]] = {
    "discover_tiktok": ("prompts/discover_tiktok.md", VIDIQ_SEARCH),
    "tiktok_source_text": ("prompts/tiktok_source_text.md", f"{VIDIQ_WATCH},{VIDIQ_POLL}"),
    "creative_script": ("prompts/creative_script.md", ""),
    "creative_scene": ("prompts/creative_scene.md", ""),
}


def run(cmd: list[str], stdin_text: str | None = None) -> tuple[int, str]:
    proc = subprocess.run(
        cmd, cwd=ROOT, input=stdin_text, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60 * 60,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def report_error(step: str, output: str) -> None:
    ensure_work_dir()
    (WORK / "last_error.txt").write_text(scrub(output)[-3000:], encoding="utf-8")
    run([PY, "scripts/notify.py", "--error", "--step", step, "--message-file", "work/last_error.txt"])


def discover_inputs() -> str:
    """Values the discovery prompt needs: the age cutoff and the ids already used."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=CANDIDATE_MAX_AGE_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    used = sorted(load_json(USED_FILE, {"used": []}).get("used", []))
    return cutoff, json.dumps(used)


def check_discover() -> str | None:
    """After discovery: trend.json must be a TikTok video that is not used yet. Marks it used."""
    trend = load_json(TREND_FILE, None)
    if not trend or not trend.get("video_id") or "tiktok.com" not in trend.get("url", ""):
        return "discover_tiktok не записал work/trend.json с TikTok-видео"
    used = set(load_json(USED_FILE, {"used": []}).get("used", []))
    if trend["video_id"] in used:
        return f"видео {trend['video_id']} уже использовано"
    used.add(trend["video_id"])
    save_json(USED_FILE, {"used": sorted(used)})
    return None


def check_source_text() -> str | None:
    text_file = WORK / "transcript.txt"
    if not text_file.exists() or len(text_file.read_text(encoding="utf-8").strip()) < 200:
        return "tiktok_source_text не записал work/transcript.txt (нужно 200+ символов текста)"
    return None


def main() -> int:
    if len(sys.argv) != 2 or (sys.argv[1] not in STEPS and sys.argv[1] not in CLAUDE_STEPS):
        print(f"usage: run_step.py <{'|'.join([*STEPS, *CLAUDE_STEPS])}>")
        return 2
    step = sys.argv[1]
    ensure_work_dir()

    if step in CLAUDE_STEPS:
        prompt_file, tools = CLAUDE_STEPS[step]
        prompt = (ROOT / prompt_file).read_text(encoding="utf-8")
        if step == "discover_tiktok":
            cutoff, used = discover_inputs()
            prompt = prompt.replace("{CUTOFF}", cutoff).replace("{USED_IDS}", used)
        if step == "tiktok_source_text":
            trend = load_json(TREND_FILE, {})
            prompt = prompt.replace("{TREND_URL}", trend.get("url", ""))
        cmd = ["claude", "-p", "--model", CLAUDE_MODEL, "--permission-mode", "acceptEdits"]
        if tools:
            cmd += ["--allowedTools", tools]
        code, output = run(cmd, stdin_text=prompt)
    else:
        code, output = run(STEPS[step])

    print(scrub(output)[-2000:])
    problem = None
    if code == 0 and step == "discover_tiktok":
        problem = check_discover()
    if code == 0 and step == "tiktok_source_text":
        problem = check_source_text()
    if code != 0 or problem:
        report_error(step, problem or output)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
