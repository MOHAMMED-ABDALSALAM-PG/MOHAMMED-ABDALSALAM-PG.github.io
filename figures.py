"""Illustrated, responsive figures for the optimisation / HPC part of the site.

All drawings are conceptual illustrations (generic ships, maps, processors);
no data is plotted here and no third-party logos are used. Colours come from
CSS custom properties, so every figure follows the light/dark theme.
"""

ARROW = '<defs><marker id="{id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="currentColor"/></marker></defs>'


def ship(x, y, s=1.0, cls=""):
    """Side view of a generic container ship, bow to the right; (x, y) = waterline at the stern."""
    return f"""<g class="ship {cls}" transform="translate({x} {y}) scale({s})">
<path class="hull" d="M0 0 L4 -14 L92 -14 L104 -22 L108 -22 L100 0 Z"/>
<path class="hull-band" d="M2 -6 L101 -6 L99 -1 L1 -1 Z"/>
<rect class="bridge" x="8" y="-34" width="14" height="20" rx="1.5"/>
<rect class="win" x="10" y="-31" width="10" height="3"/>
<rect class="stack" x="11" y="-40" width="5" height="6"/>
<rect class="box1" x="26" y="-24" width="13" height="10"/><rect class="box2" x="40" y="-24" width="13" height="10"/>
<rect class="box3" x="54" y="-24" width="13" height="10"/><rect class="box4" x="68" y="-24" width="13" height="10"/>
<rect class="box2" x="26" y="-33" width="13" height="9"/><rect class="box4" x="40" y="-33" width="13" height="9"/>
<rect class="box1" x="54" y="-33" width="13" height="9"/><rect class="box3" x="82" y="-24" width="11" height="10"/>
</g>"""


