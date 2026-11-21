# Private Vorschau „Weniger Vorlage“: vorschau.html + muster.css + umbau.py
#   python3 entwurf/muster/build_vorschau.py <Zieldatei>
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, H); from umbau import umbau
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
css = open(os.path.join(H, "muster.css"), encoding="utf-8").read()
i = h.index("</style>"); h = umbau(h[:i] + "\n" + css + h[i:])
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Weniger Vorlage</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
