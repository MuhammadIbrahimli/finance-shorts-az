Retrieve the voiceover text from the selected TikTok video through the vidIQ connector and save it for writing a new script.

Link: {TREND_URL}

Step 1. Call `vidiq_watch_shortform_content` with `url` equal to the link above and this prompt:
```
Transcribe all spoken narration and on-screen text verbatim, in order. Plain text only, no timestamps, no scene descriptions.
```
The tool is asynchronous and will return an `mcpJobId`.

Step 2. Poll `vidiq_job_poll` with that `mcpJobId` until the status becomes `completed`. If the status is `failed`, or after more than 10 polls there is still no result, stop and reply: “VIDIQ ERROR: <reason>”.

Step 3. Write the result to `work/transcript.txt` (UTF-8): spoken words and on-screen text only, in order, with no timecodes, scene descriptions, or tags such as `[music]`. If the result contains only scene descriptions and no speech, state that in the report and do not write the file.

Step 4. Write `work/transcript_meta.json`: `{"video_id": "<from work/trend.json>", "source": "vidiq_tiktok", "chars": <text length>}`.

Constraints: use this only as a source of ideas and facts for a new script. Do not copy wording or use the original footage, music, or audio. Do not send anything to Telegram or commit.