"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-14 from one shared visual plan.
Topic (type 3, secret behind a familiar brand): Coca-Cola didn't make Santa red; it repeated one Santa
for 33 years (Sundblom, 1931-1964) until the world gave Coke the credit. Idea: you own an asset by repeating it, not by inventing it."""
import json, os, pathlib

D = "2026-11-14"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-14T04:30:00Z"
KO = "https://www.coca-cola.com/us/en/about-us/faq/did-coca-cola-create-santa-claus"
LF = "https://www.logicallyfacts.com/en/fact-check/true-coca-cola-played-a-part-in-santa-s-iconic-red-image"
VF = "https://kgw.com/article/news/verify/holiday-verify/coca-cola-did-not-invent-santa-claus-modern-image-costume-red-suit/536-d4c9529c-e97d-48e5-92e2-912c7ee609fc"
WR = "https://whiterockbeverages.com/news/ho-ho-ho-setting-the-facts-straight"
FE = "https://theferret.scot/fact-check-coca-cola-red-santa-claus-christmas/"
TR = "https://www.theodorerooseveltcenter.org/digital-library/o276284/"
HU = "https://thehustle.co/12222020-coca-cola"
KCA = "https://www.coca-colacompany.com/company/history/five-things-you-never-knew-about-santa-claus-and-coca-cola"

E_KO = {"url": KO, "publisher": "The Coca-Cola Company (official FAQ)", "event_date": "undated", "retrieved_at": "2026-11-13T17:00:00Z",
        "claim": "Coca-Cola did not create the legend of Santa Claus; its advertising, starting with Haddon Sundblom's 1931 Santa, helped shape his modern image."}
E_LF = {"url": LF, "publisher": "Logically Facts", "event_date": "2020-12-22", "retrieved_at": RT,
        "claim": "Red-suited Santas existed before Coca-Cola's campaign; Sundblom painted Santa for Coca-Cola ads from 1931 to 1964, run in the Saturday Evening Post, The New Yorker, National Geographic etc. and on billboards, posters, calendars and store displays."}
E_VF = {"url": VF, "publisher": "KGW / VERIFY", "event_date": "undated", "retrieved_at": RT,
        "claim": "White Rock used the modern Santa in a 1915 mineral-water ad and a 1923 ginger-ale ad; Nast's red-and-white scheme was common about 50 years before Coke; Coca-Cola popularised the image but did not invent it."}
E_WR = {"url": WR, "publisher": "White Rock Beverages (official)", "event_date": "undated", "retrieved_at": "2026-11-13T17:00:00Z",
        "claim": "White Rock ran Santa ads in 1915-16 and colour Santa ads in 1923-25."}
E_TR = {"url": TR, "publisher": "Theodore Roosevelt Center / Library of Congress (Puck, 3 Dec 1902)", "event_date": "1902-12-03", "retrieved_at": "2026-11-13T17:00:00Z",
        "claim": "Puck Christmas cover 1902 (Frank A. Nankivell) shows Santa in a red suit with white fur (verified by eye on owner upload T-b)."}
E_HU = {"url": HU, "publisher": "The Hustle", "event_date": "2020-12-22", "retrieved_at": RT,
        "claim": "Sundblom's first Coke Santa 1931, last 1964 (over three decades); Coke did not invent Santa; the red is not a deliberate brand-colour choice."}


def obj(key, path_, x=540, y=1290, w=460, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


HAT = lambda **kw: obj("hat", f"{D}/santa_hat", **{"w": 400, "y": 1300, "credit": AI_NEW, "color": [0, 0, 0], **kw})
TA = {"key": "ta", "src": f"incoming/{D}/T-a.png", "x": 540, "y": 1320, "w": 360, "frame": True, "ar": round(720 / 925, 3), "color": [0, 0, 0],
      "credit": "The Coca-Cola Company / Haddon Sundblom (Saturday Evening Post ad; owner upload T-a)", "source_url": KCA, "anim": "rise"}
TB = {"key": "tb", "src": f"incoming/{D}/T-b.png", "x": 540, "y": 1270, "w": 430, "frame": True, "ar": round(1216 / 1600, 3), "color": [0, 0, 0],
      "credit": "Puck, 3 Dec 1902, Frank A. Nankivell / Library of Congress (owner upload T-b)", "source_url": TR, "anim": "zoom"}
TD = {"key": "td", "src": f"incoming/{D}/T-d.png", "x": 540, "y": 1290, "w": 700, "frame": True, "ar": round(825 / 578, 3), "color": [0, 0, 0],
      "credit": "Coca-Cola holiday postcard (owner upload T-d)", "source_url": "https://www.coca-cola.com/us/en/about-us/faq/did-coca-cola-create-santa-claus", "anim": "rise"}

WORDS = {"fa": (["مجله", "بیلبورد", "تقویم", "پوستر", "ویترین", "کارت پستال"], ["تقویم"]),
         "en": (["magazine", "billboard", "calendar", "poster", "store display", "postcard"], ["calendar"])}


def fx_for(sid, lang):
    if sid == "S5":
        return [{"type": "rings", "x": 540, "y": 1290, "n": 6}]
    if sid == "S7":
        w, k = WORDS[lang]
        return [{"type": "words", "mode": "pop", "words": w, "keep": k, "box": [110, 1000, 970, 1540], "size": 54, "seed": 5}]
    if sid == "S11":
        return [{"type": "viewfinder", "box": [200, 1060, 880, 1500], "t": 0.5}]
    return None


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1270, "fact", [E_KO, E_HU], [TA], None,
     "تبلیغ واقعی ساندبلوم برای کوکاکولا (آپلود مالک) در قاب روی صحنه‌ی تیره = همان بابانوئلی که همه به اسم کوکاکولا می‌شناسند؛ در پایان با T-d برمی‌گردیم"),
    ("S2", "paper", None, "interpretation", [E_HU], [HAT(anim="pop", float=5)], None,
     "کلاه قرمز بابانوئل با رنگ طبیعی = خودِ «قرمز»ی که افسانه به کوکاکولا نسبت می‌دهد؛ در S12 برمی‌گردد"),
    ("S3", "graphite", 1270, "fact", [E_TR, E_VF], [TB], None,
     "جلد پاک ۱۹۰۲ (آپلود مالک) در قاب = سند: بابانوئل ۲۹ سال پیش از ۱۹۳۱ قرمز پوشیده بود"),
    ("S4", "paper", None, "fact", [E_VF, E_WR],
     [obj("photo", "2026-10-22/photo", w=560, y=1290, rot=-3, anim="fade"),
      obj("lens", "2026-10-22/magnifier", w=360, y=1300, rot=-10, anim="slide_r", path=[[0.6, 720, 1250], [2.0, 470, 1320], [3.2, 620, 1340]])], None,
     "ذره‌بین روی عکس قدیمی = دقیق‌تر به تاریخ نگاه کن: یک نوشابه‌ی دیگر زودتر بابانوئل را در تبلیغش آورد"),
    ("S5", "graphite", 1290, "interpretation", [E_KO, E_LF], None, "S5",
     "چرخش ایده (drop): حلقه‌هایی که پشت سر هم از یک نقطه بیرون می‌زنند = تکرار بی‌وقفه، نه اختراع"),
    ("S6", "paper", None, "fact", [E_LF, E_HU], [obj("roller", "2026-10-26/paint_roller", w=560, y=1300, rot=-12, anim="slide_l",
                                                     path=[[0.4, 380, 1330], [1.6, 700, 1270], [2.8, 460, 1320]])], None,
     "غلتک رنگ که رفت‌وبرگشت می‌کند = همان تصویر را بارها و بارها روی دیوار کشیدن؛ ۳۳ سال یک نقاش"),
    ("S7", "graphite", None, "fact", [E_LF], None, "S7",
     "ابر کلمه‌های رسانه‌ها (مجله، بیلبورد، تقویم…) که شلوغ می‌شوند = همان چهره در همه‌جا، هر کریسمس"),
    ("S8", "paper", None, "interpretation", None, [obj("stone", "2026-10-26/worn_stone", w=600, y=1300, anim="rise")], None,
     "سنگ پله‌ی ساییده = تکرار طولانی در حافظه شیار می‌اندازد"),
    ("S9", "graphite", 1290, "interpretation", [E_KO, E_VF], [obj("stamp", "2026-10-29/stamp", w=360, y=1290, anim="drop")], None,
     "مُهری که پایین می‌آید = دنیا اسم کوکاکولا را پای بابانوئل زد"),
    ("S10", "paper", None, "interpretation", None, [obj("trophy", "2026-10-24/trophy", w=380, y=1300, anim="rise")], None,
     "جام = اعتبار و جایزه به کسی می‌رسد که دست نکشید، نه به اولی"),
    ("S11", "graphite", None, "fact", [E_KO, E_LF], None, "S11",
     "احتیاط یک بار: منظره‌یاب = قاب را دقیق کن؛ کوکاکولا چهره‌ی امروزی را شکل داد، رنگ را نه"),
    ("S12", "paper", None, "interpretation", None, [HAT(anim="drop", w=420, rot=-6)], None,
     "بازگشت کلاه قرمز = قرمز مال کوکاکولا نبود، ولی حالا به نامش است: مالکیت با تکرار"),
    ("S13", "graphite", 1290, "interpretation", [E_KO], [TD], None,
     "بستن دایره با همان چهره‌ی امروز (آپلود مالک) کنار کامیون = یک دارایی را انتخاب کن و آن‌قدر تکرار کن که مال تو شود"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("کوکاکولا بابانوئل را قرمز نکرد.", "b"), ("پس چرا *همه* فکر می‌کنند کرد؟", "h")],
    "S2": [("روایت معروف این است:", "b"), ("کوکاکولا لباسش را *قرمزِ برند* کرد.", "h")],
    "S3": [("این بابانوئل سال ۱۹۰۲ است.", "b"), ("همان وقت هم *قرمز* بود.", "h")],
    "S4": [("حتی یک نوشابه‌ی رقیب", "b"), ("*زودتر* در تبلیغش آوردش.", "h")],
    "S5": [("کوکاکولا اول نبود.", "b"), ("فقط *دست برنداشت*.", "h")],
    "S6": [("یک نقاش، یک بابانوئل،", "b"), ("*۳۳ سال* پشت سر هم.", "h")],
    "S7": [("مجله، بیلبورد، تقویم.", "b"), ("هر *کریسمس*.", "h")],
    "S8": [("یک چیز را آن‌قدر تکرار کن", "b"), ("تا در ذهن‌ها *شیار* بیندازد.", "h")],
    "S9": [("حالا دنیا", "b"), ("*اسم کوکاکولا* را رویش می‌نویسد.", "h")],
    "S10": [("اعتبار به اولی نمی‌رسد.", "b"), ("به کسی می‌رسد که *تکرار کرد*.", "h")],
    "S11": [("ولی انصاف بدهیم: کوکاکولا", "b"), ("چهره را ساخت، نه *رنگ* را.", "h")],
    "S12": [("لازم نیست اختراعش کنید.", "b"), ("باید *صاحبش* شوید.", "h")],
    "S13": [("یک چیز را انتخاب کنید.", "b"), ("آن‌قدر تکرار کنید که *مال شما* شود.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Coca-Cola didn't make Santa red.", "b"), ("Why does *everyone* think it did?", "h")],
    "S2": [("The story goes:", "b"), ("Coke dressed him in its *brand red*.", "h")],
    "S3": [("Here he is in 1902.", "b"), ("Already in *red*.", "h")],
    "S4": [("Even a rival soda", "b"), ("put him in its ads *first*.", "h")],
    "S5": [("Coke wasn't first.", "b"), ("It was *relentless*.", "h")],
    "S6": [("One painter. One Santa.", "b"), ("For *33 years*.", "h")],
    "S7": [("Magazines, billboards, calendars.", "b"), ("Every *Christmas*.", "h")],
    "S8": [("Repeat one thing long enough", "b"), ("and it wears a *groove*.", "h")],
    "S9": [("Now the whole world", "b"), ("writes *Coke's name* on him.", "h")],
    "S10": [("Credit doesn't go to the first.", "b"), ("It goes to whoever *never stopped*.", "h")],
    "S11": [("To be fair:", "b"), ("Coke shaped his face, not his *color*.", "h")],
    "S12": [("You don't have to invent it.", "b"), ("You have to *own* it.", "h")],
    "S13": [("Pick one thing.", "b"), ("Repeat it until it's *yours*.", "h")],
    "S14": [("Write to me.", "b")],
}
VO = {"S6": "One painter. One Santa. For thirty-three years.", "S3": "Here he is in nineteen-oh-two. Already in red."}

SOURCES = [
    {"publisher": "The Coca-Cola Company", "title": "Did Coca-Cola create Santa Claus? (FAQ)", "date": "undated (retrieved 2026-11-13)", "url": KO},
    {"publisher": "Logically Facts", "title": "True: Coca-Cola played a part in Santa's iconic red image", "date": "2020-12-22", "url": LF},
    {"publisher": "KGW / VERIFY", "title": "Coca-Cola did not invent Santa Claus' modern image", "date": "undated (retrieved 2026-11-14)", "url": VF},
    {"publisher": "White Rock Beverages", "title": "Ho Ho Ho: setting the facts straight", "date": "undated (retrieved 2026-11-13)", "url": WR},
    {"publisher": "The Hustle", "title": "Did Coca-Cola create Santa Claus?", "date": "2020-12-22", "url": HU},
    {"publisher": "Theodore Roosevelt Center / Library of Congress", "title": "Puck, Christmas cover, 3 December 1902 (Frank A. Nankivell)", "date": "1902-12-03", "url": TR},
    {"publisher": "The Ferret", "title": "Fact check: did Coca-Cola make Santa red?", "date": "2017-12-25", "url": FE},
]

CAP_FA = """کوکاکولا بابانوئل را قرمز نکرد. پس چرا همه فکر می‌کنند کرد؟

