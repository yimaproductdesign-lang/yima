"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-09 from one shared visual plan.
Topic: 'our costs went up' has stopped working; when everyone gives the same reason, customers hear an excuse."""
import json, os, pathlib

D = "2026-11-09"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-09T04:30:00Z"
CONV = "https://insideretail.us/?p=89821"
UTK = "https://haslam.utk.edu/news/ut-haslam-researcher-finds-messaging-matters-in-price-increase-notifications/"
SI = "https://www.subscriptioninsider.com/blog/price-increase-messaging-subscription-churn-news"
KKT = "https://eml.berkeley.edu/~saez/course131/Kahneman-FairnessConstraintProfit-1986.pdf"

E_KKT1 = {"url": KKT, "publisher": "American Economic Review (Kahneman, Knetsch, Thaler)", "event_date": "1986-09", "retrieved_at": RT,
          "claim": "Hardware store raises snow shovels from $15 to $20 the morning after a large snowstorm: 82% unfair (N=107)."}
E_KKT2 = {"url": KKT, "publisher": "American Economic Review (Kahneman, Knetsch, Thaler)", "event_date": "1986-09", "retrieved_at": RT,
          "claim": "Grocer raises lettuce price after the wholesale price rose because of a shortage: 79% acceptable (N=101)."}
E_UTK = {"url": UTK, "publisher": "University of Tennessee, Haslam College of Business", "event_date": "2026-07-14", "retrieved_at": RT,
         "claim": "10-month field experiment, 1,600+ customers of a Canadian self-storage company (Journal of Marketing): cost and quality justifications 'on par with providing no justification at all'; market justification reduced attrition by 29.5% vs no justification, regardless of specificity."}
E_CONV = {"url": CONV, "publisher": "Inside Retail US, republished from The Conversation (Damavandi, Antia, Kopalle)", "event_date": "2026-09-08", "retrieved_at": RT,
          "claim": "'In times of prolonged inflation, like today, cost-based justifications may not be seen as fair anymore.' 'When every company points to higher costs ... customers typically see these explanations as empty excuses.'"}


def obj(key, path_, x=540, y=1290, w=460, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path_}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


SHOVEL = lambda **kw: obj("shovel", f"{D}/snow_shovel", w=600, y=1290, credit=AI_NEW, **kw)
KEY = lambda **kw: obj("key", "2026-10-24/key", w=440, y=1290, rot=-8, **kw)
MEGA = lambda **kw: obj("mega", "2026-11-06/megaphone", w=600, y=1290, credit=AI_NEW, **kw)

EXC = {"fa": (["تورم", "اجاره", "دستمزد", "سوخت", "حمل‌ونقل", "مواد اولیه", "بهانه"], "بهانه"),
       "en": (["inflation", "rent", "wages", "fuel", "shipping", "suppliers", "excuse"], "excuse")}


def fx_for(sid, lang):
    if sid == "S2":
        w, k = EXC[lang]
        return [{"type": "words", "mode": "fade", "box": [150, 1020, 930, 1480], "seed": 4, "size": 58, "words": w, "keep": [k], "keep_at": [540, 1260]}]
    if sid == "S8":
        return [{"type": "rings", "x": 540, "y": 1290, "R": 380, "n": 5, "period": 1.6, "inward": True, "t": 0.6}]
    if sid == "S10":
        return [{"type": "viewfinder", "box": [200, 1030, 880, 1500], "t": 0.5}]
    return None


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "paper", None, "interpretation", [E_CONV], [MEGA(anim="slide_l", vibrate=2)], None,
     "بلندگو = همه همان یک جمله را بلند تکرار می‌کنند؛ همین بلندگو در پایان (S14) برمی‌گردد و خاموش کنار می‌رود"),
    ("S2", "graphite", 1260, "interpretation", [E_CONV], None, "S2",
     "ابر دلیل‌های آشنای گرانی (تورم، اجاره، دستمزد، سوخت…) محو می‌شوند و فقط «بهانه» می‌ماند = آنچه مشتری از جمله‌ی تکراری می‌شنود"),
    ("S3", "paper", None, "fact", [E_KKT1], [SHOVEL(anim="drop", rot=-4)], None,
     "پاروی برف = آزمایش ۱۹۸۶: گران کردن بعد از طوفان؛ پارو در S11 برمی‌گردد (طوفان نسازید)"),
    ("S4", "graphite", 1290, "fact", [E_KKT2], [obj("lettuce", f"{D}/lettuce", w=520, y=1290, credit=AI_NEW, anim="rise", float=3, color=[0, 0, 0])], None,
     "کاهو (خودِ محصولِ داستان، رنگی) = گرانیِ منتقل‌شده از عمده‌فروش که منصفانه پذیرفته شد"),
    ("S5", "paper", None, "fact", [E_KKT1, E_KKT2], [obj("scale", "2026-10-22/scale", w=520, y=1300, anim="fade")], None,
     "ترازو = مشتری دلیل را می‌سنجید؛ دلیل، حکم را عوض می‌کرد"),
    ("S6", "graphite", 1290, "interpretation", [E_CONV], [obj("tag", "2026-10-25/price_tag", w=480, y=1290, rot=-12, anim="drop", float=2)], None,
     "چرخش (drop): برچسب قیمتِ خالی می‌افتد = همان دلیلِ روی برچسب دیگر کار نمی‌کند"),
    ("S7", "paper", None, "fact", [E_UTK], [KEY(anim="slide_r")], None,
     "کلید = انبار اجاره‌ای آزمایش میدانی؛ همین کلید در S8 ادامه پیدا می‌کند"),
    ("S8", "graphite", 1290, "fact", [E_UTK], [KEY(anim="zoom", float=3)], "S8",
     "همان کلید با حلقه‌های رو به داخل = تقاضای بیشتر برای جای کمتر؛ دلیلی که واقعاً در بازار هست"),
    ("S9", "paper", None, "interpretation", [E_CONV], [obj("stamp", "2026-10-29/stamp", w=400, y=1290, anim="drop")], None,
     "مهر = همان جمله که روی قیمت همه کوبیده می‌شود؛ تکراری و بی‌صاحب"),
    ("S10", "graphite", None, "interpretation", None, None, "S10",
     "احتیاط یک بار: منظره‌یاب = فقط یک قاب دیدیم؛ یک شرکت، یک صنعت"),
    ("S11", "paper", None, "fact", [E_KKT1], [SHOVEL(anim="slide_l", rot=6)], None,
     "بازگشت پاروی برف = کمبودِ ساختگی همان گرانیِ بعد از طوفان است که ۸۲٪ ناعادلانه دانستند"),
    ("S12", "graphite", 1290, "interpretation", None, [obj("lens", "2026-10-22/magnifier", w=480, y=1290, rot=-10, anim="slide_r", path=[[0.6, 600, 1290], [2.2, 480, 1260], [3.4, 560, 1300]])], None,
     "ذره‌بین = دلیلی که مشتری خودش می‌تواند وارسی کند"),
    ("S13", "paper", None, "interpretation", None, [obj("ear", "2026-11-06/ear_trumpet", w=600, y=1290, credit=AI_NEW, anim="slide_r")], None,
     "شیپور گوش = مشتری هنوز گوش می‌دهد، ولی نه به تکرار"),
    ("S14", "graphite", 1290, "interpretation", None, [MEGA(anim="fade", exit=["right", 2.6])], None,
     "بازگشت بلندگوی آغاز که از قاب بیرون می‌رود = جمله‌ی همه را کنار بگذارید"),
    ("S15", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("همه می‌گویند: «هزینه‌ها بالا رفته.»", "b"), ("برای همین *کسی نمی‌شنود*.", "h")],
    "S2": [("هر برند، همان یک جمله.", "b"), ("مشتری فقط *بهانه* می‌شنود.", "h")],
    "S3": [("۱۹۸۶. فردای برف، پارو گران می‌شود.", "b"), ("۸۲٪ گفتند: *ناعادلانه*.", "h")],
    "S4": [("کاهو گران می‌شود؛ عمده‌فروش گران داده.", "b"), ("۷۹٪ گفتند: *قبول*.", "h")],
    "S5": [("دلیل، حکم را عوض می‌کرد.", "b"), ("و هزینه *منصفانه‌ترین* دلیل بود.", "h")],
    "S6": [("حالا، بعد از سال‌ها گرانی،", "b"), ("همان دلیل *کار نمی‌کند*.", "h")],
    "S7": [("یک آزمایش میدانی، یک انبار اجاره‌ای:", "b"), ("دلیل هزینه با *سکوت* فرقی نداشت.", "h")],
    "S8": [("دلیل بازار: تقاضا بیشتر، جا کمتر.", "b"), ("*۳۰٪* کمتر رفتند.", "h")],
    "S9": [("جمله‌ای که همه مهر می‌زنند،", "b"), ("مال *هیچ‌کس* نیست.", "h")],
    "S10": [("یک شرکت، یک پژوهش.", "b"), ("*نشانه* است، نه قانون.", "h")],
    "S11": [("ولی *طوفان* نسازید.", "h"), ("کمبود ساختگی همان پاروی گران است.", "b")],
    "S12": [("دلیل *راست* را بگویید،", "h"), ("که مشتری خودش ببیند.", "b")],
    "S13": [("مشتری هنوز گوش می‌دهد.", "b"), ("فقط نه به *تکرار*.", "h")],
    "S14": [("جمله‌ی همه را قرض نگیرید.", "b"), ("*دلیل خودتان* را بگویید.", "h")],
    "S15": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("Everyone says \"our costs went up.\"", "b"), ("So no one *hears* it.", "h")],
    "S2": [("Every brand, same sentence.", "b"), ("Customers hear an *excuse*.", "h")],
    "S3": [("1986. After a storm, shovels cost more.", "b"), ("82% called it *unfair*.", "h")],
    "S4": [("Lettuce costs more; wholesale did too.", "b"), ("79% said *fine*.", "h")],
    "S5": [("The reason changed the verdict.", "b"), ("Cost was the *fair* one.", "h")],
    "S6": [("Now, years into rising prices,", "b"), ("that line *fails*.", "h")],
    "S7": [("One field study, storage units:", "b"), ("\"Costs\" did no better than *silence*.", "h")],
    "S8": [("A market reason: demand up, space short.", "b"), ("*30%* fewer left.", "h")],
    "S9": [("Everyone stamps it on.", "b"), ("So it's *no one's*.", "h")],
    "S10": [("One company. One study.", "b"), ("A *signal*, not a law.", "h")],
    "S11": [("But don't *fake* a storm.", "h"), ("Fake scarcity is the shovel.", "b")],
    "S12": [("Give the *true* reason,", "h"), ("one they can see.", "b")],
    "S13": [("They still listen.", "b"), ("Just not to a *rerun*.", "h")],
    "S14": [("Don't borrow everyone's line.", "b"), ("Give them *yours*.", "h")],
    "S15": [("Write to me.", "b")],
}
VO = {"S3": "Nineteen eighty-six. After a snowstorm, a store charges more for shovels. Eighty-two percent called it unfair.",
      "S4": "A grocer charges more for lettuce, because the wholesale price went up. Seventy-nine percent said that's fine.",
      "S8": "A market reason, demand up and space short, and about thirty percent fewer people left."}

SOURCES = [
    {"publisher": "Inside Retail US (republished from The Conversation)", "title": "Shoppers are more skeptical about companies' justifications for price hikes", "date": "2026-09-08", "url": CONV},
    {"publisher": "University of Tennessee, Haslam College of Business", "title": "UT Haslam researcher finds messaging matters in price increase notifications", "date": "2026-07-14", "url": UTK},
    {"publisher": "Subscription Insider", "title": "The reason you give for a price increase can affect churn", "date": "2026-07-15", "url": SI},
    {"publisher": "American Economic Review 76(4)", "title": "Fairness as a Constraint on Profit Seeking: Entitlements in the Market (Kahneman, Knetsch, Thaler)", "date": "1986-09", "url": KKT},
]

CAP_FA = """همه می‌گویند «هزینه‌ها بالا رفته». برای همین دیگر کسی نمی‌شنود.

