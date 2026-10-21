"""Reel renderer: reel JSON -> 1080x1920 H.264 MP4 (kinetic Persian type + vector motifs + synthesized sfx).
Usage: python3 reel_render.py samples/sample_reel.json out/
Deterministic: JS render(t) is a pure function of time; frames are captured one by one with Chromium, then encoded with ffmpeg.
Text is animated per WORD (never per letter) so Persian joining/shaping stays intact. Fonts: DoranFaNum files only."""
import json, sys, pathlib, subprocess, hashlib, shutil
from playwright.sync_api import sync_playwright
from persian_text import normalize
import reel_audio

ROOT = pathlib.Path(__file__).parent.resolve()
CFG = json.loads((ROOT / "brand_config.json").read_text(encoding="utf8"))
P = CFG["palette"]
W, H, FPS = 1080, 1920, 30
SAFE = {"x0": 72, "x1": 1008, "y0": 250, "y1": 1500}   # Reels UI overlays top ~250px and bottom ~420px
THEME = {
    "primary":  dict(bg=P["primary"],  fg=P["paper"],    dim=P["slate"], acc=P["paper"], logo="on_dark"),
    "graphite": dict(bg=P["graphite"], fg=P["paper"],    dim=P["slate"], acc=P["paper"], logo="on_dark"),
    "paper":    dict(bg=P["paper"],    dim=P["teal"],    fg=P["graphite"], acc=P["teal"], logo="on_light"),
}
STYLE = {"h": (116, 800), "b": (60, 400), "s": (44, 300)}  # size px, css weight
WORD_GAP = 0.22


def schedule(reel):
    scenes = []
    for sc in reel["scenes"]:
        lines = []
        for ln in sc.get("lines", []):
            size, wt = STYLE[ln.get("kind", "h")]
            words = normalize(ln["text"]).split(" ")
            gap = ln.get("gap", WORD_GAP)
            lines.append({"size": ln.get("size", size), "weight": wt, "dim": ln.get("dim", False),
                          "words": [{"w": w, "t": round(ln["t"] + k * gap, 3)} for k, w in enumerate(words)]})
        scenes.append({"id": sc["id"], "start": sc["start"], "end": sc["end"], "theme": THEME[sc["bg"]], "bg": sc["bg"],
                       "lines": lines, "txt_top": sc.get("txt_top", 330), "motif": sc.get("motif"), "logo": sc.get("logo", False), "image": sc.get("image")})
    return scenes


def font_css():
    return "\n".join(f"@font-face{{font-family:'DoranFaNum';font-weight:{CFG['fonts']['css_weight'][n]};src:url('{(ROOT / r).as_uri()}') format('truetype');}}"
                     for n, r in CFG["fonts"]["files"].items())


