"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-12 from one shared visual plan.
Topic: Dove put bad reviews in its own ads; a perfect five stars sells less; the flaw you show makes you believable."""
import json, os, pathlib

D = "2026-11-12"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-12T03:30:00Z"
UNI = "https://www.unilever.com/news/news-search/2026/how-dove-turned-reddits-unfiltered-honesty-into-unmissable-marketing/"
UNI_C = "https://www.unilever.com/news/news-search/2026/take-a-look-at-unilevers-2026-cannes-lionswinning-campaigns/"
MD = "https://marketingdive.com/news/dove-lets-redditors-do-the-talking-in-transparency-focused-campaign/811642"
SP = "https://spiegel.medill.northwestern.edu/How-Online-Reviews-Influence-Sales"
PF = "https://paperity.org/p/59814503/the-effect-of-a-pratfall-on-increasing-interpersonal-attractiveness"
DLA = "https://www.dlapiper.com/en/insights/publications/2026/11/ftcs-actions-against-fake-reviews"

E_DOVE = {"url": UNI, "publisher": "Unilever (official newsroom)", "event_date": "2026-05-12", "retrieved_at": RT,
          "claim": "Dove published the first 50 Reddit reviews of its Intensive Repair hair mask unedited, with permission, on out-of-home billboards across New York City and social; one read 'it kinda smells like expired hotel shampoo'."}
E_MD = {"url": MD, "publisher": "Marketing Dive", "event_date": "2026-02-10", "retrieved_at": RT,
        "claim": "First 50 Reddit reviews 'regardless of opinion', unaltered, used with permission; launched with a Flatiron Plaza pop-up, Feb 5-6, 2026."}
E_SP = {"url": SP, "publisher": "Medill Spiegel Research Center, Northwestern University", "event_date": "2017 (page updated 2025)", "retrieved_at": RT,
        "claim": "Purchase likelihood typically peaks at ratings in the 4.0-4.7 range and falls as ratings approach 5.0 ('too good to be true')."}
E_PF = {"url": PF, "publisher": "Psychonomic Science 4(6) (Aronson, Willerman, Floyd)", "event_date": "1966", "retrieved_at": RT,
        "claim": "48 male students heard a taped quiz candidate (superior: 92% correct, or average: 30%), with or without a coffee-spilling blunder. The blunder raised liking for the superior candidate and lowered it for the average one."}
E_DLA = {"url": DLA, "publisher": "DLA Piper", "event_date": "2026-11-02", "retrieved_at": RT,
         "claim": "FTC complaints (allegations) in October 2026 involve fabricated positive reviews and suppression of negative reviews; the Consumer Reviews and Testimonials Rule is being enforced."}


def obj(key, path_, x=540, y=1290, w=460, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


JAR = lambda **kw: obj("jar", f"{D}/hair_mask_jar", w=430, y=1280, credit=AI_NEW, color=[0, 0, 0], **kw)
STARS = lambda **kw: obj("stars", f"{D}/stars_row", w=820, y=1260, credit=AI_NEW, **kw)

NUMS = {"fa": ("۴٫۷", "۵٫۰"), "en": ("4.7", "5.0")}


def fx_for(sid, lang):
    if sid == "S5":
        a, b = NUMS[lang]
        xa, xb = (700, 380) if lang == "fa" else (380, 700)
        return [{"type": "labels", "items": [{"text": a, "x": xa, "y": 1260, "size": 170, "acc": True, "move": "down", "t": 1.6},
                                              {"text": b, "x": xb, "y": 1260, "size": 170, "move": "up", "t": 1.6}]}]
    if sid == "S10":
        return [{"type": "viewfinder", "box": [200, 1040, 880, 1500], "t": 0.5}]
    return None


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1280, "fact", [E_DOVE, E_MD], [JAR(anim="rise", float=3)], None,
     "قوطی ماسک مو (خودِ محصول داستان، رنگی، بی‌برند) زیر نور موضعی = همان محصولی که داو نقدهای بدش را تبلیغ کرد؛ در S14 برمی‌گردد"),
    ("S2", "paper", None, "fact", [E_DOVE], [obj("mega", "2026-11-06/megaphone", w=560, y=1300, credit=AI_NEW, anim="slide_l", vibrate=2)], None,
     "بلندگو = نقد منفی را خودشان بلند و در خیابان گفتند"),
    ("S3", "graphite", 1290, "interpretation", None, [obj("eraser", "2026-10-22/eraser", w=520, y=1290, rot=-8, anim="slide_r", path=[[0.5, 620, 1290], [1.6, 460, 1300], [2.7, 600, 1285]])], None,
     "پاک‌کن که رفت‌وبرگشت می‌کند = ما نقد بد را پاک می‌کنیم"),
    ("S4", "paper", None, "fact", [E_SP], [STARS(anim="pop")], None,
     "ردیف پنج ستاره‌ی براق = امتیاز کامل؛ کمالی که بدگمانی می‌آورد"),
    ("S5", "graphite", None, "fact", [E_SP], None, "S5",
     "عدد به‌جای شیء: ۴٫۷ با رنگ برند پایین می‌نشیند، ۵٫۰ بالا می‌رود و کم‌رنگ می‌شود = اوج خرید پیش از امتیاز کامل است"),
    ("S6", "paper", None, "interpretation", [E_SP], [obj("mask", "2026-11-08/mask", w=520, y=1290, credit=AI_NEW, anim="fade", float=2)], None,
     "نقاب سفید بی‌نقص = بی‌عیبی که ساختگی به نظر می‌رسد"),
    ("S7", "graphite", 1290, "interpretation", None, [obj("lens", "2026-10-22/magnifier", w=480, y=1290, rot=-10, anim="slide_r", path=[[0.6, 620, 1290], [2.0, 460, 1260], [3.2, 580, 1310]])], None,
     "ذره‌بین که می‌گردد = مشتری دنبال ایراد می‌گردد"),
    ("S8", "paper", None, "fact", [E_PF], [obj("cup", f"{D}/spilled_cup", w=620, y=1290, credit=AI_NEW, anim="drop", rot=-3)], None,
     "چرخش ایده (drop): فنجان واژگون و قهوه‌ی ریخته = خطای آزمایش ۱۹۶۶ که آدم توانا را دوست‌داشتنی‌تر کرد"),
    ("S9", "graphite", 1290, "fact", [E_PF], [obj("trophy", "2026-10-24/trophy", w=360, y=1270, anim="rise")], None,
     "جام = شرط ماجرا: فقط برای آدمِ از پیش عالی کار کرد"),
    ("S10", "paper", None, "interpretation", [E_PF, E_SP], None, "S10",
     "احتیاط یک بار: منظره‌یاب = فقط یک قاب کوچک دیدیم؛ آزمایش قدیمی و کوچک"),
    ("S11", "graphite", 1300, "interpretation", None, [obj("scale", "2026-10-22/scale", w=520, y=1300, anim="fade")], None,
     "ترازو = مشتری عیب را کنار باقی کیفیت می‌سنجد؛ اول کفه‌ی کیفیت باید سنگین باشد"),
    ("S12", "paper", None, "interpretation", None, [obj("bowl", f"{D}/kintsugi_bowl", w=600, y=1290, credit=AI_NEW, anim="rise", color=[0, 0, 0])], None,
     "کاسه‌ی کینتسوگی با درز طلایی = ترک را پنهان نکن، تعمیرش را نشان بده (پاسخ به نقد سه‌ستاره)"),
    ("S13", "graphite", 1290, "interpretation", [E_DLA], [obj("phone", "2026-10-25/phone", w=420, y=1290, rot=-6, anim="drop")], None,
     "گوشی = جایی که نقد ساخته یا پنهان می‌شود؛ هر دو همان فریب"),
    ("S14", "paper", None, "interpretation", [E_SP], [JAR(anim="fade")], None,
     "بازگشت قوطی آغاز = برندی که عیبش را نشان داد و باور شد"),
    ("S15", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("داو نقدهای بد محصولش را", "b"), ("روی *تبلیغ خودش* برد.", "h")],
    "S2": [("یکی نوشته بود:", "b"), ("«بوی شامپوی *تاریخ‌گذشته‌ی* هتل می‌دهد.»", "h")],
    "S3": [("بیشتر ما برعکس می‌کنیم.", "b"), ("نقد بد را *پاک* می‌کنیم.", "h")],
    "S4": [("ولی پنج ستاره‌ی کامل،", "b"), ("خریدار را *بدگمان* می‌کند.", "h")],
    "S5": [("احتمال خرید", "b"), ("بین ۴ و *۴٫۷* اوج می‌گیرد.", "h")],
    "S6": [("بی‌عیبی", "b"), ("*دست‌کاری‌شده* به نظر می‌رسد.", "h")],
    "S7": [("مشتری دنبال ایراد می‌گردد.", "b"), ("نبود؟ فکر می‌کند *پنهانش* کرده‌اید.", "h")],
    "S8": [("۱۹۶۶. قهرمان مسابقه قهوه را می‌ریزد.", "b"), ("و *بیشتر* دوستش دارند.", "h")],
    "S9": [("ولی فقط چون *عالی* بود.", "h"), ("آدم معمولی با همان خطا باخت.", "b")],
    "S10": [("یک آزمایش قدیمی، ۴۸ دانشجو.", "b"), ("*نشانه* است، نه قانون.", "h")],
    "S11": [("پس اول *خوب* باشید.", "h"), ("بعد بگذارید عیب دیده شود.", "b")],
    "S12": [("نقد سه‌ستاره را پاک نکنید.", "b"), ("*جوابش* را بدهید و تعمیر را نشان دهید.", "h")],
    "S13": [("نقد ساختگی و نقد پنهان،", "b"), ("هر دو همان *دروغ* است.", "h")],
    "S14": [("۴٫۷ای که باورش می‌کنند،", "b"), ("از ۵ِ *باورنکردنی* بهتر است.", "h")],
    "S15": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Dove ran its own bad reviews", "b"), ("as *ads*.", "h")],
    "S2": [("One review:", "b"), ("\"it kinda smells like *expired* hotel shampoo.\"", "h")],
    "S3": [("Most of us do the opposite.", "b"), ("We *delete* the bad one.", "h")],
    "S4": [("But a perfect five stars", "b"), ("makes buyers *wary*.", "h")],
    "S5": [("Buying tends to peak", "b"), ("between 4 and *4.7*.", "h")],
    "S6": [("Flawless", "b"), ("looks *edited*.", "h")],
    "S7": [("Shoppers hunt for the catch.", "b"), ("No catch? You *hid* it.", "h")],
    "S8": [("1966. A quiz star spills coffee.", "b"), ("People like him *more*.", "h")],
    "S9": [("Only because he was *brilliant*.", "h"), ("The average guy lost points.", "b")],
    "S10": [("Old lab study. 48 students.", "b"), ("A *clue*, not a law.", "h")],
    "S11": [("Be *good* first.", "h"), ("Then let the flaw show.", "b")],
    "S12": [("Don't delete the three-star review.", "b"), ("*Answer* it. Show the fix.", "h")],
    "S13": [("Fake reviews, hidden reviews:", "b"), ("same *lie*.", "h")],
    "S14": [("A 4.7 people believe", "b"), ("beats a 5 nobody *trusts*.", "h")],
    "S15": [("Write to me.", "b")],
}
VO = {"S2": "One review: it kinda smells like expired hotel shampoo.",
      "S5": "Buying tends to peak somewhere between four and four point seven.",
      "S8": "Nineteen sixty-six. A quiz star spills coffee. People like him more.",
      "S10": "Old lab study. Forty-eight students. A clue, not a law.",
      "S14": "A four point seven people believe beats a five nobody trusts."}

SOURCES = [
    {"publisher": "Unilever", "title": "How Dove turned Reddit's unfiltered honesty into unmissable marketing", "date": "2026-05-12", "url": UNI},
    {"publisher": "Marketing Dive", "title": "Dove lets Redditors do the talking in transparency-focused campaign", "date": "2026-02-10", "url": MD},
    {"publisher": "Unilever", "title": "Take a look at Unilever's 2026 Cannes Lions-winning campaigns", "date": "2026-07-07", "url": UNI_C},
    {"publisher": "Medill Spiegel Research Center, Northwestern University", "title": "How Online Reviews Influence Sales", "date": "2017 (updated 2025)", "url": SP},
    {"publisher": "Psychonomic Science 4(6):227-228 (Aronson, Willerman, Floyd)", "title": "The effect of a pratfall on increasing interpersonal attractiveness", "date": "1966", "url": PF},
    {"publisher": "DLA Piper", "title": "FTC's actions against fake reviews", "date": "2026-11-02", "url": DLA},
]

CAP_FA = """داو نقدهای بد محصولش را روی تبلیغ خودش برد. و فروش ماسک مو بالا رفت.

