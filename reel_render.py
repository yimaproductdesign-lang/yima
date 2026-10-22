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
STYLE = {"xl": (168, 800), "h": (116, 800), "b": (68, 500), "s": (48, 300)}  # size px, css weight
MOTIF_MIN = {"grid": 2.2, "cloud": 2.6, "ring": 2.0, "shift": 3.0, "whisper": 3.0, "steps": 2.4, "converge": 3.4, "network": 3.4,
             "loop": 3.0, "balance": 3.2, "journey": 3.0, "focus": 2.8, "split": 2.4, "clock": 3.2, "noise": 3.2}


def word_gap(w):
    return 0.15 + 0.009 * len(w.replace("\u200c", ""))


def pause_after(w):
    c = w.strip("*")[-1:]
    return 0.30 if c in ".؟?!" else 0.15 if c in "،؛:" else 0.0


def schedule(reel):
    """Content-driven timing: reveal pace follows word length and punctuation, hold follows word count, motif has a minimum run."""
    scenes, prev_end = [], 0.0
    for sc in reel["scenes"]:
        start = sc.get("start", prev_end)
        cursor, last_in, nwords, lines = sc.get("lead", 0.25), 0.0, 0, []
        for ln in sc.get("lines", []):
            size, wt = STYLE[ln.get("kind", "h")]
            toks = (normalize(ln["text"]) if reel.get("lang", "fa") == "fa" else " ".join(ln["text"].split())).split(" ")
            t = ln["t"] if "t" in ln else cursor
            ws = []
            for k, tok in enumerate(toks):
                clean = tok.replace("*", "")
                ws.append({"w": clean, "t": round(t, 3), "em": "*" in tok})
                last_in = max(last_in, t); nwords += 1
                t += ln.get("gap", word_gap(clean)) + pause_after(tok)
            cursor = max(cursor, t) + 0.12
            lines.append({"size": ln.get("size", size), "weight": wt, "dim": ln.get("dim", False), "words": ws})
        hold = sc.get("hold", max(0.9, 0.6 + 0.06 * nwords))
        mm = MOTIF_MIN.get((sc.get("motif") or {}).get("type"), 0) if sc.get("motif") else 0
        vm = 3.0 if (sc.get("objects") or sc.get("fx")) else 0
        dur = sc.get("dur") or max((last_in + 0.42 + hold) if nwords else 0, mm, vm, 3.0 if sc.get("logo") else 2.4)
        end = sc.get("end", round(start + dur, 3))
        scenes.append({"id": sc["id"], "start": start, "end": end, "theme": THEME[sc["bg"]], "bg": sc["bg"], "lines": lines,
                       "txt_top": sc.get("txt_top", 330), "motif": sc.get("motif"), "logo": sc.get("logo", False), "image": sc.get("image"),
                       "objects": sc.get("objects"), "fx": sc.get("fx"), "style": sc.get("style", reel.get("style")), "spot_y": sc.get("spot_y"),
                       "txt_align": sc.get("txt_align", "start")})
        prev_end = end
    tmax = (reel.get("target_s") or [40, 60])[1]
    total = scenes[-1]["end"] if scenes else 0
    if total > tmax and not any("start" in s or "end" in s for s in reel["scenes"]):
        mins = []
        for s in scenes:
            last = max([w["t"] for l in s["lines"] for w in l["words"]] or [0])
            mins.append(max(last + 0.42 + 0.8 if s["lines"] else 0, 2.2, 3.0 if s["logo"] else 0))
        durs = [s["end"] - s["start"] for s in scenes]
        slack = sum(d - m for d, m in zip(durs, mins))
        f = max(0.0, (tmax - 0.5 - sum(mins)) / slack) if slack > 0 else 0
        t = 0.0
        for s, d, m in zip(scenes, durs, mins):
            s["start"] = round(t, 3); t += m + f * (d - m); s["end"] = round(t, 3)
    mood = (reel.get("audio") or {}).get("mood")
    if mood:  # snap every cut onto the beat of the music bed
        import math, reel_music
        beat = 60 / reel_music.MOODS[mood]["bpm"]; t = 0.0
        for s in scenes:
            d = s["end"] - s["start"]; d = max(1, math.ceil(d / beat - 0.2)) * beat
            s["start"] = round(t, 4); t += d; s["end"] = round(t, 4)
        def need(s):
            last = max([w["t"] for l in s["lines"] for w in l["words"]] or [0])
            nw = sum(len(l["words"]) for l in s["lines"])
            return max(last + 0.42 + 0.8 if s["lines"] else 0, nw / 3.0, 2.2, 3.0 if s["logo"] else 0)
        durs = [s["end"] - s["start"] for s in scenes]
        while sum(durs) > tmax:
            i = max(range(len(scenes)), key=lambda k: durs[k] - need(scenes[k]))
            if durs[i] - beat < need(scenes[i]): break
            durs[i] -= beat
        t = 0.0
        for s, d in zip(scenes, durs):
            s["start"] = round(t, 4); t += d; s["end"] = round(t, 4)
    for i, sc in enumerate(scenes):  # object continuity: same key in neighbouring scenes glides instead of re-entering
        keys = lambda j: {o.get("key") for o in (scenes[j].get("objects") or []) if o.get("key")} if 0 <= j < len(scenes) else set()
        for o in sc.get("objects") or []:
            o["carry_in"] = bool(o.get("key")) and o["key"] in keys(i - 1)
            o["carry_out"] = bool(o.get("key")) and o["key"] in keys(i + 1)
    gstart = None
    for i, sc in enumerate(scenes):
        m = sc["motif"] or {}; g = m.get("group")
        prev_same = i > 0 and g and (scenes[i - 1]["motif"] or {}).get("group") == g
        next_same = i + 1 < len(scenes) and g and (scenes[i + 1]["motif"] or {}).get("group") == g
        if not prev_same: gstart = sc["start"]
        sc["mstart"], sc["m_in"], sc["m_out"] = gstart, not prev_same, not next_same
    return scenes


