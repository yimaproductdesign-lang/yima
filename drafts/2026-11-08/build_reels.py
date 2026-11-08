"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-08 from one shared visual plan.
Topic: AI in ads. The audience does not punish the tool; it punishes the fake that pretends to be real."""
import json, os, pathlib

D = "2026-11-08"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-08T03:30:00Z"
MD = "https://marketingdive.com/news/how-fresh-step-used-ai-to-go-from-brief-to-ads-at-one-tenth-the-cost/873688"
NBC = "https://www.nbcnews.com/world/europe/mcdonalds-ai-generated-christmas-advert-social-media-backlash-rcna248590"
TR = "https://www.techradar.com/ai-platforms-assistants/mcdonalds-pulls-ai-generated-christmas-ad-after-backlash-over-soulless-visuals-and-holiday-chaos"
S1G = "https://system1group.com/ad-of-the-week/ai-or-no-ai-coke-gets-the-christmas-love"
NNG = "https://www.nngroup.com/articles/ai-ad/"
WSU = "https://news.wsu.edu/press-release/2024/07/30/using-the-term-artificial-intelligence-in-product-descriptions-reduces-purchase-intentions/"

E_MD = {"url": MD, "publisher": "Marketing Dive", "event_date": "2026-11-05", "retrieved_at": RT,
        "claim": "Fresh Step (Clorox) made three 15-second spots with AI agency RECE, AI-generated talking cats; brief to finished creative in 30 days at one-tenth the cost of a traditional production; live by Nov. 9; Deb Crandall (Clorox): 'We're not trying to fool anybody here.'"}
E_NBC = {"url": NBC, "publisher": "NBC News", "event_date": "2025-12-10", "retrieved_at": RT,
         "claim": "McDonald's Netherlands' 45-second AI ad 'the most terrible time of the year' was posted on a Saturday and removed by the following Wednesday after backlash (creepy, inauthentic)."}
E_S1 = {"url": S1G, "publisher": "System1", "event_date": "2025-11-20", "retrieved_at": RT,
        "claim": "Coca-Cola 'Holidays Are Coming' 2025 AI ad: 5.9 stars (maximum) on Test Your Ad; onlookers are animals, not humans; AI not mentioned in key associations; success credited to creative consistency and assets built over decades."}
E_NNG = {"url": NNG, "publisher": "Nielsen Norman Group", "event_date": "2025-12-19", "retrieved_at": RT,
         "claim": "AI visuals often provoke the uncanny-valley effect; once viewers notice subtle distortions, the emotional connection collapses."}


def obj(key, path_, x=540, y=1300, w=420, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1240, "w": 800, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.03, "color": [0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


MASK = lambda **kw: obj("mask", f"{D}/mask", w=560, y=1300, credit=AI_NEW, **kw)

TRICK = {"fa": (["ربات", "ارزان", "بی‌روح", "ماشینی", "هوش مصنوعی", "فریب"], "فریب"),
         "en": (["robots", "cheap", "soulless", "machine-made", "AI", "the trick"], "the trick")}
LBL = {"fa": ("ابزار", "خاطره"), "en": ("tool", "memory")}
REAL = {"fa": ["نظر مشتری", "قبل و بعد", "عکس غذا", "تیم شما", "ویترین"],
        "en": ["reviews", "before / after", "your dish", "your team", "shopfront"]}


def fx_for(sid, lang):
    if sid == "S2":
        w, k = TRICK[lang]
        return [{"type": "words", "mode": "fade", "box": [150, 1000, 930, 1480], "seed": 8, "size": 60, "words": w, "keep": [k], "keep_at": [540, 1250]}]
    if sid == "S6":
        a, b = LBL[lang]
        return [{"type": "labels", "items": [{"text": a, "x": 320, "y": 1260, "move": "up", "t": 1.4, "size": 92},
                                             {"text": b, "x": 760, "y": 1260, "move": "down", "acc": True, "t": 1.4, "size": 110}]}]
    if sid == "S10":
        return [{"type": "viewfinder", "box": [200, 1020, 880, 1500], "t": 0.5}]
    if sid == "S12":
        return [{"type": "words", "mode": "pop", "box": [170, 1040, 910, 1480], "seed": 5, "size": 56, "stagger": 0.08, "words": REAL[lang]}]
    return None


TC_AR, TB_AR, TA_AR = 752 / 428, 1919 / 1078, 1200 / 675

# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1300, "interpretation", None, [MASK(anim="drop")], None,
     "قلاب: نقاب = وانمود کردن؛ مشکل، چهره‌ی جعلی است نه ابزار. همین نقاب در چرخش (S9) و پایان (S14) برمی‌گردد"),
    ("S2", "paper", None, "interpretation", None, None, "S2",
     "ابر برچسب‌هایی که به هوش مصنوعی می‌زنیم (ربات، ارزان، بی‌روح…) محو می‌شوند و فقط «فریب» می‌ماند = آنچه مخاطب واقعاً نمی‌بخشد"),
    ("S3", "graphite", 1240, "fact", [E_NBC], [frame("tc", "T-c.png", TC_AR, "McDonald's Netherlands (2025), via TechRadar; owner upload", TR, w=760, blur=[0, 2.5, 1.6, 3.2])], None,
     "سند واقعی (آپلود مالک): فریم تبلیغ پایین‌کشیده با آدم‌های تقریباً واقعی؛ کمی تار می‌شود = چند روز بیشتر دوام نیاورد"),
    ("S4", "paper", None, "fact", [E_NNG], [obj("lens", "2026-10-22/magnifier", w=480, y=1290, rot=-10, anim="slide_r", path=[[0.6, 600, 1290], [2.2, 470, 1250], [3.4, 560, 1300]])], None,
     "ذره‌بین که دنبال چیزی می‌گردد = چشم مخاطب روی چهره‌ی «تقریباً» انسانی دنبال ایراد می‌گردد (دره‌ی وهمی)"),
    ("S5", "graphite", 1240, "fact", [E_S1], [frame("tb", "T-b.png", TB_AR, "Coca-Cola, Holidays Are Coming (2025); owner upload", S1G, w=820)], None,
     "سند واقعی (آپلود مالک): کامیون‌های قرمز آشنا در برف = همان ابزار، ولی سوار بر نشانه‌های چنددهه‌ای برند"),
    ("S6", "paper", None, "interpretation", [E_S1], None, "S6",
     "چرخش کوچک: «ابزار» سبک است و بالا می‌رود؛ «خاطره» سنگین می‌نشیند = آنچه تبلیغ را کشید، دارایی‌های آشنای برند بود"),
    ("S7", "graphite", 1240, "fact", [E_MD], [frame("ta", "T-a.png", TA_AR, "Courtesy of Fresh Step (via Marketing Dive); owner upload", MD, w=820)], None,
     "سند واقعی (آپلود مالک): گربه‌های سخنگو، با برچسب «AI actors used» در گوشه‌ی قاب = خیالِ آشکار که خودش را واقعی جا نمی‌زند"),
    ("S8", "paper", None, "fact", [E_MD], [obj("card", "2026-10-25/label_card", w=520, y=1300, rot=-4, anim="rise", float=2)], None,
     "کارت یادداشت سفید = یک جمله‌ی رک و بی‌پرده؛ همان حرف بازاریاب برند که قرار نیست کسی گول بخورد"),
    ("S9", "graphite", 1300, "interpretation", None, [MASK(anim="zoom", float=3)], None,
     "چرخش (drop): همان نقاب آغاز برمی‌گردد = یک ابزار، دو واکنش؛ مرز همین نقاب است"),
    ("S10", "paper", None, "interpretation", None, None, "S10",
     "احتیاط یک بار: منظره‌یاب با نقطه‌ی ضبط = هنوز در حال تماشاییم؛ برای قضاوت درباره‌ی نتیجه زود است"),
    ("S11", "graphite", 1290, "interpretation", None, [obj("pencil", "2026-10-22/pencil", w=560, y=1290, rot=-14, anim="slide_l")], None,
     "مداد = چیزی که آشکارا کشیده و خیال شده (تصویرسازی، ایده، شخصیت)؛ جای درست ابزار"),
    ("S12", "paper", None, "interpretation", None, None, "S12",
     "ابر چیزهای واقعی کسب‌وکار (نظر مشتری، قبل و بعد، عکس غذا، تیم، ویترین) = همان‌هایی که نباید جعل شوند"),
    ("S13", "graphite", 1290, "interpretation", None, [obj("photo", "2026-10-22/photo", w=560, y=1290, rot=3, anim="drop")], None,
     "عکس چاپی واقعی = چیز واقعی را همان‌طور که هست نشان بده"),
    ("S14", "paper", None, "interpretation", None, [MASK(anim="fade")], None,
     "بازگشت به نقاب آغاز، این بار روی کاغذ و روشن، زیر جمله‌ی آخر = قصه بخشیده می‌شود، نقاب نه"),
    ("S15", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("مشکل این تبلیغ‌ها هوش مصنوعی نبود.", "b"), ("*وانمود کردن* بود.", "h")],
    "S2": [("همه ابزار را مقصر می‌دانند.", "b"), ("مخاطب *فریب* را نمی‌بخشد.", "h")],
    "S3": [("کریسمس پارسال، مک‌دونالدز هلند:", "b"), ("آدم‌های *تقریباً واقعی*.", "h"), ("چند روز بعد پایینش کشیدند.", "s")],
    "S4": [("سختی کار همین «تقریباً» است.", "b"), ("چشم دنبال *ایراد* می‌گردد.", "h")],
    "S5": [("کوکاکولا همان فصل، با هوش مصنوعی:", "b"), ("حیوان‌ها، کامیون‌های *آشنا*.", "h"), ("نمره‌ی کامل در آزمون.", "s")],
    "S6": [("بار را ابزار نکشید.", "b"), ("*خاطره‌ی* چند دهه کشید.", "h")],
    "S7": [("حالا گربه‌های سخنگوی فرش‌استپ.", "b"), ("کسی خیال نمی‌کند *واقعی‌اند*.", "h")],
    "S8": [("بازاریابش:", "b"), ("«نمی‌خواهیم کسی را *گول* بزنیم.»", "h")],
    "S9": [("یک ابزار، دو واکنش.", "b"), ("مرز، *نقاب* است.", "h")],
    "S10": [("یک احتیاط: گربه‌ها تازه پخش شده‌اند.", "b"), ("هنوز *نتیجه‌ای* نیست.", "h"), ("این برداشت من است.", "s")],
    "S11": [("هوش مصنوعی برای چیزی که پیداست خیالی است:", "b"), ("طرح، ایده، *شخصیت*.", "h")],
    "S12": [("نه برای جعل واقعیت:", "b"), ("مغازه، غذا، *مشتری‌هایتان*.", "h")],
    "S13": [("این‌ها را با عکس *واقعی* نشان دهید.", "h")],
    "S14": [("مردم قصه را می‌بخشند.", "b"), ("*نقاب* را نه.", "h")],
    "S15": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("AI didn't ruin these ads.", "b"), ("*Pretending* did.", "h")],
    "S2": [("Everyone blames the tool.", "b"), ("People punish the *trick*.", "h")],
    "S3": [("Last Christmas, McDonald's Netherlands.", "b"), ("*Almost-real* people.", "h"), ("Pulled within days.", "s")],
    "S4": [("Almost is the problem.", "b"), ("The eye hunts for *flaws*.", "h")],
    "S5": [("Coca-Cola's AI ad, same season:", "b"), ("Animals. Familiar *trucks*.", "h"), ("Top test score.", "s")],
    "S6": [("The tool didn't carry it.", "b"), ("Decades of *memory* did.", "h")],
    "S7": [("Now: Fresh Step's talking cats.", "b"), ("Nobody thinks they're *real*.", "h")],
    "S8": [("Their marketer:", "b"), ("\"We're not trying to *fool* anybody.\"", "h")],
    "S9": [("Same tool. Opposite reactions.", "b"), ("The line is the *mask*.", "h")],
    "S10": [("The cats just aired.", "b"), ("No *results* yet.", "h"), ("This is my read.", "s")],
    "S11": [("Use AI for what's clearly imagined.", "b"), ("Ideas and *characters*.", "h")],
    "S12": [("Never to fake what's real:", "b"), ("your shop, food, *customers*.", "h")],
    "S13": [("Show those in a *real* photo.", "h")],
    "S14": [("People forgive a fairy tale.", "b"), ("Not a *mask*.", "h")],
    "S15": [("Write to me.", "b")],
}
VO = {"S3": "Last Christmas, McDonald's in the Netherlands. Almost-real people. Pulled within days.",
      "S5": "Same season, Coca-Cola used AI too. Animals, and the trucks you know. A top score with test audiences."}

SOURCES = [
    {"publisher": "Marketing Dive", "title": "How Fresh Step used AI to go from brief to ads at one-tenth the cost", "date": "2026-11-05", "url": MD},
    {"publisher": "NBC News", "title": "Not lovin' it: McDonald's pulls AI-generated Christmas ad after social media backlash", "date": "2025-12-10", "url": NBC},
    {"publisher": "TechRadar", "title": "McDonald's pulls AI-generated Christmas ad after backlash over soulless visuals and holiday chaos", "date": "2025-12-10", "url": TR},
    {"publisher": "System1", "title": "AI or No AI, Coke Gets the Christmas Love", "date": "2025-11-20", "url": S1G},
    {"publisher": "Nielsen Norman Group", "title": "Why AI-Generated Holiday Ads Fail, and What They Teach Us About Using AI in UX Work", "date": "2025-12-19", "url": NNG},
    {"publisher": "Washington State University", "title": "Using the term 'artificial intelligence' in product descriptions reduces purchase intentions", "date": "2024-07-30", "url": WSU},
]

CAP_FA = """مشکل این تبلیغ‌ها هوش مصنوعی نبود. وانمود کردن بود.