فوریه‌ی ۲۰۲۶، داو از کاربران ردیت خواست ماسک موی Intensive Repair را امتحان کنند و ۵۰ نقد اول را، هر چه بود، بی‌ویرایش و با اجازه‌ی نویسنده‌ها روی بیلبوردهای نیویورک و شبکه‌های اجتماعی گذاشت. یکی‌شان نوشته بود: «یه‌کم بوی شامپوی تاریخ‌گذشته‌ی هتل می‌ده.» همین هم در کمپین ماند. یونیلیور می‌گوید بیش از یک میلیارد بار دیده شد، جلوی پاپ‌آپش ساعت‌ها صف بود و فروش ماسک بالا رفت (رقمی نداده). کمپین در کن شش شیر گرفت.

چرا جواب داد؟ مرکز پژوهشی اشپیگل (دانشگاه نورث‌وسترن) دیده احتمال خرید معمولاً بین امتیاز ۴ و ۴٫۷ به اوج می‌رسد و نزدیک ۵ افت می‌کند؛ پنج ستاره‌ی کامل «زیادی خوب برای واقعی بودن» است. و آزمایش معروف ۱۹۶۶: داوطلب مسابقه‌ای که قهوه را روی خودش ریخت، اگر از قبل عالی بود، دوست‌داشتنی‌تر شد؛ اگر معمولی بود، کمتر.

