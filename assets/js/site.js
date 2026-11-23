// Progressive enhancement only: every page is fully readable without JavaScript.
(function () {
  "use strict";
  var root = document.documentElement;

  // Theme toggle (remembers the choice; otherwise follows the OS setting)
  var tbtn = document.querySelector(".theme-toggle");
  if (tbtn) {
    tbtn.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme") ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = cur === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // Mobile navigation
  var nbtn = document.querySelector(".nav-toggle");
  var list = document.getElementById("nav-list");
  if (nbtn && list) {
    nbtn.addEventListener("click", function () {
      var open = list.classList.toggle("open");
      nbtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && list.classList.contains("open")) {
        list.classList.remove("open"); nbtn.setAttribute("aria-expanded", "false"); nbtn.focus();
      }
    });
  }

  // Chart tooltips (mouse and keyboard focus)
  var tip = document.createElement("div");
  tip.className = "tooltip"; tip.setAttribute("role", "status");
  document.body.appendChild(tip);
  function show(el, x, y) {
    tip.textContent = el.getAttribute("data-tip");
    tip.classList.add("show");
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var left = Math.min(Math.max(8, x - w / 2), window.innerWidth - w - 8);
    tip.style.left = left + "px"; tip.style.top = Math.max(8, y - h - 12) + "px";
  }
  function hide() { tip.classList.remove("show"); }
  document.querySelectorAll("[data-tip]").forEach(function (el) {
    el.addEventListener("mousemove", function (ev) { show(el, ev.clientX, ev.clientY); });
    el.addEventListener("mouseleave", hide);
    el.addEventListener("focus", function () { var r = el.getBoundingClientRect(); show(el, r.left + r.width / 2, r.top); });
    el.addEventListener("blur", hide);
  });

  // Publication filters
  var listEl = document.getElementById("pub-list");
  if (!listEl) return;
  var q = document.getElementById("pub-q"), yr = document.getElementById("pub-year"),
      role = document.getElementById("pub-role"), count = document.getElementById("pub-count");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip[data-topic]"));
  var cards = Array.prototype.slice.call(listEl.querySelectorAll(".pub"));
  var groups = Array.prototype.slice.call(listEl.querySelectorAll(".year-group"));
  var params = new URLSearchParams(location.search);
  if (params.get("year")) yr.value = params.get("year");
  if (params.get("topic")) chips.forEach(function (c) { if (c.dataset.topic === params.get("topic")) c.setAttribute("aria-pressed", "true"); });

  function apply() {
    var text = q.value.trim().toLowerCase(), y = yr.value, r = role.value;
    var topics = chips.filter(function (c) { return c.getAttribute("aria-pressed") === "true"; }).map(function (c) { return c.dataset.topic; });
    var n = 0;
    cards.forEach(function (c) {
      var ok = (!y || c.dataset.year === y) && (!r || c.dataset.role === r) &&
        (!topics.length || topics.indexOf(c.dataset.topic) >= 0) &&
        (!text || c.textContent.toLowerCase().indexOf(text) >= 0);
      c.hidden = !ok; if (ok) n++;
    });
    groups.forEach(function (g) { g.hidden = !g.querySelector(".pub:not([hidden])"); });
    count.textContent = "Showing " + n + " of " + cards.length + " published papers";
  }
  q.addEventListener("input", apply); yr.addEventListener("change", apply); role.addEventListener("change", apply);
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      c.setAttribute("aria-pressed", c.getAttribute("aria-pressed") === "true" ? "false" : "true"); apply();
    });
  });
  apply();
})();
// Sidebar details start closed on small screens
(function () {
  var d = document.querySelector(".side-more");
  if (d && window.matchMedia("(max-width: 860px)").matches) d.removeAttribute("open");
})();
// S175 race: simulator vs surrogate evaluations in 10 s of real time (timings from the public repository)
(function () {
  var box = document.getElementById("s175-race");
  if (!box) return;
  var sim = +box.dataset.sim, sur = +box.dataset.sur, go = document.getElementById("race-go"), raf = 0;
  var eSim = document.getElementById("race-sim"), eSur = document.getElementById("race-sur");
  var bSim = document.getElementById("race-sim-bar"), bSur = document.getElementById("race-sur-bar");
  var maxSur = Math.floor(10 / sur);
  function draw(t) {
    var nSim = Math.floor(t / sim), nSur = Math.floor(t / sur);
    eSim.textContent = (t / sim).toFixed(2);
    eSur.textContent = nSur.toLocaleString("en-GB");
    bSim.style.width = Math.max(1, nSim / maxSur * 100) + "%";
    bSur.style.width = Math.min(100, nSur / maxSur * 100) + "%";
  }
  function run() {
    cancelAnimationFrame(raf); var t0 = performance.now(); go.disabled = true;
    (function step(now) {
      var t = Math.min(10, (now - t0) / 1000); draw(t);
      if (t < 10) raf = requestAnimationFrame(step); else { go.disabled = false; go.textContent = "Run again ▶"; }
    })(t0);
  }
  go.addEventListener("click", run);
  draw(0);
})();
