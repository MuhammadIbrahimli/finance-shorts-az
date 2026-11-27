Find one animated finance TikTok video for a broad audience through the vidIQ connector and save it to `work/trend.json`.

Step 1. Call `vidiq_instagram_tiktok_outlier_search` exactly once with these parameters:
- `query`: "animated money finance explained for beginners"
- `audienceQuery`: "Culture/Region: global; Global: true; Demographics: general audience 18-35 interested in personal finance;"
- `datePostedAfter`: "{CUTOFF}"
- `excludeContentIds`: {USED_IDS}
- `durationMax`: 90
- `resultsPerPlatform`: 10
- `embeddingType`: "concept"

Step 2. From the TikTok section (not Instagram), select ONE video using these rules:
- It is animated (animated characters, graphics, or cartoons, not live people with voiceover).
- It explains finance or tells a finance story for a broad audience (compound interest, budgeting, habits, credit), not news or market forecasts.
- It is not already among the works listed in `excludeContentIds`.
- Among qualifying results, choose the one with the most views.
If there are no qualifying TikTok results, do NOT write a file; reply on one line: “NO SUITABLE TIKTOK RESULTS”. Do not substitute an Instagram result.

Step 3. Write `work/trend.json` (UTF-8 JSON object) with these fields:
```json
{
  "source": "tiktok_vidiq",
  "video_id": "<TikTok video ID from the result>",
  "url": "<full link such as https://www.tiktok.com/@handle/video/<id>>",
  "title": "<title from result>",
  "description": "<description from result>",
  "channel": "<creator's @handle>",
  "view_count": 0,
  "published_at": "<publication date from result>",
  "duration_sec": 0
}
```
Use values from vidIQ results. Do not invent anything: if a field is missing in the result, set it to `null`.

After saving, reply with one line containing the selected video's URL. Do not send anything to Telegram or commit.