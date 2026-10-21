"""Deterministic Persian text normalisation + orthography lint (Posht-e-Bam style rules)."""
import re

ZWNJ = "‌"
AR2FA = str.maketrans({"ك": "ک", "ي": "ی", "ى": "ی", "ە": "ه", "ۀ": "هٔ"})
DIGITS = str.maketrans("0123456789٠١٢٣٤٥٦٧٨٩", "۰۱۲۳۴۵۶۷۸۹۰۱۲۳۴۵۶۷۸۹")


def normalize(s: str) -> str:
    s = s.translate(AR2FA).translate(DIGITS)
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\s+([،؛:؟!.])", r"\1", s)          # no space before punctuation
    s = re.sub(r"([،؛؟!])(?=[^\s\d«»)\]])", r"\1 ", s)  # one space after
    return s.strip()


# (pattern, message, severity)  -- severity: critical | warn
LINT = [
    (r"[كيى]", "حرف عربی (ك/ي/ى) به‌جای ک/ی", "critical"),
    (r"[0-9٠-٩]", "رقم لاتین یا عربی به‌جای رقم فارسی", "critical"),
    (r"(?<![‌])\bن?می (?=[؀-ۿ])", "«می» باید با نیم‌فاصله به فعل بچسبد", "critical"),
    (r"\bبی (?=[؀-ۿ])", "«بی» باید با نیم‌فاصله نوشته شود", "warn"),
    (r"\bهیچ (?=(?:کس|کدام|یک|گاه|جا|وقت|چیز|کجا)\b)", "«هیچ» باید با نیم‌فاصله نوشته شود", "warn"),
    (r"[؀-ۿ] (ها|های|هایی|تر|ترین)\b", "نشانه‌ی جمع/تفضیلی با فاصله‌ی کامل", "critical"),
    (r"\s[،؛:؟!]", "فاصله پیش از نشانه‌ی نگارشی", "critical"),
    (r"[،؛؟!:][^\s\d»)\]\n]", "نبودن فاصله پس از نشانه‌ی نگارشی", "warn"),
    (r"ه ی\b", "یای اضافه پس از «ه» باید با نیم‌فاصله باشد (ه‌ی)", "critical"),
    (r"\b(مثلن|واقعن|کاملن)\b", "تنوین را با «ن» ننویسید", "critical"),
    (r"[A-Za-z]", "حرف لاتین در متن فارسی", "warn"),
    (r"  +", "فاصله‌ی دوتایی", "warn"),
    (r"امارات|دبی|ابوظبی|ابوظـبی|شارجه|عجمان|فجیره|راس‌الخیمه|اماراتی|UAE|Dubai|Emirates", "نام امارات/دبی در متن ممنوع است", "critical"),
    (r"همچنین|در این راستا|لازم به ذکر|می‌توان گفت|به‌طور کلی|از سوی دیگر|در دنیای امروز|یکی از مهم‌ترین|گزارش داد|بر اساس پژوهش|آیا می‌دانستید", "عبارت خسته/خبری/ترجمه‌ای (copywriting.md)", "warn"),
    (r"فراتحلیل|اندازه‌ی اثر|معنی‌دار بودن آماری", "اصطلاح علمی در اسلاید؛ به زبان آدم ترجمه شود", "warn"),
]


def lint(s: str):
    out = []
    for pat, msg, sev in LINT:
        for m in re.finditer(pat, s):
            out.append({"severity": sev, "message": msg, "at": m.start(), "context": s[max(0, m.start() - 12): m.end() + 12]})
    return out
