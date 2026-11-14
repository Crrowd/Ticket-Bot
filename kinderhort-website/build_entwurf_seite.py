# Erzeugt aus vorschau.html eine Fassung für eine private Vorschau-Seite (claude.ai-Artifact):
# ohne eigenes HTML-Gerüst, mit „-“ statt „:“ in den Sprungmarken und deutlichem Entwurfs-Hinweis.
# Aufruf nach build.py und build_vorschau.py:  python3 build_entwurf_seite.py <Zieldatei>
import os, re, sys

W = os.path.dirname(os.path.abspath(__file__))
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
style = h[h.index("<style>"):h.index("</style>") + 8]
body = h[h.index("<body>") + 6:h.index("</body>")]

body = re.sub(r'(href="#[a-z]+):([\w-]+")', r"\1-\2", body)
body = re.sub(r'("u": "#[a-z]+):([\w-]+")', r"\1-\2", body)
body = body.replace('"#aktuelles:termine"', '"#aktuelles-termine"')

def swap(a, b):
    global body
    assert a in body, a
    body = body.replace(a, b)

swap("var parts = h.split(':'); if (document.getElementById('seite-' + parts[0])) { name = parts[0]; anchor = parts[1] || ''; }",
     "var cut = h.indexOf('-'), pg = cut < 0 ? h : h.slice(0, cut); if (document.getElementById('seite-' + pg)) { name = pg; anchor = cut < 0 ? '' : h.slice(cut + 1); }")
swap('a.getAttribute("href").split("#").pop().split(":").pop()', 'a.getAttribute("href").split("#").pop().replace(/^[a-z]+-/, "")')
# „downloads“ ist dort als Sprungmarke reserviert
body = body.replace('href="#downloads', 'href="#unterlagen').replace('"u": "#downloads', '"u": "#unterlagen')
swap('id="seite-downloads" data-page="downloads"', 'id="seite-unterlagen" data-page="unterlagen"')
assert "#downloads" not in body
swap("Vorschau der neuen Webseite – alle Seiten in einer Datei",
     "Entwurf – nicht die offizielle Webseite des Kinderhorts. Anrufen, E-Mail, Kalender und Drucken sind in dieser Vorschau deaktiviert.")

out = "<title>Kinderhort Grombühl Entwurf</title>\n" + style + "\n" + body
open(sys.argv[1], "w", encoding="utf-8").write(out)
print(sys.argv[1], round(len(out) / 1e6, 2), "MB")