def waves(x, y, w, cls="wave"):
    d = f"M{x} {y}" + "".join(f" q 7 -5 14 0 t 14 0" for _ in range(int(w // 28)))
    return f'<path class="{cls}" d="{d}"/>'


def cpu(x, y, size=64, lit=8, cores=8, label=""):
    """Generic CPU package with pins and a die of `cores` cores, `lit` of them active."""
    p = size
    pins = "".join(f'<rect class="pin" x="{x + 8 + i * (p - 16) / 6:.1f}" y="{y - 5}" width="3" height="5"/>'
                   f'<rect class="pin" x="{x + 8 + i * (p - 16) / 6:.1f}" y="{y + p}" width="3" height="5"/>'
                   f'<rect class="pin" x="{x - 5}" y="{y + 8 + i * (p - 16) / 6:.1f}" width="5" height="3"/>'
                   f'<rect class="pin" x="{x + p}" y="{y + 8 + i * (p - 16) / 6:.1f}" width="5" height="3"/>' for i in range(7))
    cols, rows = 4, max(1, cores // 4)
    cw = (p - 20 - (cols - 1) * 3) / cols
    ch = (p - 20 - (rows - 1) * 3) / rows
    cells = ""
    for k in range(cols * rows):
        cx = x + 10 + (k % cols) * (cw + 3)
        cy = y + 10 + (k // cols) * (ch + 3)
        cells += f'<rect class="core{" on" if k < lit else ""}" x="{cx:.1f}" y="{cy:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="1.5"/>'
    lab = f'<text class="chiplbl" x="{x + p / 2}" y="{y + p + 22}" text-anchor="middle">{label}</text>' if label else ""
    return f'<g class="cpu">{pins}<rect class="chip" x="{x}" y="{y}" width="{p}" height="{p}" rx="6"/>{cells}{lab}</g>'


def gpu(x, y, w=150, h=80, label=""):
    """Generic graphics card: board, fan, a die with many small cores, edge connector."""
    die_x, die_y, die_w, die_h = x + w * 0.46, y + 12, w * 0.46, h - 30
    cells = ""
    n_c = 12 if die_w > 40 else 6
    n_r = max(2, min(7, int((die_h - 8) / 4)))
    die_h = max(die_h, 18)
    cw, ch = (die_w - 8) / n_c, (die_h - 8) / n_r
    for i in range(n_c):
        for j in range(n_r):
            cells += f'<rect class="core on g" x="{die_x + 4 + i * cw:.1f}" y="{die_y + 4 + j * ch:.1f}" width="{cw - 1.2:.1f}" height="{ch - 1.2:.1f}"/>'
    fingers = "".join(f'<rect class="finger" x="{x + 30 + i * 7}" y="{y + h}" width="4.5" height="7"/>' for i in range(int((w - 50) / 7)))
    fan_cx, fan_cy, r = x + w * 0.24, y + h / 2 - 4, h * 0.3
    blades = "".join(f'<path class="blade" d="M{fan_cx} {fan_cy} q {r * 0.9} {-r * 0.2} {r * 0.75} {-r * 0.75}" transform="rotate({a} {fan_cx} {fan_cy})"/>' for a in range(0, 360, 60))
    lab = f'<text class="chiplbl" x="{x + w / 2}" y="{y + h + 26}" text-anchor="middle">{label}</text>' if label else ""
    return f"""<g class="gpu"><rect class="board" x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/>
<rect class="bracket" x="{x - 6}" y="{y - 4}" width="6" height="{h + 8}" rx="1.5"/>
<circle class="fan" cx="{fan_cx}" cy="{fan_cy}" r="{r}"/>{blades}<circle class="hub" cx="{fan_cx}" cy="{fan_cy}" r="{r * 0.22}"/>
<rect class="chip" x="{die_x}" y="{die_y}" width="{die_w}" height="{die_h}" rx="4"/>{cells}{fingers}{lab}</g>"""


def fig(svg, caption, cls=""):
    return f'<figure class="diagram {cls}">{svg}<figcaption>{caption}</figcaption></figure>'


# ---------------------------------------------------------------- overview (HTML cards)
def overview_story(compact=False):
    icon_weather = """<svg viewBox="0 0 120 80" aria-hidden="true" class="dg"><g>
<path class="cloud" d="M30 44 a14 14 0 0 1 6 -26 a18 18 0 0 1 34 4 a12 12 0 0 1 4 22 z"/>
<path class="wind" d="M80 26 h22 a5 5 0 1 0 -5 -5"/><path class="wind" d="M80 36 h30 a5 5 0 1 1 -5 5"/>
""" + waves(8, 64, 112) + waves(22, 74, 84) + "</g></svg>"
    icon_ship = """<svg viewBox="0 0 120 80" aria-hidden="true" class="dg"><g>""" + ship(6, 52, 0.95) + waves(0, 58, 120) + """
<g class="nn"><circle cx="96" cy="14" r="3.5"/><circle cx="108" cy="8" r="3.5"/><circle cx="108" cy="20" r="3.5"/><circle cx="84" cy="8" r="3.5"/><circle cx="84" cy="20" r="3.5"/>
<path d="M87 8 L93 14 M87 20 L93 14 M99 14 L105 8 M99 14 L105 20"/></g></g></svg>"""
    icon_hpc = '<svg viewBox="0 0 120 80" aria-hidden="true" class="dg">' + cpu(4, 14, 44, 8, 8) + gpu(62, 18, 54, 36) + "</svg>"
    icon_routes = """<svg viewBox="0 0 120 80" aria-hidden="true" class="dg"><rect class="sea" x="2" y="2" width="116" height="76" rx="8"/>
<path class="land" d="M2 56 C18 52 26 64 28 78 L2 78 Z"/><path class="land" d="M118 2 L118 30 C104 28 96 18 98 2 Z"/>
<path class="route r1" d="M20 64 C48 52 76 36 102 18"/><path class="route r2" d="M20 64 C62 76 98 56 102 18"/><path class="route r3" d="M20 64 C18 30 60 10 102 18"/>
<circle class="port" cx="20" cy="64" r="4"/><circle class="port" cx="102" cy="18" r="4"/></svg>"""
    steps = [
        (icon_weather, "1 · Sea and weather", "Forecasts of wind and waves along every possible path between two ports."),
        (icon_ship, "2 · Ship performance", "How speed, fuel and motions respond to the sea. A physics simulator of the S175 ship, made fast with a neural-network surrogate."),
        (icon_hpc, "3 · Parallel optimisation", "PMOO runs evolutionary algorithms (NSGA-II, SPEA2, MOEA/D) on multi-core CPUs, GPUs, or both together."),
        (icon_routes, "4 · A set of good routes", "Not one answer but a Pareto set: faster, more economical or safer routes, so the crew can choose."),
    ]
    cards = "".join(f'<li class="story-step"><div class="story-ic">{ic}</div><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in steps)
    return f'<ol class="story{" compact" if compact else ""}" aria-label="How the parts of the doctoral work fit together">{cards}</ol>'


# ---------------------------------------------------------------- weather routing scene + Pareto front
def routing_scene():
    a = ARROW.format(id="arR")
    map_svg = f"""<svg viewBox="0 0 460 310" role="img" aria-labelledby="f-map-t"><title id="f-map-t">Illustration: three candidate routes between two ports around a storm</title>{a}
<g class="dg">
<rect class="sea" x="0" y="0" width="460" height="310" rx="14"/>
{waves(150, 40, 90, "wave faint")}{waves(40, 120, 84, "wave faint")}{waves(300, 270, 112, "wave faint")}{waves(260, 220, 56, "wave faint")}
<path class="land" d="M0 175 C36 170 62 192 74 222 C86 252 70 290 56 310 L0 310 Z"/>
<path class="land" d="M460 0 L460 128 C428 122 398 100 392 66 C386 36 400 14 412 0 Z"/>
<g class="storm"><ellipse cx="236" cy="168" rx="70" ry="48"/>
<path class="cloud" d="M214 168 a11 11 0 0 1 4 -21 a15 15 0 0 1 28 3 a10 10 0 0 1 3 18 z"/>
<path class="bolt" d="M234 172 l-6 12 h7 l-4 12 l12 -16 h-7 l5 -8 z"/>
<text class="lbl" x="236" y="140" text-anchor="middle">storm</text></g>
<path class="windarrow" d="M128 160 l28 -10" marker-end="url(#arR)"/><path class="windarrow" d="M138 182 l28 -10" marker-end="url(#arR)"/>
<path class="route r3" d="M64 236 C62 120 210 52 402 70"/>
<path class="route r1" d="M64 236 C150 200 270 140 402 70"/>
<path class="route r2" d="M64 236 C200 286 352 236 402 70"/>
{ship(118, 112, 0.42, "onroute")}
<circle class="port" cx="64" cy="236" r="7"/><circle class="port" cx="402" cy="70" r="7"/>
<text class="lbl" x="44" y="262" text-anchor="middle">Port A</text><text class="lbl" x="410" y="100" text-anchor="middle">Port B</text>
<rect class="legendbg" x="96" y="276" width="356" height="28" rx="14"/>
<circle class="dot r1" cx="114" cy="290" r="6"/><text class="lbl" x="126" y="295">fastest</text>
<circle class="dot r3" cx="212" cy="290" r="6"/><text class="lbl" x="224" y="295">safest</text>
<circle class="dot r2" cx="304" cy="290" r="6"/><text class="lbl" x="316" y="295">least fuel</text>
</g></svg>"""
    pareto_svg = f"""<svg viewBox="0 0 460 310" role="img" aria-labelledby="f-par-t"><title id="f-par-t">Illustration: a Pareto front of routes trading voyage time against fuel</title>{ARROW.format(id="arP")}
<g class="dg">
<rect class="panel" x="0" y="0" width="460" height="310" rx="14"/>
<path class="axis" d="M60 262 H436" marker-end="url(#arP)"/><path class="axis" d="M60 262 V26" marker-end="url(#arP)"/>
<text class="lbl" x="436" y="292" text-anchor="end">voyage time →</text>
<text class="lbl" x="22" y="140" text-anchor="middle" transform="rotate(-90 22 140)">fuel use →</text>
<g class="dominated"><circle cx="250" cy="150" r="6"/><circle cx="300" cy="120" r="6"/><circle cx="340" cy="190" r="6"/><circle cx="210" cy="210" r="6"/><circle cx="380" cy="80" r="6"/><circle cx="290" cy="200" r="6"/><circle cx="170" cy="120" r="6"/></g>
<path class="front" d="M96 60 C130 150 220 205 404 226"/>
<g class="frontpts"><circle cx="122" cy="118" r="6"/><circle cx="148" cy="152" r="6"/><circle cx="232" cy="198" r="6"/><circle cx="300" cy="214" r="6"/></g>
<circle class="dot r1" cx="100" cy="72" r="8"/><circle class="dot r3" cx="184" cy="180" r="8"/><circle class="dot r2" cx="380" cy="224" r="8"/>
<text class="lbl" x="116" y="62">fastest</text><text class="lbl" x="196" y="166">safest</text><text class="lbl" x="372" y="252" text-anchor="middle">least fuel</text>
<text class="note" x="250" y="60">grey points: worse in both,</text><text class="note" x="250" y="78">discarded by the optimiser</text>
<text class="note" x="250" y="104">curve: Pareto front, the best</text><text class="note" x="250" y="122">compromises</text>
</g></svg>"""
    cap = ("Illustration, not data. Weather routing has several goals that pull against each other, so the optimiser returns a whole "
           "front of good compromise routes instead of one route.")
    return f'<figure class="diagram"><div class="fig-pair">{map_svg}{pareto_svg}</div><figcaption>{cap}</figcaption></figure>'


# ---------------------------------------------------------------- PMOO hardware
def pmoo_hardware():
    def card(title, sub, svg):
        return f'<li class="hw"><svg viewBox="0 0 170 120" aria-hidden="true" class="dg">{svg}</svg><h4>{title}</h4><p>{sub}</p></li>'
    serial = cpu(53, 22, 64, 1, 8)
    omp = cpu(53, 22, 64, 8, 8)
    cuda = gpu(14, 22, 146, 76)
    hybrid = cpu(10, 34, 50, 8, 8) + '<path class="link" d="M66 59 H82"/>' + gpu(90, 30, 76, 52)
    cards = "".join([
        card("Serial", "One CPU core does all the work. The reference point.", serial),
        card("CPU · OpenMP", "All cores of the processor share the population.", omp),
        card("GPU · CUDA", "Thousands of GPU threads evaluate routes at the same time.", cuda),
        card("Hybrid · CPU + GPU", "CPU and GPU split each generation between them.", hybrid),
    ])
    gen = ('<ol class="gen" aria-label="One generation of the evolutionary algorithm">'
           '<li><b>Create</b> new candidate routes by recombining and mutating good ones</li>'
           '<li><b>Evaluate</b> time, fuel and safety of every route (the costly step)</li>'
           '<li><b>Rank and select</b> the best compromises for the next generation</li></ol>')
    cap = ("Illustration of the four PMOO execution modes. The same algorithm (NSGA-II, SPEA2 or MOEA/D) runs in every mode, "
           "so speed and solution quality can be compared fairly. Generic processor drawings; no vendor logos.")
    return f'<figure class="diagram hwfig"><p class="fig-title">One generation, repeated hundreds of times</p>{gen}<ul class="hw-grid">{cards}</ul><figcaption>{cap}</figcaption></figure>'


# ---------------------------------------------------------------- S175 surrogate
def surrogate_scene():
    svg = f"""<svg viewBox="0 0 520 330" role="img" aria-labelledby="f-sur-t"><title id="f-sur-t">Illustration: the slow ship simulator is replaced by a fast neural surrogate inside the optimiser</title>{ARROW.format(id="arS")}
<g class="dg">
<rect class="sea" x="140" y="8" width="240" height="96" rx="12"/>
{ship(194, 76, 1.25)}{waves(140, 84, 240)}{waves(152, 96, 210, "wave faint")}
<text class="lbl" x="130" y="36" text-anchor="end">ship speed</text><text class="lbl" x="130" y="58" text-anchor="end">and heading</text>
<text class="lbl" x="390" y="36">waves, wind,</text><text class="lbl" x="390" y="58">draft …</text>
<path class="flow" d="M260 108 C260 130 130 124 130 150" marker-end="url(#arS)"/>
<path class="flow" d="M260 108 C260 130 390 124 390 150" marker-end="url(#arS)"/>
<rect class="box" x="20" y="154" width="220" height="92" rx="12"/>
<g class="hourglass" transform="translate(44 176)"><path d="M0 0 H26 M0 48 H26 M3 0 C3 18 23 22 23 24 C23 26 3 30 3 48 M23 0 C23 18 3 22 3 24 C3 26 23 30 23 48"/><path class="sand" d="M8 44 H18 L13 34 Z"/></g>
<text class="lbl" x="84" y="184">Physics simulator</text><text class="note" x="84" y="206">accurate but slow:</text><text class="note" x="84" y="226">about 9–14 s per call</text>
<rect class="box accent" x="280" y="154" width="220" height="92" rx="12"/>
<g class="nn big" transform="translate(296 174)"><circle cx="6" cy="8" r="5"/><circle cx="6" cy="40" r="5"/><circle cx="28" cy="4" r="5"/><circle cx="28" cy="24" r="5"/><circle cx="28" cy="44" r="5"/><circle cx="50" cy="24" r="5"/>
<path d="M11 8 L23 4 M11 8 L23 24 M11 8 L23 44 M11 40 L23 4 M11 40 L23 24 M11 40 L23 44 M33 4 L45 24 M33 24 L45 24 M33 44 L45 24"/></g>
<text class="lbl" x="362" y="184">Neural surrogate</text><text class="note" x="362" y="206">learned from 126 M</text><text class="note" x="362" y="226">runs: ≈ 3 ms per call</text>
<path class="flow" d="M390 250 C390 272 260 268 260 290" marker-end="url(#arS)"/>
<path class="flow dashed" d="M130 250 C130 272 260 268 260 290"/>
<rect class="box" x="120" y="292" width="280" height="34" rx="10"/>
<text class="lbl" x="260" y="314" text-anchor="middle">speed · fuel · motions + feasibility</text>
</g></svg>"""
    cap = ("Illustration. The optimiser needs ship performance millions of times; a neural surrogate trained on 126 million simulator "
           "runs answers about 3,000–5,000× faster, and separate classifiers flag operating points the simulator cannot evaluate. "
           "Timings from the public S175-ML-surrogate repository.")
    return fig(svg, cap, "narrow")


# ---------------------------------------------------------------- FILO2 x PMOO collaboration
def filo2_scene():
    import math
    depot = (110, 165)
    routes = {
        "r1": [(60, 80), (100, 60), (150, 75)],
        "r2": [(185, 120), (200, 175), (180, 225)],
        "r3": [(130, 260), (70, 250), (40, 200)],
        "r4": [(30, 140), (45, 105)],
    }
    paths, pts = "", ""
    for cls, cs in routes.items():
        seq = [depot] + cs + [depot]
        paths += f'<path class="route thin {cls}" d="M' + " L".join(f"{x} {y}" for x, y in seq) + '"/>'
        pts += "".join(f'<circle class="cust" cx="{x}" cy="{y}" r="5"/>' for x, y in cs)
    truck = """<g class="truck" transform="translate(150 290)"><rect class="tbox" x="0" y="-18" width="26" height="16" rx="2"/><path class="tcab" d="M26 -13 h8 l5 6 v5 h-13 z"/><circle class="wheel" cx="7" cy="0" r="3.5"/><circle class="wheel" cx="31" cy="0" r="3.5"/></g>"""
    svg = f"""<svg viewBox="0 0 520 330" role="img" aria-labelledby="f-filo-t"><title id="f-filo-t">Illustration: vehicle routes from a depot, and FILO2 working inside the PMOO multi-objective loop</title>{ARROW.format(id="arF")}
<g class="dg">
<rect class="panel" x="0" y="0" width="230" height="330" rx="14"/>
{paths}{pts}<rect class="depot" x="{depot[0] - 10}" y="{depot[1] - 10}" width="20" height="20" rx="3"/>
<text class="lbl" x="{depot[0]}" y="{depot[1] + 30}" text-anchor="middle">depot</text>
{truck}<text class="note" x="196" y="296">vehicles</text>
<text class="lbl" x="115" y="28" text-anchor="middle">thousands of customers</text>
<rect class="box" x="262" y="26" width="244" height="80" rx="12"/>
<text class="lbl" x="384" y="54" text-anchor="middle">PMOO</text>
<text class="note" x="384" y="76" text-anchor="middle">NSGA-II · SPEA2 · MOEA/D</text><text class="note" x="384" y="94" text-anchor="middle">keep a population of plans</text>
<rect class="box accent" x="262" y="150" width="244" height="80" rx="12"/>
<text class="lbl" x="384" y="178" text-anchor="middle">FILO2 engine</text>
<text class="note" x="384" y="200" text-anchor="middle">fast local search for very</text><text class="note" x="384" y="218" text-anchor="middle">large routing problems</text>
<path class="flow" d="M318 108 C300 125 300 132 318 148" marker-end="url(#arF)"/><path class="flow" d="M450 148 C468 132 468 125 450 108" marker-end="url(#arF)"/>
<text class="note" x="294" y="132" text-anchor="end">improve</text><text class="note" x="474" y="132">return</text>
<path class="flow" d="M384 232 V266" marker-end="url(#arF)"/>
<rect class="box" x="262" y="270" width="244" height="46" rx="12"/>
<text class="lbl" x="384" y="298" text-anchor="middle">a set of trade-off route plans</text>
</g></svg>"""
    cap = ('Illustration of the idea. FILO2 is the open-source heuristic for very large vehicle-routing problems by L. Accorsi and D. Vigo '
           '(<a href="https://doi.org/10.1016/j.cor.2024.106562">Computers &amp; Operations Research, 2024</a>). Ongoing work; no results are reported here.')
    return fig(svg, cap, "narrow")


# ---------------------------------------------------------------- small card figures (software cards)
def _steps(labels, y=58, x0=12, w=None, accent=None, sub=None):
    """A row of small step boxes joined by arrows; used for compact pipeline figures."""
    n = len(labels)
    w = w or (296 - (n - 1) * 14) / n
    out = ""
    for i, lab in enumerate(labels):
        x = x0 + i * (w + 14)
        cls = "box accent" if accent and i in accent else "box"
        out += f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{w:.1f}" height="46" rx="8"/>'
        lines = lab.split("|")
        for k, ln in enumerate(lines):
            out += f'<text class="mono" x="{x + w / 2:.1f}" y="{y + 22 + (k - (len(lines) - 1) / 2) * 13:.1f}" text-anchor="middle">{ln}</text>'
        if sub and sub[i]:
            out += f'<text class="mono dim" x="{x + w / 2:.1f}" y="{y + 64}" text-anchor="middle">{sub[i]}</text>'
        if i < n - 1:
            out += f'<path class="flow" d="M{x + w + 2:.1f} {y + 23} h10" marker-end="url(#arC)"/>'
    return out


def card_figure(kind):
    a = ARROW.format(id="arC")
    if kind == "pmoo":
        body = (cpu(18, 30, 52, 8, 8) + gpu(96, 32, 92, 50) +
                '<path class="link" d="M74 56 H88"/>' +
                '<text class="mono" x="44" y="112" text-anchor="middle">OpenMP</text><text class="mono" x="142" y="112" text-anchor="middle">CUDA</text>'
                '<rect class="box accent" x="212" y="26" width="96" height="76" rx="8"/>'
                '<text class="mono" x="260" y="48" text-anchor="middle">NSGA-II</text><text class="mono" x="260" y="66" text-anchor="middle">SPEA2</text><text class="mono" x="260" y="84" text-anchor="middle">MOEA/D</text>'
                '<path class="flow" d="M192 56 h16" marker-end="url(#arC)"/>'
                '<text class="mono dim" x="160" y="140" text-anchor="middle">serial · cpu · gpu · hybrid</text>')
    elif kind == "s175":
        body = (f'<rect class="sea" x="10" y="20" width="96" height="70" rx="8"/>{ship(16, 66, 0.8)}{waves(10, 72, 96)}'
                '<text class="mono dim" x="58" y="108" text-anchor="middle">9 inputs</text>'
                '<path class="flow" d="M110 55 h16" marker-end="url(#arC)"/>'
                '<rect class="box" x="130" y="18" width="80" height="32" rx="8"/><text class="mono" x="170" y="38" text-anchor="middle">feasible?</text>'
                '<rect class="box accent" x="130" y="60" width="80" height="32" rx="8"/><text class="mono" x="170" y="80" text-anchor="middle">regressor</text>'
                '<path class="flow" d="M214 55 h16" marker-end="url(#arC)"/>'
                '<rect class="box" x="234" y="30" width="76" height="50" rx="8"/><text class="mono" x="272" y="52" text-anchor="middle">speed</text><text class="mono" x="272" y="68" text-anchor="middle">fuel · motion</text>'
                '<text class="mono dim" x="160" y="132" text-anchor="middle">simulator ≈ 9–14 s → surrogate ≈ 3 ms</text>')
    elif kind == "swr":
        bars = [(1.0, "search"), (0.66, "deduplicate"), (0.4, "screen"), (0.2, "include")]
        body = ""
        for i, (f, lab) in enumerate(bars):
            w = 200 * f
            body += f'<rect class="funnel f{i}" x="{160 - w / 2:.1f}" y="{14 + i * 30}" width="{w:.1f}" height="24" rx="5"/>'
            body += f'<text class="mono" x="{160}" y="{30 + i * 30}" text-anchor="middle">{lab}</text>'
        body += '<text class="mono dim" x="160" y="140" text-anchor="middle">PRISMA 2020 · reproducible queries and logs</text>'
    elif kind == "hate":
        body = _steps(["social|media", "clean", "rules|+ LLM", "models|+ SHAP"], y=34, accent=[2],
                      sub=["Telegram", "dedupe", "native review", "explain"])
        body += '<text class="mono dim" x="160" y="140" text-anchor="middle">Sudanese Arabic · harmful-language detection</text>'
    elif kind == "dialect":
        body = ('<rect class="box" x="12" y="44" width="70" height="44" rx="8"/><text class="mono" x="47" y="70" text-anchor="middle">Arabic text</text>'
                '<path class="flow" d="M84 60 C100 60 100 36 116 36" marker-end="url(#arC)"/><path class="flow" d="M84 72 C100 72 100 96 116 96" marker-end="url(#arC)"/>'
                '<rect class="box accent" x="120" y="16" width="96" height="40" rx="8"/><text class="mono" x="168" y="40" text-anchor="middle">fine-tuned BERT</text>'
                '<rect class="box" x="120" y="76" width="96" height="40" rx="8"/><text class="mono" x="168" y="100" text-anchor="middle">LLM 0/few-shot</text>'
                '<path class="flow" d="M218 36 C234 36 234 60 248 60" marker-end="url(#arC)"/><path class="flow" d="M218 96 C234 96 234 72 248 72" marker-end="url(#arC)"/>'
                '<rect class="box" x="252" y="40" width="58" height="52" rx="8"/><text class="mono" x="281" y="62" text-anchor="middle">dialect</text><text class="mono" x="281" y="78" text-anchor="middle">label</text>'
                '<text class="mono dim" x="160" y="140" text-anchor="middle">binary and 18-dialect settings</text>')
    elif kind == "fusion":
        body = ('<rect class="box" x="12" y="18" width="84" height="36" rx="8"/><text class="mono" x="54" y="40" text-anchor="middle">narrative text</text>'
                '<rect class="box" x="12" y="62" width="84" height="36" rx="8"/><text class="mono" x="54" y="84" text-anchor="middle">attributes</text>'
                '<path class="flow" d="M98 36 C116 36 116 52 132 54" marker-end="url(#arC)"/><path class="flow" d="M98 80 C116 80 116 64 132 62" marker-end="url(#arC)"/>'
                '<rect class="box accent" x="136" y="36" width="80" height="44" rx="8"/><text class="mono" x="176" y="62" text-anchor="middle">fusion model</text>'
                '<path class="flow" d="M218 58 h18" marker-end="url(#arC)"/>'
                '<rect class="box" x="240" y="36" width="70" height="44" rx="8"/><text class="mono" x="275" y="56" text-anchor="middle">event</text><text class="mono" x="275" y="70" text-anchor="middle">class</text>'
                '<text class="mono dim" x="160" y="132" text-anchor="middle">Global Terrorism Database</text>')
    else:
        return ""
    return f'<svg class="dg cardfig" viewBox="0 0 320 150" role="img" aria-label="Schematic of the {kind} project">{a}{body}</svg>'
