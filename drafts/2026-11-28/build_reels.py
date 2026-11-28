"""Build reel_01 (fa) and reel_02 (en) for 2026-11-28 (Hershey) from one shared visual plan. motion v2."""
import json, pathlib, copy

D = "2026-11-28"
AI = "AI-generated object (Figma, gemini-3.1-flash-image)"
AIL = "AI-generated object (Figma, gemini-3.1-flash-lite-image)"
O = lambda n, d: f"assets/objects/{d}/{n}.png"

EV = {
    "film": {"url": "https://www.marketingdive.com/news/how-hershey-strategized-its-brand-film-to-be-more-than-a-90-minute-ad/875365/", "publisher": "Marketing Dive", "event_date": "2026-11-25", "retrieved_at": "2026-11-27T20:58:00+04:00", "claim": "Hershey film in theaters 25 Nov; made with the Hershey entities; 'not ... a 90-minute commercial'."},
    "rt": {"url": "https://www.rottentomatoes.com/m/hershey", "publisher": "Rotten Tomatoes", "event_date": "2026-11-27", "retrieved_at": "2026-11-27T20:58:00+04:00", "claim": "Tomatometer 17% (18 reviews), Popcornmeter 90% (100+ verified); THR: 'essentially serves as a feature-length product placement'."},
    "brit": {"url": "https://www.britannica.com/biography/Milton-Snavely-Hershey", "publisher": "Britannica", "event_date": "n/a", "retrieved_at": "2026-11-27T21:00:00+04:00", "claim": "Philadelphia shop failed; New York failed; fresh-milk caramels; sold caramel company 1900 for $1,000,000; grew despite his refusal to advertise."},
    "hco": {"url": "https://www.thehersheycompany.com/en_us/our-story/milton-hershey.html", "publisher": "The Hershey Company", "event_date": "n/a", "retrieved_at": "2026-11-27T21:00:00+04:00", "claim": "First two candy companies failed; first ended in bankruptcy."},
    "bio": {"url": "https://www.biography.com/business-leaders/milton-hershey", "publisher": "Biography.com", "event_date": "2026-11-24", "retrieved_at": "2026-11-27T21:00:00+04:00", "claim": "'Give them quality. That's the best kind of advertising in the world.'"},
}

