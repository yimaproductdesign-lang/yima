"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-10-29 from one shared visual plan."""
import json, pathlib

D = "2026-10-29"
HERE = pathlib.Path(__file__).parent
AI = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
OURA = "https://ouraring.com/blog/wear-your-best-life-brand-campaign/"
POLA = "https://creativebloq.com/design/branding/polaroid-just-dropped-the-most-iconic-anti-ai-ad-of-the-year"
RT = "2026-10-29T05:00:00Z"

EV_OURA = [
    {"url": OURA, "publisher": "Oura (official blog)", "event_date": "2026-10-08", "retrieved_at": RT,
     "claim": "'Wear Your Best Life' eschews AI; a world crafted entirely by hands; 35 modelmakers built a 1:10 city in Prague over three weeks; practical effects"},
    {"url": "https://www.famouscampaigns.com/?p=47289", "publisher": "Famous Campaigns", "event_date": "2026-10-13", "retrieved_at": RT,
     "claim": "Oura 'shunned AI in favour of handmade sets and practical effects'; '35 modelmakers in Prague'; built 'in three weeks'; Nice+Frank, director Sam Walker"},
]
EV_GARTNER = [{"url": "https://www.gartner.com/en/newsroom/press-releases/2026-03-16-gartner-marketing-survey-finds-50-percent-of-consumers-prefer-brands-that-avoid-using-genai-in-consumer-facing-content0",
               "publisher": "Gartner (press release)", "event_date": "2026-03-16", "retrieved_at": RT,
               "claim": "Survey of 1,539 US consumers, Oct 2025: 68% frequently wonder whether the content they see is real; 50% would prefer brands that do not use GenAI"}]
EV_POLA = [{"url": POLA, "publisher": "Creative Bloq", "event_date": "2025-07-19", "retrieved_at": RT,
            "claim": "Polaroid in-house outdoor campaign: 'AI can't generate sand between your toes'"}]


def obj(key, name, x=540, y=1280, w=420, **kw):
    o = {"key": key, "src": f"assets/objects/{D}/{name}.png" if "/" not in name else name, "x": x, "y": y, "w": w, "credit": AI}
    o.update(kw); return o


