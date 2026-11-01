"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-01 from one shared visual plan."""
import json, pathlib

D = "2026-11-01"
HERE = pathlib.Path(__file__).parent
AI = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-01T01:40:00Z"
AW = "https://www.adweek.com/brand-marketing/mcdonalds-ends-32-year-fifa-world-cup-sponsorship-amid-marketing-overhaul/"
NRN = "https://www.nrn.com/quick-service/mcdonald-s-is-ending-its-fifa-world-cup-sponsorship"
CL = "https://campaignlive.com/article/mcdonalds-taps-beckham-pulisic-world-cup-collectible-cup-campaign/1960190"
MD = "https://www.marketingdive.com/news/what-mcdonalds-dropping-its-fifa-sponsorship-means-for-sports-marketing/872775/"

EV_AW = [{"url": AW, "publisher": "Adweek", "event_date": "2026-10-23", "retrieved_at": RT,
          "claim": "McDonald's is ending its FIFA World Cup sponsorship after 32 years; 'biggest-ever World Cup campaign this summer'; by Wieden+Kennedy New York, more than 110 countries; CFO Ian Borden: 'provided a lift to the business ... [it] underperformed versus our expectations'"}]
EV_NRN = [{"url": NRN, "publisher": "Nation's Restaurant News", "event_date": "2026-10-26", "retrieved_at": RT,
           "claim": "CMO Morgan Flatley: 'I think we've become overly reliant on borrowed IP'; 'we need to be very selective and do it a few times'; involved since 1994"}]
EV_CL = [{"url": CL, "publisher": "Campaign", "event_date": "2026-06", "retrieved_at": RT,
          "claim": "Nine collectible cups: eight players from the ads plus Grimace; designed with Ilovedust; ads by Wieden+Kennedy New York"}]

CRED = "Image: McDonald's FIFA World Cup 26 campaign (via Campaign)"


