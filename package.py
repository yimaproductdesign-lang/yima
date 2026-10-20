"""Package two rendered+QA'd posts into the delivery contract.
Usage: python3 package.py DATE post1.json post2.json   (renders must exist in out/<post_id>/, qa_report.json beside them)"""
import sys, json, shutil, zipfile, pathlib
date, p1, p2 = sys.argv[1], sys.argv[2], sys.argv[3]
root = pathlib.Path("out").resolve(); dest = root / date
if dest.exists(): shutil.rmtree(dest)
dest.mkdir(parents=True)
caps, refs, qa, ok = [], {}, {}, True
for i, pp in enumerate((p1, p2), 1):
    post = json.loads(pathlib.Path(pp).read_text(encoding="utf8")); pid = post["post_id"]
    src = root / pid; rep = json.loads((src / "qa_report.json").read_text(encoding="utf8"))
    d = dest / f"Post_{i:02d}"; d.mkdir()
    for n in range(1, 9): shutil.copy(src / f"{n:02d}.png", d / f"{n:02d}.png")
    qa[pid] = rep; ok &= rep["status"] == "READY_FOR_REVIEW"
    refs[pid] = [e for s in post["slides"] for e in s.get("evidence", [])]
    caps.append(f"# Post {i:02d} — {post['topic']}\n\n{post['caption']}\n\n**CTA:** {post.get('cta','')}\n\n**Alt text:**\n" + "\n".join(f"{k}. {t}" for k, t in enumerate(post["alt_text"], 1)))
    with zipfile.ZipFile(dest / f"Post_{i:02d}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.glob("*.png")): z.write(f, f"Post_{i:02d}/{f.name}")
(dest / "captions.md").write_text("\n\n---\n\n".join(caps), encoding="utf8")
(dest / "references.json").write_text(json.dumps(refs, ensure_ascii=False, indent=1), encoding="utf8")
(dest / "qa_report.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf8")
status = "READY_FOR_REVIEW" if ok else "BLOCKED_QA"
(dest / "manifest.json").write_text(json.dumps({"date": date, "status": status, "posts": list(qa)}, indent=1), encoding="utf8")
with zipfile.ZipFile(dest / "FULL_PACKAGE.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(dest.rglob("*")):
        if f.is_file() and f.name != "FULL_PACKAGE.zip": z.write(f, f.relative_to(dest))
print(status, dest)
