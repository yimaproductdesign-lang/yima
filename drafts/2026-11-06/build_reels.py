"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-06 from one shared visual plan.
Topic: loud is not many. John Lewis's 2026 Christmas ad ("Gloria and Pickles") was slammed by columnists and
social media, yet in a OnePulse poll 68% said they liked or loved it, and System1 rated it 5.6 Stars."""
import json, os, pathlib

D = "2026-11-06"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-06T02:00:00Z"
DR = "https://news.designrush.com/john-lewis-saatchi-2026-christmas-ad-backlash"
FT = "https://www.fashiontimes.co.uk/john-lewis-christmas-advert-backlash-2026-1767078"
AT = "https://www.advanced-television.com/2026/11/04/john-lewis-2026-xmas-ad-scores-high-with-system1/"
CB = "https://campaignbrief.com/john-lewis-christmas-ad-scores-5-6-stars-its-highest-rating-since-excitable-edgar-in-2019/"
TD = "https://www.thedrum.com/opinion/andrew-tindall-they-may-be-loud-but-only-6-hated-the-john-lewis-christmas-ad-it-will-work"

E_BACK = {"url": FT, "publisher": "Fashion Times", "event_date": "2026-11-05", "retrieved_at": RT,
          "claim": "Gloria and Pickles drew a backlash: critics called the children 'horrid', 'spoilt, entitled, rude'; storyline 'out of touch', materialistic."}
E_DR = {"url": DR, "publisher": "DesignRush", "event_date": "2026-11-04", "retrieved_at": RT,
        "claim": "OnePulse: 68% liked or loved the ad; 36% more likely to shop, 58% no difference; System1 5.6 Stars; no sales data yet."}
E_AT = {"url": AT, "publisher": "Advanced Television", "event_date": "2026-11-04", "retrieved_at": RT,
        "claim": "System1 5.6 Stars, best John Lewis score since 2019; much of the press and social media reacted negatively."}


def obj(key, path_, x=540, y=1300, w=420, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


CRIT = {"fa": ["لوس", "بی‌ربط", "مادی", "بی‌احساس", "دور از مردم", "پرخرج", "بدترین", "سرد"],
        "en": ["spoilt", "out of touch", "tone deaf", "materialistic", "cold", "worst ever", "rude", "cynical"]}
LIKED = {"fa": (["خوب بود", "دوستش داشتم", "گرم", "قشنگ", "عاشقش شدم", "۶۸٪"], "۶۸٪"),
         "en": (["nice", "loved it", "warm", "liked it", "sweet", "68%"], "68%")}
SIFT = {"fa": (["لوس", "بدترین", "حرف درست", "بی‌ربط", "سرد", "مادی"], "حرف درست"),
        "en": (["spoilt", "worst ever", "fair point", "tone deaf", "cold", "cynical"], "fair point")}
WORKED = {"fa": ["طعمِ آشنا", "فونتِ تابلو", "رنگِ لیوان", "اسم‌های منو", "بسته‌ی قدیمی"],
          "en": ["the old recipe", "the sign font", "cup colour", "menu names", "the old pack"]}
LBL = {"fa": ("صدای بلند", "۶۸٪"), "en": ("loud", "68%")}
LBL2 = {"fa": ("کامنت‌ها", "سفارشِ دوباره"), "en": ("comments", "repeat orders")}

CR_A = "Chart: OnePulse via DesignRush (shopping intent after the ad), owner upload"
CR_B = "Image: John Lewis / Saatchi & Saatchi ad still, cropped to the set decor (no people), owner upload"
TA_AR = 1798 / 1400
TB_AR = 400 / 210


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1200, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.03, "color": [0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


def fx_for(sid, lang):
    en = lang == "en"
    if sid in ("S1", "S4"):
        return [{"type": "rings", "x": 300 if sid == "S1" else 340, "y": 1290 if sid == "S1" else 1300, "R": 420, "n": 5,
                 "period": 1.0 if sid == "S1" else 0.7, "t": 0.6, "op": 0.35}]
    if sid == "S2":
        return [{"type": "words", "mode": "pop", "box": [140, 960, 940, 1520] if en else [140, 980, 940, 1500],
                 "seed": 141 if en else 23, "size": 52 if en else 56, "stagger": 0.08, "words": CRIT[lang]}]
    if sid == "S5":
        ws, k = LIKED[lang]
        return [{"type": "words", "mode": "fade", "box": [150, 960, 930, 1480], "seed": 5, "size": 68, "t0": 0.9,
                 "words": ws, "keep": [k], "keep_at": [540, 1220]}]
    if sid == "S6":
        a, b = LBL[lang]
        return [{"type": "labels", "items": [{"text": a, "x": 330, "y": 1260, "move": "up", "t": 1.4, "size": 92},
                                             {"text": b, "x": 760, "y": 1260, "move": "down", "acc": True, "t": 1.4, "size": 120}]}]
    if sid == "S8":
        ws, k = SIFT[lang]
        return [{"type": "words", "mode": "sift", "box": [160, 940, 920, 1000], "target": [540, 1360], "seed": 9, "size": 58,
                 "keep": [k], "stagger": 0.02, "words": ws}]
    if sid == "S10":
        return [{"type": "swatch", "y": 1220, "t": 1.4}]
    if sid == "S11":
        return [{"type": "words", "mode": "fade", "box": [150, 980, 930, 1460], "seed": 11, "size": 56, "t0": 0.8,
                 "words": WORKED[lang]}]
    if sid == "S13":
        a, b = LBL2[lang]
        return [{"type": "labels", "items": [{"text": a, "x": 300, "y": 1250, "move": "up", "t": 1.4, "size": 76},
                                             {"text": b, "x": 720, "y": 1250, "move": "down", "acc": True, "t": 1.4, "size": 84}]}]
    return None


MEG = dict(credit=AI_NEW)
# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1290, "fact", [E_BACK, E_DR], [obj("meg", f"{D}/megaphone", w=600, y=1290, anim="drop", vibrate=3, **MEG)], "S1",
     "قلاب: بلندگوی فلزی زیر نور با موج‌های صدا = چند صدای خیلی بلند؛ همان چیزی که «اینترنت» را می‌سازد"),
    ("S2", "paper", None, "fact", [E_BACK, E_AT], None, "S2",
     "ابرِ شلوغِ واژه‌های انتقاد (لوس، مادی، بدترین…) که هم‌زمان چشمک می‌زنند = رگبارِ انتقاد، به زبانِ خودِ منتقدها"),
    ("S3", "graphite", 1220, "fact", [E_BACK, E_AT], [frame("tb", "T-b_decor.png", TB_AR, CR_B, DR, w=720, y=1230)], None,
     "تصویر واقعی تبلیغ (آپلود مالک)، فقط دکورِ پرزرق‌وبرق، بی‌چهره: همان صحنه‌ای که منتقدها «دور از مردم» خواندند"),
    ("S4", "paper", None, "fact", [E_BACK], [obj("meg", f"{D}/megaphone", w=520, y=1300, anim="slide_r", vibrate=2, **MEG)], "S4",
     "بلندگو برمی‌گردد و موج‌ها تندتر می‌شوند = ستون‌نویس و کامنت و تیتر، همه با یک بلندگو"),
    ("S5", "graphite", 1220, "fact", [E_DR], None, "S5",
     "واژه‌های واکنشِ عادیِ مردم (خوب بود، دوستش داشتم…) محو می‌شوند و فقط «۶۸٪» می‌ماند و بزرگ می‌شود = صدای آرامِ اکثریت"),
    ("S6", "paper", None, "interpretation", None, None, "S6",
     "چرخش (drop): «صدای بلند» سبک است، بالا می‌رود و محو می‌شود؛ «۶۸٪» سنگین پایین می‌نشیند = بلندی وزن ندارد، تعداد دارد"),
    ("S7", "graphite", 1300, "interpretation", None, [obj("ear", f"{D}/ear_trumpet", w=720, y=1300, anim="slide_l", float=3, credit=AI_NEW)], None,
     "شیپورِ گوش = باید گوش را جلو برد تا ساکت‌ها را شنید؛ کسانی که خوششان آمده پست نمی‌گذارند"),
    ("S8", "paper", None, "interpretation", None, None, "S8",
     "واژه‌های انتقاد فرو می‌ریزند و فقط «حرف درست» می‌ماند = انتقاد را وزن کن، نه حجمش را؛ می‌تواند درست باشد و باز اقلیت"),
    ("S9", "graphite", 1200, "fact", [E_DR], [frame("ta", "T-a.png", TA_AR, CR_A, DR, w=780, y=1250)], None,
     "احتیاط یک بار، با سندِ واقعی (آپلود مالک، کامل و رنگی): نمودارِ همان نظرسنجی؛ برای ۵۸٪ خرید فرقی نمی‌کند و فروش هنوز نیامده"),
    ("S10", "paper", None, "interpretation", None, None, "S10",
     "کارت‌های رنگ که جابه‌جا می‌شوند = وسوسه‌ی فردای طوفان: همه‌چیز را از نو رنگ کردن"),
    ("S11", "graphite", 1220, "interpretation", None, None, "S11",
     "نام چیزهایی که کار می‌کردند (طعم آشنا، فونت تابلو…) یکی‌یکی محو می‌شوند = پاک کردنِ همان که داشت کار می‌کرد"),
    ("S12", "paper", None, "interpretation", None, [obj("cup", "2026-10-29/cup", w=460, y=1300, anim="rise", float=2)], None,
     "فنجانِ همیشگی = مشتریِ ثابت که کامنت نمی‌گذارد و فقط دوباره سفارش می‌دهد"),
    ("S13", "graphite", 1250, "interpretation", None, None, "S13",
     "ترازوی واژه‌ها: «کامنت‌ها» بالا می‌رود و محو می‌شود، «سفارشِ دوباره» سنگین می‌ماند = رأیِ واقعی در فروش است"),
    ("S14", "paper", None, "interpretation", None, [obj("key", "2026-10-24/key", w=520, y=1300, rot=-20, anim="slide_l", float=2)], None,
     "کلید = فرمانِ برند؛ به منتقد جواب بده، ولی کلید را دستش نده"),
    ("S15", "graphite", 1270, "interpretation", None, [obj("meg", f"{D}/megaphone", w=500, y=1270, rot=90, anim="fade", **MEG)], None,
     "بازگشت به آغاز: همان بلندگو، حالا بی‌صدا و رو به آسمان، بدون موج = بلندی اندازه‌ی صداست، نه اندازه‌ی جمعیت"),
    ("S16", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("اینترنت گفت شکست خورد.", "b"), ("مردم گفتند *دوستش* دارند.", "h")],
    "S2": [("تبلیغِ کریسمسِ جان لوئیس", "b"), ("این هفته زیرِ *رگبار* رفت.", "h")],
    "S3": [("یک جشنِ پرزرق‌وبرق.", "b"), ("منتقدها گفتند: *دور از مردم*.", "h")],
    "S4": [("ستون‌نویس‌ها، کامنت‌ها، تیترها:", "b"), ("همه *یک‌صدا*.", "h")],
    "S5": [("همان روزها کسی از خودِ مردم پرسید.", "b"), ("*۶۸ درصد* گفتند دوستش دارند.", "h")],
    "S6": [("صدای بلند", "b"), ("صدای *اکثریت* نیست.", "h")],
    "S7": [("آن‌هایی که خوششان آمد", "b"), ("*کامنت* نمی‌گذارند.", "h")],
    "S8": [("انتقاد می‌تواند درست باشد", "b"), ("و باز هم *اقلیت* باشد.", "h")],
    "S9": [("همان نظرسنجی؛ فروش هنوز نیامده.", "b"), ("خریدِ *۵۸ درصد* عوض نمی‌شود.", "h")],
    "S10": [("خطر، فردای طوفان است:", "b"), ("همه‌چیز را *از نو* رنگ می‌کنید.", "h")],
    "S11": [("منو، تابلو، بسته‌بندی؛", "b"), ("همان که داشت *کار* می‌کرد.", "h")],
    "S12": [("مشتریِ همیشگی‌تان کامنت نمی‌گذارد.", "b"), ("فقط *دوباره* سفارش می‌دهد.", "h")],
    "S13": [("پیش از هر تغییر، از ده مشتری بپرسید", "b"), ("و *فروشِ* هفته را ببینید.", "h")],
    "S14": [("به منتقد مؤدبانه جواب بدهید.", "b"), ("ولی *کلید* را دستش ندهید.", "h")],
    "S15": [("بلندی، اندازه‌ی صداست؛", "b"), ("نه اندازه‌ی *جمعیت*.", "h")],
    "S16": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("The internet called it a flop.", "b"), ("People said they *liked* it.", "h")],
    "S2": [("John Lewis's Christmas ad", "b"), ("got *torn apart* this week.", "h")],
    "S3": [("A glittering party.", "b"), ("Critics said: *out of touch*.", "h")],
    "S4": [("Columnists. Comments. Headlines.", "b"), ("All one *voice*.", "h")],
    "S5": [("Meanwhile, someone asked people.", "b"), ("*68%* liked or loved it.", "h")],
    "S6": [("Loud", "b"), ("isn't *many*.", "h")],
    "S7": [("The people who liked it", "b"), ("don't *post* about it.", "h")],
    "S8": [("Criticism can be right", "b"), ("and still be the *minority*.", "h")],
    "S9": [("Same poll. Sales aren't in yet.", "b"), ("For *58%*, shopping won't change.", "h")],
    "S10": [("The morning after,", "b"), ("you *repaint* it all.", "h")],
    "S11": [("The menu. The sign. The pack.", "b"), ("The thing that was *working*.", "h")],
    "S12": [("Your regulars never comment.", "b"), ("They just order *again*.", "h")],
    "S13": [("First, ask ten regulars.", "b"), ("Then check the *till*.", "h")],
    "S14": [("Answer the critic, politely.", "b"), ("Don't hand over the *keys*.", "h")],
    "S15": [("Loud is a volume,", "b"), ("not a *headcount*.", "h")],
    "S16": [("Write to me.", "b")],
}
VO = {"S5": "Meanwhile, someone asked people. Sixty-eight percent liked or loved it.",
      "S9": "Same poll. Sales aren't in yet. For fifty-eight percent, shopping won't change."}

SOURCES = [
    {"publisher": "DesignRush", "title": "John Lewis Ad Scores 5.6 Stars at System1, Lacks Punch for Kantar", "date": "2026-11-04", "url": DR},
    {"publisher": "Fashion Times", "title": "John Lewis's 2026 Christmas Ad Sparks Backlash Over 'Horrid Kids' and Materialistic Storyline", "date": "2026-11-05", "url": FT},
    {"publisher": "Advanced Television", "title": "John Lewis 2026 Xmas ad scores high with System1", "date": "2026-11-04", "url": AT},
    {"publisher": "Campaign Brief", "title": "John Lewis Christmas ad scores 5.6 Stars, its highest rating since 'Excitable Edgar' in 2019", "date": "2026-11-05", "url": CB},
    {"publisher": "The Drum (Andrew Tindall, System1)", "title": "They may be loud, but only 6% hated the John Lewis Christmas ad. It will work", "date": "2026-11-04", "url": TD},
]

CAP_FA = """اینترنت گفت تبلیغ شکست خورد. مردم گفتند دوستش دارند.

