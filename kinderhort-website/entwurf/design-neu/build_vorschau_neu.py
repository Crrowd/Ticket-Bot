# Baut die private Vorschau des Entwurfs „Design neu“: die normale Vorschau (vorschau.html, alle Seiten in einer Datei)
# plus entwurf/design-neu/design-neu.css am Ende des Stils. Aufruf nach build.py und build_vorschau.py:
#   python3 entwurf/design-neu/build_vorschau_neu.py <Zieldatei>
import os, sys, runpy
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
css = open(os.path.join(W, "entwurf", "design-neu", "design-neu.css"), encoding="utf-8").read()
i = h.index("</style>")
h = h[:i] + "\n" + css + "\n" + h[i:]
tmp = sys.argv[1] + ".quelle.html"
open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Kinderhort Grombühl Design neu</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
