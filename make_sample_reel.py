"""Builds samples/sample_reel.json from the calibrated money-and-personality copy (typography + vector motifs only)."""
import json, pathlib
post = json.loads(pathlib.Path("drafts/2026-10-21/post_01.json").read_text(encoding="utf8"))
ev = [e for s in post["slides"] for e in s.get("evidence", [])]
L = lambda text, t, kind="h", dim=False: {"text": text, "t": t, "kind": kind, "dim": dim}
scenes = [
 {"id": "S1", "start": 0.0,  "end": 3.0,  "bg": "primary", "lines": [L("پول آدم را عوض می‌کند.", .3)], "motif": {"type": "grid", "params": {"path": [5]}}},
 {"id": "S2", "start": 3.0,  "end": 6.6,  "bg": "primary", "lines": [L("اما نه آن‌طور که فکر می‌کنید.", .2)], "motif": {"type": "grid", "params": {"path": [5, 6, 10]}}},
 {"id": "S3", "start": 6.6,  "end": 10.8, "bg": "paper",   "lines": [L("یازده پژوهش.", .2), L("پنج کشور.", .9), L("تا ۱۳۴ هزار شاغل.", 1.6, dim=True)], "motif": {"type": "cloud", "params": {"n": 420}}, "claim_type": "fact"},
 {"id": "S4", "start": 10.8, "end": 14.8, "bg": "primary", "lines": [L("منظم‌تر شدیم.", .2), L("آرام‌تر هم.", 1.3, dim=True)], "motif": {"type": "ring", "params": {}}, "claim_type": "fact"},
 {"id": "S5", "start": 14.8, "end": 19.4, "bg": "paper",   "lines": [L("این دگرگونی نیست؛ نجواست.", .2), L("بزرگ‌ترین اثر حدود شش صدم بود.", 1.8, "b", dim=True)], "motif": {"type": "whisper", "params": {}}, "claim_type": "fact"},
 {"id": "S6", "start": 19.4, "end": 23.8, "bg": "primary", "lines": [L("پول آدم را وارونه نمی‌کند.", .2), L("فقط بی‌صدا", 1.5, dim=True), L("جابه‌جایش می‌کند.", 2.2, dim=True)], "motif": {"type": "shift", "params": {}}, "claim_type": "interpretation"},
 {"id": "S7", "start": 23.8, "end": 29.0, "bg": "paper",   "lines": [{**L("اگر درآمدتان دو برابر شود،", .2, dim=True), "size": 84}, L("کدام ویژگی‌تان را به هیچ قیمتی نمی‌دهید؟", 1.5)], "motif": {"type": "steps", "params": {}}, "claim_type": "question"},
 {"id": "S8", "start": 29.0, "end": 32.0, "bg": "primary", "lines": [L("برای ما بنویسید.", .9, "b")], "logo": True, "txt_top": 1080}]
for s in scenes: s.setdefault("claim_type", "interpretation"); s["evidence"] = ev if s["claim_type"] == "fact" else []
reel = {"reel_id": "TEST_REEL_01", "date": "2026-10-21", "topic": post["topic"], "pillar": post["pillar"], "format": {"w": 1080, "h": 1920, "fps": 30},
        "scenes": scenes, "caption": post["caption"], "cta": post["cta"], "audio": {"mode": "synth_sfx", "note": "Add licensed or trending music in Instagram."}, "status": "DRAFT"}
pathlib.Path("samples").mkdir(exist_ok=True)
pathlib.Path("samples/sample_reel.json").write_text(json.dumps(reel, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(scenes))
