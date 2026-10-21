"""Package the day's reels. Usage: python3 package_reels.py YYYY-MM-DD drafts/DATE/reel_01.json drafts/DATE/reel_02.json
Expects out/<reel_id>/<reel_id>.mp4, cover.png, qa_report.json (from reel_render.py + reel_qa.py)."""
import sys, json, shutil, zipfile, pathlib
date, paths = sys.argv[1], sys.argv[2:]
root = pathlib.Path("out").resolve(); dest = root / date
if dest.exists(): shutil.rmtree(dest)
dest.mkdir(parents=True)
caps, refs, qa, ok = [], {}, {}, True
for i, rp in enumerate(paths, 1):
    r = json.loads(pathlib.Path(rp).read_text(encoding="utf8")); rid = r["reel_id"]; src = root / rid
    d = dest / f"Reel_{i:02d}"; d.mkdir()
    shutil.copy(src / f"{rid}.mp4", d / f"Reel_{i:02d}.mp4"); shutil.copy(src / "cover.png", d / "cover.png")
    rep = json.loads((src / "qa_report.json").read_text(encoding="utf8")); qa[rid] = rep; ok &= rep["status"] == "READY_FOR_REVIEW"
    refs[rid] = [e for s in r["scenes"] for e in s.get("evidence", [])]
    caps.append(f"# Reel {i:02d} — {r['topic']}\n\n{r['caption']}\n\n(music: {(r.get('audio') or {}).get('mood')})")
    with zipfile.ZipFile(dest / f"Reel_{i:02d}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.iterdir()): z.write(f, f"Reel_{i:02d}/{f.name}")
(dest / "captions.md").write_text("\n\n---\n\n".join(caps), encoding="utf8")
(dest / "references.json").write_text(json.dumps(refs, ensure_ascii=False, indent=1), encoding="utf8")
(dest / "qa_report.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf8")
status = "READY_FOR_REVIEW" if ok else "BLOCKED_QA"
(dest / "manifest.json").write_text(json.dumps({"date": date, "status": status, "reels": list(qa)}, indent=1), encoding="utf8")
with zipfile.ZipFile(dest / "FULL_PACKAGE.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(dest.rglob("*")):
        if f.is_file() and f.suffix != ".zip": z.write(f, f.relative_to(dest))
print(status, dest)
