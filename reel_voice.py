"""Voice-over for reels (Azure Speech neural voices) + ducking mix under the music bed.
Needs environment variables AZURE_SPEECH_KEY and AZURE_SPEECH_REGION, and network access to
<region>.tts.speech.microsoft.com. Without them the reel renders without a voice and QA reports it.

Reel JSON: "voice": {"enabled": true, "voice": "fa-IR-FaridNeural", "rate": "-6%", "pitch": "-3%"}
Scene JSON (optional): "vo": "the exact sentence to speak" (default: the scene's lines, *markers* removed).
Clips are cached in out/_vo_cache/ by text+voice hash, so re-renders do not call the service again."""
import os, json, hashlib, pathlib, wave, urllib.request
from xml.sax.saxutils import escape
import numpy as np

SR = 44100
DEFAULT_VOICE = {"fa": "fa-IR-FaridNeural", "en": "en-US-AndrewNeural"}
LANG_TAG = {"fa": "fa-IR", "en": "en-US"}


def scene_text(sc):
    if "vo" in sc: return sc["vo"]
    return " ".join(l["text"].replace("*", "") for l in sc.get("lines", []))


def _azure(text, voice, lang, rate, pitch):
    key, region = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region: raise RuntimeError("AZURE_SPEECH_KEY / AZURE_SPEECH_REGION not set")
    ssml = (f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{LANG_TAG[lang]}'>"
            f"<voice name='{voice}'><prosody rate='{rate}' pitch='{pitch}'>{escape(text)}</prosody></voice></speak>")
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml.encode("utf8"), method="POST",
                                 headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
                                          "X-Microsoft-OutputFormat": "riff-44100hz-16bit-mono-pcm", "User-Agent": "yima-reels"})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()


def _read(path):
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768
        assert w.getframerate() == SR
    nz = np.where(np.abs(x) > 0.004)[0]  # trim leading/trailing silence
    return x[max(0, nz[0] - 400): nz[-1] + 2000] if len(nz) else x


def prepare(reel, out_root):
    """Synthesise one clip per scene. Returns ({scene_id: samples}, status). Sets sc['vo_dur'] on the reel scenes."""
    v = reel.get("voice") or {}
    if not v.get("enabled"): return {}, "voice disabled"
    lang = reel.get("lang", "fa"); voice = v.get("voice", DEFAULT_VOICE[lang])
    cache = pathlib.Path(out_root) / "_vo_cache"; cache.mkdir(parents=True, exist_ok=True)
    clips = {}
    try:
        for sc in reel["scenes"]:
            text = scene_text(sc).strip()
            if not text: continue
            h = hashlib.sha1(json.dumps([text, voice, v.get("rate", "-6%"), v.get("pitch", "-3%")], ensure_ascii=False).encode()).hexdigest()[:16]
            f = cache / f"{h}.wav"
            if not f.exists(): f.write_bytes(_azure(text, voice, lang, v.get("rate", "-6%"), v.get("pitch", "-3%")))
            clips[sc["id"]] = _read(f); sc["vo_dur"] = round(len(clips[sc["id"]]) / SR, 3)
    except Exception as e:  # never fake a voice: render without it and say why
        for sc in reel["scenes"]: sc.pop("vo_dur", None)
        return {}, f"voice failed: {e}"
    return clips, f"voice ok: {voice}, {len(clips)} clips"


def mix(audio_path, scenes, clips, lead=0.18):
    """Place each clip at its scene start, duck the music under the voice, keep peak below -1.4 dBFS."""
    if not clips: return
    with wave.open(str(audio_path)) as w:
        music = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768
    vo = np.zeros_like(music)
    for s in scenes:
        c = clips.get(s["id"])
        if c is None: continue
        i = int((s["start"] + lead) * SR); j = min(len(vo), i + len(c)); vo[i:j] += c[: j - i]
    vo = vo / (np.abs(vo).max() + 1e-9) * 0.92
    env = np.convolve(np.abs(vo), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    env = np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
    out = music * (1 - 0.72 * env) * 0.8 + vo
    out = out / (np.abs(out).max() + 1e-9) * 0.84
    pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
    with wave.open(str(audio_path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
