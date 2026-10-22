// Editorial visual layer (objects + topic typography). Loaded by reel_render.py after the motif JS.
// Pure function of time per scene: buildVis(scene, sequential) on scene change, updateVis(scene, u, dur) every frame.
// Objects are monochrome cut-outs (or framed footage) with soft shadows; an object with the same `key` in consecutive
// scenes is carried (it glides from its last state to the new one instead of re-entering) = one continuous camera.
const objlayer = document.getElementById('objlayer'), fx = document.getElementById('fx'), bgfx = document.getElementById('bgfx');
const lerp = (a, b, p) => a + (b - a) * p;
let OBJ = {}, FX = [], lastVis = -2;
function rnd(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
function hexA(h, a) { const r = parseInt(h.slice(1, 3), 16), g = parseInt(h.slice(3, 5), 16), b = parseInt(h.slice(5, 7), 16); return `rgba(${r},${g},${b},${a})`; }
function pathAt(path, u) { // path: [[t,x,y],...] -> {x,y}
  if (!path || !path.length) return null; if (u <= path[0][0]) return { x: path[0][1], y: path[0][2] };
  for (let i = 1; i < path.length; i++) { const a = path[i - 1], b = path[i]; if (u <= b[0]) { const p = easeIO((u - a[0]) / Math.max(.001, b[0] - a[0])); return { x: lerp(a[1], b[1], p), y: lerp(a[2], b[2], p) }; } }
  const l = path[path.length - 1]; return { x: l[1], y: l[2] };
}
function resetVis() { objlayer.innerHTML = ''; fx.innerHTML = ''; OBJ = {}; FX = []; lastVis = -2; }
window.resetVis = resetVis;

function buildVis(s, si) {
  const C = s.theme, dark = s.bg !== 'paper', sequential = (si === lastVis + 1); lastVis = si;
  // background: paper = fine grid + vignette; dark = soft spotlight where the object sits
  if (s.style === 'editorial') {
    const sy = (s.spot_y || 1180);
    bgfx.style.background = dark
      ? `radial-gradient(ellipse 620px 560px at 540px ${sy}px, ${hexA('#ffffff', .10)} 0%, ${hexA('#ffffff', .04)} 45%, rgba(0,0,0,0) 75%), radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.35) 100%)`
      : `radial-gradient(ellipse at 50% 45%, rgba(255,255,255,.55) 0%, rgba(0,0,0,0) 60%, rgba(0,0,0,.10) 100%), repeating-linear-gradient(0deg, ${hexA(C.fg, .045)} 0 2px, transparent 2px 96px), repeating-linear-gradient(90deg, ${hexA(C.fg, .045)} 0 2px, transparent 2px 96px)`;
    bgfx.style.display = 'block';
  } else bgfx.style.display = 'none';
  // objects (carry by key)
  const keep = new Set();
  (s.objects || []).forEach((o, i) => {
    const k = o.key || (s.id + '_' + i); keep.add(k);
    let e = OBJ[k];
    const carry = o.carry_in && e && sequential;
    if (!e) {
      const w = document.createElement('div'); w.className = 'obj' + (o.frame ? ' frame' : '');
      const im = document.createElement('img'); im.src = o.url; w.appendChild(im);
      let rv = null; if (o.reveal) { rv = document.createElement('img'); rv.src = o.url; rv.className = 'reveal'; w.appendChild(rv); }
      objlayer.appendChild(w); e = OBJ[k] = { w, im, rv };
    } else if (o.reveal && !e.rv) { e.rv = document.createElement('img'); e.rv.src = o.url; e.rv.className = 'reveal'; e.w.appendChild(e.rv); }
    if (e.rv && !o.reveal) { e.rv.remove(); e.rv = null; }
    e.from = carry ? e.last : null; e.o = o; e.w.style.zIndex = o.z || 1;
    e.im.style.objectPosition = o.crop_pos || '50% 50%';
  });
  for (const k in OBJ) if (!keep.has(k)) { OBJ[k].w.remove(); delete OBJ[k]; }
  // typographic / vector effects
  fx.innerHTML = ''; FX = [];
  (s.fx || []).forEach(f => { const F = Object.create(FXS[f.type]); F.init(f, C, dark); FX.push(F); });
}

function updateVis(s, u, dur) {
  const fadeIn = Math.min(1, u / .14), fadeOut = Math.min(1, (dur - u) / .14), dark = s.bg !== 'paper';
  for (const k in OBJ) {
    const e = OBJ[k], o = e.o, d = o.delay || 0;
    const P = pathAt(o.path, u);
    const tgt = { x: P ? P.x : o.x, y: P ? P.y : o.y, w: o.w, rot: o.rot || 0, blur: o.blur ? o.blur[0] : 0, op: 1, sc: 1 };
    let st;
    if (e.from) { const p = easeIO(clamp(u / (o.carry_t || .9))); st = {}; for (const q in tgt) st[q] = lerp(e.from[q], tgt[q], p); if (P) { st.x = tgt.x; st.y = tgt.y; } }
    else {
      st = { ...tgt }; const p = ease(clamp((u - d) / (o.in || .8)));
      switch (o.anim || 'fade') {
        case 'drop': st.y -= (1 - p) * 300; st.rot += (1 - p) * -10; st.op = clamp((u - d) / .25); break;
        case 'rise': st.y += (1 - p) * 140; st.op = p; break;
        case 'zoom': st.sc = .82 + .18 * p; st.op = p; break;
        case 'slide_r': st.x += (1 - p) * 900; break;
        case 'slide_l': st.x -= (1 - p) * 900; break;
        case 'pop': st.sc = p < 1 ? .6 + .4 * p + .06 * Math.sin(Math.PI * p) : 1; st.op = clamp(p * 2); break;
        default: st.op = p;
      }
    }
    // life inside the scene
    if (o.blur) { const [b0, b1, t0, t1] = [o.blur[0], o.blur[1], o.blur[2] ?? .8, o.blur[3] ?? dur - .6]; st.blur = lerp(b0, b1, easeIO(clamp((u - t0) / Math.max(.1, t1 - t0)))); if (e.from) st.blur = lerp(e.from.blur, st.blur, easeIO(clamp(u / .9))); }
    if (o.push) st.sc *= 1 + o.push * u / dur;
    if (o.float) st.y += Math.sin(u * 1.7) * o.float;
    if (o.vibrate) { const a = o.vibrate * (o.vib_decay ? Math.max(0, 1 - u / dur) : 1) * clamp((u - (o.vib_t || .4)) / .2); st.x += Math.sin(u * 57) * a; st.rot += Math.sin(u * 43) * a * .08; }
    if (o.tilt) st.rot += o.tilt * easeIO(clamp((u - (o.tilt_t || 1)) / 1.2));
    if (o.exit) { const p = easeIO(clamp((u - o.exit[1]) / .8)); if (o.exit[0] === 'left') st.x -= p * 1000; else if (o.exit[0] === 'right') st.x += p * 1000; else if (o.exit[0] === 'up') { st.y -= p * 700; st.rot -= p * 25; } else st.op *= 1 - p; }
    if (!o.carry_in || !e.from) st.op *= fadeIn > 0 ? Math.min(1, fadeIn + (e.from ? 1 : 0)) : 0;
    if (!o.carry_out) st.op *= fadeOut;
    e.last = st;
    const W = e.w; W.style.width = st.w + 'px'; W.style.left = st.x + 'px'; W.style.top = st.y + 'px';
    if (o.ar) W.style.height = (st.w / o.ar) + 'px';
    W.style.transform = `translate(-50%,-50%) rotate(${st.rot}deg) scale(${st.sc})`; W.style.opacity = st.op;
    const sh = dark ? 'drop-shadow(0 40px 50px rgba(0,0,0,.55))' : 'drop-shadow(0 34px 34px rgba(30,30,30,.22)) drop-shadow(0 6px 8px rgba(30,30,30,.18))';
    const gray = o.color ? lerp(o.color[0], o.color[1], easeIO(clamp((u - (o.color[2] || .6)) / 1.2))) : 1;
    const bright = o.bright ? lerp(o.bright[0], o.bright[1], easeIO(clamp((u - .6) / (dur - 1.2)))) : 1;
    e.im.style.filter = `grayscale(${gray}) contrast(1.06) brightness(${bright}) blur(${st.blur}px)`;
    W.style.filter = o.frame ? '' : sh;
    if (e.rv) { // sharp copy inside a moving circle (magnifier)
      const R = o.reveal, Q = pathAt(R.path, u) || { x: R.x, y: R.y };
      const bx = W.getBoundingClientRect(), sx = bx.width / W.offsetWidth || 1;
      const cx = (Q.x - bx.left) / sx, cy = (Q.y - bx.top) / sx, rr = R.r / sx;
      e.rv.style.filter = `grayscale(${gray}) contrast(1.1) brightness(1.05)`; e.rv.style.clipPath = `circle(${rr * ease(clamp((u - (R.t || .3)) / .5))}px at ${cx}px ${cy}px)`;
      e.rv.style.transform = `scale(1)`;
    }
  }
  FX.forEach(F => F.update(u, dur, fadeIn * fadeOut));
}

// ---------- effects ----------
function word(txt, x, y, size, color, weight) {
  const sp = document.createElement('span'); sp.className = 'fxw'; sp.textContent = txt;
  sp.style.left = x + 'px'; sp.style.top = y + 'px'; sp.style.fontSize = size + 'px'; sp.style.color = color; sp.style.fontWeight = weight || 500;
  fx.appendChild(sp); return sp;
}
function scatter(n, box, seed) { // jittered grid positions inside box [x0,y0,x1,y1]
  const r = rnd(seed || 7), cols = Math.max(2, Math.round(Math.sqrt(n * (box[2] - box[0]) / (box[3] - box[1])))), rows = Math.ceil(n / cols), out = [];
  const cw = (box[2] - box[0]) / cols, ch = (box[3] - box[1]) / rows;
  for (let i = 0; i < n; i++) { const c = i % cols, rr = Math.floor(i / cols); out.push([box[0] + cw * (c + .5) + (r() - .5) * cw * .5, box[1] + ch * (rr + .5) + (r() - .5) * ch * .5]); }
  for (let i = out.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [out[i], out[j]] = [out[j], out[i]]; }
  return out;
}
const FXS = {
  // words of the topic as a visual. mode: fade (forgetting) | absorb (into target) | sift (fall, only keep stays) | lens (magnifier reveals) | pop (chaotic choices)
  words: {
    init(f, C, dark) {
      this.f = f; this.C = C; const box = f.box || [110, 900, 970, 1460], pos = scatter(f.words.length, box, f.seed);
      if (f.keep_at) f.words.forEach((t, i) => { if ((f.keep || []).includes(t)) pos[i] = f.keep_at; });
      const keep = new Set(f.keep || []); this.ws = f.words.map((t, i) => ({ t, k: keep.has(t), p: pos[i], e: word(t, pos[i][0], pos[i][1], (f.size || 46) * (keep.has(t) ? 1.15 : 1), keep.has(t) ? C.acc : C.fg, keep.has(t) ? 800 : 400) }));
      if (f.mode === 'lens') { const im = document.createElement('img'); im.src = f.lens_url; im.className = 'fxlens'; im.style.width = (f.lens_w || 520) + 'px'; fx.appendChild(im); this.lens = im; }
    },
    update(u, dur, a) {
      const f = this.f, n = this.ws.length;
      this.ws.forEach((w, i) => {
        const tin = .15 + i * (f.stagger ?? .05); let op = ease(clamp((u - tin) / .4)), x = w.p[0], y = w.p[1], sc = 1, bl = 0;
        if (f.mode === 'fade') { const t0 = (f.t0 || 1.0) + i * ((dur - 1.6 - (f.t0 || 1)) / n); const q = easeIO(clamp((u - t0) / .9)); if (!w.k) { op *= 1 - .9 * q; bl = 9 * q; y -= 30 * q; } else { sc = 1 + .25 * q; } }
        if (f.mode === 'absorb') { const t0 = (f.t0 || .8) + i * ((dur - 1.4 - (f.t0 || .8)) / n), q = easeIO(clamp((u - t0) / .8)); x = lerp(x, f.target[0], q); y = lerp(y, f.target[1], q); sc = 1 - .8 * q; op *= 1 - q * q; }
        if (f.mode === 'sift') { const t0 = .3 + i * ((dur - 1.6) / n), q = clamp((u - t0) / 1.1), yy = lerp(f.box[1] - 120, f.target[1], easeIO(q)); x = lerp(w.p[0], f.target[0] + (w.k ? 0 : (w.p[0] - 540) * .3), q * .9); y = yy; op = ease(clamp((u - t0) / .3)); if (!w.k && q > .75) op *= 1 - (q - .75) / .25; if (w.k) { sc = 1 + .3 * clamp((u - t0 - 1.1) / .4); } }
        if (f.mode === 'pop') { const r = Math.sin(i * 12.9898) * 43758.5453 % 1; sc = .9 + .2 * Math.abs(r); w.e.style.color = (i % 3 === 0) ? this.C.acc : this.C.fg; op *= .55 + .45 * Math.abs(Math.sin(u * 2 + i)); }
        if (f.mode === 'lens') { const L = pathAt(f.path, u), d = Math.hypot(x - L.x, y - L.y), R = f.r || 150, q = clamp(1 - d / R); op *= .38 + .62 * q; bl = 3 * (1 - q); sc = 1 + .45 * q; if (w.k) { const fin = clamp((u - (f.hit_t || dur - 1.4)) / .5); sc = Math.max(sc, 1 + .6 * fin); op = Math.max(op, fin); bl = bl * (1 - fin); } }
        w.e.style.left = x + 'px'; w.e.style.top = y + 'px';
        w.e.style.opacity = op * a; w.e.style.transform = `translate(-50%,-50%) scale(${sc})`; w.e.style.filter = bl ? `blur(${bl}px)` : '';
      });
      if (this.lens) { const L = pathAt(f.path, u), lw = f.lens_w || 520, lh = lw * (f.lens_ar || .755); this.lens.style.left = (L.x - lw * (f.lens_cx || .74)) + 'px'; this.lens.style.top = (L.y - lh * (f.lens_cy || .30)) + 'px'; this.lens.style.opacity = a * ease(clamp(u / .5)); }
    }
  },
  // labels hovering over the two pans of a balance; side 'up' floats away, 'down' settles
  labels: {
    init(f, C) { this.f = f; this.ls = f.items.map(it => ({ it, e: word(it.text, it.x, it.y, it.size || 50, it.acc ? C.acc : C.fg, it.acc ? 800 : 500) })); },
    update(u, dur, a) { this.ls.forEach(({ it, e }, i) => { const p = ease(clamp((u - .4 - i * .3) / .5)), q = easeIO(clamp((u - (it.t || 1.6)) / 1.2)); const dy = it.move === 'up' ? -120 * q : it.move === 'down' ? 40 * q : 0; e.style.opacity = a * p * (it.move === 'up' ? 1 - .7 * q : 1); e.style.transform = `translate(-50%,-50%) translateY(${dy + (1 - p) * 20}px)`; }); }
  },
  // sound: concentric ripples from a point (inward=true: they converge = listening)
  rings: {
    init(f, C) { this.f = f; this.svg = document.createElementNS(NS, 'svg'); this.svg.setAttribute('viewBox', '0 0 1080 1920'); this.svg.setAttribute('class', 'fxsvg'); fx.appendChild(this.svg); this.cs = []; for (let i = 0; i < (f.n || 6); i++) this.cs.push(el('circle', { cx: f.x, cy: f.y, r: 10, fill: 'none', stroke: f.color || C.fg, 'stroke-width': f.sw || 3 }, this.svg)); },
    update(u, dur, a) { const f = this.f, per = f.period || 1.2, R = f.R || 420; this.cs.forEach((c, i) => { let ph = ((u - (f.t || .3)) / per + i / this.cs.length) % 1; if (u < (f.t || .3)) ph = -1; if (f.inward) ph = 1 - ph; const v = ph < 0 ? 0 : ph; c.setAttribute('r', 20 + R * v); c.setAttribute('opacity', ph < 0 ? 0 : a * (1 - v) * (f.op || .55)); }); }
  },
  // camera viewfinder over footage: corner brackets + recording dot
  viewfinder: {
    init(f, C) { this.f = f; this.svg = document.createElementNS(NS, 'svg'); this.svg.setAttribute('viewBox', '0 0 1080 1920'); this.svg.setAttribute('class', 'fxsvg'); fx.appendChild(this.svg); const [x0, y0, x1, y1] = f.box, L = 70, s = { fill: 'none', stroke: C.fg, 'stroke-width': 6, 'stroke-linecap': 'round' };
      this.g = el('g', {}, this.svg); [[x0, y0, 1, 1], [x1, y0, -1, 1], [x0, y1, 1, -1], [x1, y1, -1, -1]].forEach(([x, y, dx, dy]) => el('path', { ...s, d: `M${x} ${y + dy * L} L${x} ${y} L${x + dx * L} ${y}` }, this.g));
      this.dot = el('circle', { cx: x1 - 60, cy: y0 + 60, r: 16, fill: C.acc }, this.svg); },
    update(u, dur, a) { const p = ease(clamp((u - (this.f.t || .6)) / .6)); this.g.setAttribute('opacity', a * p); this.g.setAttribute('transform', `translate(540 ${(this.f.box[1] + this.f.box[3]) / 2}) scale(${1.15 - .15 * p}) translate(-540 ${-(this.f.box[1] + this.f.box[3]) / 2})`); this.dot.setAttribute('opacity', a * p * (Math.sin(u * 6) > 0 ? 1 : .15)); }
  },
  // colour cards: red leaves, black and white arrive (identity change)
  swatch: {
    init(f, C) { this.f = f; const mk = (bg, bd) => { const d = document.createElement('div'); d.className = 'card'; d.style.background = bg; d.style.border = bd; fx.appendChild(d); return d; };
      this.red = mk('#D3263A', 'none'); this.blk = mk('#151515', 'none'); this.wht = mk('#FFFFFF', '2px solid rgba(0,0,0,.08)'); },
    update(u, dur, a) { const y = this.f.y || 1180, t = this.f.t || 1.4, p = ease(clamp(u / .6)), q = easeIO(clamp((u - t) / .9)), r = ease(clamp((u - t - .4) / .8));
      const put = (d, x, yy, rot, op) => { d.style.left = x + 'px'; d.style.top = yy + 'px'; d.style.transform = `translate(-50%,-50%) rotate(${rot}deg)`; d.style.opacity = op * a; };
      put(this.red, 540 - 1000 * q, y + (1 - p) * 80, -4 - 20 * q, p);
      put(this.blk, 430 + (1 - r) * 700, y + 20, -6 + 6 * r, r); put(this.wht, 650 + (1 - r) * 900, y - 20, 5 - 3 * r, r); }
  },
  // a sound wave that settles into a single signature stroke
  signature: {
    init(f, C) { this.f = f; this.svg = document.createElementNS(NS, 'svg'); this.svg.setAttribute('viewBox', '0 0 1080 1920'); this.svg.setAttribute('class', 'fxsvg'); fx.appendChild(this.svg); this.p = el('path', { fill: 'none', stroke: C.fg, 'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, this.svg); this.u = el('path', { fill: 'none', stroke: C.acc, 'stroke-width': 8, 'stroke-linecap': 'round', d: '', pathLength: 1, 'stroke-dasharray': '1 1' }, this.svg); },
    update(u, dur, a) { const y = this.f.y || 1180, m = easeIO(clamp((u - 1.0) / 1.6)), draw = ease(clamp(u / 1.0)); let d = '';
      for (let i = 0; i <= 120; i++) { const t = i / 120, x = 120 + 840 * t; if (t > draw) break; const wave = Math.sin(t * 46 + u * 9) * 110 * Math.sin(Math.PI * t) * (.6 + .4 * Math.sin(t * 7)); const sig = Math.sin(t * 9.4) * 70 * Math.sin(Math.PI * t) + Math.sin(t * 3.1) * 30; d += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + (y + lerp(wave, sig, m)).toFixed(1); }
      this.p.setAttribute('d', d); this.p.setAttribute('opacity', a); this.u.setAttribute('d', `M260 ${y + 150} L820 ${y + 150}`); this.u.setAttribute('stroke-dashoffset', 1 - ease(clamp((u - 2.4) / .6))); this.u.setAttribute('opacity', a); }
  },
  // wood grain: wavy parallel lines drawn in (craft, material)
  grain: {
    init(f, C) { this.f = f; this.svg = document.createElementNS(NS, 'svg'); this.svg.setAttribute('viewBox', '0 0 1080 1920'); this.svg.setAttribute('class', 'fxsvg'); fx.appendChild(this.svg); this.ls = []; const y0 = f.y0 || 980, n = f.n || 14;
      for (let i = 0; i < n; i++) { let d = ''; for (let k = 0; k <= 60; k++) { const x = 60 + k * 16, yy = y0 + i * 34 + Math.sin(k / 6 + i * .7) * 14 + Math.exp(-Math.pow((k - 30) / 7, 2)) * 60 * Math.sin(i / n * Math.PI) ; d += (k ? 'L' : 'M') + x + ' ' + yy.toFixed(1); }
        this.ls.push(el('path', { d, fill: 'none', stroke: C.fg, 'stroke-width': i % 4 === 0 ? 4 : 2, opacity: .7, pathLength: 1, 'stroke-dasharray': '1 1', 'stroke-dashoffset': 1 }, this.svg)); } },
    update(u, dur, a) { this.ls.forEach((l, i) => { l.setAttribute('stroke-dashoffset', 1 - ease(clamp((u - .3 - i * .06) / 1.4))); l.setAttribute('opacity', .55 * a); }); }
  }
};
window.buildVis = buildVis; window.updateVis = updateVis;
