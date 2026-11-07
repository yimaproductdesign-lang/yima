"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-07 from one shared visual plan.
Topic: the US Copyright Office review board found UPS's shield logos 'not creative enough' for copyright;
the idea underneath: a logo's value comes from years of consistent use, not from cleverness."""
import json, os, pathlib

D = "2026-11-07"
HERE = pathlib.Path(__file__).parent
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
MOCK = "Editorial mockup (AI-generated blank, Figma gemini-3.1-flash-image + official UPS logo, owner upload; logo is a trademark of UPS)"
RT = "2026-11-07T01:30:00Z"
TFL = "https://www.thefashionlaw.com/ups-loss-shows-the-copyright-limits-of-even-the-most-recognizable-logos/"
BL = "https://news.bloomberglaw.com/ip-law/ups-loses-appeal-to-copyright-brown-shield-logos-at-review-board"
BI = "https://www.businessinsurance.com/ups-logo-fails-to-deliver-on-copyright-protection/"
VL = "https://www.vitallaw.com/news/copyright-news-copyright-office-review-board-nothing-original-about-ups-shield-logos/ipm01452f41562e02422d897119e15fd39354"
TN = "https://www.trucknews.com/transportation/ups-unveils-new-look-with-redesigned-shield-logo/1000027706"
L360 = "https://www.law360.com/articles/2545117/copyright-board-rejects-ups-logo-registration-bid"

E_TFL = {"url": TFL, "publisher": "The Fashion Law", "event_date": "2026-11-02", "retrieved_at": RT,
         "claim": "Review Board (30 Oct) affirmed refusal to register two UPS shield logos: familiar geometric shapes, conventional gradient, ordinary lettering; 'insufficiently creative'; copyright turns on the resulting expression, not the effort or decisions; trademark rights not addressed."}
E_BL = {"url": BL, "publisher": "Bloomberg Law", "event_date": "2026-10-30", "retrieved_at": "2026-11-06T16:00:00Z",
        "claim": "Review Board upheld two refusals; no creative spark; UPS already holds trademarks for the lettered shield logo and for the dark brown colour used on its vehicles and uniforms."}
E_TN = {"url": TN, "publisher": "Truck News", "event_date": "2003-03-26", "retrieved_at": RT,
        "claim": "Previous shield designed by Paul Rand in 1961; redesigned in 2003, dropping the bow-tied parcel."}