کریسمس پارسال مک‌دونالدز هلند یک تبلیغ ۴۵ثانیه‌ای با هوش مصنوعی منتشر کرد: آدم‌های تقریباً واقعی، با زیرنویس «بدترین وقت سال». چند روز بعد، پس از موجی از واکنش‌های منفی («ترسناک»، «غیرواقعی»)، پایینش کشیدند. همان فصل، تبلیغ هوش‌مصنوعی کوکاکولا تماشاگرانش را حیوان گذاشته بود، نه آدم، و همان کامیون‌های قرمز همیشگی را آورده بود؛ در آزمون سیستم‌وان (System One) نمره‌ی کامل ۵٫۹ گرفت و در تداعی‌های بینندگان اصلاً اسمی از هوش مصنوعی نبود. خود سیستم‌وان موفقیتش را به ثبات خلاقانه و دارایی‌های چنددهه‌ای برند نسبت می‌دهد، نه به ابزار.

و حالا فرش‌استپ (کلوروکس) سه تبلیغ ۱۵ثانیه‌ای با گربه‌های سخنگوی ساخته‌شده با هوش مصنوعی ساخته؛ از بریف تا نسخه‌ی نهایی در ۳۰ روز، با یک‌دهم هزینه‌ی تولید معمول. مدیر بازاریابی‌اش گفته: «نمی‌خواهیم کسی را گول بزنیم.» در فریمی که از این تبلیغ منتشر شده، برچسب «AI actors used» هم پیداست.

