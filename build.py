#!/usr/bin/env python3
"""Build the static booleanfunction.github.io site.

Stdlib only — no third-party packages, no install required. Run:

    python3 build.py

It writes index.html and one .html per page into this directory, sharing a
common nav/header/footer. Maths is rendered client-side by MathJax (loaded from
a CDN by the visitor's browser); fonts likewise. GitHub Pages serves the .html
files directly with no further build step.
"""

# Top-level menu: (href, label) for a single link, or (label, [(href, label), ...]) for a drop-down.
NAV = [
    ("index.html", "Home"),
    ("basics.html", "Basics"),
    ("Classes", [
        ("equivalence-classes.html", "Equivalence classes &amp; data"),
        ("class-sizes.html", "Class sizes"),
        ("connectivity.html", "Connectivity"),
    ]),
    ("Research", [
        ("constructions.html", "Constructions &amp; search"),
        ("sboxes.html", "S-boxes &amp; AES"),
        ("records.html", "Records &amp; open problems"),
        ("efficient-implementation.html", "Efficient implementation"),
    ]),
    ("Tools", [
        ("explore.html", "Class Graph Explorer"),
        ("analyse.html", "Function Analyser"),
    ]),
    ("publications.html", "Publications"),
    ("learning.html", "Learning"),
]
# Flat list of all pages in the menu (for the sitemap and build log).
PAGES = [h for item in NAV for h in ([item[0]] if isinstance(item[1], str) else [s for s, _ in item[1]])]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Joanne Fuller">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="favicon.svg">
<link rel="stylesheet" href="style.css">
<script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
{extra}</head>
<body>
"""

FOOTER = """<footer class="site-footer"><div class="foot-inner">
<span>© Dr Joanne Fuller · <a href="https://orcid.org/0000-0002-5221-3505" rel="me noopener">ORCID</a> · <a href="https://scholar.google.com/citations?user=aCp_g7IAAAAJ&amp;hl=en" rel="me noopener">Google Scholar</a> · <a href="https://www.linkedin.com/in/joanne-fuller-phd-04955b1a/" rel="me noopener">LinkedIn</a></span>
<span>Content and data licensed <a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener">CC BY 4.0</a>: please <a href="equivalence-classes.html#cite">cite</a> when reusing</span>
</div></footer>
</body>
</html>
"""


def nav(active):
    links = []
    for item in NAV:
        if isinstance(item[1], str):
            href, label = item
            cls = "navlink active" if href == active else "navlink"
            cur = ' aria-current="page"' if href == active else ""
            links.append(f'<a class="{cls}" href="{href}"{cur}>{label}</a>')
        else:
            label, subs = item
            on = any(h == active for h, _ in subs)
            cur_attr = ' aria-current="page"'
            items = "".join(
                f'<a href="{h}"{cur_attr if h == active else ""}>{l}</a>' for h, l in subs)
            links.append(f'<details class="navgroup"><summary class="navlink{" active" if on else ""}">'
                         f'{label}</summary><div class="navmenu">{items}</div></details>')
    return ('<header class="site-head">'
            '<a class="masthead-title" href="index.html">Boolean Functions for Cryptography</a>'
            '<nav class="masthead-nav" aria-label="Main">' + "".join(links) + "</nav>"
            "</header>\n"
            "<script>document.addEventListener('click',function(e){document.querySelectorAll("
            "'details.navgroup[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open');});});"
            "document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll("
            "'details.navgroup[open]').forEach(function(d){d.removeAttribute('open');});});"
            "document.addEventListener('toggle',function(e){var t=e.target;if(t.matches&&t.matches('details.navgroup')&&t.open)"
            "document.querySelectorAll('details.navgroup[open]').forEach(function(d){if(d!==t)d.removeAttribute('open');});},true);"
            "</script>\n")


SITE = "https://booleanfunction.github.io/"
ORCID = "https://orcid.org/0000-0002-5221-3505"

# schema.org Dataset description (Google Dataset Search). Add the Zenodo DOI as
# "identifier" once minted.
_DATASET = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "Affine equivalence classes of 6-variable Boolean functions",
    "description": (
        "Representative truth tables for all 150,357 affine equivalence classes of "
        "Boolean functions on six variables, grouped by nonlinearity, algebraic order and "
        "maximum absolute autocorrelation, with the 74,542 classes that contain balanced "
        "functions. Computed for the PhD thesis 'Analysis of Affine Equivalent Boolean "
        "Functions for Cryptography' (Queensland University of Technology, 2003) and "
        "published on the Boolean Planet website in 2003."),
    "url": SITE + "equivalence-classes.html",
    "identifier": "https://doi.org/10.5281/zenodo.24217283",
    "sameAs": "https://doi.org/10.5281/zenodo.24217283",
    "creator": {"@type": "Person", "name": "Joanne Fuller", "@id": ORCID,
                "sameAs": [ORCID]},
    "datePublished": "2003",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "isAccessibleForFree": True,
    "keywords": ["Boolean functions", "cryptography", "affine equivalence",
                 "nonlinearity", "equivalence classes", "bent functions"],
    "citation": ("J. Fuller. Analysis of Affine Equivalent Boolean Functions for "
                 "Cryptography. PhD thesis, Queensland University of Technology, 2003. "
                 "https://eprints.qut.edu.au/15828/"),
    "distribution": [
        {"@type": "DataDownload", "encodingFormat": "application/zip",
         "contentUrl": SITE + "data/n6-classes.zip", "name": "All 150,357 classes"},
        {"@type": "DataDownload", "encodingFormat": "application/zip",
         "contentUrl": SITE + "data/n6-balanced-classes.zip",
         "name": "74,542 classes containing balanced functions"},
    ],
}
DATASET_LD = ('<script type="application/ld+json">'
              + __import__("json").dumps(_DATASET, ensure_ascii=False) + "</script>\n")


def page(slug, title, desc, body, full=False, extra=""):
    canonical = SITE if slug == "index.html" else SITE + slug
    head = HEAD.format(title=title, desc=desc, canonical=canonical, extra=extra)
    main_cls = "container" if not full else "container"
    html = head + nav(slug) + f'<main class="{main_cls}">\n' + body + "\n</main>\n" + FOOTER
    # cache-busting: version local assets by content hash so browsers fetch updated files
    import hashlib
    for asset in ("style.css", "explorer.js", "analyse.js", "aes.js"):
        try:
            v = hashlib.md5(open(asset, "rb").read()).hexdigest()[:8]
        except FileNotFoundError:
            continue
        html = html.replace(f'"{asset}"', f'"{asset}?v={v}"')
    with open(slug, "w") as f:
        f.write(html)
    return slug


# ── data tables ──────────────────────────────────────────────────────────────

N3 = [
    (1, "0xaa", 1, 0, "{(0,7),(8,1)}", "{(8,8)}"),
    (2, "0xab", 3, 1, "{(2,7),(6,1)}", "{(4,7),(8,1)}"),
    (3, "0xac", 2, 2, "{(0,4),(4,4)}", "{(0,6),(8,2)}"),
]

N4 = [
    (1, "0xaa55", 1, 0, "{(0,15),(16,1)}", "{(16,16)}"),
    (2, "0xab55", 4, 1, "{(2,15),(14,1)}", "{(12,15),(16,1)}"),
    (3, "0xbb55", 3, 2, "{(0,8),(4,7),(12,1)}", "{(8,14),(16,2)}"),
    (4, "0xaba5", 4, 3, "{(2,12),(6,3),(10,1)}", "{(4,12),(12,3),(16,1)}"),
    (5, "0xaaff", 2, 4, "{(0,12),(8,4)}", "{(0,12),(16,4)}"),
    (6, "0xaba4", 3, 4, "{(0,6),(4,8),(8,2)}", "{(0,9),(8,6),(16,1)}"),
    (7, "0xab12", 4, 5, "{(2,10),(6,6)}", "{(4,15),(16,1)}"),
    (8, "0xac90", 2, 6, "{(4,16)}", "{(0,15),(16,1)}"),
]

N5 = [
    (1, "0xaa55aa55", 1, 0, "{(0,31),(32,1)}", "{(32,32)}"),
    (2, "0xaa55ab55", 5, 1, "{(2,31),(30,1)}", "{(28,31),(32,1)}"),
    (3, "0xaa55bb55", 4, 2, "{(0,16),(4,15),(28,1)}", "{(24,30),(32,2)}"),
    (4, "0xaa5dbb55", 5, 3, "{(2,24),(6,7),(26,1)}", "{(20,28),(28,3),(32,1)}"),
    (5, "0xaaddbb55", 3, 4, "{(0,24),(8,7),(24,1)}", "{(16,28),(32,4)}"),
    (6, "0xaa5dbb51", 4, 4, "{(0,12),(4,16),(8,3),(24,1)}", "{(16,25),(24,6),(32,1)}"),
    (7, "0x2a5dbb51", 5, 5, "{(2,20),(6,10),(10,1),(22,1)}", "{(12,21),(20,10),(32,1)}"),
    (8, "0xaaddbb51", 5, 5, "{(2,24),(6,4),(10,3),(22,1)}", "{(12,24),(20,4),(28,3),(32,1)}"),
    (9, "0x2a5dbf51", 3, 6, "{(4,30),(12,1),(20,1)}", "{(8,16),(16,15),(32,1)}"),
    (10, "0x6a5dbb51", 4, 6, "{(0,10),(4,15),(8,6),(20,1)}", "{(8,16),(16,15),(32,1)}"),
    (11, "0x2addbb51", 4, 6, "{(0,12),(4,14),(8,4),(12,1),(20,1)}", "{(8,19),(16,9),(24,3),(32,1)}"),
    (12, "0xa8ddbb51", 4, 6, "{(0,16),(4,12),(12,3),(20,1)}", "{(8,24),(24,6),(32,2)}"),
    (13, "0xaeddda51", 5, 7, "{(2,15),(6,15),(10,1),(18,1)}", "{(4,10),(12,21),(32,1)}"),
    (14, "0x0a5dbf51", 5, 7, "{(2,18),(6,12),(14,1),(18,1)}", "{(4,16),(12,9),(20,6),(32,1)}"),
    (15, "0x8addda51", 5, 7, "{(2,19),(6,9),(10,3),(18,1)}", "{(4,13),(12,15),(20,3),(32,1)}"),
    (16, "0xa8dd9b51", 5, 7, "{(2,22),(6,6),(10,2),(14,1),(18,1)}", "{(4,18),(12,6),(20,6),(28,1),(32,1)}"),
    (17, "0x88ddbb51", 5, 7, "{(2,28),(14,3),(18,1)}", "{(4,24),(28,7),(32,1)}"),
    (18, "0x88ddbb11", 2, 8, "{(0,28),(16,4)}", "{(0,24),(32,8)}"),
    (19, "0x8c5dda51", 3, 8, "{(0,19),(8,12),(16,1)}", "{(0,9),(8,16),(16,6),(32,1)}"),
    (20, "0xa89d9b51", 3, 8, "{(0,22),(8,8),(16,2)}", "{(0,18),(16,12),(32,2)}"),
    (21, "0x8eddda51", 4, 8, "{(0,7),(4,16),(8,8),(16,1)}", "{(0,6),(8,22),(16,3),(32,1)}"),
    (22, "0xaefdda51", 4, 8, "{(0,9),(4,15),(8,6),(12,1),(16,1)}", "{(0,9),(8,16),(16,6),(32,1)}"),
    (23, "0x025dbf51", 4, 8, "{(0,10),(4,16),(8,4),(16,2)}", "{(0,16),(8,4),(16,9),(24,2),(32,1)}"),
    (24, "0x88ddda51", 4, 8, "{(0,11),(4,14),(8,4),(12,2),(16,1)}", "{(0,11),(8,13),(16,6),(24,1),(32,1)}"),
    (25, "0x88dd9b51", 4, 8, "{(0,14),(4,14),(12,2),(16,2)}", "{(0,17),(8,7),(24,7),(32,1)}"),
    (26, "0xceddda51", 5, 9, "{(2,15),(6,13),(10,3),(14,1)}", "{(4,22),(12,9),(32,1)}"),
    (27, "0x0eddda51", 5, 9, "{(2,15),(6,13),(10,3),(14,1)}", "{(4,24),(12,6),(20,1),(32,1)}"),
    (28, "0x425dbf51", 5, 9, "{(2,18),(6,10),(10,2),(14,2)}", "{(4,20),(12,9),(20,2),(32,1)}"),
    (29, "0x8cddda51", 5, 9, "{(2,19),(6,7),(10,5),(14,1)}", "{(4,21),(12,9),(20,1),(32,1)}"),
    (30, "0x88dddb51", 5, 9, "{(2,21),(6,7),(10,1),(14,3)}", "{(4,24),(20,7),(32,1)}"),
    (31, "0x289d9b51", 5, 9, "{(2,22),(6,4),(10,4),(14,2)}", "{(4,18),(12,12),(28,1),(32,1)}"),
    (32, "0x86fdda51", 3, 10, "{(4,28),(12,4)}", "{(0,12),(8,16),(16,3),(32,1)}"),
    (33, "0x88dddb71", 3, 10, "{(4,28),(12,4)}", "{(0,24),(16,7),(32,1)}"),
    (34, "0xcefdda51", 4, 10, "{(0,6),(4,15),(8,10),(12,1)}", "{(0,15),(8,16),(32,1)}"),
    (35, "0x0efdda51", 4, 10, "{(0,8),(4,14),(8,8),(12,2)}", "{(0,15),(8,14),(16,2),(32,1)}"),
    (36, "0x288d9b51", 4, 10, "{(0,8),(4,14),(8,8),(12,2)}", "{(0,17),(8,13),(24,1),(32,1)}"),
    (37, "0x8cfdda51", 4, 10, "{(0,10),(4,13),(8,6),(12,3)}", "{(0,12),(8,16),(16,3),(32,1)}"),
    (38, "0x8cdddb51", 4, 10, "{(0,12),(4,12),(8,4),(12,4)}", "{(0,18),(8,6),(16,7),(32,1)}"),
    (39, "0x8ccdda51", 4, 10, "{(0,12),(4,12),(8,4),(12,4)}", "{(0,8),(8,21),(16,1),(24,1),(32,1)}"),
    (40, "0x289d9b41", 4, 10, "{(0,16),(4,10),(12,6)}", "{(8,30),(32,2)}"),
    (41, "0x488ddb51", 5, 11, "{(2,12),(6,16),(10,4)}", "{(4,28),(12,3),(32,1)}"),
    (42, "0xccfdda51", 5, 11, "{(2,16),(6,10),(10,6)}", "{(4,25),(12,6),(32,1)}"),
    (43, "0x688d9b51", 5, 11, "{(2,16),(6,10),(10,6)}", "{(4,27),(12,3),(20,1),(32,1)}"),
    (44, "0x288d9b41", 5, 11, "{(2,16),(6,10),(10,6)}", "{(4,30),(28,1),(32,1)}"),
    (45, "0x288d1b41", 2, 12, "{(0,16),(8,16)}", "{(0,30),(32,2)}"),
    (46, "0xdcfdda51", 3, 12, "{(0,16),(8,16)}", "{(0,15),(8,16),(32,1)}"),
    (47, "0x68ad9b51", 3, 12, "{(0,16),(8,16)}", "{(0,27),(16,4),(32,1)}"),
    (48, "0x688ddb51", 4, 12, "{(0,4),(4,16),(8,12)}", "{(0,24),(8,6),(16,1),(32,1)}"),
]

# n = 6 equivalence classes by nonlinearity (count per NL level).
N6_BY_NL = [
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 4), (7, 6), (8, 11),
    (9, 15), (10, 29), (11, 46), (12, 92), (13, 160), (14, 325), (15, 626),
    (16, 1326), (17, 2647), (18, 5496), (19, 10789), (20, 19964), (21, 31521),
    (22, 38142), (23, 27795), (24, 10280), (25, 983), (26, 84), (27, 4), (28, 4),
]

# n = 6 classes by (nl, ord, acmax): (nl, ord, acmax, classes, classes containing balanced
# functions). Derived from the released .exp data files (data/*.zip); sums to 150,357 / 74,542.
N6_DETAIL = [
    (0, 1, 64, 1, 1), (1, 6, 60, 1, 0), (2, 5, 64, 1, 1), (3, 6, 60, 1, 0),
    (4, 4, 64, 1, 1), (4, 5, 56, 1, 1), (5, 6, 52, 1, 0), (5, 6, 60, 1, 0),
    (6, 4, 48, 1, 0), (6, 5, 48, 1, 1), (6, 5, 56, 1, 1), (6, 5, 64, 1, 1),
    (7, 6, 44, 2, 0), (7, 6, 52, 2, 0), (7, 6, 60, 2, 0), (8, 3, 64, 1, 1),
    (8, 4, 40, 1, 1), (8, 4, 48, 1, 1), (8, 4, 64, 1, 1), (8, 5, 40, 1, 1),
    (8, 5, 48, 3, 3), (8, 5, 56, 3, 3), (9, 6, 36, 1, 0), (9, 6, 44, 5, 0),
    (9, 6, 52, 6, 0), (9, 6, 60, 3, 0), (10, 4, 40, 1, 0), (10, 4, 48, 4, 0),
    (10, 5, 40, 6, 6), (10, 5, 48, 10, 10), (10, 5, 56, 6, 6), (10, 5, 64, 2, 2),
    (11, 6, 36, 5, 0), (11, 6, 44, 22, 0), (11, 6, 52, 14, 0), (11, 6, 60, 5, 0),
    (12, 3, 64, 1, 1), (12, 4, 32, 2, 2), (12, 4, 40, 4, 4), (12, 4, 48, 6, 6),
    (12, 4, 64, 3, 3), (12, 5, 32, 3, 3), (12, 5, 40, 31, 31), (12, 5, 48, 30, 30),
    (12, 5, 56, 12, 12), (13, 6, 28, 2, 0), (13, 6, 36, 48, 0), (13, 6, 44, 72, 0),
    (13, 6, 52, 29, 0), (13, 6, 60, 9, 0), (14, 3, 32, 1, 0), (14, 4, 32, 6, 0),
    (14, 4, 40, 9, 0), (14, 4, 48, 13, 0), (14, 5, 24, 1, 1), (14, 5, 32, 44, 44),
    (14, 5, 40, 153, 153), (14, 5, 48, 70, 70), (14, 5, 56, 23, 23), (14, 5, 64, 5, 5),
    (15, 6, 20, 1, 0), (15, 6, 28, 40, 0), (15, 6, 36, 296, 0), (15, 6, 44, 213, 0),
    (15, 6, 52, 62, 0), (15, 6, 60, 14, 0), (16, 2, 64, 1, 1), (16, 3, 32, 2, 2),
    (16, 3, 64, 2, 2), (16, 4, 16, 1, 1), (16, 4, 24, 1, 1), (16, 4, 32, 36, 36),
    (16, 4, 40, 26, 26), (16, 4, 48, 25, 25), (16, 4, 64, 5, 5), (16, 5, 24, 18, 18),
    (16, 5, 32, 459, 459), (16, 5, 40, 536, 536), (16, 5, 48, 175, 175), (16, 5, 56, 39, 39),
    (17, 6, 20, 6, 0), (17, 6, 28, 611, 0), (17, 6, 36, 1360, 0), (17, 6, 44, 540, 0),
    (17, 6, 52, 115, 0), (17, 6, 60, 15, 0), (18, 3, 16, 1, 0), (18, 3, 32, 1, 0),
    (18, 4, 16, 1, 0), (18, 4, 24, 22, 0), (18, 4, 32, 103, 0), (18, 4, 40, 58, 0),
    (18, 4, 48, 41, 0), (18, 5, 16, 1, 0), (18, 5, 24, 485, 483), (18, 5, 32, 2850, 2850),
    (18, 5, 40, 1532, 1532), (18, 5, 48, 336, 336), (18, 5, 56, 59, 59), (18, 5, 64, 6, 6),
    (19, 6, 12, 1, 0), (19, 6, 20, 196, 0), (19, 6, 28, 4980, 0), (19, 6, 36, 4336, 0),
    (19, 6, 44, 1083, 0), (19, 6, 52, 172, 0), (19, 6, 60, 21, 0), (20, 3, 32, 3, 3),
    (20, 3, 64, 2, 2), (20, 4, 16, 5, 5), (20, 4, 24, 134, 134), (20, 4, 32, 331, 331),
    (20, 4, 40, 94, 94), (20, 4, 48, 49, 49), (20, 4, 64, 7, 7), (20, 5, 16, 22, 19),
    (20, 5, 24, 5536, 5535), (20, 5, 32, 10368, 10365), (20, 5, 40, 2903, 2903), (20, 5, 48, 453, 453),
    (20, 5, 56, 57, 57), (21, 6, 12, 3, 0), (21, 6, 20, 3465, 0), (21, 6, 28, 19721, 0),
    (21, 6, 36, 7132, 0), (21, 6, 44, 1067, 0), (21, 6, 52, 122, 0), (21, 6, 60, 11, 0),
    (22, 3, 16, 3, 0), (22, 3, 32, 1, 0), (22, 4, 16, 38, 0), (22, 4, 24, 401, 0),
    (22, 4, 32, 326, 0), (22, 4, 40, 71, 0), (22, 4, 48, 32, 0), (22, 5, 16, 617, 613),
    (22, 5, 24, 21655, 21651), (22, 5, 32, 12852, 12852), (22, 5, 40, 1908, 1908), (22, 5, 48, 208, 208),
    (22, 5, 56, 26, 26), (22, 5, 64, 4, 4), (23, 6, 12, 14, 0), (23, 6, 20, 10898, 0),
    (23, 6, 28, 14524, 0), (23, 6, 36, 2127, 0), (23, 6, 44, 202, 0), (23, 6, 52, 25, 0),
    (23, 6, 60, 5, 0), (24, 2, 64, 1, 1), (24, 3, 16, 1, 1), (24, 3, 32, 6, 6),
    (24, 3, 64, 2, 2), (24, 4, 16, 54, 54), (24, 4, 24, 304, 304), (24, 4, 32, 161, 161),
    (24, 4, 40, 20, 20), (24, 4, 48, 11, 11), (24, 4, 64, 1, 1), (24, 5, 16, 1626, 1626),
    (24, 5, 24, 6716, 6716), (24, 5, 32, 1239, 1239), (24, 5, 40, 118, 118), (24, 5, 48, 18, 17),
    (24, 5, 56, 2, 2), (25, 6, 12, 73, 0), (25, 6, 20, 745, 0), (25, 6, 28, 149, 0),
    (25, 6, 36, 15, 0), (25, 6, 44, 1, 0), (26, 4, 16, 34, 0), (26, 4, 24, 17, 0),
    (26, 4, 32, 2, 0), (26, 4, 40, 1, 0), (26, 5, 8, 8, 0), (26, 5, 16, 13, 13),
    (26, 5, 24, 7, 7), (26, 5, 32, 1, 1), (26, 5, 40, 1, 1), (27, 6, 4, 4, 0),
    (28, 2, 0, 1, 0), (28, 3, 0, 3, 0),
]


# Self-mapping analysis (thesis Ch. 4 and App. 4), validated 2026-11-14 against the original
# PhD output (n6_fns_full.exp): n=5 sizes sum to 2^32; n=6 sizes sum to 2^64.
AFFINE_T = {2: 192, 3: 21504, 4: 10321920, 5: 20478689280, 6: 165140150353920}
SELF5 = [  # (class, example, self maps theta, functions in class)
    (1, "0xaa55aa55", 319979520, 64),
    (2, "0xaa55ab55", 9999360, 2048),
    (3, "0xaa55bb55", 645120, 31744),
    (4, "0xaa5dbb55", 64512, 317440),
    (5, "0xaaddbb55", 258048, 79360),
    (6, "0xaa5dbb51", 9216, 2222080),
    (7, "0x2a5dbb51", 1920, 10665984),
    (8, "0xaaddbb51", 9216, 2222080),
    (9, "0x2a5dbf51", 11520, 1777664),
    (10, "0x6a5dbb51", 720, 28442624),
    (11, "0x2addbb51", 768, 26664960),
    (12, "0xa8ddbb51", 18432, 1111040),
    (13, "0xaeddda51", 720, 28442624),
    (14, "0x0a5dbf51", 1152, 17776640),
    (15, "0x8addda51", 144, 142213120),
    (16, "0xa8dd9b51", 768, 26664960),
    (17, "0x88ddbb51", 64512, 317440),
    (18, "0x88ddbb11", 2064384, 9920),
    (19, "0x8c5dda51", 1152, 17776640),
    (20, "0xa89d9b51", 12288, 1666560),
    (21, "0x8eddda51", 192, 106659840),
    (22, "0xaefdda51", 72, 284426240),
    (23, "0x025dbf51", 1024, 19998720),
    (24, "0x88ddda51", 96, 213319680),
    (25, "0x88dd9b51", 5376, 3809280),
    (26, "0xceddda51", 48, 426639360),
    (27, "0x0eddda51", 144, 142213120),
    (28, "0x425dbf51", 64, 319979520),
    (29, "0x8cddda51", 48, 426639360),
    (30, "0x88dddb51", 1008, 20316160),
    (31, "0x289d9b51", 768, 26664960),
    (32, "0x86fdda51", 768, 26664960),
    (33, "0x88dddb71", 4032, 5079040),
    (34, "0xcefdda51", 120, 170655744),
    (35, "0x0efdda51", 32, 639959040),
    (36, "0x288d9b51", 768, 26664960),
    (37, "0x8cfdda51", 48, 426639360),
    (38, "0x8cdddb51", 576, 35553280),
    (39, "0x8ccdda51", 256, 79994880),
    (40, "0x289d9b41", 23040, 888832),
    (41, "0x488ddb51", 192, 106659840),
    (42, "0xccfdda51", 60, 341311488),
    (43, "0x688d9b51", 192, 106659840),
    (44, "0x288d9b41", 11520, 1777664),
    (45, "0x288d1b41", 368640, 55552),
    (46, "0xdcfdda51", 1920, 10665984),
    (47, "0x68ad9b51", 6144, 3333120),
    (48, "0x688ddb51", 1536, 13332480),
]
SELF6_FREQ = [  # (theta, number of n=6 classes)
    (1, 91184), (2, 32454), (3, 206), (4, 12522), (6, 530),
    (7, 4), (8, 5590), (10, 12), (12, 582), (14, 8),
    (16, 2665), (18, 6), (20, 30), (24, 506), (32, 1275),
    (36, 29), (40, 4), (42, 4), (48, 351), (60, 8),
    (64, 591), (72, 54), (96, 191), (120, 18), (128, 346),
    (144, 50), (168, 4), (192, 183), (240, 14), (256, 140),
    (288, 36), (320, 4), (336, 2), (360, 5), (384, 130),
    (432, 6), (480, 1), (512, 79), (576, 9), (640, 1),
    (672, 1), (720, 9), (768, 43), (1008, 5), (1024, 39),
    (1152, 54), (1296, 4), (1344, 2), (1440, 6), (1536, 72),
    (1920, 3), (2048, 29), (2160, 2), (2304, 13), (2880, 1),
    (3072, 20), (3456, 5), (3840, 8), (4032, 3), (4096, 9),
    (4320, 3), (4608, 24), (5040, 2), (5376, 1), (5760, 1),
    (6144, 22), (7680, 1), (8064, 2), (8192, 3), (9216, 2),
    (10752, 4), (12288, 19), (13824, 1), (16384, 2), (17280, 1),
    (18432, 4), (23040, 6), (24576, 3), (32256, 5), (36864, 8),
    (40320, 2), (43008, 1), (46080, 5), (49152, 7), (56448, 2),
    (61440, 1), (64512, 1), (65536, 1), (73728, 11), (86016, 2),
    (98304, 1), (110592, 2), (120960, 1), (122880, 3), (184320, 2),
    (258048, 2), (294912, 2), (344064, 1), (393216, 1), (483840, 1),
    (589824, 2), (688128, 1), (737280, 3), (884736, 1), (1105920, 4),
    (1290240, 1), (1451520, 1), (2064384, 3), (2359296, 1), (3538944, 1),
    (4128768, 2), (4423680, 1), (14450688, 1), (30965760, 2), (70778880, 1),
    (92897280, 1), (115605504, 1), (123863040, 1), (639959040, 1), (1981808640, 1),
    (20158709760, 1), (1290157424640, 1),
]
N6_FNS_BY_NL = [  # (nl, number of 6-variable functions)
    (0, 128),
    (1, 8192),
]

# Thesis Chapter 5 tables (extracted programmatically from chapter5.tex, 2026-11-14).
BENT_SURVEY = [(8, 3, 148, 19, 12, 16, 0.0), (8, 4, 461, 106, 17, 21, 0.59), (10, 3, 221, 45, 19, 24, 0.63), (10, 4, 1234, 333, 32, 37, 1.56), (10, 5, 2736, 609, 51, 56, 1.76), (12, 3, 403, 92, 37, 43, 2.16), (12, 4, 1374, 530, 56, 62, 6.07), (12, 5, 7230, 2087, 78, 84, 17.97), (12, 6, 4796, 2042, 66, 72, 19.58), (14, 3, 657, 181, 71, 78, 10.01), (14, 4, 3984, 1889, 57, 64, 111.04), (14, 5, 9866, 3760, 118, 125, 110.25), (14, 6, 24927, 8956, 187, 194, 165.32), (14, 7, 58120, 16583, 146, 153, 404.27), (16, 3, 1007, 328, 113, 121, 52.38), (16, 4, 4595, 2546, 165, 173, 248.36), (16, 5, 13204, 5897, 292, 300, 332.22), (16, 6, 43550, 21258, 365, 373, 930.08), (16, 7, 155116, 61076, 424, 432, 2361.32), (16, 8, 194022, 83545, 339, 347, 3947.06)]  # (n, maxOrd, ANF positions tested, passing half-balance, bent fns, max ANF weight, ms per fn)
BENT8_CLASSES = [(1, 2, '0x2BE74D7E,0x17DB8EBD,0x24E8BD8E,0x18D47E4D,0x4271DB17,0x7E4D18D4,0xB281D418,0x8EBD17DB'), (2, 3, '0x8B12DE47,0x47211274,0x48D11D84,0xD1B784E2,0x7B1D2E48,0xB72EE27B,0x47211274,0xDE478B12'), (3, 3, '0x8B12DE47,0x47741221,0x59C00C95,0xC0F395A6,0x7B1D2E48,0xB77BE22E,0x56300365,0xCF039A56'), (4, 3, '0x00660F96,0xF069FF99,0xC35ACCAA,0xC3A5CC55,0x69FF99F0,0x99F069FF,0xA533AAC3,0xA5CCAA3C'), (5, 4, '0xD17BF9AC,0x2E84ACF9,0x2B81DE8B,0x2B817421,0x7BD15306,0x842E0653,0x812B7421,0x812BDE8B'), (6, 4, '0xD17BF9AC,0xA60C2471,0xE74DDE8B,0x6FC5FCA9,0x7BD15306,0x0CA68EDB,0x4DE77421,0xC56F5603'), (7, 4, '0x9669F550,0x996650F5,0x33CCAFF5,0x3CC30A50,0xC9C9500A,0x6C6C0A50,0x63630AAF,0xC6C650F5'), (8, 4, '0xBD24B22B,0x7E187117,0xB117BE18,0x8DD482DB,0x81188E17,0x42244D2B,0x8D2B8224,0xB1E8BEE7'), (9, 4, '0xBD24B22B,0xBED8B1D7,0xB117BE18,0x4D14421B,0x81188E17,0x82E48DEB,0x8D2B8224,0x71287E27'), (10, 4, '0xFDA4F2AB,0xC258CD57,0x0D570258,0xCD54C25B,0x31983E97,0xFE64F16B,0xC19BCE94,0xF198FE97'), (11, 4, '0xF60650A0,0x50A0F505,0x0AFA53A3,0xAC5CF606,0x9A6A33C3,0xC3336999,0xC6369060,0x9F6FCA3A'), (12, 4, '0x8F7F26D6,0xBC4C1AEA,0x7C8C15E5,0x40B026D6,0x50A036C6,0x93630AFA,0x5CACFA0A,0x9060C939'), (13, 4, '0x659AA956,0x6A95A659,0xFCFCCFCF,0xF3F3C0C0,0x95955959,0x6565A9A9,0x00FFCC33,0x3CC30FF0'), (14, 4, '0xF13D68A4,0x0EC2975B,0x6C55390F,0x6C55390F,0x32546701,0x67AB32FE,0x635A36FF,0xC95A9CFF')]  # (class, order, words) — all verified bent (NL 120), orders verified
BENT_CLASS_LB = [(8, 1, 3, 10, None, None, None, 14), (10, 1, 7, 11, 27, None, None, 46), (12, 1, 7, 20, 32, 56, None, 116), (14, 1, 9, 26, 43, 71, 39, 189)]  # (n, ord 2..7, total): lower bounds on # bent classes, 2003
DHC_N8 = [(86, 0, 0, 0, 0), (88, 1, 0, 0, 0), (90, 1, 0, 0, 0), (92, 5, 0, 0, 0), (94, 16, 0, 0, 0), (96, 38, 0, 0, 0), (98, 95, 0, 0, 0), (100, 191, 0, 0, 0), (102, 318, 0, 0, 0), (104, 267, 0, 0, 0), (106, 64, 5, 0, 0), (108, 4, 190, 0, 0), (110, 0, 505, 38, 0), (112, 0, 300, 962, 13), (114, 0, 0, 0, 613), (116, 0, 0, 0, 374)]  # (NL, random, strong, weak, dynamic) frequencies, 1000 runs each, n = 8
EX_8_1_6_116 = [(1, 32, '0xC66FC7A0,0xB8899B46,0xE8E3ED41,0x2063B4ED,0x5EA1C35D,0xF4390587,0x33359850,0x0ABD7B8F'), (2, 32, '0x9DE5BC48,0x64D4A343,0x800355F2,0xBDB3EE6A,0x18F78F1E,0xD90B82AD,0x2C374E79,0xB57027C0'), (3, 32, '0xA374983D,0x4D768EB9,0xD0FC0589,0xB7B06CC1,0x42CEFFA3,0x0E90A702,0x145575A9,0xBB97928F'), (4, 32, '0xA633674A,0xC56E36DB,0xB88DF74A,0x4AEB0480,0x09C8B263,0xEAD07345,0x9F0591AF,0x705F74D6'), (5, 32, '0xC25E9ECD,0xCBA2D991,0x44133A1A,0x80FBDBB2,0x53875D8E,0x981607B8,0x4DB4F670,0x7F6F40A1'), (6, 32, '0xD46017F8,0xBB512E20,0x9D36E57A,0x9CBD116A,0x7CCD561F,0x1FC26876,0x04C2926A,0x4A1FBDAA'), (7, 32, '0xF0E47A90,0x11C19FC2,0xFF6A2BA1,0xC49E4A3E,0xF01C0E9F,0x19DFD43E,0x3619C255,0x2E299395'), (8, 32, '0xF0C8283E,0xF06E3D20,0x23EDD6FB,0xA464254F,0x66075D1D,0x9FE8CAD9,0x38C73302,0xA6537A45'), (9, 32, '0x981E36BA,0x8BD75C65,0x7F80FADC,0x8D80050F,0x71D84493,0x25706EF2,0xC1BE1A23,0xFEC3169B'), (10, 32, '0xCB39E0B8,0xCE7D4CEC,0x2D5963E7,0x00A4DB22,0x920F29A5,0xD83A5A91,0x4155AFC3,0xBF57F124')]  # (class, acmax, words) — verified balanced, 1-resilient, deg 6, NL 116
RANDOM_BALANCED = [(6, 21.5, 5.0, 27.9), (7, 47.9, 6.0, 43.8), (8, 103.5, 7.0, 67.6), (9, 219.2, 8.0, 102.8), (10, 456.8, 9.0, 154.7), (11, 941.9, 10.0, 231.2), (12, 1926.3, 11.0, 343.4), (13, 3916.2, 12.0, 507.8), (14, 7927.4, 13.0, 747.7), (15, 15995.5, 14.0, 1098.4), (16, 32199.1, 15.0, 1609.1)]  # (n, avg NL, avg ord, avg acmax), 1e6 random balanced fns each

# 1-local neighbourhood connectivity: class -> connecting class(frequency) distribution.
CONN3 = [
    (1, "C2(8)"),
    (2, "C1(1), C3(7)"),
    (3, "C2(8)"),
]
CONN4 = [
    (1, "C2(16)"),
    (2, "C1(1), C3(15)"),
    (3, "C2(2), C4(14)"),
    (4, "C3(3), C5(1), C6(12)"),
    (5, "C4(16)"),
    (6, "C4(8), C7(8)"),
    (7, "C6(15), C8(1)"),
    (8, "C7(16)"),
]


def conn_table(rows):
    head = ("<thead><tr><th class=\"num\">class</th>"
            "<th>connecting class (frequency) distribution</th></tr></thead>")
    body = "".join(
        f"<tr><td class=\"num\">{c}</td><td>{dist}</td></tr>" for c, dist in rows)
    return ('<div class="table-scroll"><table>' + head + "<tbody>"
            + body + "</tbody></table></div>")


# Class connection diagrams (class trees), laid out by nonlinearity — affine class at the
# bottom (root), maximum-nonlinearity / bent classes as the topmost leaves, as in the thesis.
# node id -> (x, y, kind, label); kind in {"root", "bent", "normal"}.
TREE3_NODES = {
    1: (150, 210, "root", "1"),
    2: (150, 130, "normal", "2"),
    3: (150, 50, "normal", "3"),
}
TREE3_EDGES = [(1, 2), (2, 3)]
TREE3_AXIS = [(54, "NL 2"), (134, "NL 1"), (214, "NL 0")]

TREE4_NODES = {
    1: (200, 372, "root", "1"),
    2: (200, 316, "normal", "2"),
    3: (200, 260, "normal", "3"),
    4: (200, 204, "normal", "4"),
    5: (120, 148, "normal", "5"),
    6: (260, 148, "normal", "6"),
    7: (260, 92, "normal", "7"),
    8: (260, 40, "bent", "8"),
}
TREE4_EDGES = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (6, 7), (7, 8)]
TREE4_AXIS = [(44, "NL 6"), (96, "NL 5"), (148, "NL 4"), (204, "NL 3"),
              (260, "NL 2"), (316, "NL 1"), (372, "NL 0")]


def svg_tree(width, height, nodes, edges, axis, caption, desc):
    p = [f'<figure class="diagram"><svg viewBox="0 0 {width} {height}" role="img" '
         f'aria-label="{desc}" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{caption}</title><desc>{desc}</desc>"]
    for y, lab in axis:
        p.append(f'<text class="nl-axis" x="8" y="{y + 4}">{lab}</text>')
    for a, b in edges:
        ax, ay, _, _ = nodes[a]
        bx, by, _, _ = nodes[b]
        p.append(f'<line class="edge" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}"/>')
    for x, y, kind, label in nodes.values():
        cls = {"root": "node root", "bent": "node bent", "normal": "node"}[kind]
        p.append(f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="16"/>'
                 f'<text x="{x}" y="{y + 5}">{label}</text></g>')
    p.append("</svg>")
    p.append(f"<figcaption>{caption}</figcaption></figure>")
    return "".join(p)


DIAGRAM_LEGEND = ('<div class="diagram-legend"><span class="key root"></span> affine class '
                  '(root) <span class="key bent"></span> bent class</div>')


def class_table(rows):
    head = ("<thead><tr><th class=\"num\">class</th><th>example</th>"
            "<th class=\"num\">ord</th><th class=\"num\">nl</th>"
            "<th>abs. WHT distribution</th><th>abs. AC distribution</th></tr></thead>")
    body = []
    for c, ex, ordr, nl, wht, ac in rows:
        body.append(
            f"<tr><td class=\"num\">{c}</td><td><code>{ex}</code></td>"
            f"<td class=\"num\">{ordr}</td><td class=\"num\">{nl}</td>"
            f"<td>{wht}</td><td>{ac}</td></tr>")
    return ('<div class="table-scroll"><table>' + head + "<tbody>"
            + "".join(body) + "</tbody></table></div>")


def n6_table(rows):
    half = (len(rows) + 1) // 2
    left, right = rows[:half], rows[half:]
    head = ("<thead><tr><th class=\"num\">nl</th><th class=\"num\">classes</th>"
            "<th></th><th class=\"num\">nl</th><th class=\"num\">classes</th></tr></thead>")
    body = []
    for i in range(half):
        lnl, lc = left[i]
        if i < len(right):
            rnl, rc = right[i]
            r = f"<td class=\"num\">{rnl}</td><td class=\"num\">{rc:,}</td>"
        else:
            r = "<td></td><td></td>"
        body.append(f"<tr><td class=\"num\">{lnl}</td><td class=\"num\">{lc:,}</td>"
                     f"<td></td>{r}</tr>")
    return ('<div class="table-scroll"><table>' + head + "<tbody>"
            + "".join(body) + "</tbody></table></div>")


def bf_analyse(tt, n):
    """Worked-example helper: truth table (bit i = f(i), x1 = bit 0 of i) -> dict of properties."""
    N = 1 << n
    bits = [(tt >> i) & 1 for i in range(N)]
    anf = bits[:]
    h = 1
    while h < N:
        for i in range(0, N, 2 * h):
            for j in range(i, i + h):
                anf[j + h] ^= anf[j]
        h *= 2
    dot = lambda a, b: bin(a & b).count("1") & 1
    wht = [sum((-1) ** (bits[x] ^ dot(w, x)) for x in range(N)) for w in range(N)]
    ac = [sum((-1) ** (bits[x] ^ bits[x ^ s]) for x in range(N)) for s in range(N)]
    mono = lambda m: "".join(f"x_{k + 1}" for k in range(n) if (m >> k) & 1) or "1"
    terms = [mono(m) for m in range(N) if anf[m]]
    return {
        "bits": bits, "weight": sum(bits), "anf": anf,
        "anf_str": " \\oplus ".join(terms) if terms else "0",
        "degree": max([bin(m).count("1") for m in range(N) if anf[m]] + [0]),
        "wht": wht, "nl": (N - max(map(abs, wht))) // 2, "ac": ac,
    }


# Exact class sizes for n = 3, 4 (by enumerating all 2^(2^n) functions, 2026-11-14; sums 256 / 65,536).
SIZES34 = {3: {1: 16, 2: 128, 3: 112},
           4: {1: 32, 2: 512, 3: 3840, 4: 17920, 5: 1120, 6: 26880, 7: 14336, 8: 896}}


def _class_key(bits, n):
    """(sorted |WHT|, sorted |AC|): identifies the affine class uniquely for n <= 5."""
    N = 1 << n
    w = [1 - 2 * b for b in bits]
    h = 1
    while h < N:
        for i in range(0, N, 2 * h):
            for j in range(i, i + h):
                w[j], w[j + h] = w[j] + w[j + h], w[j] - w[j + h]
        h *= 2
    ac = [abs(sum(1 - 2 * (bits[x] ^ bits[x ^ s]) for x in range(N))) for s in range(N)]
    return ",".join(map(str, sorted(map(abs, w)))) + "|" + ",".join(map(str, sorted(ac)))


def class_graph(rows, n, sizes):
    """Exact class connection graph: flip each bit of each representative and identify the
    neighbour's class. Returns JSON-ready data for the explorer (nodes, links, layout, key map)."""
    import math
    N = 1 << n
    tt = {r[0]: [(int(r[1], 16) >> i) & 1 for i in range(N)] for r in rows}
    keys = {_class_key(tt[c], n): c for c in tt}
    assert len(keys) == len(rows), f"n={n}: (|WHT|,|AC|) key not complete"
    flips = {}
    for c, bits in tt.items():
        cnt = {}
        for i in range(N):
            b = bits[:]
            b[i] ^= 1
            k = keys[_class_key(b, n)]
            cnt[k] = cnt.get(k, 0) + 1
        flips[c] = cnt
    # layers by nonlinearity, then barycentric ordering to reduce edge crossings
    nl = {r[0]: r[3] for r in rows}
    levels = sorted(set(nl.values()))
    layer = {L: [c for c in tt if nl[c] == L] for L in levels}
    nbrs = {c: [k for k in flips[c] if k != c] for c in tt}
    pos = {}
    for L in levels:
        for i, c in enumerate(layer[L]):
            pos[c] = (i + 0.5) / len(layer[L])
    for sweep in range(8):
        order = levels if sweep % 2 == 0 else levels[::-1]
        for L in order:
            bary = {c: (sum(pos[k] for k in nbrs[c]) / len(nbrs[c])) if nbrs[c] else pos[c]
                    for c in layer[L]}
            layer[L].sort(key=lambda c: (bary[c], c))
            for i, c in enumerate(layer[L]):
                pos[c] = (i + 0.5) / len(layer[L])
    props = {r[0]: r for r in rows}
    total = sum(sizes.values())
    nodes = []
    for c in tt:
        _, ex, deg, nlv, wht, ac = props[c]
        T = 2 ** (2 * n + 1) * math.prod(2 ** n - 2 ** i for i in range(n))
        nodes.append({"id": c, "hex": ex, "nl": nlv, "deg": deg,
                      "acmax": max(abs(v) for v in bf_analyse(int(ex, 16), n)["ac"][1:]),
                      "wht": wht, "ac": ac, "size": sizes[c], "theta": T // sizes[c],
                      "bal": "(0," in wht, "x": round(pos[c], 4),
                      "y": levels.index(nlv) / max(1, len(levels) - 1),
                      "flips": sorted(([k, v] for k, v in flips[c].items()), key=lambda kv: -kv[1])})
    links = sorted({tuple(sorted((a, b))) for a in tt for b in flips[a] if a != b})
    return {"n": n, "total": total, "levels": levels, "nodes": nodes,
            "links": [list(l) for l in links], "keys": keys}