بابانوئل قرمزپوش دهه‌ها پیش از کوکاکولا وجود داشت. جلد کریسمس مجله‌ی «پاک» در ۱۹۰۲ او را با لباس قرمز و خز سفید نشان می‌دهد. نوشابه‌ی وایت‌راک هم در ۱۹۱۵ و ۱۹۲۳ بابانوئل را در تبلیغش آورد. خود کوکاکولا هم در صفحه‌ی رسمی‌اش می‌گوید بابانوئل را اختراع نکرده است.

کاری که کوکاکولا کرد ساده‌تر و سخت‌تر بود: از ۱۹۳۱ تا ۱۹۶۴، یعنی ۳۳ سال، هادون ساندبلوم همان بابانوئل را برایش کشید؛ در مجله‌ها، روی بیلبورد، تقویم و ویترین مغازه‌ها. به نظر من درسش برای هر برندی روشن است: لازم نیست اولین باشید. یک چیز را انتخاب کنید و آن‌قدر تکرارش کنید که مردم نتوانند بدون شما تصورش کنند.

حدودش: کوکاکولا در ساختن چهره‌ی گرم و امروزی بابانوئل و جهانی‌کردنش واقعاً نقش داشت؛ فقط رنگ قرمز را اختراع نکرد. این‌که دقیقاً چرا دنیا قرمز را به کوکاکولا نسبت می‌دهد اندازه‌گیری نشده و «تکرار» تفسیر من است. منابع: صفحه‌ی رسمی کوکاکولا، Logically Facts، KGW/VERIFY، وایت‌راک، The Hustle و کتابخانه‌ی کنگره (جلد پاک). تصویرهای تبلیغ و کارت پستال متعلق به کوکاکولا و جلد پاک از آرشیو کتابخانه‌ی کنگره است و فقط برای تحلیل نشان داده شده؛ اشیای دیگر ریل با هوش مصنوعی ساخته شده‌اند.

