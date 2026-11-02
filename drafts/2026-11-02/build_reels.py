"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-02 from one shared visual plan.
Owner directive (2026-11-01 evening): owner images T-a..T-d + meaning-carrying vectors; no new AI objects."""
import json, pathlib

D = "2026-11-02"
HERE = pathlib.Path(__file__).parent
AI = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-02T03:30:00Z"
MR21 = "https://macrumors.com/2026/10/21/apple-music-new-look-announced/"
MR13 = "https://www.macrumors.com/2026/10/13/ios-27-2-apple-music-icon/"
CB = "https://www.creativebloq.com/news/apple-musics-miserable-new-logo-is-giving-mixed-messages"
FC = "https://www.fastcompany.com/91627164/for-the-new-apple-music-logo-designers-lean-into-the-science-of-sound"
WP = "https://www.wallpaper.com/art/music/apple-musics-new-visual-identity-turns-sound-into-liquid-with-help-from-fred-again"
BT = "https://www.bandt.com.au/apple-music-gets-watery-rebrand-via-tbwamedia-arts-lab/"
N95 = "https://9to5mac.com/2026/10/27/ios-27-2-adds-new-app-icon-for-apple-music-more-design-updates/"

EV_MR = [{"url": MR21, "publisher": "MacRumors", "event_date": "2026-10-21", "retrieved_at": RT,
          "claim": "Apple Music visuals now have a black-and-white color scheme instead of red; visuals 'made by sound' with Fred Again and NEST Acoustics; rolls out with iOS 27.2"},
         {"url": MR13, "publisher": "MacRumors", "event_date": "2026-10-13", "retrieved_at": RT,
          "claim": "iOS 27.2 icon: black on white in light mode, white on black in dark mode; widgets black instead of red; tab highlight blue instead of red"}]
EV_CB = [{"url": CB, "publisher": "Creative Bloq", "event_date": "2026-10-16", "retrieved_at": RT,
          "claim": "X user: 'The new Apple Music branding is miserable how do you sap a thing of all of its colour like this and think it's okay?'"}]
EV_SOUND = [{"url": WP, "publisher": "Wallpaper*", "event_date": "2026-10-21", "retrieved_at": RT,
             "claim": "Music played through a transducer into a shallow bath of mineral oil; vibrations filmed"},
            {"url": FC, "publisher": "Fast Company", "event_date": "2026-10-21", "retrieved_at": "2026-11-01T16:50Z",
             "claim": "Each note produces a brief burst of saturated colour (stage-1 reading; page not re-fetchable this morning)"}]

CR_C = "Image: Apple, before/after comparison (owner upload)"
CR_A = "Image: 9to5Mac, new Apple Music icon (owner upload, cropped)"
CR_B = "Image: Apple 'made by sound' frame, via Fast Company (owner upload)"
CR_D = "Image: Apple 'made by sound' film frame (owner upload)"


def obj(key, path, x=540, y=1290, w=420, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": AI}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1270, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "color": [0, 0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


WORDS = {
    "S4": {"fa": (["قرمز", "گرم", "آشنا", "پرانرژی", "شاد", "غم‌انگیز"], ["غم‌انگیز"]),
           "en": (["red", "warm", "familiar", "loud", "bright", "miserable"], ["miserable"]), "mode": "fade", "seed": 9},
    "S9": {"fa": (["رنگ", "لوگو", "شعار", "بلندتر", "مرا ببین", "تخفیف", "رنگ", "لوگو", "بلندتر"], []),
           "en": (["colour", "logo", "slogan", "louder", "look at me", "sale", "colour", "logo", "louder"], []), "mode": "pop", "seed": 4},
}


def words(sid, lang):
    w, k = WORDS[sid][lang]
    f = {"type": "words", "mode": WORDS[sid]["mode"], "box": [150, 1020, 930, 1450], "seed": WORDS[sid]["seed"], "size": 64 if sid == "S9" else 58, "t0": 0.9,
         "words": w, "keep": k}
    if len(k) == 1: f["keep_at"] = [540, 1240]
    return [f]


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1270, "fact", EV_MR, [frame("tc", "T-c.png", 1.778, CR_C, CB, w=900)], None,
     "قلاب با تصویر واقعی قبل/بعد (آپلود مالک، قاب‌دار، رنگ طبیعی): قرمزِ بیش از یک دهه کنار نسخه‌ی بی‌رنگ = «پس داد»"),
    ("S2", "paper", None, "fact", EV_MR, None, [{"type": "swatch", "y": 1260, "t": 1.3}],
     "کارت قرمز بیرون می‌رود و کارت‌های سیاه و سفید جایش می‌نشینند = خودِ تغییر رنگ، بی‌آن‌که لوگو را بازکشی کنیم"),
    ("S3", "graphite", 1270, "fact", EV_MR, [frame("ta", "T-a_icon.png", 1.0, CR_A, N95, w=560, y=1270, anim="rise")], None,
     "آیکون واقعی جدید (آپلود مالک، بریده روی آیکون): نُت همان نُت است، فقط رنگ رفته = شکل ماند"),
    ("S4", "paper", None, "fact", EV_CB, None, "S4",
     "کلمه‌های حسِ قرمز (گرم، آشنا، شاد) محو می‌شوند و فقط «غم‌انگیز» می‌ماند = واکنش بعضی طرفدارها"),
    ("S5", "graphite", 1270, "interpretation", EV_SOUND, [frame("tb", "T-b_crop.png", 1.0, CR_B, FC, w=580, y=1270, anim="zoom", push=0.06)], None,
     "چرخش (drop): قاب واقعی «ساخته‌شده با صدا» که لبه‌هایش رنگی شده = رنگ رفت توی موسیقی"),
    ("S6", "paper", None, "fact", EV_SOUND, None, [{"type": "rings", "x": 540, "y": 1250, "R": 400, "n": 6, "period": 1.3, "t": 0.5, "op": 0.85, "sw": 5}],
     "موج‌های هم‌مرکز از یک نقطه = نُتی که روغن را می‌لرزاند؛ رنگ فقط با موج می‌آید"),
    ("S7", "graphite", 1290, "interpretation", None, [obj("lens", "2026-10-22/magnifier", y=1290, w=560, rot=-10, anim="slide_r", bright=[1.3, 1.3])], None,
     "ذره‌بین = «خوانش من»؛ اپل دلیلی نگفته، این نگاه دقیق‌تر من است، نه ادعای استراتژی اپل (احتیاط یک بار)"),
    ("S8", "paper", None, "interpretation", None, None, [{"type": "frameline", "box": [250, 1030, 830, 1480], "t": 0.5, "wash_op": 0.5}],
     "قاب خالی که خودش را می‌کشد و داخلش رنگ می‌نشیند = برند قاب است، رنگ مال اثر"),
    ("S9", "graphite", 1240, "interpretation", None, None, "S9",
     "کلمه‌های بلند تبلیغ (لوگو، شعار، بلندتر، مرا ببین) شلوغ و چشمک‌زن = قابی که داد می‌زند و جای نقاشی را می‌گیرد"),
    ("S10", "paper", None, "interpretation", None, [obj("label", "2026-10-25/label_card", y=1280, w=520, rot=-4, anim="drop", float=3)], None,
     "کارت برچسب دیوار گالری = کار میزبان معرفی است، کوچک و ثابت کنار اثر"),
    ("S11", "graphite", 1290, "interpretation", None, [obj("roller", "2026-10-26/paint_roller", y=1290, w=620, rot=8, anim="slide_l", bright=[1.35, 1.35])], None,
     "غلتک رنگ = «رنگت را رنگ نکن/دور نریز»؛ پیش از رنگ‌زدن روی دارایی‌ات بپرس ستاره کیست (رد تیم)"),
    ("S12", "paper", None, "interpretation", None, [obj("stamp", "2026-10-29/stamp", y=1290, w=300, anim="drop", float=2)], None,
     "مهر = شکلی که مردم می‌شناسند، امضای ثابت تو؛ همان را نگه دار"),
    ("S13", "graphite", 1290, "interpretation", None, [frame("td", "T-d_crop.png", 2.897, CR_D, MR21, w=940, y=1290, anim="zoom")], None,
     "بازگشت به آغاز: قرمز S1 حالا رنگ موج‌های صداست کنار wordmark بی‌رنگ = قاب ساکت، اثر رنگی"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("بعد از بیش از ده سال،", "b"), ("قرمزش را *پس داد*.", "h")],
    "S2": [("اپل موزیک آیکون و لوگویش را", "b"), ("*سیاه‌وسفید* کرد.", "h")],
    "S3": [("نُت همان نُت ماند.", "b"), ("فقط *رنگ* رفت.", "h")],
    "S4": [("بعضی طرفدارها نوشتند:", "b"), ("«*غم‌انگیز* است.»", "h")],
    "S5": [("رنگ کجا رفت؟", "b"), ("توی *موسیقی*.", "h")],
    "S6": [("در فیلم معرفی، صدا لوگو را ساخت.", "b"), ("رنگ با *نُت‌ها* می‌آید.", "h")],
    "S7": [("اپل دلیلی نگفته.", "b"), ("این *خوانش* من است:", "h")],
    "S8": [("وقتی کالایت کارِ دیگران است،", "b"), ("برندت *قاب* است، نه نقاشی.", "h")],
    "S9": [("قابی که داد می‌زند،", "b"), ("نقاشی را *می‌دزدد*.", "h")],
    "S10": [("گالری، کافه، فروشگاه چندبرندی:", "b"), ("مردم برای *اثر* می‌آیند.", "h")],
    "S11": [("نمی‌گویم رنگت را دور بریز.", "b"), ("اول بپرس: *ستاره* کیست؟", "h")],
    "S12": [("شکلی را که می‌شناسند نگه دار.", "b"), ("این *امضای* توست.", "h")],
    "S13": [("قاب، آرام.", "b"), ("رنگ، مالِ *اثر*.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("More than a decade of red.", "b"), ("Then they *gave it back*.", "h")],
    "S2": [("Apple Music's icon and logo", "b"), ("went *black and white*.", "h")],
    "S3": [("The note is the same note.", "b"), ("Only the *colour* left.", "h")],
    "S4": [("Some fans called it", "b"), ("“*miserable*.”", "h")],
    "S5": [("So where did the colour go?", "b"), ("Into the *music*.", "h")],
    "S6": [("Sound shaped the new logo.", "b"), ("Colour comes with the *notes*.", "h")],
    "S7": [("Apple gave no reason.", "b"), ("This is my *reading*:", "h")],
    "S8": [("Selling other people's work?", "b"), ("you're the *frame*, not the painting.", "h")],
    "S9": [("A frame that shouts", "b"), ("*steals* the painting.", "h")],
    "S10": [("Galleries. Cafés. Concept stores.", "b"), ("People come for the *work*.", "h")],
    "S11": [("I'm not saying drop your colour.", "b"), ("First ask: who's the *star*?", "h")],
    "S12": [("Keep the shape people know.", "b"), ("That's your *signature*.", "h")],
    "S13": [("A quiet frame.", "b"), ("The colour goes to the *work*.", "h")],
    "S14": [("Write to me.", "b")],
}

SOURCES = [
    {"publisher": "MacRumors", "title": "Apple Music's New Look Officially Announced", "date": "2026-10-21", "url": MR21},
    {"publisher": "MacRumors", "title": "iOS 27.2 Adds New Apple Music Icon", "date": "2026-10-13", "url": MR13},
    {"publisher": "Creative Bloq", "title": "Apple Music's 'miserable' new logo is giving mixed messages", "date": "2026-10-16", "url": CB},
    {"publisher": "Wallpaper*", "title": "Apple Music's new visual identity ripples into view – with help from Fred Again..", "date": "2026-10-21", "url": WP},
    {"publisher": "Fast Company", "title": "For the new Apple Music logo, designers lean into the science of sound", "date": "2026-10-21", "url": FC},
    {"publisher": "B&T", "title": "Apple Music Gets Watery Rebrand Via TBWA\\Media Arts Lab", "date": "2026-10-22", "url": BT},
    {"publisher": "9to5Mac", "title": "iOS 27.2 adds new app icon for Apple Music, more design updates (image T-a)", "date": "2026-10-27", "url": N95},
]

CAP_FA = """بعد از بیش از ده سال، قرمزش را پس داد.

