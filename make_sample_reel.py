"""Builds samples/sample_reel.json: content-timed reel (no hand-set times) with meaning-matched motion."""
import json, pathlib
post = json.loads(pathlib.Path("drafts/2026-10-21/post_01.json").read_text(encoding="utf8"))
ev = [e for s in post["slides"] for e in s.get("evidence", [])]
L = lambda text, kind="h", dim=False, **k: {"text": text, "kind": kind, "dim": dim, **k}
S = [  # id, bg, lines, motif, claim_type, why this motion
 ("S1", "primary", [L("پول آدم را *عوض* می‌کند.")], {"type": "grid", "group": "g1", "params": {"path": [5, 6, 10], "hop_t": 3.0}}, "interpretation", "یک نقطه‌ی برجسته میان نقطه‌های هم‌شکل: «یک نفر» در میان جمع"),
 ("S2", "primary", [L("اما نه آن‌طور که فکر می‌کنید.")], {"type": "grid", "group": "g1"}, "interpretation", "همان نقطه جابه‌جا می‌شود، ولی آرام؛ ایده‌ی «تغییر» پیش از «اندازه‌ی تغییر»"),
 ("S3", "paper", [L("در فیلم‌ها، پول آدم را *یک‌شبه* عوض می‌کند.")], {"type": "split", "params": {}}, "metaphor", "دوپاره‌شدن ناگهانی = تغییر یک‌شبه‌ی افسانه‌ای"),
 ("S4", "paper", [L("واقعیت چیز دیگری است.", dim=True)], {"type": "focus", "params": {}}, "interpretation", "حلقه‌ها جمع می‌شوند؛ نگاه از افسانه به داده"),
 ("S5", "primary", [L("یازده پژوهش.", ), L("پنج کشور."), L("تا ۱۳۴ هزار شاغل.", dim=True)], {"type": "cloud", "params": {"n": 420}}, "fact", "ابر نقطه‌ها = مقیاس نمونه؛ یک نقطه‌ی برجسته = یک آدم"),
 ("S6", "paper", [L("وقتی درآمد بالا می‌رود،", "b"), L("آدم چه می‌شود؟")], {"type": "journey", "params": {}}, "question", "نقطه‌ای که روی منحنی بالا می‌رود = رشد درآمد؛ مقصد = پرسش"),
 ("S7", "primary", [L("*منظم‌تر* شدیم."), L("*آرام‌تر* هم.", dim=True)], {"type": "converge", "params": {}}, "fact", "نقطه‌های پراکنده به شبکه‌ی منظم می‌رسند = نظم"),
 ("S8", "paper", [L("در عوض، کمی کمتر اجتماعی."), L("کمی کمتر سازگار.", dim=True)], {"type": "network", "params": {}}, "fact", "پیوندها کم‌رنگ و گره‌ها دورتر می‌شوند"),
 ("S9", "primary", [L("این دگرگونی نیست؛ *نجواست.*"), L("بزرگ‌ترین اثر حدود شش صدم بود.", "b", dim=True)], {"type": "whisper", "params": {}}, "fact", "منحنی بزرگ نقطه‌چین (انتظار ما) در برابر برآمدگی کوچک (واقعیت)"),
 ("S10", "paper", [L("و یک چیز را هیچ‌کس نمی‌داند:", "b"), L("پول ما را عوض کرده، یا آدم‌های منظم‌تر پول بیشتری درمی‌آورند؟")], {"type": "loop", "params": {}}, "interpretation", "دو نقطه که یکدیگر را دنبال می‌کنند = علت و معلولِ دورانی"),
 ("S11", "primary", [L("پول آدم را وارونه نمی‌کند."), L("فقط *بی‌صدا* جابه‌جایش می‌کند.", dim=True)], {"type": "shift", "params": {}}, "interpretation", "نقطه‌ی درونی کمی جابه‌جا می‌شود؛ جای قبلی نقطه‌چین می‌ماند"),
 ("S12", "paper", [L("نمونه‌ها فقط از چند کشور ثروتمند غربی‌اند.", "b"), L("پس این داستان هنوز *تمام* نشده.")], {"type": "noise", "params": {}}, "fact", "سیگنال آشفته که آرام می‌شود = حدِ دانسته‌ها را صادقانه گفتن"),
 ("S13", "primary", [L("سه ماه بعد از هر افزایش حقوق،"), L("از خودتان بپرسید:", dim=True)], {"type": "clock", "params": {}}, "interpretation", "یک‌چهارم ساعت = سه ماه"),
 ("S14", "paper", [L("کدام عادت‌تان *محکم‌تر* شد؟"), L("کدام رابطه *کم‌رنگ‌تر؟*")], {"type": "balance", "params": {}}, "question", "ترازو: دو کفه‌ی «به‌دست‌آمده» و «از‌دست‌رفته»"),
 ("S15", "primary", [L("اگر درآمدتان دو برابر شود،", "b", dim=True), L("کدام ویژگی‌تان را به *هیچ* قیمتی نمی‌دهید؟")], {"type": "steps", "params": {}}, "question", "پله‌های رشد؛ آخرین پله = دو برابر شدن درآمد"),
 ("S16", "primary", [L("برای من بنویسید.", "b")], None, "interpretation", "کارت پایانی")]
scenes = []
for id_, bg, lines, motif, ct, why in S:
    sc = {"id": id_, "bg": bg, "lines": lines, "claim_type": ct, "motion_rationale": why, "evidence": ev if ct == "fact" else []}
    if motif: sc["motif"] = motif
    if id_ == "S16": sc.update(logo=True, txt_top=1080)
    scenes.append(sc)
CAPTION = ("پول آدم را عوض می‌کند؟ تا حدی. اما نه به شکلی که در فیلم‌ها می‌بینیم.\n\n"
 "یازده پژوهش بلندمدت از پنج کشور، تا ۱۳۴ هزار شاغل، میان چهار تا بیست سال پیگیری. با بالا رفتن درآمد، مسئولیت‌پذیری و آرامش هیجانی کمی بیشتر شد و سازگاری و برونگرایی کمی کمتر. اثرها کوچک‌اند و داده‌ها نمی‌گویند پول علت است یا نتیجه. نمونه‌ها فقط از چند کشور ثروتمند غربی است.\n\n"
 "اگر درآمدتان دو برابر شود، کدام ویژگی‌تان را به هیچ قیمتی نمی‌دهید؟ برای من بنویسید.\n\n"
 "منبع: PsyPost (۲۰ اکتبر ۲۰۲۶) از مقاله‌ی Li و همکاران، Psychological Bulletin؛ متن اصلی مقاله مستقیم خوانده نشده.\n\n— بهنود کاویان\n\n#روانشناسی #شخصیت #درآمد")
reel = {"reel_id": "TEST_REEL_01", "date": "2026-10-21", "topic": post["topic"], "pillar": post["pillar"], "format": {"w": 1080, "h": 1920, "fps": 30},
        "scenes": scenes, "caption": CAPTION, "cta": post["cta"], "audio": {"mode": "synth_sfx", "note": "Add licensed or trending music in Instagram."}, "status": "DRAFT"}
pathlib.Path("samples/sample_reel.json").write_text(json.dumps(reel, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(scenes))
