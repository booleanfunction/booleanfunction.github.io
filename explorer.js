/* Class Graph Explorer — booleanfunction.github.io
 * Interactive affine-equivalence class connection graphs for n = 3, 4, 5.
 * Data (computed exactly by build.py) is embedded in #graph-data. No dependencies.
 */
(function () {
  "use strict";
  const DATA = JSON.parse(document.getElementById("graph-data").textContent);
  const SVGNS = "http://www.w3.org/2000/svg";
  const $ = (id) => document.getElementById(id);

  const svg = $("gx-svg"), info = $("gx-info"), legend = $("gx-legend"), log = $("gx-log");
  let G = null, current = 5, colourMode = "deg", pinned = null, timer = null;
  const nodeEl = {}, linkEl = [];

  // ── colour scales (colour-blind-friendly) ──────────────────────────────────
  const DEG = ["#9aa3ad", "#8c6bb1", "#2b8cbe", "#41ab5d", "#fd8d3c", "#e7298a"];
  const ACSEQ = ["#0a5b66", "#0f7b8a", "#3aa7b4", "#86cdd5", "#c9e6ea", "#eef0f3"];
  function colour(n) {
    if (colourMode === "deg") return DEG[Math.min(n.deg, DEG.length - 1)];
    if (colourMode === "bal") return n.bal ? "#0f7b8a" : "#d5d9de";
    const vals = [...new Set(G.nodes.map((m) => m.acmax))].sort((a, b) => a - b);
    const t = vals.length > 1 ? vals.indexOf(n.acmax) / (vals.length - 1) : 0;
    return ACSEQ[Math.round(t * (ACSEQ.length - 1))];
  }
  function drawLegend() {
    let items = [];
    if (colourMode === "deg") {
      const ds = [...new Set(G.nodes.map((m) => m.deg))].sort((a, b) => a - b);
      items = ds.map((d) => [DEG[Math.min(d, DEG.length - 1)], "degree " + d]);
    } else if (colourMode === "bal") {
      items = [["#0f7b8a", "contains balanced functions"], ["#d5d9de", "no balanced functions"]];
    } else {
      const vals = [...new Set(G.nodes.map((m) => m.acmax))].sort((a, b) => a - b);
      items = vals.map((v, i) => [ACSEQ[Math.round((vals.length > 1 ? i / (vals.length - 1) : 0) * (ACSEQ.length - 1))], "acmax " + v]);
    }
    legend.innerHTML = items.map(([c, t]) => `<span><i style="background:${c}"></i>${t}</span>`).join("") +
      '<span class="gx-size-key">circle area ∝ log(class size)</span>';
  }

  // ── layout & drawing ───────────────────────────────────────────────────────
  const W = 1000, PADX = 70, PADY = 40;
  function el(tag, attrs, parent) {
    const e = document.createElementNS(SVGNS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function draw() {
    G = DATA[current];
    svg.innerHTML = "";
    for (const k in nodeEl) delete nodeEl[k];
    linkEl.length = 0;
    const H = Math.max(260, (G.levels.length - 1) * 62 + 2 * PADY);
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const sizes = G.nodes.map((n) => Math.log(n.size));
    const lo = Math.min(...sizes), hi = Math.max(...sizes);
    const R = (n) => 6 + 13 * (hi > lo ? (Math.log(n.size) - lo) / (hi - lo) : 0.5);
    const P = {};
    G.nodes.forEach((n) => { P[n.id] = [PADX + n.x * (W - 2 * PADX), H - PADY - n.y * (H - 2 * PADY)]; });
    // nonlinearity axis
    const ax = el("g", { class: "gx-axis" }, svg);
    G.levels.forEach((L, i) => {
      const y = H - PADY - (G.levels.length > 1 ? i / (G.levels.length - 1) : 0) * (H - 2 * PADY);
      el("line", { x1: 40, x2: W - 10, y1: y, y2: y }, ax);
      el("text", { x: 4, y: y + 4 }, ax).textContent = "NL " + L;
    });
    const gl = el("g", { class: "gx-links" }, svg);
    G.links.forEach(([a, b]) => {
      const l = el("line", { x1: P[a][0], y1: P[a][1], x2: P[b][0], y2: P[b][1] }, gl);
      linkEl.push({ a, b, el: l });
    });
    const gn = el("g", { class: "gx-nodes" }, svg);
    G.nodes.forEach((n) => {
      const g = el("g", { class: "gx-node", tabindex: 0, role: "button",
        "aria-label": `Class ${n.id}, nonlinearity ${n.nl}, degree ${n.deg}` }, gn);
      el("circle", { cx: P[n.id][0], cy: P[n.id][1], r: R(n), fill: colour(n) }, g);
      const t = el("text", { x: P[n.id][0], y: P[n.id][1] - R(n) - 4 }, g);
      t.textContent = n.id;
      g.addEventListener("mouseenter", () => setFocus(n.id));
      g.addEventListener("mouseleave", () => setFocus(pinned));
      g.addEventListener("click", () => { pinned = pinned === n.id ? null : n.id; setFocus(pinned ?? n.id); });
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pinned = n.id; setFocus(n.id); } });
      nodeEl[n.id] = g;
    });
    drawLegend();
    setFocus(null);
  }
  function recolour() {
    G.nodes.forEach((n) => nodeEl[n.id].querySelector("circle").setAttribute("fill", colour(n)));
    drawLegend();
  }

  // ── focus / info panel ─────────────────────────────────────────────────────
  const byId = (id) => G.nodes.find((n) => n.id === id);
  const fmt = (x) => x.toLocaleString("en-AU");
  function setFocus(id) {
    const nb = new Set();
    if (id != null) byId(id).flips.forEach(([k]) => nb.add(k));
    svg.classList.toggle("gx-has-focus", id != null);
    for (const k in nodeEl) {
      const c = +k;
      nodeEl[k].classList.toggle("is-focus", c === id);
      nodeEl[k].classList.toggle("is-nb", nb.has(c) && c !== id);
    }
    linkEl.forEach((l) => l.el.classList.toggle("is-on", id != null && (l.a === id || l.b === id)));
    renderInfo(id);
  }
  function renderInfo(id) {
    if (id == null) {
      info.innerHTML = `<h3>n = ${G.n}</h3>
        <p><strong>${G.nodes.length}</strong> classes, <strong>${G.links.length}</strong> connections,
        <strong>${fmt(G.total)}</strong> functions in all.</p>
        <p class="gx-hint">Hover over or tap a class to see its properties and where single-bit changes lead.
        Click to pin it.</p>`;
      return;
    }
    const n = byId(id), N = 1 << G.n, share = (100 * n.size / G.total);
    const rows = n.flips.map(([k, v]) => {
      const m = byId(k);
      const dir = m.nl > n.nl ? "▲" : m.nl < n.nl ? "▼" : "▶";
      return `<li><button type="button" data-goto="${k}">class ${k}</button>
        <span class="gx-bar"><i style="width:${(100 * v / N).toFixed(1)}%"></i></span>
        ${v} of ${N} <span class="gx-dir" title="nonlinearity ${m.nl}">${dir} NL ${m.nl}</span></li>`;
    }).join("");
    info.innerHTML = `<h3>Class ${n.id}</h3>
      <dl>
        <dt>example</dt><dd><code>${n.hex}</code></dd>
        <dt>nonlinearity</dt><dd>${n.nl}</dd>
        <dt>degree</dt><dd>${n.deg}</dd>
        <dt>acmax</dt><dd>${n.acmax}</dd>
        <dt>balanced?</dt><dd>${n.bal ? "contains balanced functions" : "no balanced functions"}</dd>
        <dt>functions</dt><dd>${fmt(n.size)} <span class="gx-muted">(${share < 0.01 ? share.toExponential(1) : share.toFixed(2)}% of all)</span></dd>
        <dt>self maps θ</dt><dd>${fmt(n.theta)}</dd>
        <dt>|WHT| dist.</dt><dd><code>${n.wht}</code></dd>
        <dt>|AC| dist.</dt><dd><code>${n.ac}</code></dd>
      </dl>
      <h4>Changing one bit of any function in this class leads to:</h4>
      <ul class="gx-flips">${rows}</ul>`;
    info.querySelectorAll("[data-goto]").forEach((b) =>
      b.addEventListener("click", () => { pinned = +b.dataset.goto; setFocus(pinned); }));
  }

  // ── hill climb (steepest ascent on nonlinearity) ───────────────────────────
  function wht(bits) {
    const w = bits.map((b) => 1 - 2 * b), N = w.length;
    for (let h = 1; h < N; h *= 2)
      for (let i = 0; i < N; i += 2 * h)
        for (let j = i; j < i + h; j++) { const a = w[j], b = w[j + h]; w[j] = a + b; w[j + h] = a - b; }
    return w;
  }
  const popcount = (v) => { let c = 0; while (v) { c += v & 1; v >>>= 1; } return c; };
  const nlOf = (bits) => (bits.length - Math.max(...wht(bits).map(Math.abs))) / 2;
  function classOf(bits) {
    const N = bits.length, ac = [];
    for (let s = 0; s < N; s++) { let t = 0; for (let x = 0; x < N; x++) t += bits[x] ^ bits[x ^ s] ? -1 : 1; ac.push(Math.abs(t)); }
    const key = wht(bits).map(Math.abs).sort((a, b) => a - b).join(",") + "|" + ac.sort((a, b) => a - b).join(",");
    return G.keys[key];
  }
  const hex = (bits) => "0x" + bits.reduce((v, b, i) => v + b * 2 ** i, 0).toString(16).padStart(bits.length / 4 || 1, "0");
  function climb() {
    stop();
    const N = 1 << G.n;
    let bits;
    if ($("gx-start").value === "affine") {
      // random affine function w.x + c (nonzero w, so it's a genuine linear part)
      const w = 1 + Math.floor(Math.random() * (N - 1)), c = Math.random() < 0.5 ? 1 : 0;
      bits = Array.from({ length: N }, (_, x) => (popcount(w & x) & 1) ^ c);
    } else {
      bits = Array.from({ length: N }, () => (Math.random() < 0.5 ? 1 : 0));
    }
    const path = [{ bits: bits.slice(), cls: classOf(bits), nl: nlOf(bits), bit: null }];
    for (;;) {
      const cur = nlOf(bits);
      let best = -1, cands = [];
      for (let i = 0; i < N; i++) {
        bits[i] ^= 1; const v = nlOf(bits); bits[i] ^= 1;
        if (v > best) { best = v; cands = [i]; } else if (v === best) cands.push(i);
      }
      if (best <= cur) break;
      const i = cands[Math.floor(Math.random() * cands.length)];
      bits[i] ^= 1;
      path.push({ bits: bits.slice(), cls: classOf(bits), nl: best, bit: i });
    }
    const maxNL = Math.max(...G.levels);
    pinned = null; setFocus(null);
    svg.classList.add("gx-climbing");
    log.innerHTML = "";
    let k = 0;
    const visited = new Set();
    const tick = () => {
      const s = path[k];
      visited.add(s.cls);
      for (const c in nodeEl) nodeEl[c].classList.toggle("is-visited", visited.has(+c));
      for (const c in nodeEl) nodeEl[c].classList.toggle("is-here", +c === s.cls);
      if (k > 0) {
        const a = path[k - 1].cls, b = s.cls;
        linkEl.forEach((l) => { if ((l.a === a && l.b === b) || (l.a === b && l.b === a)) l.el.classList.add("is-path"); });
      }
      const li = document.createElement("li");
      li.innerHTML = k === 0
        ? `start: ${$("gx-start").value === "affine" ? "affine" : "random"} function <code>${hex(s.bits)}</code> → class ${s.cls}, NL ${s.nl}`
        : `flip bit ${s.bit} → class ${s.cls}, NL ${s.nl}`;
      log.appendChild(li);
      k++;
      if (k < path.length) timer = setTimeout(tick, 700);
      else {
        const end = document.createElement("li");
        end.className = "gx-end";
        end.textContent = s.nl === maxNL
          ? `Reached the top: NL ${s.nl} is the maximum for n = ${G.n}. Final function ${hex(s.bits)}.`
          : `Stuck at a local maximum (NL ${s.nl}): no single-bit change improves nonlinearity.`;
        log.appendChild(end);
        timer = null;
      }
    };
    tick();
  }
  function stop() {
    if (timer) clearTimeout(timer);
    timer = null;
    svg.classList.remove("gx-climbing");
    Object.values(nodeEl).forEach((g) => g.classList.remove("is-visited", "is-here"));
    linkEl.forEach((l) => l.el.classList.remove("is-path"));
  }

  // ── controls ───────────────────────────────────────────────────────────────
  document.querySelectorAll("[data-n]").forEach((b) => b.addEventListener("click", () => {
    stop(); log.innerHTML = ""; pinned = null; current = +b.dataset.n;
    document.querySelectorAll("[data-n]").forEach((x) => x.setAttribute("aria-pressed", x === b));
    draw();
  }));
  $("gx-colour").addEventListener("change", (e) => { colourMode = e.target.value; recolour(); });
  $("gx-climb").addEventListener("click", climb);
  $("gx-reset").addEventListener("click", () => { stop(); log.innerHTML = ""; pinned = null; setFocus(null); });
  draw();
})();
