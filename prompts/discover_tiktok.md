Найди один анимированный финансовый TikTok-ролик для широкой аудитории через коннектор vidIQ и запиши его в work/trend.json.

Шаг 1. Вызови инструмент vidiq_instagram_tiktok_outlier_search ровно один раз со следующими параметрами:
- query: "animated money finance explained for beginners"
- audienceQuery: "Culture/Region: global; Global: true; Demographics: general audience 18-35 interested in personal finance;"
- datePostedAfter: "{CUTOFF}"
- excludeContentIds: {USED_IDS}
- durationMax: 90
- resultsPerPlatform: 10
- embeddingType: "concept"

Шаг 2. Из секции TikTok (не Instagram) выбери ОДНО видео по правилам:
- это анимация (анимированные персонажи, графика, мультипликация, а не живые люди с озвучкой);
- это финансовое объяснение или история для широкой аудитории (сложные проценты, бюджет, привычки, кредиты), а не новости и не прогнозы рынка;
- оно не из работ, уже перечисленных в excludeContentIds;
- среди подходящих выбери с наибольшим количеством просмотров.
Если подходящих TikTok-результатов нет, НЕ записывай файл и ответь одной строкой «НЕТ ПОДХОДЯЩИХ TIKTOK». Не подставляй Instagram вместо TikTok.

Шаг 3. Запиши work/trend.json (UTF-8, JSON-объект) с полями:
{
  "source": "tiktok_vidiq",
  "video_id": "<id TikTok-видео из результата>",
  "url": "<полная ссылка вида https://www.tiktok.com/@handle/video/<id>>",
  "title": "<заголовок из результата>",
  "description": "<описание из результата>",
  "channel": "<@handle автора>",
  "view_count": <число просмотров>,
  "published_at": "<дата публикации из результата>",
  "duration_sec": <длительность в секундах>
}
Значения бери из результата vidIQ. Ничего не выдумывай: если поля нет в результате, ставь null.

Ответ после записи — одна строка: url выбранного видео. Не отправляй ничего в Telegram и не коммить в git.
