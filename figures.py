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
    return fig(svg.replace("<svg ", '<svg class="wide-fig" ', 1) + (surrogate_narrow() if "f-sur-t" in svg else filo2_narrow()), cap, "narrow")


# ---------------------------------------------------------------- FILO2 x PMOO collaboration
def truck_icon(x, y, s=1.0, cls="v1"):
    """Small side-view delivery truck facing right; (x, y) = road level under the wheels."""
    return (f'<g class="truck2 {cls}" transform="translate({x:.1f} {y:.1f}) scale({s})">'
            '<rect class="halo" x="-3" y="-17" width="35" height="21" rx="5"/>'
            '<rect class="tbox" x="0" y="-14" width="19" height="12" rx="1.8"/>'
            '<path class="tcab" d="M19.5 -10.5 h5.2 l4.3 4.6 v3.9 h-9.5 z"/><path class="twin" d="M21.2 -9 h3 l2.6 2.9 h-5.6 z"/>'
            '<circle class="wheel" cx="5" cy="-1" r="2.6"/><circle class="wheel" cx="23" cy="-1" r="2.6"/></g>')


def depot_icon(x, y, s=1.0):
    """Warehouse centred on (x, y)."""
    return (f'<g class="depot2" transform="translate({x:.1f} {y:.1f}) scale({s})">'
            '<path class="wh" d="M-13 -2 L0 -12 L13 -2 V11 H-13 Z"/><rect class="door" x="-5" y="2" width="10" height="9" rx="1"/>'
            '<path class="door-l" d="M-5 5.5 h10 M-5 8.2 h10"/></g>')


def vrp_map(x0, y0, W, H, seed=11, n=460, k=5):
    """Illustrative large-scale VRP: many customers, a central depot, one coloured route per sector, trucks on routes."""
    import math, random
    rng = random.Random(seed)
    cx, cy = x0 + W / 2, y0 + H / 2
    rx, ry = W / 2 - 8, H / 2 - 8
    centres = [(rng.uniform(-.7, .7), rng.uniform(-.7, .7)) for _ in range(6)]
    pts = []
    while len(pts) < n:
        if rng.random() < .35:
            ux, uy = rng.choice(centres); ux += rng.gauss(0, .16); uy += rng.gauss(0, .16)
        else:
            ux, uy = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if ux * ux + uy * uy <= 1 and ux * ux + uy * uy > .02:
            pts.append((cx + ux * rx, cy + uy * ry))
    off = 0.35
    def sector(px, py):
        a = (math.atan2(py - cy, px - cx) + math.pi + off) % (2 * math.pi)
        return int(a / (2 * math.pi / k)) % k
    dots, routes, stops, trucks = [], [], [], []
    for (px, py) in pts:
        dots.append(f'<circle class="c v{sector(px, py) + 1}" cx="{px:.1f}" cy="{py:.1f}" r="1.7"/>')
    for sct in range(k):
        mine = [(px, py) for px, py in pts if sector(px, py) == sct]
        far = [(px, py) for px, py in mine if ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 > .2]
        rng.shuffle(far)
        chosen = far[:8]
        allp = chosen + [(cx, cy)]
        gx, gy = sum(q[0] for q in allp) / len(allp), sum(q[1] for q in allp) / len(allp)
        ring = sorted(allp, key=lambda q: math.atan2(q[1] - gy, q[0] - gx))
        i0 = ring.index((cx, cy))
        ring = ring[i0:] + ring[:i0]          # star-shaped about the centroid, so the loop never crosses itself
        chosen = ring[1:]
        seq = ring + [(cx, cy)]
        routes.append(f'<path class="vr v{sct + 1}" d="M' + " L".join(f"{a:.1f} {b:.1f}" for a, b in seq) + '"/>')
        stops += [f'<circle class="stop v{sct + 1}" cx="{a:.1f}" cy="{b:.1f}" r="3.2"/>' for a, b in chosen]
        if sct in (0, 2, 4) and len(chosen) > 5:
            (ax, ay), (bx, by) = chosen[4], chosen[5]
            trucks.append(truck_icon((ax + bx) / 2 - 11, (ay + by) / 2 + 5, .8, f"v{sct + 1}"))
    return "".join(dots) + "".join(routes) + "".join(stops) + depot_icon(cx, cy, 1.05) + "".join(trucks)


