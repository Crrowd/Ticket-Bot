# Private Vorschau „Startseiten-Varianten“: vorschau.html + Kartenstil wie live + varianten.css/js + GSAP (cdnjs)
#   python3 entwurf/landing-varianten/build_vorschau.py <Zieldatei>
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
css = open(os.path.join(H, "varianten.css"), encoding="utf-8").read()
js = open(os.path.join(H, "varianten.js"), encoding="utf-8").read()
i = h.index("</style>"); h = h[:i] + "\n" + css + h[i:]
h = h.replace("</body>", '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n<script>' + js + "</script></body>", 1)
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Startseite Varianten</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
