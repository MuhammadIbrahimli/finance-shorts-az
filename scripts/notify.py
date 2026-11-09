"""Send the result (or an error report) to Telegram.

Success:  python scripts/notify.py
          -> sends work/video.mp4 with sendVideo (or sendDocument if it is too big for
             sendVideo), then a message with title, description, cover prompt and source link.
Error:    python scripts/notify.py --error --step find_trend --message "текст ошибки"

Env: TG_TOKEN, TG_CHAT_ID.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import requests

from common import SCRIPT_FILE, TREND_FILE, VIDEO_FILE, fail, load_json, require_env

API = "https://api.telegram.org/bot{token}/{method}"
# Bot API uploads are limited to 50 MB for both sendVideo and sendDocument.
UPLOAD_LIMIT = 50 * 1024 * 1024


def call(token: str, method: str, **kwargs) -> dict:
    resp = requests.post(API.format(token=token, method=method), timeout=600, **kwargs)
    data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
    if resp.status_code != 200 or not data.get("ok"):
        fail(f"Telegram {method} вернул {resp.status_code}: {resp.text[:300]}")
    return data


def send_text(token: str, chat_id: str, text: str) -> None:
    # Telegram text messages are limited to 4096 characters.
    call(token, "sendMessage", data={"chat_id": chat_id, "text": text[:4000],
                                     "disable_web_page_preview": "true"})


def send_video(token: str, chat_id: str, path: Path, caption: str) -> None:
    size = path.stat().st_size
    with path.open("rb") as fh:
        if size <= UPLOAD_LIMIT:
            call(token, "sendVideo", data={"chat_id": chat_id, "caption": caption[:1024],
                                           "supports_streaming": "true"},
                 files={"video": (path.name, fh, "video/mp4")})
            print(f"Отправлено как видео ({size / 1e6:.1f} МБ)")
            return
    if size > UPLOAD_LIMIT:
        fail(f"Файл {size / 1e6:.1f} МБ больше лимита Telegram 50 МБ; уменьшите bitrate в render.py")
    with path.open("rb") as fh:
        call(token, "sendDocument", data={"chat_id": chat_id, "caption": caption[:1024]},
             files={"document": (path.name, fh, "video/mp4")})
    print("Отправлено как документ")


def report_success(token: str, chat_id: str) -> None:
    trend = load_json(TREND_FILE, {})
    script = load_json(SCRIPT_FILE, {})
    if not VIDEO_FILE.exists():
        fail(f"Нет файла {VIDEO_FILE}")

    title = script.get("title_az", "Maliyyə videosu")
    send_video(token, chat_id, VIDEO_FILE, title)

    details = "\n\n".join(filter(None, [
        f"🎬 Название: {title}",
        f"📝 Описание:\n{script.get('description_az', '')}",
        f"🖼 Промпт обложки:\n{script.get('cover_prompt', '')}",
        f"🔗 Источник (вдохновение, не копия): {trend.get('url', 'н/д')}",
        f"👁 Просмотров у источника: {trend.get('view_count', 'н/д')}",
    ]))
    send_text(token, chat_id, details)
    print("Отчёт отправлен в Telegram")


def report_error(token: str, chat_id: str, step: str, message: str) -> None:
    send_text(token, chat_id, f"❌ Конвейер остановлен на шаге: {step}\n\n{message}")
    print("Отчёт об ошибке отправлен в Telegram")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--error", action="store_true", help="send an error report instead")
    parser.add_argument("--step", default="неизвестно")
    parser.add_argument("--message", default="")
    parser.add_argument("--message-file", help="read the error text from a file (e.g. a log tail)")
    args = parser.parse_args()

    token = require_env("TG_TOKEN")
    chat_id = require_env("TG_CHAT_ID")

    if args.error:
        message = args.message
        if args.message_file and Path(args.message_file).exists():
            message = Path(args.message_file).read_text(encoding="utf-8", errors="replace")[-3000:]
        report_error(token, chat_id, args.step, message or "Причина не указана")
    else:
        report_success(token, chat_id)


if __name__ == "__main__":
    main()