def obj(key, path_, x=540, y=1300, w=420, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


def mock(key, name, **kw):
    o = {"key": key, "src": f"assets/mockups/{D}/{name}.png", "x": 540, "y": 1280, "w": 560, "color": [0, 0], "credit": MOCK, "source_url": "owner upload: incoming/2026-11-07/T-b.png (official UPS logo file)"}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1200, "w": 760, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.03, "color": [0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


CR_A = "UPS shield logos as filed (blank and lettered); trademarks of UPS; owner upload"
CR_C = "UPS logos 1937, 1961, today (cropped from a third-party logo-history chart, owner upload; dates removed); trademarks of UPS"
TA_AR = 738 / 273
TC_AR = 999 / 370

SEEN = {"fa": ["کامیون", "جعبه", "لباس فرم", "برچسب", "انبار", "کوچه"],
        "en": ["trucks", "boxes", "uniforms", "labels", "depots", "streets"]}
LBL = {"fa": ("زیرکانه", "آشنا"), "en": ("clever", "familiar")}


def fx_for(sid, lang):
    if sid == "S6":
        a, b = LBL[lang]
        return [{"type": "labels", "items": [{"text": a, "x": 320, "y": 1250, "move": "up", "t": 1.4, "size": 92},
                                             {"text": b, "x": 760, "y": 1250, "move": "down", "acc": True, "t": 1.4, "size": 108}]}]
    if sid == "S9":
        return [{"type": "words", "mode": "pop", "box": [140, 980, 940, 1500], "seed": 31, "size": 58, "stagger": 0.08,
                 "words": SEEN[lang]}]
    if sid == "S13":
        return [{"type": "rings", "x": 540, "y": 1290, "R": 360, "n": 4, "period": 1.6, "t": 0.6, "op": 0.25}]
    return None


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1260, "fact", [E_TFL], [mock("box", "boxes_all", w=620, y=1185, anim="drop")], None,
     "قلاب: موکاپ ویرایشی، پنج جعبه‌ی کارتنی با همان سپر روی هر کدام = نشانه‌ای که همه میلیون‌ها بار دیده‌اند؛ «تکرار» از قاب اول"),
    ("S2", "paper", None, "interpretation", None, [mock("van", "van", w=820, y=1290, anim="slide_l")], None,
     "ون قهوه‌ای با همان سپر از کنار قاب وارد می‌شود = جایی که واقعاً می‌بینیمش: کوچه، هر روز"),
    ("S3", "graphite", 1200, "fact", [E_TFL, E_BL], [frame("ta", "T-a.png", TA_AR, CR_A, TFL, w=720, y=1150),
                                                      obj("stamp", "2026-10-29/stamp", w=170, x=820, y=1400, anim="drop", rot=-8)], None,
     "سند واقعی (آپلود مالک): همان دو نسخه‌ای که رد شد، قاب‌دار؛ مهر از بالا فرود می‌آید = حکم «رد»"),
    ("S4", "paper", None, "fact", [E_TFL], [obj("shapes", f"{D}/plain_shapes", w=720, y=1290, anim="rise", credit="Plain shapes drawn by the studio (PIL), no brand mark", source_url="studio drawing (drafts/2026-11-07/build assets)")], None,
     "دلیل حکم به زبان تصویر: دایره، سپر، مربع؛ شکل‌های معمولی با سایه‌روشن ساده = «شکل‌های هندسی آشنا»"),
    ("S5", "graphite", 1290, "fact", [E_TFL], [obj("pencil", "2026-10-22/pencil", w=560, y=1290, rot=-12, anim="slide_r")], None,
     "مداد = همه‌ی زحمت و تصمیم‌های طراح؛ قانون فقط نتیجه را می‌بیند، نه مداد را"),
    ("S6", "paper", None, "interpretation", None, None, "S6",
     "چرخش (drop): «زیرکانه» سبک است، بالا می‌رود و محو می‌شود؛ «آشنا» سنگین پایین می‌نشیند = ارزش در آشنایی است"),
    ("S7", "graphite", 1200, "fact", [E_TN], [frame("tc", "T-c_strip.png", TC_AR, CR_C, TN, w=760, y=1200)], None,
     "سند واقعی (آپلود مالک، بی‌تاریخ): از سپر پرنوشته‌ی قدیم تا سپر ساده‌ی امروز = ساده‌تر شد، نه شلوغ‌تر"),
    ("S8", "paper", None, "interpretation", None, [obj("stone", "2026-10-26/worn_stone", w=640, y=1300, anim="rise", float=2)], None,
     "سنگی که آب صافش کرده = ارزشی که تکرار می‌سازد، نه تراش زیرکانه"),
    ("S9", "graphite", 1240, "interpretation", None, None, "S9",
     "ابر جاهایی که نشانه دیده می‌شود (کامیون، جعبه، لباس فرم، در خانه…) که یکی‌یکی روشن می‌شوند = تکرار در زندگی روزمره"),
    ("S10", "paper", None, "fact", [E_BL, E_TFL], [obj("key", "2026-10-24/key", w=500, y=1300, rot=-20, anim="slide_l", float=2)], None,
     "احتیاط یک بار: کلید = حمایت حقوقی هنوز سر جایش است (علامت تجاری)؛ این حکم فقط درباره‌ی کپی‌رایت بود"),
    ("S11", "graphite", 1290, "interpretation", None, [obj("thread", "2026-10-29/thread", w=480, y=1290, anim="pop", vibrate=1)], None,
     "نخ درهم = لوگوی شلوغ‌تر و عوض‌کردن هرساله؛ همان چیزی که برندهای کوچک به‌جای تکرار می‌خرند"),
    ("S12", "paper", None, "interpretation", None, [obj("cup", "2026-10-29/cup", w=480, y=1300, anim="rise", float=2)], None,
     "لیوان = سطح روزمره‌ی کسب‌وکار کوچک؛ جای همان نشانه‌ی ساده که باید هر روز تکرار شود"),
    ("S13", "graphite", 1290, "interpretation", None, [obj("watch", "2026-10-22/watch", w=400, y=1290, anim="fade")], "S13",
     "ساعت با حلقه‌های آرام = زمان، ماده‌ی اصلی؛ دست نزدن، سال‌ها"),
    ("S14", "paper", None, "interpretation", None, [mock("box", "boxes_all", w=620, y=1185, anim="zoom")], None,
     "بازگشت به آغاز: همان جعبه‌ها، حالا روی کاغذ و روشن = قلاب برعکس می‌شود: خلاقانه نیست، فراموش‌نشدنی است"),
    ("S15", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("رسماً «خلاقانه نیست».", "b"), ("ولی همه *می‌شناسندش*.", "h")],
    "S2": [("این سپر را دیده‌اید.", "b"), ("*همه‌جا* دیده‌اید.", "h")],
    "S3": [("هفته‌ی پیش دفتر کپی‌رایت آمریکا گفت:", "b"), ("به‌اندازه‌ی کافی *خلاقانه* نیست.", "h")],
    "S4": [("چند شکل آشنا، یک سایه‌روشن ساده،", "b"), ("حروف *معمولی*.", "h")],
    "S5": [("زحمتی که پایش کشیدند؟", "b"), ("*حساب* نیست. فقط نتیجه.", "h")],
    "S6": [("شبیه توهین است.", "b"), ("ولی راز *کارکردش* همین است.", "h")],
    "S7": [("در این دهه‌ها", "b"), ("*ساده‌تر* شد، نه شلوغ‌تر.", "h")],
    "S8": [("ارزشش از زیرکی نیامد.", "b"), ("از *تکرار* آمد.", "h")],
    "S9": [("هر کامیون، هر جعبه،", "b"), ("هر *درِ خانه*، سال‌ها.", "h")],
    "S10": [("یک توضیح: بحث فقط کپی‌رایت بود.", "b"), ("هنوز *علامت تجاری* آن‌هاست.", "h")],
    "S11": [("بیشتر برندهای کوچک برعکس عمل می‌کنند:", "b"), ("لوگوی *شلوغ‌تر*، هر سال یکی تازه.", "h")],
    "S12": [("یک نشانه‌ی ساده انتخاب کنید.", "b"), ("روی هر *لیوان*، هر کیسه.", "h")],
    "S13": [("بعد دیگر دست به آن نزنید.", "b"), ("*سال‌ها*.", "h")],
    "S14": [("خلاقانه نیست.", "b"), ("*فراموش‌نشدنی* است.", "h")],
    "S15": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Officially not creative.", "b"), ("Instantly *recognised*.", "h")],
    "S2": [("You know this shield.", "b"), ("You've seen it *everywhere*.", "h")],
    "S3": [("Last week, the US copyright office", "b"), ("said it's not *creative* enough.", "h")],
    "S4": [("Common shapes. A plain gradient.", "b"), ("*Ordinary* letters.", "h")],
    "S5": [("All the effort behind it?", "b"), ("Doesn't *count*. Only the result.", "h")],
    "S6": [("Sounds like an insult.", "b"), ("It's why it *works*.", "h")],
    "S7": [("Over the decades,", "b"), ("it got *simpler*, not busier.", "h")],
    "S8": [("Its value wasn't cleverness.", "b"), ("It was *repetition*.", "h")],
    "S9": [("Every truck. Every box.", "b"), ("Every *doorstep*, for decades.", "h")],
    "S10": [("To be clear: this was copyright.", "b"), ("It's still their *trademark*.", "h")],
    "S11": [("Most small brands do the opposite.", "b"), ("A *busier* logo. Then a new one.", "h")],
    "S12": [("Pick one simple mark.", "b"), ("Put it on every *cup* and bag.", "h")],
    "S13": [("Then leave it alone.", "b"), ("For *years*.", "h")],
    "S14": [("Not creative.", "b"), ("*Unmistakable*.", "h")],
    "S15": [("Write to me.", "b")],
}
VO = {"S3": "Last week, the US Copyright Office said it's not creative enough.",
      "S14": "Not creative. Unmistakable."}

