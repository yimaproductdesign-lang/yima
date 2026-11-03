"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-03 from one shared visual plan.
Topic: key value items — Uniqlo Japan cancelled a ¥100 sock rise 11 days after announcing it; the ¥1,000 jacket rise stayed."""
import json, pathlib

D = "2026-11-03"
HERE = pathlib.Path(__file__).parent
AI = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
RT = "2026-11-03T01:40:00Z"
ADV = "https://www.advertimes.com/?p=562209"
FS = "https://www.fashionsnap.com/article/2026-10-27/uniqlo-priceup-withdrawal/"
AFP = "https://www.arabnews.jp/en/business/uniqlo-cancels-socks-price-hikes-in-japan-as-inflation-bites-3001153"
BB = "https://www.thestar.com.my/aseanplus/aseanplus-news/2026/10/29/uniqlo-scraps-price-rise-on-us2-socks-after-japan-shopper-outcry"
FTN = "https://foodtradenews.com/2026/06/23/the-10-products-that-still-define-your-entire-value-proposition/"

E_ADV = {"url": ADV, "publisher": "AdverTimes (Sendenkaigi)", "event_date": "2026-10-28", "retrieved_at": RT,
         "claim": "16 Oct notice: from 10 Nov 50-colour socks ¥290->¥390 and 4-for-¥990 / 3-for-¥990 bundles end; Kando Jacket ¥6,990->¥7,990, Kando Pants ¥3,990->¥4,990. 27 Oct: sock changes cancelled with an apology; jacket/pants rises unchanged."}
E_BB = {"url": BB, "publisher": "Bloomberg via The Star", "event_date": "2026-10-29", "retrieved_at": RT,
        "claim": "Reversed less than two weeks after announcing, after shopper complaints on social media; spokesperson: 'As socks are an essential everyday item, in Japan we reconsidered our planned price revision.'"}
E_FTN = {"url": FTN, "publisher": "Food Trade News (citing McKinsey, State of Grocery North America 2026)", "event_date": "2026-06-23", "retrieved_at": RT,
         "claim": "Supermarkets carry ~30,000-60,000 SKUs; McKinsey lists about ten items (eggs, milk, bread...) that shape shoppers' view of a store's value."}

CR_A = "Image: Bloomberg, Uniqlo sock shelf (owner upload)"
CR_B = "Image: Uniqlo store sign, via FASHIONSNAP (owner upload)"


def obj(key, path, x=540, y=1300, w=420, credit=AI, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1290, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "color": [0, 0, 0], "credit": credit, "source_url": url}
    o.update(kw); return o


WORDS = {"fa": (["برنج", "صابون", "ماکارونی", "چای", "شامپو", "نان", "روغن", "شیر", "حبوبات", "تخم‌مرغ", "دستمال", "قهوه"], ["نان", "شیر", "تخم‌مرغ"]),
         "en": (["rice", "soap", "pasta", "tea", "shampoo", "bread", "oil", "milk", "beans", "eggs", "tissues", "coffee"], ["bread", "milk", "eggs"])}
SCALE_LABELS = {"fa": ("٪", "انصاف"), "en": ("%", "fair?")}


def fx_for(sid, lang):
    if sid == "S8":
        w, k = WORDS[lang]
        return [{"type": "words", "mode": "fade", "box": [150, 1040, 930, 1470], "seed": 11, "size": 56, "t0": 0.9, "words": w, "keep": k}]
    if sid == "S7":
        a, b = SCALE_LABELS[lang]
        return [{"type": "labels", "items": [{"text": a, "x": 370, "y": 1010, "size": 80, "move": "up", "t": 1.4},
                                             {"text": b, "x": 710, "y": 1010, "size": 68, "acc": True, "move": "down", "t": 1.4}]}]
    return None


# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1300, "fact", [E_ADV], [frame("ta", "T-a.png", 1.502, CR_A, BB, w=860, y=1300)], None,
     "قلاب با عکس واقعی قفسه‌ی جوراب‌ها و برچسب ¥290 (آپلود مالک، قاب‌دار، رنگ طبیعی چون خود محصول موضوع است) = همان جورابی که ماجرا سرش بود"),
    ("S2", "paper", None, "fact", [E_ADV], [obj("suit", "2026-11-01/suit", y=1300, w=440, anim="drop", float=3)], None,
     "کت روی چوب‌لباسی با برچسب = افزایش بزرگ و آشکار روی کالای سنجیده"),
    ("S3", "graphite", 1300, "fact", [E_ADV], [obj("tag", "2026-10-25/price_tag", y=1300, w=560, rot=-8, anim="slide_r", float=4, bright=[1.0, 1.1])], None,
     "برچسب قیمت سفید روی تاریکی = قیمت کوچکِ ۲۹۰ که قرار بود ۳۹۰ شود"),
    ("S4", "paper", None, "fact", [E_BB], [obj("phone", "2026-10-25/phone", y=1300, w=560, rot=-6, anim="rise", vibrate=3)], None,
     "گوشی که می‌لرزد = شکایت‌ها در شبکه‌های اجتماعی پخش شد (بدون ساختن نقل‌قول یا عدد)"),
    ("S5", "graphite", 1290, "fact", [E_ADV, E_BB], [frame("tb", "T-b.png", 1.337, CR_B, FS, w=760, y=1290, anim="drop", push=0.05)], None,
     "چرخش (drop): تابلوی واقعی فروشگاه (آپلود مالک، قاب‌دار) = خود برند تصمیمش را پس گرفت"),
    ("S6", "paper", None, "fact", [E_ADV], [obj("suit", "2026-11-01/suit", y=1300, w=440, anim="fade", float=2)], None,
     "بازگشت همان کت، بی‌حرکت و آرام = افزایش کت سر جایش ماند"),
    ("S7", "graphite", 1330, "interpretation", None, [obj("scale", "2026-10-22/scale", y=1330, w=600, anim="rise", bright=[1.25, 1.3])], "S7",
     "ترازو با دو برچسب: «٪» بالا می‌رود و سبک است، «انصاف» پایین می‌نشیند = مشتری درصد را نمی‌سنجد، انصاف را می‌سنجد"),
    ("S8", "paper", None, "fact", [E_FTN], None, "S8",
     "ابر نام کالاهای سوپرمارکت محو می‌شود و فقط نان، شیر، تخم‌مرغ می‌مانند = هزاران کالا، چند قیمتِ از بر"),
    ("S9", "graphite", 1300, "interpretation", [E_BB], [obj("socks", f"{D}/socks_stack", y=1300, w=330, anim="pop", float=3, color=[0, 0, 0], credit=AI_NEW)], None,
     "دسته‌ی جوراب رنگی (محصول موضوع، رنگ طبیعی) زیر نور = جوراب همان شیر و تخم‌مرغِ یونیکلو؛ «خوانش من» یک بار"),
    ("S10", "paper", None, "interpretation", None, [obj("stamp", "2026-10-29/stamp", y=1300, w=320, anim="drop", float=2)], None,
     "مهر = قول؛ قیمت آشنا مهر برند است، به آن دست بزنی قول را شکسته‌ای"),
    ("S11", "graphite", 1300, "interpretation", None, [obj("lens", "2026-10-22/magnifier", y=1300, w=560, rot=-10, anim="slide_r", bright=[1.3, 1.3])], None,
     "ذره‌بین = جورابِ کسب‌وکار خودت را پیدا کن"),
    ("S12", "paper", None, "interpretation", None, [obj("cup", "2026-10-29/cup", y=1300, w=440, anim="rise", float=2)], None,
     "فنجان = در کافه، اسپرسو همان جوراب است؛ مثال ملموس برای صاحب کسب‌وکار"),
    ("S13", "graphite", 1300, "interpretation", None, [frame("ta", "T-a.png", 1.502, CR_A, BB, w=860, y=1300, anim="fade", push=0.06)], None,
     "بازگشت به آغاز: همان قفسه‌ی جوراب‌ها = به قیمت آشنا آخر از همه دست بزن"),
    ("S14", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("صد ین روی جوراب،", "b"), ("از هزار ین روی کت *گران‌تر* تمام شد.", "h")],
    "S2": [("یونیکلو در ژاپن اعلام کرد:", "b"), ("کت، *هزار ین* گران‌تر.", "h")],
    "S3": [("و جوراب:", "b"), ("از ۲۹۰ ین به *۳۹۰*.", "h")],
    "S4": [("شکایت‌ها در شبکه‌های اجتماعی پخش شد.", "b"), ("سرِ یک جفت *جوراب*.", "h")],
    "S5": [("یازده روز بعد،", "b"), ("گرانی جوراب را *پس گرفت*.", "h")],
    "S6": [("و گرانی کت؟", "b"), ("*سر جایش* ماند.", "h")],
    "S7": [("خیال می‌کنیم مشتری درصد حساب می‌کند.", "b"), ("مشتری *انصاف* را می‌سنجد.", "h")],
    "S8": [("سوپرمارکت هزاران کالا دارد.", "b"), ("مشتری با حدود *ده* قیمت قضاوتش می‌کند.", "h")],
    "S9": [("خوانش من این است:", "b"), ("جوراب، *شیر و تخم‌مرغِ* یونیکلوست.", "h")],
    "S10": [("به قیمتِ آشنا که دست بزنی،", "b"), ("به *قول* برند دست زده‌ای.", "h")],
    "S11": [("هر کسب‌وکاری جورابی دارد:", "b"), ("قیمتی که مشتری همیشگی *حفظ* است.", "h")],
    "S12": [("در کافه، اسپرسو. در نانوایی، نان.", "b"), ("در آرایشگاه، *کوتاهی مو*.", "h")],
    "S13": [("آخر از همه گرانش کن، و کم‌تر از همه.", "b"), ("گرانی را جایی ببر که *ارزش* پیداست.", "h")],
    "S14": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("¥100 on socks", "b"), ("cost more than ¥1,000 on a *jacket*.", "h")],
    "S2": [("Uniqlo Japan announced price rises.", "b"), ("A jacket: *¥1,000* more.", "h")],
    "S3": [("Plain socks:", "b"), ("¥290 to *¥390*.", "h")],
    "S4": [("Complaints spread online.", "b"), ("Over a pair of *socks*.", "h")],
    "S5": [("Eleven days later,", "b"), ("the sock rise was *cancelled*.", "h")],
    "S6": [("And the jacket rise?", "b"), ("It *stayed*.", "h")],
    "S7": [("We think customers do percentages.", "b"), ("They judge *fairness*.", "h")],
    "S8": [("A supermarket sells thousands of things.", "b"), ("Shoppers judge it by about *ten*.", "h")],
    "S9": [("My reading:", "b"), ("socks are Uniqlo's *milk and eggs*.", "h")],
    "S10": [("Touch the price people know by heart,", "b"), ("and you touch the *promise*.", "h")],
    "S11": [("Every business has its socks:", "b"), ("the price regulars *remember*.", "h")],
    "S12": [("In a café, it's the espresso.", "b"), ("In a salon, the *haircut*.", "h")],
    "S13": [("Move that price last, and least.", "b"), ("Raise where the *value* shows.", "h")],
    "S14": [("Write to me.", "b")],
}

SOURCES = [
    {"publisher": "AdverTimes (Sendenkaigi)", "title": "ユニクロが「値上げ撤回」の異例対応 発表からわずか11日、ソックス「4足990円」終了を中止", "date": "2026-10-28", "url": ADV},
    {"publisher": "FASHIONSNAP", "title": "Uniqlo withdraws sock price revision (image T-b page)", "date": "2026-10-27", "url": FS},
    {"publisher": "AFP via Arab News Japan", "title": "Uniqlo cancels socks price hikes in Japan as inflation bites", "date": "2026-10-29", "url": AFP},
    {"publisher": "Bloomberg via The Star", "title": "Uniqlo scraps price rise on US$2 socks after Japan shopper outcry (image T-a)", "date": "2026-10-29", "url": BB},
    {"publisher": "Food Trade News (citing McKinsey, State of Grocery North America 2026)", "title": "The 10 Products That (Still) Define Your Entire Value Proposition", "date": "2026-06-23", "url": FTN},
]

CAP_FA = """صد ین روی جوراب، از هزار ین روی کت گران‌تر تمام شد.

