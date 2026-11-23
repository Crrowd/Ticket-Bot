# Vorschau „Verbesserungen 2“ (23.11.2026), baut auf „Kontakt kompakt“ auf:
#  1 Anschrift-Kasten nur mit Adresse, Route und „aufs Handy speichern“ (Telefon/E-Mail stehen oben)
#  3 Rundgang: kurze, eindeutige Bildtitel aus den vorhandenen Bildtexten („die Puppenecke“ → Titel „Puppenecke“, Text „im Gruppenraum“)
#   python3 entwurf/verbesserungen-2/build_vorschau.py <Zieldatei>
import os, re, sys, subprocess, html
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
ziel = sys.argv[1]; tmp = ziel + ".kk.html"
subprocess.run([sys.executable, os.path.join(W, "entwurf", "kontakt-kompakt", "build_vorschau.py"), tmp], check=True, stdout=subprocess.DEVNULL)
h = open(tmp, encoding="utf-8").read(); os.remove(tmp)

# 1 Anschrift ohne Telefon- und E-Mail-Zeile
a = h.index('<aside class="address-card'); b = h.index("</aside>", a)
card = h[a:b]
zeilen = re.findall(r'<div class="contact-row">.*?</button></div>', card, re.S)
weg = [z for z in zeilen if 'href="tel:' in z or 'href="mailto:' in z]
assert len(weg) == 2, len(weg)
for z in weg: card = card.replace(z, "", 1)
h = h[:a] + card + h[b:]

# 3 Bildtitel im Rundgang
ORT = {"Unser Gruppenraum": "im Gruppenraum", "Unser Kreativraum": "im Kreativraum", "Unser Spielflur": "im Spielflur", "Unser Flur": "im Flur"}
geaendert = []
def neu(m):
    fig = m.group(0)
    t = html.unescape(re.search(r'data-title="([^"]*)"', fig).group(1)); x = html.unescape(re.search(r'data-text="([^"]*)"', fig).group(1))
    if t not in ORT or len(x) > 40: return fig
    k = re.sub(r"^(die|der|das|ein|eine)\s+", "", x, flags=re.I)
    if k == x and not x.startswith(("Frühstücks", "Blick ")): return fig   # nur wo der Bildtext ein Ding benennt („die Bauecke“)
    nt = k[0].upper() + k[1:]; nx = ORT[t]
    geaendert.append((t, x, nt, nx))
    E = lambda s: html.escape(s, quote=True)
    fig = fig.replace(f'data-title="{E(t)}"', f'data-title="{E(nt)}"', 1).replace(f'data-text="{E(x)}"', f'data-text="{E(nx)}"', 1)
    fig = fig.replace(f'aria-label="{E(t)} – {E(x)} (Bild vergrößern)"', f'aria-label="{E(nt)} {E(nx)} (Bild vergrößern)"', 1)
    fig = fig.replace(f"<strong>{t}</strong><span>{x}</span>", f"<strong>{nt}</strong><span>{nx}</span>", 1)
    return fig
h = re.sub(r'<figure class="tour-item">.*?</figure>', neu, h, flags=re.S)
h = h.replace("<title>Kontakt kompakt</title>", "<title>Verbesserungen 2</title>", 1)
open(ziel, "w", encoding="utf-8").write(h)
for g in geaendert: print("  %-18s %-28s → %s (%s)" % g)
print(len(geaendert), "Bildtitel geändert")
