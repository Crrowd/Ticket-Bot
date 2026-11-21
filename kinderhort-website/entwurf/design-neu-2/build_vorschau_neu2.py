# Private Vorschau „Design neu 2“: vorschau.html + design-neu.css + design-neu-2.css, Status und Krankmeldung verschoben.
#   python3 entwurf/design-neu-2/build_vorschau_neu2.py <Zieldatei>
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, H); from umbau import umbau
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
css = "".join(open(p, encoding="utf-8").read() + "\n" for p in [os.path.join(W, "entwurf", "design-neu", "design-neu.css"), os.path.join(H, "design-neu-2.css")])
i = h.index("</style>"); h = umbau(h[:i] + "\n" + css + h[i:])
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Kinderhort Grombühl Design neu 2</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
