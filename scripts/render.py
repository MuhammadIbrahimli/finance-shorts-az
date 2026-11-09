"""Render the scene to a vertical MP4 (1080x1920) with the narration.

The scene is an HTML file (written by Claude from templates/scene_template.html and the
vizavi-motion skill) that exposes:
  window.DURATION_SEC  - length of the video in seconds
  window.setTime(t)    - draws the frame at time t (seconds)

Each frame is captured with headless Chromium (Playwright) and piped into ffmpeg.
If assets/music.mp3 exists it is mixed under the narration.

Env: RENDER_FPS (default 30).
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

from common import MUSIC_FILE, NARRATION_TRIM, SCENE_FILE, VIDEO_FILE, ensure_work_dir, fail

WIDTH, HEIGHT = 1080, 1920
MUSIC_VOLUME = 0.12


def audio_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def build_ffmpeg_cmd(fps: int, duration: float, audio: Path, music: Path | None, out: Path) -> list[str]:
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
        "-i", str(audio),
    ]
    if music:
        cmd += ["-stream_loop", "-1", "-i", str(music)]
        audio_map = ["-filter_complex",
                     f"[2:a]volume={MUSIC_VOLUME}[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]",
                     "-map", "[a]"]
    else:
        audio_map = ["-map", "1:a"]
    cmd += ["-map", "0:v"] + audio_map + [
        "-t", f"{duration:.3f}",
        "-r", str(fps),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out),
    ]
    return cmd


def main() -> None:
    if not SCENE_FILE.exists():
        fail(f"Нет сцены {SCENE_FILE}. Напишите её по шаблону templates/scene_template.html")
    if not NARRATION_TRIM.exists():
        fail(f"Нет озвучки {NARRATION_TRIM}. Сначала выполните tts.py и trim.py")
    ensure_work_dir()

    fps = int(os.environ.get("RENDER_FPS", "30"))
    audio_len = audio_duration(NARRATION_TRIM)
    music = MUSIC_FILE if MUSIC_FILE.exists() else None

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.goto(SCENE_FILE.resolve().as_uri(), wait_until="load")
        page.evaluate("document.fonts ? document.fonts.ready : null")
        if not page.evaluate("typeof window.setTime === 'function'"):
            fail("В сцене нет функции window.setTime(t)")
        scene_duration = page.evaluate("typeof window.DURATION_SEC === 'number' ? window.DURATION_SEC : null")
        duration = float(scene_duration) if scene_duration else audio_len
        if abs(duration - audio_len) > 1.0:
            print(f"Внимание: длительность сцены {duration:.2f} с отличается от озвучки {audio_len:.2f} с")

        frames = round(duration * fps)
        cmd = build_ffmpeg_cmd(fps, duration, NARRATION_TRIM, music, VIDEO_FILE)
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            for i in range(frames):
                page.evaluate(f"window.setTime({i / fps:.6f})")
                ff.stdin.write(page.screenshot(type="jpeg", quality=95))
        except BrokenPipeError:
            pass
        finally:
            if ff.stdin:
                ff.stdin.close()
            code = ff.wait()
            browser.close()
    if code != 0 or not VIDEO_FILE.exists():
        fail(f"ffmpeg завершился с кодом {code}")
    print(f"Видео: {VIDEO_FILE} ({frames} кадров, {duration:.2f} с, {fps} fps, музыка: {'да' if music else 'нет'})")


if __name__ == "__main__":
    main()