به نظر من مرز، ابزار نیست؛ چیزی است که خودش را واقعی جا می‌زند. چهره‌ی «تقریباً» انسانی چشم را به ایرادگیری می‌کشد (پژوهشگران Nielsen Norman Group به آن دره‌ی وهمی می‌گویند)، ولی گربه‌ی سخنگو از اول قصه است.

حدودش را بگویم: این برداشت من از سه نمونه است، نه نتیجه‌ی یک پژوهش. تبلیغ فرش‌استپ تازه پخش شده و هنوز هیچ نتیجه‌ای از آن منتشر نشده. نقدهای آنلاین کوکاکولا هم کم نبود؛ آزمون سیستم‌وان فقط یک سنجه است. پژوهش دانشگاه ایالتی واشنگتن (۲۰۲۴، بیش از ۱۰۰۰ بزرگسال آمریکایی) هم نشان داد آوردن واژه‌ی «هوش مصنوعی» در توضیح محصول اعتماد احساسی و قصد خرید را پایین آورد؛ ولی آن درباره‌ی توضیح محصول است، نه تبلیغ. منابع: Marketing Dive، NBC News، TechRadar، سیستم‌وان، Nielsen Norman Group. فریم‌های تبلیغ‌ها آپلود مالک و متعلق به صاحبانشان‌اند؛ اشیای این ریل (نقاب و دیگر اشیا) آشکارا با هوش مصنوعی ساخته شده‌اند.