def _vrp_legend(x, y):
    return (depot_icon(x + 8, y - 4, .62) + f'<text class="note" x="{x + 20}" y="{y}">depot</text>'
            + truck_icon(x + 78, y + 4, .62, "v1") + f'<text class="note" x="{x + 100}" y="{y}">vehicle</text>'
            + f'<circle class="c v3" cx="{x + 166}" cy="{y - 4}" r="2.4"/><circle class="c v2" cx="{x + 172}" cy="{y - 7}" r="2.4"/><circle class="c v5" cx="{x + 171}" cy="{y}" r="2.4"/>'
            + f'<text class="note" x="{x + 181}" y="{y}">customers</text>')


def filo2_scene():
    svg = f"""<svg viewBox="0 0 560 340" role="img" aria-labelledby="f-filo-t"><title id="f-filo-t">Illustration: hundreds of customers served from one depot by several vehicles, and FILO2 working inside the PMOO multi-objective loop</title>{ARROW.format(id="arF")}
<g class="dg">
<rect class="panel" x="0" y="0" width="292" height="340" rx="14"/>
<text class="lbl" x="16" y="28">Thousands of customers</text>
<text class="note" x="16" y="47">each colour is one vehicle's route</text>
{vrp_map(14, 58, 264, 240)}
{_vrp_legend(16, 326)}
<rect class="box" x="314" y="26" width="234" height="80" rx="12"/>
<text class="lbl" x="431" y="54" text-anchor="middle">PMOO</text>
<text class="note" x="431" y="76" text-anchor="middle">NSGA-II · SPEA2 · MOEA/D</text><text class="note" x="431" y="94" text-anchor="middle">keep a population of plans</text>
<rect class="box accent" x="314" y="150" width="234" height="80" rx="12"/>
<text class="lbl" x="431" y="178" text-anchor="middle">FILO2 engine</text>
<text class="note" x="431" y="200" text-anchor="middle">fast local search for very</text><text class="note" x="431" y="218" text-anchor="middle">large routing problems</text>
<path class="flow" d="M368 108 C350 125 350 132 368 148" marker-end="url(#arF)"/><path class="flow" d="M494 148 C512 132 512 125 494 108" marker-end="url(#arF)"/>
<text class="note" x="346" y="132" text-anchor="end">improve</text><text class="note" x="516" y="132">return</text>
<path class="flow" d="M431 232 V266" marker-end="url(#arF)"/>
<rect class="box" x="314" y="270" width="234" height="46" rx="12"/>
<text class="lbl" x="431" y="298" text-anchor="middle">a set of trade-off route plans</text>
</g></svg>"""
    cap = ('Illustration of the idea. FILO2 is the open-source heuristic for very large vehicle-routing problems by L. Accorsi and D. Vigo '
           '(<a href="https://doi.org/10.1016/j.cor.2024.106562">Computers &amp; Operations Research, 2024</a>). Ongoing work; no results are reported here.')
    return fig(svg.replace("<svg ", '<svg class="wide-fig" ', 1) + (surrogate_narrow() if "f-sur-t" in svg else filo2_narrow()), cap, "narrow")


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
                '<path class="flow" d="M212 55 h10" marker-end="url(#arC)"/>'
                '<rect class="box" x="226" y="26" width="88" height="58" rx="8"/><text class="mono" x="270" y="46" text-anchor="middle">speed</text><text class="mono" x="270" y="60" text-anchor="middle">fuel</text><text class="mono" x="270" y="74" text-anchor="middle">motions</text>'
                '<text class="mono dim" x="160" y="132" text-anchor="middle">simulator ≈ 9–14 s → surrogate ≈ 3 ms</text>')
    elif kind == "swr":
        bars = [(1.0, "search"), (0.74, "deduplicate"), (0.52, "screen"), (0.34, "include")]
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
        body = ('<rect class="box" x="8" y="44" width="76" height="44" rx="8"/><text class="mono" x="46" y="62" text-anchor="middle">Arabic</text><text class="mono" x="46" y="76" text-anchor="middle">text</text>'
                '<path class="flow" d="M84 60 C100 60 100 36 116 36" marker-end="url(#arC)"/><path class="flow" d="M84 72 C100 72 100 96 116 96" marker-end="url(#arC)"/>'
                '<rect class="box accent" x="120" y="16" width="96" height="40" rx="8"/><text class="mono" x="168" y="40" text-anchor="middle">BERT (tuned)</text>'
                '<rect class="box" x="120" y="76" width="96" height="40" rx="8"/><text class="mono" x="168" y="100" text-anchor="middle">LLM 0/few-shot</text>'
                '<path class="flow" d="M218 36 C234 36 234 60 248 60" marker-end="url(#arC)"/><path class="flow" d="M218 96 C234 96 234 72 248 72" marker-end="url(#arC)"/>'
                '<rect class="box" x="252" y="40" width="58" height="52" rx="8"/><text class="mono" x="281" y="62" text-anchor="middle">dialect</text><text class="mono" x="281" y="78" text-anchor="middle">label</text>'
                '<text class="mono dim" x="160" y="140" text-anchor="middle">binary and 18-dialect settings</text>')
    elif kind == "fusion":
        body = ('<rect class="box" x="8" y="18" width="96" height="36" rx="8"/><text class="mono" x="56" y="40" text-anchor="middle">narrative text</text>'
                '<rect class="box" x="8" y="62" width="96" height="36" rx="8"/><text class="mono" x="56" y="84" text-anchor="middle">attributes</text>'
                '<path class="flow" d="M106 36 C120 36 120 52 132 54" marker-end="url(#arC)"/><path class="flow" d="M106 80 C120 80 120 64 132 62" marker-end="url(#arC)"/>'
                '<rect class="box accent" x="136" y="36" width="84" height="44" rx="8"/><text class="mono" x="178" y="55" text-anchor="middle">fusion</text><text class="mono" x="178" y="69" text-anchor="middle">model</text>'
                '<path class="flow" d="M218 58 h18" marker-end="url(#arC)"/>'
                '<rect class="box" x="240" y="36" width="70" height="44" rx="8"/><text class="mono" x="275" y="56" text-anchor="middle">event</text><text class="mono" x="275" y="70" text-anchor="middle">class</text>'
                '<text class="mono dim" x="160" y="132" text-anchor="middle">Global Terrorism Database</text>')
    else:
        return ""
    return f'<svg class="dg cardfig" viewBox="0 0 320 150" role="img" aria-label="Schematic of the {kind} project">{a}{body}</svg>'