سال ۱۹۸۶ کانمن، نِچ و تیلر از مردم پرسیدند: فروشگاهی فردای یک برف سنگین قیمت پارو را از ۱۵ به ۲۰ دلار می‌برد. ۸۲٪ گفتند ناعادلانه است. ولی وقتی بقال قیمت کاهو را بالا برد چون قیمت عمده‌فروشی بالا رفته بود، ۷۹٪ گفتند قابل قبول است. دلیل، حکم را عوض می‌کرد؛ و «هزینه» منصفانه‌ترین دلیل بود.

حالا یک آزمایش میدانی ۱۰ ماهه با بیش از ۱۶۰۰ مشتری یک شرکت انبار اجاره‌ای در کانادا (Journal of Marketing، ۲۰۲۶) نتیجه‌ی دیگری گرفت: پیام گرانی با دلیل «هزینه» یا «کیفیت» در نگه داشتن مشتری با هیچ دلیلی فرقی نداشت. دلیل «بازار» (تقاضای بیشتر، رقابت کمتر) ریزش را ۲۹٫۵٪ نسبت به پیام بی‌دلیل کم کرد، و جزئی‌تر کردن پیام این نتیجه را عوض نکرد. خود پژوهشگرها نوشته‌اند در تورم طولانی، وقتی همه به هزینه اشاره می‌کنند، مشتری آن را بهانه‌ی توخالی می‌بیند.