SOURCES = [
    {"publisher": "The Fashion Law", "title": "UPS Loss Shows the Copyright Limits of Even the Most Recognizable Logos", "date": "2026-11-02", "url": TFL},
    {"publisher": "Bloomberg Law", "title": "UPS Loses Appeal to Copyright Brown Shield Logos at Review Board", "date": "2026-10-30", "url": BL},
    {"publisher": "Business Insurance", "title": "UPS logo fails to deliver on copyright protection", "date": "2026-11-03", "url": BI},
    {"publisher": "IP Law Daily / VitalLaw", "title": "Copyright Office Review Board: Nothing original about UPS shield logos", "date": "2026-11-04", "url": VL},
    {"publisher": "Law360", "title": "Copyright Board Rejects UPS Logo Registration Bid", "date": "2026-11-02", "url": L360},
    {"publisher": "Truck News", "title": "UPS unveils new look with redesigned shield logo", "date": "2003-03-26", "url": TN},
]

CAP_FA = """رسماً «خلاقانه نیست». ولی همه می‌شناسندش.

سی‌ام اکتبر، هیئت بازبینی دفتر کپی‌رایت آمریکا درخواست UPS را برای ثبت کپی‌رایت دو نسخه از سپر قهوه‌ای و طلایی‌اش (سپر خالی و سپر با حروف ups) رد کرد. دلیلش به زبان ساده: شکل‌های هندسی آشنا، سایه‌روشن معمولی و حروف معمولی؛ به گفته‌ی هیئت، «به‌اندازه‌ی کافی خلاقانه نیست». و نکته‌ی جالب‌تر: معیار، نتیجه‌ای است که می‌بینیم، نه زحمت و تصمیم‌هایی که پشتش بوده.

به نظر من این توهین نیست؛ تعریف از سادگی است. سپر UPS در این دهه‌ها ساده‌تر شد، نه شلوغ‌تر: پل رند در ۱۹۶۱ سپری با یک بسته‌ی روبان‌پیچ کشید و در بازطراحی ۲۰۰۳ آن بسته حذف شد. ارزشش از زیرکی نیامد؛ از سال‌ها دیده‌شدن روی هر کامیون، هر جعبه و هر در خانه آمد.

حدودش را بگویم: این فقط درباره‌ی کپی‌رایت است. UPS هنوز علامت تجاری سپر حروف‌دار و رنگ قهوه‌ای خودروها و لباس‌های فرمش را دارد؛ یعنی لوگویش بی‌حمایت نیست و «هر کسی نمی‌تواند کپی‌اش کند». این تصمیم یک هیئت اداری است، رویه‌ی الزام‌آور نیست و مشاوره‌ی حقوقی هم نیست؛ برای ثبت نشانه‌ی خودتان با وکیل علامت تجاری حرف بزنید. منبع: The Fashion Law، Bloomberg Law، Business Insurance و IP Law Daily. موکاپ ویرایشی؛ لوگو متعلق به صاحب آن است (جعبه و ون با هوش مصنوعی ساخته شده و لوگوی واقعی رویشان گذاشته شده؛ این تبلیغ یا عکس رسمی UPS نیست). لوگوها و جدول تاریخچه آپلود مالک‌اند؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

برای صاحب کافه، سالن یا مغازه: پول لوگوی شلوغ‌تر را ندهید. یک نشانه‌ی ساده انتخاب کنید و سال‌ها همان را، یک‌جور، روی هر لیوان و کیسه و تابلو و پست بگذارید.

نشانه‌ی کسب‌وکار شما در چند سال گذشته چند بار عوض شده، و مشتری‌ها کدام نسخه را به خاطر دارند؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Officially not creative. Instantly recognised.

On 30 October, the US Copyright Office's review board refused to register two versions of UPS's brown-and-gold shield (the blank shield and the one with "ups" lettering). In plain words: familiar geometric shapes, a conventional gradient, ordinary lettering. "Insufficiently creative." And the sharper point: copyright looks at the result you see, not the effort or decisions behind it.

My take: that's not an insult. It's a compliment to simplicity. The shield got simpler over the decades, not busier. Paul Rand drew a shield topped with a ribbon-tied parcel in 1961; the 2003 redesign dropped the parcel. Its value never came from cleverness. It came from years on every truck, every box, every doorstep.

The limits: this was about copyright only. UPS still holds trademarks on the lettered shield and on the dark brown of its vehicles and uniforms, so the logo isn't unprotected and no, not anyone can copy it. It's one board decision with no precedential weight, and this isn't legal advice; if you want to protect your own mark, talk to a trademark lawyer. Sources: The Fashion Law, Bloomberg Law, Business Insurance, IP Law Daily. Editorial mockups: AI-generated blank boxes and van with the real logo placed on them; the logo belongs to its owner, and these are not UPS ads or official photos. The logos and the history chart are owner uploads; other objects are AI-generated.

For owners of a café, a salon, a shop: don't pay for a busier logo. Pick one simple mark and use it the same way on every cup, bag, sign and post, for years.

How many times has your mark changed in the last five years, and which version do your customers actually remember? Write to me.

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
         "topic": "خلاقانه نیست، فراموش‌نشدنی است: ارزش لوگو از تکرار می‌آید، نه از پیچیدگی" if lang == "fa" else "Not creative, unmistakable: a logo's value comes from years of use, not cleverness",
         "pillar": "brand_identity_strategy", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#طراحی_لوگو", "#branding", "#logodesign"] if lang == "fa" else ["#branding", "#marketing", "#logodesign", "#brandidentity"],
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