# ---------------------------------------------------------------- per-paper thumbnails
def paper_figure(kind):
    """Small schematic for a publication card (viewBox 320x150). Illustrations only."""
    a = ARROW.format(id="arT")
    if kind == "route":
        body = (f'<rect class="sea" x="8" y="8" width="304" height="134" rx="10"/>'
                '<path class="land" d="M8 100 C30 98 44 112 50 142 L8 142 Z"/><path class="land" d="M312 8 L312 60 C292 58 278 44 280 8 Z"/>'
                '<ellipse class="stormfill" cx="166" cy="76" rx="38" ry="26"/>'
                '<path class="route r3" d="M40 116 C40 50 160 24 288 34"/><path class="route r1" d="M40 116 C110 92 200 62 288 34"/><path class="route r2" d="M40 116 C150 150 260 120 288 34"/>'
                '<circle class="port" cx="40" cy="116" r="5"/><circle class="port" cx="288" cy="34" r="5"/>'
                + cpu(226, 96, 30, 8, 8) + '<text class="mono" x="268" y="116">HPC</text>')
    elif kind == "hwr":
        letters = "ا ب ت ث ج ح خ د".split()
        g = "".join(f'<rect class="box" x="{10 + (i % 4) * 26}" y="{22 + (i // 4) * 30}" width="22" height="26" rx="4"/><text class="ar" x="{21 + (i % 4) * 26}" y="{41 + (i // 4) * 30}" text-anchor="middle">{l}</text>' for i, l in enumerate(letters))
        layers = "".join(f'<rect class="layer" x="{128 + i * 16}" y="{30 + i * 6}" width="12" height="{70 - i * 12}" rx="2"/>' for i in range(4))
        body = (g + '<path class="flow" d="M114 52 h10" marker-end="url(#arT)"/>' + layers +
                '<text class="mono dim" x="152" y="118" text-anchor="middle">CNN</text>'
                '<path class="flow" d="M194 52 h8" marker-end="url(#arT)"/>'
                '<rect class="box accent" x="206" y="30" width="60" height="44" rx="8"/><text class="mono" x="236" y="49" text-anchor="middle">KAN +</text><text class="mono" x="236" y="62" text-anchor="middle">attn</text>'
                '<path class="flow" d="M264 52 h10" marker-end="url(#arT)"/>'
                '<rect class="box" x="278" y="30" width="34" height="44" rx="8"/><text class="ar big" x="295" y="60" text-anchor="middle">ج</text>'
                '<text class="mono dim" x="160" y="140" text-anchor="middle">handwritten letter → class</text>')
    elif kind == "gec":
        body = ('<rect class="box" x="14" y="18" width="292" height="40" rx="8"/>'
                '<text class="ar" x="160" y="44" text-anchor="middle">ذهبت الى <tspan class="err">المدرسه</tspan> صباحا</text>'
                '<path class="flow" d="M160 62 v18" marker-end="url(#arT)"/>'
                '<rect class="box accent" x="90" y="84" width="140" height="22" rx="6"/><text class="mono" x="160" y="99" text-anchor="middle">seq2seq + multi-task</text>'
                '<path class="flow" d="M160 108 v8" marker-end="url(#arT)"/>'
                '<rect class="box" x="14" y="118" width="292" height="28" rx="8"/>'
                '<text class="ar" x="160" y="137" text-anchor="middle">ذهبت <tspan class="fix">إلى المدرسة</tspan> صباحًا</text>')
    elif kind == "cache":
        users = "".join(f'<g transform="translate({x} {y})"><circle class="user" cx="0" cy="-8" r="5"/><path class="user" d="M-7 6 q7 -12 14 0 z"/></g>' for x, y in [(70, 128), (150, 132), (236, 126)])
        body = ('<rect class="panel" x="8" y="8" width="304" height="134" rx="10"/>'
                '<rect class="lamp" x="50" y="14" width="40" height="8" rx="3"/><path class="beam" d="M54 22 L36 110 H104 L86 22 Z"/>'
                '<text class="mono dim" x="70" y="36" text-anchor="middle">VLC</text>'
                '<path class="tower" d="M250 20 l-10 34 h20 z"/><path class="wavearc" d="M262 22 a10 10 0 0 1 0 16 M268 18 a16 16 0 0 1 0 24"/>'
                '<text class="mono dim" x="250" y="68" text-anchor="middle">mmWave</text>'
                '<rect class="box accent" x="128" y="26" width="66" height="40" rx="8"/><text class="mono" x="161" y="43" text-anchor="middle">edge</text><text class="mono" x="161" y="56" text-anchor="middle">cache</text>'
                '<path class="flow" d="M126 46 H96" marker-end="url(#arT)"/><path class="flow" d="M196 46 H236" marker-end="url(#arT)"/>'
                '<path class="flow dashed" d="M90 120 C120 100 140 104 150 116"/><text class="mono dim" x="196" y="100" text-anchor="middle">predict movement</text>'
                + users)
    elif kind == "gtd":
        body = ('<rect class="box" x="10" y="16" width="120" height="118" rx="8"/>'
                '<text class="mono" x="20" y="34">EVENT RECORD</text>'
                '<rect class="field" x="20" y="42" width="44" height="8" rx="2"/><rect class="field" x="70" y="42" width="50" height="8" rx="2"/>'
                '<rect class="field" x="20" y="56" width="30" height="8" rx="2"/><rect class="field" x="56" y="56" width="64" height="8" rx="2"/>'
                '<rect class="txt" x="20" y="74" width="100" height="5" rx="2"/><rect class="txt" x="20" y="84" width="92" height="5" rx="2"/>'
                '<rect class="txt hi" x="20" y="94" width="60" height="5" rx="2"/><rect class="txt" x="20" y="104" width="96" height="5" rx="2"/><rect class="txt" x="20" y="114" width="70" height="5" rx="2"/>'
                '<path class="flow" d="M134 75 h18" marker-end="url(#arT)"/>'
                '<rect class="box accent" x="156" y="44" width="76" height="62" rx="8"/><text class="mono" x="194" y="68" text-anchor="middle">text +</text><text class="mono" x="194" y="82" text-anchor="middle">tabular</text><text class="mono" x="194" y="96" text-anchor="middle">model</text>'
                '<path class="flow" d="M234 75 h14" marker-end="url(#arT)"/>'
                '<g class="bars3"><rect x="252" y="50" width="56" height="10" rx="2" class="b1"/><rect x="252" y="66" width="34" height="10" rx="2" class="b2"/><rect x="252" y="82" width="20" height="10" rx="2" class="b2"/></g>'
                '<text class="mono dim" x="280" y="110" text-anchor="middle">group</text>')
    elif kind == "trees":
        def tree(x, y):
            return (f'<circle class="node" cx="{x}" cy="{y}" r="6"/><circle class="node" cx="{x - 18}" cy="{y + 26}" r="6"/><circle class="node" cx="{x + 18}" cy="{y + 26}" r="6"/>'
                    f'<circle class="leaf" cx="{x - 28}" cy="{y + 52}" r="5"/><circle class="leaf" cx="{x - 8}" cy="{y + 52}" r="5"/><circle class="leaf" cx="{x + 18}" cy="{y + 52}" r="5"/>'
                    f'<path class="flow" d="M{x - 3} {y + 5} L{x - 15} {y + 21} M{x + 3} {y + 5} L{x + 15} {y + 21} M{x - 21} {y + 31} L{x - 27} {y + 47} M{x - 15} {y + 31} L{x - 9} {y + 47} M{x + 18} {y + 32} V{y + 47}"/>')
        body = (tree(50, 24) + tree(122, 24) + tree(194, 24) +
                '<path class="flow" d="M228 60 h16" marker-end="url(#arT)"/>'
                '<rect class="box accent" x="248" y="38" width="62" height="44" rx="8"/><text class="mono" x="279" y="57" text-anchor="middle">vote</text><text class="mono" x="279" y="71" text-anchor="middle">→ group</text>'
                '<text class="mono dim" x="160" y="132" text-anchor="middle">tree ensembles on event attributes</text>')
    elif kind == "bigru":
        cells = "".join(f'<rect class="box" x="{20 + i * 46}" y="40" width="36" height="26" rx="6"/><text class="mono" x="{38 + i * 46}" y="57" text-anchor="middle">GRU</text>'
                        + (f'<path class="flow" d="M{56 + i * 46} 48 h8" marker-end="url(#arT)"/><path class="flow" d="M{64 + i * 46} 60 h-8" marker-end="url(#arT)"/>' if i < 3 else '') for i in range(4))
        body = ('<rect class="box" x="14" y="96" width="196" height="28" rx="6"/><text class="mono" x="112" y="114" text-anchor="middle">tokens + event features</text>'
                + cells +
                '<path class="flow" d="M112 94 V72" marker-end="url(#arT)"/><path class="flow" d="M196 53 h14" marker-end="url(#arT)"/>'
                '<rect class="box accent" x="214" y="34" width="96" height="38" rx="8"/><text class="mono" x="262" y="51" text-anchor="middle">self-</text><text class="mono" x="262" y="64" text-anchor="middle">attention</text>'
                '<text class="mono dim" x="262" y="96" text-anchor="middle">→ group</text>')
    else:
        return card_figure(kind)
    return f'<svg class="dg cardfig" viewBox="0 0 320 150" role="img" aria-label="Schematic illustration">{a}{body}</svg>'