به نظر من این شرط، اصل ماجراست: عیب فقط وقتی کمک می‌کند که کیفیت از قبل معلوم باشد. اول خوب باشید، بعد نقد سه‌ستاره را پاک نکنید؛ جوابش را بدهید و نشان بدهید چه چیزی را درست کردید. و هرگز عیب یا نقد ساختگی نسازید؛ در آمریکا همین حالا شکایت‌هایی علیه نقدهای جعلی و پنهان‌کردن نقد منفی در جریان است.

حدودش: آزمایش ۱۹۶۶ کوچک و قدیمی است (۴۸ دانشجوی مرد، با صدای ضبط‌شده)؛ داده‌ی اشپیگل مربوط به خرید آنلاین است و «معمولاً» یعنی همیشه نه؛ عددهای داو را خود یونیلیور گزارش کرده. منابع: یونیلیور، Marketing Dive، مرکز اشپیگل، Psychonomic Science (۱۹۶۶) و DLA Piper. اشیای این ریل با هوش مصنوعی ساخته شده‌اند و قوطی ماسک بی‌برند و نمایشی است.

بدترین نقدی که برایتان نوشته‌اند چه بود، و با آن چه کردید؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Dove ran bad reviews of its own product as ads. And the mask sold more.

In February 2026, Dove asked Redditors to try its Intensive Repair hair mask, then ran the first 50 reviews, whatever they said, unedited and with permission, on New York billboards and social. One read: "it kinda smells like expired hotel shampoo." It stayed in. Unilever reports more than a billion impressions, hour-long queues at the pop-up and higher mask sales (no figure given). The campaign won six Cannes Lions.