JS = r"""
const NS='http://www.w3.org/2000/svg';
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>1-Math.pow(1-x,3);
const easeIO=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const stage=document.getElementById('stage'),txt=document.getElementById('txt'),svg=document.getElementById('motif'),
      logo=document.getElementById('logo'),imgwrap=document.getElementById('imgwrap'),bgimg=document.getElementById('bgimg'),tint=document.getElementById('tint');
function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);(parent||svg).appendChild(e);return e;}
let cur=-1,M=null,words=[];

const MOTIFS={
 grid:{init(P,C){const cols=P.cols||4,rows=P.rows||4,gap=P.gap||124,r=P.r||36,cx=540,cy=P.cy||1250;
   const pos=[];this.cs=[];
   for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const x=cx+(i-(cols-1)/2)*gap,y=cy+(j-(rows-1)/2)*gap;pos.push([x,y]);
     this.cs.push(el('circle',{cx:x,cy:y,r:r,fill:'none',stroke:C.fg,'stroke-width':5,opacity:0}));}
   this.pos=pos;this.path=P.path||[5];this.hl=el('circle',{r:r,fill:C.acc,opacity:0});this.r=r;},
  update(u){this.cs.forEach((c,i)=>c.setAttribute('opacity',.75*ease(clamp((u-.04*i)/.5))));
   const hop=0.9,t0=0.8,n=this.path.length;let k=clamp((u-t0)/hop,0,n-1+0.0001),i=Math.floor(k),f=easeIO(k-i);
   const a=this.pos[this.path[Math.min(i,n-1)]],b=this.pos[this.path[Math.min(i+1,n-1)]];
   this.hl.setAttribute('cx',a[0]+(b[0]-a[0])*f);this.hl.setAttribute('cy',a[1]+(b[1]-a[1])*f);
   this.hl.setAttribute('opacity',ease(clamp((u-.5)/.4)));}},
 cloud:{init(P,C){this.N=P.n||420;this.R=P.R||290;this.cy=P.cy||1250;this.ds=[];
   for(let i=0;i<this.N;i++){const rr=this.R*Math.sqrt((i+.5)/this.N),a=i*2.399963;
     this.ds.push(el('circle',{cx:540+rr*Math.cos(a),cy:this.cy+rr*Math.sin(a),r:5.5,fill:C.fg,opacity:0}));}
   this.one=el('circle',{cx:540+this.R*Math.sqrt((this.N-.5)/this.N)*Math.cos((this.N-1)*2.399963),cy:this.cy+this.R*Math.sqrt((this.N-.5)/this.N)*Math.sin((this.N-1)*2.399963),r:13,fill:C.acc,opacity:0});this.span=P.span||2.4;},
  update(u){const n=Math.floor(this.N*ease(clamp(u/this.span)));this.ds.forEach((d,i)=>d.setAttribute('opacity',i<n?.8:0));this.one.setAttribute('opacity',ease(clamp((u-this.span)/.4)));}},
 ring:{init(P,C){this.r=P.r||170;this.cy=P.cy||1250;this.c=el('circle',{cx:540,cy:this.cy,r:this.r,fill:'none',stroke:C.fg,'stroke-width':8,pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1,transform:`rotate(-90 540 ${this.cy})`});
   this.d=el('circle',{cx:540,cy:this.cy,r:14,fill:C.acc,opacity:0});},
  update(u){const p=ease(clamp(u/.9));this.c.setAttribute('stroke-dashoffset',1-p);const b=1+.035*Math.sin(u*2*Math.PI/3);this.c.setAttribute('r',this.r*b);this.d.setAttribute('opacity',ease(clamp((u-.7)/.4)));}},
 shift:{init(P,C){this.r=P.r||170;this.cy=P.cy||1250;this.dx=P.dx||46;this.dy=P.dy||-34;
   this.c=el('circle',{cx:540,cy:this.cy,r:this.r,fill:'none',stroke:C.fg,'stroke-width':8});
   this.g=el('circle',{cx:540,cy:this.cy,r:20,fill:'none',stroke:C.dim,'stroke-width':4,'stroke-dasharray':'6 8',opacity:0});
   this.d=el('circle',{cx:540,cy:this.cy,r:20,fill:C.acc,opacity:0});},
  update(u){const a=ease(clamp(u/.6));this.c.setAttribute('opacity',a);this.g.setAttribute('opacity',a);this.d.setAttribute('opacity',a);
   const m=easeIO(clamp((u-1.2)/1.6));this.d.setAttribute('cx',540+this.dx*m);this.d.setAttribute('cy',this.cy+this.dy*m);}},
 whisper:{init(P,C){const x0=140,x1=940,y0=P.y0||1330,A=P.big||250,a=P.small||16,sg=95;this.cy=y0;
   const bump=(amp)=>{let d='';for(let i=0;i<=160;i++){const x=x0+(x1-x0)*i/160,y=y0-amp*Math.exp(-Math.pow(x-540,2)/(2*sg*sg));d+=(i?'L':'M')+x.toFixed(1)+' '+y.toFixed(1);}return d;};
   this.big=el('path',{d:bump(A),fill:'none',stroke:C.dim,'stroke-width':5,'stroke-dasharray':'2 14','stroke-linecap':'round',opacity:0});
   this.base=el('path',{d:bump(a),fill:'none',stroke:C.acc,'stroke-width':8,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});},
  update(u){this.big.setAttribute('opacity',.9*ease(clamp(u/.8)));this.base.setAttribute('stroke-dashoffset',1-easeIO(clamp((u-1.0)/1.6)));}},
 steps:{init(P,C){const n=P.n||5,w=96,g=34,base=P.base||1440;this.bs=[];const x0=540-(n*w+(n-1)*g)/2;
   for(let i=0;i<n;i++){const h=90+i*(P.dh||62);this.bs.push([el('rect',{x:x0+i*(w+g),y:base,width:w,height:0,rx:6,fill:i==n-1?C.acc:C.dim,opacity:i==n-1?1:.85}),h,base]);}},
  update(u){this.bs.forEach(([r,h,base],i)=>{const p=ease(clamp((u-.15*i)/.7));r.setAttribute('height',h*p);r.setAttribute('y',base-h*p);});}}
};

function build(si){
  const s=SC[si];cur=si;const C=s.theme;
  stage.style.background=C.bg;
  txt.innerHTML='';words=[];txt.style.top=(s.txt_top||330)+'px';
  s.lines.forEach((l,li)=>{const row=document.createElement('div');row.className='ln';
    l.words.forEach(w=>{const sp=document.createElement('span');sp.className='w';sp.textContent=w.w;sp.dataset.t=w.t;sp.dataset.li=li;
      sp.style.fontSize=l.size+'px';sp.style.fontWeight=l.weight;sp.style.color=l.dim?C.dim:C.fg;sp.style.opacity=0;row.appendChild(sp);words.push(sp);});
    txt.appendChild(row);});
  // fit: shrink all lines until the text block fits its zone
  let k=1;while(txt.getBoundingClientRect().height>SAFE_TXT_H && k>.55){k-=.04;s.lines.forEach((l,li)=>{txt.children[li].querySelectorAll('.w').forEach(e=>e.style.fontSize=(l.size*k)+'px');});}

  // balance wrapped lines: narrowest width that keeps the same row count -> no single-word orphan rows
  const rowsOf=row=>new Set([...row.children].map(c=>Math.round(c.getBoundingClientRect().top))).size;
  [...txt.children].forEach(row=>{const full=row.getBoundingClientRect().width,n0=rowsOf(row);if(n0<2)return;
    let lo=full*.35,hi=full;for(let i=0;i<14;i++){const mid=(lo+hi)/2;row.style.maxWidth=mid+'px';if(rowsOf(row)>n0)lo=mid;else hi=mid;}row.style.maxWidth=hi+'px';});
  window.__fit=k;
  svg.innerHTML='';M=null;
  if(s.motif){M=Object.create(MOTIFS[s.motif.type]);M.init(s.motif.params||{},C);}
  logo.style.display=s.logo?'block':'none';if(s.logo)logo.src=s.theme.logo_url;
  if(s.image){imgwrap.style.display='block';bgimg.src=s.image.url;tint.style.background=C.bg;}else{imgwrap.style.display='none';}
}
function render(t){
  let si=SC.findIndex(s=>t>=s.start&&t<s.end);if(si<0)si=SC.length-1;
  if(si!==cur)build(si);
  const s=SC[si],u=t-s.start,dur=s.end-s.start;
  words.forEach(e=>{const p=ease(clamp((u-parseFloat(e.dataset.t))/.42));e.style.opacity=p;e.style.transform=`translateY(${(1-p)*30}px)`;e.style.filter=`blur(${(1-p)*10}px)`;});
  const fade=Math.min(1,u/.14)*Math.min(1,(s.end-t)/.14);
  txt.style.opacity=fade;svg.style.opacity=fade;logo.style.opacity=fade;imgwrap.style.opacity=fade;
  if(s.image){bgimg.style.transform=`scale(${1+.08*u/dur})`;}
  if(M)M.update(u,dur);
  if(s.logo){const p=ease(clamp(u/.8));logo.style.transform=`translate(-50%,-50%) scale(${.94+.06*p})`;}
}
window.render=render;
window.measure=function(){return {fit:window.__fit,words:words.map(e=>{const b=e.getBoundingClientRect();return {w:e.textContent,l:b.left,r:b.right,t:b.top,b:b.bottom,fs:parseFloat(e.style.fontSize),tt:parseFloat(e.dataset.t),li:parseInt(e.dataset.li)};}),
  fonts:[...new Set(words.map(e=>getComputedStyle(e).fontFamily))],font_ok:document.fonts.check('800 40px DoranFaNum'),
  logo:document.getElementById('logo').style.display==='block'?(()=>{const b=document.getElementById('logo').getBoundingClientRect();return {l:b.left,r:b.right,t:b.top,b:b.bottom,nw:document.getElementById('logo').naturalWidth,nh:document.getElementById('logo').naturalHeight}})():null};};
"""


