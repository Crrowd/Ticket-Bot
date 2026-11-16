"""Entwurf Idee 79: Kinderzeichnungen statt Symbolen – Wachsmalstift-Linien, erzeugt mit leichtem Zittern."""
import math, random, os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
R = random.Random(7)

ROSE, TUERKIS, PETROL, SALBEI, OCKER = "#C98F86", "#2D6A6A", "#1E3B44", "#7FA9A2", "#D9A441"

def jit(pts, a=1.2):
    return [(x + R.uniform(-a, a), y + R.uniform(-a, a)) for x, y in pts]

def smooth(pts, closed=False):
    """Catmull-Rom durch alle Punkte."""
    if len(pts) == 2:
        return f"M{pts[0][0]:.1f} {pts[0][1]:.1f} L{pts[1][0]:.1f} {pts[1][1]:.1f}"
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d

def line(pts, col, w=3.8, twice=True, a=1.1):
    """Ein Strich – Kinder fahren gern zweimal drüber."""
    out = f'<path d="{smooth(jit(pts, a))}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    if twice: out += f'<path d="{smooth(jit(pts, a * 1.6))}" stroke="{col}" stroke-width="{w * .7}" fill="none" stroke-linecap="round" opacity=".55"/>'
    return out

def kreis(cx, cy, r, n=14, über=1.15):
    return [(cx + r * (1 + R.uniform(-.06, .06)) * math.cos(t), cy + r * (1 + R.uniform(-.06, .06)) * math.sin(t)) for t in [i / n * 2 * math.pi * über - .4 for i in range(n + 1)]]

def kritzel(x0, y0, x1, y1, col, dichte=7, w=2.4):
    """Ausmalen mit Zickzack, wie mit dem Wachsmalstift."""
    pts, y, links = [], y0, True
    while y <= y1:
        pts.append((x0 if links else x1, y)); y += dichte; links = not links
    return f'<path d="{smooth(jit(pts, 1.5))}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" opacity=".38"/>'

def svg(inner, label):
    return f'<svg viewBox="0 0 100 100" role="img" aria-label="{label}" class="zg"><g filter="url(#stift)">{inner}</g></svg>'

Z = {}
# Sonne
s = kritzel(36, 36, 64, 64, OCKER, 5) + line(kreis(50, 50, 15), OCKER, 3.6)
for i in range(9):
    t = i / 9 * 2 * math.pi + R.uniform(-.1, .1)
    s += line([(50 + 22 * math.cos(t), 50 + 22 * math.sin(t)), (50 + (31 + R.uniform(-3, 3)) * math.cos(t), 50 + (31 + R.uniform(-3, 3)) * math.sin(t))], OCKER, 3, False)