تبلیغ کریسمسِ امسالِ جان لوئیس («گلوریا و پیکلز») این هفته زیرِ رگبارِ انتقاد رفت: یک ستون‌نویس بچه‌های داستان را «لوس، طلبکار و بی‌ادب» خواند و خیلی‌ها در شبکه‌های اجتماعی گفتند قصه‌اش مادی و دور از زندگیِ مردم است.

همان روزها کسی از خودِ مردم پرسید. در نظرسنجیِ وان‌پالس، ۶۸ درصد گفتند تبلیغ را دوست دارند یا عاشقش‌اند؛ در همان نظرسنجی ۳۶ درصد گفتند احتمال خریدشان بیشتر شده و برای ۵۸ درصد فرقی نمی‌کند. در آزمونِ شرکتِ System1 هم ۵٫۶ ستاره گرفت، بهترین امتیازِ جان لوئیس از ۲۰۱۹؛ و به گفته‌ی همین شرکت، فقط ۶ درصد واقعاً از آن بیزار بودند. صدای بلند، صدای اکثریت نیست. آن‌هایی که خوششان آمده معمولاً چیزی نمی‌نویسند.

حدودش را بگویم: این‌ها نظرسنجی و آزمونِ سریع‌اند، نه فروش؛ اندازه‌ی نمونه منتشر نشده، عددِ ۶ درصد را یکی از کارکنانِ خودِ System1 نوشته، و کانتار معتقد است تبلیغ «ضربه‌ی احساسیِ سال‌های قبل» را ندارد. فروشِ کریسمس هنوز نیامده. نمودار و تصویرِ دکورِ تبلیغ آپلود مالک‌اند (از DesignRush و خودِ تبلیغ، بدون چهره)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند. من درباره‌ی خوب یا بد بودنِ این تبلیغ حکم نمی‌دهم؛ حرفم درباره‌ی شمردنِ صداهاست. انتقاد می‌تواند درست باشد و باز هم اقلیت باشد.