PAPER_FIG = {
    "abdalsalam2025towards": "route",
    "alsayed2026attention": "hwr", "alsayed2025hybrid": "hwr", "alsayed2024impact": "hwr",
    "mahmoud2026mtagec": "gec", "mahmoud2024bidirectional": "gec",
    "kombo2026location": "cache", "kombo2025mobility": "cache", "kombo2025collaborative": "cache",
    "abdalsalam2024textual": "gtd", "abdalsalam2021study": "gtd", "alfatih2019prediction": "trees", "abdalsalam2024bigru": "bigru",
    "abdalsalam2026hate": "hate", "abdalsalam2026dialect": "dialect",
}


# ---------------------------------------------------------------- S175: simulator vs surrogate race (static markup; JS animates)
def s175_race():
    return """<div class="race" id="s175-race" data-sim="8.94" data-sur="0.00265">
  <div class="race-top"><span class="lab-tag"><span class="pulse"></span>TEN SECONDS OF COMPUTE</span>
  <button type="button" class="lab-btn" id="race-go">Run ▶</button></div>
  <div class="race-row"><span class="race-name">Physics simulator</span><div class="race-bar"><i id="race-sim-bar"></i></div><b id="race-sim">0</b><span class="race-u">evaluations</span></div>
  <div class="race-row"><span class="race-name">Neural surrogate</span><div class="race-bar"><i id="race-sur-bar" class="fast"></i></div><b id="race-sur">0</b><span class="race-u">evaluations</span></div>
  <p class="mono-line dim">One case from the public S175-ML-surrogate repository: 8.94 s per simulator call vs 2.65 ms per surrogate call (×3,378). Shown in real time.</p>
</div>"""


