"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-10-31 from one shared visual plan."""
import json, pathlib

D = "2026-10-31"
HERE = pathlib.Path(__file__).parent
AI = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-10-31T01:40:00Z"
TC1 = "https://techcrunch.com/2026/10/02/paramount-and-warner-bros-discovery-to-become-skydance/"
TC2 = "https://techcrunch.com/2026/10/06/paramount-closes-historic-warner-bros-merger-to-form-skydance/"
DN = "https://www.deseret.com/entertainment/2026/10/02/paramount-and-warner-bros-merger-gets-new-name/"
CB = "https://creativebloq.com/entertainment/warner-bros-and-paramounts-skydance-rebrand-isnt-going-down-well"
DC = "https://designcompass.org/en/2026/10/07/skydance-paramount-warner-bros-brand-identity/"

EV_NAME = [{"url": TC1, "publisher": "TechCrunch", "event_date": "2026-10-02", "retrieved_at": RT,
            "claim": "Paramount and Warner Bros. Discovery to operate as Skydance, the name of David Ellison's original production company; Ellison: 'We never wanted a new corporate identity to diminish, alter or overshadow either one'; both studios 'remain in the spotlight'"},
           {"url": TC2, "publisher": "TechCrunch", "event_date": "2026-10-06", "retrieved_at": RT,
            "claim": "Merger completed Oct 6, 2026 (~$110bn); company named Skydance, ticker SKYD; includes Paramount+, HBO Max, CBS, CNN, MTV and more"}]
EV_KEEP = [{"url": DN, "publisher": "Deseret News", "event_date": "2026-10-02", "retrieved_at": RT,
            "claim": "Ellison: 'we wanted to preserve what has made each of these studios iconic'; studios sit under one corporate umbrella"}] + EV_NAME[:1]

CRED_A = "Image: Skydance launch video still (via Creative Bloq)"
CRED_B = "Image: Skydance identity (via Design Compass)"


