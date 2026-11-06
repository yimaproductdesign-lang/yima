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
SIFT = {"fa": (["لوس", "بدترین", "حرف درست", "بی‌ربط", "سرد", "مادی"], "حرف درست"),
        "en": (["spoilt", "worst ever", "fair point", "tone deaf", "cold", "cynical"], "fair point")}
LBL = {"fa": ("صدای بلند", "۶۸٪"), "en": ("loud", "68%")}


def fx_for(sid, lang):
    if sid == "S1":
        return [{"type": "rings", "x": 300, "y": 1290, "R": 420, "n": 5, "period": 1.0, "t": 0.6, "op": 0.35}]
    if sid == "S3":
        en = lang == "en"
        return [{"type": "words", "mode": "pop", "box": [140, 960, 940, 1520] if en else [140, 980, 940, 1500],
                 "seed": 141 if en else 23, "size": 52 if en else 56, "stagger": 0.08,
                 "words": CRIT[lang]}]
    if sid == "S5":
        a, b = LBL[lang]
        return [{"type": "labels", "items": [{"text": a, "x": 330, "y": 1500, "move": "up", "t": 1.6, "size": 62},
                                             {"text": b, "x": 750, "y": 1500, "move": "down", "acc": True, "t": 1.6, "size": 72}]}]
    if sid == "S8":
        ws, k = SIFT[lang]
        return [{"type": "words", "mode": "sift", "box": [160, 940, 920, 1000], "target": [540, 1500], "seed": 9, "size": 54,
                 "keep": [k], "stagger": 0.02, "words": ws}]
    return None


