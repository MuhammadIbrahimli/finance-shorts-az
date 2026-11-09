"""Run one pipeline step. Called by n8n (Execute Command) on the local machine.

usage: python scripts/run_step.py <step>

On failure the step's output tail is sent to Telegram as an error report (notify.py --error),
and the process exits with status 1, so n8n marks the execution as failed.
Claude steps call the local Claude Code CLI (`claude -p --model sonnet`), which uses the
existing Claude Code login; no API key is needed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from common import ROOT, WORK, ensure_work_dir, scrub

PY = sys.executable
CLAUDE_MODEL = "sonnet"

STEPS: dict[str, list[str]] = {
    "find_trend": [PY, "scripts/find_trend.py"],
    "transcript": [PY, "scripts/transcript.py"],
    "tts": [PY, "scripts/tts.py"],
    "trim": [PY, "scripts/trim.py"],
    "align": [PY, "scripts/align_words.py"],
    "render": [PY, "scripts/render.py"],
    "notify": [PY, "scripts/notify.py"],
}
# Claude steps: the prompt file is sent on stdin.
CLAUDE_STEPS: dict[str, str] = {
    "creative_script": "prompts/creative_script.md",
    "creative_scene": "prompts/creative_scene.md",
}


def run(cmd: list[str], stdin_text: str | None = None) -> tuple[int, str]:
    proc = subprocess.run(
        cmd, cwd=ROOT, input=stdin_text, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60 * 60,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def report_error(step: str, output: str) -> None:
    ensure_work_dir()
    tail = scrub(output)[-3000:]
    (WORK / "last_error.txt").write_text(tail, encoding="utf-8")
    run([PY, "scripts/notify.py", "--error", "--step", step, "--message-file", "work/last_error.txt"])


def main() -> int:
    if len(sys.argv) != 2 or (sys.argv[1] not in STEPS and sys.argv[1] not in CLAUDE_STEPS):
        print(f"usage: run_step.py <{'|'.join([*STEPS, *CLAUDE_STEPS])}>")
        return 2
    step = sys.argv[1]

    if step in CLAUDE_STEPS:
        prompt = (ROOT / CLAUDE_STEPS[step]).read_text(encoding="utf-8")
        code, output = run(["claude", "-p", "--model", CLAUDE_MODEL, "--permission-mode", "acceptEdits"],
                           stdin_text=prompt)
    else:
        code, output = run(STEPS[step])

    print(scrub(output)[-2000:])
    if code != 0:
        report_error(step, output)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
