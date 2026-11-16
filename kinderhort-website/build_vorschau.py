# Erzeugt vorschau.html: die komplette Webseite als EINE Datei
# (Bilder, Schriften, CSS und JS eingebettet; Seitenwechsel per #-Navigation).
# Aufruf nach build.py:  python3 build_vorschau.py
import os, re, io, base64
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
PAGES = ["index", "aktuelles", "kinderkrippe", "kindergarten", "kinderhort", "downloads", "kontakt", "impressum"]
ORIG = "https://kinderhort-grombuehl.de/wp-content/uploads/"
PDFS = {
    "downloads/Ferienplan_2026_27.pdf": ORIG + "2026/10/Ferienplan_2026_27.pdf",
    "downloads/HortABC.pdf": ORIG + "2021/03/HortABC.pdf",
    "downloads/Medikamentenvereinbarung.pdf": ORIG + "2021/10/Medikamentenvereinbarung.pdf",
}

_cache = {}
def data_uri(path):
    if path not in _cache:
        full = os.path.join(W, path)
        if path.endswith(".svg"):
            _cache[path] = "data:image/svg+xml;base64," + base64.b64encode(open(full, "rb").read()).decode()
        else:
            im = Image.open(full)
            buf = io.BytesIO()
            if path.endswith(".png"):
                im.thumbnail((500, 500)); im.save(buf, "PNG", optimize=True); mime = "image/png"
            else:
                im = im.convert("RGB"); im.thumbnail((960, 960)); im.save(buf, "JPEG", quality=68, optimize=True, progressive=True); mime = "image/jpeg"
            _cache[path] = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[path]

def read(p):
    return open(os.path.join(W, p), encoding="utf-8").read()

# --- CSS mit eingebetteten Schriften ---
css = read("css/style.css") + "\n" + read("css/erzeugt.css")
css = re.sub(r'url\("\.\./fonts/([^"]+)"\)',
             lambda m: 'url("data:font/woff2;base64,' + base64.b64encode(open(os.path.join(W, "fonts", m.group(1)), "rb").read()).decode() + '")', css)
css += """
.spa-page { display: none; }
.spa-page.active { display: block; }
.no-js .spa-page { display: block; }

.preview-note { background: #F1E5E3; color: #1E3B44; text-align: center; font: 700 .85rem/1.4 'Plus Jakarta Sans', sans-serif; padding: 6px 12px; }
"""

js = read("js/main.js")

header = footer = None
mains = []
for name in PAGES:
    src = read(name + ".html")
    body_cls = re.search(r"<body(?: class=\"([^\"]*)\")?>", src).group(1) or ""
    if header is None:
        header = re.search(r'(<a class="skip-link".*?</header>)', src, re.S).group(1)
        footer = re.search(r"(<footer.*?</footer>)", src, re.S).group(1)
    main = re.search(r'<main id="inhalt">(.*)</main>', src, re.S).group(1)
    # In-Page-Anker (#xyz) -> #seite:xyz
    main = re.sub(r'href="#([a-z][\w-]*)"', lambda m: f'href="#{name}:{m.group(1)}"', main)
    title = re.search(r"<title>(.*?)</title>", src).group(1)
    mains.append(f'<div class="spa-page {body_cls}" id="seite-{name}" data-page="{name}" data-title="{title}">{main}</div>')

doc = "\n".join([header, "<main id=\"inhalt\">", *mains, "</main>", footer])

# Links zwischen Seiten -> Hash-Navigation
doc = re.sub(r'href="([a-z]+)\.html#([\w-]+)"', r'href="#\1:\2"', doc)
doc = re.sub(r'href="([a-z]+)\.html"', r'href="#\1"', doc)
# PDFs -> Original-Downloads
for k, v in PDFS.items():
    doc = doc.replace(f'href="{k}" download', f'href="{v}" target="_blank" rel="noopener"').replace(f'href="{k}"', f'href="{v}" target="_blank" rel="noopener"')
# Bilder einbetten (src und data-full)
used = sorted(set(re.findall(r'(?:src|data-full|href)="(img/[^"]+)"', doc)))
keys = {path: f"i{n}" for n, path in enumerate(used)}
TRANSPARENT = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
doc = re.sub(r'src="(img/[^"]+)"', lambda m: f'src="{TRANSPARENT}" data-img="{keys[m.group(1)]}"', doc)
doc = re.sub(r'(data-full|href)="(img/[^"]+)"', lambda m: f'{m.group(1)}="#" data-{"full" if m.group(1)=="data-full" else "href"}-img="{keys[m.group(2)]}"' if m.group(1)=="href" else f'data-full="" data-full-img="{keys[m.group(2)]}"', doc)
img_map = "var IMG = {" + ",".join(f'{k}:"{data_uri(p)}"' for p, k in keys.items()) + "};" + '''
document.querySelectorAll("[data-img]").forEach(function (e) { e.src = IMG[e.dataset.img]; });
document.querySelectorAll("[data-full-img]").forEach(function (e) { e.setAttribute("data-full", IMG[e.dataset.fullImg]); });
document.querySelectorAll("[data-href-img]").forEach(function (e) { e.href = IMG[e.dataset.hrefImg]; });
'''
doc = doc.replace(' loading="lazy"', "")
doc = re.sub(r' srcset="[^"]*" sizes="[^"]*"', '', doc)
for ics in ('schliesstage.ics', 'termine.ics'):
    doc = doc.replace(f'href="downloads/{ics}" download', f'href="#" data-hinweis="Kalenderdatei auf der veröffentlichten Seite"')

router = """
(function () {
  var pages = document.querySelectorAll('.spa-page');
  function go() {
    var h = decodeURIComponent(location.hash.slice(1)), name = 'index', anchor = '';
    if (h) { var parts = h.split(':'); if (document.getElementById('seite-' + parts[0])) { name = parts[0]; anchor = parts[1] || ''; } }
    var cur;
    pages.forEach(function (p) { var on = p.dataset.page === name; p.classList.toggle('active', on); if (on) cur = p; });
    document.title = cur.dataset.title;
    document.querySelectorAll('.main-nav a').forEach(function (a) {
      if (a.getAttribute('href') === '#' + name) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    var t = anchor && cur.querySelector('#' + CSS.escape(anchor));
    if (t) { t.scrollIntoView(); } else { window.scrollTo(0, 0); }
    cur.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('visible'); });
  }
  window.addEventListener('hashchange', go);
  go();
})();
"""

daten = re.sub(r'"u": "([a-z]+)\.html#([\w-]+)"', r'"u": "#\1:\2"', read("js/daten.js"))
daten = re.sub(r'"u": "([a-z]+)\.html"', r'"u": "#\1"', daten)
for k, v in PDFS.items():
    daten = daten.replace(f'"u": "{k}"', f'"u": "{v}"')
js = js.replace('"aktuelles.html#termine"', '"#aktuelles:termine"')
html = f"""<!DOCTYPE html>
<html lang="de" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kath. Kinder- und Jugendhort Grombühl e. V. – Vorschau</title>
<link rel="icon" href="{data_uri('img/favicon.svg')}">
<style>{css}</style>
</head>
<body>
<div class="preview-note">Vorschau der neuen Webseite – alle Seiten in einer Datei</div>
{doc}
<script>{img_map}</script>
<script>{daten}</script>\n<script>{js}</script>
<script>{router}</script>
</body>
</html>
"""
out = os.path.join(W, "vorschau.html")
open(out, "w", encoding="utf-8").write(html)
print(out, round(len(html) / 1e6, 2), "MB")
