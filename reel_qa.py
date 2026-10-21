"""Automated reel QA. Usage: python3 reel_qa.py samples/sample_reel.json out/<reel_id>
Machine-checkable gates only; prose quality, motion taste and factual accuracy still need a human (see needs_human)."""
import json, sys, pathlib, subprocess, hashlib
from fontTools.ttLib import TTFont
from persian_text import normalize, lint

ROOT = pathlib.Path(__file__).parent.resolve()
CFG = json.loads((ROOT / "brand_config.json").read_text(encoding="utf8"))
P = CFG["palette"]


def lum(h):
    r = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in r]
    return .2126 * r[0] + .7152 * r[1] + .0722 * r[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


THEME = {"primary": (P["primary"], P["paper"], P["slate"]), "graphite": (P["graphite"], P["paper"], P["slate"]), "paper": (P["paper"], P["graphite"], P["teal"])}


def main(reel_path, out_dir):
    reel = json.loads(pathlib.Path(reel_path).read_text(encoding="utf8"))
    out = pathlib.Path(out_dir).resolve(); rid = reel["reel_id"]
    met = json.loads((out / "reel_metrics.json").read_text()); S = met["safe"]
    cmap = set(TTFont(ROOT / CFG["fonts"]["files"]["Regular"]).getBestCmap())
    crit, warn = [], []
    mp4 = out / f"{rid}.mp4"
    if not mp4.exists(): crit.append("mp4 missing"); mp4 = None
    if mp4:
        pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(mp4)], capture_output=True, text=True).stdout)
        v = next((s for s in pr["streams"] if s["codec_type"] == "video"), None); a = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
        if not v or (v["width"], v["height"]) != (1080, 1920): crit.append(f"video size {v and (v['width'], v['height'])}")
        if v and (v["codec_name"] != "h264" or v["pix_fmt"] != "yuv420p"): crit.append("video must be h264 yuv420p")
        if v and eval(v["r_frame_rate"]) not in (30.0,): crit.append(f"fps {v['r_frame_rate']}")
        if not a: crit.append("no audio stream")
        d = float(pr["format"]["duration"])
        if not (30 <= d <= 75): crit.append(f"duration {d:.1f}s outside 30-75s")
        elif not (40 <= d <= 60): warn.append(f"duration {d:.1f}s outside the 40-60s target")
        if int(pr["format"]["size"]) > 90 * 2 ** 20: crit.append("file larger than 90MB")
        vd = subprocess.run(["ffmpeg", "-i", str(mp4), "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
        mx = float(vd.split("max_volume:")[1].split("dB")[0]); mean = float(vd.split("mean_volume:")[1].split("dB")[0])
        if mx > -1: crit.append(f"audio clipping risk (peak {mx} dB)")
        if mean < -35: crit.append(f"audio too quiet (mean {mean} dB)")
    for sc, m in zip(reel["scenes"], met["scenes"]):
        tag = sc["id"]; ws = m["words"]
        if not m["font_ok"] or any("DoranFaNum" not in f for f in m["fonts"]): crit.append(f"{tag}: font is not DoranFaNum")
        for w in ws:
            if w["l"] < S["x0"] - 1 or w["r"] > S["x1"] + 1 or w["t"] < S["y0"] or w["b"] > S["y1"]: crit.append(f"{tag}: word «{w['w']}» outside Reels safe area"); break
        if m["fit"] < 0.7: crit.append(f"{tag}: text shrunk to {m['fit']:.2f} to fit; shorten it")
        if min(w["fs"] for w in ws) < 44 if ws else False: crit.append(f"{tag}: font below 44px (phone readability)")
        dur = m["end"] - m["start"]
        if dur < 2.2: crit.append(f"{tag}: scene shorter than 2.2s")
        lastin = max((w["tt"] for w in ws), default=0)
        if ws and lastin + .42 > dur - .8: crit.append(f"{tag}: less than 0.8s hold after last word")
        if ws and len(ws) / dur > 3.2: crit.append(f"{tag}: {len(ws) / dur:.1f} words/s too fast to read")
        bgc, fg, dim = THEME[sc["bg"]]
        if ratio(bgc, fg) < 4.5: crit.append(f"{tag}: fg contrast {ratio(bgc, fg):.2f}")
        if any(l.get("dim") for l in sc.get("lines", [])) and ratio(bgc, dim) < 4.0: crit.append(f"{tag}: dim contrast {ratio(bgc, dim):.2f}")
        # orphan rows
        for li in {w["li"] for w in ws}:
            row = [w for w in ws if w["li"] == li]; ts = sorted(w["t"] for w in row); tops = [ts[0]]
            for x in ts[1:]:
                if x - tops[-1] > 40: tops.append(x)
            if len(row) >= 3 and len(tops) >= 2 and sum(1 for w in row if w["t"] > tops[-1] - 40) == 1: warn.append(f"{tag}: line {li + 1} ends with a single-word row")
        for ln in sc.get("lines", []):
            txt = normalize(ln["text"]).replace("*", "")
            for it in lint(ln["text"].replace("*", "")): (crit if it["severity"] == "critical" else warn).append(f"{tag}: {it['message']} «{it['context']}»")
            miss = {c for c in txt if not c.isspace() and ord(c) not in cmap}
            if miss: crit.append(f"{tag}: glyphs missing {''.join(sorted(miss))}")
        if sc.get("claim_type") == "fact" and not sc.get("evidence"): crit.append(f"{tag}: fact without evidence")
        if sc.get("logo") and m["logo"]:
            lg = m["logo"]; rh = lg["b"] - lg["t"]
            if rh <= 0 or not lg["nh"]: crit.append(f"{tag}: logo not loaded"); continue
            if rh > lg["nh"] + 1: crit.append(f"{tag}: logo upscaled")
            if abs((lg["r"] - lg["l"]) / rh - lg["nw"] / lg["nh"]) > .01: crit.append(f"{tag}: logo distorted")
    # motion semantics: every motif needs a reason; variety; no mechanical repetition
    mot = [(s.get("motif") or {}) for s in reel["scenes"]]
    for s, m in zip(reel["scenes"], mot):
        if m and len(s.get("motion_rationale", "").strip()) < 8: crit.append(f"{s['id']}: motif without motion_rationale")
    types = [m.get("type") for m in mot if m]
    if len(set(types)) < 5: crit.append(f"only {len(set(types))} distinct motifs; need >= 5 for a 40-60s reel")
    for i in range(2, len(mot)):
        a, b, c = mot[i - 2], mot[i - 1], mot[i]
        if a and b and c and a.get("type") == b.get("type") == c.get("type") and not (a.get("group") and a.get("group") == b.get("group") == c.get("group")):
            warn.append(f"{reel['scenes'][i]['id']}: same motif three scenes in a row")
    for it in lint(reel.get("caption", "")):
        if "امارات" in it["message"]: crit.append(f"caption: {it['message']}")
    for k, v in CFG["logo"]["files"].items():
        if hashlib.sha256((ROOT / v["path"]).read_bytes()).hexdigest() != v["sha256"]: crit.append(f"logo[{k}] hash mismatch")
    if not any(s.get("logo") for s in reel["scenes"]): crit.append("no logo end card")
    for sc, m in zip(reel["scenes"], met["scenes"]):
        if sc.get("logo"):
            sg = m.get("sig")
            if not sg or sg["text"] != CFG["signature"]["text"]: crit.append(f"{sc['id']}: signature «{CFG['signature']['text']}» missing on end card")
            elif sg["b"] > S["y1"] or "DoranFaNum" not in sg["font"]: crit.append(f"{sc['id']}: signature outside safe area or wrong font")
            if not any("برای من بنویسید" in l["text"] for l in sc.get("lines", [])): warn.append(f"{sc['id']}: end card CTA should be «برای من بنویسید.»")
    score = max(0, 100 - 15 * len(crit) - 2 * len(warn))
    status = "READY_FOR_REVIEW" if not crit and score >= CFG["qa"]["mandatory_threshold"] else "BLOCKED_QA"
    rep = {"reel_id": rid, "status": status, "score": score, "critical": crit, "warnings": warn,
           "needs_human": ["watch and listen to the full reel on a phone", "Persian copy quality and orthography", "facts vs sources", "motion taste and pacing", "sourced imagery rights (if any)"]}
    (out / "qa_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf8")
    print(json.dumps({k: rep[k] for k in ("status", "score", "critical", "warnings")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
