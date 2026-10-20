"""Automated QA. Usage: python3 qa.py samples/sample_post.json out/<post_id>
Hard failures (critical) force BLOCKED_QA. This gate covers only what a machine can verify;
orthography judgement, prose quality and art relevance still need a reviewer (listed in `needs_human`)."""
import json, sys, pathlib, hashlib
from PIL import Image
from fontTools.ttLib import TTFont
from persian_text import normalize, lint

ROOT = pathlib.Path(__file__).parent.resolve()
CFG = json.loads((ROOT / "brand_config.json").read_text(encoding="utf8"))
W, H, M = CFG["canvas"]["width"], CFG["canvas"]["height"], CFG["canvas"]["safe_margin_px"]


def main(post_path, out_dir):
    post = json.loads(pathlib.Path(post_path).read_text(encoding="utf8"))
    out = pathlib.Path(out_dir).resolve()
    metrics = {m["slide"]: m for m in json.loads((out / "layout_metrics.json").read_text())["slides"]}
    cmaps = {n: set(TTFont(ROOT / p).getBestCmap()) for n, p in CFG["fonts"]["files"].items()}
    crit, warn, per_slide = [], [], []

    # logo integrity
    for k, v in CFG["logo"]["files"].items():
        if hashlib.sha256((ROOT / v["path"]).read_bytes()).hexdigest() != v["sha256"]:
            crit.append(f"logo[{k}] hash mismatch")
    if not CFG["logo"]["confirmed_by_owner"]:
        warn.append("logo not confirmed by owner (colour variants derived from the 400x877 master)")
    if "UNCONFIRMED" in CFG["fonts"]["license_status"]:
        warn.append("font licence unconfirmed")

    seen_hash = set()
    for s in post["slides"]:
        n = s["slide_number"]; m = metrics[n]; tag = f"slide {n:02d}"
        png = out / f"{n:02d}.png"
        if not png.exists():
            crit.append(f"{tag}: PNG missing"); continue
        im = Image.open(png)
        if im.size != (W, H): crit.append(f"{tag}: size {im.size} != {(W, H)}")
        if m["png_sha256"] in seen_hash: crit.append(f"{tag}: duplicate image")
        seen_hash.add(m["png_sha256"])
        # text
        text = normalize(s["headline"] + "\n" + s.get("body", ""))
        for it in lint(s["headline"] + "\n" + s.get("body", "")):
            (crit if it["severity"] == "critical" else warn).append(f"{tag}: {it['message']} «{it['context']}»")
        missing = {c for c in text if not c.isspace() and ord(c) not in cmaps["Regular"]}
        if missing: crit.append(f"{tag}: glyphs missing in DoranFaNum: {''.join(sorted(missing))}")
        # font
        if not m["font_ok"] or any("DoranFaNum" not in f for f in m["families"]):
            crit.append(f"{tag}: font not DoranFaNum {m['families']}")
        # layout
        z = m["zone"]
        for nm in ("h", "b"):
            r = m[nm]
            if r and (r["l"] < M - 1 or r["r"] > W - M + 1 or r["b"] > z["b"] + 1):
                crit.append(f"{tag}: {nm} outside safe area")
        if m["zone_overflow"]: crit.append(f"{tag}: text overflows its zone")
        if m["h_font_px"] < CFG["fonts"]["min_size_px"]["headline"]: crit.append(f"{tag}: headline {m['h_font_px']}px below minimum")
        if m["b_font_px"] and m["b_font_px"] < CFG["fonts"]["min_size_px"]["body"]: crit.append(f"{tag}: body below minimum")
        lg = m["logo"]
        if m["h"]["b"] > lg["t"] - CFG["logo"]["clear_space_px"] or (m["b"] and m["b"]["b"] > lg["t"] - CFG["logo"]["clear_space_px"]):
            crit.append(f"{tag}: text violates logo clear space")
        nat_h = m["logo_natural"][1]; rh = lg["b"] - lg["t"]
        if rh > nat_h + 1: crit.append(f"{tag}: logo upscaled")
        if abs((lg["r"] - lg["l"]) / rh - m["logo_natural"][0] / m["logo_natural"][1]) > 0.01: crit.append(f"{tag}: logo distorted")
        if m["h_lines"] > 4: warn.append(f"{tag}: headline {m['h_lines']} lines")
        # claims
        if s["claim_type"] == "fact" and not s.get("evidence"): crit.append(f"{tag}: fact without evidence")
        per_slide.append({"slide": n, "h_font_px": m["h_font_px"], "h_lines": m["h_lines"], "b_font_px": m["b_font_px"]})

    if len(post["slides"]) != 8: crit.append("post must have exactly 8 slides")
    score = max(0, 100 - 15 * len(crit) - 2 * len(warn))
    status = "READY_FOR_REVIEW" if (not crit and score >= CFG["qa"]["mandatory_threshold"]) else "BLOCKED_QA"
    rep = {"post_id": post["post_id"], "status": status, "score": score, "critical": crit, "warnings": warn, "slides": per_slide,
           "needs_human": ["orthography and punctuation judgement", "prose clarity (Ashouri)", "factual claims vs sources", "art relevance and non-repetition", "phone-size readability check"]}
    (out / "qa_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf8")
    print(json.dumps({k: rep[k] for k in ("status", "score", "critical", "warnings")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