s += line([(44, 47), (44.5, 48)], PETROL, 3.4, False) + line([(56, 47), (56.5, 48)], PETROL, 3.4, False) + line([(43, 55), (50, 59), (57, 55)], PETROL, 2.6, False)
Z["sonne"] = ("Sonne", s)
# Haus (Kindergarten)
h = kritzel(26, 50, 74, 82, ROSE, 6) + line([(25, 50), (24, 83), (76, 84), (75, 50)], ROSE) + line([(20, 53), (50, 22), (80, 53)], TUERKIS, 3.6)
h += line([(44, 84), (44, 66), (56, 66), (56, 84)], PETROL, 2.8) + line([(30, 58), (40, 58), (40, 66), (30, 66), (30, 58)], PETROL, 2.4, False)
h += line([(64, 36), (64, 26), (70, 26), (70, 42)], TUERKIS, 2.8, False)
Z["haus"] = ("Haus", h)
# Kind mit Luftballon (Krippe)
k = line(kreis(42, 34, 9), PETROL, 3) + line([(42, 43), (42, 66)], PETROL) + line([(30, 52), (42, 49), (55, 46)], PETROL)
k += line([(42, 66), (34, 84)], PETROL) + line([(42, 66), (50, 84)], PETROL)
k += kritzel(60, 12, 80, 36, ROSE, 5) + line(kreis(70, 24, 12, 12), ROSE, 3.4) + line([(70, 36), (66, 42), (60, 44), (55, 46)], PETROL, 1.8, False)
Z["kind"] = ("Kind mit Luftballon", k)
# Schulranzen (Hort)
r = kritzel(28, 36, 72, 80, TUERKIS, 6) + line([(30, 34), (70, 33), (73, 80), (27, 81), (30, 34)], TUERKIS, 3.4)
r += line([(30, 34), (32, 54), (68, 53), (70, 33)], PETROL, 2.8) + line([(46, 53), (47, 60), (54, 60), (53, 53)], OCKER, 2.6, False)
r += line([(40, 33), (42, 22), (58, 22), (60, 33)], PETROL, 3)
Z["ranzen"] = ("Schulranzen", r)
# Kalender
c = line([(22, 26), (78, 25), (79, 82), (21, 83), (22, 26)], PETROL, 3) + kritzel(23, 27, 77, 37, ROSE, 4) + line([(22, 38), (78, 37)], PETROL, 2.6, False)
c += line([(34, 18), (34, 30)], PETROL, 3, False) + line([(66, 18), (66, 30)], PETROL, 3, False)
for i in range(3):
    for j in range(4):
        x, y = 31 + j * 13, 50 + i * 11
        c += line([(x, y), (x + 3, y + .5)], SALBEI if (i, j) != (1, 2) else ROSE, 4 if (i, j) == (1, 2) else 3, False)
c += line(kreis(60, 61, 7, 10), ROSE, 2.4, False)
Z["kalender"] = ("Kalender", c)
# Telefon
t = line([(30, 22), (40, 20), (46, 34), (40, 40), (52, 58), (60, 54), (74, 64), (72, 76), (60, 80), (40, 70), (26, 46), (24, 32), (30, 22)], TUERKIS, 3.4)
t += kritzel(30, 24, 42, 36, TUERKIS, 4) + kritzel(60, 62, 72, 76, TUERKIS, 4)
t += line([(60, 24), (66, 18)], OCKER, 2.6, False) + line([(66, 32), (76, 28)], OCKER, 2.6, False) + line([(56, 18), (58, 12)], OCKER, 2.6, False)
Z["telefon"] = ("Telefon", t)
# Bett mit Thermometer (krank)
b = line([(18, 70), (82, 70)], PETROL, 3.4) + line([(18, 50), (18, 82)], PETROL, 3.4) + line([(82, 62), (82, 82)], PETROL, 3.4)
b += kritzel(26, 56, 80, 68, SALBEI, 4) + line([(24, 56), (82, 56), (82, 68)], SALBEI, 2.8, False) + line(kreis(30, 52, 6, 10), PETROL, 2.6)
b += line([(54, 18), (54, 40)], ROSE, 4.2, False) + line(kreis(54, 44, 4, 8), ROSE, 3, False) + line([(58, 24), (61, 24)], ROSE, 2, False) + line([(58, 30), (61, 30)], ROSE, 2, False)
Z["krank"] = ("Bett mit Thermometer", b)
# Blume
f = line([(50, 86), (49, 64), (51, 46)], TUERKIS, 3.2) + line([(49, 70), (38, 62), (49, 64)], TUERKIS, 2.6) + line([(50, 74), (62, 66), (50, 68)], TUERKIS, 2.6)
for i in range(6):
    tt = i / 6 * 2 * math.pi
    f += line(kreis(50 + 10 * math.cos(tt), 34 + 10 * math.sin(tt), 6, 8, 1.05), ROSE, 2.6, False)
f += kritzel(45, 29, 55, 39, OCKER, 3, 3) + line(kreis(50, 34, 5, 8), OCKER, 2.8, False)
Z["blume"] = ("Blume", f)

def card(key, titel, text, alt):
    lab, zg = Z[key]
    return f'''<article class="area"><div class="pic">{svg(zg, lab)}</div><div><h3>{titel}</h3><p>{text}</p><span class="mehr">Mehr erfahren →</span></div></article>'''