def page_html(scenes):
    for s in scenes:
        s["theme"] = dict(s["theme"], logo_url=(ROOT / CFG["logo"]["files"][s["theme"]["logo"]]["path"]).as_uri())
        if s.get("image"):
            s["image"] = dict(s["image"], url=pathlib.Path(s["image"]["path"]).resolve().as_uri())
    txt_h = 760
    return f"""<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><style>{font_css()}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:'DoranFaNum';text-rendering:geometricPrecision;-webkit-font-smoothing:antialiased}}
#imgwrap{{position:absolute;inset:0;display:none;overflow:hidden}}
#bgimg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.05)}}
#tint{{position:absolute;inset:0;opacity:.58;mix-blend-mode:multiply}}
#motif{{position:absolute;inset:0;width:{W}px;height:{H}px}}
#txt{{position:absolute;left:{SAFE['x0']}px;right:{W - SAFE['x1']}px;top:330px;display:flex;flex-direction:column;align-items:center;gap:34px;direction:rtl;text-align:center}}
.ln{{display:flex;flex-wrap:wrap;justify-content:center;gap:0 .36em;line-height:1.4}}
.w{{display:inline-block;will-change:transform,opacity,filter}}
#logo{{position:absolute;left:50%;top:760px;height:420px;width:auto;transform:translate(-50%,-50%);display:none}}
</style></head><body><div id="stage"><div id="imgwrap"><img id="bgimg"><div id="tint"></div></div><svg id="motif" viewBox="0 0 {W} {H}"></svg><div id="txt"></div><img id="logo"></div>
<script>const SC={json.dumps(scenes, ensure_ascii=False)};const SAFE_TXT_H={txt_h};{JS}</script></body></html>"""