def obj(key, path, x=540, y=1290, w=420, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": AI}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1280, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "color": [0, 0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


def words(lang):
    if lang == "fa":
        return [{"type": "words", "mode": "fade", "box": [140, 1000, 940, 1460], "seed": 7, "size": 58, "t0": 0.9, "keep_at": [540, 1240],
                 "words": ["سهام", "ادغام", "نماد بورس", "هیئت‌مدیره", "بانک", "فیلم"], "keep": ["فیلم"]}]
    return [{"type": "words", "mode": "fade", "box": [140, 1000, 940, 1460], "seed": 7, "size": 58, "t0": 0.9, "keep_at": [540, 1240],
             "words": ["shares", "merger", "ticker", "board", "bank", "the film"], "keep": ["the film"]}]


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1260, "fact", EV_NAME, [frame("tb", "T-b_crop.png", 1.88, CRED_B, DC, y=1345, w=760)], None,
     "قلاب با تصویر واقعی (آپلود مالک، قاب‌دار): نام تازه بالای دو نام افسانه‌ای = دو اسم یکی شدند و اسم تازه هیچ‌کدامشان نیست"),
    ("S2", "paper", None, "fact", EV_NAME, [obj("plate", f"{D}/nameplate", y=1290, w=600, anim="drop")], None,
     "پلاک برنجی سردر = اسمی برای ساختمان؛ اسمی که روی در دفتر است، نه روی پرده"),
    ("S3", "graphite", 1280, "fact", EV_KEEP, [frame("ta", "T-a.png", 1.209, CRED_A, CB, y=1280, w=660)], None,
     "منظومه‌ی نام‌ها (آپلود مالک): ده‌ها نام آشنا زیر نام تازه سر جایشان‌اند = نام‌های مشتری‌پسند زیر نور می‌مانند"),
    ("S4", "paper", None, "interpretation", None, [obj("ticket", f"{D}/ticket", y=1300, w=560, rot=-5, anim="pop", float=5)], None,
     "ته‌بلیت سینما = مردم بلیت فیلم می‌خرند، نه بلیت شرکت؛ پاره‌ی بلیت یعنی تجربه‌ی واقعی تماشاگر"),
    ("S5", "graphite", 1240, "interpretation", None, None, "WORDS",
     "کلمه‌های شرکتی (سهام، ادغام، نماد بورس، هیئت‌مدیره، بانک) محو می‌شوند و فقط «فیلم» می‌ماند و بزرگ می‌شود = مشتری فقط فیلم را می‌بیند"),
    ("S6", "paper", None, "interpretation", None, [obj("stamp", "2026-10-29/stamp", y=1300, w=330, anim="drop", vibrate=4)], None,
     "مهر لاستیکی اداری = قرارداد، بانک، کاغذبازی؛ دنیای مخاطبانِ اسم بالای سر"),
    ("S7", "graphite", 1290, "interpretation", None, [obj("key", "2026-10-24/key", y=1320, w=420, rot=-10, anim="rise", bright=[1.4, 1.4])], None,
     "چرخش ایده: کلید = برندها درها را باز می‌کنند؛ شرکت مادر فقط دسته‌کلید را نگه می‌دارد"),
    ("S8", "paper", None, "interpretation", None, [obj("trophy", "2026-10-24/trophy", y=1300, w=380, anim="rise")], None,
     "جام = وسوسه‌ی برنده‌بودن؛ اسم خودت بالای همه، مثل اسم قهرمان روی جام"),
    ("S9", "graphite", 1290, "interpretation", None, [obj("lens", "2026-10-22/magnifier", y=1330, w=430, rot=-6, anim="pop", float=5, bright=[1.4, 1.4])], None,
     "ذره‌بین = هنوز زود است برای قضاوت؛ با دقت نگاه کن، ولی قاعده روشن است؛ احتیاط یک بار و کوتاه"),
    ("S10", "paper", None, "interpretation", None, [obj("label", "2026-10-25/label_card", y=1310, w=460, rot=4, anim="slide_r")], None,
     "برچسب = برای هر اسم بنویس چه کسی آن را می‌خواند؛ برچسب‌زدن مخاطب"),
    ("S11", "graphite", 1290, "interpretation", None, [obj("sign", "2026-10-22/signpost", y=1300, w=440, anim="rise", bright=[1.4, 1.4])], None,
     "تابلوی راهنما = مشتری دنبال تابلویی می‌رود که می‌شناسد؛ همان اسمی که جست‌وجو می‌کند"),
    ("S12", "paper", None, "interpretation", None,
     [obj("plate", f"{D}/nameplate", x=330, y=1280, w=400, rot=-4, anim="slide_l"),
      obj("ticket", f"{D}/ticket", x=760, y=1330, w=380, rot=6, anim="slide_r", delay=0.3)], None,
     "بازگشت به آغاز: پلاک سردر (اسم شما) کنار ته‌بلیت (اسم آن‌ها) = هر اسم سر جای خودش؛ بستن دایره‌ی ریل"),
    ("S13", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("دو استودیوی افسانه‌ای یکی شدند.", "b"), ("اسم تازه *هیچ‌کدامشان* نیست.", "h")],
    "S2": [("اسم شرکت مادر حالا اسکای‌دنس است.", "b"), ("اسمی برای *ساختمان*.", "h")],
    "S3": [("زیرش، اسم‌های آشنا", "b"), ("هنوز *زیر نور* ایستاده‌اند.", "h")],
    "S4": [("این بخشِ هوشمندانه‌ی ماجراست.", "b"), ("کسی از *شرکت* بلیت نمی‌خرد.", "h")],
    "S5": [("مردم برای فیلم پول می‌دهند،", "b"), ("برای اسمی که *می‌شناسند*.", "h")],
    "S6": [("اسم بالای سر، مخاطب دیگری دارد:", "b"), ("*بانک*، کارمند، سهام‌دار.", "h")],
    "S7": [("شرکت مادر دسته‌کلید را نگه می‌دارد.", "b"), ("*برندها* درها را باز می‌کنند.", "h")],
    "S8": [("هر بنیان‌گذاری این وسوسه را می‌شناسد:", "b"), ("اسم *خودتان* بالای همه.", "h")],
    "S9": [("برای قضاوت درباره‌ی این اسم زود است.", "s"), ("ولی قاعده سر جایش است:", "b"), ("هر اسم، *یک* مخاطب.", "h")],
    "S10": [("پیش از عوض‌کردن اسم،", "b"), ("بنویسید هر اسم را *چه کسی* می‌خواند.", "h")],
    "S11": [("بعد از اسمی محافظت کنید", "b"), ("که مشتری *جست‌وجویش* می‌کند.", "h")],
    "S12": [("اسم خودتان روی در.", "b"), ("اسم آن‌ها روی *پرده*.", "h")],
    "S13": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Two legendary studios merged.", "b"), ("The new name is *neither*.", "h")],
    "S2": [("The parent is now Skydance.", "b"), ("A name for the *building*.", "h")],
    "S3": [("Underneath, the famous names", "b"), ("*stay* in the spotlight.", "h")],
    "S4": [("That's the smart part.", "b"), ("Nobody buys a ticket from a *company*.", "h")],
    "S5": [("People pay for the film,", "b"), ("and a name they *know*.", "h")],
    "S6": [("The name on top talks to", "b"), ("*banks*, staff and investors.", "h")],
    "S7": [("The parent holds the key ring.", "b"), ("The *brands* open the doors.", "h")],
    "S8": [("Every founder knows the itch:", "b"), ("put *your* name on top.", "h")],
    "S9": [("Too early to judge this one.", "s"), ("But the rule holds:", "b"), ("every name has *one* audience.", "h")],
    "S10": [("Before you rename,", "b"), ("write down who *reads* each name.", "h")],
    "S11": [("Then protect the one", "b"), ("customers already *search* for.", "h")],
    "S12": [("Your name goes on the door.", "b"), ("Theirs stays on the *screen*.", "h")],
    "S13": [("Write to me.", "b")],
}

