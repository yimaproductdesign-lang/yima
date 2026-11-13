"""Hook cover for a reel (owner, 2026-11-13: «ریل‌ها کاوری که قلابشان کند ندارند»).

Usage: python3 cover_render.py <reel.json> <out_dir> [--prepend]
- Reads reel["cover"]: {"bg": "paper|graphite|primary", "kicker": "...", "title": ["line", "line"],
  "objects": [{"src": ..., "x": 540, "y": 1240, "w": 560, "rot": 0, "frame": false, "ar": 1.0}]}
  *word* in title = accent + underline (max two).
- Writes out/<reel_id>/cover.png (1080x1920). Text and objects sit inside the profile-grid crop
  (3:4, y 240-1680) so the hook is readable both full-screen and in the grid.
- --prepend: puts the cover as the first 0.4 s of out/<reel_id>/<reel_id>.mp4 (frame 0 = hook, audio shifted),
  so the feed / trial-reel thumbnail is never an empty first frame.
"""
import json, sys, pathlib, subprocess, html, re
from playwright.sync_api import sync_playwright
from persian_text import normalize
from reel_render import font_css, THEME, W, H, FPS

HOLD = 0.4
GRID = (240, 1680)


def esc_line(t):
    parts = re.split(r"(\*[^*]+\*)", t)
    return "".join(f'<span class="em">{html.escape(p[1:-1])}</span>' if p.startswith("*") else html.escape(p) for p in parts if p)


def page(reel):
    c = reel["cover"]; lang = reel.get("lang", "fa"); th = THEME[c.get("bg", "paper")]
    rtl = lang == "fa"; fam = "'DoranFaNum'" if rtl else "'BrandLatin'"
    nz = (lambda s: normalize(s)) if rtl else (lambda s: s)
    acc = "#356C7C" if c.get("bg", "paper") == "paper" else "#8FB8C4"
    dark = c.get("bg", "paper") != "paper"
    bgfx = ("radial-gradient(ellipse 70% 40% at 50% 66%, rgba(255,255,255,.10), rgba(0,0,0,0) 70%)" if dark else
            "radial-gradient(ellipse at 50% 55%, rgba(255,255,255,.6) 0%, rgba(0,0,0,0) 60%, rgba(0,0,0,.08) 100%)")
    objs = "".join(
        f'<img class="o{" fr" if o.get("frame") else ""}" src="{(pathlib.Path(o["src"]).resolve()).as_uri()}" '
        f'style="left:{o.get("x", 540)}px;top:{o.get("y", 1240)}px;width:{o.get("w", 560)}px;'
        f'{"height:%dpx;object-fit:cover;" % round(o.get("w", 560) / o["ar"]) if o.get("ar") else ""}'
        f'transform:translate(-50%,-50%) rotate({o.get("rot", 0)}deg)">' for o in c.get("objects", []))
    lines = "".join(f'<div class="t">{esc_line(nz(t))}</div>' for t in c["title"])
    return f"""<!doctype html><html dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf8"><style>
{font_css()}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:{th['bg']}}}
#bg{{position:absolute;inset:0;background:{bgfx}}}
#col{{position:absolute;left:96px;right:96px;top:300px;font-family:{fam};color:{th['fg']};text-align:start}}
.k{{font-size:54px;font-weight:500;opacity:.78;margin-bottom:26px;white-space:nowrap;width:max-content}}
.t{{font-weight:800;line-height:1.08;white-space:nowrap;width:max-content;max-width:none;letter-spacing:{'0' if rtl else '-0.02em'}}}
.em{{color:{acc};text-decoration:underline;text-decoration-thickness:9px;text-underline-offset:{'22px' if rtl else '14px'}}}
.o{{position:absolute;filter:drop-shadow(0 34px 34px rgba(0,0,0,{'.55' if dark else '.22'}))}}
.o.fr{{border-radius:20px;filter:none;box-shadow:0 40px 70px rgba(0,0,0,.45)}}
</style></head><body><div id="bg"></div>{objs}<div id="col"><div class="k">{html.escape(nz(c.get('kicker', '')))}</div>{lines}</div>
<script>
// one size for all title lines: the largest that keeps every line inside the column (max 168px); called after fonts load
window.doFit=()=>{{const ts=[...document.querySelectorAll('.t')];let s=168;
const fit=()=>ts.every(t=>t.getBoundingClientRect().width<=888);
while(s>80){{ts.forEach(t=>t.style.fontSize=s+'px');if(fit())break;s-=2;}}
const k=document.querySelector('.k');let ks=54;k.style.fontSize=ks+'px';while(k.getBoundingClientRect().width>888&&ks>36){{ks-=2;k.style.fontSize=ks+'px';}}
return {{size:s,bottom:document.getElementById('col').getBoundingClientRect().bottom,
  objs:[...document.querySelectorAll('.o')].map(o=>{{const r=o.getBoundingClientRect();return [r.top,r.bottom]}})}};}};
</script></body></html>"""


def main(reel_path, out_dir, prepend=False):
    reel = json.loads(pathlib.Path(reel_path).read_text(encoding="utf8"))
    out = pathlib.Path(out_dir).resolve() / reel["reel_id"]; out.mkdir(parents=True, exist_ok=True)
    (out / "cover.html").write_text(page(reel), encoding="utf8")
    with sync_playwright() as pw:
        exe = "/opt/pw-browsers/chromium"
        br = pw.chromium.launch(executable_path=exe) if pathlib.Path(exe).exists() else pw.chromium.launch()
        pg = br.new_context(viewport={"width": W, "height": H}).new_page()
        pg.goto((out / "cover.html").as_uri())
        pg.evaluate("Promise.all([500,800].flatMap(w=>[document.fonts.load(`${w} 80px BrandLatin`,'Brand $148'),document.fonts.load(`${w} 80px DoranFaNum`,'کش مو ۱۴۸')]))")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        m = pg.evaluate("window.doFit()"); pg.wait_for_timeout(100); pg.screenshot(path=str(out / "cover.png")); br.close()
    issues = []
    if m["size"] < 110: issues.append(f"title only {m['size']}px; shorten the hook")
    if m["bottom"] > GRID[1]: issues.append("title runs below the grid crop")
    for t, b in m["objs"]:
        if t < m["bottom"] + 20: issues.append("object overlaps the title")
        if b > GRID[1]: issues.append("object runs below the grid crop")
    (out / "cover_metrics.json").write_text(json.dumps({**m, "issues": issues}, indent=1), encoding="utf8")
    print("cover", out / "cover.png", f"title {m['size']}px", "OK" if not issues else issues)
    if prepend:
        mp4 = out / f"{reel['reel_id']}.mp4"; tmp = out / "_with_cover.mp4"
        ms = int(HOLD * 1000)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(HOLD), "-framerate", str(FPS), "-i", str(out / "cover.png"), "-i", str(mp4),
                        "-filter_complex", f"[0:v]scale={W}:{H},format=yuv420p,setsar=1[c];[1:v]setsar=1[v];[c][v]concat=n=2:v=1:a=0[vo];"
                                           f"[1:a]adelay={ms}|{ms}[ao]",
                        "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp)], check=True)
        tmp.replace(mp4); print("prepended cover", HOLD, "s ->", mp4)
    return issues


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2], "--prepend" in sys.argv) else 0)