# shared visual plan: (id, bg, evidence keys, claim_type, objects, fx, extras, rationale)
PLAN = [
    ("S1", "graphite", ["brit", "film"], "fact",
     [{"key": "choc", "src": O("chocolate_whole", "2026-10-25"), "x": 560, "y": 1300, "w": 640, "rot": -8, "color": [0, 0, 0], "credit": AIL, "anim": "rise"},
      {"key": "ticket", "src": O("ticket", "2026-10-31"), "x": 520, "y": 1240, "w": 500, "rot": 10, "credit": AIL, "anim": "drop", "delay": .5, "z": 2}],
     [], {"spot_y": 1260, "shake": [0.75, 10]},
     "بلیت سینما که روی شکلات می‌افتد = تناقض قلاب: مردی که تبلیغ نمی‌کرد، حالا مردم برای تبلیغش بلیت می‌خرند"),
    ("S2", "paper", ["bio"], "fact",
     [{"key": "scale", "src": O("scale", "2026-10-22"), "x": 540, "y": 1300, "w": 560, "credit": AIL, "anim": "swing"}],
     [], {"cam": {"push": .06}},
     "ترازو = «کیفیت» به‌جای فریاد؛ جمله‌ی خودش که کیفیت را بهترین تبلیغ می‌دانست"),
    ("S3", "graphite", ["hco", "brit"], "fact",
     [{"key": "lock", "src": O("padlock", D), "x": 540, "y": 1290, "w": 420, "credit": AI, "anim": "swing"}],
     [], {"spot_y": 1270, "shake": [0.55, 14], "wipe": "v"},
     "قفل سنگین که روی در مغازه تاب می‌خورد = ورشکستگی؛ لرزش دوربین لحظه‌ی سقوط است"),
    ("S4", "paper", ["brit", "hco"], "fact",
     [], [{"type": "timeline", "y": 1290, "x0": 250, "x1": 830, "items": "TL", "active": 2, "t": .3, "span": 2.2, "size": 58, "note_size": 44}],
     {}, "خط زمانی که نقطه‌به‌نقطه پیش می‌رود = دو شکست پشت سر هم، و نقطه‌ی سوم (لنکستر) که روشن می‌ماند"),
    ("S5", "graphite", ["brit"], "fact",
     [{"key": "milk", "src": O("juice_glass", "2026-10-24"), "x": 540, "y": 1340, "w": 300, "noscale": True, "credit": AIL, "anim": "rise", "push": .08}],
     [], {"spot_y": 1270},
     "لیوان شیر (تک‌رنگ) = همان ایده‌ی ساده: کارامل با شیر تازه"),
    ("S6", "paper", ["brit"], "fact",
     [], [{"type": "counter", "x": 540, "y": 1180, "size": 170, "acc": True, "t": .4, "dur": 1.5, "COUNTER": 1, "bar": [150, 930, 1420], "max": 1, "to": 1}],
     {"flash": False},
     "شمارنده‌ای که تا یک میلیون دلار بالا می‌رود = فروش کارخانه‌ی کارامل در ۱۹۰۰ و شرط‌بندی روی شکلات"),
    ("S7", "graphite", ["brit"], "fact",
     [{"key": "choc", "src": O("chocolate_gap", "2026-10-25"), "x": 540, "y": 1300, "w": 660, "rot": 6, "color": [0, 0, 0], "credit": AIL, "anim": "zoom"},
      {"key": "mega", "src": O("megaphone", "2026-11-06"), "x": 800, "y": 1500, "w": 300, "rot": 160, "credit": AIL, "anim": "fade", "delay": .8, "blur": [0, 3, 1.2, 3]}],
     [], {"spot_y": 1280},
     "شکلات رنگی در نور و بلندگوی خاموشِ وارونه در گوشه = شرکت بزرگ شد بی‌آن‌که فریاد بزند"),
    ("S8", "primary", ["film"], "fact",
     [], [{"type": "filmstrip", "y": 1270, "h": 300, "rot": -7, "speed": 150, "words": "FILMWORDS", "size": 50}],
     {"flash": True, "shake": [0.05, 8], "wipe": "iris"},
     "نوار فیلم که از قاب رد می‌شود (لحظه‌ی چرخش، drop) = زندگی او حالا روی پرده‌ی سینماست"),
    ("S9", "paper", ["rt"], "quote",
     [], [{"type": "slam", "text": "SLAM", "x": 540, "y": 1260, "size": 150, "t": 1.1, "rot": -8}],
     {"shake": [1.25, 12]},
     "مهر قرمز که روی صحنه کوبیده می‌شود = حکم منتقد: «تبلیغ»"),
    ("S10", "graphite", ["rt"], "fact",
     [], [{"type": "versus", "y": 1230, "size": 180, "suffix": "%", "a": {"value": 17, "label": "CRITICS"}, "b": {"value": 90, "label": "AUDIENCE"}, "ta": .5, "tb": 1.6}],
     {"wipe": "v"},
     "دو عدد کنار هم که می‌شمارند = شکاف منتقد و تماشاگر؛ رنگ تأکید روی ۹۰"),
    ("S11", "paper", ["rt"], "interpretation",
     [{"key": "ticket", "src": O("ticket", "2026-10-31"), "x": 540, "y": 1290, "w": 640, "rot": -6, "credit": AIL, "anim": "drop", "float": 6}],
     [], {"cam": {"push": .07}},
     "بازگشت بلیت = از آگهی فرار می‌کنیم ولی برای داستان بلیت می‌خریم"),
    ("S12", "graphite", ["hco"], "interpretation",
     [{"key": "lock", "src": O("padlock", D), "x": 540, "y": 1300, "w": 440, "credit": AI, "anim": "rise", "tilt": -12, "tilt_t": 1.2}],
     [], {"spot_y": 1280},
     "قفل ورشکستگی برمی‌گردد (بستن دایره با S3) = داستانی که می‌خریم همان شکست است"),
    ("S13", "paper", [], "interpretation",
     [], [{"type": "words", "mode": "fade", "words": "LENSWORDS", "keep": "LENSKEEP", "keep_at": [540, 1260], "box": [150, 1060, 930, 1470], "size": 54, "seed": 3, "t0": 0.9}],
     {}, "ادعاهای تکراری (بهترین، شماره‌ی یک…) محو می‌شوند و فقط «اولین شکست» می‌ماند و بزرگ می‌شود = بهترین تبلیغ شاید همان چیزی باشد که پنهانش می‌کنید"),
    ("S14", "primary", [], "interpretation", [], [], {"logo": True, "txt_top": 1080}, "کارت پایانی"),
]