یونیکلو ۱۶ اکتبر در ژاپن اعلام کرد از ۱۰ نوامبر قیمت چند کالا بالا می‌رود: «کت کاندو» از ۶٬۹۹۰ ین به ۷٬۹۹۰ ین، و جوراب‌های ساده‌ی پنجاه‌رنگ از ۲۹۰ به ۳۹۰ ین؛ بسته‌های «چهار جفت ۹۹۰ ین» هم قرار بود تمام شوند. شکایت‌ها در شبکه‌های اجتماعی پخش شد. ۲۷ اکتبر، یازده روز بعد، یونیکلو تغییر قیمت جوراب را لغو کرد و برای تغییرِ درست بعد از اعلام عذر خواست. گرانی کت و شلوار سر جایش ماند.

دلیل رسمی‌شان این بود که جوراب «کالای ضروری روزمره» است. خوانش من یک قدم جلوتر است: مشتری همه‌ی قیمت‌های شما را به خاطر ندارد؛ چند قیمت را از بر دارد و با همان‌ها قضاوت می‌کند که «این‌جا منصف است یا نه». در سوپرمارکت این قیمت‌ها نان و شیر و تخم‌مرغ‌اند؛ مک‌کنزی حدود ده کالا را نام می‌برد که برداشت خریدار از ارزش یک فروشگاه را می‌سازند. در یونیکلو، به نظر من، جوراب همین نقش را دارد. به آن قیمت که دست بزنی، به قول برند دست زده‌ای.

