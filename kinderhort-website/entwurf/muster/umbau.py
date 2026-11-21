# Vorschau „Weniger Vorlage“ (21.11.2026): HTML-Änderungen nur auf der Startseite (#seite-index in der Vorschau)
import re
def _start(h):
    a = h.index('id="seite-index"'); a = h.rindex("<div", 0, a)
    b = h.index('<div class="spa-page', a + 10)
    return a, b

def startseite(s):
    # 1 Etiketten, die nur die Überschrift wiederholen, entfallen
    for k in ["Das zeichnet uns aus", "Virtueller Rundgang", "Aktuelles", "Schließtage"]:
        t = '<span class="kicker">' + k + '</span>'
        assert s.count(t) == 1, k; s = s.replace(t, "")
    # 4 Zahlenreihe als ein Satz mit den Zahlen in Fett
    a = s.index('<div class="stats three">'); b = s.index('<div class="teasers">', a)
    s = s[:a] + ('<p class="fakten reveal">Wir öffnen um <b>6:45 Uhr</b>, der Hort betreut bis <b>18:00 Uhr</b>, auch in den Ferien. '
                 'Geschlossen ist an <b>höchstens 30 Tagen</b> im Jahr, gleich in allen Abteilungen. '
                 'Und <b>zwei Köchinnen</b> kochen jeden Tag frisch mit regionalen Zutaten.</p>\n    ') + s[b:]
    # 7 genauere Linktexte unter den Bereichskarten
    for name, ziel in [("Kinderkrippe", "Zur Kinderkrippe"), ("Kindergarten", "Zum Kindergarten"), ("Kinderhort", "Zum Kinderhort")]:
        m = re.search(r'(<h3>' + name + r'</h3><p>.*?</p><span class="more">)Mehr erfahren', s, re.S)
        assert m, name; s = s[:m.start()] + m.group(1) + ziel + s[m.end():]
    return s

def umbau(h):
    a, b = _start(h)
    return h[:a] + startseite(h[a:b]) + h[b:]