def font_css():
    lat = CFG["fonts"].get("latin")
    extra = "\n".join(f"@font-face{{font-family:'{lat['family']}';font-weight:{CFG['fonts']['css_weight'][n]};src:url('{(ROOT / r).as_uri()}');}}" for n, r in lat["files"].items()) if lat else ""
    return extra + "\n" + "\n".join(f"@font-face{{font-family:'DoranFaNum';font-weight:{CFG['fonts']['css_weight'][n]};src:url('{(ROOT / r).as_uri()}') format('truetype');}}"
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
   this.pos=pos;this.hopT=P.hop_t||0.8;this.path=P.path||[5];this.hl=el('circle',{r:r,fill:C.acc,opacity:0});this.r=r;},
  update(u){this.cs.forEach((c,i)=>c.setAttribute('opacity',.75*ease(clamp((u-.04*i)/.5))));
   const hop=0.9,t0=this.hopT,n=this.path.length;let k=clamp((u-t0)/hop,0,n-1+0.0001),i=Math.floor(k),f=easeIO(k-i);
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

 converge:{init(P,C){const n=P.n||36,cols=6,gap=P.gap||64,cy=P.cy||1250;let sd=P.seed||7;
   const rnd=()=>{sd|=0;sd=sd+0x6D2B79F5|0;let t=Math.imul(sd^sd>>>15,1|sd);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
   this.d=[];for(let i=0;i<n;i++){const gx=540+((i%cols)-(cols-1)/2)*gap,gy=cy+(Math.floor(i/cols)-(n/cols-1)/2)*gap;
     const sx=540+(rnd()-.5)*720,sy=cy+(rnd()-.5)*520;this.d.push([el('circle',{cx:sx,cy:sy,r:9,fill:i==n-1?C.acc:C.fg,opacity:0}),sx,sy,gx,gy]);}},
  update(u){const p=easeIO(clamp((u-.9)/2.4));this.d.forEach(([c,sx,sy,gx,gy],i)=>{c.setAttribute('cx',sx+(gx-sx)*p);c.setAttribute('cy',sy+(gy-sy)*p);c.setAttribute('opacity',.9*ease(clamp((u-.03*i)/.4)));});}},
 network:{init(P,C){const cy=P.cy||1250,n=9;this.cy=cy;this.n=[];for(let i=0;i<n;i++){const a=i/n*2*Math.PI-1.2,r=i%2?170:240;this.n.push([540+r*Math.cos(a),cy+r*Math.sin(a)]);}
   const pairs=[];for(let i=0;i<n;i++){pairs.push([i,(i+1)%n]);pairs.push([i,(i+3)%n]);}
   this.e=pairs.map(([a,b],k)=>[el('line',{x1:0,y1:0,x2:0,y2:0,stroke:C.fg,'stroke-width':3,opacity:0}),a,b,k]);
   this.c=this.n.map((_,i)=>el('circle',{r:16,fill:i==0?C.acc:C.fg,opacity:0}));},
  update(u){const dr=easeIO(clamp((u-2.2)/1.4)),drift=1+.14*dr;const pos=this.n.map(([x,y])=>[540+(x-540)*drift,this.cy+(y-this.cy)*drift]);
   this.c.forEach((c,i)=>{c.setAttribute('cx',pos[i][0]);c.setAttribute('cy',pos[i][1]);c.setAttribute('opacity',ease(clamp((u-.07*i)/.4)));});
   this.e.forEach(([l,a,b,k])=>{const p=ease(clamp((u-.5-.06*k)/.5));l.setAttribute('x1',pos[a][0]);l.setAttribute('y1',pos[a][1]);
     l.setAttribute('x2',pos[a][0]+(pos[b][0]-pos[a][0])*p);l.setAttribute('y2',pos[a][1]+(pos[b][1]-pos[a][1])*p);
     const weak=k%3==0?(1-.75*dr):1;l.setAttribute('opacity',p>0?.55*weak:0);});}},
 loop:{init(P,C){this.cy=P.cy||1250;this.R=P.R||150;
   this.ring=el('circle',{cx:540,cy:this.cy,r:this.R,fill:'none',stroke:C.dim,'stroke-width':3,'stroke-dasharray':'4 12',opacity:0});
   this.l=el('line',{stroke:C.dim,'stroke-width':3,opacity:0});this.a=el('circle',{r:26,fill:C.acc,opacity:0});this.b=el('circle',{r:26,fill:'none',stroke:C.fg,'stroke-width':6,opacity:0});},
  update(u){const f=ease(clamp(u/.6));this.ring.setAttribute('opacity',f);this.a.setAttribute('opacity',f);this.b.setAttribute('opacity',f);this.l.setAttribute('opacity',.6*f);
   const th=-Math.PI/2+u*1.25,R=this.R,ax=540+R*Math.cos(th),ay=this.cy+R*Math.sin(th),bx=540-R*Math.cos(th),by=this.cy-R*Math.sin(th);
   this.a.setAttribute('cx',ax);this.a.setAttribute('cy',ay);this.b.setAttribute('cx',bx);this.b.setAttribute('cy',by);
   this.l.setAttribute('x1',ax);this.l.setAttribute('y1',ay);this.l.setAttribute('x2',bx);this.l.setAttribute('y2',by);}},
 balance:{init(P,C){this.cy=P.cy||1250;this.L=P.L||260;const c=this.cy;
   this.base=el('path',{d:`M540 ${c+20} L495 ${c+170} L585 ${c+170} Z`,fill:'none',stroke:C.fg,'stroke-width':6,'stroke-linejoin':'round',opacity:0});
   this.beam=el('line',{stroke:C.fg,'stroke-width':8,'stroke-linecap':'round',opacity:0});
   this.sl=el('line',{stroke:C.dim,'stroke-width':3,opacity:0});this.sr=el('line',{stroke:C.dim,'stroke-width':3,opacity:0});
   this.pl=el('circle',{r:44,fill:'none',stroke:C.fg,'stroke-width':6,opacity:0});this.pr=el('circle',{r:44,fill:C.acc,opacity:0});this.piv=el('circle',{cx:540,cy:c+20,r:12,fill:C.fg,opacity:0});},
  update(u){const f=ease(clamp(u/.6));[this.base,this.beam,this.pl,this.pr,this.piv].forEach(e=>e.setAttribute('opacity',f));[this.sl,this.sr].forEach(e=>e.setAttribute('opacity',.7*f));
   const v=Math.max(0,u-.6),ang=(15*Math.exp(-1.1*v)*Math.cos(v*4.2)+5*(1-Math.exp(-v)))*Math.PI/180,c=this.cy+20,L=this.L;
   const lx=540-L*Math.cos(ang),ly=c+L*Math.sin(ang),rx=540+L*Math.cos(ang),ry=c-L*Math.sin(ang);
   this.beam.setAttribute('x1',lx);this.beam.setAttribute('y1',ly);this.beam.setAttribute('x2',rx);this.beam.setAttribute('y2',ry);
   this.sl.setAttribute('x1',lx);this.sl.setAttribute('y1',ly);this.sl.setAttribute('x2',lx);this.sl.setAttribute('y2',ly+90);
   this.sr.setAttribute('x1',rx);this.sr.setAttribute('y1',ry);this.sr.setAttribute('x2',rx);this.sr.setAttribute('y2',ry+90);
   this.pl.setAttribute('cx',lx);this.pl.setAttribute('cy',ly+134);this.pr.setAttribute('cx',rx);this.pr.setAttribute('cy',ry+134);}},
 journey:{init(P,C){const cy=P.cy||1250;this.path=el('path',{d:`M180 ${cy+200} C 380 ${cy+200}, 420 ${cy-60}, 620 ${cy-40} S 840 ${cy-200}, 900 ${cy-220}`,fill:'none',stroke:C.dim,'stroke-width':5,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':'1 1','stroke-dashoffset':1});
   this.tgt=el('circle',{cx:900,cy:cy-220,r:36,fill:'none',stroke:C.fg,'stroke-width':5,opacity:0});this.dot=el('circle',{r:22,fill:C.acc,opacity:0});},
  update(u){const p=easeIO(clamp((u-.3)/2.6)),len=this.path.getTotalLength(),pt=this.path.getPointAtLength(len*p);this.path.setAttribute('stroke-dashoffset',1-p);
   this.dot.setAttribute('cx',pt.x);this.dot.setAttribute('cy',pt.y);this.dot.setAttribute('opacity',ease(clamp(u/.4)));this.tgt.setAttribute('opacity',ease(clamp((u-.2)/.6)));}},
 focus:{init(P,C){this.cy=P.cy||1250;this.rs=[];for(let i=0;i<5;i++)this.rs.push(el('circle',{cx:540,cy:this.cy,r:320,fill:'none',stroke:i==4?C.acc:C.fg,'stroke-width':i==4?8:4,opacity:0}));},
  update(u){const p=easeIO(clamp((u-.2)/2.4));this.rs.forEach((c,i)=>{const r0=320-i*45,r1=108-i*18;c.setAttribute('r',r0+(r1-r0)*p);c.setAttribute('opacity',(i==4?1:.7)*ease(clamp((u-.08*i)/.5)));});}},
 split:{init(P,C){this.cy=P.cy||1250;this.a=el('circle',{cx:540,cy:this.cy,r:120,fill:C.acc,opacity:0});this.b=el('circle',{cx:540,cy:this.cy,r:120,fill:'none',stroke:C.fg,'stroke-width':8,opacity:0});},
  update(u){const f=ease(clamp(u/.5));this.a.setAttribute('opacity',f);this.b.setAttribute('opacity',u>.8?1:0);const s=easeIO(clamp((u-.8)/1.2));
   this.a.setAttribute('cx',540-170*s);this.b.setAttribute('cx',540+170*s);this.a.setAttribute('r',120-34*s);this.b.setAttribute('r',120-34*s);}},
 clock:{init(P,C){this.cy=P.cy||1250;this.R=190;this.ring=el('circle',{cx:540,cy:this.cy,r:this.R,fill:'none',stroke:C.fg,'stroke-width':6,opacity:0});this.t=[];
   for(let i=0;i<12;i++){const a=i/12*2*Math.PI-Math.PI/2,R=this.R;this.t.push(el('line',{x1:540+(R-26)*Math.cos(a),y1:this.cy+(R-26)*Math.sin(a),x2:540+(R-6)*Math.cos(a),y2:this.cy+(R-6)*Math.sin(a),stroke:C.fg,'stroke-width':4,opacity:0}));}
   this.arc=el('path',{fill:C.acc,opacity:0});this.hand=el('line',{x1:540,y1:this.cy,stroke:C.fg,'stroke-width':8,'stroke-linecap':'round',opacity:0});},
  update(u){const f=ease(clamp(u/.5)),r=this.R-30,cy=this.cy;this.ring.setAttribute('opacity',f);this.t.forEach(l=>l.setAttribute('opacity',.8*f));this.hand.setAttribute('opacity',f);
   const p=easeIO(clamp((u-.5)/2.6)),a=-Math.PI/2+p*Math.PI/2,x=540+r*Math.cos(a),y=cy+r*Math.sin(a);
   this.hand.setAttribute('x2',x);this.hand.setAttribute('y2',y);this.arc.setAttribute('d',`M540 ${cy} L540 ${cy-r} A${r} ${r} 0 0 1 ${x} ${y} Z`);this.arc.setAttribute('opacity',.4*f);}},
 noise:{init(P,C){this.cy=P.cy||1250;this.p=el('polyline',{fill:'none',stroke:C.fg,'stroke-width':6,'stroke-linejoin':'round','stroke-linecap':'round',opacity:0});},
  update(u){const A=130*(1-easeIO(clamp((u-1.6)/1.6))),fr=Math.floor(u*10);let pts='';
   for(let i=0;i<=48;i++){const x=120+840*i/48,h=Math.sin(i*12.9898+fr*78.233)*43758.5453,r=(h-Math.floor(h))*2-1;pts+=x.toFixed(1)+','+(this.cy+A*r).toFixed(1)+' ';}
   this.p.setAttribute('points',pts);this.p.setAttribute('opacity',ease(clamp(u/.4)));}},
 steps:{init(P,C){const n=P.n||5,w=96,g=34,base=P.base||1440;this.bs=[];const x0=540-(n*w+(n-1)*g)/2;
   for(let i=0;i<n;i++){const h=90+i*(P.dh||62);this.bs.push([el('rect',{x:x0+i*(w+g),y:base,width:w,height:0,rx:6,fill:i==n-1?C.acc:C.dim,opacity:i==n-1?1:.85}),h,base]);}},
  update(u){this.bs.forEach(([r,h,base],i)=>{const p=ease(clamp((u-.15*i)/.7));r.setAttribute('height',h*p);r.setAttribute('y',base-h*p);});}}
};

let curGroup=null;
function build(si){
  const s=SC[si];cur=si;const C=s.theme;
  stage.style.background=C.bg;stage.style.setProperty('--ac',C.acc);
  txt.innerHTML='';words=[];txt.style.top=(s.txt_top||330)+'px';
  const JUST=s.style==='editorial'&&s.txt_align!=='center'&&!s.logo;txt.classList.toggle('justify',JUST);
  s.lines.forEach((l,li)=>{const row=document.createElement('div');row.className='ln';if(FAM!=='DoranFaNum')row.style.columnGap=(l.size*.27)+'px';
    l.words.forEach(w=>{const sp=document.createElement('span');sp.className='w'+(w.em?' em':'');sp.textContent=w.w;sp.dataset.t=w.t;sp.dataset.li=li;sp.dataset.em=w.em?1:0;
      sp.style.fontSize=l.size+'px';sp.style.fontWeight=l.weight;sp.style.color=l.dim?C.dim:C.fg;sp.style.opacity=0;if(JUST&&row.childNodes.length)row.appendChild(document.createTextNode(' '));row.appendChild(sp);words.push(sp);});
    if(JUST){row.classList.add('just');row.style.fontSize=l.size+'px';row.style.lineHeight='1.32';}
    txt.appendChild(row);});
  if(JUST){ // aligned block: each headline line is broken into rows that each fill the measure exactly (per-row size, best split chosen); body lines justified
    const M=txt.getBoundingClientRect().width;
    s.lines.forEach((l,li)=>{const row=txt.children[li];
      [...row.childNodes].forEach(n=>{if(n.nodeType===3)n.remove();});row.style.whiteSpace='nowrap';
      const ws=[...row.querySelectorAll('.w')];const sp=.26*l.size;const wl=ws.map(e=>e.getBoundingClientRect().width);const n=ws.length;
      const P=l.size>=150?[160,200,96]:l.weight>=700?[118,150,82]:l.size>=60?[62,76,48]:[46,54,44];const T=P[0],mx=P[1],mn=P[2];
      const width=(a,b)=>{let w=0;for(let i=a;i<b;i++)w+=wl[i]+(i<b-1?sp:0);return w;};
      let best=null;
      const tryS=cuts=>{const b=[0,...cuts,n];const sz=[];for(let g=0;g<b.length-1;g++)sz.push(Math.max(44,Math.min(mx,l.size*M/width(b[g],b[g+1]))));
        let cost=sz.reduce((a,x)=>a+Math.abs(Math.log(x/T)),0)+.8*Math.log(Math.max(...sz)/Math.min(...sz))+.12*(b.length-2)+sz.reduce((a,x)=>a+(x<mn?2+(mn-x)/10:0),0);
        for(let g=0;g<b.length-1;g++)if(b[g+1]-b[g]===1&&n>2)cost+=.6;
        if(!best||cost<best.cost)best={cost,b,sz};};
      tryS([]);for(let a=1;a<n;a++){tryS([a]);for(let c=a+1;c<n;c++){tryS([a,c]);}}
      const b=best.b;row.style.fontSize=Math.min(...best.sz)+'px';row.style.textAlignLast='';row.style.textAlign='start';
      for(let g=0;g<b.length-1;g++){const f=best.sz[g]*.99;for(let i=b[g];i<b[g+1];i++){ws[i].style.fontSize=f+'px';ws[i].style.marginInlineEnd=(i<b[g+1]-1)?(.26*f)+'px':'0';}
        if(g<b.length-2)ws[b[g+1]-1].after(document.createElement('br'));}
      l.size=Math.max(...best.sz);l.rows=b;l.szs=best.sz;});}
  txt.querySelectorAll('.w').forEach(e=>e.dataset.fs0=parseFloat(e.style.fontSize));
  let k=1;while(txt.getBoundingClientRect().height>SAFE_TXT_H && k>.55){k-=.04;txt.querySelectorAll('.w').forEach(e=>{e.style.fontSize=(e.dataset.fs0*k)+'px';});}
  const rowsOf=row=>new Set([...row.children].map(c=>Math.round(c.getBoundingClientRect().top))).size;
  if(!JUST)[...txt.children].forEach(row=>{const full=row.getBoundingClientRect().width,n0=rowsOf(row);if(n0<2)return;
    let lo=full*.35,hi=full;for(let i=0;i<14;i++){const mid=(lo+hi)/2;row.style.maxWidth=mid+'px';if(rowsOf(row)>n0)lo=mid;else hi=mid;}row.style.maxWidth=hi+'px';});
  window.__fit=k;
  const g=s.motif&&s.motif.group||null;
  if(!(g&&g===curGroup&&M)){svg.innerHTML='';M=null;curGroup=null;
    if(s.motif){M=Object.create(MOTIFS[s.motif.type]);M.init(s.motif.params||{},C);curGroup=g;}}
  logo.style.display=s.logo?'block':'none';if(s.logo)logo.src=s.theme.logo_url;const sg=document.getElementById('sig');sg.style.display=s.logo?'block':'none';sg.textContent=SIG;sg.style.color=C.fg;
  if(!JUST)txt.style.alignItems=s.txt_align==='right'?'flex-start':'center';else{txt.style.alignItems='stretch';txt.style.textAlign='';}
  if(!JUST)txt.style.textAlign=s.txt_align==='right'?'right':'center';[...txt.children].forEach(r=>r.style.justifyContent=s.txt_align==='right'?'flex-start':'center');
  if(window.buildVis)buildVis(s,si);
  if(s.image){imgwrap.style.display='block';bgimg.src=s.image.url;const h=C.bg,r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16),c=a=>`rgba(${r},${g},${b},${a})`;tint.style.background=`linear-gradient(180deg,${c(.9)} 0%,${c(.8)} 45%,${c(.6)} 70%,${c(.85)} 100%)`;}else{imgwrap.style.display='none';}
}
function render(t){
  let si=SC.findIndex(s=>t>=s.start&&t<s.end);if(si<0)si=SC.length-1;
  if(si!==cur)build(si);
  const s=SC[si],u=t-s.start,dur=s.end-s.start;
  words.forEach(e=>{const tw=parseFloat(e.dataset.t),p=ease(clamp((u-tw)/.42)),em=e.dataset.em==='1';
    const pop=em?1+.10*Math.sin(Math.PI*clamp((u-tw)/.5)):1;
    e.style.opacity=p;e.style.transform=`translateY(${(1-p)*30}px) scale(${pop})`;e.style.filter=`blur(${(1-p)*10}px)`;
    if(em)e.style.setProperty('--u',ease(clamp((u-tw-.3)/.4)));});
  const fade=Math.min(1,u/.14)*Math.min(1,(s.end-t)/.14);
  const mf=Math.min(s.m_in?Math.min(1,u/.14):1,s.m_out?Math.min(1,(s.end-t)/.14):1);
  txt.style.opacity=fade;svg.style.opacity=mf;logo.style.opacity=fade;imgwrap.style.opacity=fade;
  if(s.image){bgimg.style.transform=`scale(${1+.08*u/dur})`;}
  if(window.updateVis)updateVis(s,u,dur);
  if(M)M.update(t-s.mstart,dur);
  if(s.logo){const p=ease(clamp(u/.8));logo.style.transform=`translate(-50%,-50%) scale(${.94+.06*p})`;const q=ease(clamp((u-.6)/.6)),sg=document.getElementById('sig');sg.style.opacity=q*fade;sg.style.transform=`translateY(${(1-q)*20}px)`;}
}
window.render=render;
window.measure=function(){return {fit:window.__fit,words:words.map(e=>{const b=e.getBoundingClientRect();return {w:e.textContent,l:b.left,r:b.right,t:b.top,b:b.bottom,fs:parseFloat(e.style.fontSize),tt:parseFloat(e.dataset.t),li:parseInt(e.dataset.li)};}),
  fonts:[...new Set(words.map(e=>getComputedStyle(e).fontFamily))],font_ok:document.fonts.check('800 40px '+FAM),
  sig:(()=>{const e=document.getElementById('sig');if(e.style.display!=='block')return null;const b=e.getBoundingClientRect();return {text:e.textContent,t:b.top,b:b.bottom,font:getComputedStyle(e).fontFamily};})(),logo:document.getElementById('logo').style.display==='block'?(()=>{const b=document.getElementById('logo').getBoundingClientRect();return {l:b.left,r:b.right,t:b.top,b:b.bottom,nw:document.getElementById('logo').naturalWidth,nh:document.getElementById('logo').naturalHeight}})():null};};
"""


VIS_JS = (ROOT / "reel_visuals.js").read_text(encoding="utf8")


def page_html(scenes, lang="fa"):
    for s in scenes:
        s["theme"] = dict(s["theme"], logo_url=(ROOT / CFG["logo"]["files"][s["theme"]["logo"]]["path"]).as_uri())
        if s.get("image"):
            s["image"] = dict(s["image"], url=pathlib.Path(s["image"]["path"]).resolve().as_uri())
        for o in s.get("objects") or []:
            o["url"] = pathlib.Path(o["src"]).resolve().as_uri()
        for f in s.get("fx") or []:
            if f.get("lens"): f["lens_url"] = pathlib.Path(f["lens"]).resolve().as_uri()
    txt_h = 760
    DIR, ORIG = ("rtl", "right") if lang == "fa" else ("ltr", "left")
    FAM = "DoranFaNum" if lang == "fa" else CFG["fonts"]["latin"]["family"]
    START = "right" if lang == "fa" else "left"
    return f"""<!doctype html><html lang="{lang}" dir="{DIR}"><head><meta charset="utf-8"><style>{font_css()}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:'{FAM}';text-rendering:geometricPrecision;-webkit-font-smoothing:antialiased}}
