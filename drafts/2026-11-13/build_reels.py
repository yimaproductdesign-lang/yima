"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-13 from one shared visual plan.
Topic (type 1, famous-brand controversy): Skims' $148 advent calendar of hair ties and keychains;
refunds after the unboxing backlash. Idea: a price is a promise, and the unboxing makes the gap public."""
import json, os, pathlib

D = "2026-11-13"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-13T01:20:00Z"
YH = "https://www.yahoo.com/entertainment/articles/kim-kardashian-skims-offers-refunds-200823739.html"
GN = "https://globalnews.ca/news/12144875/skims-refund-advent-calendar-kim-kardashian/"
FU = "https://fashionunited.uk/news/fashion/skims-advent-calendar-backlash-tests-the-limits-of-brand-led-pricing/2026110991265"
YI = "https://yahoo.com/entertainment/celebrity/fashion/articles/kim-kardashian-lingerie-brand-forced-111754685.html"
OL = "https://journals.sagepub.com/doi/10.1177/002224378001700405"

E_YH = {"url": YH, "publisher": "Yahoo Entertainment (via Where Is The Buzz; statement to Today.com)", "event_date": "2026-11-09", "retrieved_at": RT,
        "claim": "Skims 'Accessories Advent Calendar', released Oct 29, $148 (US) / £158 (UK), 12 days of surprises; contents: bear keychain, hair elastics, satin scrunchies, bobby pins, hair clips, bra-elastic headbands, comb keychain, logo keychain, logo squishy toy; no clothing."}
E_GN = {"url": GN, "publisher": "Global News (Rachel Goodman)", "event_date": "2026-11-10", "retrieved_at": RT,
        "claim": "Skims: 'the calendar didn't meet expectations and we have personally contacted every customer' and 'offered them a choice of a full refund or a SKIMS credit'. Kayla Ryan's unboxing TikTok had over 22 million views; another review over 8 million."}
E_FU = {"url": FU, "publisher": "FashionUnited (Renan Botelho de Carvalho)", "event_date": "2026-11-09", "retrieved_at": RT,
        "claim": "Kayla Ryan's TikTok unboxing: over 18.9 million views; backlash framed as a test of how much premium a brand name can support outside its category."}
E_YI = {"url": YI, "publisher": "Yahoo (The Independent syndication)", "event_date": "2026-11-10", "retrieved_at": RT,
        "claim": "None of the brand's underwear was included; Skims said the calendar 'didn't meet expectations', offered full refund or store credit, and disabled the product page; no plans to restock."}
E_OL = {"url": OL, "publisher": "Journal of Marketing Research 17(4) (Richard L. Oliver)", "event_date": "1980", "retrieved_at": RT,
        "claim": "Expectation-disconfirmation model: satisfaction is a function of expectations and of how far performance confirms or falls short of them (simplified on screen as 'what you got minus what you expected')."}


def obj(key, path_, x=540, y=1290, w=460, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


CAL = lambda **kw: obj("cal", f"{D}/advent_calendar", **{"w": 560, "y": 1290, "credit": AI_NEW, "color": [0, 0, 0], **kw})
HAIR = lambda **kw: obj("hair", f"{D}/hair_accessories", **{"w": 640, "y": 1300, "credit": AI_NEW, "color": [0, 0, 0], **kw})
KEY = lambda **kw: obj("squishy", f"{D}/squishy_keychain", **{"w": 330, "y": 1290, "credit": AI_NEW, **kw})
TAG = lambda **kw: obj("tag", "2026-10-25/price_tag", **{"w": 520, "y": 1290, **kw})

WORDS = {"fa": (["سوتین", "شورت", "بادی", "لباس زیر", "گن", "کش مو"], ["کش مو"]),
         "en": (["bra", "briefs", "bodysuit", "lingerie", "shapewear", "hair tie"], ["hair tie"])}
PRICE = {"fa": "۱۴۸ دلار", "en": "$148"}
LOGO = {"key": "logo", "src": "assets/objects/2026-11-13/skims_logo_card.png", "x": 540, "y": 1250, "w": 680, "frame": True, "ar": 1.78,
        "color": [0, 0, 0], "credit": "SKIMS (official logo; owner upload T-a)", "source_url": "https://skims.com/pages/nikeskims", "anim": "rise"}
PHOTO = {"key": "nikeskims", "src": "incoming/2026-11-13/T-b_nikeskims.png", "x": 540, "y": 1270, "w": 560, "frame": True, "ar": 1.0,
         "color": [0, 0, 0], "credit": "NikeSKIMS product photo (SKIMS / Nike; owner upload T-b)", "source_url": "https://skims.com/pages/nikeskims", "anim": "zoom"}


def fx_for(sid, lang):
    if sid == "S8":
        return [{"type": "labels", "items": [{"text": PRICE[lang], "x": 540, "y": 1070, "size": 170, "acc": True, "move": "down", "t": 1.4}]}]
    if sid == "S8_words_unused":
        w, k = WORDS[lang]
        return [{"type": "words", "mode": "fade", "words": w, "keep": k, "box": [130, 1040, 950, 1480], "size": 56, "seed": 7}]
    if sid == "S11":
        return [{"type": "viewfinder", "box": [200, 1040, 880, 1500], "t": 0.5}]
    return None


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1290, "fact", [E_YH, E_GN], [LOGO], None,
     "لوگوی واقعی اسکیمز (آپلود مالک) در قاب، روی صحنه‌ی تیره = برند را همان لحظه که نامش می‌آید نشان بده"),
    ("S2", "paper", None, "fact", [E_YH], [CAL(anim="fade", x=320, y=1240, w=400), HAIR(anim="drop", x=760, y=1390, w=400)], None,
     "جعبه‌ی کشویی تقویم (بی‌برند، رنگی) و کش موهایی که کنارش می‌ریزند = همان چیزی که پشت درها بود؛ تقویم در S12 و S13 برمی‌گردد"),
    ("S3", "graphite", 1290, "fact", [E_GN, E_FU], [obj("phone", "2026-10-25/phone", w=420, y=1290, rot=-6, anim="drop", vibrate=2)], None,
     "گوشی که می‌لرزد = آنباکسینگ جلوی دوربین و میلیون‌ها بازدید"),
    ("S4", "paper", None, "fact", [E_GN, E_YI], [obj("stamp", "2026-10-29/stamp", w=360, y=1270, anim="drop")], None,
     "مُهر که پایین می‌آید = تصمیم رسمی: بازپرداخت یا اعتبار برای همه"),
    ("S5", "graphite", 1290, "interpretation", [E_FU], [TAG(anim="drop", rot=-8)], None,
     "چرخش ایده (drop): برچسب قیمتِ خالی = مشکل خودِ قیمت بود، نه کالا؛ در S6 و S7 ادامه دارد"),
    ("S6", "paper", None, "interpretation", None, [KEY(anim="pop", float=5)], None,
     "جاکلیدی فشاری کوچک و بامزه = همین اقلام با قیمت دیگر، هدیه‌ای بامزه بودند"),
    ("S7", "graphite", 1285, "fact", [E_YH, E_YI], [PHOTO], None,
     "عکس واقعی محصول نایکی‌اسکیمز (آپلود مالک) در قاب روی صحنه‌ی تیره = این چیزی است که اسکیمز می‌فروشد؛ و در تقویم نبود"),
    ("S8", "paper", None, "interpretation", [E_YH], [TAG(anim="drop", x=560, y=1385, rot=6, w=400)], "S8",
     "برچسب قیمت برمی‌گردد و عدد ۱۴۸ بالایش می‌نشیند = قیمت یک قول است"),
    ("S9", "graphite", 1300, "interpretation", [E_OL], [obj("scale", "2026-10-22/scale", w=520, y=1300, anim="fade")], None,
     "ترازو = رضایت، سنجیدنِ آنچه گرفتی با آنچه انتظار داشتی"),
    ("S10", "paper", None, "interpretation", [E_FU], [obj("mega", "2026-11-06/megaphone", w=540, y=1300, credit=AI_NEW, anim="slide_l", vibrate=2)], None,
     "بلندگو = هر آنباکسینگ حالا نقدی است که بلند گفته می‌شود"),
    ("S11", "graphite", None, "interpretation", [E_GN, E_FU], None, "S11",
     "احتیاط یک بار: منظره‌یاب = فقط قابِ واکنش‌ها را دیده‌ایم، نه عدد فروش و ضرر"),
    ("S12", "paper", None, "interpretation", None, [CAL(anim="fade", w=520), obj("lens", "2026-10-22/magnifier", w=380, y=1300, rot=-10, anim="slide_r", path=[[0.6, 700, 1250], [2.0, 470, 1320], [3.2, 640, 1360]])], None,
     "ذره‌بین روی کشوهای تقویم = پیش از قیمت‌گذاری، پشت هر در را بسنج"),
    ("S13", "graphite", 1290, "interpretation", None, [CAL(anim="rise", w=560)], None,
     "بازگشت جعبه‌ی آغاز زیر نور = بسته قول می‌دهد، داخلش باید پای قول بایستد"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("اسکیمز، برند کیم کارداشیان،", "b"), ("تقویم کریسمس *۱۴۸* دلاری فروخت.", "h")],
    "S2": [("پشت درهایش:", "b"), ("کش مو، گیره، *جاکلیدی*.", "h")],
    "S3": [("خریدارها جعبه را جلوی دوربین باز کردند.", "b"), ("*میلیون‌ها* نفر تماشا کردند.", "h")],
    "S4": [("اسکیمز عذرخواهی کرد", "b"), ("و به *همه* پیشنهاد بازپرداخت داد.", "h")],
    "S5": [("ولی مشکل، کش مو نبود.", "b"), ("مشکل *برچسب قیمت* بود.", "h")],
    "S6": [("همین جعبه، ارزان‌تر،", "b"), ("می‌شد هدیه‌ای *بامزه*.", "h")],
    "S7": [("و یک برند پوشاک،", "b"), ("*پوشاک* را جا انداخت.", "h")],
    "S8": [("قیمت فقط یک عدد نیست.", "b"), ("یک *قول* است.", "h")],
    "S9": [("رضایت، یک تفریق ساده است:", "b"), ("آنچه گرفتی، *منهای* آنچه انتظار داشتی.", "h")],
    "S10": [("حالا هر جعبه‌ای که باز می‌شود،", "b"), ("یک نقد *عمومی* است.", "h")],
    "S11": [("از فروش و ضررش خبر نداریم.", "b"), ("فقط *واکنش‌ها* را دیده‌ایم.", "h")],
    "S12": [("پیش از قیمت‌گذاری بپرسید:", "b"), ("پشت *هر در* چه هست؟", "h")],
    "S13": [("جعبه‌ی زیبا قول می‌دهد.", "b"), ("*داخلش* باید پای قول بایستد.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Kim Kardashian's Skims", "b"), ("sold a *$148* advent calendar.", "h")],
    "S2": [("Behind the doors:", "b"), ("hair ties, clips, a *keychain*.", "h")],
    "S3": [("Buyers filmed the unboxing.", "b"), ("*Millions* watched.", "h")],
    "S4": [("Skims apologized", "b"), ("and offered *every* buyer a refund.", "h")],
    "S5": [("But hair ties weren't the problem.", "b"), ("The *price tag* was.", "h")],
    "S6": [("Same box, lower price:", "b"), ("a *cute* gift.", "h")],
    "S7": [("And a clothing brand", "b"), ("*left out* the clothes.", "h")],
    "S8": [("A price isn't just a number.", "b"), ("It's a *promise*.", "h")],
    "S9": [("Satisfaction is simple math:", "b"), ("what you got, *minus* what you expected.", "h")],
    "S10": [("Now every unboxing", "b"), ("is a *public* review.", "h")],
    "S11": [("We don't know the sales hit.", "b"), ("Only the *reaction*.", "h")],
    "S12": [("Before you price it, ask:", "b"), ("what's behind *each door*?", "h")],
    "S13": [("A beautiful box makes a promise.", "b"), ("What's *inside* has to keep it.", "h")],
    "S14": [("Write to me.", "b")],
}
VO = {"S1": "Kim Kardashian's Skims sold a hundred and forty-eight dollar advent calendar.",
      "S9": "Satisfaction is simple math. What you got, minus what you expected."}

SOURCES = [
    {"publisher": "Yahoo Entertainment (Where Is The Buzz; Skims statement to Today.com)", "title": "Kim Kardashian's Skims Offers Refunds After $148 Advent Calendar Sparks Backlash", "date": "2026-11-09", "url": YH},
    {"publisher": "Global News", "title": "SKIMS to refund $148 advent calendar filled with hair ties, bobby pins", "date": "2026-11-10", "url": GN},
    {"publisher": "FashionUnited", "title": "Skims' advent calendar backlash tests the limits of brand-led pricing", "date": "2026-11-09", "url": FU},
    {"publisher": "Yahoo (The Independent)", "title": "Kim Kardashian's lingerie brand forced to offer refunds for 'absolute joke' £158 advent calendar", "date": "2026-11-10", "url": YI},
    {"publisher": "Journal of Marketing Research 17(4):460-469 (Richard L. Oliver)", "title": "A Cognitive Model of the Antecedents and Consequences of Satisfaction Decisions", "date": "1980", "url": OL},
]

CAP_FA = """اسکیمز، برند کیم کارداشیان، یک تقویم کریسمسِ ۱۴۸ دلاری فروخت. پشت درهایش کش مو بود.

