#!/usr/bin/env python3
"""Static site generator for the academic website.

Standard library only. Reads data/*.json and writes the site to dist/.
Run:  python3 build.py            (outputs dist/)
"""
import html
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

import figures

figures.PAPER_FIG.update({"abdalsalam_pmoo": "pmoo", "abdalsalam_s175": "s175", "abdalsalam_swr_review": "swr", "abdalsalam_gtd_fusion": "fusion"})

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

PROFILE = json.loads((ROOT / "data/profile.json").read_text())
PUBS = json.loads((ROOT / "data/publications.json").read_text())
PROJ = json.loads((ROOT / "data/projects.json").read_text())
RES = json.loads((ROOT / "data/resources.json").read_text())
GH_PATH = ROOT / "data/github.json"
GH = json.loads(GH_PATH.read_text()) if GH_PATH.exists() else {"repos": {}, "retrieved_at": None}

SITE = PROFILE["site_url"].rstrip("/")
TOPICS = PUBS["topics"]
TOPIC_ORDER = ["maritime-hpc", "arabic-nlp", "security-analytics", "networking"]
TOPIC_SLOT = {t: i + 1 for i, t in enumerate(TOPIC_ORDER)}
SELF_NAMES = {"Mohammed Abdalsalam", "Mohammed ALfatih", "Mohammed Alfatih O. Abdalsalam"}
BUILD_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

e = html.escape


# --------------------------------------------------------------------------- helpers
def icon(name, size=18):
    paths = {
        "github": '<path d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.71 1.26 3.37.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z" fill="currentColor"/>',
        "orcid": '<circle cx="12" cy="12" r="11" fill="currentColor"/><path d="M8.2 7.3a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Zm-.7 1.3h1.4v8.6H7.5V8.6Zm3.4 0h3.3c3.1 0 4.5 2.2 4.5 4.3 0 2.3-1.8 4.3-4.5 4.3h-3.3V8.6Zm1.4 7.3h1.8c2.6 0 3.2-2 3.2-3 0-1.7-1.1-3-3.2-3h-1.8v6Z" fill="var(--surface)"/>',
        "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5" fill="none" stroke="currentColor" stroke-width="1.8"/>',
        "doc": '<path d="M6 2.8h8l4 4V21.2H6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M14 2.8v4h4M8.8 12h6.4M8.8 15.5h6.4" fill="none" stroke="currentColor" stroke-width="1.8"/>',
        "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M13.5 4l-3 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "sun": '<circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
        "moon": '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
        "data": '<ellipse cx="12" cy="5.5" rx="7.5" ry="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4.5 5.5v13c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-13M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    }
    return f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{paths[name]}</svg>'


def authors_html(authors):
    out = []
    for a in authors:
        if a in SELF_NAMES or a.startswith("Mohammed Alfatih"):
            out.append(f'<strong class="me">{e(a)}</strong>')
        else:
            out.append(e(a))
    return ", ".join(out)


def link_btn(url, label, ic="ext", cls="btn-link"):
    return f'<a class="{cls}" href="{e(url)}" rel="noopener" target="_blank">{icon(ic, 15)}<span>{e(label)}</span></a>'


NAV = [("/research/", "Research"), ("/publications/", "Publications"), ("/projects/", "Software"),
       ("/about/", "Academic"), ("/#contact", "Contact")]


def page(path, title, description, body, extra_head=""):
    canonical = SITE + path
    nav = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == path else ""}>{label}</a></li>' for href, label in NAV)
    person_ld = {
        "@context": "https://schema.org", "@type": "Person",
        "name": PROFILE["name"], "alternateName": [PROFILE["short_name"], "Mohammed ALfatih"],
        "jobTitle": PROFILE["title"], "email": "mailto:" + PROFILE["email"],
                "worksFor": {"@type": "CollegeOrUniversity", "name": PROFILE["employer"]},
        "url": SITE + "/", "image": SITE + "/assets/img/portrait-640.jpg",
        "sameAs": [f"https://orcid.org/{PROFILE['orcid']}", f"https://github.com/{PROFILE['github']}",
                   f"https://github.com/{PROFILE['github_nlp']}"],
        "knowsAbout": ["Multi-objective optimization", "Ship weather routing", "High-performance computing",
                       "Machine learning", "Arabic natural language processing"],
    }
    full_title = title if path == "/" else f"{title} · {PROFILE['short_name']}"
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(PROFILE['name'])}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'profile' if path == '/' else 'website'}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1b2e">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/site.css">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<script type="application/ld+json">{json.dumps(person_ld, ensure_ascii=False)}</script>
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="hdr">
    <a class="brand" href="/">{e(PROFILE['short_name'])}</a>
    <nav aria-label="Main">
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-list">Menu <span class="bars" aria-hidden="true"></span></button>
      <ul id="nav-list">{nav}</ul>
    </nav>
    <button class="theme-toggle" type="button" aria-label="Toggle dark mode">{icon('moon')}{icon('sun')}</button>
  </div>
</header>
<div class="shell">
{sidebar()}
<main id="main">
{body}
<footer class="site-footer"><p>© {BUILD_DATE[:4]} {e(PROFILE['short_name'].upper())}</p><p>Optimisation · HPC · Machine learning · Arabic NLP</p></footer>
</main>
</div>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------------- charts (inline SVG)
def chart_pubs_by_year(pubs, chart_id="chart-years"):
    years = list(range(min(p["year"] for p in pubs), max(p["year"] for p in pubs) + 1))
    counts = {y: {t: 0 for t in TOPIC_ORDER} for y in years}
    for p in pubs:
        counts[p["year"]][p["topic"]] += 1
    maxv = max(sum(c.values()) for c in counts.values())
    svgs = "".join(_years_svg(years, counts, maxv, len(pubs), W, cls) for W, cls in ((640, "wide"), (340, "narrow")))
    legend = "".join(f'<li><span class="sw s{TOPIC_SLOT[t]}"></span>{e(TOPICS[t])}</li>' for t in TOPIC_ORDER)
    rows = "".join(
        f"<tr><th scope='row'>{y}</th>" + "".join(f"<td>{counts[y][t]}</td>" for t in TOPIC_ORDER) + f"<td>{sum(counts[y].values())}</td></tr>"
        for y in years)
    head = "".join(f"<th scope='col'>{e(TOPICS[t])}</th>" for t in TOPIC_ORDER)
    return f"""<figure class="chart" id="{chart_id}">
  <figcaption><span class="chart-title">Published papers per year, by research area</span>
  <span class="chart-sub">Peer-reviewed journal articles and conference papers (n = {len(pubs)}); accepted papers excluded. Years without papers shown as empty.</span></figcaption>
  <ul class="legend">{legend}</ul>
  {svgs}
  <details class="table-view"><summary>Show data table</summary><table><thead><tr><th scope="col">Year</th>{head}<th scope="col">Total</th></tr></thead><tbody>{rows}</tbody></table></details>
  <p class="chart-source">Source: publication dataset on this site, verified against Crossref and ORCID ({e(PUBS['as_of'])}).</p>
</figure>"""


