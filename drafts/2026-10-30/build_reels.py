"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-10-30 from one shared visual plan."""
import json, pathlib

D = "2026-10-30"
HERE = pathlib.Path(__file__).parent
AI = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-10-30T01:30:00Z"
DIELINE = "https://thedieline.com/coca-cola-unveils-newly-refreshed-global-visual-identity-system/"
PRESS = "Image: The Coca-Cola Company (press image, via The Dieline)"
KO = "https://www.coca-colacompany.com/media-center/coca-cola-sharpens-its-identity-under-one-bold-visual-system"
CB = "https://creativebloq.com/news/the-coca-cola-rebrand-is-still-causing-confusion-three-months-on"
PE = "https://www.packagingeurope.com/is-coca-colas-refreshed-packaging-a-success-or-a-mistake/"
FN = "https://www.foodnavigator.com/Article/2011/12/02/Consumers-see-red-over-Coke-s-white-can-campaign/"

EV_KO = [{"url": KO, "publisher": "The Coca-Cola Company (official)", "event_date": "2026-07-20", "retrieved_at": RT,
          "claim": "Unified visual system across more than 200 markets; Rapha Abreu: 'with one seamless visual identity, we can deliver one recognizable brand experience'; Zero Sugar: larger 'Zero Sugar' text, black Dynamic Ribbon on cans, black cap on PET"}]
EV_CB = [{"url": CB, "publisher": "Creative Bloq", "event_date": "2026-10-11", "retrieved_at": RT,
          "claim": "Three months on, Original and Zero Sugar are easy to mix up; Zero's only remaining colour cue is a black ribbon; flight attendant on TikTok: 'lost count of how many wrong Cokes I've handed out this week'; commenters with diabetes/allergy rely on the cue"}]
EV_PE = [{"url": PE, "publisher": "Packaging Europe", "event_date": "2026-07-27", "retrieved_at": RT,
          "claim": "Experts split: praise for a tighter family; concern that the two look extremely similar"}]
EV_FN = [{"url": FN, "publisher": "FoodNavigator", "event_date": "2011-12-02", "retrieved_at": RT,
          "claim": "2011 white holiday cans confused with silver Diet Coke; about a month after launch only red was being shipped; company did not cite confusion as the reason"}]