def vec(i, n):
    return "(" + ",".join(str((i >> k) & 1) for k in range(n)) + ")"


def simple_table(headers, rows, num_cols=()):
    """Generic table: headers list, rows of values; columns in num_cols right-aligned, ints comma-formatted."""
    th = "".join(f'<th class="num">{h}</th>' if i in num_cols else f"<th>{h}</th>"
                 for i, h in enumerate(headers))
    body = []
    for r in rows:
        cells = []
        for i, v in enumerate(r):
            txt = f"{v:,}" if isinstance(v, int) else str(v)
            cells.append(f'<td class="num">{txt}</td>' if i in num_cols else f"<td>{txt}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return ('<div class="table-scroll"><table><thead><tr>' + th + "</tr></thead><tbody>"
            + "".join(body) + "</tbody></table></div>")


def n6_detail_table(rows):
    head = ("<thead><tr><th class=\"num\">nl</th><th class=\"num\">ord</th>"
            "<th class=\"num\">acmax</th><th class=\"num\">classes</th>"
            "<th class=\"num\">with balanced</th><th>file</th></tr></thead>")
    body = []
    for nl, o, a, n, b in rows:
        f = f"n6_nl{nl}_ord{o}_acmax{a}.exp"
        body.append(f"<tr><td class=\"num\">{nl}</td><td class=\"num\">{o}</td>"
                    f"<td class=\"num\">{a}</td><td class=\"num\">{n:,}</td>"
                    f"<td class=\"num\">{b:,}</td><td><code>{f}</code></td></tr>")
    return ('<div class="table-scroll"><table>' + head + "<tbody>"
            + "".join(body) + "</tbody></table></div>")