# ---------------------------------------------------------------- upright phone versions of the wide concept figures
def surrogate_narrow():
    return f"""<svg class="narrow-fig" viewBox="0 0 340 470" role="img" aria-labelledby="f-surn-t"><title id="f-surn-t">Illustration: the slow ship simulator is replaced by a fast neural surrogate inside the optimiser</title>{ARROW.format(id="arSn")}
<g class="dg">
<rect class="sea" x="20" y="8" width="300" height="96" rx="12"/>
{ship(104, 76, 1.25)}{waves(20, 84, 300)}{waves(32, 96, 270, "wave faint")}
<text class="note" x="170" y="126" text-anchor="middle">speed, heading, waves, wind, draft …</text>
<path class="flow" d="M170 134 V154" marker-end="url(#arSn)"/>
<rect class="box" x="20" y="158" width="300" height="78" rx="12"/>
<g class="hourglass" transform="translate(40 172)"><path d="M0 0 H26 M0 48 H26 M3 0 C3 18 23 22 23 24 C23 26 3 30 3 48 M23 0 C23 18 3 22 3 24 C3 26 23 30 23 48"/><path class="sand" d="M8 44 H18 L13 34 Z"/></g>
<text class="lbl" x="84" y="186">Physics simulator</text><text class="note" x="84" y="208">accurate but slow:</text><text class="note" x="84" y="226">about 9–14 s per call</text>
<text class="note" x="170" y="258" text-anchor="middle">replaced inside the optimiser by</text>
<rect class="box accent" x="20" y="270" width="300" height="78" rx="12"/>
<g class="nn big" transform="translate(32 286)"><circle cx="6" cy="8" r="5"/><circle cx="6" cy="40" r="5"/><circle cx="28" cy="4" r="5"/><circle cx="28" cy="24" r="5"/><circle cx="28" cy="44" r="5"/><circle cx="50" cy="24" r="5"/>
<path d="M11 8 L23 4 M11 8 L23 24 M11 8 L23 44 M11 40 L23 4 M11 40 L23 24 M11 40 L23 44 M33 4 L45 24 M33 24 L45 24 M33 44 L45 24"/></g>
<text class="lbl" x="98" y="298">Neural surrogate</text><text class="note" x="98" y="320">learned from 126 M runs:</text><text class="note" x="98" y="338">≈ 3 ms per call</text>
<path class="flow" d="M170 352 V376" marker-end="url(#arSn)"/>
<rect class="box" x="20" y="380" width="300" height="52" rx="10"/>
<text class="lbl" x="170" y="403" text-anchor="middle">speed · fuel · motions</text><text class="note" x="170" y="422" text-anchor="middle">+ feasibility flags</text>
</g></svg>"""