تقویم «اکسسوری» اسکیمز آخر اکتبر عرضه شد: ۱۴۸ دلار در آمریکا و ۱۵۸ پوند در بریتانیا، با وعده‌ی «دوازده روز سورپرایز». داخلش کش مو، اسکرانچی، سنجاق سر، گیره، جاکلیدی و یک عروسک فشاری بود؛ هیچ لباسی، حتی یک لباس زیر، در کار نبود. ویدیوی آنباکسینگ یکی از اینفلوئنسرها در تیک‌تاک بیش از ۱۸ میلیون بار دیده شد. اسکیمز گفت تقویم «برای بعضی‌ها انتظارات را برآورده نکرد»، با همه‌ی خریدارها تماس گرفت و بازپرداخت کامل یا اعتبار خرید پیشنهاد داد.

به نظر من مشکل، کش مو نبود. همین اقلام با قیمت دیگری هدیه‌ای بامزه بودند. و برندی که لباس می‌فروشد، در تقویمش هیچ لباسی نگذاشت. قیمت یک قول است. مدل کلاسیک ریچارد اولیور (۱۹۸۰) می‌گوید رضایت به فاصله‌ی «آنچه انتظار داشتی» و «آنچه گرفتی» بستگی دارد. قیمت بالا انتظار را بالا برد، و آنباکسینگ این فاصله را جلوی میلیون‌ها نفر گذاشت.

