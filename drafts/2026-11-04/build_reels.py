"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-04 from one shared visual plan.
Topic: the logo that faces the room. The glowing Apple logo returns on the new MacBook Pro (28 Oct 2026);
on early PowerBooks/iBooks the logo faced the owner and read upside down to everyone else, until Apple flipped it."""
import json, pathlib

D = "2026-11-04"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-04T01:30:00Z"
MR1 = "https://macrumors.com/2026/10/28/illuminated-logo-returns-to-macbook-pro"
MR2 = "https://www.macrumors.com/2026/10/28/macbook-pro-glowing-apple-logo/"
ENG = "https://www.engadget.com/2012/05/21/the-story-of-apples-upside-down-logo/"
CNN = "https://edition.cnn.com/2012/05/22/tech/gaming-gadgets/apple-upside-down-logo"

E_MR = {"url": MR1, "publisher": "MacRumors", "event_date": "2026-10-28", "retrieved_at": RT,
        "claim": "New MacBook Pro (announced 28 Oct 2026) brings back the illuminated rear Apple logo, dropped in the 2016 MacBook Pro redesign. The article gives no reason from Apple."}
E_ENG = {"url": ENG, "publisher": "Engadget (citing former Apple employee Joe Moreno)", "event_date": "2012-05-21", "retrieved_at": RT,
         "claim": "On PowerBooks and iBooks the logo first faced the user and read upside down to onlookers when the lid was open; the decision was later reversed."}
E_CNN = {"url": CNN, "publisher": "CNN (citing Joe Moreno)", "event_date": "2012-05-22", "retrieved_at": RT,
         "claim": "'Opening a laptop from the wrong end is a self-correcting problem that only lasts for a few seconds. However, viewing the upside logo is a problem that lasts indefinitely.' Reversed within a few years."}

CR_A = "Image: glowing logo on the new MacBook Pro (owner upload; requested from MacRumors' report, original source not confirmed)"
CR_B = "Image: iBook, clamshell era (owner upload; source not stated)"
CR_C = "Image: TV still cropped to a PowerBook lid, logo upside down to the camera (owner upload; source not stated)"


def obj(key, path, x=540, y=1300, w=420, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1290, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "credit": credit, "source_url": url}
    o.update(kw); return o


WORDS = {"fa": ["لیوان", "کیسه", "جعبه", "رسید", "تابلو", "برچسب"],
         "en": ["cup", "bag", "box", "receipt", "sign", "sticker"]}


def fx_for(sid, lang):
    if sid == "S11":
        return [{"type": "words", "mode": "pop", "box": [150, 1000, 930, 1480], "seed": 397, "size": 72, "words": WORDS[lang]}]
    if sid == "S7":
        return [{"type": "rings", "x": 540, "y": 1180, "n": 5, "R": 380, "period": 1.6, "t": 1.2, "op": .35}]
    return None


LAP = dict(w=640, y=1310)
# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1290, "fact", [E_MR], [frame("ta", "T-a.png", 1.778, CR_A, MR1, w=900, y=1290)], None,
     "قلاب: عکس واقعی لوگوی روشن روی درِ لپ‌تاپ در تاریکی (آپلود مالک، قاب‌دار) = همان نشانی که خریدار نمی‌بیند"),
    ("S2", "paper", None, "interpretation", None, [obj("lap", f"{D}/laptop_back", credit=AI_NEW, anim="rise", float=3, **LAP)], None,
     "لپ‌تاپ از پشت، درِ ساده بی‌نشان، رو به ما = ما جای «اتاق» نشسته‌ایم؛ لوگو رو به ماست، نه رو به صاحبش"),
    ("S3", "graphite", 1290, "fact", [E_ENG], [frame("tb", "T-b.png", 1.005, CR_B, "owner upload (source not stated)", w=460, y=1290, anim="drop", push=0.03)], None,
     "عکس واقعی آی‌بوک قدیمی (آپلود مالک، کوچک و قاب‌دار، بدون بزرگ‌نمایی) = دورانِ پاوربوک و آی‌بوک"),
    ("S4", "paper", None, "fact", [E_ENG], [obj("lap", f"{D}/laptop_back", credit=AI_NEW, anim="fade", tilt=180, tilt_t=1.4, **LAP)], None,
     "همان لپ‌تاپ وسط صحنه ۱۸۰ درجه می‌چرخد = برای صاحبش درست، برای بقیه وارونه"),
    ("S5", "graphite", 1290, "fact", [E_ENG, E_CNN], [frame("tc", "T-c_lid.png", 1.407, CR_C, "owner upload (source not stated)", w=720, y=1290, anim="drop", push=0.05)], None,
     "چرخش (drop): برش واقعی از درِ پاوربوک که لوگویش رو به دوربین وارونه است (چهره و دست بیرون از قاب) = سند همان وارونگی، پیش از برعکس شدن"),
    ("S6", "paper", None, "fact", [E_CNN], [obj("watch", "2026-10-22/watch", w=380, y=1300, anim="drop", float=2)], None,
     "ساعت = چند ثانیه در برابر همیشه؛ استدلالِ کارمند سابق اپل درباره‌ی زمان"),
    ("S7", "graphite", 1180, "fact", [E_MR], [obj("bulb", f"{D}/bulb", credit=AI_NEW, w=270, y=1280, anim="rise", bright=[0.55, 1.35])], "S7",
     "لامپی که آرام روشن می‌شود و حلقه‌های نور = بعد از حدود ده سال خاموشی، نشان دوباره روشن شد"),
    ("S8", "paper", None, "interpretation", None, [obj("plate", "2026-10-31/nameplate", w=600, y=1300, anim="slide_r", float=2)], None,
     "پلاک رو به بیرون = نشانی که برای بیننده‌ها نوشته شده، نه برای کسی که پشتش نشسته"),
    ("S9", "graphite", 1300, "interpretation", [E_MR], [obj("lens", "2026-10-22/magnifier", w=540, y=1300, rot=-10, anim="slide_r", bright=[1.3, 1.3])], None,
     "ذره‌بین = «خوانش من»؛ اپل دلیل نگفته، این برداشت است و یک بار روی صفحه می‌آید"),
    ("S10", "paper", None, "interpretation", None, [obj("cup", "2026-10-29/cup", w=430, y=1310, anim="slide_l", float=2)], None,
     "لیوان کافه که از کنار وارد می‌شود = نشانِ کافه در دست مشتری از جلوی رهگذرها می‌گذرد"),
    ("S11", "graphite", 1260, "interpretation", None, None, "S11",
     "ابرِ نام سطح‌هایی که نشان روی‌شان سفر می‌کند (کیسه، جعبه، رسید...) با تپش = ویترینِ سیار، شلوغ و در حرکت"),
    ("S12", "paper", None, "interpretation", None, [obj("phone", "2026-10-25/phone", w=560, y=1300, rot=-6, anim="rise")], "S12",
     "گوشی = عکس؛ نشان در قابِ دوربینِ دیگران هم باید درست خوانده شود"),
    ("S13", "graphite", 1290, "interpretation", None, [frame("ta", "T-a.png", 1.778, CR_A, MR1, w=900, y=1290, anim="fade", push=0.06)], None,
     "بازگشت به آغاز: همان لوگوی روشن = نشانت را برای کسی بساز که هنوز نخریده"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("کسی که پولِ این لوگو را داده،", "b"), ("تنها کسی است که *نمی‌بیندش*.", "h")],
    "S2": [("لپ‌تاپ را باز کن.", "b"), ("لوگو رو به *اتاق* است.", "h")],
    "S3": [("در دورانِ پاوربوک و آی‌بوک،", "b"), ("لوگو رو به *صاحبش* بود.", "h")],
    "S4": [("درِ بسته: برای او درست.", "b"), ("درِ باز: برای بقیه *وارونه*.", "h")],
    "S5": [("به روایتِ یک کارمند سابق اپل،", "b"), ("چند سال بعد *برعکسش* کردند.", "h")],
    "S6": [("اشتباه باز کردن، چند ثانیه است.", "b"), ("لوگوی وارونه *تمامی ندارد*.", "h")],
    "S7": [("سالِ ۲۰۱۶ نورش خاموش شد.", "b"), ("مک‌بوک پروی تازه *دوباره روشنش* کرد.", "h")],
    "S8": [("خریدار پشتِ صفحه نشسته.", "b"), ("اتاق *تمام روز* نگاهش می‌کند.", "h")],
    "S9": [("اپل دلیلش را نگفته. خوانش من:", "b"), ("نشانِ برند مالِ *تماشاگر* است.", "h")],
    "S10": [("لیوانِ کافه‌ات در خیابان راه می‌رود،", "b"), ("جلوی چشمِ *رهگذرها*.", "h")],
    "S11": [("کیسه، جعبه، رسید:", "b"), ("ویترینِ *سیار* تو هستند.", "h")],
    "S12": [("در عکس‌هایشان هم", "b"), ("نشانت باید *درست* خوانده شود.", "h")],
    "S13": [("پس نشانت را طراحی کن", "b"), ("برای کسی که *هنوز نخریده*.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Whoever paid for this logo", "b"), ("never *sees* it.", "h")],
    "S2": [("Open the laptop.", "b"), ("The logo faces the *room*.", "h")],
    "S3": [("On old PowerBooks and iBooks,", "b"), ("it faced the *owner*.", "h")],
    "S4": [("Right way up when shut.", "b"), ("*Upside down* to everyone else.", "h")],
    "S5": [("A former Apple employee recalls", "b"), ("they *flipped* it.", "h")],
    "S6": [("The wrong end costs seconds.", "b"), ("An upside-down logo *never stops*.", "h")],
    "S7": [("The glow went dark in 2016.", "b"), ("The new MacBook Pro *relights* it.", "h")],
    "S8": [("The buyer faces the screen.", "b"), ("The room stares *all day*.", "h")],
    "S9": [("Apple hasn't said why. My reading:", "b"), ("logos are for *onlookers*.", "h")],
    "S10": [("Your café cup walks the street,", "b"), ("seen by *strangers*.", "h")],
    "S11": [("Bag, box, receipt:", "b"), ("a *travelling* shop window.", "h")],
    "S12": [("In their photos too,", "b"), ("it must read *right way up*.", "h")],
    "S13": [("So design your mark", "b"), ("for whoever *hasn't bought yet*.", "h")],
    "S14": [("Write to me.", "b")],
}
# spoken versions where the screen line reads awkwardly aloud
VO = {"S7": "The glow went dark in twenty sixteen. The new MacBook Pro relights it.", "S5": "A former Apple employee recalls that they flipped it, a few years later."}

SOURCES = [
    {"publisher": "MacRumors", "title": "Illuminated Apple Logo Returns to MacBook Pro After 10 Years", "date": "2026-10-28", "url": MR1},
    {"publisher": "MacRumors", "title": "Here's a Real-World Look at the New MacBook Pro's Glowing Apple Logo", "date": "2026-10-28", "url": MR2},
    {"publisher": "Engadget", "title": "The story of Apple's upside down logo", "date": "2012-05-21", "url": ENG},
    {"publisher": "CNN (via Wired)", "title": "Why Apple's logo was once upside down", "date": "2012-05-22", "url": CNN},
]

CAP_FA = """کسی که پولِ این لوگو را داده، تنها کسی است که نمی‌بیندش.

