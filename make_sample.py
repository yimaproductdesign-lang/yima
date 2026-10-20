"""Generates samples/sample_post.json -- a TEST post (interpretive copy, no factual claims, no external sources)."""
import json, pathlib

Z = "‌"
S = [  # role, layout, bg, headline, body, claim_type, claim
    ("hook", "cover", "primary", f"برند شما لوگو نیست؛ سیستمی از تصمیم{Z}هاست.", "", "interpretation", "برند مجموعه‌ای از تصمیم‌های هماهنگ است، نه یک نشانه."),
    ("question", "question", "paper", f"چرا برندهایی با لوگوی زیبا هنوز مبهم{Z}اند؟", "", "question", "زیبایی نشانه برابر با وضوح معنا نیست."),
    ("context", "body", "primary", "مشتری لوگو را تنها نمی‌بیند.", f"او رنگ، لحن، قیمت، سرعت پاسخ و تجربه{Z}ی تحویل را کنار هم می{Z}خواند.", "interpretation", "مخاطب نشانه‌ها را در کنار هم تفسیر می‌کند."),
    ("insight", "body", "paper", "معنا را گیرنده می‌سازد.", f"فرستنده فقط نشانه می{Z}فرستد؛ رمزگشایی در ذهن مخاطب رخ می{Z}دهد.", "interpretation", "در مدل ارتباط، معنا در رمزگشایی ساخته می‌شود."),
    ("tension", "body", "graphite", "هر ناهم‌خوانی کوچک، نویز است.", f"رنگی که با لحن نمی{Z}خواند، وعده{Z}ای که با تحویل نمی{Z}خواند.", "metaphor", "ناهم‌خوانی را می‌توان نویز در کانال ارتباط دید."),
    ("practice", "body", "primary", "یک آزمون ساده.", f"سه نقطه{Z}ی تماس برندتان را کنار هم بگذارید. اگر بدون لوگو هم بشود فهمید که از یک برندند، سیستم دارید.", "interpretation", "آزمون تشخیص بدون لوگو معیار انسجام است."),
    ("conclusion", "statement", "paper", "انسجام یعنی معنا، فرم و کاربرد یک حرف بزنند.", "", "interpretation", "انسجام = هم‌راستایی معنا، فرم و کاربرد."),
    ("prompt", "closing", "primary", f"کدام نقطه{Z}ی تماس برند شما بیشترین نویز را دارد؟", "برای ما بنویسید.", "question", "پرسش گفت‌وگوآفرین."),
]
slides = []
for i, (role, layout, bg, h, b, ct, claim) in enumerate(S, 1):
    slides.append({
        "post_id": "TEST_POST_01", "slide_number": i, "role": role, "layout": layout,
        "headline": h, "body": b, "central_claim": claim, "claim_type": ct,
        "background": {"mode": bg},
        "visual_metaphor": "تایپوگرافی‌محور؛ در این نمونه تصویر مفهومی تولید نشده است",
        "art_direction": {
            "thesis": claim, "subject": "فقط تایپوگرافی و فضای خالی", "framing": "قاب بسته، بدون سوژه",
            "composition": "بلوک متن در ناحیه‌ی تعیین‌شده، فضای منفی آزاد", "lighting": "تخت",
            "contrast": "بالا", "negative_space": "حداقل ۴۰٪ قاب", "typography_zone": "center" if layout in ("cover", "statement", "question", "closing") else "bottom",
            "why_this_image": "نمونه‌ی آزمون رندرر؛ بدون تصویر", "forbidden_cliche": "لامپ، دست‌دادن، نمودار صعودی"},
        "evidence": [], "qa_status": "DRAFT"})
post = {
    "post_id": "TEST_POST_01", "date": "2026-10-21", "topic": "انسجام: هویت به‌مثابه‌ی سیستم (نمونه‌ی آزمون)",
    "pillar": "brand_visual_strategy",
    "selection": {"score_total": 0, "score_breakdown": {}, "confidence": "low", "topic_kind": "evergreen", "trend_verified": False},
    "slides": slides,
    "caption": "نمونه‌ی آزمون رندرر؛ متن واقعی نیست.",
    "cta": "کدام نقطه‌ی تماس برند شما بیشترین نویز را دارد؟",
    "alt_text": [f"اسلاید {i}" for i in range(1, 9)],
    "status": "DRAFT"}
pathlib.Path("samples").mkdir(exist_ok=True)
pathlib.Path("samples/sample_post.json").write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf8")
print("ok")
