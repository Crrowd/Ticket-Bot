# Vorschau „Verbesserungen“ (21.11.2026): kleine HTML-Änderungen an der Startseite.
# 1 Link „Kind krankmelden“ im Startbereich unter den Knöpfen
# 4 Hinweisband nur, wenn der nächste Termin in höchstens 3 Tagen ist
def umbau(h, ziel="#krankmelden"):
    a = '<a class="btn btn-ghost" href="kontakt.html">Kontakt aufnehmen</a>\n      </div>'
    if a not in h:
        a = a.replace('href="kontakt.html"', 'href="#kontakt"')
    assert h.count(a) == 1, "hero-actions"
    h = h.replace(a, a + '\n      <a class="hero-krank" href="' + ziel + '"><span>Kind krankmelden</span> <span aria-hidden="true">→</span></a>', 1)
    b = "var nextEv = K.termine.filter(function (t) { return t.bis >= heute; })[0];"
    if b in h:
        h = h.replace(b, b + " if (nextEv && (parse(nextEv.von) - new Date()) / 864e5 > 3) nextEv = null;", 1)
    return h