Why did it work? Northwestern's Spiegel Research Center found purchase likelihood typically peaks at ratings between 4.0 and 4.7 and falls as they approach 5.0: perfect looks too good to be true. And in a classic 1966 study, a quiz candidate who spilled coffee became more likeable, but only if he was already excellent. The average candidate who did the same lost points.

My take: that condition is the whole story. A flaw only helps once your quality is obvious. Be good first. Then don't delete the three-star review; answer it and show what you changed. And never fake a flaw or a review; regulators are already going after fake reviews and suppressed negative ones.

The limits: the 1966 study is small and old (48 male students, taped audio); the Spiegel data is about online shopping, and "typically" means not always; Dove's numbers are Unilever's own. Sources: Unilever, Marketing Dive, Spiegel Research Center, Psychonomic Science (1966), DLA Piper. The objects in this reel are AI-generated; the jar is an unbranded stand-in.

What's the worst review anyone ever left you, and what did you do with it? Write to me.

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
        f = fx_for(fx, lang) if isinstance(fx, str) else fx
        if f: s["fx"] = f
        s["motion_rationale"] = why
        if sid == "S15": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        if lang == "en" and VOICE and sid in VO: s["vo"] = VO[sid]
        scenes.append(s)
    r = {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
         "topic": "داو نقد بدش را تبلیغ کرد: پنج ستاره‌ی کامل کمتر می‌فروشد؛ عیبی که نشان می‌دهید، برندتان را باورپذیر می‌کند" if lang == "fa" else "Dove advertised its bad reviews: a perfect five stars sells less; the flaw you show makes your brand believable",
         "pillar": "brand_trust_reviews", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#customerreviews", "#consumerpsychology"] if lang == "fa" else ["#marketing", "#branding", "#customerreviews", "#consumerpsychology"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S8"}, "status": "DRAFT", "style": "editorial", "lang": lang}
    if lang == "en" and VOICE:
        r["voice"] = {"enabled": True, "voice": "en-US-AndrewNeural", "rate": "-6%", "pitch": "-3%"}
    return r


VOICE = bool(os.environ.get("AZURE_SPEECH_KEY") and os.environ.get("AZURE_SPEECH_REGION"))

if __name__ == "__main__":
    for n, lang in ((1, "fa"), (2, "en")):
        (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
    for L, C in (("fa", FA), ("en", EN)):
        print(L, sum(len(t.replace("*", "").split()) for v in C.values() for t, _ in v))
    print("voice", VOICE)