def filo2_narrow():
    return f"""<svg class="narrow-fig" viewBox="0 0 340 640" role="img" aria-labelledby="f-filon-t"><title id="f-filon-t">Illustration: hundreds of customers served from one depot by several vehicles, and FILO2 working inside the PMOO multi-objective loop</title>{ARROW.format(id="arFn")}
<g class="dg">
<rect class="panel" x="6" y="6" width="328" height="330" rx="14"/>
<text class="lbl" x="20" y="32">Thousands of customers</text>
<text class="note" x="20" y="51">each colour is one vehicle's route</text>
{vrp_map(18, 62, 304, 236)}
{_vrp_legend(22, 322)}
<path class="flow" d="M170 340 V360" marker-end="url(#arFn)"/>
<rect class="box" x="30" y="364" width="280" height="70" rx="12"/>
<text class="lbl" x="170" y="390" text-anchor="middle">PMOO</text>
<text class="note" x="170" y="412" text-anchor="middle">NSGA-II · SPEA2 · MOEA/D</text><text class="note" x="170" y="428" text-anchor="middle">keep a population of plans</text>
<rect class="box accent" x="30" y="478" width="280" height="70" rx="12"/>
<text class="lbl" x="170" y="504" text-anchor="middle">FILO2 engine</text>
<text class="note" x="170" y="526" text-anchor="middle">fast local search for very</text><text class="note" x="170" y="542" text-anchor="middle">large routing problems</text>
<path class="flow" d="M110 436 V476" marker-end="url(#arFn)"/><path class="flow" d="M230 476 V436" marker-end="url(#arFn)"/>
<text class="note" x="102" y="462" text-anchor="end">improve</text><text class="note" x="238" y="462">return</text>
<path class="flow" d="M170 550 V576" marker-end="url(#arFn)"/>
<rect class="box" x="30" y="580" width="280" height="44" rx="12"/>
<text class="lbl" x="170" y="607" text-anchor="middle">a set of trade-off route plans</text>
</g></svg>"""


