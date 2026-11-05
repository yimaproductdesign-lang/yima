"""Builds reel_01.json (fa) and reel_02.json (en) for 2026-11-05 from one shared visual plan.
Topic: the monocle that was never there. People remember famous logos confidently, consistently and wrongly
(Prasad & Bainbridge 2022, Psychological Science; Creative Bloq feature 4 Nov 2026)."""
import json, os, pathlib

D = "2026-11-05"
HERE = pathlib.Path(__file__).parent
AI_NEW = "AI-generated object (Figma, gemini-3.1-flash-image)"
AI_OLD = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
RT = "2026-11-05T01:30:00Z"
CB = "https://www.creativebloq.com/inspiration/youve-been-picturing-these-logos-wrong-your-whole-life"
UC = "https://news.uchicago.edu/story/visual-mandela-effect-false-memories-psychology-neuroscience-pikachu-mr-monopoly-waldo"
SS = "https://socialsciences.uchicago.edu/node/21404"
NN = "https://neurosciencenews.com/logo-visual-mandela-effect-21066/"
APS = "https://www.psychologicalscience.org/publications/observer/visual-memory-distortions.html"

E_CB = {"url": CB, "publisher": "Creative Bloq", "event_date": "2026-11-04", "retrieved_at": RT,
        "claim": "Brain Bridge Lab (Univ. of Chicago), 40 images: Apple and Ralph Lauren ~80% correct; Monopoly man, Volkswagen, Fruit of the Loom only 20-30% chose the real logo; drawing from memory, people made the same mistakes unprompted."}
E_UC = {"url": SS, "publisher": "University of Chicago (Social Sciences Division)", "event_date": "2022-06-19", "retrieved_at": RT,
        "claim": "People are very confident in the wrong image; errors are shared; cornucopia chosen over plate argues against schema theory as sole cause; even looking at the right area they still erred; cause not yet pinpointed."}
E_NN = {"url": NN, "publisher": "Neuroscience News (UChicago release)", "event_date": "2022-07", "retrieved_at": RT,
        "claim": "Mr. Monopoly has never worn a monocle; consistent, confident false memories; no attentional or visual differences drive the effect."}

CR_C = "Image: University of Chicago / The Brain Bridge Lab (Prasad & Bainbridge 2022), owner upload"
CR_B = "Image: participants' drawings from memory, The Brain Bridge Lab (via Creative Bloq), owner upload"


def obj(key, path, x=540, y=1300, w=420, credit=AI_OLD, **kw):
    o = {"key": key, "src": f"assets/objects/{path}.png", "x": x, "y": y, "w": w, "credit": credit}
    o.update(kw); return o


def frame(key, img, ar, credit, url, **kw):
    o = {"key": key, "src": f"incoming/{D}/{img}", "x": 540, "y": 1290, "w": 900, "ar": ar, "frame": True,
         "anim": "zoom", "push": 0.04, "credit": credit, "source_url": url}
    o.update(kw); return o


WORDS = {"fa": ["رنگ", "فاصله", "گوشه", "سایه", "خط", "حرف", "شکل", "لوگو"],
         "en": ["colour", "gap", "corner", "shadow", "line", "letter", "shape", "logo"]}
LBL = {"fa": ("بشقاب", "شاخ"), "en": ("plate", "horn")}

TC_AR = 1380 / 776
TB_AR = 1000 / 563
TA_AR = 1000 / 563
CR_A = "Image: research figure, Prasad & Bainbridge 2022 (The Brain Bridge Lab), owner upload"


def fx_for(sid, lang):
    if sid == "S4":
        k = WORDS[lang][-1]
        return [{"type": "words", "mode": "fade", "box": [150, 1020, 930, 1480], "seed": 511, "size": 66,
                 "words": WORDS[lang], "keep": [k], "keep_at": [540, 1250]}]
    if sid == "S7":  # brackets land on the original (left of the three)
        return [{"type": "viewfinder", "box": [222, 1060, 436, 1240], "t": 1.2}]
    if sid == "S8":
        p, h = LBL[lang]
        return [{"type": "labels", "items": [{"text": p, "x": 330, "y": 1520, "move": "up", "t": 1.6, "size": 58},
                                             {"text": h, "x": 745, "y": 1520, "move": "down", "acc": True, "t": 1.6, "size": 58}]}]
    return None


