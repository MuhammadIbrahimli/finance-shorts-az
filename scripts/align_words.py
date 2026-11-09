"""Word timings for karaoke subtitles.

The subtitle text must be EXACTLY the script text (AGENTS.md). Timings come from speech
recognition of the narration (faster-whisper, language az), and the script words are
aligned onto the recognised words with a global Needleman-Wunsch alignment.

Input:  work/narration_trim.wav, work/script.json ("narration_az")
Output: work/words.json  [{"w": "<script token>", "s": start, "e": end}, ...]
        work/align_report.json (unmatched tokens are interpolated and listed)

Env: WHISPER_MODEL (default "medium", per AGENTS.md).
"""
from __future__ import annotations

import difflib
import os
import re

from common import NARRATION_TRIM, SCRIPT_FILE, WORDS_FILE, ensure_work_dir, fail, load_json, save_json

LANGUAGE = "az"
GAP = -0.7


def normalize(token: str) -> str:
    table = str.maketrans({"ı": "i", "ə": "e", "ö": "o", "ü": "u", "ç": "c", "ş": "s", "ğ": "g"})
    return re.sub(r"[^a-z0-9]", "", token.lower().translate(table))


def similarity(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na.isdigit() or nb.isdigit():
        return 1.0 if na == nb else 0.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def recognise(path) -> list[dict]:
    from faster_whisper import WhisperModel

    model = WhisperModel(os.environ.get("WHISPER_MODEL", "medium"), device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(path), language=LANGUAGE, word_timestamps=True,
                                   vad_filter=False, beam_size=5)
    words = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                words.append({"w": text, "s": float(w.start), "e": float(w.end)})
    return words


def align(script_tokens: list[str], rec: list[dict]) -> list[int | None]:
    """Return, for each script token, the index of the matched recognised word (or None)."""
    n, m = len(script_tokens), len(rec)
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    move = [[""] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = i * GAP
        move[i][0] = "up"
    for j in range(1, m + 1):
        score[0][j] = j * GAP
        move[0][j] = "left"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = similarity(script_tokens[i - 1], rec[j - 1]["w"])
            diag = score[i - 1][j - 1] + (s * 2.0 if s >= 0.5 else -1.0)
            up = score[i - 1][j] + GAP
            left = score[i][j - 1] + GAP
            best = max(diag, up, left)
            score[i][j] = best
            move[i][j] = "diag" if best == diag else ("up" if best == up else "left")

    matches: list[int | None] = [None] * n
    i, j = n, m
    while i > 0 and j > 0:
        step = move[i][j]
        if step == "diag":
            if similarity(script_tokens[i - 1], rec[j - 1]["w"]) >= 0.5:
                matches[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif step == "up":
            i -= 1
        else:
            j -= 1
    return matches


def main() -> None:
    ensure_work_dir()
    script = load_json(SCRIPT_FILE, {})
    narration = script.get("narration_az", "").strip()
    if not narration:
        fail("В work/script.json нет narration_az")
    if not NARRATION_TRIM.exists():
        fail(f"Нет {NARRATION_TRIM}: сначала tts.py и trim.py")

    tokens = narration.split()
    rec = recognise(NARRATION_TRIM)
    if not rec:
        fail("Распознавание озвучки не вернуло слов")

    matches = align(tokens, rec)
    unmatched = [t for t, mt in zip(tokens, matches) if mt is None]

    # Matched tokens take the recognised timing. Each run of unmatched tokens is spread
    # evenly across the gap between its matched neighbours.
    times: list[tuple[float, float] | None] = [
        (rec[mt]["s"], rec[mt]["e"]) if mt is not None else None for mt in matches]
    k = 0
    while k < len(times):
        if times[k] is not None:
            k += 1
            continue
        run_start = k
        while k < len(times) and times[k] is None:
            k += 1
        run_end = k  # exclusive
        gap_start = times[run_start - 1][1] if run_start > 0 else 0.0
        gap_end = times[run_end][0] if run_end < len(times) else rec[-1]["e"]
        step = max(gap_end - gap_start, 0.05) / (run_end - run_start)
        for n in range(run_start, run_end):
            times[n] = (gap_start + step * (n - run_start), gap_start + step * (n - run_start + 1))

    words = [{"w": tok, "s": round(s, 3), "e": round(e, 3)} for tok, (s, e) in zip(tokens, times)]
    save_json(WORDS_FILE, words)
    save_json(WORDS_FILE.with_name("align_report.json"),
              {"tokens": len(tokens), "recognised": len(rec), "unmatched": unmatched})
    print(f"Слов в сценарии: {len(tokens)}; распознано: {len(rec)}; без пары: {len(unmatched)}")
    if len(unmatched) > max(3, len(tokens) // 10):
        print("ВНИМАНИЕ: много слов без пары. Проверьте расхождение озвучки и сценария (AGENTS.md).")


if __name__ == "__main__":
    main()