def hs_narrow():
    def box(x, y, w, h, l1, l2="", acc=False):
        t = f'<rect class="box{" accent" if acc else ""}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
        if l2:
            t += f'<text x="{x + w / 2}" y="{y + h / 2 - 3}" text-anchor="middle">{l1}</text><text class="sm" x="{x + w / 2}" y="{y + h / 2 + 14}" text-anchor="middle">{l2}</text>'
        else:
            t += f'<text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle">{l1}</text>'
        return t
    return f"""<svg class="narrow-fig" viewBox="0 0 340 416" role="img" aria-labelledby="dg-hsn-t"><title id="dg-hsn-t">Hybrid annotation and modelling pipeline for Sudanese Arabic harmful-language detection</title>{ARROW.format(id="arHn")}
<g class="dg">
{box(60, 8, 220, 48, "Telegram &amp; Twitter text")}
<path class="flow" d="M170 58 V78" marker-end="url(#arHn)"/>
{box(60, 82, 220, 48, "Normalise &amp; de-duplicate")}
<path class="flow" d="M150 132 C150 146 90 142 90 160" marker-end="url(#arHn)"/><path class="flow" d="M190 132 C190 146 250 142 250 160" marker-end="url(#arHn)"/>
{box(10, 164, 155, 60, "Weak supervision", "Sudanese rules", True)}
{box(175, 164, 155, 60, "LLM annotation", "+ native-speaker review", True)}
<path class="flow" d="M90 226 C90 246 150 240 150 258" marker-end="url(#arHn)"/><path class="flow" d="M250 226 C250 246 190 240 190 258" marker-end="url(#arHn)"/>
{box(60, 262, 220, 48, "Aggregated labels")}
<path class="flow" d="M170 312 V332" marker-end="url(#arHn)"/>
{box(40, 336, 260, 72, "Models", "transformers, ensembles, SHAP / LIME")}
</g></svg>"""
