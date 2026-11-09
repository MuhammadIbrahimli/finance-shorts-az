# Ежедневный запуск: финансовое Short-видео на азербайджанском (канал Disli Hardz)

Ты работаешь в клоне репозитория `finance-shorts-az` в облачной рутине. Один запуск = один ролик. Перед началом прочитай `AGENTS.md` (через `CLAUDE.md`): это постоянные правила канала (формат, стиль, субтитры, проверка, выдача). Они имеют приоритет над скиллом `.claude/skills/vizavi-motion`, если расходятся (например, музыка: её нет).

Публиковать видео где-либо **нельзя**. Результат уходит только в Telegram (видео и текст выдачи). Не используй чужие видео как есть: ни кадры, ни звук, ни текст целиком. Используй факты и идеи, переписанные своими словами.

Ключи и токены — только из переменных окружения. Не печатай их, не записывай в файлы и не коммить.

## 0. Окружение

```bash
pip install -r requirements.txt
playwright install chromium --with-deps
ffmpeg -version >/dev/null && ffprobe -version >/dev/null || echo "NO FFMPEG"
```

Если ffmpeg отсутствует, сразу отправь отчёт об ошибке (раздел «Ошибки») и остановись.

Переменные: `YOUTUBE_API_KEY`, `GEMINI_API_KEY`, `TG_TOKEN`, `TG_CHAT_ID`. Опционально: `GEMINI_TTS_MODEL`, `GEMINI_TTS_VOICE`, `WHISPER_MODEL` (по умолчанию `medium`), `RENDER_FPS` (по умолчанию 24).

Все промежуточные файлы — в `work/`. Эта папка не коммитится.

## Порядок

Шаги выполняются по порядку. Если шаг упал, отправь отчёт об ошибке и остановись:
`python scripts/notify.py --error --step "<номер и название>" --message "<причина, 1–3 предложения>"`

### 1. Тренд
```bash
python scripts/find_trend.py
```
Выбирает самое просматриваемое финансовое Short (≤90 с, не старше 14 дней, нет в `used.json`). Пишет `work/trend.json` и добавляет id в `used.json`.

### 2. Транскрипт
Если подключён коннектор vidIQ с инструментом `video_transcript`, вызови его для `url` из `work/trend.json` и сохрани текст без таймкодов в `work/vidiq_transcript.txt`. Затем:
```bash
python scripts/transcript.py
```
Скрипт возьмёт vidIQ-файл, если он есть, иначе субтитры YouTube. Если транскрипт короче 300 символов или его нет, это ошибка: не придумывай текст.

### 3. Сценарий, перевод, выдача (пишешь ты)
Прочитай `work/transcript.txt` и `work/trend.json`. Напиши `work/script.json`:
```json
{
  "source_url": "из trend.json",
  "title_az": "Başlıq: до 90 символов",
  "cover_prompt_az": "Örtük üçün prompt: промпт обложки 9:16 в стиле видео, текст ниже середины кадра, декоративная типографика (см. AGENTS.md)",
  "description_az": "Təsvir: 2–4 предложения по сути видео, затем ровно 5 хэштегов",
  "narration_az": "текст озвучки, 90–130 слов, примерно 30–50 секунд",
  "key_facts": ["факты и числа из источника, которые сохранены"]
}
```
Правила:
- Передавай смысл, факты и цифры точно. Числа, проценты, даты не меняй.
- Формулировки пиши свои, не копируй предложения. Структуру идеи можно сохранить.
- Если утверждение нельзя проверить, пиши «по данным источника» или не включай.
- Не давай персональных инвестиционных советов. Не говори «покупайте» про конкретные активы.
- Азербайджанский: ə, ı, ö, ü, ş, ç, ğ.
- Описание содержит ровно 5 хэштегов (`#...`), иначе отправка остановится.

### 4. Озвучка
```bash
python scripts/tts.py          # work/narration.wav (Gemini TTS)
python scripts/trim.py         # work/narration_trim.wav (паузы >0.4 с -> 0.2 с)
python scripts/align_words.py  # work/words.json (тайминги слов сценария)
```
Проверь длительность `work/narration_trim.wav` (ffprobe). Если она вне 20–60 с, перепиши `narration_az` и повтори шаги 4 (озвучка, обрезка и выравнивание).

### 5. Раскадровка
Напиши `work/storyboard.md`: таблица `таймкод | фраза | что видно | план/ракурс | движение`. Покрой всю озвучку по словам из `work/words.json`. Каждая фраза — своя среда, люди без лиц, полноценные фигуры, действие читается. Никакой музыки.

### 6. Сцена
Сделай `work/scene/index.html` по `templates/scene_template.html`:
- `window.DURATION_SEC` = длительность озвучки + 1.2 с;
- `window.WORDS` = содержимое `work/words.json` (вставь массив в файл);
- `window.renderAt(t)` рисует кадр в стиле бумажного коллажа по `AGENTS.md`. Сохрани `drawSubtitles(t)` поверх кадра (караоке, плашка y≈1540).

Ориентир стиля: `references/2d-video/sheets/sheet_02.png`, `references/2d-video/AGENTS.md`.

### 7. Рендер
```bash
python scripts/render.py       # work/video.mp4, 1080x1920, 24 fps
```
Если рендер упал, исправь сцену и повтори только этот шаг (не больше двух раз).

### 8. Контроль качества (обязательно)
```bash
python tools/make_review_sheets.py work/video.mp4 work/review
```
Затем запусти три субагента из `.claude/agents/` и передай им пути `work/` и `work/review/`:
- `video-quality-reviewer`: смысл, анатомия, движение, соответствие словам, технические параметры;
- `art-director`: стиль бумажного коллажа, цвет, детали, композиция;
- `subtitle-auditor`: караоке, границы слов, текст, плашка.

Исправь все замечания MAJOR/FAIL, пересобери затронутые сцены и повтори проверку. Если субагенты недоступны, проверь сам и явно сообщи в отчёте, что независимая проверка не проводилась.

Проверка финала:
```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt -show_entries format=duration -of default=nw=1 work/video.mp4
```
Ожидаемо: h264, 1080, 1920, 24/1, yuv420p, есть аудио AAC, длительность = озвучка + хвост.

### 9. Отправка в Telegram
```bash
python scripts/notify.py
```
Отправляется видео и текст выдачи (Başlıq, Örtük üçün prompt, Təsvir). Ничего другого.

### 10. Сохранение used.json
`find_trend.py` уже обновил `used.json`. Закоммить и отправь в `main` только его:
```bash
git config user.name "finance-shorts-bot"
git config user.email "finance-shorts-bot@users.noreply.github.com"
git add used.json
git commit -m "Mark video as used: <video_id из work/trend.json>"
git push origin HEAD:main
```
Не коммить `work/`, не создавай ветки и PR.

## Ошибки
```bash
python scripts/notify.py --error --step "<шаг>" --message "<что случилось>"
```
Не выдавай заглушку за готовое видео. Если что-то не получилось, пиши об этом прямо.

## Итог запуска
В конце коротко: ссылка на источник, источник транскрипта (`vidiq` или `youtube_captions`), длительность, результат проверок (какие субагенты запускались и что нашли), отправлено ли в Telegram, что не проверено.
