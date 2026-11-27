# Images: Conditional Provider Selection

Read this only when images/reference editing are needed. The supplied research is dated **2026-10-16**. Documentation was checked; practical character-identity preservation was not tested. The information below does not configure integrations or imply account access. Use an already available permitted tool; registration, MCP/API access, or a local backend is not enabled automatically. If one route is unavailable, choose another while preserving the production plan and stating real limitations.

## Main candidates

### Krea — ready MCP candidate

[Official instructions](https://www.krea.ai/docs/developers/mcp), endpoint: https://api.krea.ai/mcp.
MCP through OAuth uses workspace compute units; an API token uses a **separate paid API balance**. Do not confuse these billing methods.

According to [pricing](https://www.krea.ai/pricing), Free provides 100 units daily without a card. The page's estimates are about 25 Klein or 5 Krea 3 Beta images per day; this is **not a guaranteed number of reference edits**. Do not promise free Nano Banana/GPT Image. MCP describes discovery/schema, references via URL/base64/upload, jobs, and retrieving results; check the selected tool's actual schema before calling it.

[Krea 3](https://www.krea.ai/blog/introducing-krea-3) claims up to 6 references; character consistency was not tested in the research. Commercial licensing is listed for paid plans; treat Free as a personal testing option and do not promise it is suitable for a monetized final. Native alpha is unconfirmed: download the result and, if needed, remove the background locally while checking edges.

### Cloudflare Workers AI — REST candidate, not a ready general-purpose MCP

[Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/): Free provides 10,000 neurons/day, reset at 00:00 UTC, with no paid overage on Free; the [product page](https://www.cloudflare.com/products/workers-ai/) says no card is required. Neurons are compute units, **not a count of finished images**.

For [FLUX.2 Klein 4B](https://developers.cloudflare.com/workers-ai/models/flux-2-klein-4b/), the [schema announcement](https://developers.cloudflare.com/changelog/post/2026-01-15-flux-2-klein-4b-workers-ai/) describes multipart input with up to 4 binary fields named input_image_0 through input_image_3; each reference must be **under 512×512**; output dimensions are 256–1920 and the result is base64. Do not substitute a different schema or model limit.

The [REST API](https://developers.cloudflare.com/workers-ai/get-started/rest-api/) requires a narrow adapter/script in a suitable client if separately authorized. The generic https://mcp.cloudflare.com/mcp endpoint was not verified for this workflow; do not promise a turnkey MCP. Native alpha is unconfirmed.

### Web interfaces as fallback

[Gemini web](https://support.google.com/gemini/answer/14286560?hl=en) describes reference editing and downloads; [limits can change](https://support.google.com/gemini/answer/16275805?hl=en). This is **not a free image API**; [API pricing](https://ai.google.dev/gemini-api/docs/pricing) is separate. Automation is possible only if an actual browser tool is available; ordinary chat does not imply browser access.

[Images in ChatGPT](https://help.openai.com/en/articles/11084440-images-in-chatgpt) is a similar web fallback, including requests for transparency. ChatGPT Free does not mean a free API, and a transparency request does not replace checking the result's alpha channel.

## Additional options and free-tier limits

| Option | What documentation confirms and what not to promise |
|---|---|
| [Leonardo pricing](https://leonardo.ai/pricing) | 150 tokens/day, free creations are public, API is separate. [Image guidance](https://intercom.help/leonardo-ai/en/articles/8497988-image-guidance) is Limited. [Transparency](https://intercom.help/leonardo-ai/en/articles/9075772-transparency) is described for eligible SD1.5/SDXL; reference+alpha on Free must be tested. |
| [Ideogram plans](https://docs.ideogram.ai/plans-and-billing/available-plans.md) | 30 credits/week with Google/Apple/Microsoft login; free creations are public. Do not promise a free API. |
| [Hugging Face Inference](https://huggingface.co/docs/inference-providers/main/pricing) and [ZeroGPU Spaces](https://huggingface.co/docs/hub/main/spaces-zerogpu) | $0.10/month in Inference; Spaces have queues and quotas. Not a reliable production backend by default. |
| [Pollinations Pollen FAQ](https://raw.githubusercontent.com/pollinations/pollinations/main/enter.pollinations.ai/POLLEN_FAQ.md) | Purchased/earned Pollen. Do not treat it as unlimited or as a free daily image API. |
| [Recraft Free](https://www.recraft.ai/docs/plans-and-billing/free-plan) | Limited free plan without a commercial license; do not promise a free commercial final. |
| Replicate / fal | Trials are not recurring free access. Do not list them as permanently free without newly checking the specific offer. |

## Optional local route

[ComfyUI MCP](https://docs.comfy.org/agent-tools/mcp), a small SD1.5/IPAdapter setup, and [rembg](https://github.com/danielgatis/rembg) are a separate option when a suitable environment is already available or setup is explicitly authorized. Do not install automatically. Do not promise powerful image-editing models on an RTX 3050 6 GB: the supplied research lists an 8.4 GB VRAM benchmark for the standard Klein 4B, above this card's memory.

Use the same canonical references for each new pose rather than a chain of increasingly drifting generations. For smooth motion, animating a consistent cutout/rig is often better than generating each frame independently. Check real alpha and edges on light/dark backgrounds: PNG alone does not imply transparency. Full workflow: [image continuity](image-continuity.md).

Briefly report the provider/model actually used, available route, date limitations were checked, and source/terms. VidIQ may be an optional audio source for a future authorized task; it is not a universal dependency and is not claimed to be unconditionally free. No voice was selected for the user, and no generation is performed while preparing this revision.