به نظر من مشتری دیگر خود دلیل را نمی‌سنجد؛ تکراری بودنش را می‌شنود. ولی این مجوز ساختن «تقاضا» یا «کمبود» نیست؛ کمبود ساختگی همان پاروی گران بعد از طوفان است. دلیلی بگویید که درباره‌ی بازار و کسب‌وکار خودتان راست است و مشتری خودش می‌تواند ببیند.

حدودش: این یک پژوهش است، با یک شرکت و در یک صنعت؛ نتیجه‌اش برای کافه یا فروشگاه شما قطعی نیست. عدد ۳۰٪ روی تصویر گرد شده‌ی ۲۹٫۵٪ است. منابع: The Conversation (بازنشر Inside Retail)، دانشگاه تنسی (Haslam)، Subscription Insider، و مقاله‌ی American Economic Review (۱۹۸۶). اشیای این ریل (پارو، کاهو و بقیه) آشکارا با هوش مصنوعی ساخته شده‌اند.

آخرین بار که قیمتتان را بالا بردید، به مشتری چه گفتید؛ و اگر جای او بودید، باورش می‌کردید؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Everyone says "our costs went up." That's why no one hears it.

In 1986, Kahneman, Knetsch and Thaler asked people about a hardware store that raises snow shovels from $15 to $20 the morning after a big storm. 82% called it unfair. But when a grocer raised the price of lettuce because the wholesale price had gone up, 79% called it acceptable. The reason changed the verdict, and cost was the fair one.