۲۸ اکتبر، با مک‌بوک پروی تازه، لوگوی روشنِ پشتِ درِ لپ‌تاپ برگشت؛ نوری که با بازطراحی مک‌بوک پروی ۲۰۱۶ خاموش شده بود (گزارشِ مک‌رومرز و دیگر سایت‌های خبری اپل). صاحبِ لپ‌تاپ تقریباً هیچ‌وقت آن لوگو را نمی‌بیند. اتاق همیشه می‌بیند.

ماجرای قدیمی‌ترش جالب‌تر است. به روایتِ جو مورنو، کارمند سابق اپل، روی پاوربوک‌ها و آی‌بوک‌ها لوگو اول رو به صاحبش بود: با درِ بسته برای او درست، و با درِ باز برای همه‌ی اطرافیان وارونه. چون آدم‌ها لپ‌تاپ را از طرفِ اشتباه باز می‌کردند. چند سال بعد برعکسش کردند. استدلالش این بود: اشتباه باز کردن چند ثانیه طول می‌کشد و خودش درست می‌شود؛ لوگوی وارونه پیشِ چشمِ دیگران تمامی ندارد.

حدودش را بگویم: اپل نه دلیل حذفِ نور را گفته، نه دلیل برگشتنش را؛ این‌که «نشان مالِ تماشاگر است» خوانش من است. ماجرای وارونگی هم روایتِ یک نفر است که سال ۲۰۱۲ در انگجت و سی‌ان‌ان بازگو شد. عکس‌ها آپلود مالک‌اند (منبعِ دقیقشان تأیید نشده)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

