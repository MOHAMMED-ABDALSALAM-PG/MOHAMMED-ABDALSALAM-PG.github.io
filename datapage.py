"""Figures and content for the Data page (Sudanese Arabic datasets and data collection).

Every number here comes from the author's papers and dataset cards:
- dialect corpus: hate-speech paper (IAENG IJCS revision), corpus section and table;
- hate-speech dataset: same paper (class counts, labelling functions, LLMs, human review);
- sentiment dataset: DATASET_CARD.md of the Sudanese sentiment framework.
Platform icons are generic drawings (no third-party logos).
"""
from html import escape as e

A = '<defs><marker id="{id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="currentColor"/></marker></defs>'

# generic 24x24 glyphs, drawn with strokes in currentColor
GLYPH = {
    "x": '<path d="M4 9h16M4 15h16M10 4 8 20M16 4l-2 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "telegram": '<path d="M21 4 3 11l6 2.5L19 7l-8 8 .5 5 3-3.5L19 20z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    "facebook": '<rect x="3.5" y="4" width="17" height="16" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M7 8.5h10M7 12h10M7 15.5h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "play": '<rect x="6" y="2.5" width="12" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m12 7.5 1.3 2.7 2.9.4-2.1 2 .5 2.9-2.6-1.4-2.6 1.4.5-2.9-2.1-2 2.9-.4z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="m8.5 12 2.4 2.4 4.6-4.8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "gear": '<circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.8v3M12 18.2v3M2.8 12h3M18.2 12h3M5.5 5.5l2.1 2.1M16.4 16.4l2.1 2.1M5.5 18.5l2.1-2.1M16.4 7.6l2.1-2.1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "db": '<ellipse cx="12" cy="5.5" rx="7.5" ry="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4.5 5.5v13c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-13M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    "clock": '<circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3.5 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "mask": '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4.5 20.5c1.2-3.8 4-5.5 7.5-5.5s6.3 1.7 7.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M3 3l18 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "ids": '<path d="M5 4h14v16H5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 8.5h2M8 12h2M8 15.5h2M12.5 8.5H16M12.5 12H16M12.5 15.5H16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "people": '<circle cx="8.5" cy="8.5" r="3" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="16.5" cy="9.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 19.5c.8-3.2 3-4.8 5.5-4.8s4.7 1.6 5.5 4.8M14.5 15c2.6-.4 5 .9 6 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "scale": '<path d="M12 4v16M7 20h10M5 7h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="m5 7-2.5 6h5zM19 7l-2.5 6h5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
}

SOURCES = [("x", "X (Twitter)", "s1"), ("telegram", "Telegram", "s3"), ("facebook", "Facebook pages", "s2"), ("play", "Google Play", "s4")]


def glyph(name, x, y, size=24, cls=""):
    k = size / 24
    return f'<g class="gl {cls}" transform="translate({x} {y}) scale({k:.3f})">{GLYPH[name]}</g>'


def html_icon(name, size=22):
    return f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{GLYPH[name]}</svg>'


# ------------------------------------------------------------------ overview figure
def _box(x, y, w, h, title, lines, cls="box", ic=None, ic_cls=""):
    out = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
    tx = x + 14
    if ic:
        out += glyph(ic, x + 12, y + 12, 22, ic_cls)
        tx = x + 44
    out += f'<text class="lbl" x="{tx}" y="{y + 29}">{title}</text>'
    for i, ln in enumerate(lines):
        out += f'<text class="note" x="{x + 14}" y="{y + 56 + i * 19}">{ln}</text>'
    return out


