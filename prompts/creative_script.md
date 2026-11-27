Write a short finance-video script in Azerbaijani for the Disli Hardz channel.

Read first: `AGENTS.md` (channel rules), `work/trend.json`, and `work/transcript.txt` (source of the idea).

Rules:
- Use the source only for ideas and facts. Do not copy its wording, dialogue structure, music cues, or shots. Write original text.
- Verify facts and figures yourself (for example, calculate compound interest explicitly). Do not invent data.
- Do not give personalized investment advice. General educational content is allowed.
- The audience is broad. Use simple language and clear examples.
- Remove profanity completely: rewrite the sentence without profanity; do not replace it with euphemisms.

Write `work/script.json` in UTF-8 with exactly these fields:
```json
{
  "source_url": "from work/trend.json",
  "title_az": "Başlıq: up to 90 characters",
  "cover_prompt_az": "Örtük üçün prompt: an Azerbaijani 9:16 cover prompt in the video's style, text below the frame center, decorative typography",
  "description_az": "Təsvir: 2–4 sentences, then EXACTLY 5 hashtags (#...)",
  "narration_az": "voiceover, 80–110 words, about 40–55 seconds",
  "key_facts": ["verified figures and facts used"]
}
```

After saving, validate the JSON with `python -c "import json;json.load(open('work/script.json',encoding='utf-8'));print('ok')"` and confirm there are exactly five hashtags in `description_az`.

Do not send anything to Telegram or commit. Briefly report the file path and list `key_facts`.