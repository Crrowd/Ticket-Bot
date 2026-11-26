import re, html, json, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.lib.utils import simpleSplit

S = "/tmp/claude-0/-home-user-Ticket-Bot/3857ef81-ae33-5daf-8f34-2f2e0da75b55/scratchpad"
W = "/home/user/Ticket-Bot/kinderhort-website"
OUT = "/home/user/Ticket-Bot/Zeitangaben-pruefen.pdf"

# Schrift: Plus Jakarta Sans in zwei Stärken
for wght, name in ((400, "Jakarta"), (600, "JakartaB")):
    p = f"{S}/{name}.ttf"
    if not os.path.exists(p):
        f = TTFont(f"{W}/fonts/plus-jakarta-sans-latin-wght-normal.woff2"); f.flavor = None
        instancer.instantiateVariableFont(f, {"wght": wght}, inplace=True); f.save(p)
    pdfmetrics.registerFont(RLFont(name, p))

PETROL, ROSE, ROSE_S, SALBEI, PAPIER, TUERKIS = map(HexColor, ["#1E3B44", "#D4B5B0", "#F1E5E3", "#A8C5C0", "#F3F8F7", "#2D6A6A"])

# Inhalte aus der bestehenden Prüfseite
h = open(f"{S}/zeiten-quelle.html", encoding="utf-8").read()
fragen = [re.sub(r"<[^>]+>", "", html.unescape(x)) for x in re.findall(r"<li>(<b>.*?)</li>", h.split('class="fragen"')[1].split("</ol>")[0])]
abschnitte = []
for m in re.finditer(r"<section><h2>(.*?) <span>\d+</span></h2><ul>(.*?)</ul></section>", h, re.S):
    items = [html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<label[^>]*>(.*?)</label>", m.group(2), re.S)]
    abschnitte.append((m.group(1), items))

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Zeitangaben prüfen"); c.setAuthor("Kath. Kinder- und Jugendhort Grombühl e. V."); c.setSubject("Alle Uhrzeiten der Website zum Abhaken")
BW, BH = A4; L = 18 * mm; R = BW - 18 * mm; TEXTW = R - L - 12 * mm
y = BH - 20 * mm; seite = 1; nr = 0
form = c.acroForm

def fuss():
    c.setFont("Jakarta", 8); c.setFillColor(HexColor("#5A7177"))
    c.drawString(L, 10 * mm, "Kath. Kinder- und Jugendhort Grombühl e. V. · Zeitangaben der Website prüfen")
    c.drawRightString(R, 10 * mm, f"Seite {seite}")

def neue_seite():
    global y, seite
    fuss(); c.showPage(); seite += 1; y = BH - 20 * mm

def platz(nötig):
    if y - nötig < 18 * mm: neue_seite()

# Kopf
c.setFillColor(PETROL); c.setFont("JakartaB", 22); c.drawString(L, y - 6 * mm, "Zeitangaben prüfen"); y -= 12 * mm
c.setFont("Jakarta", 10)
for z in simpleSplit("Alle Uhrzeiten und Zeiträume, die gerade auf der Website stehen, nach Seiten sortiert. Stimmt eine Angabe, das Kästchen abhaken. Stimmt sie nicht, die richtige Zeit ins Feld daneben schreiben. Das geht direkt am Computer, Tablet oder Handy (z. B. in Adobe Acrobat Reader oder in der iPhone-App „Dateien“) und genauso auf Papier. Danach das PDF einfach zurückschicken.", "Jakarta", 10, R - L):
    c.drawString(L, y, z); y -= 13
y -= 6

# Rückfragen
zeilen = []
for i, f in enumerate(fragen, 1):
    zeilen += [(i, z) for z in simpleSplit(f, "Jakarta", 9.5, R - L - 14 * mm)]
kh = 18 + len(zeilen) * 12.5 + len(fragen) * 4 + 10
c.setFillColor(ROSE_S); c.roundRect(L, y - kh, R - L, kh, 8, stroke=0, fill=1)
c.setFillColor(PETROL); c.setFont("JakartaB", 11); c.drawString(L + 5 * mm, y - 15, "Drei Rückfragen"); yy = y - 30; last = 0
for i, z in zeilen:
    if i != last:
        c.setFont("JakartaB", 9.5); c.drawString(L + 5 * mm, yy, f"{i}."); last = i; yy -= 0
    c.setFont("Jakarta", 9.5); c.drawString(L + 10 * mm, yy, z); yy -= 12.5
    if zeilen.index((i, z)) + 1 < len(zeilen) and zeilen[zeilen.index((i, z)) + 1][0] != i: yy -= 4
y -= kh + 8 * mm

for titel, items in abschnitte:
    platz(30 * mm)
    c.setFillColor(SALBEI); c.roundRect(L, y - 8 * mm, R - L, 8 * mm, 6, stroke=0, fill=1)
    c.setFillColor(PETROL); c.setFont("JakartaB", 12); c.drawString(L + 4 * mm, y - 5.5 * mm, titel)
    c.setFont("Jakarta", 9); c.drawRightString(R - 4 * mm, y - 5.4 * mm, f"{len(items)} Angaben"); y -= 12 * mm
    for t in items:
        nr += 1
        z = simpleSplit(t, "Jakarta", 9.5, TEXTW)
        hoehe = len(z) * 12 + 22
        platz(hoehe + 4)
        form.checkbox(name=f"ok_{nr}", tooltip=f"Angabe {nr} stimmt", x=L, y=y - 13, size=12, buttonStyle="check",
                      borderColor=PETROL, fillColor=white, textColor=TUERKIS, borderWidth=1, forceBorder=True)
        c.setFillColor(PETROL); c.setFont("Jakarta", 9.5); yy = y - 9
        for zz in z: c.drawString(L + 7 * mm, yy, zz); yy -= 12
        c.setFont("Jakarta", 7.5); c.setFillColor(HexColor("#5A7177")); c.drawString(L + 7 * mm, yy - 5, "Richtig wäre:")
        form.textfield(name=f"korrektur_{nr}", tooltip=f"Korrektur zu Angabe {nr}", x=L + 25 * mm, y=yy - 9, width=R - L - 25 * mm, height=12,
                       fontName="Helvetica", fontSize=8, borderColor=HexColor("#C9D6D4"), fillColor=PAPIER, textColor=PETROL, borderWidth=.6, forceBorder=True)
        y = yy - 15
        c.setStrokeColor(HexColor("#DCE5E3")); c.setLineWidth(.5); c.line(L, y + 3, R, y + 3)
    y -= 6 * mm

platz(40 * mm)
c.setFillColor(PETROL); c.setFont("JakartaB", 11); c.drawString(L, y - 4 * mm, "Sonst noch etwas?"); y -= 8 * mm
form.textfield(name="sonstiges", tooltip="Weitere Anmerkungen", x=L, y=y - 28 * mm, width=R - L, height=26 * mm, fontName="Helvetica", fontSize=9,
               borderColor=HexColor("#C9D6D4"), fillColor=PAPIER, textColor=PETROL, borderWidth=.6, forceBorder=True, fieldFlags="multiline")
y -= 32 * mm
c.setFont("Jakarta", 9); c.setFillColor(PETROL); c.drawString(L, y, "Geprüft von: ____________________________      Datum: ______________")
fuss(); c.save()
print(OUT, nr, "Angaben,", seite, "Seiten")
