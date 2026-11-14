/* Linear redundancy check — booleanfunction.github.io
 * Builds the AES S-box from its definition (inversion in GF(2^8) + affine map), computes
 * all 255 component functions b_alpha, and verifies the thesis mapping b1(x) = b0(D01 x).
 * Compares with a random bijective S-box. No dependencies.
 */
(function (root) {
  "use strict";
  function gmul(a, b) {
    let r = 0;
    while (b) { if (b & 1) r ^= a; a <<= 1; if (a & 0x100) a ^= 0x11b; b >>= 1; }
    return r;
  }
  function aesSbox() {
    const inv = new Array(256).fill(0);
    for (let x = 1; x < 256; x++) for (let y = 1; y < 256; y++) if (gmul(x, y) === 1) { inv[x] = y; break; }
    return inv.map((b) => {
      let s = 0;
      for (let i = 0; i < 8; i++) {
        const bit = ((b >> i) ^ (b >> ((i + 4) % 8)) ^ (b >> ((i + 5) % 8)) ^ (b >> ((i + 6) % 8)) ^ (b >> ((i + 7) % 8)) ^ (0x63 >> i)) & 1;
        s |= bit << i;
      }
      return s;
    });
  }
  function randomSbox() {
    const s = Array.from({ length: 256 }, (_, i) => i);
    for (let i = 255; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [s[i], s[j]] = [s[j], s[i]]; }
    return s;
  }
  const parity = (v) => { v ^= v >> 4; v ^= v >> 2; v ^= v >> 1; return v & 1; };
  const component = (S, a) => S.map((y) => parity(y & a));
  function fwht(v) {
    const w = v.slice(), N = w.length;
    for (let h = 1; h < N; h *= 2)
      for (let i = 0; i < N; i += 2 * h)
        for (let j = i; j < i + h; j++) { const a = w[j], b = w[j + h]; w[j] = a + b; w[j + h] = a - b; }
    return w;
  }
  function profile(bits) {
    const F = fwht(bits.map((b) => 1 - 2 * b));
    const R = fwht(F.map((v) => v * v)).map((v) => v / 256);
    const A = bits.slice();
    for (let h = 1; h < 256; h *= 2)
      for (let i = 0; i < 256; i += 2 * h)
        for (let j = i; j < i + h; j++) A[j + h] ^= A[j];
    let deg = 0;
    A.forEach((c, m) => { if (c) { let k = 0, t = m; while (t) { k += t & 1; t >>= 1; } deg = Math.max(deg, k); } });
    const dist = (arr) => { const m = new Map(); arr.forEach((v) => { const a = Math.abs(v); m.set(a, (m.get(a) || 0) + 1); }); return [...m].sort((p, q) => p[0] - q[0]); };
    const wd = dist(F), ad = dist(R);
    return {
      nl: (256 - Math.max(...F.map(Math.abs))) / 2, deg, acmax: Math.max(...R.slice(1).map(Math.abs)),
      key: JSON.stringify([wd, ad]), whtStr: "{" + wd.map(([v, c]) => `(${v},${c})`).join(",") + "}",
      acStr: "{" + ad.map(([v, c]) => `(${v},${c})`).join(",") + "}",
    };
  }
  function analyseSbox(S) {
    const keys = new Map();
    let nlMin = 256, nlMax = 0;
    for (let a = 1; a < 256; a++) {
      const p = profile(component(S, a));
      keys.set(p.key, (keys.get(p.key) || 0) + 1);
      nlMin = Math.min(nlMin, p.nl); nlMax = Math.max(nlMax, p.nl);
    }
    return { distinct: keys.size, nlMin, nlMax };
  }
  // Thesis D01 (x = (x1..x8)^T with x8 the least significant bit): b1(x) = b0(D01 x)
  const D01 = [[1,0,1,1,0,0,1,0],[0,1,0,1,0,1,1,0],[0,0,0,1,0,0,1,0],[1,0,0,1,1,0,0,0],
               [0,1,0,1,1,1,0,0],[1,0,0,0,1,1,1,0],[1,1,0,1,0,0,0,0],[1,0,0,0,1,1,0,1]];
  function applyD(D, x) {
    const v = []; for (let k = 0; k < 8; k++) v.push((x >> (7 - k)) & 1);
    let y = 0;
    for (let r = 0; r < 8; r++) { let s = 0; for (let c = 0; c < 8; c++) s ^= D[r][c] & v[c]; y |= s << (7 - r); }
    return y;
  }
  function checkD01(S) {
    const b0 = component(S, 1), b1 = component(S, 2);
    let agree = 0; for (let x = 0; x < 256; x++) if (b1[x] === b0[applyD(D01, x)]) agree++;
    return agree;
  }
  root.AESR = { aesSbox, randomSbox, analyseSbox, checkD01, profile, component };

  if (typeof document === "undefined" || !document.getElementById("aes-run")) return;
  const $ = (id) => document.getElementById(id);
  $("aes-run").addEventListener("click", () => {
    const S = aesSbox();
    const rows = [];
    for (let i = 0; i < 8; i++) {
      const p = profile(component(S, 1 << i));
      rows.push(`<tr><td>b<sub>${i}</sub></td><td class="num">${p.nl}</td><td class="num">${p.deg}</td><td class="num">${p.acmax}</td><td><code>${p.whtStr}</code></td></tr>`);
    }
    const all = analyseSbox(S), agree = checkD01(S);
    $("aes-out").innerHTML = `
      <p>✓ S-box built from its definition: <code>S(0x00) = 0x${S[0].toString(16)}</code>,
      <code>S(0x53) = 0x${S[0x53].toString(16)}</code>, as in the AES standard.</p>
      <div class="table-scroll"><table><thead><tr><th>output bit</th><th class="num">nl</th><th class="num">degree</th><th class="num">acmax</th><th>|WHT| distribution</th></tr></thead><tbody>${rows.join("")}</tbody></table></div>
      <p>✓ All <strong>255</strong> component functions b<sub>α</sub> share
      <strong>${all.distinct === 1 ? "one identical" : all.distinct + " different"}</strong>
      |WHT| and |AC| distribution${all.distinct === 1 ? "" : "s"} (nonlinearity ${all.nlMin}${all.nlMax !== all.nlMin ? "–" + all.nlMax : ""}).</p>
      <p>${agree === 256 ? "✓" : "✗"} The thesis mapping <strong>b<sub>1</sub>(x) = b<sub>0</sub>(D<sub>01</sub>x)</strong>
      holds for <strong>${agree} of 256</strong> inputs: output bit 1 of AES is output bit 0 with its
      inputs linearly transformed.</p>`;
  });
  $("aes-random").addEventListener("click", () => {
    const r = analyseSbox(randomSbox());
    $("aes-rand-out").innerHTML = `<p>A random bijective 8 × 8 S-box: its 255 component functions have
      <strong>${r.distinct}</strong> different |WHT|/|AC| distributions (nonlinearity ${r.nlMin}–${r.nlMax}).
      ${r.distinct === 255 ? "Every pair differs, so no two of them can be affine equivalent: no linear redundancy at all." :
        "Functions with different distributions cannot be affine equivalent, so at most a handful of pairs could be."}</p>`;
  });
})(typeof window !== "undefined" ? window : this);
