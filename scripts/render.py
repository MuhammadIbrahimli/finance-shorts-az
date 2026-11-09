"""Render the scene to a vertical MP4 (1080x1920, 24 fps) with the narration.

Scene contract (see templates/scene_template.html and AGENTS.md):
  window.renderAt(t)   - draws the frame at time t (seconds); a pure function of t
  window.DURATION_SEC  - optional; defaults to the length of the narration
  <canvas id="c">      - the frame is taken from this element (falls back to the viewport)

Frames are captured with headless Chromium (Playwright) and piped to ffmpeg as JPEG.
Music is intentionally not mixed in: the channel rules allow only the voice (AGENTS.md).

Env: RENDER_FPS (default 24).
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

from common import NARRATION_TRIM, SCENE_FILE, VIDEO_FILE, ensure_work_dir, fail, scrub

WIDTH, HEIGHT = 1080, 1920
DEFAULT_FPS = 24


def audio_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def build_ffmpeg_cmd(fps: int, duration: float, audio: Path, out: Path) -> list[str]:
    return [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
        "-i", str(audio),
        "-map", "0:v", "-map", "1:a",
        "-vf", "format=yuv420p",
        "-af", "apad",
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264", "-preset", "slow", "-crf", "22",
        "-pix_fmt", "yuv420p", "-color_range", "tv",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out),
    ]


def main() -> None:
    if not SCENE_FILE.exists():
        fail(f"Нет сцены {SCENE_FILE}. Напишите её по шаблону templates/scene_template.html")
    if not NARRATION_TRIM.exists():
        fail(f"Нет озвучки {NARRATION_TRIM}. Сначала выполните tts.py и trim.py")
    ensure_work_dir()

    fps = int(os.environ.get("RENDER_FPS", DEFAULT_FPS))
    audio_len = audio_duration(NARRATION_TRIM)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.on("pageerror", lambda e: print(f"PAGEERR {scrub(str(e))}"))
        page.goto(SCENE_FILE.resolve().as_uri(), wait_until="load")
        page.evaluate("document.fonts ? document.fonts.ready : null")
        if not page.evaluate("typeof window.renderAt === 'function'"):
            fail("В сцене нет функции window.renderAt(t)")
        scene_duration = page.evaluate(
            "typeof window.DURATION_SEC === 'number' ? window.DURATION_SEC : null")
        duration = float(scene_duration) if scene_duration else audio_len
        # The scene should be the narration plus a short tail (AGENTS.md): 0 to 2.5 s longer.
        if not (0 <= duration - audio_len <= 2.5):
            print(f"Внимание: длительность сцены {duration:.2f} с, озвучка {audio_len:.2f} с; "
                  "проверьте хвост (норма: озвучка + 1–1.5 с)")

        canvas = page.query_selector("#c")
        frames = round(duration * fps)
        ff = subprocess.Popen(build_ffmpeg_cmd(fps, duration, NARRATION_TRIM, VIDEO_FILE),
                              stdin=subprocess.PIPE)
        try:
            for i in range(frames):
                page.evaluate(f"window.renderAt({i / fps:.6f})")
                shot = canvas.screenshot(type="jpeg", quality=95) if canvas else \
                    page.screenshot(type="jpeg", quality=95)
                ff.stdin.write(shot)
        except BrokenPipeError:
            pass
        finally:
            if ff.stdin:
                ff.stdin.close()
            code = ff.wait()
            browser.close()
    if code != 0 or not VIDEO_FILE.exists():
        fail(f"ffmpeg завершился с кодом {code}")
    print(f"Видео: {VIDEO_FILE} ({frames} кадров, {duration:.2f} с, {fps} fps)")


if __name__ == "__main__":
    main()