SOURCES = [
    {"publisher": "TechCrunch", "title": "Paramount and Warner Bros. Discovery to become Skydance", "date": "2026-10-02", "url": TC1},
    {"publisher": "TechCrunch", "title": "Paramount closes historic Warner Bros. merger to form Skydance", "date": "2026-10-06", "url": TC2},
    {"publisher": "Deseret News", "title": "Paramount and Warner Bros. merger gets new name", "date": "2026-10-02", "url": DN},
    {"publisher": "Creative Bloq", "title": "Warner Bros and Paramount's Skydance rebrand isn't going down well (reaction; image T-a)", "date": "2026-10-03", "url": CB},
    {"publisher": "Design Compass", "title": "Skydance: Paramount and Warner Bros brand identity (image T-b)", "date": "2026-10-07", "url": DC},
]

CAP_FA = """دو استودیوی افسانه‌ای یکی شدند. اسم تازه، هیچ‌کدامشان نیست.

پارامونت و وارنر برادرز دیسکاوری در ۶ اکتبر ادغام شدند و شرکت تازه «اسکای‌دنس» نام گرفت؛ اسم شرکت تولیدی قبلی دیوید الیسون. خودش نوشته: «هرگز نخواستیم یک هویت شرکتی تازه، هیچ‌کدام از این دو را کم‌رنگ کند، تغییر دهد یا تحت‌الشعاع قرار دهد.» و اسم‌های آشنا، از پارامونت و برادران وارنر تا اچ‌بی‌او مکس و سی‌ان‌ان، با همان اسم خودشان زیر این چتر قرار گرفته‌اند.

به نظر من بخش هوشمندانه‌ی ماجرا همین است. کسی از «شرکت» بلیت نمی‌خرد؛ برای فیلم می‌آید، برای اسمی که می‌شناسد. اسم بالای سر مخاطب دیگری دارد: بانک، کارمند، سهام‌دار. شرکت مادر دسته‌کلید را نگه می‌دارد؛ برندها درها را باز می‌کنند.

وسوسه‌ی گذاشتن اسم خودتان بالای همه‌چیز را هر بنیان‌گذاری می‌شناسد. پیش از عوض‌کردن اسم، بنویسید هر اسم را چه کسی می‌خواند، و از اسمی که مشتری جست‌وجویش می‌کند محافظت کنید.

حدودش را هم بگویم: برای قضاوت درباره‌ی خودِ اسم «اسکای‌دنس» خیلی زود است. واکنش‌های اولیه در شبکه‌های اجتماعی بیشتر منفی بوده (به گزارش Creative Bloq)، ولی این روایت آدم‌هاست، نه داده. منبع‌ها: TechCrunch، Deseret News، Creative Bloq و Design Compass. دو تصویر واقعی از ویدئوی معرفی و هویت اسکای‌دنس‌اند (آپلود مالک)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

در کسب‌وکار شما، مشتری کدام اسم را صدا می‌زند: اسم شرکت یا اسم محصول؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Two legendary studios merged. The new name is neither of them.

Paramount and Warner Bros. Discovery closed their merger on October 6, and the combined company is called Skydance, the name of David Ellison's original production company. His words: "We never wanted a new corporate identity to diminish, alter or overshadow either one." Paramount, Warner Bros., HBO Max, CNN and the rest sit underneath it, under their own names.

My take: that's the smart part. Nobody buys a ticket from a holding company. People pay for the film, and for a name they know. The name on top has a different audience: banks, staff, investors. The parent holds the key ring; the brands open the doors.

Every founder knows the itch to put their own name on top. Before you rename anything, write down who reads each name, and protect the one customers already search for.

The limits: it's far too early to judge the Skydance name itself. Early online reaction has been mostly unkind (per Creative Bloq), but that's social posts, not data. Sources: TechCrunch, Deseret News, Creative Bloq, Design Compass. The two real images are from Skydance's launch video and identity (owner uploads); the other objects are AI-generated.

In your business, which name do customers actually say out loud: the company's or the product's? Write to me.

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
        if sid == "S13": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        scenes.append(s)
    return {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
            "topic": "اسم روی ساختمان، اسم روی پرده: هر اسم یک مخاطب دارد" if lang == "fa" else "The name on the building vs the name on the screen",
            "pillar": "naming_brand_architecture", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
            "caption": CAP_FA if lang == "fa" else CAP_EN,
            "hashtags": ["#برندینگ", "#بازاریابی", "#brandstrategy", "#rebrand"] if lang == "fa" else ["#branding", "#marketing", "#brandstrategy", "#rebrand"],
            "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
            "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S7"}, "status": "DRAFT", "style": "editorial", "lang": lang}


for n, lang in ((1, "fa"), (2, "en")):
    (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
print("ok")
