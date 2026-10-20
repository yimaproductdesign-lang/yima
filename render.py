"""Deterministic renderer: post JSON -> 1080x1350 PNGs (+ editable HTML + layout metrics).
Usage: python3 render.py samples/sample_post.json out/
Image models never draw text or logo; this layer does, with the real DoranFaNum files and the untouched logo PNGs.
"""
import json, sys, pathlib, hashlib, html
from playwright.sync_api import sync_playwright
from persian_text import normalize

ROOT = pathlib.Path(__file__).parent.resolve()
CFG = json.loads((ROOT / "brand_config.json").read_text(encoding="utf8"))
P, CV = CFG["palette"], CFG["canvas"]
W, H, M = CV["width"], CV["height"], CV["safe_margin_px"]
LOGO = CFG["logo"]
FOOT = LOGO["render_height_px"] + LOGO["clear_space_px"]  # reserved footer band

THEME = {  # bg, headline, body, counter, logo-key, rule
    "primary":  (P["primary"],  P["paper"],    P["paper"],    P["slate"], "on_dark",  P["slate"]),
    "graphite": (P["graphite"], P["paper"],    P["paper"],    P["slate"], "on_dark",  P["slate"]),
    "paper":    (P["paper"],    P["graphite"], P["graphite"], P["teal"],  "on_light", P["teal"]),
    "image":    (P["primary"],  P["paper"],    P["paper"],    P["paper"], "on_dark",  P["paper"]),
}
SIZES = {  # start, min  (px)
    "cover": (132, 80), "statement": (112, 72), "question": (104, 72),
    "body": (88, 64), "closing": (96, 64)}
TOP = {"cover": 330, "statement": 330, "question": 330, "closing": 330, "body": 330}
ZONE_JUSTIFY = {"top": "flex-start", "center": "center", "bottom": "flex-end"}


def font_css():
    out = []
    for name, rel in CFG["fonts"]["files"].items():
        wt = CFG["fonts"]["css_weight"][name]
        out.append(f"@font-face{{font-family:'DoranFaNum';font-weight:{wt};src:url('{(ROOT / rel).as_uri()}') format('truetype');}}")
    return "\n".join(out)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def slide_html(s, total=8):
    mode = s["background"]["mode"]
    bg, hc, bc, cc, logo_key, rule = THEME[mode]
    h_start, h_min = SIZES[s["layout"]]
    zone = s["art_direction"]["typography_zone"]
    jc = ZONE_JUSTIFY.get(zone, "center")
    logo_path = (ROOT / LOGO["files"][logo_key]["path"]).as_uri()
    bgimg = ""
    if mode == "image":
        bgimg = (f"<div class='img' style=\"background-image:url('{pathlib.Path(s['background']['image_path']).resolve().as_uri()}')\"></div>"
                 f"<div class='scrim' style='opacity:{s['background']['scrim_opacity']}'></div>")
    head = html.escape(normalize(s["headline"]))
    body = html.escape(normalize(s.get("body", "")))
    counter = normalize(f"{s['slide_number']} / {total}")
    body_html = f"<p id='b'>{body}</p>" if body else ""
    return f"""<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<style>{font_css()}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{bg}}}
body{{font-family:'DoranFaNum';font-feature-settings:'kern','liga','calt';text-rendering:geometricPrecision;-webkit-font-smoothing:antialiased;position:relative}}
.img{{position:absolute;inset:0;background-size:cover;background-position:center}}
.scrim{{position:absolute;inset:0;background:{P['primary']}}}
#zone{{position:absolute;top:{M}px;right:{M}px;left:{M}px;bottom:{M + FOOT}px;display:flex;flex-direction:column;justify-content:flex-start;padding-top:{TOP[s['layout']]}px;align-items:stretch}}
#rule{{width:96px;height:6px;background:{rule};margin-bottom:56px}}
h1{{font-weight:800;color:{hc};line-height:1.32;font-size:{h_start}px;text-align:right;text-wrap:balance}}
p{{font-weight:400;color:{bc};line-height:1.85;font-size:44px;margin-top:44px;text-align:right;max-width:880px;text-wrap:pretty}}
#ctr{{position:absolute;right:{M}px;bottom:{M}px;font-weight:400;font-size:32px;color:{cc};letter-spacing:.02em}}
#logo{{position:absolute;left:{M}px;bottom:{M}px;height:{LOGO['render_height_px']}px;width:auto;display:block}}
</style></head><body>{bgimg}
<div id="zone"><div id="rule"></div><h1 id="h">{head}</h1>{body_html}</div>
<div id="ctr">{html.escape(counter)}</div>
<img id="logo" src="{logo_path}" alt="">
<script>
const z=document.getElementById('zone'),h=document.getElementById('h');
let s={h_start};
while(z.scrollHeight>z.clientHeight+1 && s>{h_min}){{s-=4;h.style.fontSize=s+'px';}}
</script></body></html>"""


def measure(page):
    return page.evaluate("""()=>{
      const r=e=>{const b=e.getBoundingClientRect();return {l:b.left,t:b.top,r:b.right,b:b.bottom}};
      const q=id=>document.getElementById(id);
      const zone=q('zone'),h=q('h'),b=q('b'),logo=q('logo'),ctr=q('ctr');
      return {zone:r(zone),zone_overflow:zone.scrollHeight>zone.clientHeight+1,
        h:r(h),h_font_px:parseFloat(getComputedStyle(h).fontSize),h_lines:Math.round(h.getBoundingClientRect().height/parseFloat(getComputedStyle(h).lineHeight)),
        b:b?r(b):null,b_font_px:b?parseFloat(getComputedStyle(b).fontSize):null,
        logo:r(logo),logo_natural:[logo.naturalWidth,logo.naturalHeight],ctr:r(ctr),
        font_ok:document.fonts.check("800 40px DoranFaNum"),
        families:[...new Set([h,b,ctr].filter(Boolean).map(e=>getComputedStyle(e).fontFamily))]}}""")


def main(post_path, out_dir):
    post = json.loads(pathlib.Path(post_path).read_text(encoding="utf8"))
    out = pathlib.Path(out_dir).resolve() / post["post_id"]
    (out / "html").mkdir(parents=True, exist_ok=True)
    metrics = {"canvas": [W, H], "slides": []}
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium") if pathlib.Path("/opt/pw-browsers/chromium").exists() else pw.chromium.launch()
        ctx = br.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        page = ctx.new_page()
        for s in post["slides"]:
            n = s["slide_number"]
            hp = out / "html" / f"{n:02d}.html"
            hp.write_text(slide_html(s), encoding="utf8")
            page.goto(hp.as_uri()); page.evaluate("document.fonts.ready"); page.wait_for_timeout(150)
            m = measure(page); m["slide"] = n
            png = out / f"{n:02d}.png"
            page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": W, "height": H})
            m["png_sha256"] = sha(png)
            metrics["slides"].append(m)
        br.close()
    (out / "layout_metrics.json").write_text(json.dumps(metrics, indent=1), encoding="utf8")
    print("rendered", len(metrics["slides"]), "slides ->", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