حدودش: از فروش یا ضرر مالی اسکیمز عددی منتشر نشده؛ آمار بازدیدها در گزارش‌های مختلف فرق دارد (۱۸٫۹ تا بیش از ۲۲ میلیون)؛ «رضایت = گرفته منهای انتظار» ساده‌شده‌ی آن مدل است. منابع: Global News، FashionUnited، Yahoo/The Independent و Journal of Marketing Research. اشیای این ریل با هوش مصنوعی ساخته شده‌اند و جعبه‌ی تقویم بی‌برند و نمایشی است. لوگو و عکس نایکی‌اسکیمز متعلق به صاحبانشان است و فقط برای نقد و تحلیل نشان داده شده.

اگر امروز محصولتان را جلوی دوربین باز کنند، کدام در خالی‌تر از قیمتش است؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Kim Kardashian's Skims sold a $148 advent calendar. Behind the doors: hair ties.

The Skims accessories calendar launched at the end of October: $148 in the US, £158 in the UK, sold as "12 days of fun surprises". Inside were hair elastics, scrunchies, bobby pins, clips, keychains and a squishy toy. No clothing, not even underwear. One creator's TikTok unboxing passed 18 million views. Skims said that "for some, the calendar didn't meet expectations", contacted every buyer and offered a full refund or store credit.