def flow_wide():
    s = [A.format(id="arD")]
    for i, (g, name, c) in enumerate(SOURCES):
        y = 16 + i * 66
        s.append(f'<rect class="box" x="6" y="{y}" width="150" height="54" rx="10"/>')
        s.append(glyph(g, 18, y + 15, 24, c))
        s.append(f'<text class="lbl" x="48" y="{y + 32}">{name.replace(" pages", "")}</text>')
        s.append(f'<path class="flow" d="M158 {y + 27} C168 {y + 27} 166 144 176 144" marker-end="url(#arD)"/>')
    s.append(_box(180, 40, 142, 208, "Collect", ["Python collectors", "public posts and", "reviews only", "throttled requests", "platform terms", "respected"], "box", "gear"))
    s.append('<path class="flow" d="M324 144 h14" marker-end="url(#arD)"/>')
    s.append(_box(342, 40, 142, 208, "Protect", ["emails, phones,", "links and user", "mentions removed", "deduplicated", "texts shared as", "IDs + labels"], "box accent", "shield"))
    for i, (t, n) in enumerate([("Dialect corpus", "6.76 M sentences"), ("Hate speech", "40,000 labelled"), ("Sentiment", "13,293 reviews")]):
        y = 16 + i * 92
        s.append(f'<path class="flow" d="M486 144 C494 144 492 {y + 38} 500 {y + 38}" marker-end="url(#arD)"/>')
        s.append(f'<rect class="box ds" x="504" y="{y}" width="130" height="76" rx="10"/>')
        s.append(glyph("db", 606, y + 38, 18))
        s.append(f'<text class="mono" x="516" y="{y + 24}">{t}</text>')
        s.append(f'<text class="lbl" x="516" y="{y + 52}">{n.split(" ")[0] + (" M" if " M " in n else "")}</text>')
        s.append(f'<text class="mono dim" x="516" y="{y + 68}">{n.split(" ")[-1]}</text>')
    return ('<svg class="wide-fig" viewBox="0 0 640 296" role="img" aria-labelledby="f-data-t"><title id="f-data-t">'
            'From public social-media posts and app reviews to three Sudanese Arabic datasets: collect, protect, label</title>'
            f'<g class="dg">{"".join(s)}</g></svg>')


