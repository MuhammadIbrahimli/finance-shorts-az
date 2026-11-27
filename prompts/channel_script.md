Write a short-video script in Azerbaijani for the Daxilde channel. Work in the repository's current directory.

Read first:
1. `channels/daxilde/AGENTS.md` — channel rules (topics: psychology, neuroscience, health; style, subtitles, delivery, profanity).
2. `work/trend.json` — selected source TikTok video (channel, link, views).
3. `work/transcript.txt` — transcript obtained through vidIQ; source of the idea and facts.

Script rules:
- Use the source only for ideas and facts. Do not copy its wording, dialogue order, or structure. Write original text.
- Remove profanity completely: rewrite the sentence without it, without euphemistic substitutes or asterisks.
- Verify facts, numbers, and names. Do not invent studies or figures. Qualify disputed claims with “according to some sources” or omit them.
- No medical advice or diagnoses; do not urge viewers to take medication.
- The audience is broad. Use simple language and one central image per phrase.

Write `work/script.json` in UTF-8 with exactly these fields:
```json
{
  "source_url": "from work/trend.json",
  "theme": "psychology | neuroscience | health",
  "accent": "amber | red | cyan | peach | mint (scene accent per channel rules)",
  "title_az": "Başlıq: up to 90 characters",
  "cover_prompt_az": "Örtük üçün prompt: a 9:16 cover prompt in the Kahlo's Notebook style, text below the frame center, decorative typography (see channel rules)",
  "description_az": "Təsvir: 2–4 sentences, then EXACTLY 5 hashtags (#...)",
  "narration_az": "voiceover, 80–110 words, about 40–55 seconds",
  "key_facts": ["verified facts and figures used"],
  "metaphors": ["3–5 visual metaphors for scenes"]
}
```

After saving, validate the JSON with `python -c "import json;json.load(open('work/script.json',encoding='utf-8'));print('ok')"` and confirm that `description_az` has exactly five hashtags.

Do not send anything to Telegram or commit. Briefly report the file path and list `key_facts`.