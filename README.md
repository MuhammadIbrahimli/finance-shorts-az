# finance-shorts-az

Автоматический конвейер коротких финансовых видео (9:16, 1080×1920) на азербайджанском языке.
Раз в день его запускает облачная рутина Claude Code по инструкции из [prompt.md](prompt.md).
Готовое видео и отчёт приходят в Telegram. **Ничего никуда не публикуется.**

## Как это работает

```
find_trend ─► transcript ─► перевод и сценарий (пишет Claude) ─► tts ─► trim ─► сцена (пишет Claude) ─► render ─► notify
```

| Скрипт | Что делает | Нужно |
|---|---|---|
| `scripts/find_trend.py` | Ищет самые просматриваемые финансовые Shorts не старше 14 дней (≤90 с), которых нет в `used.json`. Пишет выбор в `work/trend.json` и `used.json`. | `YOUTUBE_API_KEY` |
| `scripts/transcript.py` | Берёт текст озвучки: сначала файл из vidIQ (`work/vidiq_transcript.txt`, его сохраняет Claude через коннектор `video_transcript`), иначе субтитры YouTube. | коннектор vidIQ (опционально) |
| `scripts/tts.py` | Озвучивает `narration_az` из `work/script.json` через Gemini TTS. Пишет `work/narration.wav`. | `GEMINI_API_KEY` |
| `scripts/trim.py` | Пауз длиннее 0.4 с сокращает до 0.2 с. Пишет `work/narration_trim.wav`. | ffmpeg |
| `scripts/render.py` | Открывает сцену `work/scene/index.html` в Chromium, кадр за кадром снимает её и собирает MP4 с озвучкой. Фоновая музыка подмешивается, если есть `assets/music.mp3`. | Playwright + Chromium, ffmpeg |
| `scripts/notify.py` | Отправляет видео в Telegram (`sendVideo`, а если больше 50 МБ, то `sendDocument`) и отчёт: название, описание, промпт обложки, ссылка на источник. С флагом `--error` шлёт отчёт об ошибке. | `TG_TOKEN`, `TG_CHAT_ID` |

Сценарий, перевод, название, описание, промпт обложки и сцену пишет Claude во время запуска рутины. Скрипты только готовят данные и собирают видео.

## Структура

```
prompt.md                 инструкция для одного запуска рутины (вставляется в рутину)
scripts/                  конвейер (common.py — общие пути и помощники)
templates/scene_template.html   каркас сцены с контрактом window.setTime(t)
.claude/skills/vizavi-motion/   скилл motion-роликов, по которому строится сцена
used.json                 id уже использованных видео
assets/                   сюда можно положить music.mp3 (лицензированная музыка)
work/                     промежуточные файлы, не коммитится
```

## Настройка рутины (один раз, вручную)

1. Создайте облачную рутину с расписанием «раз в день». Репозиторий: `MuhammadIbrahimli/finance-shorts-az`, ветка `main`.
2. Вставьте содержимое `prompt.md` как промпт рутины.
3. Окружение (setup script). Ubuntu-образ:
   ```bash
   apt-get update && apt-get install -y ffmpeg
   pip install -r requirements.txt
   playwright install chromium --with-deps
   ```
4. Переменные окружения (секреты рутины, в чат их не передавать):

| Переменная | Что это | Обязательна |
|---|---|---|
| `YOUTUBE_API_KEY` | ключ YouTube Data API v3 (Google Cloud Console) | да |
| `GEMINI_API_KEY` | ключ Gemini API (Google AI Studio) | да |
| `TG_TOKEN` | токен бота от @BotFather | да |
| `TG_CHAT_ID` | id чата или канала, куда бот пишет | да |
| `GEMINI_TTS_MODEL` | модель TTS, по умолчанию `gemini-2.5-flash-preview-tts` | нет |
| `GEMINI_TTS_VOICE` | голос, по умолчанию `Kore` | нет |
| `RENDER_FPS` | частота кадров, по умолчанию 30 | нет |

5. Коннектор vidIQ: подключите его к рутине, если хотите получать транскрипт через vidIQ. Без него скрипт возьмёт субтитры YouTube.
6. Право пушить в `main`: рутина коммитит `used.json` напрямую в `main` (как вы просили, без PR). Для этого у рутины должен быть доступ на запись в репозиторий (GitHub-токен или deploy key с правом записи в настройках рутины).
7. Лицензированная музыка (по желанию): положите свой трек в `assets/music.mp3` и закоммитьте. Без него видео будет без музыки. Конвейер музыку не скачивает.

## Ограничения

- **YouTube может блокировать субтитры с облачных IP.** Тогда `transcript.py` не сработает, и видео пропускается с отчётом об ошибке. Надёжный путь — подключённый vidIQ.
- **Субтитры YouTube через API-ключ не скачиваются** (для `captions.download` нужен OAuth владельца канала). Поэтому используется библиотека `youtube-transcript-api`, которая читает публичные субтитры. Это неофициальный способ.
- **Азербайджанский в Gemini TTS** официально не подтверждён в документации, которую я смотрел. Проверьте первый результат. Если голос звучит плохо, попробуйте другую модель в `GEMINI_TTS_MODEL`.
- **Music и sound design:** автоматической генерации нет. Скилл `vizavi-motion` по умолчанию требует музыку, поэтому без `assets/music.mp3` это требование не выполнено.
- **Лимит Telegram:** 50 МБ для ботов. Видео 30–60 с при CRF 20 обычно укладывается.
- `used.json` помечает видео использованным сразу после выбора, даже если дальше конвейер упал.

## Локальная проверка

```bash
pip install -r requirements.txt && playwright install chromium
python scripts/find_trend.py          # нужен YOUTUBE_API_KEY
python scripts/trim.py work/narration.wav work/narration_trim.wav
python scripts/render.py              # нужны work/scene/index.html и work/narration_trim.wav
```

## Авторство сцен

Сцены строятся по скиллу `vizavi-motion` из `.claude/skills/`. Скилл взят из личной установки владельца репозитория.
