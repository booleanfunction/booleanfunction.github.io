/* Function Analyser — booleanfunction.org
 * Paste a truth table; get its cryptographic properties and (for n <= 6) its class.
 * Everything is computed in the browser from the definitions. No dependencies.
 *
 * Truth-table conventions (as used throughout this site):
 *   - single hex value (n <= 5):        bit i of the value is f(i)
 *   - comma-separated 32-bit words:     word w, bit k is f(32w + k)  (as in the n = 6 data files)
 *   - binary string of 0/1:             character i is f(i)
 */
(function (root) {
  "use strict";

  // ── parsing ──────────────────────────────────────────────────────────────
  function parse(text) {
    const s = text.trim().replace(/^tt=/i, "").replace(/;$/, "").trim();
    if (!s) throw new Error("Enter a truth table.");
    let bits;
    if (/^[01\s]+$/.test(s) && s.replace(/\s/g, "").length >= 4 && !/^0x/i.test(s)) {
      bits = s.replace(/\s/g, "").split("").map(Number);
    } else if (s.includes(",")) {
      const words = s.split(",").map((w) => w.trim()).filter(Boolean);
      bits = [];
      for (const w of words) {
        if (!/^(0x)?[0-9a-f]{1,8}$/i.test(w)) throw new Error(`"${w}" is not a 32-bit hex word.`);
        const v = parseInt(w.replace(/^0x/i, ""), 16);
        for (let k = 0; k < 32; k++) bits.push((v >>> k) & 1);
      }
    } else {
      const h = s.replace(/^0x/i, "");
      if (!/^[0-9a-f]+$/i.test(h)) throw new Error("Use hex (e.g. 0xe8), 32-bit words separated by commas, or a 0/1 string.");
      if (h.length > 8) throw new Error("For more than 32 bits, give comma-separated 32-bit words (word 0 first).");
      const v = parseInt(h, 16), len = Math.max(4, h.length * 4);
      // smallest power of two >= number of hex bits
      let N = 4; while (N < len) N *= 2;
      bits = []; for (let k = 0; k < N; k++) bits.push(Math.floor(v / 2 ** k) % 2);
    }
    const N = bits.length, n = Math.log2(N);
    if (!Number.isInteger(n) || n < 2) throw new Error(`Truth table has ${N} bits; it must be a power of two (at least 4).`);
    if (n > 10) throw new Error("This tool handles up to n = 10 (1,024 bits).");
    return bits;
  }

  // ── transforms ───────────────────────────────────────────────────────────
  function wht(bits) {
    const w = bits.map((b) => 1 - 2 * b), N = w.length;
    for (let h = 1; h < N; h *= 2)
      for (let i = 0; i < N; i += 2 * h)
        for (let j = i; j < i + h; j++) { const a = w[j], b = w[j + h]; w[j] = a + b; w[j + h] = a - b; }
    return w;
  }
  function anf(bits) {
    const a = bits.slice(), N = a.length;
    for (let h = 1; h < N; h *= 2)
      for (let i = 0; i < N; i += 2 * h)
        for (let j = i; j < i + h; j++) a[j + h] ^= a[j];
    return a;
  }
  function autocorr(bits) {
    // r(s) = WHT^{-1}( F(w)^2 ): compute via squared spectrum for speed
    const F = wht(bits), N = F.length, r = F.map((v) => v * v);
    for (let h = 1; h < N; h *= 2)
      for (let i = 0; i < N; i += 2 * h)
        for (let j = i; j < i + h; j++) { const a = r[j], b = r[j + h]; r[j] = a + b; r[j + h] = a - b; }
    return r.map((v) => v / N);
  }
  const popcount = (v) => { let c = 0; while (v) { c += v & 1; v >>>= 1; } return c; };
  function dist(arr) {
    const m = new Map();
    arr.forEach((v) => { const a = Math.abs(v); m.set(a, (m.get(a) || 0) + 1); });
    return [...m.entries()].sort((x, y) => x[0] - y[0]);
  }
  const distStr = (d) => "{" + d.map(([v, c]) => `(${v},${c})`).join(",") + "}";

  // ── algebraic immunity (Gaussian elimination over GF(2)) ─────────────────
  function hasAnnihilator(points, n, d) {
    const monos = [];
    for (let m = 0; m < 1 << n; m++) if (popcount(m) <= d) monos.push(m);
    const C = monos.length, W = Math.ceil(C / 32);
    if (points.length < C) return true; // more unknowns than equations: nonzero solution exists
    const rows = points.map((x) => {
      const r = new Uint32Array(W);
      monos.forEach((m, c) => { if ((m & x) === m) r[c >> 5] |= 1 << (c & 31); });
      return r;
    });
    let rank = 0;
    for (let c = 0; c < C && rank < rows.length; c++) {
      const wd = c >> 5, bit = 1 << (c & 31);
      let p = rank; while (p < rows.length && !(rows[p][wd] & bit)) p++;
      if (p === rows.length) continue;
      [rows[rank], rows[p]] = [rows[p], rows[rank]];
      for (let r = 0; r < rows.length; r++)
        if (r !== rank && rows[r][wd] & bit) for (let k = 0; k < W; k++) rows[r][k] ^= rows[rank][k];
      rank++;
    }
    return rank < C;
  }
  function algebraicImmunity(bits, n) {
    const ones = [], zeros = [];
    bits.forEach((b, x) => (b ? ones : zeros).push(x));
    if (!ones.length || !zeros.length) return 0;
    for (let d = 1; d <= n; d++)
      if (hasAnnihilator(ones, n, d) || hasAnnihilator(zeros, n, d)) return d;
    return n;
  }

  // ── the analysis ─────────────────────────────────────────────────────────
  function analyse(bits) {
    const N = bits.length, n = Math.log2(N);
    const F = wht(bits), A = anf(bits), R = autocorr(bits);
    const weight = bits.reduce((a, b) => a + b, 0);
    const maxW = Math.max(...F.map(Math.abs));
    const terms = [];
    for (let m = 0; m < N; m++) if (A[m]) terms.push(m);
    const degree = terms.length ? Math.max(...terms.map(popcount)) : 0;
    // correlation immunity: largest t with F(w) = 0 for all 1 <= wt(w) <= t
    let ci = 0;
    for (let t = 1; t <= n; t++) {
      let ok = true;
      for (let w = 1; w < N && ok; w++) if (popcount(w) <= t && popcount(w) >= 1 && F[w] !== 0) ok = false;
      if (ok) ci = t; else break;
    }
    // propagation criterion: largest k with r(s) = 0 for all 1 <= wt(s) <= k
    let pc = 0;
    for (let k = 1; k <= n; k++) {
      let ok = true;
      for (let s = 1; s < N && ok; s++) if (popcount(s) <= k && R[s] !== 0) ok = false;
      if (ok) pc = k; else break;
    }
    const acmax = Math.max(...R.slice(1).map(Math.abs));
    const nl = (N - maxW) / 2;
    const bentNL = n % 2 === 0 ? 2 ** (n - 1) - 2 ** (n / 2 - 1) : null;
    return {
      n, N, weight, balanced: weight === N / 2, degree,
      anfTerms: terms, nl, maxW, bent: bentNL !== null && nl === bentNL,
      whtDist: dist(F), acDist: dist(R), acmax, ci, resilient: weight === N / 2 ? ci : null, pc,
      linearStructures: R.slice(1).filter((v) => Math.abs(v) === N).length,
      ai: N <= 1024 ? algebraicImmunity(bits, n) : null,
      key: dist(F).map(([v, c]) => Array(c).fill(v)).flat().join(",") + "|" +
           dist(R).map(([v, c]) => Array(c).fill(v)).flat().join(","),
    };
  }
  function anfString(terms, n) {
    if (!terms.length) return "0";
    return terms.map((m) => {
      if (m === 0) return "1";
      let s = "";
      for (let k = 0; k < n; k++) if ((m >> k) & 1) s += `x<sub>${k + 1}</sub>`;
      return s;
    }).join(" ⊕ ");
  }

  root.BFA = { parse, analyse, anfString, distStr, wht, algebraicImmunity };

  // ── UI (only when running in a page) ─────────────────────────────────────
  if (typeof document === "undefined" || !document.getElementById("fa-input")) return;
  const $ = (id) => document.getElementById(id);
  const DATA = JSON.parse($("fa-data").textContent);
  const fmt = (x) => x.toLocaleString("en-AU");
  function run() {
    const out = $("fa-out");
    let bits;
    try { bits = parse($("fa-input").value); }
    catch (e) { out.innerHTML = `<p class="fa-error">${e.message}</p>`; return; }
    const r = analyse(bits), n = r.n;
    let cls = "";
    if (n <= 5) {
      const c = DATA.keys[n][r.key];
      const p = DATA.classes[n][c];
      cls = `<dt>affine class</dt><dd><strong>class ${c}</strong> of ${DATA.count[n]} for n = ${n}
        (representative <code>${p.hex}</code>, ${fmt(p.size)} functions).
        <a href="explore.html">See it in the Class Graph Explorer</a> or the
        <a href="equivalence-classes.html">class tables</a>.</dd>`;
    } else if (n === 6) {
      const b = DATA.n6[`${r.nl},${r.degree},${r.acmax}`];
      cls = `<dt>affine class</dt><dd>in data file <code>n6_nl${r.nl}_ord${r.degree}_acmax${r.acmax}.exp</code>,
        which holds ${b ? fmt(b) : "?"} of the 150,357 classes
        (<a href="equivalence-classes.html#cite">download the data</a>).</dd>`;
    }
    const anfTxt = r.anfTerms.length <= 40 ? anfString(r.anfTerms, n)
      : `${fmt(r.anfTerms.length)} terms (too many to show)`;
    const maxNLnote = r.bent ? " — <strong>bent</strong> (maximum possible)" : "";
    out.innerHTML = `
      <dl class="fa-props">
        <dt>inputs</dt><dd>n = ${n} (${r.N} truth-table bits)</dd>
        <dt>Hamming weight</dt><dd>${r.weight} ${r.balanced ? "— <strong>balanced</strong>" : "(not balanced)"}</dd>
        <dt>algebraic degree</dt><dd>${r.degree}</dd>
        <dt>ANF</dt><dd class="fa-anf">${anfTxt}</dd>
        <dt>nonlinearity</dt><dd><strong>${r.nl}</strong>${maxNLnote} <span class="fa-muted">(max |F̂| = ${r.maxW})</span></dd>
        <dt>algebraic immunity</dt><dd>${r.ai} <span class="fa-muted">(optimum for n = ${n} is ${Math.ceil(n / 2)})</span></dd>
        <dt>correlation immunity</dt><dd>order ${r.ci}${r.balanced && r.ci ? ` (${r.ci}-resilient)` : ""}</dd>
        <dt>propagation criterion</dt><dd>PC(${r.pc})</dd>
        <dt>absolute indicator</dt><dd>${r.acmax}${r.linearStructures ? ` <span class="fa-muted">(${r.linearStructures} linear structure${r.linearStructures > 1 ? "s" : ""})</span>` : ""}</dd>
        ${cls}
        <dt>|WHT| distribution</dt><dd><code>${distStr(r.whtDist)}</code></dd>
        <dt>|AC| distribution</dt><dd><code>${distStr(r.acDist)}</code></dd>
      </dl>`;
  }
  $("fa-go").addEventListener("click", run);
  $("fa-input").addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); run(); } });
  document.querySelectorAll("[data-example]").forEach((b) => b.addEventListener("click", () => {
    let v = b.dataset.example;
    if (v === "random") {
      const n = 6, words = [];
      for (let w = 0; w < 2 ** n / 32; w++) words.push("0x" + Math.floor(Math.random() * 2 ** 32).toString(16).toUpperCase().padStart(8, "0"));
      v = words.join(",");
    }
    $("fa-input").value = v; run();
  }));
  // deep link: analyse.html?tt=<truth table>
  try {
    const q = new URLSearchParams(location.search).get("tt");
    if (q) $("fa-input").value = q;
  } catch (e) { /* ignore */ }
  run();
})(typeof window !== "undefined" ? window : this);
