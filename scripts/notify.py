"""Send the finished video and the Azerbaijani output block to Telegram.

Success: python scripts/notify.py
  -> video (sendVideo; sendDocument if it is over the sendVideo limit), then the text block:
     Başlıq / Örtük üçün prompt / Təsvir (exactly 5 hashtags). Nothing else is sent.
Error:   python scripts/notify.py --error --step find_trend --message "..."

Env: TG_TOKEN, TG_CHAT_ID. The token is never printed; errors are scrubbed.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import requests

from common import SCRIPT_FILE, VIDEO_FILE, fail, load_json, require_env, scrub

API = "https://api.telegram.org/bot{token}/{method}"
# Bot API uploads are limited to 50 MB for both sendVideo and sendDocument.
UPLOAD_LIMIT = 50 * 1024 * 1024
TIMEOUT = 600


def call(token: str, method: str, data: dict, files: dict | None = None) -> None:
    try:
        resp = requests.post(API.format(token=token, method=method), data=data,
                             files=files, timeout=TIMEOUT)
    except requests.RequestException as exc:  # message may contain the URL with the token
        fail(f"Telegram {method}: сетевая ошибка {type(exc).__name__}")
    if resp.status_code != 200 or not resp.json().get("ok"):
        fail(f"Telegram {method} вернул {resp.status_code}: {scrub(resp.text[:300])}")


def send_text(token: str, chat_id: str, text: str) -> None:
    # Telegram text messages are limited to 4096 characters.
    call(token, "sendMessage", {"chat_id": chat_id, "text": text[:4000]})


def send_video(token: str, chat_id: str, path: Path, caption: str) -> None:
    size = path.stat().st_size
    if size > UPLOAD_LIMIT:
        fail(f"Видео {size / 1e6:.1f} МБ больше лимита Telegram 50 МБ; уменьшите crf в render.py")
    with path.open("rb") as fh:
        if size <= 49 * 1024 * 1024:
            call(token, "sendVideo",
                 {"chat_id": chat_id, "caption": caption[:1000], "supports_streaming": "true",
                  "width": "1080", "height": "1920"},
                 {"video": (path.name, fh, "video/mp4")})
            print(f"Видео отправлено ({size / 1e6:.1f} МБ)")
            return
    with path.open("rb") as fh:
        call(token, "sendDocument", {"chat_id": chat_id, "caption": caption[:1000]},
             {"document": (path.name, fh, "video/mp4")})
    print("Видео отправлено как документ")


def output_block(script: dict) -> str:
    title = script.get("title_az", "").strip()
    cover = script.get("cover_prompt_az", "").strip()
    description = script.get("description_az", "").strip()
    if not title or not cover or not description:
        fail("В work/script.json не хватает title_az, cover_prompt_az или description_az")
    tags = re.findall(r"#\S+", description)
    if len(tags) != 5:
        fail(f"В описании должно быть ровно 5 хэштегов, найдено {len(tags)}")
    return (f"Başlıq\n{title}\n\n"
            f"Örtük üçün prompt\n{cover}\n\n"
            f"Təsvir\n{description}")


def report_success(token: str, chat_id: str) -> None:
    if not VIDEO_FILE.exists():
        fail(f"Нет файла {VIDEO_FILE}")
    script = load_json(SCRIPT_FILE, {})
    block = output_block(script)
    send_video(token, chat_id, VIDEO_FILE, script.get("title_az", ""))
    send_text(token, chat_id, block)
    print("Текст выдачи отправлен")


def report_error(token: str, chat_id: str, step: str, message: str) -> None:
    send_text(token, chat_id, f"❌ Конвейер остановлен на шаге: {step}\n\n{scrub(message)}")
    print("Отчёт об ошибке отправлен")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--error", action="store_true", help="send an error report instead")
    parser.add_argument("--step", default="неизвестно")
    parser.add_argument("--message", default="")
    parser.add_argument("--message-file", help="read the error text from a file (log tail)")
    parser.add_argument("--check", action="store_true",
                        help="only verify the token and chat (no message is sent)")
    args = parser.parse_args()

    token = require_env("TG_TOKEN")
    chat_id = require_env("TG_CHAT_ID")

    if args.check:
        try:
            me = requests.get(API.format(token=token, method="getMe"), timeout=30)
            chat = requests.get(API.format(token=token, method="getChat"),
                                params={"chat_id": chat_id}, timeout=30)
        except requests.RequestException as exc:
            fail(f"Telegram: сетевая ошибка {type(exc).__name__}")
        print(f"getMe: {me.status_code} ok={me.json().get('ok')}; "
              f"getChat: {chat.status_code} ok={chat.json().get('ok')}")
        return

    if args.error:
        message = args.message
        if args.message_file and Path(args.message_file).exists():
            message = Path(args.message_file).read_text(encoding="utf-8", errors="replace")[-3000:]
        report_error(token, chat_id, args.step, message or "Причина не указана")
    else:
        report_success(token, chat_id)


if __name__ == "__main__":
    main()