MON = dict(credit=AI_NEW)
# (id, bg, spot_y, claim_type, evidence, objects, fx, rationale)
PLAN = [
    ("S1", "graphite", 1280, "fact", [E_NN], [obj("mon", f"{D}/monocle", w=520, y=1290, anim="drop", float=3, carry_out=True, **MON)], None,
     "قلاب: مونوکلِ تنها، بی‌صاحب، زیر نور = همان جزئیاتی که هرگز روی صورتِ مرد مونوپولی نبود"),
    ("S2", "paper", None, "fact", [E_UC], [obj("mon", f"{D}/monocle", w=600, y=1290, push=0.06, carry_in=True, **MON)], None,
     "همان مونوکل ادامه می‌دهد و بزرگ‌تر می‌شود = در ذهنِ ما واضح‌تر و مطمئن‌تر از واقعیت"),
    ("S3", "graphite", 1290, "fact", [E_CB], [frame("tc", "T-c.png", TC_AR, CR_C, UC, w=900, y=1290, color=[0, 0])], None,
     "تصویر کامل و رنگیِ آزمونِ پژوهش (آپلود مالک، قاب‌دار، به خواست مالک): سه نسخه از هر برند و شخصیت؛ بیننده خودش امتحان می‌کند"),
    ("S4", "paper", None, "fact", [E_CB], None, "S4",
     "ابرِ جزئیاتِ لوگو (رنگ، فاصله، گوشه...) محو می‌شود و فقط «لوگو» می‌ماند = حافظه کلیت را نگه می‌دارد و جزئیات را می‌بازد"),
    ("S5", "graphite", 1290, "fact", [E_CB], [frame("tb", "T-b.png", TB_AR, CR_B, CB, w=900, y=1290, anim="drop", push=0.03, color=[0, 0])], None,
     "همه‌ی نقاشی‌های واقعیِ شرکت‌کننده‌ها از حافظه، کامل و رنگی (آپلود مالک) با فلش روی خطاهای مشترک (مونوکل، شاخ، دم) = همان اشتباه‌ها"),
    ("S6", "paper", None, "fact", [E_UC, E_NN], [obj("lens", "2026-10-22/magnifier", w=540, y=1300, rot=-10, anim="slide_r")], None,
     "ذره‌بین = نگاهِ دقیق؛ مشکل از نگاه کردن به جای اشتباه نبود"),
    ("S7", "graphite", 1290, "fact", [E_UC], [frame("ta", "T-a.png", TA_AR, CR_A, APS, w=900, y=1290, anim="fade", push=0.02, color=[0, 0])], None,
     "چرخش: شکلِ اصلی پژوهش، کامل و رنگی (ردیف A = اصل، B = نسخه‌ی شاخ‌دار) = جواب آزمون؛ برچسب‌های خودِ شکل اصل و نسخه‌ی ساختگی را نشان می‌دهند"),
    ("S8", "paper", None, "fact", [E_UC], [obj("scale", "2026-10-22/scale", w=620, y=1300, anim="rise")], "S8",
     "ترازو: «بشقاب» (جوابِ منطقی) سبک می‌شود و بالا می‌رود، «شاخ» سنگین می‌ماند = انتخاب، با منطق نمی‌خواند"),
    ("S9", "graphite", 1290, "fact", [E_UC], [obj("photo", "2026-10-22/photo", w=560, y=1300, rot=-4, anim="drop", blur=[0, 7, 1.2, 3.2])], None,
     "عکسِ قدیمی که تار می‌شود = حافظه عکس نیست؛ و چرایش هنوز معلوم نیست (احتیاط یک بار)"),
    ("S10", "paper", None, "interpretation", None, [obj("brain", "2026-10-22/brain", w=520, y=1300, anim="rise", float=3)], None,
     "مغز = جایی که برند واقعاً زندگی می‌کند، نه کتابچه‌ی برند"),
    ("S11", "graphite", 1300, "interpretation", None, [obj("pen", "2026-10-22/pencil", w=600, y=1300, rot=-20, anim="slide_l")], None,
     "مداد = آزمونِ صاحب کسب‌وکار: از مشتری بخواه از حافظه بکشد"),
    ("S12", "paper", None, "interpretation", None, [obj("plate", "2026-10-31/nameplate", w=600, y=1300, anim="drop", float=2)], None,
     "تابلوی نام = آنچه همه به یاد می‌آورند؛ برندِ واقعی"),
    ("S13", "graphite", 1300, "interpretation", None, [obj("eraser", "2026-10-22/eraser", w=440, y=1300, rot=8, anim="pop")], None,
     "پاک‌کن = آنچه مشتری اضافه می‌کند: یا قصه‌ای که نگه می‌داری، یا خطایی که پاک می‌کنی"),
    ("S14", "paper", None, "interpretation", None, [obj("mon", f"{D}/monocle", w=560, y=1290, anim="zoom", float=3, **MON)], None,
     "بازگشت به آغاز: همان مونوکل = برندِ شما در ذهنِ مشتری چه جزئیاتی دارد که شما نساختید؟"),
    ("S15", "primary", None, "interpretation", None, None, None, "کارت پایانی"),
]