def _years_svg(years, counts, maxv, n, W, cls):
    H, ml, mr, mt, mb = (260, 34, 8, 14, 30) if cls == "wide" else (220, 26, 4, 14, 30)
    pw, ph = W - ml - mr, H - mt - mb
    step = pw / len(years)
    bw = min(44, step * 0.6)
    ymax = maxv + (1 if maxv < 5 else 0)
    sy = lambda v: mt + ph - v / ymax * ph
    g = []
    for v in range(0, ymax + 1):
        y = sy(v)
        g.append(f'<line class="grid" x1="{ml}" x2="{W - mr}" y1="{y:.1f}" y2="{y:.1f}"/>'
                 f'<text class="tick" x="{ml - 8}" y="{y + 4:.1f}" text-anchor="end">{v}</text>')
    bars = []
    for i, yr in enumerate(years):
        x = ml + step * i + (step - bw) / 2
        base = 0
        segs = [(t, counts[yr][t]) for t in TOPIC_ORDER if counts[yr][t]]
        total = sum(c for _, c in segs)
        for j, (t, c) in enumerate(segs):
            y0, y1 = sy(base), sy(base + c)
            hgt = y0 - y1 - (2 if j < len(segs) - 1 else 0)
            top = j == len(segs) - 1
            r = 4 if top else 0
            path = rounded_top_rect(x, y1, bw, max(hgt, 1), r)
            tip = f"{yr} · {TOPICS[t]}: {c} paper{'s' if c > 1 else ''}"
            bars.append(f'<path class="mark s{TOPIC_SLOT[t]}" d="{path}" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title></path>')
            base += c
        if total:
            bars.append(f'<text class="val" x="{x + bw / 2:.1f}" y="{sy(total) - 6:.1f}" text-anchor="middle">{total}</text>')
        bars.append(f'<text class="tick" x="{x + bw / 2:.1f}" y="{H - 10}" text-anchor="middle">{yr}</text>')
    return f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="Stacked bar chart of published papers per year from {years[0]} to {years[-1]}, total {n}">{"".join(g)}<line class="axis" x1="{ml}" x2="{W - mr}" y1="{sy(0):.1f}" y2="{sy(0):.1f}"/>{"".join(bars)}</svg>'


def rounded_top_rect(x, y, w, h, r):
    r = min(r, h, w / 2)
    if r <= 0:
        return f"M{x:.1f},{y:.1f}h{w:.1f}v{h:.1f}h{-w:.1f}z"
    return (f"M{x:.1f},{y + h:.1f}V{y + r:.1f}Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f}"
            f"H{x + w - r:.1f}Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f}V{y + h:.1f}z")


def chart_topics(pubs, accepted):
    counts = {t: sum(1 for p in pubs if p["topic"] == t) for t in TOPIC_ORDER}
    acc = {t: sum(1 for p in accepted if p["topic"] == t) for t in TOPIC_ORDER}
    first = {t: sum(1 for p in pubs if p["topic"] == t and p["role"] == "first-author") for t in TOPIC_ORDER}
    order = sorted(TOPIC_ORDER, key=lambda t: -counts[t])
    maxv = max(counts[t] + acc[t] for t in order)

    def svg(W, cls):
        rowh, mr = 50, (150 if cls == "wide" else 120)
        H = rowh * len(order) + 4
        sx = lambda v: v / maxv * (W - mr)
        parts = []
        for i, t in enumerate(order):
            y = 4 + i * rowh
            parts.append(f'<text class="cat" x="0" y="{y + 13}">{e(TOPICS[t])}</text>')
            by, bh = y + 20, 18
            w = sx(counts[t])
            tip = f"{TOPICS[t]}: {counts[t]} published ({first[t]} first-author)"
            parts.append(f'<path class="mark s{TOPIC_SLOT[t]}" d="{rounded_right_rect(0, by, w, bh, 4)}" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title></path>')
            label = f"{counts[t]}"
            if acc[t]:
                aw = sx(acc[t])
                atip = f"{TOPICS[t]}: {acc[t]} accepted, not yet published"
                parts.append(f'<path class="mark accepted s{TOPIC_SLOT[t]}" d="{rounded_right_rect(w + 2, by, aw - 2, bh, 4)}" tabindex="0" data-tip="{e(atip)}"><title>{e(atip)}</title></path>')
                label += f" + {acc[t]} accepted"
                w += aw
            parts.append(f'<text class="val" x="{w + 8:.1f}" y="{by + 14}">{label}</text>')
        return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="Horizontal bar chart of papers by research area">'
                f'<defs><pattern id="hatch-{cls}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="var(--surface)"/><line x1="0" y1="0" x2="0" y2="6" stroke="currentColor" stroke-width="3"/></pattern></defs>'
                f'{"".join(parts).replace("class=\"mark accepted", "fill=\"url(#hatch-" + cls + ")\" class=\"mark accepted")}</svg>')

    rows = "".join(f"<tr><th scope='row'>{e(TOPICS[t])}</th><td>{counts[t]}</td><td>{first[t]}</td><td>{acc[t]}</td></tr>" for t in order)
    return f"""<figure class="chart" id="chart-topics">
  <figcaption><span class="chart-title">Papers by research area</span>
  <span class="chart-sub">Each paper is assigned to one area by its main application domain. Solid bars: published; hatched: accepted, not yet published.</span></figcaption>
  {svg(640, "wide")}{svg(340, "narrow")}
  <details class="table-view"><summary>Show data table</summary><table><thead><tr><th scope="col">Area</th><th scope="col">Published</th><th scope="col">of which first-author</th><th scope="col">Accepted</th></tr></thead><tbody>{rows}</tbody></table></details>
</figure>"""