def flow_narrow():
    s = [A.format(id="arDn")]
    for i, (g, name, c) in enumerate(SOURCES):
        x, y = 6 + (i % 2) * 168, 6 + (i // 2) * 62
        s.append(f'<rect class="box" x="{x}" y="{y}" width="160" height="52" rx="10"/>')
        s.append(glyph(g, x + 12, y + 14, 24, c))
        s.append(f'<text class="lbl" x="{x + 46}" y="{y + 31}">{name.replace(" pages", "")}</text>')
    s.append('<path class="flow" d="M170 124 v16" marker-end="url(#arDn)"/>')
    s.append(_box(6, 144, 328, 104, "Collect", ["Python collectors · public posts and", "reviews only · throttled requests ·", "platform terms respected"], "box", "gear"))
    s.append('<path class="flow" d="M170 250 v16" marker-end="url(#arDn)"/>')
    s.append(_box(6, 270, 328, 104, "Protect", ["emails, phones, links and user mentions", "removed · duplicates removed · texts", "shared as IDs + labels"], "box accent", "shield"))
    s.append('<path class="flow" d="M170 376 v16" marker-end="url(#arDn)"/>')
    for i, (t, n) in enumerate([("Dialect corpus", "6.76 M sentences"), ("Hate speech", "40,000 labelled"), ("Sentiment", "13,293 reviews")]):
        y = 396 + i * 56
        s.append(f'<rect class="box ds" x="6" y="{y}" width="328" height="46" rx="10"/>')
        s.append(glyph("db", 18, y + 13, 20))
        s.append(f'<text class="lbl" x="48" y="{y + 29}">{t}</text>')
        s.append(f'<text class="note" x="322" y="{y + 29}" text-anchor="end">{n}</text>')
    return ('<svg class="narrow-fig" viewBox="0 0 340 562" role="img" aria-labelledby="f-datan-t"><title id="f-datan-t">'
            'From public posts and reviews to three Sudanese Arabic datasets</title>'
            f'<g class="dg">{"".join(s)}</g></svg>')


def overview_figure():
    cap = ("How the data are built. Public posts and app reviews are collected with Python tools, personal details are removed, "
           "and the labelled data are shared as record identifiers and labels rather than raw texts. Icons are generic drawings.")
    return f'<figure class="diagram narrow">{flow_wide()}{flow_narrow()}<figcaption>{cap}</figcaption></figure>'


# ------------------------------------------------------------------ small charts for the dataset cards
def _rr(x, y, w, h, r=4):
    r = min(r, w / 2, h / 2)
    return (f"M{x + r:.1f},{y:.1f} H{x + w - r:.1f} Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} V{y + h - r:.1f} "
            f"Q{x + w:.1f},{y + h:.1f} {x + w - r:.1f},{y + h:.1f} H{x + r:.1f} Q{x:.1f},{y + h:.1f} {x:.1f},{y + h - r:.1f} "
            f"V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} Z")


def _stack(y, parts, total, x0=12, W=296, h=26, label=None):
    """One horizontal 100% bar; parts = [(name, count, slot)]; 2px gaps; tooltips; labels under each segment."""
    out, x = [], x0
    if label:
        out.append(f'<text class="cat" x="{x0}" y="{y - 8}">{label}</text>')
    gap = 2
    usable = W - gap * (len(parts) - 1)
    for i, (name, n, slot) in enumerate(parts):
        w = usable * n / total
        tip = f"{name}: {n:,} ({100 * n / total:.1f}%)"
        out.append(f'<path class="mark {slot}" d="{_rr(x, y, w, h)}" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title></path>')
        anchor, tx = ("start", x) if i == 0 else (("end", x + w) if i == len(parts) - 1 else ("middle", x + w / 2))
        out.append(f'<text class="val" x="{tx:.1f}" y="{y + h + 16}" text-anchor="{anchor}">{name}</text>')
        out.append(f'<text class="tick" x="{tx:.1f}" y="{y + h + 31}" text-anchor="{anchor}">{n:,}</text>')
        x += w + gap
    return "".join(out)


def chart_corpus():
    steps = [("Collected", 6755955, "6.76 M"), ("After cleaning", 4052505, "4.05 M"), ("Unique", 3409732, "3.41 M")]
    out = []
    for i, (name, n, short) in enumerate(steps):
        y = 14 + i * 40
        w = 200 * n / steps[0][1]
        tip = f"{name}: {n:,} sentences"
        out.append(f'<text class="cat" x="12" y="{y + 17}">{name}</text>')
        out.append(f'<path class="mark s1" d="{_rr(112, y, w, 24)}" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title></path>')
        out.append(f'<text class="val" x="{112 + w + 6:.1f}" y="{y + 17}">{short}</text>' if w < 160 else
                   f'<text class="val inv" x="{112 + w - 8:.1f}" y="{y + 17}" text-anchor="end">{short}</text>')
    return f'<svg viewBox="0 0 320 132" role="img" aria-label="Dialect corpus: 6,755,955 sentences collected, 4,052,505 after cleaning, 3,409,732 unique">{"".join(out)}</svg>'


def chart_hate():
    parts = [("Hate", 7425, "s2"), ("Offensive", 8780, "s4"), ("Neutral", 23795, "s1")]
    return f'<svg viewBox="0 0 320 96" role="img" aria-label="Hate-speech dataset: 7,425 hate, 8,780 offensive, 23,795 neutral sentences">{_stack(24, parts, 40000, label="Three classes · 40,000 sentences")}</svg>'


def chart_sentiment():
    cls = [("Positive", 5954, "s3"), ("Negative", 4265, "s2"), ("Neutral", 3074, "s1")]
    sec = [("Banking", 7347, "s1"), ("Telecom", 3446, "s4"), ("Transport", 2500, "s2")]
    return (f'<svg viewBox="0 0 320 190" role="img" aria-label="Sentiment dataset: 5,954 positive, 4,265 negative, 3,074 neutral; banking 7,347, telecom 3,446, transport 2,500">'
            f'{_stack(24, cls, 13293, label="Sentiment")}{_stack(118, sec, 13293, label="Sector")}</svg>')


DATASETS = [
    {
        "id": "corpus", "icon": "db", "kind": "Corpus", "name": "Sudanese Arabic dialect corpus",
        "big": "6.76 M", "unit": "sentences",
        "text": ("6,755,955 Sudanese Arabic sentences from X (Twitter) and Telegram, covering 2015–2020 and 2023–2025. "
                 "Cleaning keeps Sudanese-dialect text of 5–50 words and removes non-Sudanese content and Modern Standard Arabic "
                 "news headlines, leaving 4,052,505 sentences, of which 3,409,732 are unique. The hate-speech dataset is sampled from "
                 "these unique sentences."),
        "facts": ["X (Twitter) · Telegram", "2015–2020 · 2023–2025", "dialect filtering · deduplication"],
        "chart": chart_corpus, "avail": "Not publicly released — available on request for research collaboration", "public": False,
        "url": None,
    },
    {
        "id": "hate", "icon": "shield", "kind": "Labelled dataset", "name": "Sudanese Arabic hate-speech dataset",
        "big": "40,000", "unit": "sentences",
        "text": ("40,000 sentences sampled from the corpus (27,300 keyword-targeted, 12,700 random), labelled hate, offensive or neutral (and harmful vs neutral for the "
                 "binary task). Labels combine 40 Sudanese-specific weak-supervision rules with two large language models "
                 "(GPT-4o-mini and Llama-3.1-70B) by majority vote; three native speakers then reviewed a stratified sample of 10,000 sentences."),
        "facts": ["3 classes + binary", "40 rules + 2 LLMs", "10,000 human-reviewed"],
        "chart": chart_hate, "avail": "Public: record identifiers, splits and labels (texts are not redistributed)", "public": True,
        "url": "https://github.com/scander91/sudanese-hate-speech-detection/tree/main/data/ids",
    },
    {
        "id": "sentiment", "icon": "play", "kind": "Labelled dataset", "name": "Sudanese Arabic sentiment dataset",
        "big": "13,293", "unit": "reviews",
        "text": ("13,293 Sudanese Arabic Google Play reviews of eight banking, telecom and transport apps, labelled positive, negative "
                 "or neutral, with leakage-safe splits that keep near-duplicate reviews together. It reflects how customers talk about "
                 "real services, so it suits both research and customer-feedback analysis for companies."),
        "facts": ["8 apps · 3 sectors", "positive · negative · neutral", "leakage-safe splits"],
        "chart": chart_sentiment, "avail": "Available on request for research and for commercial or industry collaboration; terms agreed case by case", "public": False,
        "url": None,
    },
]


def dataset_card(d, email):
    facts = "".join(f"<li>{e(f)}</li>" for f in d["facts"])
    if d["url"]:
        btn = f'<a class="btn-link strong" href="{e(d["url"])}" rel="noopener">{html_icon("ids", 16)}<span>Get IDs and labels</span></a>'
    else:
        btn = f'<a class="btn-link strong" href="mailto:{email}?subject={e(d["name"])}">{html_icon("db", 16)}<span>Request by email</span></a>'
    return f"""<article class="ds-card" id="{d['id']}">
  <div class="ds-top"><span class="ds-ic">{html_icon(d['icon'], 22)}</span><div><p class="kind">{e(d['kind'])}</p><h3>{e(d['name'])}</h3></div>
  <p class="ds-big"><b>{d['big']}</b><span>{d['unit']}</span></p></div>
  <div class="ds-body"><div class="ds-main"><p>{e(d['text'])}</p>
  <ul class="ds-facts">{facts}</ul>
  <p class="avail {'public' if d['public'] else 'private'}"><span class="dot" aria-hidden="true"></span>{e(d['avail'])}</p>
  <div class="proj-foot">{btn}</div></div>
  <figure class="chart ds-chart">{d['chart']()}</figure></div>
</article>"""


COLLECT = [
    ("x", "s1", "X (Twitter)", "Public posts in Sudanese Arabic, used in the dialect corpus and the hate-speech dataset."),
    ("telegram", "s3", "Telegram", "Sudanese Arabic messages from 2015–2020 and 2023–2025; the recent posts capture conflict-era vocabulary."),
    ("facebook", "s2", "Facebook pages", "Posts from public news, media and telecom pages, collected with a browser-based Python scraper."),
    ("play", "s4", "Google Play", "Public app reviews collected with the open-source google-play-scraper library."),
]

ETHICS = [
    ("scale", "Public content and platform rules", "Only publicly visible posts and reviews are collected, following each platform's terms of use."),
    ("clock", "Polite, throttled collection", "Collectors wait between requests and page loads instead of flooding a website."),
    ("mask", "Personal data removed", "Emails, phone numbers, links and user mentions are replaced with placeholder tokens; annotation looks at the text, not at who wrote it."),
    ("ids", "No raw texts redistributed", "Released data are record identifiers, splits and labels, subject to the platforms' terms of service."),
    ("people", "Care for annotators", "Reviewers were told the material could contain offensive and conflict-related language and could stop at any time."),
    ("gear", "Reproducible pipeline", "Deduplication by text hash, documented cleaning steps, and fixed, leakage-safe train / validation / test splits."),
]


def collect_html():
    src = "".join(f'<li class="{c}"><span class="src-ic">{html_icon(g, 22)}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for g, c, t, d in COLLECT)
    eth = "".join(f'<li><span class="eth-ic">{html_icon(g, 20)}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for g, t, d in ETHICS)
    return src, eth