#imgwrap{{position:absolute;inset:0;display:none;overflow:hidden}}
#bgimg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.05)}}
#tint{{position:absolute;inset:0}}
#bgfx{{position:absolute;inset:0;display:none}}
#objlayer,#fx{{position:absolute;inset:0;overflow:hidden}}
#objlayer{{z-index:1}}#fx{{z-index:2}}#txt,#logo,#sig{{z-index:3}}
.obj{{position:absolute;will-change:transform,opacity,filter}}
.obj img{{display:block;width:100%;height:auto}}
.obj.frame img{{height:100%;object-fit:cover;border-radius:18px;box-shadow:0 40px 70px rgba(0,0,0,.45)}}
.obj .reveal{{position:absolute;left:0;top:0;width:100%;height:auto}}
.obj.frame .reveal{{height:100%;object-fit:cover;border-radius:18px}}
.fxw{{position:absolute;white-space:nowrap;font-family:'{FAM}';direction:{DIR};will-change:transform,opacity,filter}}
.fxsvg{{position:absolute;inset:0;width:{W}px;height:{H}px}}
.fxlens{{position:absolute;filter:drop-shadow(0 30px 30px rgba(0,0,0,.3))}}
.card{{position:absolute;width:300px;height:420px;border-radius:22px;box-shadow:0 30px 50px rgba(0,0,0,.25)}}
#motif{{position:absolute;inset:0;width:{W}px;height:{H}px}}
#txt{{position:absolute;left:{SAFE['x0']}px;right:{W - SAFE['x1']}px;top:330px;display:flex;flex-direction:column;align-items:center;gap:34px;direction:{DIR};text-align:center}}
.ln{{display:flex;flex-wrap:wrap;justify-content:center;gap:0 .36em;line-height:1.4}}
#txt.justify{{left:96px;right:96px;gap:22px}}
.ln.just{{display:block;text-align:justify;text-align-last:{START};word-spacing:.02em;hyphens:none}}
.ln.just .w{{vertical-align:baseline}}
.w{{display:inline-block;position:relative;will-change:transform,opacity,filter}}
.em::after{{content:'';position:absolute;right:0;left:0;bottom:-2px;height:7px;border-radius:4px;background:var(--ac);transform:scaleX(var(--u,0));transform-origin:{ORIG}}}
#logo{{position:absolute;left:50%;top:760px;height:420px;width:auto;transform:translate(-50%,-50%);display:none}}
#sig{{position:absolute;left:0;right:0;top:1380px;text-align:center;font-weight:500;font-size:56px;letter-spacing:.02em;display:none;direction:{DIR}}}
</style></head><body><div id="stage"><div id="bgfx"></div><div id="imgwrap"><img id="bgimg"><div id="tint"></div></div><svg id="motif" viewBox="0 0 {W} {H}"></svg><div id="objlayer"></div><div id="fx"></div><div id="txt"></div><img id="logo"><div id="sig"></div></div>
<script>const FAM='{FAM}';const SC={json.dumps(scenes, ensure_ascii=False)};const SAFE_TXT_H={txt_h};const SIG={json.dumps(CFG['signature']['text'] if lang == 'fa' else CFG['signature']['text_en'], ensure_ascii=False)};{JS}</script><script>{VIS_JS}</script></body></html>"""


def main(reel_path, out_dir):
    reel = json.loads(pathlib.Path(reel_path).read_text(encoding="utf8"))
    out = pathlib.Path(out_dir).resolve() / reel["reel_id"]
    if out.exists(): shutil.rmtree(out)
    (out / "frames").mkdir(parents=True)
    scenes = schedule(reel)
    total = scenes[-1]["end"]
    html = page_html(json.loads(json.dumps(scenes)), reel.get("lang", "fa"))
    (out / "reel.html").write_text(html, encoding="utf8")
    metrics = {"fps": FPS, "size": [W, H], "safe": SAFE, "duration": total, "scenes": []}
    n = int(round(total * FPS))
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium") if pathlib.Path("/opt/pw-browsers/chromium").exists() else pw.chromium.launch()
        page = br.new_context(viewport={"width": W, "height": H}, device_scale_factor=1).new_page()
        page.goto((out / "reel.html").as_uri()); page.evaluate("Promise.all([300,400,500,800].flatMap(w=>[document.fonts.load(`${w} 40px BrandLatin`,'Brand'),document.fonts.load(`${w} 40px DoranFaNum`,'پول آدم')]))"); page.evaluate("document.fonts.ready"); page.wait_for_timeout(300)
        for s in scenes:  # layout metrics near the end of each scene, when every word is visible
            page.evaluate(f"render({s['end'] - 0.2})"); page.wait_for_timeout(200)
            m = page.evaluate("measure()"); m.update(scene=s["id"], start=s["start"], end=s["end"], bg=s["bg"]); metrics["scenes"].append(m)
        page.evaluate("cur=-1; if(window.resetVis) resetVis();")
        for i in range(n):
            page.evaluate(f"render({i / FPS})")
            page.screenshot(path=str(out / "frames" / f"{i:05d}.jpg"), type="jpeg", quality=95, clip={"x": 0, "y": 0, "width": W, "height": H})
        # cover frame: first scene, all words visible
        page.evaluate("cur=-1; if(window.resetVis) resetVis();")
        page.evaluate(f"render({scenes[0]['end'] - 0.2})"); page.screenshot(path=str(out / "cover.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
        br.close()
    (out / "reel_metrics.json").write_text(json.dumps(metrics, indent=1), encoding="utf8")
    reel_audio.synth(scenes, total, out / "audio.wav", reel.get("audio") or {})
    mp4 = out / f"{reel['reel_id']}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(out / "frames" / "%05d.jpg"), "-i", str(out / "audio.wav"),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", str(mp4)], check=True)
    shutil.rmtree(out / "frames")
    print("rendered", mp4, f"{total:.1f}s", mp4.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
