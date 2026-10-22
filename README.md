# Behnood Editorial Studio — deterministic renderer prototype

python3 make_sample.py && python3 render.py samples/sample_post.json out && python3 qa.py samples/sample_post.json out/TEST_POST_01

- `render.py`  post JSON -> 1080x1350 PNG (Chromium, real DoranFaNum, untouched logo PNGs) + editable HTML + layout_metrics.json
- `qa.py`      machine-checkable gates -> qa_report.json (READY_FOR_REVIEW / BLOCKED_QA)
- `persian_text.py` normaliser + orthography lint (Posht-e-Bam rules)
- `brand_config.json`, `slide_brief.schema.json`, `post.schema.json` — v2.1

Open items: logo not owner-confirmed (aspect mismatch between files), font licence unconfirmed,
no image generation / research / scheduling yet, QA cannot judge prose, orthography nuance or art.

## Daily run
`python3 render.py <post.json> out && python3 qa.py <post.json> out/<post_id>` for each post, then
`python3 package.py YYYY-MM-DD post1.json post2.json`. Posts are written to `drafts/YYYY-MM-DD/` following `post.schema.json`.

## Copy
All Persian copy follows `copywriting.md` (voice, hooks, rhythm, banned phrases, self-review). Ashouri's prose guide is no longer used; Posht-e-Bam stays for orthography.

## Daily reels (current format)
Two 40-60s reels per day, 1080x1920, 30fps. Per reel: write `drafts/DATE/reel_0N.json` (schema: see `make_sample_reel.py`; copy rules `copywriting.md`; motion rules `motion.md`), then
`python3 reel_render.py drafts/DATE/reel_0N.json out && python3 reel_qa.py drafts/DATE/reel_0N.json out/<reel_id>`, then
`python3 package_reels.py DATE drafts/DATE/reel_01.json drafts/DATE/reel_02.json`.
Music: generative, moods `reflective` or `dark` only. End card: logo, «برای من بنویسید.», «بهنود کاویان». Never name the UAE in copy.

Visual style (since 2026-10-22): editorial objects + topic-word typography (`reel_visuals.js`, rules in `motion.md`). AI-generated monochrome objects live in `assets/objects/DATE/` (cut out with rembg). Abstract motifs are a fallback only.

## Daily format (from 2026-10-23)
One topic per day in **branding, brand strategy or marketing**, two reels on the same idea and the same visual plan:
- `drafts/DATE/reel_01.json`: Persian, `"lang": "fa"`, copy rules `copywriting.md`, CTA «برای من بنویسید.», signature «بهنود کاویان».
- `drafts/DATE/reel_02.json`: English, `"lang": "en"`, copy rules `copywriting_en.md` (written natively, not translated), CTA «Write to me.», signature «Behnood Kavian», Latin font Inter (`assets/fonts/inter`, OFL).
Reference samples: `samples/sample_reel.json` (fa), `samples/sample_reel_en.json` (en). The renderer switches direction, font and signature by `lang`; QA lints each language with its own rules.

## Voice-over (Azure Speech)
**English reel only** (owner: the Persian reel stays as it is, music without voice). `reel_voice.py` adds a male narrator per scene and ducks the music under it. Voice: `en-US-AndrewNeural`; rate -6 %, pitch -3 % for a soft, warm read. Enable with `"voice": {"enabled": true}` in the reel JSON; a scene can set `"vo"` to the exact spoken sentence (e.g. numbers written out, smoother spoken order). Scene length grows to fit the voice. Requires `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` in the environment and network access to `<region>.tts.speech.microsoft.com`; without them the reel renders without a voice (QA blocks a reel that requested a voice and did not get one). Clips are cached in `out/_vo_cache/`.