MEG = dict(credit=AI_NEW)
# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1290, "fact", [E_BACK, E_DR], [obj("meg", f"{D}/megaphone", w=600, y=1290, anim="drop", vibrate=3, **MEG)], "S1",
     "قلاب: بلندگوی فلزی زیر نور با موج‌های صدا = چند صدای خیلی بلند؛ همان چیزی که «اینترنت» را می‌سازد"),
    ("S2", "paper", None, "fact", [E_BACK, E_AT], [obj("phone", "2026-10-25/phone", w=520, y=1300, rot=-8, anim="rise", vibrate=2)], None,
     "گوشیِ لرزان = کامنت‌ها و تیترهایی که یک‌شبه روی صفحه انباشته می‌شوند"),
    ("S3", "graphite", 1250, "fact", [E_BACK], None, "S3",
     "ابرِ شلوغِ واژه‌های انتقاد (لوس، مادی، بدترین…) که هم‌زمان چشمک می‌زنند = همه با یک صدا، و آن‌قدر بلند که بیشتر از آنچه هستند به نظر می‌رسند"),
    ("S4", "paper", None, "fact", [E_DR], [obj("lens", "2026-10-22/magnifier", w=560, y=1300, rot=-10, anim="slide_r")], None,
     "ذره‌بین = به‌جای خواندنِ هیاهو، از خودِ مردم پرسیدن و دقیق نگاه کردن؛ عدد ۶۸ درصد"),
    ("S5", "graphite", 1300, "interpretation", None, [obj("scale", "2026-10-22/scale", w=600, y=1130, anim="rise")], "S5",
     "چرخش (drop): ترازو؛ «صدای بلند» سبک است و بالا می‌رود، «۶۸٪» سنگین پایین می‌ماند = بلندی وزن ندارد، تعداد دارد"),
    ("S6", "paper", None, "interpretation", None, [obj("ear", f"{D}/ear_trumpet", w=720, y=1300, anim="slide_l", float=3, credit=AI_NEW)], None,
     "شیپورِ گوش = باید گوش را جلو برد تا ساکت‌ها را شنید؛ کسانی که خوششان آمده پست نمی‌گذارند"),
    ("S7", "graphite", 1300, "fact", [E_DR], [obj("watch", "2026-10-22/watch", w=440, y=1300, anim="fade", float=2)], None,
     "احتیاط یک بار: ساعت = داوریِ اصلی، یعنی فروش، هنوز نرسیده؛ این فقط یک نظرسنجی سریع است"),
    ("S8", "paper", None, "interpretation", None, [obj("sieve", "2026-10-22/sieve", w=680, y=1210, anim="rise")], "S8",
     "صافی: واژه‌های انتقاد می‌ریزند و فقط «حرفِ درست» می‌ماند = انتقاد را وزن کن، نه حجمش را؛ می‌تواند درست باشد و باز اقلیت"),
    ("S9", "graphite", 1300, "interpretation", None, [obj("roller", "2026-10-26/paint_roller", w=640, y=1300, rot=-12, anim="slide_r", path=[[0.4, 600, 1300], [2.6, 480, 1300]])], None,
     "غلتکِ رنگ که روی صحنه می‌کشد = وسوسه‌ی فردای طوفان: همه‌چیز را از نو رنگ کردن"),
    ("S10", "paper", None, "interpretation", None, [obj("eraser", "2026-10-22/eraser", w=440, y=1300, rot=8, anim="pop")], None,
     "پاک‌کن = پاک کردنِ منو، تابلو و بسته‌بندی؛ همان چیزی که داشت کار می‌کرد"),
    ("S11", "graphite", 1300, "interpretation", None, [obj("cup", "2026-10-29/cup", w=460, y=1300, anim="rise", float=2)], None,
     "فنجانِ همیشگی = مشتریِ ثابت که کامنت نمی‌گذارد و فقط دوباره سفارش می‌دهد"),
    ("S12", "paper", None, "interpretation", None, [obj("ticket", "2026-10-31/ticket", w=640, y=1300, rot=-4, anim="drop")], None,
     "تکه‌رسیدِ پاره = رأیِ واقعی: سفارشِ دوباره و فروشِ هفته، نه کامنت"),
    ("S13", "graphite", 1300, "interpretation", None, [obj("key", "2026-10-24/key", w=520, y=1300, rot=-20, anim="slide_l", float=2)], None,
     "کلید = فرمانِ برند؛ به منتقد جواب بده، ولی کلید را دستش نده"),
    ("S14", "paper", None, "interpretation", None, [obj("meg", f"{D}/megaphone", w=500, y=1270, rot=90, anim="fade", **MEG)], None,
     "بازگشت به آغاز: همان بلندگو، حالا بی‌صدا و رو به آسمان، بدون موج = بلندی اندازه‌ی صداست، نه اندازه‌ی جمعیت"),
    ("S15", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("اینترنت گفت شکست خورد.", "b"), ("مردم گفتند *دوستش* دارند.", "h")],
    "S2": [("تبلیغِ کریسمسِ جان لوئیس", "b"), ("این هفته زیرِ *رگبار* رفت.", "h")],
    "S3": [("ستون‌نویس‌ها، کامنت‌ها، تیترها:", "b"), ("همه *یک‌صدا*.", "h")],
    "S4": [("همان روزها کسی از خودِ مردم پرسید.", "b"), ("*۶۸ درصد* گفتند دوستش دارند.", "h")],
    "S5": [("صدای بلند", "b"), ("صدای *اکثریت* نیست.", "h")],
    "S6": [("آن‌هایی که خوششان آمد", "b"), ("*کامنت* نمی‌گذارند.", "h")],
    "S7": [("یک نظرسنجیِ سریع است؛ فروش هنوز نیامده.", "b"), ("ولی *نسبت* را ببینید.", "h")],
    "S8": [("انتقاد می‌تواند درست باشد", "b"), ("و باز هم *اقلیت* باشد.", "h")],
    "S9": [("خطر، فردای طوفان است:", "b"), ("همه‌چیز را *از نو* رنگ می‌کنید.", "h")],
    "S10": [("منو، تابلو، بسته‌بندی؛", "b"), ("همان که داشت *کار* می‌کرد.", "h")],
    "S11": [("مشتریِ همیشگی‌تان کامنت نمی‌گذارد.", "b"), ("فقط *دوباره* سفارش می‌دهد.", "h")],
    "S12": [("پیش از هر تغییر، از ده مشتری بپرسید", "b"), ("و *فروشِ* هفته را ببینید.", "h")],
    "S13": [("به منتقد مؤدبانه جواب بدهید.", "b"), ("ولی *کلید* را دستش ندهید.", "h")],
    "S14": [("بلندی، اندازه‌ی صداست؛", "b"), ("نه اندازه‌ی *جمعیت*.", "h")],
    "S15": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("The internet called it a flop.", "b"), ("People said they *liked* it.", "h")],
    "S2": [("John Lewis's Christmas ad", "b"), ("got *torn apart* this week.", "h")],
    "S3": [("Columnists. Comments. Headlines.", "b"), ("All one *voice*.", "h")],
    "S4": [("Meanwhile, someone asked people.", "b"), ("*68%* liked or loved it.", "h")],
    "S5": [("Loud", "b"), ("isn't *many*.", "h")],
    "S6": [("The people who liked it", "b"), ("don't *post* about it.", "h")],
    "S7": [("One quick poll. Sales aren't in yet.", "b"), ("But look at the *ratio*.", "h")],
    "S8": [("Criticism can be right", "b"), ("and still be the *minority*.", "h")],
    "S9": [("Then comes the morning after:", "b"), ("you *repaint* it all.", "h")],
    "S10": [("The menu. The sign. The pack.", "b"), ("The thing that was *working*.", "h")],
    "S11": [("Your regulars never comment.", "b"), ("They just order *again*.", "h")],
    "S12": [("Before you change a thing,", "b"), ("ask ten regulars. Check the *till*.", "h")],
    "S13": [("Answer the critic, politely.", "b"), ("Don't hand over the *keys*.", "h")],
    "S14": [("Loud is a volume,", "b"), ("not a *headcount*.", "h")],
    "S15": [("Write to me.", "b")],
}
VO = {"S4": "Meanwhile, someone asked people. Sixty-eight percent liked or loved it."}