def cards(items):
    out = ['<div class="prop-cards">']
    for num, lbl in items:
        out.append(f'<div class="card"><div class="num">{num}</div><div class="lbl">{lbl}</div></div>')
    out.append("</div>")
    return "".join(out)


# S-box survey, transcribed from the original Boolean Planet page summ_sbox.htm (c. 2003).
# (cipher, design technique, size, individual: classes, nl min, nl max,
#  XOR combinations: classes, nl min, nl max)   None = not applicable
FFI = "Finite field inversion"
BSA = "Bit-sliced algebraic; contains fixed points"
SBOXES = [
    ("AES (Rijndael), Grand-Cru, Mugi, Q, Scream", FFI, "8 × 8", 1, 112, 112, 1, 112, 112),
    ("Anubis", "Pseudo-random", "8 × 8", 8, 96, 108, 255, 94, 110),
    ("Noekeon", BSA, "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Q (s-box 1)", BSA, "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Q (s-box 2)", BSA, "4 × 4", 1, 4, 4, 2, 4, 4),
    ("Q (s-box 3)", BSA, "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Camellia (s-box 1)", FFI, "8 × 8", 1, 112, 112, 1, 112, 112),
    ("Camellia (s-box 4)", FFI, "8 × 8", 1, 112, 112, 1, 112, 112),
    ("SC2000", "Unknown", "5 × 5", 1, 12, 12, 1, 12, 12),
    ("SC2000", "Unknown", "6 × 6", 1, 24, 24, 1, 24, 24),
    ("Hierocrypt", "Unknown", "8 × 8", 8, 106, 110, 255, 106, 112),
    ("Serpent (s-box 1)", "Heuristic", "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Serpent (s-box 2)", "Heuristic", "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Serpent (s-box 3)", "Heuristic", "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Serpent (s-box 4)", "Heuristic", "4 × 4", 1, 4, 4, 2, 4, 4),
    ("Serpent (s-box 5)", "Heuristic", "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Serpent (s-box 6)", "Heuristic", "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Serpent (s-box 7)", "Heuristic", "4 × 4", 2, 4, 4, 2, 4, 4),
    ("Serpent (s-box 8)", "Heuristic", "4 × 4", 1, 4, 4, 2, 4, 4),
    ("Khazad", "Pseudo-random", "8 × 8", 8, 98, 108, 255, 96, 110),
    ("Square", FFI, "8 × 8", 1, 112, 112, 1, 112, 112),
    ("Misty1", "Heuristic; contains fixed points", "7 × 7", 1, 56, 56, 1, 56, 56),
    ("Misty1", "Heuristic; contains fixed points", "9 × 9", 1, 240, 240, 1, 240, 240),
    ("Sober-t32", "Hybrid of Skipjack S-box and ISRC-designed S-box", "8 × 32",
     32, 104, 112, None, None, None),
    ("Skipjack", "Unknown", "8 × 8", 8, 104, 108, 255, 100, 108),
    ("Mars", "Heuristic", "9 × 32", 32, 207, 226, None, None, None),
]