حدودش را هم بگویم: این یک ماجراست، نه پژوهش. بخش بزرگ‌ترِ گرانی جوراب در پایان بسته‌ها بود (چهار جفت از ۹۹۰ به ۱٬۵۶۰ ین)، نه فقط آن صد ین. و این‌که جوراب «شیر و تخم‌مرغِ» یونیکلوست برداشت من است، نه حرف خود یونیکلو. یک امتیاز هم باید به یونیکلو داد: یازده روزه شنید و برگشت. منبع‌ها: AdverTimes، FASHIONSNAP، خبرگزاری فرانسه، بلومبرگ و Food Trade News (به نقل از گزارش مک‌کنزی). دو عکس واقعی آپلود مالک است (Bloomberg و FASHIONSNAP)؛ اشیای دیگر با هوش مصنوعی ساخته شده‌اند.

برای صاحب کسب‌وکار: «جوراب» خودتان را پیدا کنید؛ همان قیمتی که مشتری همیشگی حفظ است (اسپرسو، نان، کوتاهی مو). آخر از همه و کم‌تر از همه به آن دست بزنید، گرانی را جایی ببرید که ارزش دیده می‌شود، و یک بار و روشن اعلامش کنید.

در کسب‌وکار شما، جوراب چیست؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """¥100 on socks cost more than ¥1,000 on a jacket.

On 16 October, Uniqlo announced price rises in Japan from 10 November: the Kando Jacket from ¥6,990 to ¥7,990, and its plain 50-colour socks from ¥290 to ¥390, with the 4-for-¥990 sock bundles ending. Complaints spread on social media. On 27 October, eleven days later, Uniqlo cancelled the sock changes and apologised for changing course right after the notice. The jacket and trouser rises stayed.

Their stated reason: socks are "an essential everyday item." My reading goes one step further. Customers don't remember all your prices. They remember a few, and they use those few to decide whether you're fair. In a supermarket it's bread, milk and eggs; McKinsey names about ten items that shape how shoppers see a store's value. At Uniqlo, I think, socks play that role. Touch that price and you touch the promise.

The limits: this is one story, not a study. Most of the sock increase sat in the end of the bundles (four pairs going from ¥990 to ¥1,560), not just the ¥100. And "socks are Uniqlo's milk and eggs" is my reading, not Uniqlo's words. Credit where due: they listened and reversed in eleven days. Sources: AdverTimes, FASHIONSNAP, AFP, Bloomberg, Food Trade News (citing McKinsey). The two real photos are owner uploads (Bloomberg, FASHIONSNAP); the other objects are AI-generated.

For owners: find your socks, the price your regulars remember (the espresso, the bread, the haircut). Move it last and least. Raise where the value is visible. Announce it once, plainly.

What are the socks in your business? Write to me.

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
        scenes.append(s)
    return {"reel_id": f"{D}_{'FA' if lang == 'fa' else 'EN'}", "date": D,
            "topic": "صد ین روی جوراب، هزار ین روی کت: مشتری چند قیمت را از بر دارد" if lang == "fa" else "¥100 on socks, ¥1,000 on a jacket: customers remember a few prices, not all of them",
            "pillar": "pricing_communication_brand_promise", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
            "caption": CAP_FA if lang == "fa" else CAP_EN,
            "hashtags": ["#برندینگ", "#بازاریابی", "#pricingstrategy", "#قیمت_گذاری"] if lang == "fa" else ["#branding", "#marketing", "#pricingstrategy", "#smallbusinesstips"],
            "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
            "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S5"}, "status": "DRAFT", "style": "editorial", "lang": lang}


if __name__ == "__main__":
    for n, lang in ((1, "fa"), (2, "en")):
        (HERE / f"reel_0{n}.json").write_text(json.dumps(build(lang), ensure_ascii=False, indent=1), encoding="utf8")
    for L, C in (("fa", FA), ("en", EN)):
        print(L, sum(len(t.replace("*", "").split()) for v in C.values() for t, _ in v))
