# Vorschau „Kontakt kompakt“ (23.11.2026): Telefon und E-Mail als schmale Knopfzeile unter „Kind krankmelden“,
# Öffnungsstatus klein daneben statt als Listeneintrag; darunter nur die drei E-Mail-Vorlagen.
#   python3 entwurf/kontakt-kompakt/build_vorschau.py <Zieldatei>
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
a = h.index('id="seite-kontakt"'); a = h.rindex("<div", 0, a); b = h.index('<div class="spa-page', a + 10)
seg = h[a:b]
def raus(muster):
    global seg
    m = re.search(muster, seg, re.S); assert m, muster
    blk = m.group(0); seg = seg.replace(blk, "", 1); return blk
tel = raus(r'<a class="quick-card reveal" href="tel:\+4993127898920">.*?</a>\s*')
mail = raus(r'<a class="quick-card reveal" href="mailto:kinderhort\.grombuehl@t-online\.de">.*?</a>\s*')
raus(r'<div class="quick-card status-mini reveal" id="status-kontakt" hidden>.*?</span></span>\s*</div>\s*')
svg_tel = re.search(r'<svg.*?</svg>', tel, re.S).group(0)
svg_mail = re.search(r'<svg.*?</svg>', mail, re.S).group(0)
zeile = ('<div class="kontakt-zeile">'
         f'<a class="btn btn-primary" href="tel:+4993127898920">{svg_tel} 0931&nbsp;2789892&nbsp;0</a>'
         f'<a class="btn btn-ghost" href="mailto:kinderhort.grombuehl@t-online.de">{svg_mail} E-Mail schreiben</a>'
         '<p class="kz-status" id="status-kontakt" hidden><span class="status-today"></span><span class="status-sub"></span></p>'
         '</div>')
m = re.search(r'(<div class="quick-grid">\s*<a class="quick-card reveal" href="[^"]*">.*?</a>)', seg, re.S); assert m
seg = seg.replace(m.group(1), m.group(1) + zeile, 1)
css = '''
/* Vorschau Kontakt kompakt */
#seite-kontakt .kontakt-zeile { grid-column: 1 / -1; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 16px; margin: -8px 0 24px; }
#seite-kontakt .kontakt-zeile .btn svg { width: 20px; height: 20px; }
html body #seite-kontakt .kontakt-zeile .btn-primary { background: var(--ink); color: var(--paper); }
html body #seite-kontakt .kontakt-zeile .btn-primary:hover { background: var(--surface); }
#seite-kontakt .quick-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 1100px) { #seite-kontakt .quick-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 700px) { #seite-kontakt .quick-grid { grid-template-columns: minmax(0, 1fr); } }
/* „Kind krankmelden“ wie die anderen Einträge, Telefon und E-Mail als große Zeile ganz oben */
#seite-kontakt .kontakt-zeile { order: -1; margin: 0 0 28px; }
html body #seite-kontakt .quick-grid > .quick-card:first-child { grid-column: auto; padding: 18px 0; margin: 0; background: none; box-shadow: none; border-radius: 0; border-top: 1px solid rgb(var(--ink-rgb) / .2); }
#seite-kontakt .quick-grid > .quick-card:first-child strong { font-size: inherit; }
html body #seite-kontakt .quick-grid > .quick-card:first-child .quick-icon { background: var(--rose); width: 40px; height: 40px; border-radius: 12px; }
#seite-kontakt .kontakt-zeile .btn { min-height: 64px; padding: 0 30px; font-size: 1.2rem; gap: 12px; }
#seite-kontakt .kontakt-zeile .btn svg { width: 24px; height: 24px; }
#seite-kontakt .kz-status { margin: 0 0 0 auto; display: flex; align-items: center; gap: 8px; font: 600 .95rem var(--font-body); color: var(--ink); }
#seite-kontakt .kz-status::before { content: ""; width: 9px; height: 9px; border-radius: 50%; background: var(--state-open); }
#seite-kontakt .kz-status.is-closed::before { background: var(--state-closed); }
#seite-kontakt .kz-status .status-sub { display: none; }
@media (max-width: 700px) { #seite-kontakt .kontakt-zeile .btn { flex: 1 1 100%; justify-content: center; } #seite-kontakt .kz-status { margin: 4px 0 0; } }
'''
h = h[:a] + seg + h[b:]
i = h.index("</style>"); h = h[:i] + css + h[i:]
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Kontakt kompakt</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