FA = {
    "S1": [("مردِ مونوپولی هیچ‌وقت", "b"), ("*مونوکل* نداشت.", "h")],
    "S2": [("ولی بیشترِ ما می‌بینیمش،", "b"), ("و سرش *شرط* هم می‌بندیم.", "h")],
    "S3": [("از هر کدام سه نسخه.", "b"), ("کدام *واقعی* است؟", "h")],
    "S4": [("برای لوگوهایی مثل فولکس‌واگن،", "b"), ("فقط *۲۰ تا ۳۰ درصد* درست گفتند.", "h")],
    "S5": [("از حافظه که کشیدند،", "b"), ("*همان* اشتباه‌ها تکرار شد.", "h")],
    "S6": [("حتی وقتی همان‌جا را نگاه کردند،", "b"), ("باز *اشتباه* کردند.", "h")],
    "S7": [("لوگوی «فروت آو د لوم» میوه دارد.", "b"), ("ولی هرگز *شاخ* نداشت.", "h")],
    "S8": [("بشقاب منطقی‌تر بود.", "b"), ("باز هم *شاخ* را انتخاب کردند.", "h")],
    "S9": [("چرایش هنوز معلوم نیست.", "b"), ("حافظه *عکس* نیست.", "h")],
    "S10": [("برندِ شما آن نیست که طراحی کردید.", "b"), ("آن است که در ذهن‌ها *ماند*.", "h")],
    "S11": [("یک آزمونِ ساده:", "b"), ("پنج مشتری تابلویتان را *از حافظه* بکشند.", "h")],
    "S12": [("آنچه همه می‌کشند،", "b"), ("برندِ *واقعی* شماست.", "h")],
    "S13": [("آنچه همه اضافه می‌کنند،", "b"), ("یا *قصه* است، یا *خطا*.", "h")],
    "S14": [("برندِ شما در ذهنِ مشتری", "b"), ("چه *مونوکلی* به چشم زده؟", "h")],
    "S15": [("برای من بنویسید.", "b")],
}
EN = {
    "S1": [("The Monopoly man", "b"), ("never wore a *monocle*.", "h")],
    "S2": [("Yet most of us see one,", "b"), ("and we'd *bet* on it.", "h")],
    "S3": [("Three versions of each.", "b"), ("Which ones are *real*?", "h")],
    "S4": [("For logos like Volkswagen,", "b"), ("only *20 to 30%* got it right.", "h")],
    "S5": [("From memory,", "b"), ("people drew the *same* mistakes.", "h")],
    "S6": [("Even looking right at it,", "b"), ("still *wrong*.", "h")],
    "S7": [("Fruit of the Loom has fruit.", "b"), ("It never had a *horn*.", "h")],
    "S8": [("A plate makes more sense.", "b"), ("They still picked the *horn*.", "h")],
    "S9": [("Nobody knows why yet.", "b"), ("Memory isn't a *photo*.", "h")],
    "S10": [("Your brand isn't your design.", "b"), ("It's what *survived* in their heads.", "h")],
    "S11": [("Try this: five customers", "b"), ("draw your sign *from memory*.", "h")],
    "S12": [("What they all keep", "b"), ("is your *real* brand.", "h")],
    "S13": [("What they all add", "b"), ("is a *story*, or a *mistake*.", "h")],
    "S14": [("In your customers' heads,", "b"), ("what's your *monocle*?", "h")],
    "S15": [("Write to me.", "b")],
}
VO = {"S4": "For logos like Volkswagen, only twenty to thirty percent got it right."}

SOURCES = [
    {"publisher": "Creative Bloq", "title": "Why do millions of us remember famous logos all wrong? The Mandela effect, explained", "date": "2026-11-04", "url": CB},
    {"publisher": "University of Chicago News", "title": "Visual Mandela effect: false memories of Pikachu, Mr. Monopoly and Waldo", "date": "2022-07-15", "url": UC},
    {"publisher": "University of Chicago, Social Sciences Division", "title": "New Research Shows Consistency in What We Misremember", "date": "2022-06-19", "url": SS},
    {"publisher": "Neuroscience News", "title": "Study Finds Widespread False Memories of Logos and Characters, Including Mr. Monopoly and Pikachu", "date": "2022-07", "url": NN},
    {"publisher": "APS Observer", "title": "Visual memory distortions (Prasad & Bainbridge 2022, Psychological Science 33(12), 1971-1988)", "date": "2024-06-12", "url": APS},
]