ICON = {
    "kalender": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "telefon": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "krank": '<path d="M12 3v11"/><circle cx="12" cy="17" r="3.5"/>',
    "haus": '<path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z"/>',
}
def ic(k): return f'<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

vergleich = "".join(f'''<div class="vg"><span class="lbl">{name}</span><div class="pair"><div class="alt">{ic(k)}<small>heute</small></div><div class="neu">{svg(Z[k][1], Z[k][0])}<small>gemalt</small></div></div></div>'''
                    for k, name in [("krank", "Kind krankmelden"), ("kalender", "Termine"), ("telefon", "Durchwahlen"), ("haus", "Anfahrt")])
galerie = "".join(f'<figure>{svg(zg, lab)}<figcaption>{lab}</figcaption></figure>' for k, (lab, zg) in Z.items())

html = f'''<title>Kinderzeichnungen</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap">
<style>
/* Layout: Erklärung oben, dann die Zeichnungen in echter Umgebung (Bereichskarten, Schnellwege), unten alle Motive */
:root {{
  --paper: #F3F8F7; --card: #FFFFFF; --ink: #1E3B44; --ink-soft: #4A6670; --sage: #A8C5C0; --rose: #D4B5B0; --teal: #2D6A6A; --line: rgba(30,59,68,.12);
  --font: "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --paper: #10232A; --card: #F3F8F7; --ink: #E3EEEC; --ink-soft: #A9C1BE; --line: rgba(227,238,236,.14); color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --paper: #10232A; --card: #F3F8F7; --ink: #E3EEEC; --ink-soft: #A9C1BE; --line: rgba(227,238,236,.14); color-scheme: dark; }}
body {{ background: var(--paper); color: var(--ink); font: 16px/1.6 var(--font); }}
.wrap {{ max-width: 1040px; margin: 0 auto; padding-block: 40px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 56px; }}
h1 {{ font-size: clamp(2rem, 5vw, 3rem); line-height: 1.08; margin: 8px 0 12px; text-wrap: balance; letter-spacing: -.02em; }}
h2 {{ font-size: 1.4rem; margin: 0 0 6px; text-wrap: balance; }}
.kicker {{ display: inline-block; font-size: .8rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; background: var(--rose); color: #1E3B44; padding: 4px 12px; border-radius: 999px; }}
.lead {{ max-width: 38em; color: var(--ink-soft); font-size: 1.08rem; margin: 0; }}
.sec > p {{ margin: 0 0 20px; color: var(--ink-soft); max-width: 40em; }}
.zg {{ width: 100%; height: 100%; display: block; }}
.areas {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; }}
.area {{ background: var(--card); color: #1E3B44; border-radius: 20px; padding: 22px; display: grid; gap: 14px; box-shadow: 0 14px 30px -20px rgba(30,59,68,.45); }}
.area .pic {{ width: 132px; height: 132px; border-radius: 18px; background: #E6EFED; padding: 8px; }}
.area h3 {{ margin: 0; font-size: 1.2rem; }} .area p {{ margin: 4px 0 8px; color: #4A6670; font-size: .95rem; }}
.area .mehr {{ font-weight: 700; font-size: .92rem; color: #2D6A6A; }}
.vgl {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; }}
.vg {{ border: 1px solid var(--line); border-radius: 16px; padding: 16px; display: grid; gap: 10px; }}
.vg .lbl {{ font-weight: 700; }}
.pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.pair > div {{ display: grid; justify-items: center; gap: 6px; padding: 12px 8px; border-radius: 12px; background: var(--card); color: #1E3B44; }}
.pair .alt svg {{ width: 44px; height: 44px; margin: 8px 0; }} .pair .neu svg {{ width: 60px; height: 60px; }}
.pair small {{ font-size: .75rem; color: #4A6670; font-weight: 600; }}
.gal {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin: 0; }}
.gal figure {{ margin: 0; background: var(--card); border-radius: 16px; padding: 12px 12px 10px; display: grid; gap: 4px; color: #1E3B44; }}
@media (max-width: 640px) {{ .gal {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
.gal svg {{ aspect-ratio: 1; }} .gal figcaption {{ font-size: .85rem; font-weight: 600; text-align: center; }}
.note {{ border-left: 4px solid var(--rose); padding: 4px 0 4px 16px; color: var(--ink-soft); max-width: 44em; }}
.note b {{ color: var(--ink); }}
.ctl {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 18px; }}
.ctl button {{ font: 600 .9rem var(--font); border: 1px solid var(--line); background: transparent; color: var(--ink); padding: 8px 14px; border-radius: 10px; cursor: pointer; }}
.ctl button[aria-pressed="true"] {{ background: var(--ink); color: var(--paper); border-color: var(--ink); }}
.ctl button:focus-visible {{ outline: 2px solid var(--rose); outline-offset: 2px; }}
body.ohne-stift .zg g {{ filter: none; }}
</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <filter id="stift" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.3" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="9" result="k"/>
    <feColorMatrix in="k" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.3 1.45" result="m"/>
    <feComposite in="d" in2="m" operator="in"/>
  </filter>
</defs></svg>
<main class="wrap">
  <header>
    <span class="kicker">Entwurf · Idee 79</span>
    <h1>Kinderzeichnungen statt Symbolen</h1>
    <p class="lead">So könnte die Seite aussehen, wenn an einigen Stellen gemalte Bilder statt der gleichförmigen Symbole stehen. Die Zeichnungen hier habe ich im Stil von Wachsmalstiften erzeugt. Später können echte Bilder der Kinder an ihre Stelle treten.</p>
  </header>

  <section class="sec">
    <h2>Auf der Startseite: die drei Bereiche</h2>
    <p>Die größte Wirkung haben die Zeichnungen bei den Bereichskarten. Sie bekommen damit ein eigenes Gesicht.</p>
    <div class="areas">
      {card("kind", "Kinderkrippe", "Für Kinder von 11 Monaten bis 3 Jahren, in kleinen Gruppen.", "")}
      {card("haus", "Kindergarten", "Von 3 Jahren bis zur Schule: spielen, entdecken, Freunde finden.", "")}
      {card("ranzen", "Kinderhort", "Nach der Schule: Hausaufgaben, Ruhe und Zeit zum Toben.", "")}
    </div>
  </section>

  <section class="sec">
    <h2>Bei den Schnellwegen: heute und gemalt</h2>
    <p>Links das Symbol, das heute auf der Seite steht, rechts die gemalte Fassung.</p>
    <div class="ctl" role="group" aria-label="Darstellung">
      <button type="button" id="b-stift" aria-pressed="true">Mit Wachsmalstift-Struktur</button>
      <button type="button" id="b-glatt" aria-pressed="false">Glatte Linien</button>
    </div>
    <div class="vgl">{vergleich}</div>
  </section>

  <section class="sec">
    <h2>Alle Motive</h2>
    <p>Acht Motive in den Farben der Seite: Rosé, Türkis, Petrol und Salbei, dazu ein warmes Ocker für die Sonne.</p>
    <div class="gal">{galerie}</div>
  </section>

  <p class="note"><b>Wie es weitergehen kann:</b> Gefallen Ihnen die Zeichnungen, baue ich sie bei den Bereichskarten und Schnellwegen ein. Noch schöner wäre es mit echten Bildern: Die Kinder malen die Motive auf Papier, und ich wandle die Fotos davon in saubere Linien um.</p>
</main>
<script>
(function () {{
  var a = document.getElementById("b-stift"), b = document.getElementById("b-glatt");
  function set(stift) {{ document.body.classList.toggle("ohne-stift", !stift); a.setAttribute("aria-pressed", stift); b.setAttribute("aria-pressed", !stift); }}
  a.addEventListener("click", function () {{ set(true); }}); b.addEventListener("click", function () {{ set(false); }});
}})();
</script>
'''
open(D + "kinderzeichnungen.html", "w", encoding="utf-8").write(html)
print("ok", len(html))
