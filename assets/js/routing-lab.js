/* Weather-routing lab: an illustrative browser model (not the research code).
   45 candidate voyages (9 paths x 5 speeds) between two ports around a storm.
   Each voyage gets three objectives -- time, fuel and the highest wave met --
   and the Pareto front among them is shown. The user changes storm strength
   and the preference; the chosen voyage is animated. */
(function () {
  "use strict";
  var host = document.getElementById("routing-lab");
  if (!host) return;
  var NS = "http://www.w3.org/2000/svg";
  var W = 600, H = 300, A = { x: 70, y: 236 }, B = { x: 532, y: 72 }, C = { x: 300, y: 150 };
  var SPEEDS = [12, 13.5, 15, 16.5, 18], OFFS = [-200, -150, -100, -50, 0, 50, 100, 150, 200];
  var NM_PER_UNIT = 2.2, reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var state = { s: 0.6, pref: "balanced", t: 0, raf: 0, playing: !reduce };

  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function pathPts(off) {
    var mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2, dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy);
    var cx = mx + (-dy / L) * off, cy = my + (dx / L) * off, pts = [];
    for (var i = 0; i <= 60; i++) {
      var t = i / 60, u = 1 - t;
      pts.push({ x: u * u * A.x + 2 * u * t * cx + t * t * B.x, y: u * u * A.y + 2 * u * t * cy + t * t * B.y });
    }
    return pts;
  }
  var PATHS = OFFS.map(pathPts);

  function wave(p, s) {
    var R = 55 + 75 * s, d2 = (p.x - C.x) * (p.x - C.x) + (p.y - C.y) * (p.y - C.y);
    return 1.2 + 7.5 * s * Math.exp(-d2 / (R * R));
  }
  function evaluate(s) {
    var out = [];
    PATHS.forEach(function (pts, pi) {
      SPEEDS.forEach(function (v) {
        var time = 0, fuel = 0, hmax = 0;
        for (var i = 1; i < pts.length; i++) {
          var mid = { x: (pts[i].x + pts[i - 1].x) / 2, y: (pts[i].y + pts[i - 1].y) / 2 };
          var h = wave(mid, s), nm = Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y) * NM_PER_UNIT;
          var eff = v * Math.max(0.45, 1 - 0.055 * h), dt = nm / eff;
          time += dt; fuel += dt * 0.0016 * v * v * v * (1 + 0.09 * h) / 10; hmax = Math.max(hmax, h);
        }
        out.push({ pi: pi, v: v, time: time, fuel: fuel, hmax: hmax });
      });
    });
    out.forEach(function (a) {
      a.front = !out.some(function (b) {
        return b !== a && b.time <= a.time && b.fuel <= a.fuel && b.hmax <= a.hmax &&
          (b.time < a.time || b.fuel < a.fuel || b.hmax < a.hmax);
      });
    });
    return out;
  }
  function choose(c, pref) {
    var f = c.filter(function (x) { return x.front; });
    function rng(k) { var v = f.map(function (x) { return x[k]; }); return [Math.min.apply(0, v), Math.max.apply(0, v)]; }
    var rt = rng("time"), rf = rng("fuel"), rh = rng("hmax");
    function n(x, r) { return r[1] > r[0] ? (x - r[0]) / (r[1] - r[0]) : 0; }
    var w = { fastest: [1, 0.02, 0.02], fuel: [0.02, 1, 0.02], safest: [0.05, 0.05, 1], balanced: [1, 1, 1] }[pref];
    var best = null, bs = Infinity;
    f.forEach(function (x) {
      var sc = w[0] * n(x.time, rt) + w[1] * n(x.fuel, rf) + w[2] * n(x.hmax, rh);
      if (sc < bs) { bs = sc; best = x; }
    });
    return best;
  }

  // ---------- DOM
  host.innerHTML = "";
  host.classList.add("lab-live");
  var top = document.createElement("div"); top.className = "lab-top";
  top.innerHTML = '<span class="lab-tag"><span class="pulse"></span>BROWSER SIMULATION</span><span class="lab-status" aria-live="polite"></span>';
  var playBtn = document.createElement("button"); playBtn.type = "button"; playBtn.className = "lab-btn";
  top.appendChild(playBtn); host.appendChild(top);

  var tabs = document.createElement("div"); tabs.className = "lab-tabs"; tabs.setAttribute("role", "group"); tabs.setAttribute("aria-label", "Sea state");
  [["01", "Calm sea", 0.0], ["02", "Storm", 0.6], ["03", "Severe storm", 1.0]].forEach(function (d) {
    var b = document.createElement("button"); b.type = "button"; b.className = "lab-tab"; b.dataset.s = d[2];
    b.innerHTML = '<span class="n">' + d[0] + "</span> " + d[1]; tabs.appendChild(b);
  });
  host.appendChild(tabs);

  var svg = el("svg", { viewBox: "0 0 " + W + " " + H, class: "lab-map", role: "img", "aria-label": "Map with candidate voyages around a storm; the highlighted route is the current choice" }, host);
  var defs = el("defs", {}, svg);
  var grad = el("linearGradient", { id: "labSeaGrad", x1: 0, y1: 0, x2: 0.4, y2: 1 }, defs);
  el("stop", { offset: "0", class: "sea-a" }, grad); el("stop", { offset: "1", class: "sea-b" }, grad);
  var pat = el("pattern", { id: "labWaves", width: 36, height: 22, patternUnits: "userSpaceOnUse" }, defs);
  el("path", { d: "M2 12 q7 -6 14 0 M20 4 q7 -6 14 0", class: "lab-wavepat" }, pat);
  el("rect", { x: 0, y: 0, width: W, height: H, rx: 12, fill: "url(#labSeaGrad)" }, svg);
  el("rect", { x: 0, y: 0, width: W, height: H, rx: 12, fill: "url(#labWaves)" }, svg);
  el("path", { d: "M0 190 C40 186 70 206 84 236 C96 262 84 290 74 300 L0 300 Z", class: "lab-land" }, svg);
  el("path", { d: "M600 0 L600 120 C566 116 530 98 522 66 C516 38 528 14 540 0 Z", class: "lab-land" }, svg);
  var storm = el("g", {}, svg), rings = [];
  for (var r = 0; r < 4; r++) rings.push(el("circle", { cx: C.x, cy: C.y, class: "lab-storm r" + r }, storm));
  var stormLbl = el("text", { x: C.x, y: C.y + 4, "text-anchor": "middle", class: "lab-mono" }, storm);
  var candG = el("g", {}, svg), candEls = PATHS.map(function (pts) {
    return el("path", { d: "M" + pts.map(function (p) { return p.x.toFixed(1) + " " + p.y.toFixed(1); }).join(" L"), class: "lab-cand" }, candG);
  });
  var chosen = el("path", { class: "lab-route" }, svg);
  var done = el("path", { class: "lab-done" }, svg);
  [A, B].forEach(function (p, i) {
    el("circle", { cx: p.x, cy: p.y, r: 7, class: "lab-port" }, svg);
    var t = el("text", { x: i ? 566 : 40, y: i ? 36 : 272, "text-anchor": "middle", class: "lab-mono strong" }, svg);
    t.textContent = i ? "PORT B" : "PORT A";
  });
  var shipG = el("g", { class: "lab-ship" }, svg);
  // S175 container ship seen from above, bow pointing +x (about 46 x 13 map units)
  el("path", { d: "M-24 -5 L-24 5 Q-24 6.5 -22 6.5 L12 6.5 Q20 6.5 24 0 Q20 -6.5 12 -6.5 L-22 -6.5 Q-24 -6.5 -24 -5 Z", class: "hull" }, shipG);
  var cols = ["c1", "c2", "c3", "c4", "c2", "c1", "c3"];
  for (var ci = 0; ci < 7; ci++) {
    el("rect", { x: -14 + ci * 4.4, y: -5, width: 3.8, height: 4.6, class: "box " + cols[ci] }, shipG);
    el("rect", { x: -14 + ci * 4.4, y: 0.4, width: 3.8, height: 4.6, class: "box " + cols[(ci + 2) % 7] }, shipG);
  }
  el("rect", { x: -21.5, y: -5, width: 5.5, height: 10, rx: 1, class: "bridge" }, shipG);
  el("rect", { x: -20.5, y: -1.2, width: 2.2, height: 2.4, class: "funnel" }, shipG);
  var shipLbl = el("text", { class: "lab-shiplbl", "text-anchor": "middle" }, svg); shipLbl.textContent = "S175";

  var prefs = document.createElement("div"); prefs.className = "lab-prefs"; prefs.setAttribute("role", "group"); prefs.setAttribute("aria-label", "What matters most");
  prefs.innerHTML = '<span class="lab-mono-h">WHAT MATTERS MOST</span>';
  [["fastest", "Time"], ["fuel", "Fuel"], ["safest", "Safety"], ["balanced", "Balanced"]].forEach(function (d) {
    var b = document.createElement("button"); b.type = "button"; b.className = "lab-pref"; b.dataset.pref = d[0]; b.textContent = d[1]; prefs.appendChild(b);
  });
  host.appendChild(prefs);

  var stats = document.createElement("div"); stats.className = "lab-stats";
  stats.innerHTML = [["time", "Voyage time", "hours"], ["fuel", "Fuel", "tonnes (model units)"], ["wave", "Highest wave met", "metres"], ["front", "Pareto-optimal voyages", "of 45 candidates"]]
    .map(function (d) { return '<div><span class="k">' + d[1] + '</span><b id="lab-' + d[0] + '">–</b><span class="u">' + d[2] + "</span></div>"; }).join("");
  host.appendChild(stats);

  var bottom = document.createElement("div"); bottom.className = "lab-bottom";
  var par = el("svg", { viewBox: "0 0 300 150", class: "lab-pareto", role: "img", "aria-label": "Fuel against voyage time for all candidate voyages" });
  var slider = document.createElement("label"); slider.className = "lab-slider";
  slider.innerHTML = '<span class="lab-mono-h">STORM STRENGTH <b id="lab-s"></b></span><input type="range" min="0" max="100" step="1" aria-label="Storm strength">';
  var legend = document.createElement("p"); legend.className = "lab-legend";
  legend.innerHTML = '<span><i class="lg-front"></i>Pareto-optimal</span><span><i class="lg-dom"></i>dominated</span><span><i class="lg-sel"></i>chosen voyage</span>';
  var side = document.createElement("div"); side.appendChild(slider); side.appendChild(legend);
  bottom.appendChild(par); bottom.appendChild(side); host.appendChild(bottom);
  var range = slider.querySelector("input");

  // ---------- render
  var cur = null, pick = null;
  function render() {
    var s = state.s;
    rings.forEach(function (c, i) { c.setAttribute("r", (55 + 75 * s) * (1 - i * 0.22)); c.style.opacity = s < 0.03 ? 0 : 1; });
    stormLbl.textContent = s < 0.03 ? "" : "STORM";
    cur = evaluate(s); pick = choose(cur, state.pref);
    var frontPaths = {};
    cur.forEach(function (x) { if (x.front) frontPaths[x.pi] = 1; });
    candEls.forEach(function (p, i) { p.setAttribute("class", "lab-cand" + (frontPaths[i] ? " on" : "")); });
    chosen.setAttribute("d", candEls[pick.pi].getAttribute("d"));
    document.getElementById("lab-time").textContent = pick.time.toFixed(1);
    document.getElementById("lab-fuel").textContent = pick.fuel.toFixed(1);
    document.getElementById("lab-wave").textContent = pick.hmax.toFixed(1);
    document.getElementById("lab-front").textContent = cur.filter(function (x) { return x.front; }).length;
    document.getElementById("lab-s").textContent = Math.round(s * 100) + "%";
    range.value = Math.round(s * 100);
    host.querySelector(".lab-status").textContent = (s < 0.03 ? "Calm sea" : s < 0.8 ? "Storm on the direct path" : "Severe storm") + " · " + pick.v + " kn";
    Array.prototype.forEach.call(tabs.children, function (b) { b.setAttribute("aria-pressed", Math.abs(+b.dataset.s - s) < 0.01 ? "true" : "false"); });
    Array.prototype.forEach.call(prefs.querySelectorAll(".lab-pref"), function (b) { b.setAttribute("aria-pressed", b.dataset.pref === state.pref ? "true" : "false"); });
    drawPareto();
    if (!state.playing) placeShip(0.5);
  }
  function drawPareto() {
    while (par.firstChild) par.removeChild(par.firstChild);
    var tx = cur.map(function (x) { return x.time; }), fy = cur.map(function (x) { return x.fuel; });
    var t0 = Math.min.apply(0, tx), t1 = Math.max.apply(0, tx), f0 = Math.min.apply(0, fy), f1 = Math.max.apply(0, fy);
    function X(t) { return 36 + (t - t0) / ((t1 - t0) || 1) * 250; }
    function Y(f) { return 124 - (f - f0) / ((f1 - f0) || 1) * 110; }
    el("path", { d: "M36 8 V128 H292", class: "lab-axis" }, par);
    var a1 = el("text", { x: 292, y: 144, "text-anchor": "end", class: "lab-mono" }, par); a1.textContent = "VOYAGE TIME →";
    var a2 = el("text", { x: 12, y: 70, "text-anchor": "middle", class: "lab-mono", transform: "rotate(-90 12 70)" }, par); a2.textContent = "FUEL →";
    cur.slice().sort(function (a, b) { return a.front - b.front; }).forEach(function (x) {
      el("circle", { cx: X(x.time), cy: Y(x.fuel), r: x.front ? 4.2 : 3.2, class: x.front ? "pt front" : "pt" }, par);
    });
    el("circle", { cx: X(pick.time), cy: Y(pick.fuel), r: 8, class: "pt sel" }, par);
  }
  function placeShip(t) {
    var pts = PATHS[pick.pi], f = t * (pts.length - 1), i = Math.min(pts.length - 2, Math.floor(f)), u = f - i;
    var x = pts[i].x + (pts[i + 1].x - pts[i].x) * u, y = pts[i].y + (pts[i + 1].y - pts[i].y) * u;
    var ang = Math.atan2(pts[i + 1].y - pts[i].y, pts[i + 1].x - pts[i].x) * 180 / Math.PI;
    shipG.setAttribute("transform", "translate(" + x.toFixed(1) + " " + y.toFixed(1) + ") rotate(" + ang.toFixed(1) + ")");
    shipLbl.setAttribute("x", x.toFixed(1)); shipLbl.setAttribute("y", (y - 14).toFixed(1));
    var len = chosen.getTotalLength ? chosen.getTotalLength() : 0;
    if (len) { done.setAttribute("d", chosen.getAttribute("d")); done.style.strokeDasharray = len; done.style.strokeDashoffset = len * (1 - t); }
  }
  var last = 0;
  function tick(ts) {
    if (!state.playing) return;
    var dt = last ? Math.min(0.05, (ts - last) / 1000) : 0; last = ts;
    state.t = (state.t + dt * 0.12 * (pick.v / 15)) % 1;
    placeShip(state.t);
    state.raf = requestAnimationFrame(tick);
  }
  function setPlaying(p) {
    state.playing = p; playBtn.textContent = p ? "Pause ❚❚" : "Play ▶";
    playBtn.setAttribute("aria-pressed", p ? "true" : "false");
    cancelAnimationFrame(state.raf); last = 0;
    if (p) state.raf = requestAnimationFrame(tick); else placeShip(state.t || 0.5);
  }
  tabs.addEventListener("click", function (ev) { var b = ev.target.closest(".lab-tab"); if (b) { state.s = +b.dataset.s; render(); } });
  prefs.addEventListener("click", function (ev) { var b = ev.target.closest(".lab-pref"); if (b) { state.pref = b.dataset.pref; render(); } });
  range.addEventListener("input", function () { state.s = range.value / 100; render(); });
  playBtn.addEventListener("click", function () { setPlaying(!state.playing); });
  render(); setPlaying(state.playing);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { es.forEach(function (en) { if (!en.isIntersecting && state.playing) { cancelAnimationFrame(state.raf); last = 0; } else if (en.isIntersecting && state.playing) { state.raf = requestAnimationFrame(tick); } }); }).observe(host);
  }
})();