def obj(key, path, x=540, y=1290, w=420, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": AI}
    o.update(kw); return o


def frame(key, img, ar, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1300, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "color": [0, 0, 0], "credit": CRED, "source_url": CL}
    o.update(kw); return o


WORDS = {
    "S3": {"fa": (["ستاره‌ها", "جام", "استادیوم", "هیاهو", "چهره‌های مشهور", "قرضی"], ["قرضی"]),
           "en": (["stars", "trophy", "stadium", "hype", "famous faces", "borrowed"], ["borrowed"])},
    "S9": {"fa": (["قرارداد", "استادیوم", "ستاره", "پوستر", "هیاهو", "مال خودتان"], ["مال خودتان"]),
           "en": (["contract", "stadium", "stars", "poster", "hype", "yours"], ["yours"])},
}


def words(sid, lang):
    w, k = WORDS[sid][lang]
    f = {"type": "words", "mode": "fade", "box": [140, 1000, 940, 1460], "seed": 11 if sid == "S3" else 5, "size": 56, "t0": 0.9,
         "words": w, "keep": k}
    if len(k) == 1: f["keep_at"] = [540, 1240]
    return [f]


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1300, "fact", EV_AW + EV_CL, [frame("ta", "T-a.jpg", 1.876, y=1300, w=900)], None,
     "قلاب با تصویر واقعی کمپین (آپلود مالک، قاب‌دار): ستاره‌ها روی نیمکت، جام کنارشان = بزرگ‌ترین مهمانی؛ و درست بعدش رفتن"),
    ("S2", "paper", None, "fact", EV_AW + EV_NRN, [obj("ball", f"{D}/football", y=1300, w=440, anim="drop", float=4)], None,
     "توپ چرمی کهنه = ۳۲ سال کنار بازی؛ کهنگی توپ یعنی زمان طولانی همراهی"),
    ("S3", "graphite", 1240, "fact", EV_NRN, None, "S3",
     "کلمه‌های شهرت قرضی (ستاره، جام، استادیوم، هیاهو) محو می‌شوند و فقط «قرضی» می‌ماند = تشخیص خود مدیر بازاریابی"),
    ("S4", "paper", None, "fact", EV_AW, [obj("scale", "2026-10-22/scale", y=1320, w=480, anim="rise")], None,
     "ترازو = انصاف و سنجش؛ اثر داشت ولی کفه‌ی انتظار سنگین‌تر بود (احتیاط یک بار، کوتاه)"),
    ("S5", "graphite", 1290, "fact", EV_CL, [frame("cups", "T-c_cups.jpg", 0.805, y=1270, w=440, credit="Image: McDonald's World Cup collectible cups (owner upload)")], None,
     "چرخش (drop): عکس واقعی لیوان‌های کلکسیونی (آپلود مالک، قاب‌دار) با چهره‌ی ستاره‌ها = لیوان، نه جام؛ چهره‌های قرضی روی محصول خودشان"),
    ("S6", "paper", None, "interpretation", None, [obj("suit", f"{D}/suit", y=1290, w=470, anim="drop", float=3)], None,
     "کت روی چوب‌لباسی با برچسب کرایه = شهرت قرضی برازنده است ولی پس داده می‌شود"),
    ("S7", "graphite", 1300, "interpretation", None, [obj("trophy", "2026-10-24/trophy", y=1310, w=360, anim="rise", bright=[1.4, 1.4])], None,
     "جام زیر نور = تشویق و پیروزی مال صاحب صحنه است، نه کسی که کنارش ایستاده"),
    ("S8", "paper", None, "interpretation", None, [obj("ticket", "2026-10-31/ticket", y=1300, w=540, rot=-5, anim="pop", float=5)], None,
     "ته‌بلیت = قرارداد حمایت مثل بلیت است؛ تاریخ دارد و تمام می‌شود"),
    ("S9", "graphite", 1240, "interpretation", None, None, "S9",
     "کلمه‌های قرضی (قرارداد، استادیوم، ستاره، پوستر) محو می‌شوند و فقط «مال خودتان» می‌ماند و بزرگ می‌شود؛ شخصیت، صدا و آیین در تیتر"),
    ("S10", "paper", None, "interpretation", None, [obj("sieve", "2026-10-22/sieve", y=1300, w=560, rot=-8, anim="slide_r")], None,
     "صافی = گزینش؛ «خیلی گزیده و چند بار» (حرف خود مدیر بازاریابی)، نه هرگز"),
    ("S11", "graphite", 1300, "interpretation", None, [obj("tag", "2026-10-25/price_tag", y=1310, w=420, rot=6, anim="pop", bright=[1.4, 1.4])], None,
     "برچسب قیمت = بهای اجاره‌ی نور صحنه؛ پیش از پرداخت بپرس چه برایت می‌ماند"),
    ("S12", "paper", None, "interpretation", None,
     [obj("ball", f"{D}/football", x=330, y=1360, w=300, anim="slide_l"),
      obj("house", "2026-10-29/mini_house", x=750, y=1290, w=230, anim="rise", delay=0.3)], None,
     "بازگشت به آغاز: توپ (بازی دیگران) برمی‌گردد کنار خانه‌ای که ساخته می‌شود = تشویق اجاره‌ای، اسم ساختنی"),
    ("S13", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("بزرگ‌ترین کمپین جام جهانی‌اش را ساخت.", "b"), ("بعد، *رفت*.", "h")],
    "S2": [("۳۲ سال ایستاد کنار", "b"), ("بزرگ‌ترین *بازی* دنیا.", "h")],
    "S3": [("مدیر بازاریابی‌اش گفت:", "b"), ("«زیادی به اعتبار *قرضی* تکیه کرده‌ایم.»", "h")],
    "S4": [("انصافاً بی‌اثر نبود؛ کمکش کرد.", "b"), ("فقط *کمتر* از انتظارش.", "h")],
    "S5": [("به لیوان‌های کلکسیونی‌اش نگاه کنید.", "b"), ("هشت ستاره. *یکی* از خودشان.", "h")],
    "S6": [("شهرت قرضی، کت کرایه‌ای است.", "b"), ("برازنده است. ولی *پس‌دادنی*.", "h")],
    "S7": [("تشویق مال کسی است", "b"), ("که *صحنه* مال اوست.", "h")],
    "S8": [("قرارداد حمایت، بلیت است.", "b"), ("*تاریخ انقضا* دارد.", "h")],
    "S9": [("آنچه می‌ماند، مال خودتان است:", "b"), ("شخصیت، صدا، *آیین*.", "h")],
    "S10": [("نمی‌گویم هیچ‌وقت حامی نشوید.", "b"), ("*کم*، و آگاهانه.", "h")],
    "S11": [("پیش از اجاره‌ی نور صحنه بپرسید:", "b"), ("خاموش که شد، *چه* برایم می‌ماند؟", "h")],
    "S12": [("تشویق را می‌شود اجاره کرد.", "b"), ("اسم را باید *ساخت*.", "h")],
    "S13": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Their biggest World Cup campaign ever.", "b"), ("Then they *walked away*.", "h")],
    "S2": [("32 years beside", "b"), ("the world's biggest *game*.", "h")],
    "S3": [("Their marketing chief:", "b"), ("“overly reliant on *borrowed* IP.”", "h")],
    "S4": [("Fair: it gave “a lift.”", "b"), ("Just *less* than expected.", "h")],
    "S5": [("Look at the collectible cups.", "b"), ("Eight stars. *One* of their own.", "h")],
    "S6": [("Borrowed fame is a rented suit.", "b"), ("It fits. Then it goes *back*.", "h")],
    "S7": [("The applause goes to", "b"), ("whoever *owns* the stage.", "h")],
    "S8": [("A sponsorship is a ticket.", "b"), ("It has an *end date*.", "h")],
    "S9": [("What stays is yours:", "b"), ("character, sound, *ritual*.", "h")],
    "S10": [("I'm not saying never.", "b"), ("Do it *rarely*, on purpose.", "h")],
    "S11": [("Before you rent a spotlight, ask:", "b"), ("what's *mine* when it's off?", "h")],
    "S12": [("You can rent the applause.", "b"), ("You have to *build* the name.", "h")],
    "S13": [("Write to me.", "b")],
}