Now a 10-month field experiment with more than 1,600 customers of a Canadian self-storage company (Journal of Marketing, 2026) found something else. Price-rise notes that blamed costs or promised better quality kept customers no better than notes with no reason at all. A market reason (more demand, less competition) cut attrition by 29.5% against the no-reason note, and making the message more detailed didn't change that. The researchers write that in prolonged inflation, when every company points to higher costs, customers tend to see it as an empty excuse.

My take: customers no longer weigh the reason. They hear the repetition. That is not a licence to invent demand or scarcity; a fake shortage is the snow shovel all over again. Give the reason that is actually true about your market and your business, one customers can see for themselves.

The limits: this is one study, one company, one industry; it doesn't prove what will happen at your café or shop. The 30% on screen is 29.5% rounded. Sources: The Conversation (via Inside Retail), University of Tennessee Haslam College, Subscription Insider, and the 1986 American Economic Review paper. The objects in this reel (the shovel, the lettuce and the rest) are openly AI-generated.

The last time you raised a price, what did you tell customers, and would you have believed it? Write to me.

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
         "topic": "«هزینه‌ها بالا رفته» دیگر کار نمی‌کند؛ وقتی همه همین را می‌گویند، مشتری بهانه می‌شنود" if lang == "fa" else "'Our costs went up' has stopped working: when everyone says it, customers hear an excuse",
         "pillar": "pricing_communication", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#pricingstrategy", "#قیمت_گذاری"] if lang == "fa" else ["#marketing", "#branding", "#pricingstrategy", "#consumerpsychology"],
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
