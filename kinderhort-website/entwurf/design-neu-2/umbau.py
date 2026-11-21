# Entwurf „Design neu 2“: verschiebt Status-Karte und „Kind krankmelden“ aus dem Startbereich
# in den Abschnitt „Termine & Unterlagen“ (über die Wochenübersicht). Sonst bleibt das HTML gleich.
import re

def _block(h, start_pat, tag):
    m = re.search(start_pat, h)
    assert m, start_pat
    i = m.start(); depth = 0
    for t in re.finditer(r"<(/?)" + tag + r"\b[^>]*>", h[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return i, i + t.end()
    raise ValueError(start_pat)

def umbau(h):
    a, b = _block(h, r'<div class="status-card" id="status"', "div")
    status = h[a:b]; h = h[:a] + h[b:]
    a, b = _block(h, r'<details class="krank in-hero" id="krankmelden"', "details")
    krank = h[a:b].replace('class="krank in-hero"', 'class="krank in-heute"', 1); h = h[:a] + h[b:]
    ziel = '<div class="woche reveal" data-woche'
    assert h.count(ziel) == 1
    return h.replace(ziel, '<div class="heute">' + status + krank + '</div>\n    ' + ziel, 1)
