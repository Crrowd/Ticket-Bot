# Aushang A4 mit drei QR-Codes (Website, Kind krankmelden, Termine abonnieren) als HTML zum Drucken.
# Braucht das Python-Paket „qrcode“.   python3 entwurf/aushang/aushang.py   → entwurf/aushang/aushang.html
import os, io, base64, qrcode, qrcode.image.svg
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
SITE = "https://kinderhort-grombuehl.de/"
CODES = [
    ("Unsere Website", "Termine, Schließtage, Fragen und Kontakt", SITE, "kinderhort-grombuehl.de"),
    ("Kind krankmelden", "Gruppe anrufen oder E-Mail mit Vorlage", SITE + "kontakt.html#schnell", "kinderhort-grombuehl.de › Kind krankmelden"),
    ("Termine im Handy", "Kalender abonnieren – neue Termine kommen von selbst", "webcal://kinderhort-grombuehl.de/downloads/termine.ics", "Termine abonnieren"),
]
def svg(data):
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    b = io.BytesIO(); img.save(b); s = b.getvalue().decode()
    s = s[s.index("<svg"):].replace('fill="#000000"', 'fill="#1E3B44"')
    return s
font = base64.b64encode(open(os.path.join(W, "fonts/plus-jakarta-sans-latin-wght-normal.woff2"), "rb").read()).decode()
logo = base64.b64encode(open(os.path.join(W, "img/favicon.svg"), "rb").read()).decode()
karten = "".join(f'<div class="code"><div class="qr">{svg(u)}</div><div><h2>{t}</h2><p>{s}</p><p class="url">{z}</p></div></div>' for t, s, u, z in CODES)
html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Aushang mit QR-Codes</title>
<style>
@font-face {{ font-family: "PJS"; src: url(data:font/woff2;base64,{font}) format("woff2"); font-weight: 200 800; }}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{ font-family: "PJS", system-ui, sans-serif; color: #1E3B44; background: #fff; }}
.blatt {{ width: 210mm; height: 297mm; padding: 18mm 18mm 14mm; display: flex; flex-direction: column; background: #F3F8F7; }}
.kopf {{ display: flex; align-items: center; gap: 6mm; }}
.kopf img {{ width: 20mm; height: 20mm; }}
.kopf p {{ margin: 0; font-size: 11pt; font-weight: 600; line-height: 1.3; }}
h1 {{ font-size: 34pt; line-height: 1.05; letter-spacing: -.03em; margin: 9mm 0 3mm; }}
.lead {{ font-size: 14pt; margin: 0 0 8mm; max-width: 150mm; }}
.codes {{ display: grid; gap: 6mm; flex: 1; align-content: start; }}
.code {{ display: grid; grid-template-columns: 46mm 1fr; gap: 9mm; align-items: center; background: #fff; border-radius: 6mm; padding: 5mm; box-shadow: 0 0 0 .3mm rgb(30 59 68 / .15); }}
.qr svg {{ width: 46mm; height: 46mm; display: block; }}
.code h2 {{ margin: 0 0 2mm; font-size: 20pt; letter-spacing: -.02em; }}
.code p {{ margin: 0; font-size: 12pt; line-height: 1.4; }}
.code .url {{ margin-top: 3mm; font-size: 10pt; font-weight: 600; color: #2D6A6A; }}
.fuss {{ display: flex; justify-content: space-between; align-items: end; gap: 8mm; margin-top: 8mm; padding-top: 5mm; border-top: .4mm solid #D4B5B0; font-size: 10.5pt; }}
.fuss b {{ font-size: 13pt; }}
</style></head><body>
<div class="blatt">
  <div class="kopf"><img src="data:image/svg+xml;base64,{logo}" alt=""><p>Kath. Kinder- und Jugendhort<br>Grombühl e. V.</p></div>
  <h1>Alles Wichtige<br>auf dem Handy</h1>
  <p class="lead">Kamera auf den Code halten – fertig. Kein App-Download nötig.</p>
  <div class="codes">{karten}</div>
  <div class="fuss"><div><b>0931 2789892 0</b><br>Montag bis Freitag ab 6:45 Uhr</div><div>Lindleinstraße 20, 97080 Würzburg</div></div>
</div>
</body></html>'''
open(os.path.join(H, "aushang.html"), "w", encoding="utf-8").write(html)
print("aushang.html", len(html) // 1024, "KB")