برای صاحب کسب‌وکار: فردای یک موجِ عصبانی، منو و تابلو و بسته‌بندی را عوض نکنید. از ده مشتریِ همیشگی بپرسید، سفارش‌های دوباره و فروشِ هفته را ببینید. به منتقد مؤدبانه جواب بدهید، ولی بگذارید اکثریتِ ساکت رأی بدهد.

آخرین باری که چند صدای بلند شما را به تغییرِ چیزی واداشت، کِی بود، و بعدش فروش چه شد؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """The internet called it a flop. People said they liked it.

John Lewis's 2026 Christmas ad, "Gloria and Pickles", got torn apart this week. One columnist called the children "spoilt, entitled, rude"; plenty of people online called the story materialistic and out of touch.

Meanwhile, someone asked people. In a OnePulse poll, 68% said they liked or loved it; in the same poll, 36% said they were more likely to shop there and 58% said it made no difference. System1 gave it 5.6 Stars, John Lewis's best score since 2019, and System1's Andrew Tindall wrote in The Drum that only 6% felt real contempt. Loud isn't the same as many. The people who like something rarely post about it.

The limits: these are quick polls and ad tests, not sales. Sample sizes weren't published, the 6% figure comes from someone who works at System1, and Kantar's view is that the ad "lacks the emotive punch" of earlier years. Christmas sales aren't in yet. The chart and the set-decor still are owner uploads (from DesignRush and the ad itself, no faces shown); the other objects are AI-generated. I'm not judging whether the ad is good; my point is about how we count voices. Criticism can be right and still be the minority.

For owners: the morning after an angry wave, don't repaint the menu, the sign or the pack. Ask ten regulars, check repeat orders and the week's takings. Answer the critic politely, then let the quiet majority vote.

When did a few loud voices last push you to change something, and what happened to sales after? Write to me.

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
        if sid == "S16": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        if lang == "en" and VOICE and sid in VO: s["vo"] = VO[sid]
        scenes.append(s)
    r = {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
         "topic": "صدای بلند، صدای اکثریت نیست: انتقادِ پرسروصدا را وزن کن، نه حجمش را" if lang == "fa" else "Loud isn't many: weigh the backlash, don't count its volume",
         "pillar": "brand_communication_consumer_behaviour", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#brandstrategy", "#consumerbehavior"] if lang == "fa" else ["#branding", "#marketing", "#brandstrategy", "#consumerbehavior"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S6"}, "status": "DRAFT", "style": "editorial", "lang": lang}
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
