"""Shorten long pauses in the narration.

Rule: any silence longer than 0.4 s is cut down to exactly 0.2 s.
Shorter pauses are left untouched.

Implementation: ffmpeg silencedetect finds the silences, then the audio is re-assembled
from segments with atrim + concat. (ffmpeg's silenceremove cannot do this exactly: it always
keeps the first stop_duration of a silence, so a 2 s pause would become ~0.6 s.)

Usage: python scripts/trim.py [input.wav] [output.wav]
"""
from __future__ import annotations

import re
import subprocess
import sys

from common import NARRATION_RAW, NARRATION_TRIM, fail

NOISE = "-40dB"
MIN_SILENCE = 0.4   # silences longer than this are shortened
KEEP_SILENCE = 0.2  # ...to this length
SILENCE_RE = re.compile(r"silence_start: (?P<start>[\d.]+)")
END_RE = re.compile(r"silence_end: (?P<end>[\d.]+)")


def duration(path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def detect_silences(src, total: float) -> list[tuple[float, float]]:
    """Return (start, end) of every silence longer than MIN_SILENCE."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src),
         "-af", f"silencedetect=noise={NOISE}:d={MIN_SILENCE}", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        fail(f"ffmpeg silencedetect упал: {result.stderr[-400:]}")
    starts = [float(m.group("start")) for m in SILENCE_RE.finditer(result.stderr)]
    ends = [float(m.group("end")) for m in END_RE.finditer(result.stderr)]
    silences = []
    for i, start in enumerate(starts):
        end = ends[i] if i < len(ends) else total  # silence running to the end of file
        silences.append((start, end))
    return silences


def build_segments(silences, total: float) -> list[tuple[float, float]]:
    """Keep speech as is; keep only KEEP_SILENCE of each long silence."""
    segments: list[tuple[float, float]] = []
    cursor = 0.0
    for start, end in silences:
        if end - start <= MIN_SILENCE:
            continue
        segments.append((cursor, start))
        segments.append((start, min(start + KEEP_SILENCE, end)))
        cursor = end
    segments.append((cursor, total))
    return [(a, b) for a, b in segments if b - a > 0.001]


def main() -> None:
    src = sys.argv[1] if len(sys.argv) > 1 else NARRATION_RAW
    dst = sys.argv[2] if len(sys.argv) > 2 else NARRATION_TRIM

    total = duration(src)
    silences = detect_silences(src, total)
    segments = build_segments(silences, total)

    parts = [
        f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[s{i}]"
        for i, (a, b) in enumerate(segments)
    ]
    labels = "".join(f"[s{i}]" for i in range(len(segments)))
    graph = ";".join(parts) + f";{labels}concat=n={len(segments)}:v=0:a=1[out]"

    result = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-filter_complex", graph, "-map", "[out]", str(dst)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        fail(f"ffmpeg concat упал: {result.stderr[-400:]}")

    print(f"Пауз длиннее {MIN_SILENCE} с: {len(silences)}; длительность {total:.2f} с -> {duration(dst):.2f} с ({dst})")


if __name__ == "__main__":
    main()