اپل موزیک با iOS 27.2 آیکون و لوگویش را سیاه‌وسفید کرد. شکل نُت همان است؛ فقط رنگ رفته. ویجت‌ها هم از قرمز به سیاه رفتند. بعضی طرفدارها در شبکه‌های اجتماعی نوشتند این برند «غم‌انگیز» شده است.

رنگ کجا رفت؟ در هویت تازه، لوگو را صدا شکل داده: Fred again.. و NEST Acoustics نُت‌ها را با یک مبدل صوتی در حوضچه‌ی کم‌عمقی از روغن معدنی پخش کردند و لرزش‌ها را جلوی دوربین فیلم گرفتند (آژانس: TBWA\\Media Arts Lab). در قاب‌های این فیلم، رنگ با نُت‌ها می‌آید.

خوانش من این است: وقتی چیزی که می‌فروشید کار دیگران است (گالری، کافه‌ای که قهوه‌ی برشته‌کارهای دیگر را دم می‌کند، فروشگاه چندبرندی، پلتفرم فروش)، برند شما قاب است، نه نقاشی. قابی که داد می‌زند، نقاشی را می‌دزدد. مردم برای اثر می‌آیند؛ قاب باید ثابت، آشنا و آرام باشد.

حدودش را هم بگویم: اپل دلیلی برای حذف قرمز نگفته و این فقط یک خوانش است. کنار گذاشتن یک دارایی متمایز ریسک دارد و غولی مثل اپل از پسش برمی‌آید؛ درس این نیست که رنگتان را دور بریزید. درس این است که اول بپرسید ستاره کیست، و شکلی را که مردم می‌شناسند نگه دارید. منبع‌ها: MacRumors، Creative Bloq، Wallpaper*، Fast Company، B&T و 9to5Mac. چهار قاب واقعی آپلود مالک است (تصاویر Apple و 9to5Mac)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