My take: hair ties weren't the problem. At a different price, the same box is a cute gift. And a clothing brand left out the clothes. A price is a promise. Richard Oliver's classic 1980 model says satisfaction depends on the gap between what you expected and what you got. The price set the expectation; the unboxing showed the gap to millions.

The limits: Skims hasn't published any sales or cost figures; view counts differ by outlet (18.9 to over 22 million); "what you got minus what you expected" is a simplification of that model. Sources: Global News, FashionUnited, Yahoo/The Independent, Journal of Marketing Research. The objects in this reel are AI-generated; the calendar box is an unbranded stand-in. The SKIMS logo and the NikeSKIMS photo belong to their owners and are shown for commentary.

If someone opened your product on camera today, which door would feel emptier than its price? Write to me.

— Behnood Kavian"""


COVER_OBJ = [{"src": f"assets/objects/{D}/advent_calendar.png", "x": 440, "y": 1180, "w": 620},
             {"src": f"assets/objects/{D}/hair_accessories.png", "x": 770, "y": 1390, "w": 460, "rot": -4}]
COVER = {"fa": {"bg": "paper", "kicker": "تقویم کریسمس اسکیمز", "title": ["۱۴۸ دلار", "برای *کش مو*؟"], "objects": COVER_OBJ},
         "en": {"bg": "paper", "kicker": "Skims' advent calendar", "title": ["$148", "for *hair ties*?"], "objects": COVER_OBJ}}


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
        if sid == "S14": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        if lang == "en" and VOICE and sid in VO: s["vo"] = VO[sid]
        scenes.append(s)
    r = {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
         "topic": "تقویم ۱۴۸ دلاری اسکیمز پر از کش مو بود: قیمت یک قول است، و آنباکسینگ فاصله‌ی قول و جعبه را عمومی می‌کند" if lang == "fa" else "Skims' $148 advent calendar was full of hair ties: a price is a promise, and the unboxing makes the gap public",
         "pillar": "pricing_brand_promise", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#skims", "#adventcalendar"] if lang == "fa" else ["#marketing", "#branding", "#skims", "#adventcalendar"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}
    r["cover"] = COVER[lang]
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
