# booleanfunction.github.io

The public website for **Boolean Functions for Cryptography** research — a modern home for
the original *Boolean Planet* site, served at [booleanfunction.github.io](https://booleanfunction.github.io/).

Plain static HTML — **no build framework or toolchain required**. GitHub Pages serves the
`.html` files directly. Maths and webfonts are loaded client-side from CDNs by the visitor's
browser (MathJax, Google Fonts); nothing is fetched or executed during the build.

## Scope

This repository is **public** and intentionally contains only already-published research
results and reference material:

- Affine equivalence class tables for n = 3, 4, 5, the n = 6 summary, and the original n = 6
  class representative data files (`data/`)
- The Theorem of Connectivity (from the PhD thesis)
- Efficient implementation techniques (word packing, WHT/ANF/AC transforms)
- S-box survey (equivalence classes and nonlinearity of cipher S-box coordinate functions)
- Publications, learning resources, curated resources and best-known records

The research **code**, the modern Rust library, other datasets, and unpublished new results
live in a **separate private repository** and are not part of this site.

## Previewing

Just open `index.html` in a browser — there is no build step to run first.

## Editing

Page content and the data tables live in `build.py` (Python standard library only, no
third-party packages). After editing, regenerate the HTML:

```sh
python3 build.py
```

This rewrites all the `.html` pages plus `404.html`, `sitemap.xml` and `robots.txt`. The shared navigation, header and footer are defined
once in `build.py`, so a change there propagates to every page. Styling is in `style.css`.

## Publishing

Published as the GitHub Pages user site of the `booleanfunction` account (this repository is
`booleanfunction.github.io`), served from the default branch root. No Actions workflow or build is
needed, since the committed `.html` is the site. A custom domain can be added later via a `CNAME`
file and the Pages settings.

## Structure

| File | Purpose |
|------|---------|
| `build.py` | Source of all page content + data tables; regenerates the HTML |
| `index.html` | Home |
| `basics.html` | Worked introduction (3-input majority function): ANF, Walsh, NL, AC, equivalence |
| `equivalence-classes.html` | Affine equivalence class tables (n = 3, 4, 5; n = 6 summary) |
| `explore.html` + `explorer.js` | Interactive class connection graphs (n = 3, 4, 5) with hill-climb animation; graph data computed exactly in `build.py` (`class_graph`), JS has no dependencies |
| `analyse.html` + `analyse.js` | Function Analyser: paste a truth table (n ≤ 10); NL, degree, ANF, WHT/AC, CI, PC, AI, class (n ≤ 5) / data file (n = 6). Deep link `analyse.html?tt=…` |
| `constructions.html` | Thesis Ch. 5: bent construction, Boolean terrain, dynamic hill climbing, history of heuristic search at QUT (tables extracted from the thesis source) |
| `class-sizes.html` | Self-mapping constant: class sizes (all 48 for n = 5), θ distribution and NL counts for n = 6 |
| `connectivity.html` | The Theorem of Connectivity, with n = 3, 4 connection diagrams |
| `efficient-implementation.html` | Implementation techniques |
| `sboxes.html` + `aes.js` | Linear redundancy (thesis Ch. 6 / FSE 2003) with in-browser AES check, and the S-box survey |
| `publications.html` | Publications |
| `learning.html` | Learning, plus the curated resources list (`#resources`) |
| `resources.html` | Redirect to `learning.html#resources` (pages merged 2026-11-14) |
| `records.html` | Best-known functions by criterion, and open problems |
| `data/` | n = 6 class representatives: `n6-classes.zip` (150,357), `n6-balanced-classes.zip` (74,542) |
| `404.html` | Not-found page (generated) |
| `sitemap.xml`, `robots.txt` | Search-engine indexing (generated from `NAV`) |
| `CNAME` | Custom domain for GitHub Pages |
| `LICENSE` | CC BY 4.0 for content and data |
| `CITATION.cff` | Citation metadata (GitHub "Cite this repository"); cite the 2003 PhD thesis |
| `style.css` | Theme (palette, type, layout) |
| `favicon.svg` | Site icon |

© Dr Joanne Fuller.
