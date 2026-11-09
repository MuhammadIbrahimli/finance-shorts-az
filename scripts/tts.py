"""Voice the Azerbaijani narration with the Gemini TTS API.

Reads work/script.json ("narration_az") and writes work/narration.wav.
Requires: GEMINI_API_KEY. Optional: GEMINI_TTS_MODEL, GEMINI_TTS_VOICE.
"""
from __future__ import annotations

import base64
import os
import re
import time
import wave

import requests

from common import NARRATION_RAW, SCRIPT_FILE, ensure_work_dir, fail, load_json, require_env

DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_VOICE = "Kore"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_RATE = 24000


def parse_rate(mime: str) -> int:
    m = re.search(r"rate=(\d+)", mime or "")
    return int(m.group(1)) if m else DEFAULT_RATE


def request_audio(api_key: str, model: str, voice: str, text: str) -> tuple[bytes, int]:
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Read the following Azerbaijani text naturally, clearly and calmly, "
                            "like a short financial explainer:\n\n" + text
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "languageCode": "az-AZ",
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}},
            },
        },
    }
    for attempt in range(4):
        resp = requests.post(
            ENDPOINT.format(model=model),
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            json=body,
            timeout=180,
        )
        if resp.status_code in (429, 500, 503) and attempt < 3:
            time.sleep(5 * (attempt + 1))
            continue
        if resp.status_code != 200:
            fail(f"Gemini TTS вернул {resp.status_code}: {resp.text[:400]}")
        break

    part = resp.json()["candidates"][0]["content"]["parts"][0]["inlineData"]
    return base64.b64decode(part["data"]), parse_rate(part.get("mimeType", ""))


def main() -> None:
    api_key = require_env("GEMINI_API_KEY")
    model = os.environ.get("GEMINI_TTS_MODEL", DEFAULT_MODEL)
    voice = os.environ.get("GEMINI_TTS_VOICE", DEFAULT_VOICE)
    ensure_work_dir()

    script = load_json(SCRIPT_FILE, None)
    if not script or not script.get("narration_az", "").strip():
        fail("В work/script.json нет поля narration_az")

    pcm, rate = request_audio(api_key, model, voice, script["narration_az"])
    if not pcm:
        fail("Gemini TTS вернул пустое аудио")

    with wave.open(str(NARRATION_RAW), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit PCM
        wav.setframerate(rate)
        wav.writeframes(pcm)
    print(f"Озвучка: {NARRATION_RAW} ({len(pcm) / (2 * rate):.1f} с, модель {model}, голос {voice})")


if __name__ == "__main__":
    main()