SOURCES = [
    {"publisher": "Adweek", "title": "McDonald's Ends 32-Year FIFA World Cup Sponsorship Amid Marketing Overhaul", "date": "2026-10-23", "url": AW},
    {"publisher": "Nation's Restaurant News", "title": "McDonald's is ending its FIFA World Cup sponsorship", "date": "2026-10-26", "url": NRN},
    {"publisher": "Campaign", "title": "McDonald's taps Beckham, Pulisic for World Cup collectible cup campaign (image T-a)", "date": "2026-06", "url": CL},
    {"publisher": "Marketing Dive", "title": "What McDonald's dropping its FIFA sponsorship means for sports marketing (context)", "date": "2026-10-27", "url": MD},
]

CAP_FA = """بزرگ‌ترین کمپین جام جهانی‌اش را ساخت. بعد، رفت.

مک‌دونالد ۳۲ سال حامی جام جهانی فیفا بود. تابستان امسال بزرگ‌ترین کمپین جام جهانی تاریخش را در بیش از ۱۱۰ کشور اجرا کرد و حالا این همکاری را تمام می‌کند. مورگان فلتلی، مدیر ارشد بازاریابی جهانی‌اش، گفته: «فکر می‌کنم بیش از حد به اعتبار قرضی (IP قرضی) تکیه کرده‌ایم.»

به لیوان‌های کلکسیونی نگاه کنید: نُه لیوان؛ هشت تا با چهره‌ی ستاره‌های فوتبال، یکی با گریمس، شخصیتِ خودِ مک‌دونالد. کل درس در همین یک ردیف است. شهرت قرضی کت کرایه‌ای است؛ برازنده است، ولی پس‌دادنی. تشویق مال کسی است که صحنه مال اوست، و قرارداد حمایت تاریخ انقضا دارد. آنچه می‌ماند مال خودتان است: یک شخصیت، یک صدا، یک آیین، اسمی که مشتری جست‌وجویش می‌کند.

به نظر من حرف این نیست که هیچ‌وقت حامی نشوید. خود فلتلی گفته باید «خیلی گزیده و فقط چند بار» این کار را کرد. پیش از این‌که برای نور صحنه‌ی دیگران پول بدهید (یک رویداد، یک غرفه، یک چهره‌ی مشهور)، بپرسید خاموش که شد، چه برایتان می‌ماند.

حدودش را هم بگویم: کمپین شکست نخورد. ایان بوردن، مدیر مالی شرکت، گفته به کسب‌وکار «رونق داد» ولی «کمتر از انتظار ما» عمل کرد. منبع‌ها: Adweek، Nation's Restaurant News، Campaign و Marketing Dive. دو قاب واقعی از تصاویر کمپین جام جهانی مک‌دونالد است (آپلود مالک؛ عکس نیمکت به نقل از Campaign)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

اگر فردا همه‌ی حامی‌ها، شریک‌ها و چهره‌های مشهور از کنار کسب‌وکارتان بروند، چه چیزی هنوز مال خودتان است؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Their biggest World Cup campaign ever. Then they walked away.

McDonald's has stood next to the FIFA World Cup for 32 years. This summer it ran its biggest-ever World Cup campaign, built by Wieden+Kennedy New York across more than 110 countries. Now it's ending the sponsorship. Its global CMO, Morgan Flatley: "I think we've become overly reliant on borrowed IP."

Look at the collectible cups: nine of them, eight with star players, one with Grimace, McDonald's own character. The whole lesson fits on one shelf. Borrowed fame is a rented suit: it fits, then it goes back. The applause goes to whoever owns the stage, and a sponsorship has an end date. What stays is what you own: a character, a sound, a ritual, a name people search for.

My take: this isn't "never sponsor." Flatley's own words were to "be very selective and do it a few times." Before you pay for someone else's spotlight (an event, a booth, a famous face), ask what will still be yours when it's off.

The limits: it wasn't a flop. CFO Ian Borden said the campaign "provided a lift to the business" but "underperformed versus our expectations." Sources: Adweek, Nation's Restaurant News, Campaign, Marketing Dive. The two real frames come from McDonald's World Cup campaign images (owner uploads; the bench photo via Campaign); the other objects are AI-generated.

If every sponsor, partner and famous face left your business tomorrow, what would still be yours? Write to me.

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
        if fx: s["fx"] = words(fx, lang)
        s["motion_rationale"] = why
        if sid == "S13": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        scenes.append(s)
    return {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
            "topic": "شهرت قرضی: تشویق مال صاحب صحنه است" if lang == "fa" else "Borrowed fame: the applause goes to whoever owns the stage",
            "pillar": "brand_equity_campaigns_sponsorship", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
            "caption": CAP_FA if lang == "fa" else CAP_EN,
            "hashtags": ["#برندینگ", "#بازاریابی", "#brandstrategy", "#sponsorship"] if lang == "fa" else ["#branding", "#marketing", "#brandstrategy", "#sponsorship"],
            "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
            "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}


for n, lang in ((1, "fa"), (2, "en")):
    (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
print("ok")