در کسب‌وکار شما، مشتری برای چه چیزی می‌آید: برای قاب، یا برای اثری که در قاب است؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """More than a decade of red. Then they gave it back.

With iOS 27.2, Apple Music's icon and logo went black and white. The note is the same shape; only the colour left. Widgets went from red to black. Some fans online called the new branding "miserable."

So where did the colour go? The new identity was shaped by sound: Fred again.. and NEST Acoustics played notes through a transducer into a shallow bath of mineral oil and filmed the vibrations in camera (agency: TBWA\\Media Arts Lab). In those frames, the colour arrives with the notes.

My reading: when what you sell is other people's work (a gallery, a café pouring other roasters' coffee, a multi-brand store, a marketplace), your brand is the frame, not the painting. A frame that shouts steals the painting. People come for the work; the frame should be consistent, recognisable and quiet.

The limits: Apple gave no reason for dropping red, so this is one reading, not Apple's strategy. Dropping a distinctive asset is risky, and a giant can afford it. The lesson isn't "drop your colour." It's "decide who the star is, and keep the shape people know." Sources: MacRumors, Creative Bloq, Wallpaper*, Fast Company, B&T, 9to5Mac. The four real frames are owner uploads (images by Apple and 9to5Mac); the other objects are AI-generated.

What do your customers come for: the frame, or the work inside it? Write to me.

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
        if fx: s["fx"] = words(fx, lang) if isinstance(fx, str) else json.loads(json.dumps(fx))
        s["motion_rationale"] = why
        if sid == "S14": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        scenes.append(s)
    return {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
            "topic": "برند تو قاب است، نه نقاشی: اپل موزیک رنگش را به موسیقی داد" if lang == "fa" else "Your brand is the frame, not the painting: Apple Music gave its colour to the music",
            "pillar": "visual_identity_distinctive_assets", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
            "caption": CAP_FA if lang == "fa" else CAP_EN,
            "hashtags": ["#برندینگ", "#branding", "#brandidentity", "#visualidentity"] if lang == "fa" else ["#branding", "#marketing", "#brandidentity", "#visualidentity"],
            "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
            "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}


for n, lang in ((1, "fa"), (2, "en")):
    (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
print("ok")