برای صاحب کافه، سالن یا مغازه: از هوش مصنوعی برای چیزی استفاده کنید که پیداست خیالی است؛ تصویرسازی، ایده، شخصیت. ولی مغازه، غذا، تیم، نظر مشتری و «قبل و بعد» را با عکس واقعی نشان دهید.

شما کجا از هوش مصنوعی استفاده می‌کنید، و آیا مشتری‌تان می‌داند؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """AI didn't ruin these ads. Pretending did.

Last Christmas, McDonald's Netherlands released a 45-second AI ad: almost-real people under the line "the most terrible time of the year". After a wave of backlash ("creepy", "inauthentic"), it was pulled within days. The same season, Coca-Cola's AI ad made its onlookers animals, not people, and brought back the red trucks everyone knows. It scored the maximum 5.9 stars in System1's testing, and AI didn't even come up in what viewers associated with it. System1 credits creative consistency and assets built over decades, not the tool.

Now Fresh Step (Clorox) has made three 15-second spots with AI-generated talking cats: brief to finished ads in 30 days, at a tenth of the cost of a traditional shoot. Their marketer: "We're not trying to fool anybody here." The released frame even carries an "AI actors used" label.

My take: the line isn't the tool. It's the fake that passes itself off as real. A face that's almost human sends the eye hunting for flaws (Nielsen Norman Group calls it the uncanny valley). A talking cat is a story from the first frame.

The limits: this is my reading of three cases, not a study. Fresh Step's ads have only just aired, and there are no results yet. Coca-Cola's ad had plenty of online critics; System1's test is one measure. A Washington State University study (2024, 1,000+ US adults) found that putting "artificial intelligence" in product descriptions lowered emotional trust and purchase intent, but that was product copy, not ads. Sources: Marketing Dive, NBC News, TechRadar, System1, Nielsen Norman Group. Ad frames are owner uploads and belong to their owners; the objects in this reel (the mask and the rest) are openly AI-generated.

For owners of a café, a salon, a shop: use AI for what's clearly imagined: illustration, ideas, characters. But show your shop, your food, your team, your reviews and your before-and-after with real photos.

Where do you use AI in your marketing, and do your customers know? Write to me.

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
         "topic": "مخاطب از هوش مصنوعی نمی‌رنجد؛ از وانمود کردن می‌رنجد" if lang == "fa" else "People don't hate AI ads. They hate being fooled.",
         "pillar": "advertising_creative_strategy", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#بازاریابی", "#تبلیغات", "#branding", "#aimarketing"] if lang == "fa" else ["#marketing", "#branding", "#advertising", "#aimarketing"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S9"}, "status": "DRAFT", "style": "editorial", "lang": lang}
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