TXT = {
 "fa": {
  "S1": [("بنیان‌گذار هرشی تبلیغ نمی‌کرد.", "b"), ("حالا مردم برای *تبلیغش* بلیت می‌خرند.", "h")],
  "S2": [("جمله‌ی خودش این بود:", "b"), ("«کیفیت بدهید؛ بهترین *تبلیغ* همین است.»", "h")],
  "S3": [("ولی قبل از شکلات،", "b"), ("اول *ورشکست* شد.", "h")],
  "S4": [("اولین مغازه‌ی شیرینی‌اش شکست خورد.", "b"), ("دومی هم *شکست* خورد.", "h")],
  "S5": [("بعد یک فکر ساده:", "b"), ("کارامل با *شیر تازه*.", "h")],
  "S6": [("کارخانه‌ی کاراملش را فروخت", "b"), ("و همه را روی *شکلات* گذاشت.", "h")],
  "S7": [("شرکتش سریع بزرگ شد،", "b"), ("بی‌آن‌که *تبلیغ* کند.", "h")],
  "S8": [("حالا، بیش از صد سال بعد،", "b"), ("زندگی‌اش روی *پرده‌ی سینما* است.", "h")],
  "S9": [("شرکت خودش در ساختنش شریک بود.", "b"), ("یک منتقد نوشت: *تبلیغی* به‌اندازه‌ی یک فیلم.", "h")],
  "S10": [("امتیازهای اولیه:", "b"), ("ولی *تماشاگرها* دوستش داشتند.", "h")],
  "S11": [("از آگهی فرار می‌کنیم،", "b"), ("ولی برای *داستان* بلیت می‌خریم.", "h")],
  "S12": [("و داستانی که می‌خریم،", "b"), ("*شکست* است، نه ادعا.", "h")],
  "S13": [("شکستی که پنهانش می‌کنید", "b"), ("شاید بهترین *تبلیغ* شما باشد.", "h")],
  "S14": [("برای من بنویسید.", "b")],
  "TL": [{"label": "فیلادلفیا", "note": "شکست"}, {"label": "نیویورک", "note": "شکست"}, {"label": "لنکستر", "note": "کارامل"}],
  "COUNTER": {"prefix": "", "suffix": " میلیون دلار", "to": 1, "label": "۱۹۰۰", "size": 150},
  "FILMWORDS": ["۱۸۷۶", "۱۹۰۰", "۲۰۲۶"],
  "SLAM": "تبلیغ؟",
  "CRITICS": "منتقدها", "AUDIENCE": "تماشاگرها",
  "LENSWORDS": ["بهترین", "شماره‌ی یک", "اولین شکست", "بی‌رقیب", "کیفیت برتر"],
  "TICKETWORD": "ورودی سینما",
  "LENSKEEP": ["اولین شکست"],
 },
 "en": {
  "S1": [("Hershey's founder refused to advertise.", "b"), ("Now people buy *tickets* to watch his ad.", "h")],
  "S2": [("His rule:", "b"), ("“Give them quality. That's the best kind of *advertising*.”", "h")],
  "S3": [("But before the chocolate,", "b"), ("he went *broke*.", "h")],
  "S4": [("His first candy shop failed.", "b"), ("So did the *second*.", "h")],
  "S5": [("Then one simple idea:", "b"), ("caramels made with *fresh milk*.", "h")],
  "S6": [("He sold the caramel company", "b"), ("and bet it all on *chocolate*.", "h")],
  "S7": [("The company grew fast", "b"), ("while he *refused* to advertise.", "h")],
  "S8": [("Now, over a century later,", "b"), ("his life is on the *big screen*.", "h")],
  "S9": [("His company helped make it.", "b"), ("One critic called it feature-length *product placement*.", "h")],
  "S10": [("Early scores:", "b"), ("Audiences *loved* it.", "h")],
  "S11": [("We skip ads.", "b"), ("We buy *tickets* for stories.", "h")],
  "S12": [("And the story we pay for", "b"), ("is the *failure*, not the boast.", "h")],
  "S13": [("The failure you hide", "b"), ("might be your best *ad*.", "h")],
  "S14": [("Write to me.", "b")],
  "TL": [{"label": "Philadelphia", "note": "failed"}, {"label": "New York", "note": "failed"}, {"label": "Lancaster", "note": "caramels"}],
  "COUNTER": {"prefix": "$", "suffix": "", "to": 1000000, "comma": True, "label": "1900", "size": 170},
  "FILMWORDS": ["1876", "1900", "2026"],
  "SLAM": "AD?",
  "CRITICS": "critics", "AUDIENCE": "audiences",
  "LENSWORDS": ["the best", "No. 1", "our first failure", "unbeatable", "premium"],
  "TICKETWORD": "ADMIT ONE",
  "LENSKEEP": ["our first failure"],
 },
}