برای صاحب کسب‌وکار: لیوان، کیسه، جعبه و رسیدِ شما بیشتر از آن‌که دیده‌ی خریدار باشند، دیده‌ی خیابان‌اند. نشانت را طوری بگذار که از بیرون، از دور و در عکسِ دیگران درست خوانده شود. برای کسی که هنوز نخریده.

نشانِ کسب‌وکارِ شما الان رو به کیست؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """The person who paid for this logo is the one who never sees it.

On 28 October the new MacBook Pro brought back the glowing logo on the back of the lid, switched off since the 2016 MacBook Pro redesign (reported by MacRumors and other Apple news sites). The owner almost never sees it. The room always does.

The older story is better. As former Apple employee Joe Moreno told it, on PowerBooks and iBooks the logo first faced the owner: right way up with the lid shut, upside down to everyone else once it was open, because people kept opening the laptop from the wrong end. A few years later Apple flipped it. His logic: opening the wrong end is a few seconds of fumbling that fixes itself; an upside-down logo in front of everyone else never stops.

The limits: Apple hasn't said why the glow went away or why it's back, so "a logo is for the onlooker" is my reading, not Apple's. The upside-down story is one person's account, retold by Engadget and CNN in 2012. The photos are owner uploads (exact sources not confirmed); the other objects are AI-generated.

For owners: your cup, bag, box and receipt are seen by the street far more than by the buyer. Make your mark read from the outside, from a distance, in other people's photos. Design it for the one who hasn't bought yet.

Which way is your mark facing right now? Write to me.

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
        if sid == "S14": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        if lang == "en" and VOICE and sid in VO: s["vo"] = VO[sid]
        scenes.append(s)
    r = {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
         "topic": "لوگویی که رو به جمع است: نشان برند بیشتر برای اطرافیانِ مشتری است تا خودِ او" if lang == "fa" else "The logo that faces the room: your mark works hardest for the people around your customer",
         "pillar": "identity_visibility_consumer_behaviour", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#logodesign", "#طراحی_لوگو"] if lang == "fa" else ["#branding", "#marketing", "#logodesign", "#brandidentity"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}
    if lang == "en" and VOICE:
        r["voice"] = {"enabled": True, "voice": "en-US-AndrewNeural", "rate": "-6%", "pitch": "-3%"}
    return r


import os
VOICE = bool(os.environ.get("AZURE_SPEECH_KEY") and os.environ.get("AZURE_SPEECH_REGION"))

if __name__ == "__main__":
    for n, lang in ((1, "fa"), (2, "en")):
        (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
    for L, C in (("fa", FA), ("en", EN)):
        print(L, sum(len(t.replace("*", "").split()) for v in C.values() for t, _ in v))
    print("voice", VOICE)
