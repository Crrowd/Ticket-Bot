# Vorschau: Etiketten auf der Kinderhort-Seite, die nur die Überschrift wiederholen, entfallen (6 von 10)
#   python3 entwurf/hort-etiketten/build_vorschau.py <Zieldatei>
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
WEG = ["Räumlichkeiten", "Tagesablauf", "Das zeichnet uns aus", "Zusammenarbeit mit den Schulen", "Meistgestellte Fragen", "Schließtage"]
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
a = h.index('id="seite-kinderhort"'); a = h.rindex("<div", 0, a); b = h.index('<div class="spa-page', a + 10)
seg = h[a:b]
for k in WEG:
    t = '<span class="kicker">' + k + '</span>'
    assert seg.count(t) == 1, k; seg = seg.replace(t, "")
h = h[:a] + seg + h[b:]
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Kinderhort Etiketten</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