SOURCES = [
    {"publisher": "DesignRush", "title": "John Lewis Ad Scores 5.6 Stars at System1, Lacks Punch for Kantar", "date": "2026-11-04", "url": DR},
    {"publisher": "Fashion Times", "title": "John Lewis's 2026 Christmas Ad Sparks Backlash Over 'Horrid Kids' and Materialistic Storyline", "date": "2026-11-05", "url": FT},
    {"publisher": "Advanced Television", "title": "John Lewis 2026 Xmas ad scores high with System1", "date": "2026-11-04", "url": AT},
    {"publisher": "Campaign Brief", "title": "John Lewis Christmas ad scores 5.6 Stars, its highest rating since 'Excitable Edgar' in 2019", "date": "2026-11-05", "url": CB},
    {"publisher": "The Drum (Andrew Tindall, System1)", "title": "They may be loud, but only 6% hated the John Lewis Christmas ad. It will work", "date": "2026-11-04", "url": TD},
]

CAP_FA = """اینترنت گفت تبلیغ شکست خورد. مردم گفتند دوستش دارند.

تبلیغ کریسمسِ امسالِ جان لوئیس («گلوریا و پیکلز») این هفته زیرِ رگبارِ انتقاد رفت: یک ستون‌نویس بچه‌های داستان را «لوس، طلبکار و بی‌ادب» خواند و خیلی‌ها در شبکه‌های اجتماعی گفتند قصه‌اش مادی و دور از زندگیِ مردم است.

همان روزها کسی از خودِ مردم پرسید. در نظرسنجیِ وان‌پالس، ۶۸ درصد گفتند تبلیغ را دوست دارند یا عاشقش‌اند. در آزمونِ شرکتِ System1 هم ۵٫۶ ستاره گرفت، بهترین امتیازِ جان لوئیس از ۲۰۱۹؛ و به گفته‌ی همین شرکت، فقط ۶ درصد واقعاً از آن بیزار بودند. صدای بلند، صدای اکثریت نیست. آن‌هایی که خوششان آمده معمولاً چیزی نمی‌نویسند.

حدودش را بگویم: این‌ها نظرسنجی و آزمونِ سریع‌اند، نه فروش؛ اندازه‌ی نمونه منتشر نشده، عددِ ۶ درصد را یکی از کارکنانِ خودِ System1 نوشته، و کانتار معتقد است تبلیغ «ضربه‌ی احساسیِ سال‌های قبل» را ندارد. فروشِ کریسمس هنوز نیامده. من درباره‌ی خوب یا بد بودنِ این تبلیغ حکم نمی‌دهم؛ حرفم درباره‌ی شمردنِ صداهاست. انتقاد می‌تواند درست باشد و باز هم اقلیت باشد.

برای صاحب کسب‌وکار: فردای یک موجِ عصبانی، منو و تابلو و بسته‌بندی را عوض نکنید. از ده مشتریِ همیشگی بپرسید، سفارش‌های دوباره و فروشِ هفته را ببینید. به منتقد مؤدبانه جواب بدهید، ولی بگذارید اکثریتِ ساکت رأی بدهد.

آخرین باری که چند صدای بلند شما را به تغییرِ چیزی واداشت، کِی بود، و بعدش فروش چه شد؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """The internet called it a flop. People said they liked it.

John Lewis's 2026 Christmas ad, "Gloria and Pickles", got torn apart this week. One columnist called the children "spoilt, entitled, rude"; plenty of people online called the story materialistic and out of touch.

Meanwhile, someone asked people. In a OnePulse poll, 68% said they liked or loved it. System1 gave it 5.6 Stars, John Lewis's best score since 2019, and System1's Andrew Tindall wrote in The Drum that only 6% felt real contempt. Loud isn't the same as many. The people who like something rarely post about it.

The limits: these are quick polls and ad tests, not sales. Sample sizes weren't published, the 6% figure comes from someone who works at System1, and Kantar's view is that the ad "lacks the emotive punch" of earlier years. Christmas sales aren't in yet. I'm not judging whether the ad is good; my point is about how we count voices. Criticism can be right and still be the minority.

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
        if sid == "S15": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        if lang == "en" and VOICE and sid in VO: s["vo"] = VO[sid]
        scenes.append(s)
    r = {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
         "topic": "صدای بلند، صدای اکثریت نیست: انتقادِ پرسروصدا را وزن کن، نه حجمش را" if lang == "fa" else "Loud isn't many: weigh the backlash, don't count its volume",
         "pillar": "brand_communication_consumer_behaviour", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#brandstrategy", "#consumerbehavior"] if lang == "fa" else ["#branding", "#marketing", "#brandstrategy", "#consumerbehavior"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}
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