def rounded_right_rect(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    if w <= 0:
        return ""
    return (f"M{x:.1f},{y:.1f}H{x + w - r:.1f}Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f}"
            f"V{y + h - r:.1f}Q{x + w:.1f},{y + h:.1f} {x + w - r:.1f},{y + h:.1f}H{x:.1f}z")


def chart_s175():
    d = PROJ["s175_speed"]
    rows = d["rows"]
    lo, hi = -3, 2  # 1 ms .. 100 s

    def svg(W, cls):
        mr, rowh = (90, 82) if cls == "wide" else (70, 82)
        H = rowh * len(rows) + 30
        sx = lambda v: (math.log10(v) - lo) / (hi - lo) * (W - mr)
        parts = []
        for kk in range(lo, hi + 1):
            x = sx(10 ** kk)
            lab = {-3: "1 ms", -2: "10 ms", -1: "0.1 s", 0: "1 s", 1: "10 s", 2: "100 s"}[kk]
            anchor = "start" if kk == lo else "middle"
            parts.append(f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="4" y2="{H - 26}"/><text class="tick" x="{x:.1f}" y="{H - 8}" text-anchor="{anchor}">{lab}</text>')
        for i, r in enumerate(rows):
            y = 4 + i * rowh
            parts.append(f'<text class="cat" x="0" y="{y + 13}">{e(r["case"])} · {e(r["ratio"])} faster</text>')
            for j, (key, cls2, name) in enumerate([("simulator_s", "s1", "Physical simulator (CPU)"), ("surrogate_s", "s3", "ML surrogate (GPU)")]):
                v = r[key]
                yy = y + 20 + j * 24
                w = max(sx(v), 3)
                fmt = f"{v:g} s" if v >= 1 else f"{v * 1000:.2f} ms"
                tip = f"{r['case']} · {name}: {fmt}"
                parts.append(f'<path class="mark {cls2}" d="{rounded_right_rect(0, yy, w, 18, 4)}" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title></path>')
                parts.append(f'<text class="val" x="{w + 6:.1f}" y="{yy + 13}">{fmt}</text>')
        return f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="Log-scale bar chart comparing simulator and surrogate evaluation time">{"".join(parts)}</svg>'

    trs = "".join(f"<tr><th scope='row'>{e(r['case'])}</th><td>{r['simulator_s']} s</td><td>{r['surrogate_s'] * 1000:.2f} ms</td><td>{r['ratio']}</td></tr>" for r in rows)
    return f"""<figure class="chart" id="chart-s175">
  <figcaption><span class="chart-title">{e(d['title'])}</span><span class="chart-sub">Wall-clock time per call, logarithmic axis. Measured result reported in the public repository.</span></figcaption>
  <ul class="legend"><li><span class="sw s1"></span>Physical simulator (CPU)</li><li><span class="sw s3"></span>ML surrogate (GPU)</li></ul>
  {svg(640, "wide")}{svg(340, "narrow")}
  <details class="table-view"><summary>Show data table</summary><table><thead><tr><th scope="col">Case</th><th scope="col">Simulator</th><th scope="col">Surrogate</th><th scope="col">Speed-up</th></tr></thead><tbody>{trs}</tbody></table></details>
  <p class="chart-source">Source: {e(d['source'])}</p>
</figure>"""


def chart_recency():
    repos = GH.get("repos", {})
    if not repos:
        return ""
    names = {p["repo"]: p.get("short", p["name"]) for p in PROJ["projects"]}
    items = sorted(((r, v) for r, v in repos.items() if v.get("pushed_at")), key=lambda kv: kv[1]["pushed_at"], reverse=True)
    ref = datetime.strptime(GH["retrieved_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    span_days = 365
    W, ml, mr, rowh = 640, 190, 20, 30
    H = rowh * len(items) + 40
    sx = lambda days: ml + (1 - days / span_days) * (W - ml - mr)
    parts = []
    for m in range(0, 13, 3):
        days = m * 30.4
        x = sx(days)
        lab = "now" if m == 0 else f"{m} mo ago"
        parts.append(f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="4" y2="{H - 28}"/><text class="tick" x="{x:.1f}" y="{H - 10}" text-anchor="middle">{lab}</text>')
    trs = []
    for i, (r, v) in enumerate(items):
        y = 10 + i * rowh
        pushed = datetime.strptime(v["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        days = (ref - pushed).days
        x = sx(min(days, span_days))
        area = next(p["area"] for p in PROJ["projects"] if p["repo"] == r)
        tip = f"{names[r]}: last push {pushed:%d %b %Y}"
        parts.append(f'<text class="cat" x="{ml - 12}" y="{y + 9}" text-anchor="end">{e(names[r])}</text>')
        parts.append(f'<line class="stem" x1="{x:.1f}" x2="{W - mr}" y1="{y + 5}" y2="{y + 5}"/>')
        parts.append(f'<circle class="mark dot s{TOPIC_SLOT[area]}" cx="{x:.1f}" cy="{y + 5}" r="6" tabindex="0" data-tip="{e(tip)}"><title>{e(tip)}</title></circle>')
        trs.append(f"<tr><th scope='row'><a href='{e(v['html_url'])}'>{e(r)}</a></th><td>{pushed:%Y-%m-%d}</td></tr>")
    return f"""<figure class="chart" id="chart-recency">
  <figcaption><span class="chart-title">Latest activity on featured public repositories</span>
  <span class="chart-sub">Date of the most recent push to each repository over the past 12 months. Dot colour = research area.</span></figcaption>
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="Dot plot of the last push date for each featured repository">{''.join(parts)}</svg>
  <details class="table-view"><summary>Show data table</summary><table><thead><tr><th scope="col">Repository</th><th scope="col">Last push</th></tr></thead><tbody>{''.join(trs)}</tbody></table></details>
  <p class="chart-source">Source: GitHub REST API, public metadata only, retrieved {e(GH['retrieved_at'][:10])}; refreshed weekly by a scheduled workflow.</p>
</figure>"""


# --------------------------------------------------------------------------- diagrams (conceptual)
def diagram(kind):
    if kind == "routing":
        return figures.routing_scene()
    if kind == "pmoo":
        return figures.pmoo_hardware()
    if kind == "s175":
        return figures.surrogate_scene()
    if kind == "filo2":
        return figures.filo2_scene()
    if kind == "race":
        return figures.s175_race()
    if kind in ("arabtech", "security", "net"):
        sets = {"arabtech": [("hwr", "Handwritten character recognition: a CNN extracts features and a KAN or attention head classifies the letter."),
                             ("gec", "Grammatical error correction: a sequence-to-sequence model rewrites the sentence (example: spelling of hamza and taa marbuta).")],
                "security": [("gtd", "Event records combine fields and free text; models use both to classify the attack or attribute the group."),
                             ("bigru", "BiGRU with self-attention over text and event features (PeerJ CS, 2024).")],
                "net": [("cache", "Indoor VLC and mmWave access with an edge cache; user movement and preferences are predicted to decide what to cache.")]}[kind]
        wrap_cls = "fig-pair" if len(sets) > 1 else "fig-one"
        cells = "".join(f'<div><div class="sw-fig">{figures.paper_figure(k)}</div><p class="mono-line dim">{e(c)}</p></div>' for k, c in sets)
        return f'<figure class="diagram"><div class="{wrap_cls}">{cells}</div><figcaption>Illustrations, not data.</figcaption></figure>'
    if True:
        svg = """<svg viewBox="0 0 680 210" role="img" aria-labelledby="dg-hs-t">
<title id="dg-hs-t">Hybrid annotation and modelling pipeline for Sudanese Arabic harmful-language detection</title>
<defs><marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="currentColor"/></marker></defs>
<g class="dg">
<rect class="box" x="8" y="70" width="112" height="64" rx="10"/><text x="64" y="97" text-anchor="middle">Telegram &amp;</text><text x="64" y="115" text-anchor="middle">Twitter text</text>
<rect class="box" x="148" y="70" width="112" height="64" rx="10"/><text x="204" y="97" text-anchor="middle">Normalise &amp;</text><text x="204" y="115" text-anchor="middle">de-duplicate</text>
<rect class="box accent" x="290" y="14" width="140" height="50" rx="10"/><text x="360" y="36" text-anchor="middle">Weak-supervision</text><text class="sm" x="360" y="53" text-anchor="middle">Sudanese rules</text>
<rect class="box accent" x="290" y="140" width="140" height="50" rx="10"/><text x="360" y="162" text-anchor="middle">LLM annotation</text><text class="sm" x="360" y="179" text-anchor="middle">+ native-speaker review</text>
<rect class="box" x="458" y="70" width="96" height="64" rx="10"/><text x="506" y="97" text-anchor="middle">Aggregated</text><text x="506" y="115" text-anchor="middle">labels</text>
<rect class="box" x="580" y="56" width="92" height="92" rx="10"/><text x="626" y="86" text-anchor="middle">Models</text><text class="sm" x="626" y="106" text-anchor="middle">transformers,</text><text class="sm" x="626" y="121" text-anchor="middle">ensembles,</text><text class="sm" x="626" y="136" text-anchor="middle">SHAP / LIME</text>
<path class="flow" d="M120 102H146" marker-end="url(#ar3)"/>
<path class="flow" d="M260 102 C275 102 275 39 288 39" marker-end="url(#ar3)"/><path class="flow" d="M260 102 C275 102 275 165 288 165" marker-end="url(#ar3)"/>
<path class="flow" d="M430 39 C445 39 445 95 456 95" marker-end="url(#ar3)"/><path class="flow" d="M430 165 C445 165 445 109 456 109" marker-end="url(#ar3)"/>
<path class="flow" d="M554 102H578" marker-end="url(#ar3)"/>
</g></svg>"""
        cap = "Conceptual diagram (not experimental data): rule-based weak supervision and LLM labels are combined, checked on a human-reviewed sample, and used to train and explain classifiers; model selection uses validation data only."
    svg = svg.replace("<svg ", '<svg class="wide-fig" ', 1) + figures.hs_narrow()
    return f'<figure class="diagram">{svg}<figcaption>{e(cap)}</figcaption></figure>'


# --------------------------------------------------------------------------- components
def pub_card(p, compact=False):
    status = p.get("status_label") or ("Published" if p["status"] == "published" else p["status"])
    badges = [f'<span class="tag t{TOPIC_SLOT[p["topic"]]}">{e(TOPICS[p["topic"]])}</span>']
    if p["role"] == "first-author":
        badges.append('<span class="tag plain">First author</span>')
    if p["type"] == "conference":
        badges.append('<span class="tag plain">Conference</span>')
    if p["status"] != "published":
        badges.append(f'<span class="tag status">{e(status)}</span>')
    links = []
    if p.get("doi"):
        links.append(link_btn(p["url"], "DOI " + p["doi"], "doc"))
    if p.get("open_access_url") and p.get("open_access_url") != p.get("url"):
        links.append(link_btn(p["open_access_url"], "Open-access PDF", "doc"))
    elif p.get("open_access_url"):
        links.append('<span class="oa">Open access</span>')
    if p.get("code_url"):
        links.append(link_btn(p["code_url"], "Code", "code"))
    venue = f'<em>{e(p["venue"])}</em>' + (f', {e(p["details"])}' if p.get("details") else "")
    if p["status"] == "under-consideration":
        venue = "<em>Manuscript under consideration</em>"
    note = f'<p class="name-note">{e(p["name_note"])}</p>' if p.get("name_note") else ""
    if p.get("credit"):
        note += f'<p class="credit">{e(p["credit"])}</p>'
    summary = "" if compact else f'<p class="summary">{e(p["summary"])}</p>'
    return f"""<article class="pub" data-year="{p['year']}" data-topic="{p['topic']}" data-status="{p['status']}" data-role="{p['role']}">
  <div class="pub-year" aria-hidden="true">{'' if p['status'] == 'under-consideration' else p['year']}</div>
  {'' if compact or p['id'] not in figures.PAPER_FIG else '<div class="pub-fig">' + figures.paper_figure(figures.PAPER_FIG[p['id']]) + '</div>'}
  <div class="pub-body">
    <h3 class="pub-title">{e(p['title'])}</h3>
    <p class="authors">{authors_html(p['authors'])}</p>
    <p class="venue">{venue}{'' if p["status"] == "under-consideration" else ' · ' + str(p['year'])}</p>{note}
    {summary}
    <div class="pub-meta">{''.join(badges)}</div>
    {('<div class="pub-links">' + ''.join(links) + '</div>') if links else ''}
  </div>
</article>"""


REPO_FIG = {
    "MOHAMMED-ABDALSALAM-PG/PMOO-V1": "pmoo", "MOHAMMED-ABDALSALAM-PG/S175-ML-surrogate": "s175",
    "MOHAMMED-ABDALSALAM-PG/SWR-HPC-systematic-review": "swr", "scander91/sudanese-hate-speech-detection": "hate",
    "scander91/arabic-dialect-BERT-LLM": "dialect", "scander91/MSF-CBERT": "fusion",
    "scander91/Intelligent-Fusion-of-Heterogeneous-Data-for-Terrorist-Organization": "fusion",
}


def project_card(p, accepted_by_id):
    gh = GH.get("repos", {}).get(p["repo"])
    url = gh["html_url"] if gh else f"https://github.com/{p['repo']}"
    updated = ""
    if gh and gh.get("pushed_at"):
        updated = f'<span class="updated">Updated {datetime.strptime(gh["pushed_at"][:10], "%Y-%m-%d"):%b %Y}</span>'
    lic = f' · {e(gh["license"])} licence' if gh and gh.get("license") and gh["license"] != "NOASSERTION" else ""
    tech = "".join(f"<li>{e(t)}</li>" for t in p["tech"])
    paper = ""
    if p.get("paper_id") and p["paper_id"] in accepted_by_id:
        a = accepted_by_id[p["paper_id"]]
        paper = f'<p class="proj-paper"><span>Paper</span> {e(a["title"])} — <em>{e(a["venue"])}</em> ({e(a["status_label"])})</p>'
    elif p.get("paper"):
        paper = f'<p class="proj-paper"><span>Paper</span> {e(p["paper"])}</p>'
    extra = "".join(link_btn(l["url"], l["label"]) for l in p.get("links", []))
    return f"""<article class="proj t{TOPIC_SLOT[p['area']]}">
  <div class="proj-head"><span class="tag t{TOPIC_SLOT[p['area']]}">{e(TOPICS[p['area']])}</span><span class="tag status">{e(p['status'])}</span></div>
  <h3><a href="{e(url)}" rel="noopener">{e(p['name'])}</a></h3>
  <p class="repo-name">{icon('github', 14)} {e(p['repo'])}{lic}</p>
  {('<div class="sw-fig proj-fig">' + figures.card_figure(REPO_FIG[p['repo']]) + '</div>') if p['repo'] in REPO_FIG else ''}
  <p>{e(p['description'])}</p>
  <p class="contrib">{e(p['contribution'])}</p>
  {paper}
  <ul class="tech" aria-label="Technologies">{tech}</ul>
  <div class="proj-foot">{link_btn(url, 'Repository', 'github', 'btn-link strong')}{extra}{updated}</div>
</article>"""


# --------------------------------------------------------------------------- pages
def sidebar():
    pubs = PUBS["publications"]
    links = [(f"https://orcid.org/{PROFILE['orcid']}", "ORCID"), (f"https://github.com/{PROFILE['github']}", "GitHub"),
             (f"https://github.com/{PROFILE['github_nlp']}", "GitHub · NLP"), ("/publications/", "Publications")]
    lk = "".join(f'<li><a href="{u}"{" rel=\"noopener\"" if u.startswith("http") else ""}>{t}<span aria-hidden="true">{"↗" if u.startswith("http") else "→"}</span></a></li>' for u, t in links)
    return f"""<aside class="side" aria-label="Profile">
  <div class="side-id">
    <a href="/" class="side-photo" tabindex="-1" aria-hidden="true"><picture>
      <source type="image/webp" srcset="/assets/img/portrait-320.webp 320w, /assets/img/portrait-640.webp 640w" sizes="180px">
      <img src="/assets/img/portrait-640.jpg" width="640" height="640" alt="">
    </picture></a>
    <div>
      <p class="side-name">{e(PROFILE['short_name'])}</p>
      <p class="side-title">PhD Student</p>
      <p class="side-sub">AI &amp; HPC Researcher</p>
    </div>
  </div>
  <div class="side-int"><p class="side-h">Areas of interest</p><ul>
    <li>Multi-objective optimisation</li><li>High-performance computing</li><li>Ship weather routing</li>
    <li>Machine-learning surrogates</li><li>Low-resource Arabic NLP</li></ul></div>
  <details class="side-more" open>
    <summary>Details and links</summary>
    <dl class="side-dl">
      <div><dt>Location</dt><dd>{e(PROFILE['location'])}</dd></div>
      <div><dt>Email</dt><dd><a href="mailto:{PROFILE['email']}">{e(PROFILE['email'])}</a></dd></div>
      <div><dt>Lecturer</dt><dd>Univ. of the Holy Quran &amp; Islamic Sciences</dd></div>
    </dl>
    <ul class="side-links">{lk}</ul>
    <p class="side-stats"><b>{len(pubs)}</b> publications<br><b>{len(PUBS['accepted'])}</b> accepted · <b>{len(PUBS.get('under_consideration', []))}</b> under consideration</p>
  </details>
</aside>"""


def home():
    pubs = PUBS["publications"]
    allp = {p["id"]: p for p in pubs + PUBS["accepted"]}
    first_sentence = lambda s: s.split(". ")[0].rstrip(".") + "."

    rows = [
        ("Ship weather routing &amp; HPC", "Multi-objective evolutionary algorithms (NSGA-II, SPEA2, MOEA/D) for routing ships through changing weather, accelerated with OpenMP, CUDA and hybrid CPU–GPU execution.", "https://doi.org/10.12716/1001.19.01.12", "Paper"),
        ("Machine-learning surrogates", "Neural surrogates that replace a slow ship-performance simulator inside the optimiser, with feasibility classifiers and safety-biased errors.", "https://github.com/MOHAMMED-ABDALSALAM-PG/S175-ML-surrogate", "Code"),
        ("Large-scale vehicle routing", "Collaboration with Prof. Daniele Vigo and Dr. Luca Accorsi: integrating their FILO2 heuristic with PMOO for multi-objective routing.", "/research/#filo2", "Overview"),
        ("Low-resource Arabic NLP", "Sudanese Arabic corpora, LLM-assisted annotation, harmful-language detection and dialect identification with BERT models and LLMs.", "/publications/#accepted", "Papers"),
        ("Arabic language technologies", "Handwritten character recognition (CNN, CNN–KAN) and multi-task grammatical error correction, as co-author.", "/publications/?topic=arabic-nlp", "Papers"),
        ("Security-event analytics", "Text and tabular fusion for classifying and attributing events in the Global Terrorism Database.", "https://doi.org/10.7717/peerj-cs.2252", "Paper"),
    ]
    prof = "".join(f'<li><h3>{t}</h3><p>{d}</p><a href="{u}"{" rel=\"noopener\"" if u.startswith("http") else ""}>{l} →</a></li>' for t, d, u, l in rows)

    chips = ["Python", "C/C++", "CUDA", "OpenMP", "MPI", "PyTorch", "scikit-learn", "LaTeX", "Git"]
    chip_html = "".join(f"<li>{e(c)}</li>" for c in chips)

    cards_spec = [
        ("MOHAMMED-ABDALSALAM-PG/PMOO-V1", "pmoo", "Population → OpenMP / CUDA → Pareto front", "Parallel computing · Optimisation"),
        ("MOHAMMED-ABDALSALAM-PG/S175-ML-surrogate", "s175", "Inputs → feasibility → regression → outputs", "Scientific machine learning"),
        ("scander91/sudanese-hate-speech-detection", "hate", "Collect → normalise → label → train → explain", "Arabic NLP"),
        ("scander91/arabic-dialect-BERT-LLM", "dialect", "Text → BERT | LLM → dialect", "Arabic NLP"),
        ("MOHAMMED-ABDALSALAM-PG/SWR-HPC-systematic-review", "swr", "Search → deduplicate → screen → include", "Systematic review"),
        ("scander91/Intelligent-Fusion-of-Heterogeneous-Data-for-Terrorist-Organization", "fusion", "Text + attributes → fusion → class", "Security analytics"),
    ]
    projs = {p["repo"]: p for p in PROJ["projects"]}
    cards = ""
    for repo, fig, pipe, area in cards_spec:
        p = projs[repo]
        desc = ". ".join(p["description"].split(". ")[:1]).rstrip(".") + "."
        cards += f"""<article class="sw-card">
  <p class="eyebrow">{e(area)}</p>
  <h3>{e(p['short'])}</h3>
  <p>{e(desc)}</p>
  <div class="sw-fig">{figures.card_figure(fig)}</div>
  <p class="mono-line">{e(pipe)}</p>
  <p class="mono-line dim">{e(p['status'])}</p>
  <p class="sw-links"><a href="https://github.com/{e(repo)}" rel="noopener">Code</a><a href="/projects/">Details</a></p>
</article>"""

    hl_ids = ["abdalsalam2025towards", "abdalsalam2026hate", "abdalsalam2024bigru", "abdalsalam2024textual"]
    hl = ""
    for i in hl_ids:
        p = allp[i]
        links = []
        if p.get("open_access_url"):
            links.append(f'<a href="{e(p["open_access_url"])}" rel="noopener">Paper</a>')
        if p.get("doi"):
            links.append(f'<a href="https://doi.org/{e(p["doi"])}" rel="noopener">DOI</a>')
        if p.get("code_url"):
            links.append(f'<a href="{e(p["code_url"])}" rel="noopener">Code</a>')
        venue = e(p["venue"]) + (", " + e(p["details"]) if p.get("details") else "")
        status = "" if p["status"] == "published" else f' · <span class="st">{e(p.get("status_label", ""))}</span>'
        thumb = f'<div class="pub-fig hl-fig">{figures.paper_figure(figures.PAPER_FIG[i])}</div>' if i in figures.PAPER_FIG else ""
        hl += f"""<li><span class="yr">{p['year']}</span>{thumb}<div>
  <h3>{e(p['title'])}</h3>
  <p class="au">{authors_html(p['authors'])}</p>
  <p class="ve"><em>{venue}</em>{status}</p>
  <p class="su">{e(first_sentence(p['summary']))}</p>
  <p class="hl-links">{''.join(links)}</p></div></li>"""

    rec = [
        ("Appointment", "University Lecturer", "University of the Holy Quran and Islamic Sciences, Sudan · Nov 2016–present"),
        ("Ph.D.", "PhD Student", ""),
        ("Research", "Research Assistant", "Wuhan University of Technology & Sudan University of Science and Technology · 2018–2024"),
        ("M.Sc.", "Information Technology (First Class)", "University of Madras, India · 2015"),
        ("B.Sc.", "Information Technology", "Al-Zaeim Al-Azhari University, Sudan · 2012"),
        ("Fellowship", "Polonium International Doctoral Fellowship · NAWA PROM", "Excellence Initiative – Research University (IDUB)"),
        ("Talks", "TransNav 2025 · AICS 2019", "Gdynia, Poland · Hubei, China"),
        ("Teaching", "Lecturer in computer science since 2015", "Cambridge International College and other Sudanese colleges · 2015–2019"),
    ]
    rec_html = "".join(f'<li><span class="lbl">{e(a)}</span><div><h3>{e(b)}</h3>{("<p>" + e(c) + "</p>") if c else ""}</div></li>' for a, b, c in rec)

    body = f"""
<section class="intro-block">
  <p class="eyebrow">PhD Student · AI &amp; HPC Researcher</p>
  <h1>HPC-based multi-objective optimisation for ships at sea.</h1>
  <p>I design algorithms that make hard decisions computable. My doctoral research builds multi-objective evolutionary optimisers and machine-learning surrogates for ship weather routing, and accelerates them on multi-core CPUs and GPUs.</p>
  <p>In parallel, I build data and models for Sudanese Arabic, where labelled data are scarce: corpora, LLM-assisted annotation, harmful-language detection and dialect identification. I have taught computer science at university level since 2015.</p>
  <p class="note"><span class="pulse" aria-hidden="true"></span>Open to research collaborations in optimisation, HPC and Arabic NLP</p>
  <p class="jump"><a href="#lab">Try the interactive demo ↘</a><a href="/publications/">Browse all publications</a><a href="/projects/">Explore research software</a><a href="#contact">Get in touch</a></p>
</section>

<section class="block" id="lab" aria-labelledby="lab-h">
  <div class="block-head"><div><p class="eyebrow">Interactive routing lab</p><h2 id="lab-h">Weather routing in motion.</h2></div><a href="/research/#maritime">Explore the research ↗</a></div>
  <p class="block-lede">Make the storm stronger, choose what matters most, and watch the ship change its route and speed.</p>
  <div id="routing-lab" class="lab"><noscript>{figures.routing_scene()}</noscript></div>
  <p class="mono-line dim">Illustrative model, not the research code · 9 paths × 5 speeds · objectives: time, fuel, highest wave met</p>
</section>

<section class="block" aria-labelledby="prof-h">
  <div class="block-head"><div><p class="eyebrow">Research profile</p><h2 id="prof-h">From ocean routes to Arabic dialects.</h2></div><a href="/research/">Research overview →</a></div>
  <p class="block-lede">One thread runs through the work: methods that are fast, honest about uncertainty, and tested against real constraints.</p>
  <ul class="prof-rows">{prof}</ul>
</section>

<section class="block" aria-labelledby="bring-h">
  <p class="eyebrow">What I bring</p><h2 id="bring-h">Research that runs, end to end.</h2>
  <div class="bring">
    <div><h3>End-to-end research</h3><p>Problem framing, algorithm design, experiments with fixed protocols, statistics, papers and reproducibility packages.</p></div>
    <div><h3>Parallel computing</h3><p>OpenMP, CUDA and hybrid CPU–GPU implementations, benchmarked fairly against serial baselines.</p></div>
    <div><h3>Teaching and communication</h3><p>University lecturer since 2015, international collaborations, and clear explanation of technical results.</p></div>
  </div>
  <ul class="chips-mono">{chip_html}</ul>
</section>

<section class="block" aria-labelledby="sw-h">
  <div class="block-head"><div><p class="eyebrow">Research software</p><h2 id="sw-h">From papers to working code.</h2></div><a href="/projects/">All software &amp; data →</a></div>
  <div class="sw-grid">{cards}</div>
</section>

<section class="block" aria-labelledby="hl-h">
  <div class="block-head"><div><p class="eyebrow">First-author highlights</p><h2 id="hl-h">Selected papers.</h2></div><a href="/publications/">All publications →</a></div>
  <ol class="hl">{hl}</ol>
</section>

<section class="block" aria-labelledby="rec-h">
  <p class="eyebrow">Professional record</p><h2 id="rec-h">Experience and education.</h2>
  <ul class="rec">{rec_html}</ul>
</section>

<section class="block" id="contact" aria-labelledby="ct-h">
  <p class="eyebrow">Contact</p><h2 id="ct-h">Let's work together.</h2>
  <p class="block-lede">I welcome conversations about research collaboration, datasets, and academic positions.</p>
  <p><a class="mail-big" href="mailto:{PROFILE['email']}">{e(PROFILE['email'])} →</a></p>
</section>"""
    return page("/", PROFILE["name"], "Mohammed Abdalsalam, PhD student: multi-objective ship weather routing, parallel optimisation on CPUs and GPUs, machine-learning surrogates, and Sudanese Arabic NLP.",
                body, extra_head='<script src="/assets/js/routing-lab.js" defer></script>')


def research():
    accepted = {a["id"]: a for a in PUBS["accepted"]}
    pubs = {p["id"]: p for p in PUBS["publications"]}

    def refs(ids):
        items = []
        for i in ids:
            p = pubs.get(i) or accepted.get(i)
            st = "" if p["status"] == "published" else f" — {p['status_label']}"
            href = p.get("url") or "/publications/"
            items.append(f'<li><a href="{e(href)}">{e(p["title"])}</a> <span class="muted">({e(p["venue"])}, {p["year"]}{e(st)})</span></li>')
        return "<ul class='refs'>" + "".join(items) + "</ul>"

    sections = [
        ("maritime", "maritime-hpc", "Maritime AI and multi-objective optimisation",
         "A ship's route through changing weather trades off voyage time, fuel and safety. These goals conflict, so there is no single best route but a Pareto front of compromises — and computing it with evolutionary algorithms over a weather forecast is expensive.",
         "Multi-objective evolutionary algorithms (NSGA-II, SPEA2, MOEA/D) and Pareto-front analysis; parallel implementations with OpenMP, CUDA and hybrid CPU–GPU execution; a PRISMA-based systematic review of how HPC has been used in ship weather routing.",
         "Faster optimisers let routing systems re-plan as forecasts update, which is a prerequisite for using multi-objective routing operationally rather than offline.",
         ["abdalsalam2025towards"], ["routing", "pmoo"]),
        ("filo2", "maritime-hpc", "Large-scale vehicle routing: FILO2 inside PMOO (collaboration)",
         "Delivery companies plan routes for thousands of customers, and in practice they care about more than total distance. Multi-objective algorithms can show those trade-offs, but on their own they are too slow for problems of this size.",
         "Together with Prof. Daniele Vigo (University of Bologna) and Dr. Luca Accorsi, I am integrating FILO2, their state-of-the-art heuristic for very large vehicle-routing problems, with my PMOO framework. The aim is to let PMOO's algorithms (NSGA-II, SPEA2, MOEA/D) use FILO2 as their fast improvement engine, so that they can find a set of good trade-off route plans for large instances.",
         "It brings the speed of a leading single-objective solver into multi-objective optimisation, and carries the ideas of my ship-routing work over to road logistics.",
         [], ["filo2"]),
        ("surrogates", "maritime-hpc", "Machine learning for scientific computing",
         "Physics-based ship-performance models are accurate but slow; inside an optimiser they are called millions of times. Infeasible operating points and safety-relevant outputs make naive regression risky.",
         "Neural surrogate models trained on large simulator grids (126 million evaluations of the S175 model in the ERA-NET MarTERA ROUTING project), explicit feasibility classifiers, asymmetric loss functions that bias errors toward conservative predictions, leakage-safe splits and off-grid validation against fresh simulator runs.",
         "Reliable surrogates move expensive physics out of the inner loop of route optimisation while keeping its safety-critical behaviour visible.",
         [], ["s175", "race"]),
        ("arabic-nlp", "arabic-nlp", "Low-resource Arabic NLP and Sudanese dialects",
         "Sudanese Arabic has very few labelled datasets, so harmful-language detection, sentiment analysis and dialect identification lag far behind Modern Standard Arabic and the better-resourced dialects.",
         "Corpus construction from social media and app reviews; hybrid annotation that combines Sudanese-specific weak-supervision rules with large language model labelling and native-speaker review; continued pre-training of a Sudanese BERT (SudaBERT-v2); systematic comparison of fine-tuned Arabic BERT models and zero/few-shot LLMs; explainability with SHAP and LIME.",
         "Shared corpora, models and reproducible benchmarks are what allow a low-resource dialect community to build moderation, analytics and assistive tools.",
         ["abdalsalam2026hate", "abdalsalam2026dialect"], ["hs"]),
        ("arabic-tech", "arabic-nlp", "Arabic language technologies",
         "Arabic script is cursive with position-dependent letter forms, and Arabic grammar is morphologically rich — both hard for recognition and correction systems.",
         "Convolutional networks, CNN–Kolmogorov–Arnold Network hybrids and attention for handwritten character recognition; sequence-to-sequence and multi-task grammatical error correction with large synthetic training data (co-authored work).",
         "Better recognition and correction tools support digitisation, education and writing assistance for Arabic.",
         ["alsayed2026attention", "alsayed2025hybrid", "alsayed2024impact", "mahmoud2026mtagec", "mahmoud2024bidirectional"], ["arabtech"]),
        ("security", "security-analytics", "Machine learning for security-event analytics",
         "Event databases such as the Global Terrorism Database combine structured attributes with free-text descriptions, are heavily imbalanced, and are used by analysts to study patterns of political violence.",
         "Tree-based ensembles, DistilBERT text features combined with structured attributes, BiGRU with self-attention, class rebalancing; later work on multi-source fusion and entity recognition.",
         "Shows how textual evidence can be integrated with tabular records to support analysis; this line of work began during the author's research-assistant period (2018–2024).",
         ["alfatih2019prediction", "abdalsalam2021study", "abdalsalam2024textual", "abdalsalam2024bigru"], ["security"]),
        ("networking", "networking", "Intelligent networking (co-authored)",
         "Indoor edge networks combining visible-light and millimetre-wave links must decide what to cache near moving users.",
         "Mobility prediction (BiGRU, transformers), preference modelling (collaborative filtering, NeuMF), LSTM forecasting and reinforcement learning (Soft Actor-Critic) for cache placement under software-defined control.",
         "Contributes machine-learning methods to proactive content delivery in next-generation networks.",
         ["kombo2025collaborative", "kombo2025mobility", "kombo2026location"], ["net"]),
    ]
    NOTES = {
        "surrogates": '<p class="muted">Manuscript under consideration; code at <a href="https://github.com/MOHAMMED-ABDALSALAM-PG/S175-ML-surrogate">S175-ML-surrogate</a>.</p>',
        "filo2": '<p class="muted">Ongoing collaboration, shown as an overview only. FILO2 itself is by L. Accorsi and D. Vigo (<a href="https://doi.org/10.1016/j.cor.2024.106562">Computers &amp; Operations Research, 2024</a>).</p>',
    }
    toc = "".join(f'<li><a href="#{sid}">{e(title)}</a></li>' for sid, _, title, *_ in sections)
    blocks = []
    for sid, topic, title, problem, methods, why, ids, dg in sections:
        blocks.append(f"""<section class="research-block t{TOPIC_SLOT[topic]}" id="{sid}" aria-labelledby="{sid}-h">
  <h2 id="{sid}-h">{e(title)}</h2>
  <div class="pmw">
    <div><h3>Problem</h3><p>{e(problem)}</p></div>
    <div><h3>Methods</h3><p>{e(methods)}</p></div>
    <div><h3>Why it matters</h3><p>{e(why)}</p></div>
  </div>
  {''.join(diagram(k) for k in (dg or []))}
  {('<h3 class="refs-h">Related papers</h3>' + refs(ids)) if ids else NOTES.get(sid, '')}
</section>""")
    body = f"""<section class="wrap page-head"><p class="eyebrow">Research</p><h1>Algorithms, computing and language</h1>
<p class="lede">My doctoral work, <em>{e(PROFILE['dissertation'])}</em>, connects evolutionary optimisation, machine learning and parallel computing. Alongside it, I build data and models for low-resource Arabic.</p>
<nav class="toc" aria-label="Research areas"><ul>{toc}</ul></nav></section>
<section class="wrap"><h2 class="story-h">The big picture</h2>{figures.overview_story()}</section>
<div class="wrap">{''.join(blocks)}</div>"""
    return page("/research/", "Research", "Research directions of Mohammed Abdalsalam: ship weather routing, parallel multi-objective optimisation, ML surrogates, and low-resource Arabic NLP.", body)


def publications():
    pubs = sorted(PUBS["publications"], key=lambda p: (-p["year"], p["title"]))
    acc = PUBS["accepted"]
    years = sorted({p["year"] for p in pubs}, reverse=True)
    year_opts = "".join(f'<option value="{y}">{y}</option>' for y in years)
    topic_btns = "".join(f'<button type="button" class="chip" data-topic="{t}" aria-pressed="false"><span class="sw s{TOPIC_SLOT[t]}"></span>{e(TOPICS[t])}</button>' for t in TOPIC_ORDER)
    groups = []
    for y in years:
        items = "".join(pub_card(p) for p in pubs if p["year"] == y)
        groups.append(f'<section class="year-group" data-year="{y}"><h2 class="year-h">{y}</h2>{items}</section>')
    acc_cards = "".join(pub_card(a) for a in acc)
    uc_cards = "".join(pub_card(a) for a in PUBS.get("under_consideration", []))
    n_j = sum(1 for p in pubs if p["type"] == "journal")
    body = f"""<section class="wrap page-head"><p class="eyebrow">Publications</p><h1>Peer-reviewed publications</h1>
<p class="lede">{len(pubs)} published papers — {n_j} journal articles and {len(pubs) - n_j} conference paper — plus {len(acc)} accepted papers on Sudanese Arabic NLP. {len(PUBS.get('under_consideration', []))} further manuscripts are under consideration and are listed separately below. The 2019 paper appears under the earlier name form “Mohammed ALfatih”.</p>
<p class="lede small">Every entry was checked against its DOI record (Crossref) or the journal, and against the ORCID record <a href="https://orcid.org/{PROFILE['orcid']}">{PROFILE['orcid']}</a>. Summaries are written from the published abstracts; where an abstract could not be accessed, the summary is limited to what the title and venue state. A machine-readable version is available as <a href="/publications.json">publications.json</a>.</p></section>

<section class="wrap charts-row">{chart_pubs_by_year(PUBS['publications'])}{chart_topics(PUBS['publications'], acc)}</section>

<section class="wrap" aria-labelledby="acc-h">
  <h2 id="acc-h" class="block-h">Accepted papers <span class="muted">— not yet published</span></h2>
  <div class="pub-list accepted-list">{acc_cards}</div>
</section>

<section class="wrap" aria-labelledby="uc-h">
  <h2 id="uc-h" class="block-h">Under consideration <span class="muted">— submitted manuscripts</span></h2>
  <p class="muted section-note">Submitted work that is still being reviewed. Journals are not named until a decision is made; code and data are already public.</p>
  <div class="pub-list accepted-list">{uc_cards}</div>
</section>

<section class="wrap" aria-labelledby="pub-h">
  <h2 id="pub-h" class="block-h">Published papers</h2>
  <div class="filters" role="group" aria-label="Filter publications">
    <label class="search"><span class="sr-only">Search titles, authors and venues</span><input type="search" id="pub-q" placeholder="Search title, author, venue…"></label>
    <label class="sel"><span>Year</span><select id="pub-year"><option value="">All</option>{year_opts}</select></label>
    <label class="sel"><span>Authorship</span><select id="pub-role"><option value="">All</option><option value="first-author">First author</option><option value="co-author">Co-author</option></select></label>
    <div class="chips">{topic_btns}</div>
  </div>
  <p class="filter-count" id="pub-count" aria-live="polite"></p>
  <div class="pub-list" id="pub-list">{''.join(groups)}</div>
</section>"""
    return page("/publications/", "Publications", f"Verified list of {len(pubs)} peer-reviewed publications by Mohammed Abdalsalam, with DOIs, summaries and code links.", body)


def projects():
    accepted = {a["id"]: a for a in PUBS["accepted"]}
    featured = [p for p in PROJ["projects"] if p["featured"]]
    other = [p for p in PROJ["projects"] if not p["featured"]]
    cards = "".join(project_card(p, accepted) for p in featured)
    other_cards = "".join(project_card(p, accepted) for p in other)
    res = []
    for r in RES["resources"]:
        avail_cls = "public" if r["public"] else "private"
        link = link_btn(r["url"], "Get the data", "data", "btn-link strong") if r.get("url") else f'<a class="btn-link" href="mailto:{PROFILE["email"]}?subject={e(r["name"])}">{icon("mail", 15)}<span>Ask by email</span></a>'
        res.append(f"""<article class="resource">
  <p class="kind">{icon('data', 16)} {e(r['kind'])}</p>
  <h3>{e(r['name'])}</h3>
  <p>{e(r['description'])}</p>
  <p class="avail {avail_cls}"><span class="dot" aria-hidden="true"></span>{e(r['availability'])}</p>
  <div class="proj-foot">{link}</div>
</article>""")
    body = f"""<section class="wrap page-head"><p class="eyebrow">Software &amp; Data</p><h1>Research software, datasets and models</h1>
<p class="lede">Reproducibility packages and research code for my papers. Each card says what the code does, my role in it, and the status of the paper it belongs to. The repositories are on two GitHub accounts: <a href="https://github.com/{PROFILE['github']}">{PROFILE['github']}</a> (optimisation, HPC, maritime) and <a href="https://github.com/{PROFILE['github_nlp']}">{PROFILE['github_nlp']}</a> (NLP).</p></section>
<section class="wrap"><h2 class="block-h">Featured projects</h2><div class="proj-grid">{cards}</div></section>
<section class="wrap" aria-labelledby="res-h"><h2 id="res-h" class="block-h">Datasets &amp; models</h2>
<p class="muted section-note">Resources I created for Sudanese Arabic NLP. Availability is stated exactly. Texts collected from social media are shared as identifiers and labels only.</p>
<div class="res-grid">{''.join(res)}</div></section>
<section class="wrap charts-row">{chart_s175()}</section>
<section class="wrap"><h2 class="block-h">More research code</h2><div class="proj-grid">{other_cards}</div></section>"""
    return page("/projects/", "Software & Data", "Research software, datasets and models by Mohammed Abdalsalam: parallel multi-objective optimisation, ship-performance surrogates, and Sudanese Arabic NLP resources.", body)


def about():
    edu = "".join(f"""<li><span class="when">{e(x['period'])}</span><div><h3>{e(x['degree'])}</h3>{('<p class="org">' + e(x['institution']) + ', ' + e(x['place']) + '</p>') if x['institution'] else ''}{('<p>' + e(x['note']) + '</p>') if x['note'] else ''}</div></li>""" for x in PROFILE["education"])
    exp = "".join(f"""<li><span class="when">{e(x['period'])}</span><div><h3>{e(x['role'])}</h3><p class="org">{e(x['org'])}</p><ul>{''.join('<li>' + e(pt) + '</li>' for pt in x['points'])}</ul></div></li>""" for x in PROFILE["experience"])
    skills = "".join(f"""<div class="skill-group"><h3>{e(s['group'])}</h3><ul>{''.join('<li>' + e(i) + '</li>' for i in s['items'])}</ul></div>""" for s in PROFILE["skills"])
    lst = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    body = f"""<section class="wrap page-head"><p class="eyebrow">About</p><h1>Background</h1>
<p class="lede">I am a PhD student in Information and Communication Technology, supervised by dr hab. inż. Joanna Szłapczyńska and dr hab. inż. Paweł Czarnul. Professionally, I am a University Lecturer at the University of the Holy Quran and Islamic Sciences in Sudan (since 2016), after teaching at several colleges from 2015; from 2018 to 2024 I was a research assistant with Wuhan University of Technology and Sudan University of Science and Technology.</p></section>
<div class="wrap about-grid">
  <section aria-labelledby="edu-h"><h2 id="edu-h" class="block-h">Education</h2><ol class="timeline">{edu}</ol></section>
  <section aria-labelledby="exp-h"><h2 id="exp-h" class="block-h">Professional experience</h2><ol class="timeline">{exp}</ol></section>
</div>
<section class="wrap" aria-labelledby="doc-h"><h2 id="doc-h" class="block-h">Doctoral research</h2>
<ul class="plain">{''.join('<li>' + e(pt) + '</li>' for pt in PROFILE['doctoral']['points'])}</ul></section>
<section class="wrap" aria-labelledby="sk-h"><h2 id="sk-h" class="block-h">Skills</h2><div class="skills">{skills}</div><p class="muted">Languages: {e(PROFILE['languages'])}.</p></section>
<div class="wrap about-grid three">
  <section><h2 class="block-h">Scholarships &amp; mobility</h2><ul class="plain">{lst(PROFILE['scholarships'])}</ul></section>
  <section><h2 class="block-h">Conference presentations</h2><ul class="plain">{lst(PROFILE['presentations'])}</ul></section>
  <section><h2 class="block-h">Recognition</h2><ul class="plain">{lst(PROFILE['awards'])}</ul></section>
</div>
<section class="wrap section contact-band" id="contact"><h2>Contact</h2>
<p>Email: <a href="mailto:{PROFILE['email']}">{e(PROFILE['email'])}</a></p>
<p class="muted">PhD student · ORCID <a href="https://orcid.org/{PROFILE['orcid']}">{PROFILE['orcid']}</a></p></section>"""
    return page("/about/", "About", "Education, research and teaching experience, and skills of Mohammed Abdalsalam.", body)


def not_found():
    body = """<section class="wrap page-head"><h1>Page not found</h1><p class="lede">The page you requested does not exist. Try the <a href="/">home page</a> or the <a href="/publications/">publications</a>.</p></section>"""
    return page("/404.html", "Page not found", "Page not found.", body).replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"')


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "assets", DIST / "assets")
    pages = {"index.html": home(), "research/index.html": research(), "publications/index.html": publications(),
             "projects/index.html": projects(), "about/index.html": about(), "404.html": not_found()}
    for rel, content in pages.items():
        out = DIST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content)
    public_pubs = {k: v for k, v in PUBS.items()}
    (DIST / "publications.json").write_text(json.dumps(public_pubs, indent=1, ensure_ascii=False))
    urls = ["/", "/research/", "/publications/", "/projects/", "/about/"]
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{BUILD_DATE}</lastmod></url>" for u in urls)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    (DIST / ".nojekyll").write_text("")
    print(f"built {len(pages)} pages into {DIST}")


if __name__ == "__main__":
    main()
