Получи текст озвучки выбранного TikTok-ролика через коннектор vidIQ и сохрани его для написания нового сценария.

Ссылка: {TREND_URL}

Шаг 1. Вызови vidiq_watch_shortform_content с url = ссылка выше и prompt:
"Transcribe all spoken narration and on-screen text verbatim, in order. Plain text only, no timestamps, no scene descriptions."
Инструмент асинхронный: он вернёт mcpJobId.

Шаг 2. Опрашивай vidiq_job_poll с этим mcpJobId, пока статус не станет completed. Если статус failed или прошло больше 10 опросов без результата, остановись и ответь строкой «ОШИБКА VIDIQ: <причина>».

Шаг 3. Запиши результат в work/transcript.txt (UTF-8): только текст реплик и надписей по порядку, без таймкодов, без описаний сцен, без пометок вида [music]. Если в результате есть только описание сцен без речи, так и напиши в отчёте и не записывай файл.

Шаг 4. Запиши work/transcript_meta.json: {"video_id": "<из work/trend.json>", "source": "vidiq_tiktok", "chars": <длина текста>}.

Ограничения: это источник идей и фактов для нового сценария. Не копируй формулировки, не используй кадры, музыку или звук оригинала. Не отправляй ничего в Telegram и не коммить в git.