def main(reel_path, out_dir):
    reel = json.loads(pathlib.Path(reel_path).read_text(encoding="utf8"))
    out = pathlib.Path(out_dir).resolve() / reel["reel_id"]
    if out.exists(): shutil.rmtree(out)
    (out / "frames").mkdir(parents=True)
    scenes = schedule(reel)
    total = scenes[-1]["end"]
    html = page_html(json.loads(json.dumps(scenes)))
    (out / "reel.html").write_text(html, encoding="utf8")
    metrics = {"fps": FPS, "size": [W, H], "safe": SAFE, "duration": total, "scenes": []}
    n = int(round(total * FPS))
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium") if pathlib.Path("/opt/pw-browsers/chromium").exists() else pw.chromium.launch()
        page = br.new_context(viewport={"width": W, "height": H}, device_scale_factor=1).new_page()
        page.goto((out / "reel.html").as_uri()); page.evaluate("Promise.all([300,400,800].map(w=>document.fonts.load(`${w} 40px DoranFaNum`,'پول آدم')))"); page.evaluate("document.fonts.ready"); page.wait_for_timeout(300)
        for s in scenes:  # layout metrics near the end of each scene, when every word is visible
            page.evaluate(f"render({s['end'] - 0.2})"); page.wait_for_timeout(200)
            m = page.evaluate("measure()"); m.update(scene=s["id"], start=s["start"], end=s["end"], bg=s["bg"]); metrics["scenes"].append(m)
        for i in range(n):
            page.evaluate(f"render({i / FPS})")
            page.screenshot(path=str(out / "frames" / f"{i:05d}.jpg"), type="jpeg", quality=95, clip={"x": 0, "y": 0, "width": W, "height": H})
        # cover frame: first scene, all words visible
        page.evaluate(f"render({scenes[0]['end'] - 0.2})"); page.screenshot(path=str(out / "cover.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
        br.close()
    (out / "reel_metrics.json").write_text(json.dumps(metrics, indent=1), encoding="utf8")
    reel_audio.synth(scenes, total, out / "audio.wav")
    mp4 = out / f"{reel['reel_id']}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(out / "frames" / "%05d.jpg"), "-i", str(out / "audio.wav"),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", str(mp4)], check=True)
    shutil.rmtree(out / "frames")
    print("rendered", mp4, f"{total:.1f}s", mp4.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