def sbox_table(rows):
    head = ("<thead><tr><th rowspan=\"2\">cipher</th><th rowspan=\"2\">design technique</th>"
            "<th rowspan=\"2\">size</th>"
            "<th colspan=\"3\">individual functions</th>"
            "<th colspan=\"3\">XOR combinations</th></tr>"
            "<tr><th class=\"num\">classes</th><th class=\"num\">nl min</th><th class=\"num\">nl max</th>"
            "<th class=\"num\">classes</th><th class=\"num\">nl min</th><th class=\"num\">nl max</th>"
            "</tr></thead>")
    body = []
    for row in rows:
        name, design, size = row[:3]
        nums = "".join(f"<td class=\"num\">{'n/a' if v is None else v}</td>" for v in row[3:])
        body.append(f"<tr><td>{name}</td><td>{design}</td><td>{size}</td>{nums}</tr>")
    return ('<div class="table-scroll"><table>' + head + "<tbody>"
            + "".join(body) + "</tbody></table></div>")


# ── pages ──────────────────────────────────────────────────────────────────

def build():
    # Home
    home = f"""<div class="hero">
<div class="tagline">The Boolean Planet · a world of zeros and ones</div>
<h1>Boolean Functions for Cryptography</h1>
<p>Boolean functions — built from nothing but zeros and ones — sit at the heart of
block ciphers, stream ciphers and hash functions. The strength of these systems depends
on choosing functions with the right cryptographic properties. This site collects results,
data and reference material from ongoing research into the design and analysis of
cryptographic Boolean functions.</p>
</div>

<h2>What's here</h2>
<p>A Boolean function of $n$ inputs is a map $f : \\{{0,1\\}}^n \\to \\{{0,1\\}}$ — its truth
table is a string of $2^n$ bits. Despite this simple definition, finding functions that
resist all known attacks remains an open problem. Researchers measure a function against
criteria such as <strong>nonlinearity</strong>, <strong>correlation immunity</strong>,
<strong>algebraic degree</strong> and <strong>autocorrelation</strong>, and group functions
into <strong>affine equivalence classes</strong> that share these properties.</p>

{cards([("150,357", "n = 6 equivalence classes"), ("74,542", "contain balanced functions"),
        ("4", "bent classes (NL = 28)"), ("n ≤ 6", "fully classified")])}

<h2>Explore</h2>
<ul>
<li><a href="basics.html"><strong>The Basics</strong></a>: a worked introduction, from truth table
to Walsh spectrum, nonlinearity and affine equivalence.</li>
<li><a href="equivalence-classes.html"><strong>Equivalence Classes</strong></a> — complete
affine equivalence class tables for $n = 3, 4, 5$, and a full summary of the 150,357 classes
for $n = 6$.</li>
<li><a href="explore.html"><strong>Class Graph Explorer</strong></a>: an interactive map of how the
classes connect for $n = 3, 4, 5$, with a hill-climbing animation.</li>
<li><a href="analyse.html"><strong>Function Analyser</strong></a>: paste any truth table (up to
10 inputs) to get its nonlinearity, degree, Walsh spectrum, algebraic immunity and class.</li>
<li><a href="class-sizes.html"><strong>Class Sizes</strong></a>: the self-mapping constant, which
counts the functions in every class, with exact counts by nonlinearity for $n = 6$.</li>
<li><a href="efficient-implementation.html"><strong>Efficient Implementation</strong></a> —
the word-packing and transform techniques that make exhaustive Boolean function research
feasible.</li>
<li><a href="constructions.html"><strong>Constructions and Search</strong></a>: a bent function
construction, the Boolean terrain, dynamic hill climbing, and the history of heuristic search at
QUT.</li>
<li><a href="sboxes.html"><strong>S-boxes and Linear Redundancy</strong></a>: why all 255 component
functions of the AES S-box are affine equivalent (check it in your browser), and a survey of
cipher S-boxes.</li>
<li><a href="publications.html"><strong>Publications</strong></a> — papers on cryptographic
Boolean function analysis and linear redundancy in the AES S-box.</li>
<li><a href="learning.html"><strong>Learning</strong></a> — references and resources for
getting into the field.</li>
</ul>

<h2>About</h2>
<p>This work began as PhD research at the Queensland University of Technology (Information
Security Research Centre) and continues today. The original <em>Boolean Planet</em> site
accompanied that research and was widely used as a reference for the $n = 6$ classification —
data that researchers have continued to draw on, including NIST's 2018 study of the
multiplicative complexity of 6-variable Boolean functions. This is its modern home.</p>

<h2>About me</h2>
<p>I completed my PhD on Boolean functions for cryptography
at the Queensland University of Technology in 2003, and since then my work has spanned:</p>
<ul>
<li><strong>Data science</strong>: I'm currently a Senior Data Scientist at Optimum, analysing
Optimum Network performance.</li>
<li><strong>Formal verification of blockchain systems</strong> at Consensys, where I co-authored
papers on deductive verification of smart contracts in Dafny
(<a href="https://arxiv.org/abs/2208.02920">arXiv 2208.02920</a>), a formal and executable
semantics of the Ethereum Virtual Machine in Dafny
(<a href="https://arxiv.org/abs/2303.00152">arXiv 2303.00152</a>), and formal verification of
the Ethereum 2.0 Beacon Chain.</li>
<li><strong>Financial econometrics</strong> at QUT's School of Economics and Finance: forecasting
volatility and electricity price spikes.</li>
<li><strong>Teaching</strong> at university and secondary level.</li>
</ul>
<p>My interest in Boolean functions never stopped. I've kept coming back to them over the years,
and I have unpublished work that I'm keen to finalise and share. This site is a first step.</p>
<p><strong>My research interests:</strong> cryptographic Boolean functions and their classification;
affine equivalence and invariants; cryptanalysis.</p>
<p>By <strong>Dr Joanne Fuller</strong> ·
<a href="https://orcid.org/0000-0002-5221-3505" rel="me noopener">ORCID 0000-0002-5221-3505</a> ·
<a href="https://scholar.google.com/citations?user=aCp_g7IAAAAJ&amp;hl=en" rel="me noopener">Google Scholar</a> ·
<a href="https://www.linkedin.com/in/joanne-fuller-phd-04955b1a/" rel="me noopener">LinkedIn</a> ·
<a href="https://eprints.qut.edu.au/15828/1/Joanne_Fuller_Thesis.pdf">PhD thesis (PDF)</a></p>"""
    page("index.html", "Boolean Functions for Cryptography",
         "Research, data and reference material on Boolean functions for cryptography — the Boolean Planet.",
         home, extra='<meta name="google-site-verification" content="o6ujCVw5XLwPzOo71x56H4U-ZcqMI4dI0_lqqAXOMBw">\n')

    # Equivalence classes
    eq = f"""<h1>Affine Equivalence Classes</h1>

<h2>Definitions</h2>
<p>An <strong>affine transform</strong> maps a Boolean function $f$ to a function $g$ such that</p>
<p>$$g(x) = f(Dx^{{T}} + a^{{T}}) + b \\cdot x^{{T}} + c,$$</p>
<p>where $D$ is an $n \\times n$ invertible matrix over $\\mathrm{{GF}}(2)$, $a$ and $b$ are
$n$-bit vectors, and $c$ is a binary constant. Two functions related by an affine transform
are <strong>affine equivalent</strong>, and the set of all functions equivalent to a given
$f$ forms its <strong>affine equivalence class</strong>.</p>
<p>Affine transforms preserve the most important cryptographic properties — nonlinearity,
algebraic degree, the absolute Walsh–Hadamard spectrum and the absolute autocorrelation
spectrum are all <em>invariant</em> across a class. Classifying functions into equivalence
classes therefore reduces the study of $2^{{2^{{n}}}}$ individual functions to a far smaller
set of representatives.</p>
<p>The tables below give, for each class: an <strong>example</strong> truth table (hex), the
algebraic order (<strong>ord</strong>), the <strong>nonlinearity</strong> (<strong>nl</strong>),
and the distributions of absolute Walsh–Hadamard (<strong>WHT</strong>) and absolute
autocorrelation (<strong>AC</strong>) values, written as $\\{{(\\text{{value}},
\\text{{multiplicity}}), \\ldots\\}}$.</p>

<h2>In coding-theory terms</h2>
<p>Boolean functions have a natural home in coding theory. The truth tables of all functions of
degree at most $r$ form the binary <strong>Reed–Muller code</strong> $\\mathrm{{RM}}(r,n)$, and
the affine functions are exactly $\\mathrm{{RM}}(1,n)$. Collecting a function together with all
of its affine offsets gives a <em>coset</em> of $\\mathrm{{RM}}(1,n)$, and the affine equivalence
classes are the orbits of these cosets under invertible affine changes of variable — the maps
$x \\mapsto \\mathcal{{D}}x \\oplus a$ with $\\mathcal{{D}} \\in \\mathrm{{GL}}(n, \\mathrm{{GF}}(2))$.
This is the viewpoint from which J. A. Maiorana first enumerated the 150,357 classes of
$\\mathcal{{B}}_6$ in 1991.</p>
<p>The same language describes the cryptographic measures directly: the
<strong>nonlinearity</strong> of $f$ is its Hamming distance to $\\mathrm{{RM}}(1,n)$, and the
<strong>bent functions</strong> — the maximum-nonlinearity classes, which exist only for even
$n$ — attain the <strong>covering radius</strong> of $\\mathrm{{RM}}(1,n)$. More generally, the
distance from $f$ to $\\mathrm{{RM}}(r,n)$ is its $r$-th order nonlinearity.</p>

<h2>Equivalence Classes, $n = 3$</h2>
<p>The complete set of equivalence classes for $n \\le 5$ can be found by exhaustive search.
For three input variables there are <strong>3</strong> classes.</p>
{class_table(N3)}

<h2>Equivalence Classes, $n = 4$</h2>
<p>For four input variables there are <strong>8</strong> classes.</p>
{class_table(N4)}
<p>Class 8 is <strong>bent</strong>: it achieves the maximum nonlinearity $2^{{n-1}} -
2^{{n/2-1}} = 6$ and has a flat absolute Walsh spectrum.</p>

<h2>Equivalence Classes, $n = 5$</h2>
<p>For five input variables there are <strong>48</strong> classes.</p>
{class_table(N5)}
<p>The maximum nonlinearity for $n = 5$ is <strong>12</strong> (classes 45–48); no bent
functions exist for odd $n$.</p>

<h2>Equivalence Classes, $n = 6$</h2>
<p>For six input variables there are <strong>150,357</strong> equivalence classes — too many
to list individually, but completely enumerated. Of these, <strong>74,542</strong> contain
balanced functions. The table below summarises the classes by nonlinearity; within each
nonlinearity level the classes further split by algebraic order and maximum absolute
autocorrelation.</p>
{cards([("150,357", "total classes"), ("74,542", "with balanced functions"),
        ("28", "maximum nonlinearity (bent)")])}

<h3>Classes by nonlinearity</h3>
{n6_table(N6_BY_NL)}
<p>The <strong>4 bent classes</strong> at nonlinearity 28 are the maximally nonlinear
functions for $n = 6$: one of algebraic order 2 (the quadratic bent class) and three of
order 3. Together they account for over 5 billion individual bent functions.</p>

<h3>Data files</h3>
<p>The complete classification gives one representative function for every class. It is
split into one file per combination of nonlinearity, algebraic order and maximum absolute
autocorrelation $(\\text{{nl}}, \\text{{ord}}, \\text{{acmax}})$. These data files accompanied
the original site and have been used by other researchers, for example in NIST's study of
the multiplicative complexity of 6-variable Boolean functions.</p>
<ul>
<li><a href="data/n6-classes.zip"><strong>All classes</strong></a> (<code>n6-classes.zip</code>,
670 KB): 182 files, 150,357 class representatives.</li>
<li><a href="data/n6-balanced-classes.zip"><strong>Classes containing balanced functions</strong></a>
(<code>n6-balanced-classes.zip</code>, 335 KB): 94 files (<code>n6_bal_…</code>), 74,542 classes.</li>
</ul>
<p><strong>Format.</strong> Plain text, one class per line:</p>
<pre><code>class=150341; tt=0x110707FF,0xE0422107;</code></pre>
<p><code>class</code> is the class number and <code>tt</code> is the 64-bit truth table of a
representative, written as two 32-bit words. In the balanced files the classes are numbered
separately (1–74,542). Each class contains at least one balanced function, but the
representative listed is the class's usual representative and is not necessarily balanced
itself.</p>

<details>
<summary><strong>Classes by (nl, ord, acmax)</strong>: all 182 combinations</summary>
{n6_detail_table(N6_DETAIL)}
</details>

<h3>History of this data</h3>
<ul>
<li><strong>1991.</strong> Maiorana classified the cosets of the Reed–Muller code $R(1,6)$,
establishing that there are 150,357 affine equivalence classes for $n = 6$. That work, in
coding-theory terms, gives weight distributions and stabiliser orders rather than
representative functions with their cryptographic properties.</li>
<li><strong>2003.</strong> The PhD research behind this site re-enumerated all 150,357 classes
using the Theorem of Connectivity and produced, for every class, a truth-table representative
together with its nonlinearity, algebraic order and autocorrelation, identified the 74,542
classes containing balanced functions, and counted the functions in each class via a
self-mapping constant (tabulated in the thesis appendices). The data files were published on
the original <em>Boolean Planet</em> website in 2003 and described in the thesis
(December 2003).</li>
<li><strong>2018.</strong> Çalık, Sönmez Türan and Peralta computed the multiplicative complexity
of every $n = 6$ class, using these representative functions
(<a href="https://eprint.iacr.org/2018/002">ePrint 2018/002</a>).</li>
<li><strong>2026.</strong> The original files are re-released here unchanged, after
re-validation: the class totals, and the properties of a random sample of representatives
against their file names.</li>
</ul>

<h3 id="cite">How to cite</h3>
<p>If you use these data files or tables, please cite the thesis, and the archived dataset if you
used the files:</p>
<div class="callout-note"><p>J. Fuller. <em>Analysis of Affine Equivalent Boolean Functions for
Cryptography.</em> PhD thesis, Queensland University of Technology, Brisbane, Australia, 2003.
<a href="https://eprints.qut.edu.au/15828/1/Joanne_Fuller_Thesis.pdf">https://eprints.qut.edu.au/15828/</a>.</p>
<p>J. Fuller. <em>Boolean Functions for Cryptography: affine equivalence class data.</em> Zenodo,
2026. <a href="https://doi.org/10.5281/zenodo.24217283">doi:10.5281/zenodo.24217283</a>
(data first published 2003).</p></div>
<pre><code>@phdthesis{{fuller2003affine,
  author = {{Joanne Fuller}},
  title  = {{Analysis of Affine Equivalent Boolean Functions for Cryptography}},
  school = {{Queensland University of Technology}},
  address = {{Brisbane, Australia}},
  year   = {{2003}},
  url    = {{https://eprints.qut.edu.au/15828/}},
  note   = {{Data: \\url{{https://booleanfunction.github.io/equivalence-classes.html}}}}
}}

@misc{{fuller_n6_data,
  author    = {{Joanne Fuller}},
  title     = {{Boolean Functions for Cryptography: affine equivalence class data}},
  publisher = {{Zenodo}},
  year      = {{2026}},
  doi       = {{10.5281/zenodo.24217283}},
  url       = {{https://doi.org/10.5281/zenodo.24217283}},
  note      = {{Data first published 2003}}
}}</code></pre>"""
    page("equivalence-classes.html", "Affine Equivalence Classes — Boolean Functions for Cryptography",
         "Affine equivalence class tables for Boolean functions of n = 3, 4, 5 and the full n = 6 classification data (150,357 classes).",
         eq, extra=DATASET_LD)

    # Theorem of Connectivity
    conn = f"""<h1>The Theorem of Connectivity</h1>
<p>Affine equivalence groups functions that share the same cryptographic properties, but it
says nothing about how those classes sit <em>relative to one another</em>. The theorem of
connectivity supplies exactly that missing structure: it describes how a function relates to
its immediate neighbours — the functions one bit-flip away in the truth table — and shows that
this local structure is itself an invariant of the equivalence class. The result lets us view
the whole Boolean space not as a flat collection of $2^{{2^{{n}}}}$ functions but as a set of
<strong>connected equivalence classes</strong> — the cosets of $\\mathrm{{RM}}(1,n)$ under the
affine group.</p>

<h2>The 1-local neighbourhood</h2>
<p>The starting point is the immediate neighbourhood of a function: everything at Hamming
distance one from it.</p>
<div class="callout-note"><p><strong>Definition.</strong> The <em>1-local neighbourhood</em> of
a Boolean function $f \\in \\mathcal{{B}}_n$ consists of all $2^n$ functions $f_{{(i)}}$,
$i \\in \\mathbf{{Z}}_2^{{\\,n}}$, with $\\operatorname{{dist}}(f, f_{{(i)}}) = 1$. We say
$f_{{(i)}}$ is <em>connected to</em> $f$:
$$f_{{(i)}}(x) = \\begin{{cases}} f(x) & x \\neq i \\\\ f(x) \\oplus 1 & x = i. \\end{{cases}}$$</p></div>

<h2>The theorem</h2>
<p>The key result is that an affine transform maps neighbours to neighbours: if $f$ and $g$ are
affine equivalent under some transform, then every neighbour of $f$ corresponds — under that
<em>same</em> transform — to a neighbour of $g$.</p>
<div class="callout-note"><p><strong>Theorem (Connectivity).</strong> Let $f_{{(i)}}$ be defined
as above. Then for $g(x) = f(\\mathcal{{D}}x \\oplus a) \\oplus b \\cdot x \\oplus c$ there
exists a connecting function $g_{{(j)}}$ such that
$$g_{{(j)}}(x) = f_{{(i)}}(\\mathcal{{D}}x \\oplus a) \\oplus b \\cdot x \\oplus c, \\qquad
j = \\mathcal{{D}}^{{-1}}(i \\oplus a), \\qquad i = \\mathcal{{D}}j \\oplus a.$$</p></div>
<p>Because $\\mathcal{{D}}$ is non-singular this correspondence is a bijection, which gives the
property that makes connectivity useful:</p>
<div class="callout-note"><p><strong>Corollary.</strong> The 1-local neighbourhood of $g$ is a
<em>permutation</em> of the 1-local neighbourhood of $f$. Repeating the argument extends this to
any distance $m$: the $m$-local neighbourhood of $g$ is a permutation of that of $f$.</p></div>

<h2>Connectivity between classes</h2>
<p>Since neighbours are preserved, we can summarise a class by <em>which classes it connects
to</em>, and how often. Every function in a class has the same connection profile. For $n = 3$,
for instance, every single-bit change to a class-1 function yields a class-2 function; a class-2
function has one change leading back to class 1 and seven leading to class 3.</p>

<h3>Equivalence class connectivity, $n = 3$</h3>
{{conn3}}

<h3>Equivalence class connectivity, $n = 4$</h3>
{{conn4}}

<p>The $n = 5$ connectivity profile follows the same form across its 48 classes (see the
<a href="equivalence-classes.html">equivalence class tables</a> for the classes themselves).</p>

<h2>Class connection diagrams</h2>
<p>Drawing one node per class and one branch per connection turns the space into a tree.
Arranged by nonlinearity, the affine class sits at the root and the maximally nonlinear
classes — including the bent classes for even $n$ — form the topmost leaves. The branches
are sparse near the top (high-nonlinearity classes have few connections) and grow thicker
toward the root, revealing the inherent shape of the Boolean space.</p>
<div class="diagram-row">
{{tree3}}
{{tree4}}
</div>
{{legend}}
<p>For $\\mathcal{{B}}_3$ the tree is a simple chain; for $\\mathcal{{B}}_4$ it begins to
branch, with class 5 forming a leaf at nonlinearity 4 and the bent class 8 at the very top.
The diagram for the 48 classes of $\\mathcal{{B}}_5$ is far richer but follows the same
principle; only a partial, high-nonlinearity component is feasible for $\\mathcal{{B}}_6$.</p>

<h2>Why it matters</h2>
<p>The connection profile is an affine invariant, so it is a powerful tool for telling classes
apart and for navigating the space:</p>
<ul>
<li><strong>A non-exhaustive equivalence test.</strong> Two functions can be shown
<em>inequivalent</em> by comparing their connecting-class distributions — the first
distinguishing technique for Boolean functions of six or more inputs that does not require an
exhaustive search for an affine transform. For $n = 6$, comparing distributions out to a
distance of four gives complete class distinction.</li>
<li><strong>Enumerating the classes.</strong> Starting from the constant-zero function and
repeatedly examining connecting functions for new classes is guaranteed (by the theorem) to
find them all. Run for $n = 6$, this independently verified the existence of exactly
<strong>150,357</strong> equivalence classes and confirmed the set is complete.</li>
<li><strong>A map of the space.</strong> The connections form a tree-like diagram of how the
classes relate — a visual representation of the structure of $\\mathcal{{B}}_3$,
$\\mathcal{{B}}_4$ and $\\mathcal{{B}}_5$, and a partial map of $\\mathcal{{B}}_6$.</li>
</ul>
<p>The theorem of connectivity was the foundation of the PhD research from which this site
grew — the result that turns the unmanageable Boolean space into a navigable structure.</p>"""
    tree3 = svg_tree(300, 250, TREE3_NODES, TREE3_EDGES, TREE3_AXIS,
                     "Class connection diagram, n = 3",
                     "Tree of the three n=3 equivalence classes connected by single-bit changes, "
                     "arranged by nonlinearity from the affine class at the root to class 3 at the top.")
    tree4 = svg_tree(360, 410, TREE4_NODES, TREE4_EDGES, TREE4_AXIS,
                     "Class connection diagram, n = 4",
                     "Tree of the eight n=4 equivalence classes connected by single-bit changes, "
                     "arranged by nonlinearity from the affine class at the root to the bent class 8 at the top.")
    conn = (conn.replace("{conn3}", conn_table(CONN3))
                .replace("{conn4}", conn_table(CONN4))
                .replace("{tree3}", tree3)
                .replace("{tree4}", tree4)
                .replace("{legend}", DIAGRAM_LEGEND))
    page("connectivity.html", "The Theorem of Connectivity — Boolean Functions for Cryptography",
         "The theorem of connectivity: how affine equivalence classes connect through their 1-local neighbourhoods.",
         conn)

    # Efficient implementation
    ei = """<h1>Efficient Implementation</h1>

<h2>Why implementation matters</h2>
<p>Fundamental to any area of research is the ability to reproduce reported experiments, both
for verification and for advancement. Boolean function research is unusual in how much it
depends on raw computation: classifying functions, searching for good ones and computing
their properties can involve <strong>many billions of steps</strong>. Yet the cryptographic
literature has historically said little about <em>how</em> to implement these computations
efficiently, leaving each researcher to reinvent the machinery.</p>
<p>This page summarises the implementation techniques that made the exhaustive $n = 6$
classification feasible. The guiding principle is to minimise not just the <em>number</em> of
operations but the number of <em>expensive</em> operations — conditionals, multiplication,
division, modular reduction — in favour of cheap bitwise operations (XOR, AND, SHIFT).</p>

<h2>Packing truth tables into words</h2>
<p>The natural representation of a Boolean function is a full array of $2^n$ integers, one per
input. It is simple, but wasteful: a truth table or ANF needs only <strong>one bit</strong>
per entry, so a full integer array uses 32× more memory than necessary.</p>
<p>The alternative packs the output values into the full machine word. A function of $n$
variables then needs an array of</p>
<p>$$N = 2^{n} / 32 = 2^{\\,n-5}$$</p>
<p>32-bit words (for $n \\ge 5$) — a memory saving of roughly <strong>97%</strong>. Bit $i$ of
the truth table lives at bit $i \\bmod 32$ of word $\\lfloor i / 32 \\rfloor$:</p>
<pre><code>/* set bit i to 1 */   array[i &gt;&gt; 5] |=  (1 &lt;&lt; (i &amp; 31));
/* get bit i       */   ( array[i &gt;&gt; 5] &gt;&gt; (i &amp; 31) ) &amp; 1;</code></pre>
<p>The shift <code>i &gt;&gt; 5</code> replaces a division and <code>i &amp; 31</code> replaces
a modular reduction — both examples of <em>strength reduction</em>. Crucially, packing also
lets many transforms process <strong>32 outputs at once</strong>. Computing a Hamming weight,
for instance, needs only $2^{\\,n-5}$ word-level popcounts instead of $2^{n}$ single-bit
lookups.</p>

<h2>Key transforms</h2>
<p>Three transforms underpin almost all property computations. Each was implemented to operate
directly on the packed words, using precomputed lookup tables for the byte-level sub-results.</p>

<h3>Algebraic Normal Form</h3>
<p>The ANF gives the unique multilinear polynomial representation of a function over
$\\mathrm{GF}(2)$ (the functions of degree at most $r$ are exactly the Reed–Muller code
$\\mathrm{RM}(r,n)$), and from it the <strong>algebraic order</strong> and <strong>algebraic
weight</strong>. The transform is a Möbius transform over the Boolean lattice; with
byte-indexed lookup tables the four bytes of each 32-bit word can be transformed together,
then combined.</p>

<h3>Walsh–Hadamard Transform</h3>
<p>The WHT is the workhorse of nonlinearity analysis: the nonlinearity follows directly from
the maximum absolute Walsh coefficient,</p>
<p>$$\\mathrm{NL}(f) = 2^{\\,n-1} - \\tfrac{1}{2}\\,\\max_{a}\\,\\lvert W_f(a)\\rvert .$$</p>
<p>A precomputed table of the WHT of every 8-bit sub-function turns the transform into a small
number of table lookups and additions per word.</p>

<h3>Autocorrelation</h3>
<p>By the <strong>Wiener–Khinchin theorem</strong> the autocorrelation is the inverse WHT of
the power spectrum ($W_f^2$). The optimised autocorrelation routine therefore reuses the WHT
implementation directly, computing the squared spectrum and transforming back.</p>

<h2>In the modern library</h2>
<p>These same ideas carry over to 64-bit words, where an $n = 6$ function fits in a single
machine word and the per-function cost roughly halves again. A modern reimplementation of
these transforms — with the packing scheme above — is in active development and validates its
results against the classification data published on this site.</p>"""
    page("efficient-implementation.html", "Efficient Implementation — Boolean Functions for Cryptography",
         "Word-packing and Walsh–Hadamard/ANF/autocorrelation transform techniques for Boolean function research.",
         ei)

    # Publications
    pub = """<h1>Publications</h1>
<p>Publications from this research. Where a paper is freely available, a link is
given; please consult the publisher of record for the version of record.</p>

<h2>PhD thesis</h2>
<div class="entry">
<div class="ref-title">Analysis of Affine Equivalent Boolean Functions for Cryptography</div>
<div class="ref-meta">J. Fuller. PhD thesis, Information Security Research Centre, Faculty of
Information Technology, Queensland University of Technology, Brisbane, Australia, December 2003.
Freely available from QUT ePrints:
<a href="https://eprints.qut.edu.au/15828/1/Joanne_Fuller_Thesis.pdf">eprints.qut.edu.au/15828</a></div>
<div class="ref-note">The source of the results on this site: efficient algorithms for Boolean
function analysis; the complete affine equivalence classification for $n \\le 6$; the
<a href="connectivity.html">Theorem of Connectivity</a> between equivalence classes and, from it,
the first non-exhaustive test for affine equivalence and a self-mapping constant that enables
enumeration of the classes; new constructions for bent and for maximum-nonlinearity balanced
8-input functions; and linear redundancy in S-boxes.</div>
</div>

<h2>Cryptographic Boolean functions</h2>
<div class="entry">
<div class="ref-title">Efficient Algorithms for Analysis of Cryptographic Boolean Functions</div>
<div class="ref-meta">J. Fuller, W. Millan and E. Dawson. Australasian Workshop on
Combinatorial Algorithms (AWOCA), Fraser Island, Australia, 2002.</div>
<div class="ref-note">Implementation techniques for fast analysis of Boolean function
cryptographic properties — the packing and transform methods behind the exhaustive $n = 6$
classification. See <a href="efficient-implementation.html">Efficient Implementation</a>.</div>
</div>
<div class="entry">
<div class="ref-title">Evolutionary Generation of Bent Functions for Cryptography</div>
<div class="ref-meta">J. Fuller, W. Millan and E. Dawson. IEEE Congress on Evolutionary
Computation (CEC 2003), Canberra, Australia, December 2003.</div>
<div class="ref-note">Search methods that generate bent functions, analysed by the affine
equivalence classes they reach.</div>
</div>
<div class="entry">
<div class="ref-title">New Concepts in Evolutionary Search for Boolean Functions in Cryptology</div>
<div class="ref-meta">W. Millan, J. Fuller and E. Dawson. IEEE Congress on Evolutionary
Computation (CEC 2003), Canberra, Australia, December 2003.</div>
<div class="ref-note">Applies the affine equivalence class structure from the thesis, including
the self-mapping constant, to evolutionary search for cryptographic Boolean functions.</div>
</div>

<h2>Linear redundancy in the AES S-box</h2>
<div class="entry">
<div class="ref-title">On Linear Redundancy in the AES S-box</div>
<div class="ref-meta">J. Fuller and W. Millan. IACR ePrint Archive, 2002.</div>
<div class="ref-note">Analysis of linear redundancy structure in the AES substitution box.</div>
</div>
<div class="entry">
<div class="ref-title">Linear Redundancy in S-boxes</div>
<div class="ref-meta">J. Fuller and W. Millan. Fast Software Encryption (FSE), Lund, Sweden, 2003.</div>
<div class="ref-note">The peer-reviewed presentation of the linear redundancy results, showing
that the AES S-box (and others) exhibit linear redundancy — every output coordinate function
is affine-equivalent to a single function. See the <a href="sboxes.html">S-box survey</a>.</div>
</div>

<h2>Stream ciphers</h2>
<div class="entry">
<div class="ref-title">The LILI-II Keystream Generator</div>
<div class="ref-meta">A. Clark, E. Dawson, J. Fuller, J. Golić, H-J. Lee, W. Millan, S-J. Moon and
L. Simpson. Australasian Conference on Information Security and Privacy (ACISP 2002), Lecture
Notes in Computer Science 2384, pp. 25–39, Springer, 2002.</div>
</div>

<h2>Related work using this data</h2>
<div class="entry">
<div class="ref-title">The Multiplicative Complexity of 6-variable Boolean Functions</div>
<div class="ref-meta">Ç. Çalık, M. Sönmez Türan and R. Peralta. IACR ePrint 2018/002.
<a href="https://eprint.iacr.org/2018/002">eprint.iacr.org/2018/002</a></div>
<div class="ref-note">Computes the multiplicative complexity (minimum AND-gate count) of all
150,357 $n = 6$ equivalence classes — building on the classification published here. Relevant
to lightweight cryptography and NIST standardisation work.</div>
</div>

<div class="callout-note"><p>If you use the $n = 6$ classification data, please cite the PhD
thesis above (see <a href="equivalence-classes.html#cite">how to cite</a>). If you have used
the data in your own work, I'd be glad to hear about it.</p></div>"""
    page("publications.html", "Publications — Boolean Functions for Cryptography",
         "Publications on cryptographic Boolean function analysis and linear redundancy in the AES S-box.",
         pub)

    # Learning
    learn = """<h1>Learning</h1>
<p>A short, opinionated set of starting points for getting into Boolean functions for
cryptography. This list will grow.</p>

<h2>Core concepts</h2>
<p>A Boolean function $f : \\{0,1\\}^n \\to \\{0,1\\}$ is judged for cryptographic use against a
handful of properties:</p>
<ul>
<li><strong>Balance</strong> — equal numbers of zeros and ones in the truth table. A biased
function leaks information.</li>
<li><strong>Nonlinearity</strong> $\\mathrm{NL}(f)$ — the Hamming distance to the nearest
affine function; equivalently, the distance to the first-order Reed–Muller code
$\\mathrm{RM}(1,n)$. High nonlinearity resists linear approximation (linear cryptanalysis).</li>
<li><strong>Algebraic degree</strong> — the degree of the ANF; the functions of degree at most
$r$ form the Reed–Muller code $\\mathrm{RM}(r,n)$. Low degree is exploitable.</li>
<li><strong>Correlation immunity</strong> — statistical independence of the output from small
subsets of inputs; essential for combining functions in stream ciphers.</li>
<li><strong>Autocorrelation / propagation</strong> — how the function changes under input
differences; related to the strict avalanche criterion.</li>
<li><strong>Algebraic immunity</strong> — resistance to algebraic attacks (a post-2003
criterion); the minimum degree of an annihilator of $f$ or $f \\oplus 1$.</li>
</ul>
<p>These criteria interact and often conflict: improving one can worsen another. Designing a
function that is simultaneously good across all of them — and provably so — is the central
challenge.</p>

<h2>Key transforms</h2>
<ul>
<li><strong>Walsh–Hadamard transform (WHT)</strong> — the spectral tool behind nonlinearity
and correlation immunity.</li>
<li><strong>Algebraic Normal Form (ANF)</strong> — the polynomial representation behind
algebraic degree and algebraic immunity, computed via the Möbius transform.</li>
<li><strong>Autocorrelation</strong> — derived from the WHT by the Wiener–Khinchin theorem.</li>
</ul>
<p>See <a href="efficient-implementation.html">Efficient Implementation</a> for how these are
computed in practice.</p>

<h2>Foundational reading</h2>
<ul>
<li><strong>O. S. Rothaus</strong>, <em>On Bent Functions</em>, J. Combinatorial Theory (A),
1976 — the origin of bent functions and maximum nonlinearity.</li>
<li><strong>T. Siegenthaler</strong>, <em>Correlation-Immunity of Nonlinear Combining
Functions</em>, IEEE Trans. Information Theory, 1984 — introduces correlation immunity and the
trade-off with degree.</li>
<li><strong>W. Meier and O. Staffelbach</strong>, <em>Nonlinearity Criteria for Cryptographic
Functions</em>, EUROCRYPT 1989.</li>
<li><strong>N. Courtois and W. Meier</strong>, <em>Algebraic Attacks on Stream Ciphers with
Linear Feedback</em>, EUROCRYPT 2003 — introduces algebraic immunity.</li>
<li><strong>C. Carlet</strong>, <em>Boolean Functions for Cryptography and Coding Theory</em>,
Cambridge University Press — a comprehensive modern reference that, as its title signals, treats
the two fields together.</li>
<li><strong>F. J. MacWilliams and N. J. A. Sloane</strong>, <em>The Theory of Error-Correcting
Codes</em>, North-Holland, 1977 — the standard reference for Reed–Muller codes and their
covering radii.</li>
<li><strong>J. A. Maiorana</strong>, <em>A Classification of the Cosets of the Reed–Muller Code
R(1,6)</em>, Mathematics of Computation, 1991 — the coding-theory enumeration of the 150,357
affine equivalence classes for $n = 6$.</li>
</ul>

<h2>Tools</h2>
<ul>
<li>This site's <a href="equivalence-classes.html">equivalence class tables</a> — concrete
examples with full property profiles for $n \\le 6$.</li>
<li>A modern open-source library implementing these properties is in development; details will
be linked here when it is released.</li>
<li>See <a href="#resources">Resources</a> below for a curated list of openly available
papers and datasets.</li>
</ul>"""

    # Resources — curated linked bibliography
    resources = """<h1>Resources</h1>
<p>A curated, growing list of openly available papers, datasets and references for Boolean
functions in cryptography. Links point to canonical sources — author / arXiv preprints, IACR
ePrint, PubMed Central, the AMS, publisher DOIs, and official code repositories. Entries marked
<span class="res-tag">free</span> have free full text.</p>
<p class="muted">This list grows over time. If a link breaks or you have a suggestion, please get
in touch.</p>

<h2>Textbooks &amp; surveys</h2>
<ul>
<li><a href="https://arxiv.org/abs/2105.10386">R. O'Donnell, <em>Analysis of Boolean
Functions</em></a> (2014; 2021 arXiv edition) — <span class="res-tag">free</span>. The standard
modern textbook; ~500 exercises.</li>
<li><a href="https://link.springer.com/article/10.1007/s10623-015-0145-8">C. Carlet &amp;
S. Mesnager, "Four Decades of Research on Bent Functions"</a>, <em>Des. Codes Cryptogr.</em> 78
(2016) — authoritative survey of bent (maximally nonlinear) functions.</li>
<li><a href="https://arxiv.org/abs/2301.08012">M. Đurasević, D. Jakobović, L. Mariot &amp; S. Picek,
"A Survey of Metaheuristic Algorithms for the Design of Cryptographic Boolean Functions"</a> (2023) —
<span class="res-tag">free</span>. The modern search-based / heuristic design of Boolean functions.</li>
</ul>

<h2>Classification &amp; affine equivalence ($n \\le 6$)</h2>
<ul>
<li><a href="https://www.ams.org/journals/mcom/1991-57-195/S0025-5718-1991-1079017-5/">J. A.
Maiorana, "A Classification of the Cosets of the Reed–Muller Code R(1,6)"</a>, <em>Math.
Comp.</em> 57 (1991) — <span class="res-tag">free</span>. First enumeration of the 150,357 affine
equivalence classes for $n = 6$.</li>
<li><a href="https://eprint.iacr.org/2004/248">A. Braeken, Y. Borissov, S. Nikova &amp;
B. Preneel, "Classification of Boolean Functions of 6 Variables or Less…"</a> (ICALP 2005) —
<span class="res-tag">free</span>. CI / resiliency / propagation classification.</li>
<li><a href="https://arxiv.org/abs/2007.12308">X.-D. Hou, "On the Number of Affine Equivalence
Classes of Boolean Functions"</a> (2020) — <span class="res-tag">free</span>. Counting AGL(n,2)
orbits.</li>
<li><a href="https://arxiv.org/abs/1705.04507">P. Leopardi, "Classifying Bent Functions by Their
Cayley Graphs"</a> (2018) — <span class="res-tag">free</span>. Cayley-graph / extended-affine
classification of bent functions up to dimension 8 (with SageMath).</li>
<li><a href="https://arxiv.org/abs/2208.02469">V. Gillot &amp; P. Langevin, "Classification of Some
Cosets of Reed–Muller Codes"</a> (2022) — <span class="res-tag">free</span>. Classifies the
length-128 (n = 7) Reed–Muller cosets under the affine group.</li>
<li><a href="https://eprint.iacr.org/2005/025">Q.-S. Meng, M. Yang, H.-G. Zhang &amp; Y. Liu, "The
Analysis of Affinely Equivalent Boolean Functions"</a> (2005) — <span class="res-tag">free</span>.
A general algorithm to test affine equivalence and recover the transform.</li>
</ul>

<h2>Algebraic immunity &amp; algebraic attacks</h2>
<ul>
<li><a href="https://iacr.org/archive/eurocrypt2003/26560345/26560345.pdf">N. Courtois &amp;
W. Meier, "Algebraic Attacks on Stream Ciphers with Linear Feedback"</a> (EUROCRYPT 2003) —
<span class="res-tag">free</span>. Introduced algebraic attacks via low-degree multiples.</li>
<li>W. Meier, E. Pasalic &amp; C. Carlet, "Algebraic Attacks and Decomposition of Boolean
Functions" (EUROCRYPT 2004, LNCS 3027) — defines <em>algebraic immunity</em> and proves
AI(f) ≤ ⌈n/2⌉. <span class="res-note">Springer / search by title.</span></li>
<li>D. K. Dalai, K. C. Gupta &amp; S. Maitra — "Results on Algebraic Immunity…" (INDOCRYPT 2004)
and "Cryptographically Significant Boolean Functions: Construction &amp; Analysis in Terms of
Algebraic Immunity" (FSE 2005). <span class="res-note">Springer / search by title.</span></li>
<li><a href="https://arxiv.org/abs/2510.01720">P. Sarkar, "Constructions of Efficiently Implementable
Boolean Functions with Provable Nonlinearity/Resiliency/Algebraic Immunity Trade-Offs"</a> (2025) —
<span class="res-tag">free</span>. A general framework for functions with provable NL / resiliency /
AI trade-offs.</li>
</ul>

<h2>Multiplicative complexity &amp; datasets</h2>
<ul>
<li><a href="https://eprint.iacr.org/2018/002">Ç. Çalık, M. Sönmez Türan &amp; R. Peralta, "The
Multiplicative Complexity of 6-variable Boolean Functions"</a> (2018) — <span class="res-tag">free</span>
(also <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC7802510/">open access via PMC</a>).
Multiplicative complexity for all 150,357 $n = 6$ classes.</li>
<li><a href="https://doi.org/10.1007/s12095-015-0150-9">J. Boyar, M. G. Find &amp; R. Peralta,
"On Various Nonlinearity Measures for Boolean Functions"</a>, <em>Cryptogr. Commun.</em> 8 (2016)
— six affine-invariant measures (free author manuscript via PubMed Central).</li>
<li><a href="https://github.com/usnistgov/Circuits">NIST — minimal-multiplication circuits for
6-variable predicates</a> — <span class="res-tag">free</span>. One representative + a minimal-AND
circuit per $n = 6$ class.</li>
</ul>

<h2>Higher-order nonlinearity &amp; covering radius</h2>
<ul>
<li><a href="https://arxiv.org/abs/1809.04864">"The Covering Radius of the Reed–Muller Code
RM(2,7) is 40"</a> — <span class="res-tag">free</span>. Settles the maximum second-order
nonlinearity for $n = 7$.</li>
<li><a href="https://arxiv.org/abs/1510.08535">"On the Covering Radius of the Second-Order
Reed–Muller Code of Length 128"</a> — <span class="res-tag">free</span>. Related
second-order-nonlinearity / covering-radius work.</li>
</ul>

<h2>Foundational classics</h2>
<p class="muted">Origin papers — widely cited; not all are freely online (check a library or the
publisher).</p>
<ul>
<li>O. S. Rothaus, "On Bent Functions," <em>J. Combinatorial Theory A</em> 20 (1976) — defines
bent functions.</li>
<li>T. Siegenthaler, "Correlation-Immunity of Nonlinear Combining Functions for Cryptographic
Applications," <em>IEEE Trans. Inf. Theory</em> (1984) — correlation immunity and the degree
trade-off.</li>
<li>W. Meier &amp; O. Staffelbach, "Nonlinearity Criteria for Cryptographic Functions"
(EUROCRYPT 1989).</li>
</ul>"""
    # Learning + Resources merged into one page (2026-11-14); resources.html now redirects.
    res_section = (resources.replace("<h2>", "<h3>").replace("</h2>", "</h3>")
                   .replace("<h1>Resources</h1>", '<h2 id="resources">Resources: papers and datasets</h2>'))
    page("learning.html", "Learning — Boolean Functions for Cryptography",
         "Concepts, foundational reading, and a curated list of openly available papers and datasets for Boolean functions in cryptography.",
         learn + "\n\n" + res_section)
    page("resources.html", "Resources — Boolean Functions for Cryptography",
         "The resources list has moved to the Learning page.",
         '<h1>Resources</h1><p>This list has moved to the '
         '<a href="learning.html#resources">Learning page</a>.</p>',
         extra='<meta http-equiv="refresh" content="0; url=learning.html#resources">\n'
               '<meta name="robots" content="noindex">\n')

    # Records — best-known functions
    records = """<h1>Records: Best-Known Functions</h1>
<p>Best-known cryptographic Boolean functions for given parameters, with the work that first
reported each result. Organised by <em>objective</em> — because the criteria trade off
(Siegenthaler's bound, the nonlinearity–algebraic-immunity tension, …), "best" is only meaningful
once the optimised property and the fixed constraints are specified.</p>
<div class="callout-note"><p><strong>Work in progress — corrections welcome.</strong> This is a
best-effort community record and may be incomplete or out of date. If you know a stronger result, a
missing entry, or a correction to a first attribution, please <a href="index.html">get in
touch</a>. Entries without a link cite the publication of record; <strong>★</strong> marks an open
target.</p></div>

<h2>Maximum nonlinearity</h2>
<p>For even $n$ the maximum over all functions is the bent value $2^{n-1}-2^{n/2-1}$. Balanced
functions cannot be bent, so their record is lower.</p>
<div class="table-scroll"><table>
<thead><tr><th class="num">n</th><th>all functions</th><th>balanced</th><th>first reference</th></tr></thead>
<tbody>
<tr><td class="num">4</td><td>6 (bent)</td><td>4</td><td>Rothaus (1976); exhaustive</td></tr>
<tr><td class="num">5</td><td>12</td><td>12</td><td>classical — covering radius of RM(1,5)</td></tr>
<tr><td class="num">6</td><td>28 (bent)</td><td>26</td><td>Rothaus (1976); balanced via the <a href="equivalence-classes.html">n=6 classification</a></td></tr>
<tr><td class="num">7</td><td>56</td><td>56</td><td>classical — covering radius of RM(1,7)</td></tr>
<tr><td class="num">8</td><td>120 (bent)</td><td>116 <span class="res-note">(best known)</span></td><td>Rothaus (1976); balanced: Stănică–Maitra–Clark (2004)</td></tr>
</tbody></table></div>
<p class="muted">Maximum nonlinearity for odd $n \\ge 9$ is open (best-known values exceed the
bent-concatenation bound).</p>

<h2>Algebraic immunity</h2>
<p>The maximum possible algebraic immunity is $\\lceil n/2 \\rceil$ (Meier–Pasalic–Carlet, 2004).
The meaningful record is the best nonlinearity attainable <em>together with</em> optimal AI.</p>
<div class="table-scroll"><table>
<thead><tr><th class="num">n</th><th class="num">optimal AI</th><th>best balanced NL at optimal AI</th><th>status / reference</th></tr></thead>
<tbody>
<tr><td class="num">6</td><td class="num">3</td><td>26</td><td>balanced NL=26, AI=3 attained — <a href="equivalence-classes.html">n=6 classification</a></td></tr>
<tr><td class="num">8</td><td class="num">4</td><td>&lt; 116</td><td><strong>★ OPEN — balanced NL=116 with AI=4 is not known</strong></td></tr>
</tbody></table></div>

<h2>Affine equivalence class counts</h2>
<div class="table-scroll"><table>
<thead><tr><th class="num">n</th><th class="num">affine classes</th><th class="num">with balanced functions</th><th>first reference</th></tr></thead>
<tbody>
<tr><td class="num">3</td><td class="num">3</td><td class="num">—</td><td>exhaustive (classical)</td></tr>
<tr><td class="num">4</td><td class="num">8</td><td class="num">—</td><td>exhaustive (classical)</td></tr>
<tr><td class="num">5</td><td class="num">48</td><td class="num">—</td><td>Berlekamp–Welch (1972)</td></tr>
<tr><td class="num">6</td><td class="num">150,357</td><td class="num">74,542</td><td><a href="https://www.ams.org/journals/mcom/1991-57-195/S0025-5718-1991-1079017-5/">Maiorana (1991)</a>; Fuller (2003); Braeken et al. (2005)</td></tr>
</tbody></table></div>
<p class="muted">A complete affine-equivalence classification for $n = 7$ is open.</p>

<h2>Bent functions (even $n$)</h2>
<div class="table-scroll"><table>
<thead><tr><th class="num">n</th><th class="num">bent NL</th><th>number of bent functions</th><th>reference</th></tr></thead>
<tbody>
<tr><td class="num">4</td><td class="num">6</td><td>896</td><td>classical</td></tr>
<tr><td class="num">6</td><td class="num">28</td><td>5,425,430,528</td><td>classical; 4 affine classes (<a href="equivalence-classes.html">this site</a>)</td></tr>
<tr><td class="num">8</td><td class="num">120</td><td>enumerated</td><td>Langevin &amp; Leander (2008)</td></tr>
</tbody></table></div>

<h2>Second-order nonlinearity (covering radius of RM(2,n))</h2>
<div class="table-scroll"><table>
<thead><tr><th class="num">n</th><th class="num">max NL₂</th><th>reference</th></tr></thead>
<tbody>
<tr><td class="num">6</td><td class="num">18</td><td>Schatz (1981)</td></tr>
<tr><td class="num">7</td><td class="num">40</td><td><a href="https://arxiv.org/abs/1809.04864">Gao et al. (2019)</a></td></tr>
</tbody></table></div>

<h2>Multiplicative complexity ($n = 6$)</h2>
<p>Every 6-variable Boolean function can be implemented with at most <strong>6 AND gates</strong>;
the multiplicative complexity of all 150,357 affine classes is known
(<a href="https://eprint.iacr.org/2018/002">Çalık, Sönmez Türan &amp; Peralta, 2018</a>).</p>

<h2>★ Open targets</h2>
<ul>
<li><strong>$n = 8$, balanced, NL = 116 <em>and</em> AI = 4.</strong> NL=116 balanced functions are
known (Stănică–Maitra–Clark, 2004) and AI = 4 is the optimum, but no function is known to achieve
both.</li>
<li>Maximum nonlinearity of functions for $n \\ge 9$.</li>
<li>A complete affine-equivalence classification for $n = 7$.</li>
</ul>"""
    page("records.html", "Records: Best-Known Functions — Boolean Functions for Cryptography",
         "Best-known cryptographic Boolean functions by criterion, with first-discovery references.",
         records)

    # S-box survey
    sb = f"""<h1>S-boxes and Linear Redundancy</h1>
<p>An S-box (substitution box) maps $n$ input bits to $m$ output bits and is the main source of
nonlinearity in most block ciphers. A bijective $n \\times n$ S-box can be viewed as $n$ Boolean
functions $b_0, \\ldots, b_{{n-1}}$, one per output bit, together with all $2^n - 1$ of their XOR
combinations $b_\\alpha$. These <em>component functions</em> determine the S-box's resistance to
linear and differential cryptanalysis.</p>

<h2>Linear redundancy</h2>
<p>The PhD research proposed a new S-box criterion: an S-box has <strong>linear redundancy</strong> if
two of its component functions are <a href="equivalence-classes.html">affine equivalent</a>,
that is, one output is just another output with its inputs linearly transformed. For random
S-boxes this essentially never happens: in 10,000 random bijective S-boxes of size $7 \\times 7$
and $8 \\times 8$, <em>none</em> had any linear redundancy. Its presence is therefore a clear sign of
non-random structure.</p>

<h2>The AES S-box</h2>
<p>The AES S-box (inversion in $\\mathrm{{GF}}(2^8)$ followed by an affine map) has excellent
nonlinearity, degree and autocorrelation. Using the equivalence test built on the
<a href="connectivity.html">Theorem of Connectivity</a>, Fuller and Millan (2002) showed that
<strong>all 255 component functions of the AES S-box are affine equivalent</strong>: the AES S-box
has <em>complete</em> linear redundancy. The search for each mapping was cut to about $2^{{15}}$
candidates, and exactly eight distinct linear transforms relate any pair. For example, output bit
1 is output bit 0 with its inputs transformed by a fixed matrix,
$b_1(x) = b_0(D_{{01}}\\,x)$, with</p>
<p>$$D_{{01}} = \\begin{{pmatrix}}
1&0&1&1&0&0&1&0\\\\ 0&1&0&1&0&1&1&0\\\\ 0&0&0&1&0&0&1&0\\\\ 1&0&0&1&1&0&0&0\\\\
0&1&0&1&1&1&0&0\\\\ 1&0&0&0&1&1&1&0\\\\ 1&1&0&1&0&0&0&0\\\\ 1&0&0&0&1&1&0&1
\\end{{pmatrix}}$$</p>
<p>(with $x = (x_1, \\ldots, x_8)^T$ and $x_8$ the least significant bit). As the thesis records,
following this result Biham, Wagner, and Youssef and Tavares (2002) showed that
<em>every</em> S-box based on finite field inversion or power maps has complete linear redundancy,
and the surrounding affine maps do not remove it.</p>

<div class="aes-demo">
<p><strong>Check it yourself.</strong> This builds the AES S-box in your browser from its definition,
analyses all 255 component functions, and tests the mapping above on every input.</p>
<p><button type="button" id="aes-run" class="gx-primary">Run the check on AES</button>
<button type="button" id="aes-random">Compare a random S-box</button></p>
<div id="aes-out" aria-live="polite"></div>
<div id="aes-rand-out" aria-live="polite"></div>
</div>

<h2>Removing it</h2>
<p>Can the redundancy be removed without giving up too much strength? The thesis gave
<em>tweaking</em> algorithms that repeatedly swap S-box outputs: a two-step version, and a four-step
version that keeps the self-inverse property of inversion S-boxes and creates no fixed points.
Applied to finite field S-boxes, they produced bijective $8 \\times 8$ S-boxes <strong>without
linear redundancy</strong> with nonlinearity 108, degree 7 and maximum autocorrelation 56. The
best such S-box previously in use, from the original Hierocrypt specification, had 106, 6 and 72.</p>
<p>The security impact of linear redundancy is still not fully understood. The thesis suggested
avenues for cryptanalysis (reduced-round distinguishers, the algebraic representation of
Rijndael, the key schedule's use of the S-box) and recommended S-boxes without linear redundancy
until the implications are known.</p>

<h2>Survey of cipher S-boxes</h2>
<p>An $m \\times k$ S-box has $k$ output coordinates, each a Boolean function of $m$ inputs.
The table below summarises, for a range of well-known cipher S-boxes, how many distinct
<a href="equivalence-classes.html">affine equivalence classes</a> those coordinate functions
fall into and the range of their nonlinearity. It does this both for the individual coordinate
functions and for all non-zero XOR combinations of them (for an 8 × 8 S-box, the 255 non-zero
linear combinations of the outputs).</p>
<p>When every function falls into a <strong>single class</strong>, the S-box has
<strong>linear redundancy</strong>: each output can be obtained from any other by an affine
transformation. The AES S-box, built by inversion in a finite field, is the standout example.
See the papers on linear redundancy on the <a href="publications.html">Publications</a> page.</p>

{sbox_table(SBOXES)}

<div class="callout-note"><p>Notes from the original survey: the Rijndael (AES) S-box functions
are also affine-equivalent to those of the Camellia S-boxes (the same primitive polynomial is
used to construct each), and to those of the Square S-box. "n/a" marks S-boxes with more
outputs than inputs, where the XOR-combination analysis was not carried out.</p></div>"""
    page("sboxes.html", "S-boxes and Linear Redundancy — Boolean Functions for Cryptography",
         "Linear redundancy in S-boxes: all 255 component functions of the AES S-box are affine equivalent (with an in-browser check), how to remove it, and a survey of cipher S-boxes.",
         sb, extra='<script src="aes.js" defer></script>\n')

    # Basics: worked example with the 3-input majority function
    n = 3
    maj = sum(1 << i for i in range(8) if bin(i).count("1") >= 2)
    M = bf_analyse(maj, n)
    lin = lambda w: " \\oplus ".join(f"x_{k + 1}" for k in range(n) if (w >> k) & 1) or "0"
    tt_rows = [(i, vec(i, n), M["bits"][i], M["anf"][i]) for i in range(8)]
    wht_rows = [(vec(w, n), f"${lin(w)}$", M["wht"][w]) for w in range(8)]
    ac_rows = [(vec(s, n), M["ac"][s]) for s in range(8)]
    bent_tt = sum(1 << i for i in range(16) if (((i & 1) and (i >> 1) & 1) ^ (((i >> 2) & 1) and (i >> 3) & 1)))
    B = bf_analyse(bent_tt, 4)
    maxw = max(map(abs, M["wht"]))
    basics = f"""<h1>Boolean Functions: The Basics</h1>
<p>This page builds up the main cryptographic measures of a Boolean function step by step, using
one small example throughout: the <strong>majority function</strong> on three inputs, which
outputs 1 when at least two of its inputs are 1. Every number here is computed directly from
the definitions.</p>

<h2>1. Truth table</h2>
<p>A Boolean function of $n$ inputs is a map $f: \\{{0,1\\}}^n \\to \\{{0,1\\}}$. The most direct
description is its <strong>truth table</strong>: the output for each of the $2^n$ inputs. We
number the inputs $x = (x_1, x_2, x_3)$ by $i = x_1 + 2x_2 + 4x_3$. Reading the outputs as bits
$f(0), f(1), \\ldots$ (least significant first) gives the hexadecimal form used on this site:
majority is <code>0x{maj:02x}</code>.</p>
{simple_table(["i", "x = (x₁,x₂,x₃)", "f(x)", "ANF coefficient"], tt_rows, num_cols=(0, 2, 3))}
<p>The <strong>Hamming weight</strong> is the number of 1s: here {M["weight"]} of 8, so the function is
<strong>balanced</strong> (equally many 0s and 1s), which is essential for most cryptographic uses:
an unbalanced output leaks a statistical bias.</p>

<h2>2. Algebraic normal form and degree</h2>
<p>Every Boolean function can be written uniquely as an XOR of AND-terms, its <strong>algebraic
normal form</strong> (ANF). The coefficients (last column above) come from the truth table by the
binary Möbius transform. For majority:</p>
<p>$$f(x) = {M["anf_str"]}.$$</p>
<p>The <strong>algebraic degree</strong> (or order) is the size of the largest term: here
<strong>{M["degree"]}</strong>. Degree 1 functions are <em>affine</em> (linear plus a constant) and offer
no security; higher degree resists algebraic attacks.</p>

<h2>3. Walsh–Hadamard transform</h2>
<p>The Walsh–Hadamard transform measures how strongly $f$ correlates with each linear function
$\\omega \\cdot x$:</p>
<p>$$\\hat F(\\omega) = \\sum_{{x}} (-1)^{{f(x) \\oplus \\omega \\cdot x}}.$$</p>
<p>A value of 0 means no correlation; $\\pm 2^n$ means $f$ equals that linear function (or its
complement).</p>
{simple_table(["ω", "linear function ω·x", "F̂(ω)"], wht_rows, num_cols=(2,))}

<h2>4. Nonlinearity</h2>
<p>The <strong>nonlinearity</strong> is the Hamming distance from $f$ to the nearest affine function,
and it comes straight from the largest Walsh value:</p>
<p>$$\\mathrm{{NL}}(f) = 2^{{n-1}} - \\tfrac12 \\max_\\omega |\\hat F(\\omega)| = 4 - \\tfrac12 \\cdot {maxw} = {M["nl"]}.$$</p>
<p>High nonlinearity defends against <em>linear cryptanalysis</em>, which exploits correlation with
linear functions. For $n = 3$, {M["nl"]} is the largest nonlinearity possible, so majority is as good
as a 3-input function gets.</p>
<p>For even $n$ the maximum, $2^{{n-1}} - 2^{{n/2-1}}$, is reached by <strong>bent functions</strong>, whose
Walsh values all have the same magnitude $2^{{n/2}}$. The classic example for $n = 4$ is
$x_1x_2 \\oplus x_3x_4$ (<code>0x{bent_tt:04x}</code>): every $|\\hat F(\\omega)| = {abs(B["wht"][0])}$, and its
nonlinearity is {B["nl"]}. Bent functions are never balanced, which is why balanced functions
of high nonlinearity are a central research problem (see <a href="records.html">Records</a>).</p>

<h2>5. Autocorrelation</h2>
<p>The <strong>autocorrelation</strong> measures how $f$ changes when the input is shifted by $s$:</p>
<p>$$\\hat r(s) = \\sum_x (-1)^{{f(x) \\oplus f(x \\oplus s)}}.$$</p>
{simple_table(["shift s", "r̂(s)"], ac_rows, num_cols=(1,))}
<p>$\\hat r(0) = 2^n$ always. Large values for $s \\ne 0$ indicate predictable behaviour under
input differences, the weakness exploited by <em>differential cryptanalysis</em>. The largest
magnitude over $s \\ne 0$ is the <strong>absolute indicator</strong> (the <em>acmax</em> used in this
site's tables); for majority it is {max(abs(v) for v in M["ac"][1:])}, the worst possible. Flipping
all three inputs always flips the output ($\\hat r(1,1,1) = {M["ac"][7]}$), a so-called <em>linear
structure</em>. So majority is optimal for nonlinearity but weak here: good functions must balance
several criteria at once, which is what makes their design hard.</p>

<h2>6. Affine equivalence</h2>
<p>Changing variables affinely, adding an affine function, or complementing the output,
$g(x) = f(Dx \\oplus a) \\oplus b \\cdot x \\oplus c$, preserves nonlinearity, degree (above 1) and the
absolute Walsh and autocorrelation distributions. So functions fall into <strong>equivalence
classes</strong> that share these properties. For $n = 3$ there are only three classes, and
majority belongs to class 3, the class of maximum nonlinearity. Instead of studying all
$2^{{2^n}}$ functions, one representative per class suffices: see the
<a href="equivalence-classes.html">equivalence class tables</a>, and
<a href="class-sizes.html">how big each class is</a>.</p>
<p>Note that Hamming weight is <em>not</em> preserved (adding $b \\cdot x$ changes it), so a class can
contain both balanced and unbalanced functions.</p>

<h2>Where next</h2>
<ul>
<li><a href="efficient-implementation.html">Efficient Implementation</a>: computing these
transforms fast, with word packing.</li>
<li><a href="connectivity.html">The Theorem of Connectivity</a>: how the classes link
together.</li>
<li><a href="learning.html">Learning</a>: books and courses for going further.</li>
</ul>"""
    page("basics.html", "Boolean Functions: The Basics — Boolean Functions for Cryptography",
         "A worked introduction to cryptographic Boolean functions: truth table, ANF, degree, Walsh–Hadamard transform, nonlinearity, bent functions, autocorrelation and affine equivalence.",
         basics)

    # Class Graph Explorer (interactive)
    gdata = {3: class_graph(N3, 3, SIZES34[3]), 4: class_graph(N4, 4, SIZES34[4]),
             5: class_graph(N5, 5, {r[0]: r[3] for r in SELF5})}
    gjson = __import__("json").dumps(gdata, separators=(",", ":"))
    explore = f"""<h1>Class Graph Explorer</h1>
<p>Every Boolean function belongs to an affine equivalence class, and changing a single bit of
its truth table moves it to a neighbouring class. By the
<a href="connectivity.html">Theorem of Connectivity</a>, every function in a class has the same
neighbours, in the same proportions, so the classes form a graph. Here it is for
$n = 3$, $4$ and $5$, layered by nonlinearity from the affine class at the bottom to the most
nonlinear classes at the top.</p>

<div class="gx-controls">
  <div class="gx-seg" role="group" aria-label="Number of input variables">
    <button type="button" data-n="3" aria-pressed="false">n = 3</button>
    <button type="button" data-n="4" aria-pressed="false">n = 4</button>
    <button type="button" data-n="5" aria-pressed="true">n = 5</button>
  </div>
  <label>Colour by
    <select id="gx-colour">
      <option value="deg">algebraic degree</option>
      <option value="ac">absolute indicator (acmax)</option>
      <option value="bal">contains balanced functions</option>
    </select>
  </label>
  <label>Climb from
    <select id="gx-start">
      <option value="affine">an affine function (bottom)</option>
      <option value="random">a random function</option>
    </select>
  </label>
  <button type="button" id="gx-climb" class="gx-primary">▶ Watch a hill climb</button>
  <button type="button" id="gx-reset">Reset</button>
</div>

<div class="gx-wrap">
  <div class="gx-canvas">
    <svg id="gx-svg" role="img" aria-label="Class connection graph"></svg>
    <div id="gx-legend" class="gx-legend"></div>
  </div>
  <aside id="gx-info" class="gx-info" aria-live="polite"></aside>
</div>
<ol id="gx-log" class="gx-log" aria-live="polite"></ol>

<h2>Reading the graph</h2>
<ul>
<li><strong>Height</strong> is nonlinearity; <strong>circle size</strong> is the number of
functions in the class (log scale), from the <a href="class-sizes.html">self-mapping
constant</a>. Almost all functions live in a few large classes near the top-middle.</li>
<li><strong>Lines</strong> join classes that are one bit apart. The panel lists, for the selected
class, where each of the $2^n$ possible single-bit changes leads. ▲ means up in nonlinearity.</li>
<li><strong>Hill climb</strong> starts from a random function and repeatedly makes the single-bit
change that most increases nonlinearity, the simplest version of the heuristic searches used to
find cryptographically strong functions. Run it a few times on $n = 5$: some climbs reach the
top, others stall at a <em>local maximum</em>.</li>
</ul>
<div class="callout-note"><p>The graphs are computed exactly from the class representatives on the
<a href="equivalence-classes.html">class tables</a>: for $n \\le 5$ the absolute Walsh and
autocorrelation distributions together identify a class uniquely. They reproduce Figures 4.1–4.3
of the <a href="https://eprints.qut.edu.au/15828/">PhD thesis</a> (2003), with the layout
re-ordered to reduce crossings.</p></div>
<script type="application/json" id="graph-data">{gjson}</script>
<script src="explorer.js" defer></script>"""
    page("explore.html", "Class Graph Explorer — Boolean Functions for Cryptography",
         "Interactive explorer of the affine equivalence class connection graphs for Boolean functions with n = 3, 4 and 5 inputs, with a hill-climbing animation.",
         explore)

    # Constructions and search history
    import urllib.parse as _up

    def tt_link(words):
        return (f'<a href="analyse.html?tt={_up.quote(words)}" title="Open in the Function Analyser">'
                f"<code>{words.replace(',', ', ')}</code></a>")
    rb = [(n, nl, o, a) for n, nl, o, a in RANDOM_BALANCED]
    bs = [(n, mo, b, f"{ms:g}") for n, mo, _, _, b, _, ms in BENT_SURVEY]
    lbrows = [tuple("–" if v is None else v for v in r) for r in BENT_CLASS_LB]
    b8 = [(c, o, tt_link(w)) for c, o, w in BENT8_CLASSES]
    dh = [r for r in DHC_N8 if any(r[1:])]
    avg = lambda col: sum(r[0] * r[col] for r in DHC_N8) / sum(r[col] for r in DHC_N8)
    e116 = [(c, a, tt_link(w)) for c, a, w in EX_8_1_6_116]
    cons = f"""<h1>Constructions and Search</h1>
<p>Recognising a good Boolean function is easy; <em>finding</em> one is hard. There are
$2^{{2^n}}$ functions of $n$ inputs, and the cryptographically strong ones are a vanishingly small
fraction. This page describes the two construction methods developed in the PhD research
(Chapter 5 of the <a href="https://eprints.qut.edu.au/15828/">thesis</a>), the picture of the
"Boolean terrain" that motivated them, and the history of heuristic search at QUT.
Every example function below links to the <a href="analyse.html">Function Analyser</a>, so
you can check it yourself.</p>

<h2>Why random search fails</h2>
<p>A million random balanced functions were generated for each $n$. On average they fall far short
of the best known values: for $n = 8$, the average nonlinearity is 103.5, against a best known 116.</p>
<details><summary><strong>Average properties of random balanced functions</strong> ($10^6$ samples per $n$)</summary>
{simple_table(["n", "average nonlinearity", "average degree", "average acmax"], rb, num_cols=(0, 1, 2, 3))}
</details>

<h2>1. A new construction of bent functions</h2>
<p>Bent functions have the maximum possible nonlinearity for even $n$. The construction rests on a
simple property proved in the thesis: split a function's truth table into two halves along any
non-zero direction $\\omega$. Then</p>
<p style="text-align:center"><em>a function is bent if and only if, in every non-zero direction,
exactly one of the two halves is balanced.</em></p>
<p>Together with the bound $\\deg f \\le n/2$ for bent functions, this gives a fast filter:</p>
<ol>
<li>Start from a quadratic bent function, $x_1x_{{n/2+1}} \\oplus x_2x_{{n/2+2}} \\oplus \\cdots$.</li>
<li>Try adding ANF terms of degree 3 up to a chosen maximum (at most $n/2$), starting from a random
position.</li>
<li>Discard any term that breaks the weight or "half balanced" conditions in the $n$ unit
directions, which is cheap to test. Only the survivors need a full Walsh transform.</li>
<li>Keep the term if the result is still bent, and repeat to build a chain of bent functions of
increasing degree.</li>
</ol>
<p>On a 500 MHz Pentium III in 2003 this produced bent functions for $n = 8$ to $16$, at speeds from
under a millisecond to about 4 seconds per function.</p>
<details><summary><strong>Construction results</strong> (bent functions produced per run)</summary>
{simple_table(["n", "max degree", "bent functions", "ms per function"], bs, num_cols=(0, 1, 2, 3))}
</details>
<h3>How many classes does it reach?</h3>
<p>A construction is only as useful as the variety it produces: any one function generates its whole
affine class, so the real measure is how many <em>classes</em> a method reaches. The thesis
classified the output by affine equivalence, giving lower bounds on the number of bent classes.
For comparison, $n = 6$ has exactly 4.</p>
{simple_table(["n", "degree 2", "3", "4", "5", "6", "7", "total classes found"], lbrows, num_cols=tuple(range(8)))}
<details><summary><strong>The 14 bent classes found for $n = 8$</strong>, with example functions</summary>
{simple_table(["class", "degree", "example (8 × 32-bit words)"], b8, num_cols=(0, 1))}
</details>
<p class="fa-muted">These were the counts reached in 2003; they are lower bounds, not complete
classifications.</p>

<h2>2. The Boolean terrain</h2>
<p>Hill climbing improves a function by small truth-table changes. Changing one bit moves every Walsh
value by $\\pm 2$; changing two bits (one 0 and one 1, so the weight is unchanged) moves each by
$-4$, $0$ or $+4$, so nonlinearity rises by 2, stays level, or falls by 2. For each function, the
possible two-bit changes therefore split into an <strong>improvement set</strong>, a
<strong>static set</strong> and a <strong>reduction set</strong>. Which sets are non-empty describes
the local shape of the landscape:</p>
{simple_table(["shape", "improvement", "static", "reduction"], [("peak", "–", "–", "✓"), ("plateau", "–", "✓", "–"), ("ridge", "–", "✓", "✓"), ("trough", "✓", "–", "–"), ("saddle point", "✓", "–", "✓"), ("valley", "✓", "✓", "–"), ("slope", "✓", "✓", "✓")])}
<p>Surveys of this terrain for $n = 4$, $5$ and $6$, and of the functions met during searches at
$n = 8$, show that most functions sit on <em>slopes</em>, but as
nonlinearity rises the improvement set shrinks to nothing and highly nonlinear functions sit on
<strong>ridges</strong>. That is exactly where ordinary hill climbing stops.</p>

<h2>3. Dynamic hill climbing</h2>
<p><em>Strong</em> hill climbing (Millan, Clark and Dawson, 1997) only accepts improving moves, so it
halts at the first ridge. <em>Weak</em> hill climbing (1999) also accepts level moves, but rarely
finds the few improving ones. <strong>Dynamic hill climbing</strong> switches between the two: it
takes an improving move whenever one exists, and otherwise walks along the ridge with level moves
(up to a limit), checking for a new improving move at every step.</p>
<p>For balanced functions of 8 inputs, over 1,000 runs of each method:</p>
{simple_table(["nonlinearity", "random", "strong HC", "weak HC", "dynamic HC"], dh, num_cols=(0, 1, 2, 3, 4))}
<p>Average final nonlinearity (computed from the table): random {avg(1):.1f}, strong
{avg(2):.1f}, weak {avg(3):.1f}, <strong>dynamic {avg(4):.1f}</strong>. Only dynamic hill climbing
reached 114 and 116, and it reached 116, the best known for balanced 8-input functions, in
<strong>374 of 1,000 runs</strong>.</p>
<p>Every nonlinearity-116 function found sat at an isolated <strong>peak</strong>: no two-bit change
kept it at 116. The thesis noted that if this holds for all such functions, then balanced functions
with nonlinearity 118 cannot exist. Whether they do remains an
<a href="records.html">open problem</a>.</p>
<p>Classifying the output found <strong>4,797 distinct classes</strong> of balanced nonlinearity-116
functions. A modified version that preserves correlation immunity produced 1-resilient
(8, 1, 6, 116) functions; ten example classes are below. The same approach, combined with
concatenation, gave a 12-input 1-resilient function of degree 10 and nonlinearity 1,992, the best
known at the time (since improved).</p>
<details><summary><strong>Ten (8, 1, 6, 116) classes</strong>: balanced, 1-resilient, degree 6, nonlinearity 116</summary>
{simple_table(["class", "acmax", "example (8 × 32-bit words)"], e116, num_cols=(0, 1))}
</details>

<h2>A short history of heuristic search at QUT</h2>
<p>The Information Security Research Centre at QUT was an early centre for heuristic design of
cryptographic Boolean functions:</p>
<ul class="timeline">
<li><strong>1997.</strong> W. Millan, A. Clark and E. Dawson introduce hill climbing
("Smart Hill Climbing Finds Better Boolean Functions", SAC 1997) and a genetic algorithm
("An Effective Genetic Algorithm for Finding Highly Nonlinear Boolean Functions", ICICS 1997) for
cryptographic Boolean functions. PhD theses by Millan (1997) and Clark (1998) follow.</li>
<li><strong>1998–1999.</strong> Heuristic design of balanced functions (Eurocrypt 1998) and weak hill
climbing (ACISP 1999), from the same group.</li>
<li><strong>2000.</strong> J. A. Clark and J. L. Jacob introduce simulated annealing for Boolean
function design (ACISP 2000).</li>
<li><strong>2002.</strong> Efficient algorithms for Boolean function analysis (Fuller, Millan and
Dawson, AWOCA 2002): the fast transforms that made large-scale searches and the exhaustive
$n = 6$ classification practical. See <a href="efficient-implementation.html">Efficient
Implementation</a>.</li>
<li><strong>2003.</strong> "Evolutionary Generation of Bent Functions for Cryptography" (Fuller, Millan
and Dawson) and "New Concepts in Evolutionary Search for Boolean Functions in Cryptology" (Millan,
Fuller and Dawson), both at the IEEE Congress on Evolutionary Computation. The PhD thesis
(December 2003) presents the bent construction, the terrain classification and dynamic hill
climbing above, and analyses the output of each construction by affine equivalence class.</li>
</ul>
<p>Try a simple version yourself: the <a href="explore.html">Class Graph Explorer</a> animates a
hill climb through the classes for $n \\le 5$.</p>"""
    page("constructions.html", "Constructions and Search — Boolean Functions for Cryptography",
         "A bent function construction, the Boolean terrain, dynamic hill climbing for balanced 8-input functions of nonlinearity 116, and the history of heuristic search at QUT.",
         cons)

    # Function Analyser (interactive)
    fa_data = {
        "keys": {n: g["keys"] for n, g in gdata.items()},
        "classes": {n: {nd["id"]: {"hex": nd["hex"], "size": nd["size"]} for nd in g["nodes"]}
                    for n, g in gdata.items()},
        "count": {n: len(g["nodes"]) for n, g in gdata.items()},
        "n6": {f"{nl},{o},{a}": c for nl, o, a, c, _ in N6_DETAIL},
    }
    fa = f"""<h1>Function Analyser</h1>
<p>Paste the truth table of any Boolean function with up to 10 inputs to see its
cryptographic properties, all computed in your browser from the definitions on the
<a href="basics.html">Basics</a> page. For $n \\le 5$ it also tells you exactly which
<a href="equivalence-classes.html">affine equivalence class</a> the function belongs to, and
for $n = 6$ which of the original classification data files contains its class.</p>

<div class="fa-box">
  <label for="fa-input">Truth table</label>
  <textarea id="fa-input" rows="3" spellcheck="false">0xe8</textarea>
  <div class="fa-actions">
    <button type="button" id="fa-go" class="gx-primary">Analyse</button>
    <span class="fa-muted">Examples:</span>
    <button type="button" data-example="0xe8">majority (n=3)</button>
    <button type="button" data-example="0x7888">bent (n=4)</button>
    <button type="button" data-example="0x2a5dbf51">n=5 class 9</button>
    <button type="button" data-example="0x110707FF,0xE0422107">n=6 data file entry</button>
    <button type="button" data-example="random">random (n=6)</button>
  </div>
  <p class="fa-help">Formats: a hex value for $n \\le 5$ (bit $i$ is $f(i)$, e.g.
  <code>0xe8</code>); comma-separated 32-bit words for larger $n$, word 0 first, as in the
  data files (e.g. <code>0x110707FF,0xE0422107</code>); or a string of 0s and 1s,
  $f(0)$ first.</p>
</div>
<div id="fa-out" class="fa-out" aria-live="polite"></div>
<script type="application/json" id="fa-data">{__import__("json").dumps(fa_data, separators=(",", ":"))}</script>
<script src="analyse.js" defer></script>"""
    page("analyse.html", "Function Analyser — Boolean Functions for Cryptography",
         "Paste a Boolean function's truth table to compute its nonlinearity, degree, ANF, Walsh spectrum, autocorrelation, correlation immunity, algebraic immunity and affine class.",
         fa)

    # Class sizes / self-mapping constant
    s5 = [(c, f"<code>{e}</code>", s, f) for c, e, s, f in SELF5]
    nl6 = [(k, v) for k, v in N6_FNS_BY_NL]
    cs = f"""<h1>Counting the Functions in Each Class</h1>
<p>An affine equivalence class groups Boolean functions that share the same cryptographic
properties. But how <em>big</em> is each class, that is, how many of the $2^{{2^n}}$ functions does it
contain? The PhD research behind this site answered this exactly for every class with
$n \\le 6$, using what the thesis calls the <strong>self-mapping constant</strong>.</p>

<h2>Self mappings</h2>
<p>An affine transform maps $f$ to $g(x) = f(Dx \\oplus a) \\oplus b \\cdot x \\oplus c$, where $D$ is an
invertible $n \\times n$ binary matrix, $a, b \\in \\mathbb{{Z}}_2^n$ and $c \\in \\mathbb{{Z}}_2$.
A transform that maps $f$ to <em>itself</em> is a <strong>self mapping</strong> of $f$. The identity is
always one, so every function has at least one.</p>
<p>The thesis proves three facts about self mappings (Chapter 4):</p>
<ol>
<li>The self mappings of $f$ form a <strong>subgroup</strong> of the affine group, so their number,
$\\theta$, divides the order of the group.</li>
<li>If $f$ and $g$ are equivalent, the number of distinct transforms taking $f$ to $g$ is
<strong>exactly $\\theta$</strong>, the number of self mappings of $f$.</li>
<li>Equivalent functions have the <strong>same</strong> number of self mappings, so $\\theta$ is a
property of the whole class: the <em>self-mapping constant</em>.</li>
</ol>

<h2>The class-size formula</h2>
<p>Counting the choices for $D$ (row $k$ can be any vector outside the span of the previous
rows, giving $2^n - 2^k$ choices), $a$, $b$ and $c$, the total number of affine transforms is</p>
<p>$$\\mathcal{{T}} = 2^{{2n+1}} \\prod_{{i=0}}^{{n-1}} \\left(2^n - 2^i\\right).$$</p>
<p>Since every function in a class $\\mathcal{{C}}$ is reached from $f$ by exactly $\\theta$ of these
transforms, the number of functions in the class is simply</p>
<p>$$\\#\\mathcal{{C}} = \\frac{{\\mathcal{{T}}}}{{\\theta}}.$$</p>
<p>(This is an instance of the orbit–stabiliser theorem; the self mappings are the stabiliser of
$f$ in the affine group.) The bounds follow immediately: $\\theta \\ge 1$, and the largest
$\\theta$ belongs to the smallest class, the affine functions, with $2^{{n+1}}$ members.</p>
{simple_table(["n", "affine transforms 𝒯"], [(n, t) for n, t in AFFINE_T.items() if n >= 3], num_cols=(0, 1))}
<p>For example, with $n = 4$ there are $15 \\times 14 \\times 12 \\times 8 = 20{{,}}160$ invertible
matrices, and $20{{,}}160 \\times 16 \\times 16 \\times 2 = 10{{,}}321{{,}}920$ transforms.</p>

<h2>All 48 classes for $n = 5$</h2>
<p>Class numbers and example functions match the
<a href="equivalence-classes.html">$n = 5$ class table</a>. There are 33 distinct values of $\\theta$,
from 32 (class 35, the largest class, with 639,959,040 functions) to 319,979,520 (the affine
class, with 64). The class sizes sum to exactly $2^{{32}} = 4{{,}}294{{,}}967{{,}}296$.</p>
{simple_table(["class", "example", "self maps θ", "functions in class"], s5, num_cols=(0, 2, 3))}

<h2>$n = 6$: the self-mapping distribution</h2>
<p>For the 150,357 classes of $n = 6$ there are <strong>122</strong> distinct values of $\\theta$.
Most classes have no symmetry at all: <strong>91,184 classes have $\\theta = 1$</strong> (only the
identity), so each contains the full $\\mathcal{{T}} = 165{{,}}140{{,}}150{{,}}353{{,}}920$ functions. A further
32,454 have $\\theta = 2$ and 12,522 have $\\theta = 4$. At the other extreme, the affine class has
$\\theta = 1{{,}}290{{,}}157{{,}}424{{,}}640$.</p>
<details>
<summary><strong>Number of $n = 6$ classes for each value of θ</strong>: all 122 values</summary>
{simple_table(["self maps θ", "classes"], SELF6_FREQ, num_cols=(0, 1))}
</details>

<h2>How many functions have each nonlinearity? ($n = 6$)</h2>
<p>Summing the class sizes over the classes at each nonlinearity gives the exact number of
6-variable functions with that nonlinearity. For nonlinearity below 16 these follow from a known
closed formula, $\\binom{{64}}{{N}} \\cdot 2^{{7}}$; for 16 and above, the thesis obtained them by
summing class sizes. The total is exactly $2^{{64}}$, and the 5,425,430,528 functions of
nonlinearity 28 are precisely the bent functions, summed over the four bent classes.</p>
{simple_table(["nonlinearity", "number of functions"], nl6, num_cols=(0, 1))}

<div class="callout-note"><p><strong>Source.</strong> J. Fuller, <em>Analysis of Affine Equivalent
Boolean Functions for Cryptography</em>, PhD thesis, QUT, 2003: Chapter 4 (self mappings,
class sizes, nonlinearity counts) and Appendix 4 (tables), available from
<a href="https://eprints.qut.edu.au/15828/">QUT ePrints</a>; see also Millan, Fuller and Dawson,
CEC 2003. All tables on this page were re-checked in 2026 against the original PhD output
files. Maiorana's 1991 classification of the cosets of $\\mathrm{{RM}}(1,6)$ records stabiliser
orders in coding-theory terms.</p></div>"""
    page("class-sizes.html", "Class Sizes and the Self-Mapping Constant — Boolean Functions for Cryptography",
         "How many Boolean functions are in each affine equivalence class: the self-mapping constant, all 48 class sizes for n = 5, and function counts by nonlinearity for n = 6.",
         cs)

    # 404 (GitHub Pages serves 404.html for missing paths; absolute links so it works at any depth)
    nf = """<h1>Page not found</h1>
<p>Sorry, that page doesn't exist. It may have moved when the original <em>Boolean Planet</em>
site was rebuilt.</p>
<p>Try the <a href="/">home page</a> or the
<a href="/equivalence-classes.html">equivalence class tables and n = 6 data</a>.</p>"""
    page("404.html", "Page not found — Boolean Functions for Cryptography",
         "Page not found.", nf, extra='<meta name="robots" content="noindex">\n')

    # sitemap.xml + robots.txt
    urls = [SITE if s == "index.html" else SITE + s for s in PAGES]
    with open("sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
                + "</urlset>\n")
    with open("robots.txt", "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")

    print("Built: " + ", ".join(PAGES) + ", resources.html (redirect), 404.html, sitemap.xml, robots.txt")


if __name__ == "__main__":
    build()