def frame(key, img, credit, url, ar, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1250, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "color": [0, 0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


# shared visual plan: (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1250, "fact", EV_OURA, [frame("ta", "T-a.png", "Oura 'Wear Your Best Life' behind-the-scenes photo (owner upload)", OURA, 1.776, y=1320, w=820)], None,
     "قلاب با مدرک واقعی: پشت‌صحنه‌ی شهر مینیاتوری که ماکت‌سازی رویش خم شده (آپلود مالک، قاب‌دار زیر نور موضعی) = ۳۵ نفر، سه هفته، با دست"),
    ("S2", "paper", None, "fact", EV_OURA, [obj("ring", "ring", y=1250, w=300, anim="drop", float=4)], None,
     "یک انگشتر ساده و تنها که می‌افتد وسط کاغذ = این‌همه زحمت برای یک شیء کوچک"),
    ("S3", "graphite", 1250, "fact", EV_OURA, [frame("tb", "T-b.png", "Oura 'Wear Your Best Life' campaign frame (owner upload)", OURA, 1.778)], None,
     "نتیجه‌ی واقعی کمپین (آپلود مالک): دستی که انگشتر دارد در باشگاه مینیاتوری راه می‌رود = هر قاب با دست ساخته شده، نه با ماشین"),
    ("S4", "paper", None, "interpretation", None, [obj("stamp", "stamp", y=1270, w=330, anim="drop", vibrate=4)], None,
     "مهر لاستیکی که با ضربه فرود می‌آید و می‌لرزد = تصویر را می‌شود بی‌نهایت بار، در یک ثانیه، کوبید"),
    ("S5", "graphite", 1290, "interpretation", None, [obj("phone", "assets/objects/2026-10-25/phone.png", y=1300, w=460, rot=-4, anim="slide_r", bright=[1.7, 1.7], path=[[0, 540, 1340], [3.6, 540, 1240]])], None,
     "گوشی از راست می‌آید و آرام مثل فید بالا می‌رود = فیدی که بی‌وقفه تصویر بی‌نقص و بی‌صاحب رد می‌کند"),
    ("S6", "paper", None, "fact", EV_GARTNER, [obj("lens", "assets/objects/2026-10-22/magnifier.png", y=1290, w=470, rot=-6, anim="pop", float=5)], None,
     "ذره‌بین = مخاطب حالا با دقت و بدگمانی نگاه می‌کند: واقعی است یا ساختگی؟"),
    ("S7", "graphite", 1250, "fact", EV_POLA, [frame("tc", "T-c.png", "Polaroid outdoor campaign artwork (owner upload)", POLA, 1.778)], None,
     "کمپین واقعی پولاروید (آپلود مالک، قاب‌دار): عکس فوری با جمله‌ی دست‌نویس = «واقعی بودن» خودش شعار تبلیغ شده"),
    ("S8", "paper", None, "interpretation", None, [obj("watch", "assets/objects/2026-10-22/watch.png", y=1330, w=330, anim="pop")], None,
     "چرخش (drop): ساعت = زمانی که خرج شده؛ زحمت پیامِ «برایت وقت گذاشتم» است"),
    ("S9", "graphite", 1290, "interpretation", None, [obj("tweezers", "tweezers", y=1290, w=560, rot=-4, anim="slide_l", bright=[1.5, 1.5])], None,
     "موچین ماکت‌ساز که یک آجر ریز را نگه داشته = زحمتی که جعلش سخت است، آجر به آجر"),
    ("S10", "paper", None, "interpretation", None, [obj("cup", "cup", y=1300, w=420, anim="rise")], None,
     "فنجان دست‌ساز با لبه‌ی کج = نقص کوچک، امضای دست و مدرک زحمت"),
    ("S11", "graphite", 1290, "interpretation", None, [obj("scale", "assets/objects/2026-10-22/scale.png", y=1300, w=470, anim="rise", tilt=-5, tilt_t=1.4, bright=[1.4, 1.4])], None,
     "ترازو که کج می‌شود = ساختنِ ارزان در یک کفه، باورکردنِ گران در کفه‌ی دیگر"),
    ("S12", "paper", None, "interpretation", None, [obj("thread", "thread", y=1300, w=400, anim="rise", float=4)], None,
     "قرقره و سوزن = دوخت پشت پارچه که کسی نمی‌بیند؛ کار ماشین را بگذار برای پشت‌صحنه"),
    ("S13", "graphite", 1220, "interpretation", None, [obj("house", "mini_house", y=1200, w=250, anim="rise")], None,
     "بازگشت به آغاز: یک خانه‌ی مینیاتوری دست‌ساز از همان شهر صحنه‌ی اول = زحمت را جایی بگذار که دیده می‌شود"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("۳۵ نفر. سه هفته.", "h"), ("یک شهر کوچک، با *دست*.", "h")],
    "S2": [("برای فروش یک *انگشتر*.", "h")],
    "S3": [("و اورا عمداً سراغ", "b"), ("*هوش مصنوعی* نرفت.", "h")],
    "S4": [("امروز هر تصویری را", "b"), ("در چند *ثانیه* می‌شود ساخت.", "h")],
    "S5": [("فید پر از تصویرهای بی‌نقص است،", "b"), ("و *بی‌صاحب*.", "h")],
    "S6": [("مخاطب حالا ریز می‌شود و می‌پرسد:", "b"), ("*واقعی* است؟", "h")],
    "S7": [("حالا «واقعی بودن»", "b"), ("خودش *شعار* تبلیغ شده.", "h")],
    "S8": [("داده‌ها هنوز کم‌اند.", "s"), ("ولی به نظر من، زحمت می‌گوید:", "b"), ("«برایت *وقت* گذاشتم.»", "h")],
    "S9": [("زحمت را سخت می‌شود جعل کرد؛", "b"), ("برای همین *باورش* می‌کنیم.", "h")],
    "S10": [("کجیِ کوچکِ لبه‌ی این فنجان", "b"), ("نقص نیست؛ *مدرک* است.", "h")],
    "S11": [("هرچه ساختنش ارزان‌تر به نظر برسد،", "b"), ("باورکردنش *گران‌تر* است.", "h")],
    "S12": [("ماشین را بگذارید برای کارهایی", "b"), ("که مشتری *نمی‌بیند*.", "h")],
    "S13": [("و زحمت را جایی خرج کنید", "b"), ("که *دیده* می‌شود.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("35 people. Three weeks.", "b"), ("A tiny city, built by *hand*.", "h")],
    "S2": [("To sell a *ring*.", "h")],
    "S3": [("And Oura kept AI", "b"), ("out of it. On *purpose*.", "h")],
    "S4": [("Today, any image", "b"), ("takes *seconds* to make.", "h")],
    "S5": [("Feeds are full of perfect pictures", "b"), ("nobody *made*.", "h")],
    "S6": [("So people squint and ask:", "b"), ("is this *real*?", "h")],
    "S7": [("Now “real” itself", "b"), ("is the *ad line*.", "h")],
    "S8": [("The data is still thin.", "s"), ("But my take: effort says", "b"), ("“I spent *time* on you.”", "h")],
    "S9": [("Effort is hard to fake.", "b"), ("That's why we *believe* it.", "h")],
    "S10": [("That wobble on the rim", "b"), ("isn't a flaw. It's *proof*.", "h")],
    "S11": [("The cheaper it looks to make,", "b"), ("the harder it is to *believe*.", "h")],
    "S12": [("Let machines do the work", "b"), ("customers never *see*.", "h")],
    "S13": [("Spend the effort", "b"), ("where they *look*.", "h")],
    "S14": [("Write to me.", "b")],
}

SOURCES = [
    {"publisher": "Oura (official blog)", "title": "Wear Your Best Life: Oura's new brand campaign", "date": "2026-10-08", "url": OURA},
    {"publisher": "Famous Campaigns", "title": "Oura skips AI to build a tiny city where hands do the walking", "date": "2026-10-13", "url": "https://www.famouscampaigns.com/?p=47289"},
    {"publisher": "The Drum", "title": "Ad of the day: Oura lets its fingers do the living in handmade miniature city", "date": "2026-10-08", "url": "https://www.thedrum.com/news/ad-of-the-day-oura-lets-its-fingers-do-the-living-in-handmade-miniature-city"},
    {"publisher": "Gartner", "title": "Gartner marketing survey finds 50% of consumers prefer brands that avoid using GenAI in consumer-facing content", "date": "2026-03-16", "url": EV_GARTNER[0]["url"]},
    {"publisher": "Creative Bloq", "title": "Polaroid just dropped the most iconic anti-AI ad of the year", "date": "2025-07-19", "url": POLA},
]

CAP_FA = """۳۵ نفر، سه هفته، یک شهر کوچک با دست. برای فروش یک انگشتر.

اورا، سازنده‌ی انگشتر هوشمند، برای کمپین تازه‌اش «Wear Your Best Life» عمداً سراغ هوش مصنوعی نرفت. به نوشته‌ی وبلاگ خودش، ۳۵ ماکت‌ساز در پراگ ظرف سه هفته شهری در مقیاس یک‌دهم ساختند و همه‌چیز با جلوه‌های عملی، جلوی دوربین، گرفته شد. پولاروید هم پیش‌تر روی بیلبوردهایش نوشته بود که هوش مصنوعی نمی‌تواند شنِ لای انگشت‌های پا را بسازد.

به نظر من موضوع ضدیت با هوش مصنوعی نیست. وقتی ساختن هر تصویری چند ثانیه طول می‌کشد، زحمتِ دیده‌شده خودش پیام می‌شود: «برایت وقت گذاشتم.» زحمت را سخت می‌شود جعل کرد و برای همین باورش می‌کنیم. هرچه چیزی ارزان‌تر ساخته به نظر برسد، باورکردنش گران‌تر تمام می‌شود.

راه عملی‌اش این است: ماشین را برای کارهایی بگذارید که مشتری نمی‌بیند، و دست و وقت آدم‌ها را جایی خرج کنید که دیده می‌شود.

حدودش را هم بگویم: در نظرسنجی گارتنر (۱٬۵۳۹ مصرف‌کننده‌ی آمریکایی، اکتبر ۲۰۲۵) ۶۸ درصد گفته‌اند مدام از خودشان می‌پرسند محتوایی که می‌بینند واقعی است یا نه، و نیمی گفته‌اند برندهایی را ترجیح می‌دهند که از هوش مصنوعی مولد استفاده نمی‌کنند. این حرفِ آدم‌هاست، نه رفتار خریدشان، و فقط در یک کشور. از نتیجه‌ی فروش کمپین اورا هم هنوز عددی منتشر نشده. بقیه برداشت خود من است. منبع‌ها: وبلاگ اورا، Famous Campaigns، The Drum، Gartner و Creative Bloq. تصویرهای واقعی از کمپین‌های اورا و پولاروید‌اند (آپلود مالک)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

در کار شما، زحمت کجا خرج می‌شود: جایی که مشتری می‌بیند، یا پشت‌صحنه؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """Thirty-five people. Three weeks. A tiny city, built by hand. To sell a ring.

For its new "Wear Your Best Life" campaign, Oura chose not to use AI. Its own blog says 35 modelmakers in Prague built a one-tenth-scale city in three weeks, shot with practical effects. Polaroid got there earlier with a billboard line: AI can't generate sand between your toes.

My take: this isn't an anti-AI sermon. When any image takes seconds to make, visible effort becomes the message. It says "I spent time on you." Effort is hard to fake, which is exactly why we believe it. The cheaper something looks to make, the more expensive it is to believe.

The practical version: let machines do the work customers never see, and spend human hands and hours where they look.

The limits: in Gartner's survey (1,539 US consumers, October 2025), 68% said they often wonder whether the content they see is real, and half said they'd prefer brands that don't use GenAI. That is what people say, not what they buy, and it's one country. Oura hasn't published results for the campaign yet. The rest is my reading. Sources: Oura's blog, Famous Campaigns, The Drum, Gartner, Creative Bloq. The real photos are from Oura's and Polaroid's campaigns (owner uploads); the other objects are AI-generated.

Where does the effort go in your business: where customers can see it, or backstage? Write to me.

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
        if fx: s["fx"] = fx
        s["motion_rationale"] = why
        if sid == "S14": s.update({"logo": True, "txt_top": 1080})
        s["lines"] = [{"text": t, "kind": k, "dim": False} for t, k in copy[sid]]
        scenes.append(s)
    r = {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
         "topic": "وقتی همه‌چیز را می‌شود در چند ثانیه ساخت، زحمتِ دیده‌شده خودش پیام است" if lang == "fa" else "When anything can be generated in seconds, visible effort becomes the message",
         "pillar": "brand_communication_trust", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#برندسازی", "#craftsmanship"] if lang == "fa" else ["#branding", "#marketing", "#brandstrategy", "#craftsmanship"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S8"}, "status": "DRAFT", "style": "editorial", "lang": lang}
    return r


for n, lang in ((1, "fa"), (2, "en")):
    (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
print("ok")