CAP_FA = """مردِ مونوپولی هیچ‌وقت مونوکل نداشت. ولی احتمالاً همین الان دارید می‌بینیدش.

پژوهشگرانِ دانشگاه شیکاگو (پراساد و بینبریج، ۲۰۲۲) چهل تصویرِ آشنا را با نسخه‌های دست‌کاری‌شده کنار هم گذاشتند. برای اپل و رالف لورن حدود ۸۰ درصد درست انتخاب کردند؛ برای مرد مونوپولی، فولکس‌واگن و «فروت آو د لوم» فقط ۲۰ تا ۳۰ درصد. آدم‌ها به انتخابِ غلطشان مطمئن بودند، و وقتی از حافظه کشیدند، همان اشتباه‌ها را تکرار کردند. حتی کسانی که درست به همان نقطه نگاه کرده بودند.

عجیب‌ترش: لوگوی «فروت آو د لوم» هرگز شاخِ فراوانی نداشته. بشقاب جوابِ منطقی‌تری بود، ولی آدم‌ها باز شاخ را انتخاب کردند. یعنی مغز همیشه «جورترین» جزئیات را اضافه نمی‌کند. چرایش هنوز معلوم نیست؛ اسمش را گذاشته‌اند «اثر ماندلای تصویری».

حدودش را بگویم: این یک پژوهش آزمایشگاهی است با چند ده تا صد شرکت‌کننده در هر آزمایش، نه نظرسنجی از مشتری‌های شما. خبرِ تازه، گزارشی است که کریتیو بلاک ۴ نوامبر منتشر کرد؛ خودِ پژوهش مالِ ۲۰۲۲ است. تصویرهای آزمون آپلود مالک‌اند (از منبع‌های بالا)، اشیای دیگر با هوش مصنوعی ساخته شده‌اند. اینکه «برند همان است که در ذهن می‌ماند» برداشتِ من است.

برای صاحب کسب‌وکار: از پنج مشتری بخواهید تابلو یا لیوانتان را از حافظه بکشند. آنچه همه می‌کشند، برندِ واقعی شماست. آنچه همه از خودشان اضافه می‌کنند، یا قصه‌ای است که می‌شود ساخت، یا خطایی که باید درستش کرد.

برندِ شما در ذهنِ مشتری چه جزئیاتی دارد که خودتان هرگز نساختید؟ برای من بنویسید.

— بهنود کاویان"""

CAP_EN = """The Monopoly man never wore a monocle. You can probably see it anyway.

Researchers at the University of Chicago (Prasad and Bainbridge, 2022) showed people 40 familiar images next to altered versions. For Apple and Ralph Lauren, around 80% picked the real one. For the Monopoly man, Volkswagen and Fruit of the Loom, only 20 to 30% did. People were confident in their wrong picks, and when they drew the images from memory, they repeated the same mistakes. Even those who looked right at the spot.

The strange part: the Fruit of the Loom logo never had a horn of plenty. A plate would make more sense, and people still chose the horn. So the brain doesn't simply add the detail that fits best. Why it happens is still unknown; researchers call it the visual Mandela effect.

The limits: this is lab research with roughly fifty to a hundred people per experiment, not a survey of your customers. The fresh news is a Creative Bloq feature from 4 November; the study itself is from 2022. The test images are owner uploads from the sources below; the other objects are AI-generated. "Your brand is what survives in their heads" is my reading.

For owners: ask five customers to draw your sign or your cup from memory. What they all keep is your real brand. What they all add is either a story you can build on or a mistake you need to fix.

What does your brand wear in your customers' heads that you never gave it? Write to me.

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
         "topic": "مونوکلی که هرگز نبود: مشتری برندت را با اطمینان به یاد دارد، ولی نسخه‌ای را که تو نساختی" if lang == "fa" else "The monocle that was never there: customers remember your brand with total confidence, and remember it wrong",
         "pillar": "identity_memory_consumer_behaviour", "format": {"w": 1080, "h": 1920, "fps": 30}, "scenes": scenes,
         "caption": CAP_FA if lang == "fa" else CAP_EN,
         "hashtags": ["#برندینگ", "#بازاریابی", "#logodesign", "#mandelaeffect"] if lang == "fa" else ["#branding", "#marketing", "#logodesign", "#mandelaeffect"],
         "sources": SOURCES, "cta": "برای من بنویسید." if lang == "fa" else "Write to me.",
         "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S7"}, "status": "DRAFT", "style": "editorial", "lang": lang}
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