def obj(key, path, x=540, y=1290, w=420, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": AI}
    o.update(kw); return o


def frame(key, img, ar=1.778, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1280, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "color": [0, 0, 0], "credit": PRESS, "source_url": DIELINE}
    o.update(kw); return o


def words(lang):
    if lang == "fa":
        return [{"type": "words", "mode": "fade", "box": [140, 980, 940, 1460], "seed": 5, "size": 58, "t0": 0.9, "keep_at": [540, 1230],
                 "words": ["سفید", "خرس قطبی", "زمستان", "نقره‌ای", "رژیمی", "قرمز"], "keep": ["قرمز"]}]
    return [{"type": "words", "mode": "fade", "box": [140, 980, 940, 1460], "seed": 5, "size": 58, "t0": 0.9, "keep_at": [540, 1230],
             "words": ["white", "polar bear", "winter", "silver", "diet", "red"], "keep": ["red"]}]


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1280, "fact", EV_KO, [frame("ta", "T-a.png", y=1300, w=880)], None,
     "قلاب با مدرک واقعی (آپلود مالک، قاب‌دار): دو قوطی قرمزِ روی هم که فقط یک سطر ریز فرقشان است = دو قوطی قرمز، یکی بدون قند"),
    ("S2", "paper", None, "interpretation", None, [obj("watch", "2026-10-22/watch", y=1320, w=330, anim="pop")], None,
     "ساعت = فقط یک ثانیه وقت برای انتخاب جلوی قفسه"),
    ("S3", "graphite", 1280, "fact", EV_KO, [frame("tg", "T-g.png")], None,
     "بطری کلاسیک روی روبان قرمز (آپلود مالک) = برند مادر که از دور شناخته می‌شود؛ کاری که یک‌دستی خوب انجام می‌دهد"),
    ("S4", "paper", None, "interpretation", None, [obj("stamp", "2026-10-29/stamp", y=1300, w=330, anim="drop", vibrate=4)], None,
     "مهر لاستیکی که فرود می‌آید = یک نقش، همه‌جا یک‌جور؛ تکرار، حافظه می‌سازد"),
    ("S5", "graphite", 1280, "fact", EV_KO + EV_CB, [frame("td", "T-d.png", anim="slide_r", push=0.03)], None,
     "چرخش ایده: ردیف هفت قوطیِ همه قرمز (آپلود مالک) از راست وارد می‌شود = هفت محصول، یک رنگ"),
    ("S6", "paper", None, "interpretation", None, [obj("roller", "2026-10-26/paint_roller", y=1300, w=560, rot=-6, anim="slide_l")], None,
     "غلتک رنگ که از چپ رد می‌شود = همه‌چیز یک‌رنگ می‌شود و تفاوت‌ها هم زیر رنگ می‌روند"),
    ("S7", "graphite", 1280, "fact", EV_CB, [frame("te", "T-e.png")], None,
     "دستی که قوطی را به دست دیگر می‌دهد (آپلود مالک) = قوطی اشتباه دست‌به‌دست می‌شود؛ بدون نشان‌دادن یا نام‌بردن از کسی"),
    ("S8", "paper", None, "fact", EV_KO + EV_CB, [obj("lens", "2026-10-22/magnifier", y=1350, w=430, rot=-6, anim="pop", float=5)], None,
     "ذره‌بین = تفاوت هست (نوار مشکی، نوشته‌ی درشت‌تر) ولی فقط با دقت دیده می‌شود؛ احتیاط یک بار و کوتاه"),
    ("S9", "graphite", 1290, "interpretation", None, [obj("scale", "2026-10-22/scale", y=1310, w=470, anim="rise", tilt=-5, tilt_t=1.4, bright=[1.4, 1.4])], None,
     "ترازو = دو کفه: شناخته‌شدنِ برند و پیدا‌شدنِ محصول؛ هر دو باید وزن داشته باشند"),
    ("S10", "paper", None, "interpretation", None, [obj("basket", "2026-10-24/basket", y=1320, w=560, anim="drop")], None,
     "سبد خرید که می‌افتد = محصول اشتباه در سبد؛ یک بار خنده، بار سوم بی‌اعتمادی"),
    ("S11", "graphite", 1220, "fact", EV_FN, None, "WORDS",
     "کلمه‌های کمپین ۲۰۱۱ (سفید، خرس قطبی، نقره‌ای، رژیمی) محو می‌شوند و فقط «قرمز» می‌ماند و بزرگ می‌شود = قوطی سفید چند هفته بعد قرمز شد"),
    ("S12", "paper", None, "interpretation", None, [obj("key", "2026-10-24/key", y=1340, w=420, rot=-10, anim="pop")], None,
     "کلید = نشانه‌ای که فقط به یک قفل می‌خورد؛ یک نشانه‌ی بی‌اشتباه برای هر محصول"),
    ("S13", "graphite", 1280, "fact", EV_KO, [frame("tc", "T-c.png")], None,
     "بازگشت به قوطی‌های آغاز: خانواده‌ی محصول با درپوش مشکی (آپلود مالک) = نشانه‌ای که از فاصله‌ی یک دست کار می‌کند؛ تست یک‌ثانیه‌ای"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("دو قوطی قرمز.", "h"), ("یکی *بدون قند* است.", "h")],
    "S2": [("یک ثانیه وقت دارید.", "b"), ("*کدام*؟", "h")],
    "S3": [("یک زبان تصویری در بیش از ۲۰۰ بازار.", "b"), ("از ته راهرو *شناخته* می‌شود.", "h")],
    "S4": [("و این حرکت هوشمندانه‌ای است.", "b"), ("*یک‌دستی* یعنی حافظه.", "h")],
    "S5": [("ولی حالا هفت محصول", "b"), ("یک *رنگ* دارند.", "h")],
    "S6": [("غلتکی که همه‌چیز را یک‌رنگ می‌کند،", "b"), ("*تفاوت‌ها* را هم می‌پوشاند.", "h")],
    "S7": [("آدم‌ها می‌گویند", "b"), ("قوطیِ *اشتباه* دست‌به‌دست می‌شود.", "h")],
    "S8": [("فعلاً روایت است، نه آمار فروش.", "s"), ("فرق هست: نوار مشکی، نوشته‌ی درشت‌تر.", "b"), ("ولی باید *دقیق* نگاه کنید.", "h")],
    "S9": [("برند باید *شناخته* شود؛", "b"), ("محصول باید *پیدا* شود.", "h")],
    "S10": [("یک بار اشتباه، خنده دارد.", "b"), ("بار سوم، *اعتماد* می‌رود.", "h")],
    "S11": [("قوطی سفیدِ زمستانی‌اش هم", "b"), ("چند هفته بعد *قرمز* شد.", "h")],
    "S12": [("به هر محصول یک نشانه بدهید", "b"), ("که *نشود* اشتباهش گرفت.", "h"), ("یک رنگ یا یک فرم، از هر طرف.", "s")],
    "S13": [("از فاصله‌ی یک دست،", "b"), ("در یک *ثانیه* امتحانش کنید.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Two red cans.", "h"), ("One has *zero sugar*.", "h")],
    "S2": [("You have one second.", "b"), ("*Which* one?", "h")],
    "S3": [("One system, 200+ markets.", "b"), ("Known from across the *aisle*.", "h")],
    "S4": [("That part is smart.", "b"), ("Sameness builds *memory*.", "h")],
    "S5": [("But now seven products", "b"), ("wear one *color*.", "h")],
    "S6": [("Paint it all one color,", "b"), ("and *differences* vanish too.", "h")],
    "S7": [("People say the wrong can", "b"), ("keeps getting *handed* out.", "h")],
    "S8": [("So far: stories, not sales data.", "s"), ("The cues: a black ribbon, bigger type.", "b"), ("You just have to *look*.", "h")],
    "S9": [("The brand should be *recognized*.", "b"), ("The product should be *found*.", "h")],
    "S10": [("One mix-up is funny.", "b"), ("The third costs *trust*.", "h")],
    "S11": [("Coke's white winter cans", "b"), ("were *red* again within weeks.", "h")],
    "S12": [("Give every product one cue", "b"), ("nobody can *miss*.", "h"), ("Color or shape, from every side.", "s")],
    "S13": [("Test it at arm's length.", "b"), ("In one *second*.", "h")],
    "S14": [("Write to me.", "b")],
}