SOURCES = [
    {"publisher": "Marketing Dive", "title": "How Hershey strategized its brand film to be more than a 90-minute ad", "date": "2026-11-25", "url": EV["film"]["url"]},
    {"publisher": "The Hershey Company", "title": "From Story to Screen: Bringing Milton Hershey's Legacy to New Generations", "date": "2026-11", "url": "https://www.thehersheycompany.com/en_us/home/newsroom/blog/from-story-to-screen-bringing-milton-hersheys-legacy-to-new-generations.html"},
    {"publisher": "Rotten Tomatoes", "title": "Hershey (2026)", "date": "retrieved 2026-11-27", "url": EV["rt"]["url"]},
    {"publisher": "Encyclopaedia Britannica", "title": "Milton Snavely Hershey", "date": "retrieved 2026-11-27", "url": EV["brit"]["url"]},
    {"publisher": "The Hershey Company", "title": "Milton Hershey", "date": "retrieved 2026-11-27", "url": EV["hco"]["url"]},
    {"publisher": "Biography.com", "title": "Milton Hershey", "date": "2026-11-24", "url": EV["bio"]["url"]},
]

CAP = {
 "fa": """بنیان‌گذار هرشی تبلیغ نمی‌کرد. حالا مردم برای تبلیغش بلیت سینما می‌خرند.

میلتون هرشی می‌گفت: «کیفیت بدهید؛ بهترین تبلیغ دنیا همین است.» شرکتش هم با این‌که تبلیغ نمی‌کرد سریع بزرگ شد. ولی قبل از شکلات، دو کسب‌وکار شیرینی‌اش (فیلادلفیا و نیویورک) شکست خوردند و اولی به ورشکستگی کشید. بعد کارامل با شیر تازه گرفت، در ۱۹۰۰ کارخانه‌ی کاراملش را یک میلیون دلار فروخت و همه را روی شکلات گذاشت.

این هفته فیلم «هرشی» به سینماها آمد؛ فیلمی که شرکت‌ها و نهادهای هرشی در ساختنش همکاری کردند. یک منتقد هالیوود ریپورتر آن را «جاگذاری محصول به‌اندازه‌ی یک فیلم» خواند. امتیاز اولیه‌ی منتقدها ۱۷٪ است و تماشاگرها ۹۰٪.

به نظر من درسش این است: مردم از آگهی فرار می‌کنند ولی برای داستان پول می‌دهند، و داستانی که می‌خرند معمولاً شکست است، نه ادعای «ما بهترینیم».

حدودش: امتیازها اولیه‌اند و نمونه کوچک است (۱۸ نقد و بیش از ۱۰۰ امتیاز تماشاگر تا ۲۷ نوامبر) و تغییر می‌کنند. آمار فروش بلیت پیدا نکردم و بودجه یا سرمایه‌گذار فیلم در منابعی که خواندم نیامده. «تبلیغ نمی‌کرد» نظر و روش خودش بود؛ شرکت از راه‌های غیرمعمول، مثل ماشین تحویل رنگ‌شده، دیده می‌شد. منابع: Marketing Dive، وبلاگ و تاریخچه‌ی رسمی هرشی، Rotten Tomatoes، بریتانیکا، Biography.com. اشیای ریل با هوش مصنوعی ساخته شده‌اند.

شکستی که برندتان پنهانش می‌کند چیست؟ برای من بنویسید.

— بهنود کاویان""",
 "en": """Hershey's founder refused to advertise. Now people buy cinema tickets to watch his ad.

Milton Hershey's rule was simple: "Give them quality. That's the best kind of advertising in the world." His company grew fast while he refused to advertise. But before the chocolate came failure: his first candy business in Philadelphia ended in bankruptcy, and a second attempt in New York failed too. Then fresh-milk caramels worked. In 1900 he sold the caramel company for $1 million and bet it all on chocolate.

This week a film about his life opened in cinemas, made in partnership with the Hershey entities. The Hollywood Reporter's critic called it "feature-length product placement." Early scores: 17% from critics, 90% from audiences.

My take: we skip ads, but we pay for stories. And the story people pay for is rarely "we're the best." It's the part where you went broke.

Limits: the scores are early and small (18 reviews, 100+ audience ratings as of 27 Nov) and will move. I found no box office figures, and none of the sources I read name the film's budget or funder. "Refused to advertise" was his stance; the company still promoted itself in unusual ways, like a painted delivery car. Sources: Marketing Dive, Hershey's official blog and history, Rotten Tomatoes, Britannica, Biography.com. Objects in the reel are AI-generated.

What failure is your brand hiding? Write to me.

— Behnood Kavian""",
}

