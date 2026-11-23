# Vorschau „Verbesserungen 3“ (23.11.2026)
#  2 Aktuelles: Etiketten „Vormerktermine“ und „Schließtage“ entfallen (wiederholen die Überschrift)
#  4 Kontakt: unter „Fragen Sie einfach“ Links zu den ausführlichen Fragen je Bereich
#  5 Downloads: Dateien nur noch einmal („Für alle Bereiche“ + „Nur Kinderhort“), ruhigere Dateizeilen,
#    Etiketten „Downloads“/„Kalender“ und der Abschnitt „Hier finden Sie alle aktuellen Termine“ entfallen
#   python3 entwurf/verbesserungen-3/build_vorschau.py <Zieldatei>
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
def seite(name, fn):
    global h
    a = h.index(f'id="seite-{name}"'); a = h.rindex("<div", 0, a); b = h.index('<div class="spa-page', a + 10)
    h = h[:a] + fn(h[a:b]) + h[b:]
def weg(seg, t):
    assert seg.count(t) == 1, t; return seg.replace(t, "")

def aktuelles(s):
    s = weg(s, '<span class="kicker">Vormerktermine</span>')
    return weg(s, '<span class="kicker">Schließtage</span>')

def kontakt(s):
    i = s.index('id="frag"'); j = s.index("  </div>\n</section>", i)
    zeile = ('<p class="frag-weiter">Ausführliche Antworten nach Bereich: '
             '<a href="#kinderkrippe:fragen">Kinderkrippe</a> · <a href="#kindergarten:fragen">Kindergarten</a> · <a href="#kinderhort:fragen">Kinderhort</a></p>\n')
    return s[:j] + zeile + s[j:]

def downloads(s):
    i = s.index('<div class="downloads">'); j = s.index("</div>\n</div>", i) + len("</div>\n</div>")
    block = s[i:j]
    lis = re.findall(r"<li><a class=\"dl-link\".*?</a></li>", block, re.S)
    plan = next(x for x in lis if "Ferienplan" in x); medi = next(x for x in lis if "Medikament" in x); abc = next(x for x in lis if "HortABC" in x)
    neu = ('<div class="downloads two">\n'
           f'  <div class="dl-group reveal"><h3>Für alle Bereiche</h3><ul>{plan}{medi}</ul></div>\n'
           f'  <div class="dl-group theme-hort reveal"><h3>Nur Kinderhort</h3><ul>{abc}</ul></div>\n</div>')
    s = s[:i] + neu + s[j:]
    s = weg(s, '<span class="kicker">Downloads</span>')
    s = weg(s, '<span class="kicker">Kalender</span>')
    m = re.search(r'<section class="section tight">\s*<div class="container">\s*<div class="section-head"><span class="kicker">Aktuelles</span><h2>Hier finden Sie alle aktuellen Termine</h2>.*?</section>', s, re.S)
    assert m; return s.replace(m.group(0), "", 1)

seite("aktuelles", aktuelles); seite("kontakt", kontakt); seite("downloads", downloads)
css = '''
/* Vorschau Verbesserungen 3 */
.frag-weiter { margin: 20px 0 0; font-weight: 500; }
.frag-weiter a { font-weight: 600; }
#seite-unterlagen .dl-link { background: rgb(var(--ink-rgb) / .05); }
@media (hover: hover) and (pointer: fine) { #seite-unterlagen .dl-link:hover { background: rgb(var(--ink-rgb) / .1); translate: none; } }
'''
i = h.index("</style>"); h = h[:i] + css + h[i:]
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Verbesserungen 3</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