SOURCES = [
    {"publisher": "The Coca-Cola Company", "title": "Coca-Cola sharpens its identity under one bold visual system", "date": "2026-07-20", "url": KO},
    {"publisher": "Creative Bloq", "title": "The Coca-Cola rebrand is still causing confusion three months on", "date": "2026-10-11", "url": CB},
    {"publisher": "Packaging Europe", "title": "Is Coca-Cola's refreshed packaging a success or a mistake?", "date": "2026-07-27", "url": PE},
    {"publisher": "FoodNavigator", "title": "Consumers see red over Coke's white can campaign", "date": "2011-12-02", "url": FN},
    {"publisher": "The Dieline", "title": "Coca-Cola unveils newly refreshed global visual identity system (press images)", "date": "2026-07", "url": DIELINE},
]

CAP_FA = """دو قوطی قرمز. یکی بدون قند. یک ثانیه وقت دارید.

کوکاکولا امسال بسته‌بندی‌هایش را در بیش از ۲۰۰ بازار زیر یک نظام تصویری برد. به گفته‌ی خود شرکت، هدف این است که با «یک هویت تصویری یکپارچه» یک تجربه‌ی برندِ قابل‌شناختن بسازد. به نظر من حرکت درستی است: یک‌دستی یعنی حافظه، و برند را از ته راهرو می‌شناسید.

ولی حالا نسخه‌ی معمولی و زیرو شوگر خیلی شبیه هم شده‌اند. تنها نشانه‌ی رنگیِ زیرو یک نوار مشکی است، کنار نوشته‌ای درشت‌تر. سه ماه بعد، آدم‌ها هنوز در شبکه‌های اجتماعی تعریف می‌کنند که قوطی اشتباه برداشته‌اند یا دست کسی داده‌اند؛ چند نفر نوشته‌اند به خاطر دیابت یا حساسیت، به همان نشانه تکیه می‌کنند. یک بار اشتباه خنده دارد؛ بار سوم اعتماد می‌رود.

درسش معماری برند است: نشانه‌های برند مادر برای شناختن، و برای هر محصول یک نشانه‌ی بی‌اشتباه، رنگ یا فرم، که از هر طرف بسته دیده شود. امتحانش ساده است: از فاصله‌ی یک دست، در یک ثانیه.

حدودش را هم بگویم: شواهد سردرگمی فعلاً روایت آدم‌ها و گزارش رسانه‌هاست، نه آمار فروش، و بعضی متخصص‌های بسته‌بندی، خانواده‌ی یک‌دست‌تر را تحسین کرده‌اند. در ۲۰۱۱ هم قوطی‌های سفید زمستانی کوکاکولا را با نسخه‌ی رژیمیِ نقره‌ای اشتباه می‌گرفتند و حدود یک ماه بعد دوباره قرمز شدند؛ شرکت رسماً سردرگمی را دلیلش اعلام نکرد. منبع‌ها: بیانیه‌ی کوکاکولا، Creative Bloq، Packaging Europe و FoodNavigator. عکس‌های واقعی، تصویرهای مطبوعاتی شرکت کوکاکولا‌اند (از طریق The Dieline، آپلود مالک)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

محصول‌های شما از فاصله‌ی یک دست از هم جدا می‌شوند، یا فقط برندتان شناخته می‌شود؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Two red cans. One has zero sugar. You have one second.

This year Coca-Cola moved its packaging in more than 200 markets onto one visual system. In the company's words, "with one seamless visual identity, we can deliver one recognizable brand experience." My take: that part is smart. Consistency is memory, and you know the brand from across the aisle.

But Original and Zero Sugar now look very alike. Zero's only color cue left is a black ribbon, next to bigger type. Three months in, people are still posting about grabbing, or handing out, the wrong can. A few say they rely on that cue because of diabetes or an allergy. One mix-up is funny. The third one costs trust.

The lesson is brand architecture: masterbrand cues so people recognize you, and one unmistakable cue per product, a color or a shape, visible from every side of the pack. The test is simple: arm's length, one second.

The limits: the evidence of confusion is stories and press coverage, not sales data, and some packaging experts praise the tighter family. In 2011, Coke's white winter cans were mistaken for silver Diet Coke and went back to red about a month later; the company never named confusion as the reason. Sources: The Coca-Cola Company, Creative Bloq, Packaging Europe, FoodNavigator. The real photos are Coca-Cola press images (via The Dieline, owner uploads); the other objects are AI-generated.

At arm's length, can your customers tell your products apart, or only recognize your brand? Write to me.

— Behnood Kavian"""


def build(lang):
    copy = FA if lang == "fa" else EN
    scenes = []
    for sid, bg, spot, ct, ev, objs, fx, why in PLAN:
        s = {"id": sid, "bg": bg}
        if spot: s["spot_y"] = spot
        s["claim_type"] = ct
        if ev: s["evidence"] = ev
        if objs: s["objects"] = json.loads(json.dumps(objs))
        if fx: s["fx"] = words(lang)
        s["motion_rationale"] = why
        if sid == "S14": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        scenes.append(s)
    return {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
            "topic": "وقتی برند آن‌قدر یک‌دست می‌شود که محصول گم می‌شود" if lang == "fa" else "When your brand gets so consistent your products disappear",
            "pillar": "brand_architecture_packaging", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
            "caption": CAP_FA if lang == "fa" else CAP_EN,
            "hashtags": ["#برندینگ", "#بازاریابی", "#packagingdesign", "#brandstrategy"] if lang == "fa" else ["#branding", "#marketing", "#packagingdesign", "#brandstrategy"],
            "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
            "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}


for n, lang in ((1, "fa"), (2, "en")):
    (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
print("ok")