برند شما کدام یک چیز را آن‌قدر تکرار کرده که دیگر مال خودش شده باشد؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Coca-Cola didn't make Santa red. So why does everyone think it did?

Red-suited Santas existed decades before Coke. Puck magazine's 1902 Christmas cover shows him in red with white fur. White Rock, another soda brand, put Santa in its ads in 1915 and 1923. Coca-Cola's own FAQ says it didn't create Santa.

What Coke did was simpler, and harder: from 1931 to 1964, 33 years, Haddon Sundblom painted the same Santa for its ads. Magazines, billboards, calendars, store displays. My take: you don't need to be first. Pick one thing and repeat it until people can't picture it without you.

The limits: Coke really did shape Santa's warm, modern face and made him global; it just didn't invent the red. Why the world credits Coke hasn't been measured; "repetition" is my reading. Sources: The Coca-Cola Company FAQ, Logically Facts, KGW/VERIFY, White Rock, The Hustle, Library of Congress (Puck cover). The ad and postcard images belong to Coca-Cola, the Puck cover is from the Library of Congress; shown for commentary. The other objects are AI-generated.

What's the one thing your brand has repeated long enough to own? Write to me.

— Behnood Kavian"""

COVER_OBJ = [{"src": f"assets/objects/{D}/santa_hat.png", "x": 540, "y": 1300, "w": 560, "rot": -4}]
COVER = {"fa": {"bg": "paper", "kicker": "بابانوئلِ کوکاکولا", "title": ["کوکاکولا", "بابانوئل را *قرمز* نکرد"], "objects": COVER_OBJ},
         "en": {"bg": "paper", "kicker": "Coca-Cola's Santa", "title": ["Coke didn't", "make Santa *red*"], "objects": COVER_OBJ}}


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
         "topic": "کوکاکولا بابانوئل را قرمز نکرد؛ ۳۳ سال همان یکی را تکرار کرد تا دنیا اسمش را به نام کوکاکولا بنویسد" if lang == "fa" else "Coca-Cola didn't make Santa red; it repeated the same Santa for 33 years until the world gave Coke the credit",
         "pillar": "brand_assets_consistency", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#cocacola", "#santaclaus"] if lang == "fa" else ["#branding", "#marketing", "#cocacola", "#santaclaus"],
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
