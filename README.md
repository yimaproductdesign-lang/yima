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