HT = {"fa": ["#برندینگ", "#بازاریابی", "#hershey", "#storytelling"], "en": ["#branding", "#marketing", "#hersheys", "#brandstorytelling"]}
COVER = {
 "fa": {"bg": "graphite", "kicker": "راز شکلات هرشی", "title": ["تبلیغ نمی‌کرد،", "حالا *فیلم* شد"]},
 "en": {"bg": "graphite", "kicker": "The secret behind Hershey's", "title": ["He refused ads.", "Now he's *a film*."]},
}


def sub(v, T):
    if isinstance(v, str) and v in T: return copy.deepcopy(T[v])
    if isinstance(v, list): return [sub(x, T) for x in v]
    if isinstance(v, dict): return {k: sub(x, T) for k, x in v.items()}
    return v


def build(lang):
    T = TXT[lang]; scenes = []
    for sid, bg, ev, ct, objs, fx, ex, why in PLAN:
        fxs = []
        for f in fx:
            f = sub(f, T)
            if f.get("type") == "counter":
                c = T["COUNTER"]; f.update({k: c[k] for k in c if k != "size"}); f["size"] = c["size"]; f["max"] = c["to"]; f.pop("COUNTER", None)
            if f.get("type") == "versus":
                f["a"]["label"] = T["CRITICS"]; f["b"]["label"] = T["AUDIENCE"]
            if f.get("type") == "slam": f["text"] = T["SLAM"]
            fxs.append(f)
        sc = {"id": sid, "bg": bg, "claim_type": ct, "evidence": [EV[k] for k in ev], "motion_rationale": why,
              "lines": [{"text": t, "kind": k, "dim": False} for t, k in T[sid]]}
        if objs:
            sc["objects"] = copy.deepcopy(objs)
            for o in sc["objects"]:
                if o["w"] < 600 and not o.pop("noscale", False): o["w"] = round(o["w"] * 1.18)
                o["y"] = o["y"] - 50
            for f in fxs:
                if f.get("type") == "labels":
                    for it in f["items"]: it["y"] -= 50
        if fxs: sc["fx"] = fxs
        sc.update(copy.deepcopy(ex))
        scenes.append(sc)
    cov = dict(COVER[lang]); cov["objects"] = [
        {"src": O("chocolate_whole", "2026-10-25"), "x": 560, "y": 1300, "w": 600, "rot": -8},
        {"src": O("ticket", "2026-10-31"), "x": 520, "y": 1220, "w": 500, "rot": 10}]
    n = "01" if lang == "fa" else "02"
    return {"reel_id": f"{D}_{lang.upper()}", "date": D, "lang": lang, "style": "editorial", "motion": "v2",
            "topic": "بنیان‌گذار هرشی تبلیغ نمی‌کرد؛ حالا زندگی‌اش فیلمی است که منتقدها آگهی می‌خوانند و تماشاگرها دوستش دارند" if lang == "fa" else "Hershey's founder refused to advertise; now his life is a film critics call product placement and audiences love",
            "pillar": "brand_storytelling_content_marketing", "format": {"w": 1080, "h": 1920, "fps": 30},
            "audio": {"mode": "generative", "mood": "dark", "drop_scene": "S8"},
            "cover": cov, "scenes": scenes, "caption": CAP[lang], "hashtags": HT[lang], "sources": SOURCES,
            "cta": "برای من بنویسید." if lang == "fa" else "Write to me.", "status": "DRAFT"}, n


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for lang in ("fa", "en"):
        r, n = build(lang)
        (here / f"reel_{n}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf8")
        print("wrote", here / f"reel_{n}.json", len(r["scenes"]), "scenes")
