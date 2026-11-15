# Erzeugt die statischen HTML-Seiten der Kinderhort-Webseite.
import os, re, html, csv, json, datetime as dt
from urllib.parse import quote
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
ORG = "Kath. Kinder- und Jugendhort Grombühl e. V."
SITE = "https://kinderhort-grombuehl.de/"   # Adresse, unter der die Seite veröffentlicht wird
MAIL = "kinderhort.grombuehl@t-online.de"
e = html.escape

# ---------- Daten aus daten/*.csv ----------
def read_csv(name):
    with open(os.path.join(W, "daten", name), encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter=";") if any((v or "").strip() for v in r.values())]

def d(s):
    return dt.datetime.strptime(s.strip(), "%d.%m.%Y").date()

SCHLIESSTAGE = read_csv("schliesstage.csv")
TERMINE = read_csv("termine.csv")
FEIERTAGE = read_csv("feiertage.csv")
PLAN_JAHR = f"{d(SCHLIESSTAGE[0]['erster Schließtag']).year}/{d(SCHLIESSTAGE[-1]['letzter Schließtag']).year}"

def mailto(subject, body):
    return f"mailto:{MAIL}?subject={quote(subject)}&body={quote(body)}"

KRANK_MAIL = mailto("Krankmeldung / Abwesenheit", "Liebes Team,\n\nunser Kind kann leider nicht in die Einrichtung kommen.\n\nName des Kindes: \nGruppe / Bereich: \nAbwesend von – bis: \nGrund (freiwillig): \n\nViele Grüße\n")
PLATZ_MAIL = mailto("Platzanfrage", "Liebes Team,\n\nwir interessieren uns für einen Platz in Ihrer Einrichtung.\n\nName des Kindes: \nGeburtsdatum: \nGewünschter Bereich (Krippe / Kindergarten / Hort): \nGewünschter Beginn: \nGewünschte Betreuungszeiten: \nName der Eltern: \nTelefon: \n\nViele Grüße\n")

_dims = {}
def dims(src):
    if src not in _dims:
        with Image.open(os.path.join(W, src)) as im:
            _dims[src] = im.size
    return _dims[src]

def webp(src):
    """Erzeugt WebP-Fassungen (volle Größe + 800 px) und liefert das srcset."""
    if not src.endswith(".jpg"):
        return ""
    base = src[:-4]
    full, small = os.path.join(W, base + ".webp"), os.path.join(W, base + "-800.webp")
    if not os.path.exists(full) or not os.path.exists(small):
        with Image.open(os.path.join(W, src)) as im:
            im = im.convert("RGB")
            im.save(full, "WEBP", quality=74, method=6)
            sm = im.copy(); sm.thumbnail((800, 800)); sm.save(small, "WEBP", quality=74, method=6)
    w, _ = dims(src)
    sw = min(800, w) if w >= dims(src)[1] else int(800 * w / dims(src)[1])
    return f"{base}-800.webp {sw}w, {base}.webp {w}w"

_lqip = {}
def lqip(src):
    """Winzige, unscharfe Vorschau als Hintergrund, bis das Bild geladen ist."""
    if not src.endswith(".jpg"):
        return ""
    if src not in _lqip:
        import io, base64
        with Image.open(os.path.join(W, src)) as im:
            im = im.convert("RGB"); im.thumbnail((16, 16))
            buf = io.BytesIO(); im.save(buf, "WEBP", quality=35)
        _lqip[src] = base64.b64encode(buf.getvalue()).decode()
    return f' style="background-image:url(data:image/webp;base64,{_lqip[src]})"'

def img(src, alt="", cls="", lazy=True, extra="", sizes="(max-width: 900px) 100vw, 50vw"):
    w, h = dims(src)
    cls = (cls + " ph").strip() if src.endswith(".jpg") else cls
    extra += lqip(src)
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    ss = webp(src)
    sset = f' srcset="{ss}" sizes="{sizes}"' if ss else ""
    return f'<img src="{src}"{sset} alt="{e(alt)}" width="{w}" height="{h}"{c}{l}{extra}>'

# ---------- Icons ----------
def icon(name, size=24):
    p = {
        "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><circle cx="17.5" cy="9" r="2.6"/><path d="M16.5 14.6c2.6.2 4.4 1.9 5 4.9"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
        "pot": '<path d="M4 10h16v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M2 10h20M9 6c0-1.5 1-1.5 1-3M14 6c0-1.5 1-1.5 1-3"/>',
        "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "left": '<path d="M15 5l-7 7 7 7"/>',
        "right": '<path d="M9 5l7 7-7 7"/>',
        "down": '<path d="M6 9l6 6 6-6"/>',
        "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
        "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        "play": '<path d="M8 5.5v13l10.5-6.5z"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.8-3.8"/>',
        "copy": '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        "share": '<path d="M12 15V3M7 8l5-5 5 5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
        "list": '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
        "grid": '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M9 9v12M15 9v12M3 15h18"/>',
        "home": '<path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z"/>',
    }[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

def bunting(colors=("#D4B5B0", "#A8C5C0", "#D4B5B0", "#F3F8F7"), n=18, bg=None):
    # Wimpelkette angelehnt an das Logo
    w = 1200
    step = w / n
    parts = []
    if bg:
        parts.append(f'<rect width="{w}" height="46" fill="{bg}"/>')
    parts.append(f'<path d="M0 6 Q {w/2} 22 {w} 6" fill="none" stroke="#D4B5B0" stroke-width="1.5" opacity=".7"/>')
    for i in range(n):
        x0 = i * step + 4
        x1 = x0 + step - 8
        t0 = (x0 / w); t1 = (x1 / w)
        y0 = 6 + 16 * 4 * t0 * (1 - t0) * 0.5 * 2
        y1 = 6 + 16 * 4 * t1 * (1 - t1) * 0.5 * 2
        xm = (x0 + x1) / 2
        ym = (y0 + y1) / 2 + 26
        c = colors[i % len(colors)]
        parts.append(f'<path class="flag" d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f} L{xm:.1f} {ym:.1f} Z" fill="{c}"/>')
    return f'<svg class="bunting" viewBox="0 0 {w} 46" preserveAspectRatio="none" aria-hidden="true">{"".join(parts)}</svg>'

BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true">'
              '<circle cx="24" cy="24" r="23" fill="#1E3B44"/>'
              '<path d="M6 17 Q24 25 42 17" fill="none" stroke="#fff" stroke-width="1.6"/>'
              '<path d="M9 18.3 L15 21 L11.2 29Z" fill="#D4B5B0"/>'
              '<path d="M16.5 21.6 L22.5 23 L19 31.5Z" fill="#A8C5C0"/>'
              '<path d="M24.5 23 L30.5 21.8 L28.6 31.4Z" fill="#D4B5B0"/>'
              '<path d="M32 21.3 L38.5 18.4 L37.6 28.3Z" fill="#A8C5C0"/>'
              '</svg>')

NAV = [
    ("index.html", "Startseite"),
    ("BEREICHE", "Bereiche"),
    ("aktuelles.html", "Aktuelles"),
    ("downloads.html", "Downloads"),
    ("kontakt.html", "Kontakt"),
]
BEREICHE = [
    ("krippe", "kinderkrippe.html", "Kinderkrippe", "ab 11 Monaten · Sonnen- &amp; Sternengruppe", "img/p2160110.jpg"),
    ("kiga", "kindergarten.html", "Kindergarten", "3 Jahre bis Einschulung · Bären, Bienen, Spatzen", "img/blick-vom-fenster-in-den-raum.jpg"),
    ("hort", "kinderhort.html", "Kinderhort", "ab der Einschulung · alle Schulformen", "img/kreatviraum-5-1.jpg"),
]
MEGA_LINKS = [("ueberblick", "Zielgruppe &amp; Öffnungszeiten"), ("raeume", "Räumlichkeiten"), ("rundgang", "Virtueller Rundgang"),
              ("tagesablauf", "Tagesablauf"), ("fragen", "Häufige Fragen")]

def mega(active):
    pages = [x[1] for x in BEREICHE]
    default = BEREICHE[pages.index(active)][0] if active in pages else "krippe"
    cols = "".join(
        f'<div class="mega-col c-{k}"><a class="mega-title" href="{h}"{' aria-current="page"' if h == active else ""}>{t}<small>{sub}</small></a>'
        + "<ul>" + "".join(f'<li><a href="{h}#{a}">{l}</a></li>' for a, l in MEGA_LINKS) + "</ul></div>"
        for k, h, t, sub, _ in BEREICHE)
    visual = "".join(
        f'<figure class="v-{k}{" def" if k == default else ""}">{img(im, "", sizes="320px")}<figcaption>{t}<small>{sub}</small></figcaption></figure>'
        for k, h, t, sub, im in BEREICHE)
    return f'<div class="mega"><div class="mega-cols">{cols}</div><div class="mega-visual" aria-hidden="true">{visual}</div></div>'

NAV_EXTRA = ('<li class="nav-extra">'
    f'<figure class="nav-photo">{img("img/p2160110.jpg", "", sizes="360px")}</figure>'
    '<p class="nav-extra-title">Wir sind für Sie da</p>'
    f'<a class="nav-quick" href="tel:+4993127898920">{icon("phone", 20)}<span>0931&nbsp;2789892&nbsp;0<small>Anrufen, Mo–Fr ab 6:45 Uhr</small></span></a>'
    f'<a class="nav-quick" href="mailto:kinderhort.grombuehl@t-online.de">{icon("mail", 20)}<span>E-Mail schreiben<small>kinderhort.grombuehl@t-online.de</small></span></a>'
    f'<p class="nav-addr">{icon("pin", 18)}<span>Lindleinstraße 20, 97080 Würzburg</span></p>'
    '</li>')

def header(active):
    items = []
    for href, label in NAV:
        if href == "BEREICHE":
            inside = active in [x[1] for x in BEREICHE]
            items.append(
                f'<li class="has-drop"><button class="drop-toggle{" current" if inside else ""}" type="button" aria-expanded="false" aria-haspopup="true">'
                f'Bereiche {icon("down", 16)}</button>{mega(active)}</li>')
            continue
        cur = ' aria-current="page"' if href == active else ""
        cls = ' class="nav-cta"' if href == "kontakt.html" else ""
        badge = '<span class="nav-badge" aria-hidden="true"></span>' if href == "aktuelles.html" else ""
        items.append(f'<li><a href="{href}"{cls}{cur}>{label}{badge}</a></li>')
    return f'''<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html">
      {BRAND_MARK}
      <span class="brand-text"><span class="b-pre">Kath. Kinder- und Jugendhort</span> <span class="b-name">Grombühl e. V.</span></span>
    </a>
    <div class="open-wrap" hidden>
      <button class="open-pill" type="button" aria-expanded="false" aria-controls="oeffnung-pop"><span class="open-dot" aria-hidden="true"></span><span class="open-txt"></span></button>
      <div class="open-pop" id="oeffnung-pop" role="dialog" aria-label="Öffnungszeiten heute" hidden></div>
    </div>
    <nav class="main-nav" id="hauptmenue" aria-label="Hauptnavigation">
      <ul>
        {"".join(items)}
        {NAV_EXTRA}
      </ul>
    </nav>
    <button class="search-btn js-search" type="button" aria-keyshortcuts="Control+K">{icon("search", 18)}<span>Suche</span><kbd aria-hidden="true">Strg K</kbd></button>
    <button class="nav-toggle" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="hauptmenue"><span></span></button>
  </div>
</header>'''

MOBILE_BAR = f'''<nav class="mobile-bar no-print" aria-label="Schnellzugriff">
  <a href="tel:+4993127898920">{icon("phone", 22)}<span>Anrufen</span></a>
  <a href="{KRANK_MAIL}">{icon("mail", 22)}<span>Krankmelden</span></a>
  <a href="aktuelles.html#termine" class="cal-target">{icon("calendar", 22)}<span>Termine</span><span class="nav-badge" aria-hidden="true"></span></a>
  <button type="button" class="js-search">{icon("search", 22)}<span>Suche</span></button>
</nav>'''


FOOTER = f'''<footer class="site-footer">
  {bunting(bg=None)}
  <div class="container">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="img/logo.png" alt="Logo {ORG}" width="1030" height="608" loading="lazy">
        <p>Kinderkrippe • Kindergarten • Kinderhort<br><span class="footer-claim">Weil Qualität zählt!</span></p>
      </div>
      <div>
        <h2 class="foot-title">Anschrift</h2>
        <p>{ORG}<br>Lindleinstraße 20<br>97080 Würzburg</p>
      </div>
      <div>
        <h2 class="foot-title">Kontakt</h2>
        <ul>
          <li><a href="tel:+4993127898920">0931&nbsp;2789892&nbsp;0</a></li>
          <li><a href="mailto:kinderhort.grombuehl@t-online.de">kinderhort.grombuehl@t-online.de</a></li>
          <li><a href="kontakt.html">Alle Durchwahlen</a></li>
          <li><a href="{KRANK_MAIL}">Kind krankmelden</a></li>
        </ul>
      </div>
      <div>
        <h2 class="foot-title">Seiten</h2>
        <ul>
          <li><a href="kinderkrippe.html">Kinderkrippe</a></li>
          <li><a href="kindergarten.html">Kindergarten</a></li>
          <li><a href="kinderhort.html">Kinderhort</a></li>
          <li><a href="aktuelles.html">Aktuelles</a></li>
          <li><a href="downloads.html">Downloads</a></li>
          <li><button type="button" class="link-btn js-app">Als App aufs Handy</button></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> {ORG}</span>
      <span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span>
    </div>
  </div>
</footer>'''


# ---------- Fachbegriffe (Erklärungen bitte vom Hort prüfen lassen) ----------
GLOSSAR = {
    "BayKiBiG": "Bayerisches Kinderbildungs- und -betreuungsgesetz. Es regelt unter anderem die Förderung der Kitas und erlaubt bis zu 30 Schließtage im Jahr.",
    "Inhouseschulungen": "Fortbildungen, die im eigenen Haus für das ganze Team gemeinsam stattfinden.",
    "Portfolio": "Eine Mappe, in der die Entwicklung Ihres Kindes mit Fotos, Bildern und Beobachtungen festgehalten wird.",
    "Vorkurs Deutsch": "Zusätzliche, schulvorbereitende Förderung für Vorschulkinder in Grammatik, Sprachverständnis und Wortschatz.",
    "Fachkraftquote": "Anteil der Mitarbeitenden mit pädagogischer Fachausbildung. 100 Prozent heißt: nur staatlich anerkannte Erzieherinnen und Erzieher.",
    "Partizipationsmöglichkeiten": "Wege, auf denen die Kinder ihren Alltag mitbestimmen, zum Beispiel in der Kinderkonferenz.",
    "Kinderkonferenz": "Wöchentliche Runde, in der die Hortkinder Themen besprechen und zum Beispiel Ausflüge und Ferienpläne abstimmen.",
    "Mindestbuchungszeit": "Die kürzeste Betreuungszeit pro Tag, die Sie buchen können.",
    "Projektarbeit": "Die Kinder wählen ein Thema nach ihren Interessen und erarbeiten es über längere Zeit gemeinsam.",
}

def glossar(body):
    """Markiert pro Seite das erste Vorkommen jedes Fachbegriffs in Fließtext (nicht in Überschriften, Links, Knöpfen)."""
    for term in GLOSSAR:
        for m in re.finditer(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", body):
            pos = m.start()
            if body.rfind("<", 0, pos) > body.rfind(">", 0, pos):
                continue   # steht in einem Tag
            tags = re.findall(r"<(/?)([a-z0-9]+)", body[:pos])
            stack = []
            for close, name in tags:
                if name in ("br", "img", "input", "meta", "link", "source", "hr"):
                    continue
                if close:
                    while stack and stack.pop() != name:
                        pass
                else:
                    stack.append(name)
            if not stack or stack[-1] not in ("p", "li", "span", "div", "blockquote"):
                continue
            if set(stack) & {"h1", "h2", "h3", "h4", "a", "button", "summary", "strong", "label", "small", "script", "title", "figcaption", "time"}:
                continue
            btn = f'<button type="button" class="term" data-term="{term}" aria-haspopup="dialog">{term}</button>'
            body = body[:pos] + btn + body[m.end():]
            break
    return body

def page(fname, title, desc, active, body, theme="", head=""):
    body = glossar(body)
    full_title = f"{title} – {ORG}" if title else f"{ORG} – Weil Qualität zählt!"
    bcls = f' class="{theme}"' if theme else ""
    doc = f'''<!DOCTYPE html>
<html lang="de" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">
<script>(function (c) {{ try {{ if (localStorage.getItem("hinweis-aus")) c += " no-hint"; }} catch (e) {{}} document.documentElement.className = c; }})("js");</script>
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#A8C5C0">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:url" content="{SITE}{'' if fname == 'index.html' else fname}">
<meta property="og:image" content="{SITE}img/og-bild.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}{'' if fname == 'index.html' else fname}">{head}
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Kinderhort">
<link rel="preload" href="fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body{bcls}>
{header(active)}
<main id="inhalt">
{body}
</main>
{FOOTER}
{MOBILE_BAR}
<script type="speculationrules">{{"prerender":[{{"where":{{"selector_matches":"a[href$='.html'], a[href*='.html#']"}},"eagerness":"moderate"}}]}}</script>
<script src="js/daten.js" defer></script>
<script src="js/main.js" defer></script>
</body>
</html>
'''
    doc = "\n".join(line.rstrip() for line in doc.split("\n"))
    with open(os.path.join(W, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES_WRITTEN.append(fname)

PAGES_WRITTEN = []

# ---------- Bausteine ----------
def page_hero(title, sub, image, kicker, links=None, alt=""):
    sn = ""
    if links:
        sn = '\n<nav class="subnav no-print" aria-label="Auf dieser Seite"><div class="container"><ul>' + "".join(
            f'<li><a href="#{a}">{l}</a></li>' for a, l in links) + "</ul></div></nav>"
    return f'''<section class="page-hero">
  <div class="container">
    <div class="page-hero-card">
      {img(image, alt or title, lazy=False, sizes="100vw")}
      <div class="page-hero-content">
        <span class="eyebrow">{kicker}</span>
        <h1>{title}</h1>
        <p>{sub}</p>
      </div>
    </div>
  </div>
</section>{sn}'''

def simple_hero(title, sub, kicker):
    return f'''<section class="page-hero simple">
  <div class="container">
    <div class="page-hero-card">
      <div class="page-hero-content">
        <span class="eyebrow">{kicker}</span>
        <h1>{title}</h1>
        <p>{sub}</p>
      </div>
    </div>
  </div>
</section>'''

def info_cards(cards):
    out = []
    for ic, title, big, text in cards:
        b = f'<span class="big">{big}</span>' if big else ""
        out.append(f'<div class="info-card reveal"><div class="icon">{icon(ic, 28)}</div><h3>{title}</h3>{b}{text}</div>')
    return '<div class="info-grid">' + "".join(out) + "</div>"

def rooms(items):
    """Räume mit Foto im Zweierraster; bei ungerader Zahl wird der letzte breit.
    Räume ohne Foto folgen gesammelt in einer eigenen Zeile – so steht nichts allein."""
    pics = [r for r in items if r[2]]
    texts = [r for r in items if not r[2]]
    out = []
    for n, (name, text, image) in enumerate(pics):
        wide = " wide" if len(pics) % 2 and n == len(pics) - 1 else ""
        out.append(f'<article class="room{wide} reveal">{img(image, name)}<div class="txt"><h3>{name}</h3><p>{text}</p></div></article>')
    html = '<div class="rooms">' + "".join(out) + "</div>"
    if texts:
        html += f'<div class="rooms rooms-text n{len(texts)}">' + "".join(
            f'<article class="room no-img reveal"><div class="txt"><h3>{name}</h3><p>{text}</p></div></article>' for name, text, _ in texts) + "</div>"
    return html

def tour(group, items):
    figs = []
    for i, (image, title, text) in enumerate(items):
        figs.append(
            f'<figure class="tour-item"><button type="button" data-full="{image}" data-group="{group}" '
            f'data-title="{e(title)}" data-text="{e(text)}" aria-label="{e(title)} – {e(text)} (Bild vergrößern)">'
            f'{img(image, title + " – " + text)}</button>'
            f'<figcaption><strong>{title}</strong><span>{text}</span></figcaption></figure>')
    return f'''<div class="tour">
  <div class="tour-controls">
    <span class="count" aria-live="polite"></span>
    <button class="btn btn-ghost story-open" type="button" data-group="{group}">{icon("play", 18)} Als Geschichte ansehen</button>
    <button class="round-btn tour-prev" type="button" aria-label="Zurück">{icon("left")}</button>
    <button class="round-btn tour-next" type="button" aria-label="Weiter">{icon("right")}</button>
  </div>
  <div class="tour-track" tabindex="0" aria-label="Bilder des virtuellen Rundgangs">
    {"".join(figs)}
  </div>
</div>'''

def timeline(rows):
    out = []
    for r in rows:
        if isinstance(r, str):
            out.append(f'</ol><h3 class="timeline-sub">{r}</h3><ol class="timeline">')
        else:
            t, txt = r
            out.append(f'<li><time>{t}</time><div class="tl-body">{txt}</div></li>')
    return '<ol class="timeline">' + "".join(out) + "</ol>"

def features(items, groups=None):
    if not groups:
        return '<ul class="features">' + "".join(f'<li class="reveal">{x}</li>' for x in items) + "</ul>"
    assert sorted(n for _, idx in groups for n in idx) == list(range(len(items))), "Jeder Punkt muss genau einer Gruppe zugeordnet sein"
    return '<div class="feature-groups">' + "".join(
        f'<div class="feature-group reveal"><h3>{t}</h3><ul class="features">' + "".join(f"<li>{items[n]}</li>" for n in idx) + "</ul></div>"
        for t, idx in groups) + "</div>"

def faq(items):
    out = []
    for q, a in items:
        out.append(f'<details class="reveal"><summary>{q}</summary><div><p>{a}</p></div></details>')
    search = ('<div class="faq-search reveal"><label class="visually-hidden" for="faq-suche">Fragen durchsuchen</label>'
              f'{icon("search", 20)}<input type="search" id="faq-suche" placeholder="Frage suchen, z. B. Brotzeit, Ferien, Windeln" autocomplete="off" enterkeyhint="search">'
              '<span class="faq-count" aria-live="polite"></span></div>'
              '<p class="faq-empty muted" hidden>Keine passende Frage gefunden. Rufen Sie uns gern an: 0931 2789892 0.</p>')
    return '<div class="faq">' + search + "".join(out) + "</div>"

def section(id_, kicker, title, intro, content, cls="", center=False):
    i = f"<p>{intro}</p>" if intro else ""
    c = " center" if center else ""
    idattr = f' id="{id_}"' if id_ else ""
    return f'''<section class="section {cls}"{idattr}>
  <div class="container">
    <div class="section-head{c}"><span class="kicker">{kicker}</span><h2>{title}</h2>{i}</div>
    {content}
  </div>
</section>'''

# ---------- Ferienplan ----------
PLAN = [(r["Anlass"], r["geöffnet bis"], r["erster Schließtag"], r.get("Hinweis erster Tag", ""),
         r["letzter Schließtag"], r.get("Hinweis letzter Tag", ""), r["wieder geöffnet"], int(r["Schließtage"]))
        for r in SCHLIESSTAGE]

def plan_table():
    rows = []
    for name, open_until, first, fn, last, ln, reopen, n in PLAN:
        f = first + (f"<small>({fn})</small>" if fn else "")
        l = last + (f"<small>({ln})</small>" if ln else "")
        rows.append(f"<tr><th scope=\"row\">{name}</th><td>{open_until}</td><td>{f}</td><td>{l}</td><td>{reopen}</td><td class=\"num\">{n:02d}</td></tr>")
    total = sum(p[-1] for p in PLAN)
    return f'''<div class="table-wrap reveal" tabindex="0" role="region" aria-label="Ferienplan – Tabelle, seitlich scrollbar">
<table class="plan">
  <caption>Die Ferienzeiten Ihres Kindes für Krippe, Kindergarten und Kinderhort im Jahr {PLAN_JAHR}</caption>
  <thead><tr><th scope="col">Wann?</th><th scope="col">Wir haben geöffnet bis …</th><th scope="col">Erster Schließtag</th><th scope="col">Letzter Schließtag</th><th scope="col">Wir öffnen wieder am …</th><th scope="col" class="num">Schließtage</th></tr></thead>
  <tbody>{"".join(rows)}</tbody>
  <tfoot><tr><td colspan="5">Schließtage gesamt</td><td class="num">{total}</td></tr></tfoot>
</table>
</div>
<p class="plan-note">Damit Sie rechtzeitig Ihre Urlaubspläne schmieden können: Kinderkrippe, Kindergarten und Kinderhort haben die gleichen Schließtage.
<a href="downloads/Ferienplan_2026_27.pdf">Ferienplan als PDF herunterladen</a> ·
<a href="img/schliesstage-2026-2027.jpg" data-full="img/schliesstage-2026-2027.jpg" data-group="plan" data-title="Ferienplan 2026/2027" data-text="Original-Aushang mit Schließtagen und Vormerkterminen">Original-Aushang ansehen</a></p>
<div class="btn-row no-print">
  <a class="btn btn-primary" href="downloads/schliesstage.ics" download>{icon("calendar", 20)} Schließtage in meinen Kalender</a>
  <button class="btn btn-ghost js-print-plan" type="button">{icon("file", 20)} Ferienplan drucken</button>
</div>'''

def ferienplan_section(cls="alt"):
    return section("ferienplan", "Ferienplan", f"Schließtage {PLAN_JAHR}",
                   "In allen Abteilungen des Hauses haben wir an maximal 30 gleichen Tagen im Jahr geschlossen.",
                   '<div class="yearline reveal" data-yearline></div>' + plan_table(), cls=cls)

def abc_section(name, link_text):
    return f'''<section class="section tight">
  <div class="container">
    <div class="cta-band reveal">
      <div><h2>{name}</h2><p>Das {name} finden Sie in unserem Downloadbereich – mit allen wichtigen Infos von A bis Z.</p></div>
      <div class="actions"><a class="btn btn-accent" href="downloads.html">{icon("file", 20)} {link_text}</a></div>
    </div>
  </div>
</section>'''

KUECHE = ("Zwei Köchinnen bereiten täglich in der hauseigenen Küche des Hortes frisch und aus regionalen Zutaten "
          "ein kindgerechtes warmes Mittagessen nach den neuesten ernährungswissenschaftlichen Grundsätzen zu.")
WEISSER_RAUM = ("Dieser Raum steht ganz im Zeichen der Ruhe und Entspannung. Hier können die Kinder auf dem Wasserbett träumen, "
                "unter dem Lichtwasserfall entspannen und auf einer Sofalandschaft die Farbreflexe der Wassersäulen beobachten. "
                "Regelmäßig können Kinder in diesem Raum bei Traumreisen und autogenem Training mitmachen.")

MONATE = ["Jan", "Feb", "März", "Apr", "Mai", "Juni", "Juli", "Aug", "Sep", "Okt", "Nov", "Dez"]
def ev(r):
    a, b = d(r["von"]), d(r["bis"] or r["von"])
    day = f"{a.day:02d}" if a == b else (f"{a.day:02d}.–{b.day:02d}." if a.month == b.month else f"{a.day:02d}.{a.month:02d}.–")
    mon = f"{MONATE[b.month - 1]} {b.year}"
    key = f'{a.isoformat()}|{r["Titel"]}'
    return (f'<li class="event reveal" data-ende="{b.isoformat()}" data-von="{a.isoformat()}" data-titel="{e(r["Titel"])}" data-text="{e(r["Beschreibung"])}">'
            f'<div class="date"><b>{day}</b><span>{mon}</span></div>'
            f'<p><strong>{e(r["Titel"])}</strong>{e(r["Beschreibung"])}</p>'
            f'<div class="ev-acts"><button class="save" type="button" aria-pressed="false" data-key="{e(key)}" aria-label="{e(r["Titel"])} merken">'
            f'<span class="a">Merken</span><span class="b" aria-hidden="true">{icon("check", 16)} Gemerkt</span></button>'
            f'<button class="share" type="button" aria-label="{e(r["Titel"])} teilen">{icon("share", 18)}</button></div></li>')

STATUS_CARD = f'''<div class="status-card" id="status" aria-live="polite" hidden>
        <div class="status-row"><span class="status-dot"></span><strong class="status-today"></strong></div>
        <p class="status-sub"></p>
        <p class="status-next">{icon("calendar", 18)} <span></span></p>
      </div>'''

MARK_CIRCLE = '<svg class="mark-svg" viewBox="0 0 100 50" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M60 6 C 30 0 4 8 4 26 C 4 44 40 48 70 44 C 96 40 98 20 84 10 C 74 4 56 3 44 5"/></svg>'
MARK_UNDER = '<svg class="mark-svg" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M3 12 C 25 6 55 4 97 9 M12 17 C 40 13 70 13 90 15"/></svg>'

# =====================================================================
# STARTSEITE
# =====================================================================
STIMMEN_DATEN = read_csv("elternstimmen.csv") if os.path.exists(os.path.join(W, "daten/elternstimmen.csv")) else []
STIMMEN = "" if not STIMMEN_DATEN else ('<section class="section alt" id="stimmen"><div class="container"><div class="section-head center"><span class="kicker">Elternstimmen</span><h2>Das sagen Familien</h2></div>'
    '<div class="quotes reveal" tabindex="0" aria-roledescription="Karussell" aria-label="Elternstimmen">' + "".join(
    f'<figure class="quote{" on" if i == 0 else ""}"><blockquote><p>{e(r["Zitat"])}</p></blockquote><figcaption>{e(r["Von"])}</figcaption></figure>' for i, r in enumerate(STIMMEN_DATEN)) +
    '<div class="q-dots">' + "".join(f'<button type="button" aria-label="Stimme {i + 1}"{" class=\"on\"" if i == 0 else ""}><i></i></button>' for i in range(len(STIMMEN_DATEN))) + '</div></div></div></section>')

WORDS = [('spielen', 1.9, 50, 48), ('lachen', 1.4, 22, 24), ('forschen', 1.25, 79, 22), ('singen', 1.05, 14, 70), ('basteln', 1.3, 82, 72), ('Freunde', 1.6, 46, 82), ('toben', 1.0, 30, 50), ('lesen', 1.1, 70, 50), ('kochen', 0.95, 56, 16), ('Natur', 1.15, 8, 30), ('Hausaufgaben', 0.9, 88, 94), ('Feste', 1.05, 12, 94), ('Musik', 0.95, 93, 47), ('Englisch', 0.9, 36, 12), ('Ausflüge', 1.0, 64, 92), ('turnen', 0.95, 4, 52)]
WORDCLOUD = ('<div class="word-cloud reveal" role="img" aria-label="Was Kinder bei uns erleben: ' + ", ".join(w for w, *_ in WORDS) + '">' + "".join(
    f'<span style="left:{x}%;top:{y}%;font-size:{z}rem;--d:{i * -0.45:.2f}s">{w}</span>' for i, (w, z, x, y) in enumerate(WORDS)) + "</div>")

home = f'''
<section class="hero">
  <canvas class="season-fx" aria-hidden="true"></canvas>
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">{icon("pin", 16)} Lindleinstraße 20 · Würzburg-Grombühl</span>
      <h1>Kath. Kinder- und Jugendhort <span class="hl">Grombühl</span></h1>
      <p class="lead">Weil <span class="mark circle">Qualität{MARK_CIRCLE}</span> zählt! Eine vielfältige, große Kita für Kinder von 11 Monaten bis 16 Jahren – mit Herz, Zeit und viel Platz zum Entdecken.</p>
      <div class="hero-actions">
        <a class="btn btn-primary js-magnet" href="#bereiche">Unsere Bereiche {icon("arrow", 20)}</a>
        <a class="btn btn-ghost" href="kontakt.html">Kontakt aufnehmen</a>
      </div>
      {STATUS_CARD}
    </div>
    <div class="hero-collage">
      <figure class="c1">{img("img/p2170270.jpg", "Heller Gruppenraum im Kindergarten", lazy=False)}</figure>
      <figure class="c2">{img("img/img_4956.jpg", "Ein Kind entdeckt die Weltkarte im Kinderhort", lazy=False)}</figure>
      <figure class="c3">{img("img/p2160131.jpg", "Gruppenraum der Kinderkrippe", lazy=False)}</figure>
      <figure class="c4">{img("img/p2160031.jpg", "Der Weiße Raum mit Wassersäulen", lazy=False)}</figure>
      <div class="hero-badge"><span><b>3</b>Bereiche unter einem Dach</span></div>
    </div>
  </div>
</section>

<div class="announce" id="hinweis"></div>

<section class="section alt" id="bereiche">
  <div class="container">
    <div class="section-head center"><span class="kicker">Krippe · Kindergarten · Hort</span><h2>Ein Haus für jedes Alter</h2>
      <p>Mit Krippe, Kindergarten und Hort unter einem Dach können wir Kindern und Familien ein einheitliches Konzept und einen nahtlosen Wechsel gewährleisten.</p></div>
    <div class="areas">
      <a class="area-card theme-krippe reveal" href="kinderkrippe.html">
        <div class="thumb">{img("img/p2160110.jpg", "Gruppenraum der Kinderkrippe")}<span class="age">ab 11 Monaten</span></div>
        <div class="bar"></div>
        <div class="body"><h3>Kinderkrippe</h3><p>Sonnen- und Sternengruppe: liebevolle Betreuung für die Kleinsten – vom 11. Monat bis zum August des Jahres, in dem sie 3 Jahre alt werden.</p><span class="more">Mehr erfahren {icon("arrow", 18)}</span></div>
      </a>
      <a class="area-card theme-kiga reveal" href="kindergarten.html">
        <div class="thumb">{img("img/blick-vom-fenster-in-den-raum.jpg", "Gruppenraum im Kindergarten")}<span class="age">3 Jahre bis Einschulung</span></div>
        <div class="bar"></div>
        <div class="body"><h3>Kindergarten</h3><p>Bären-, Bienen- und Spatzengruppe: Projektarbeit, Englisch, Vorkurs Deutsch und viel Freispiel im großen Garten.</p><span class="more">Mehr erfahren {icon("arrow", 18)}</span></div>
      </a>
      <a class="area-card theme-hort reveal" href="kinderhort.html">
        <div class="thumb">{img("img/kreatviraum-5-1.jpg", "Kreativraum im Kinderhort")}<span class="age">ab der Einschulung</span></div>
        <div class="bar"></div>
        <div class="body"><h3>Kinderhort</h3><p>Für alle Schulformen – mit begleiteten, korrigierten Hausaufgaben, Freitagsausflügen und Ferienbetreuung bis 18:00 Uhr.</p><span class="more">Mehr erfahren {icon("arrow", 18)}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section green">
  <div class="container">
    <div class="section-head"><span class="kicker">Das zeichnet uns aus</span><h2>Mehr als Betreuung</h2>
      <p>Lange Öffnungszeiten, eine hauseigene Küche und viel Raum zum Spielen, Lernen und Entspannen – mitten in der Stadt.</p></div>
    <div class="stats">
      <div class="stat reveal"><b>6:45</b><span>Uhr öffnen wir – der Hort betreut bis 18:00 Uhr, auch in den Ferien</span></div>
      <div class="stat reveal"><b>max. 30</b><span>Schließtage im Jahr – gleich in allen Abteilungen</span></div>
      <div class="stat reveal"><b>2</b><span>Köchinnen kochen täglich frisch mit regionalen Zutaten</span></div>
      <div class="stat reveal"><b>11 M.–16 J.</b><span>breites Altersspektrum in einem Haus</span></div>
    </div>
    {WORDCLOUD}
    <div class="teasers">
      <a class="teaser reveal" href="#" data-full="img/p2160031.jpg" data-group="home" data-title="Weißer Raum" data-text="{e(WEISSER_RAUM)}">{img("img/p2160031.jpg", "Weißer Raum")}<div><h3>Weißer Raum</h3><p>Wasserbett, Lichtwasserfall und Wassersäulen – ein Ort für Ruhe und Traumreisen.</p></div></a>
      <a class="teaser reveal" href="#" data-full="img/p2160054.jpg" data-group="home" data-title="Hauseigene Küche" data-text="Hier wird täglich frisch gekocht.">{img("img/p2160054.jpg", "Hauseigene Küche")}<div><h3>Hauseigene Küche</h3><p>Hier wird täglich frisch und kindgerecht gekocht.</p></div></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container welcome">
    <div class="welcome-photo reveal">{img("img/petra-lachnit.png", "Petra Lachnit, Einrichtungsleitung")}</div>
    <div class="reveal">
      <span class="kicker">Herzlich Willkommen</span>
      <h2>Schön, dass Sie da sind!</h2>
      <blockquote>
        <p>Herzlich Willkommen auf den Seiten des Kath. Kinder- und Jugendhortes Grombühl. Ich freue mich sehr, dass Sie sich für unsere Kita interessieren. Wir wollen Ihnen mit unserer Homepage eine gute erste Orientierung geben und Ihnen weiterhelfen, wenn Sie nach einer passenden Kita suchen oder sich zunächst nur ein Bild von uns machen möchten.</p>
        <p>Sicher fällt Ihnen gleich auf, dass wir eine vielfältige und große Kita sind, mit einem breit gefächerten Altersspektrum, das sich an Kinder von 11 Monaten bis hin zu 16 Jahren richtet. Vielfalt und Individualität sind uns wichtig und das praktizieren wir hier täglich in unserer Pädagogik.</p>
        <details class="read-more"><summary><span>Den ganzen Gruß lesen</span></summary>
        <p>Wir achten auf die Stärken jedes Kindes und wollen allen Kindern – ob Krippen-, Kindergarten- oder Hortkindern – vielfältige Möglichkeiten bieten, diese Stärken in sich zu entdecken und immer weiter zu entwickeln. Dazu braucht es vielfältige Angebote, Projekte und ein ausgewogenes Maß an Begleitung und Freiheit. Daran arbeiten wir täglich!</p>
        <p>Gerne informieren wir Sie, wenn Sie mehr wissen möchten. Wir freuen uns auf Sie und Ihr Kind.</p>
        </details>
      </blockquote>
      <div class="signature">Herzliche Grüße, Ihre<strong>Petra Lachnit</strong><span>Einrichtungsleitung – Kath. Kinder- und Jugendhort Grombühl</span></div>
    </div>
  </div>
</section>

<section class="section alt" id="rundgang">
  <div class="container">
    <div class="section-head"><span class="kicker">Virtueller Rundgang</span><h2>Schauen Sie sich bei uns um</h2>
      <p>Fotos aus allen drei Bereichen zeigen Gruppenräume, Turnraum, Weißen Raum, Bistro und Küche – ganz ohne Termin.</p></div>
    <div class="teasers three">
      <a class="teaser reveal" href="kinderkrippe.html#rundgang">{img("img/puppenecke3.jpg", "Puppenecke der Kinderkrippe")}<div><h3>Kinderkrippe</h3><p>16 Bilder ansehen {icon("arrow", 18)}</p></div></a>
      <a class="teaser reveal" href="kindergarten.html#rundgang">{img("img/blick-vom-nebenraum-in-den-gruppenraum.jpg", "Gruppenraum im Kindergarten")}<div><h3>Kindergarten</h3><p>16 Bilder ansehen {icon("arrow", 18)}</p></div></a>
      <a class="teaser reveal" href="kinderhort.html#rundgang">{img("img/kreatviraum-4.jpg", "Kreativraum im Kinderhort")}<div><h3>Kinderhort</h3><p>24 Bilder ansehen {icon("arrow", 18)}</p></div></a>
    </div>
  </div>
</section>

<!--EINBLICKE-->

<section class="section" id="aktuell">
  <div class="container">
    <div class="section-head"><span class="kicker">Aktuelles</span><h2>Termine &amp; Unterlagen</h2>
      <p>Die nächsten Termine auf einen Blick. Vergangene Termine verschwinden automatisch.</p></div>
    <div class="notes-grid">
      <div>
        <ul class="event-list" data-max="3">
          {"".join(ev(r) for r in TERMINE)}
        </ul>
        <p class="events-empty muted" hidden>Aktuell stehen keine weiteren Termine an.</p>
        <div class="btn-row"><a class="btn btn-primary" href="aktuelles.html">Alle Termine {icon("arrow", 20)}</a>
          <a class="btn btn-ghost" href="downloads/termine.ics" download>{icon("calendar", 20)} Alle in den Kalender</a></div>
        <div class="saved-row" hidden><button class="btn btn-primary js-saved-ics" type="button">{icon("calendar", 20)} Gemerkte Termine in den Kalender (<span class="saved-n">0</span>)</button></div>
      </div>
      <div class="note-card reveal">
        <h3>Unterlagen zum Herunterladen</h3>
        <p>Hier finden Sie weitere Informationsblätter: Ferienplan, KinderhortABC und die Medikamentenvereinbarung.</p>
        <a class="btn btn-primary" href="downloads.html">{icon("file", 20)} Zu den Downloads</a>
      </div>
    </div>
  </div>
</section>

{ferienplan_section()}
{STIMMEN}
<section class="section tight">
  <div class="container">
    <div class="cta-band reveal">
      <div><h2>Lernen Sie uns <span class="mark under">kennen{MARK_UNDER}</span></h2><p>Sie haben Fragen zu Krippe, Kindergarten oder Hort? Rufen Sie uns an oder schreiben Sie uns eine E-Mail.</p></div>
      <div class="actions">
        <a class="btn btn-primary" href="tel:+4993127898920">{icon("phone", 20)} 0931&nbsp;2789892&nbsp;0</a>
        <a class="btn btn-ghost js-magnet" href="{PLATZ_MAIL}">{icon("mail", 20)} Platz anfragen</a>
      </div>
    </div>
  </div>
</section>
'''
JSONLD = {
    "@context": "https://schema.org", "@type": "ChildCare", "name": ORG, "url": SITE,
    "description": "Kinderkrippe, Kindergarten und Kinderhort unter einem Dach in Würzburg-Grombühl.",
    "image": SITE + "img/og-bild.jpg", "logo": SITE + "img/logo.png",
    "telephone": "+49 931 27898920", "email": MAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Lindleinstraße 20", "postalCode": "97080",
                "addressLocality": "Würzburg", "addressRegion": "Bayern", "addressCountry": "DE"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "06:45", "closes": "18:00"}],
}
page("index.html", "", "Kath. Kinder- und Jugendhort Grombühl e. V. in Würzburg: Kinderkrippe, Kindergarten und Kinderhort unter einem Dach. Weil Qualität zählt!", "index.html", home,
     head='\n<script type="application/ld+json">' + json.dumps(JSONLD, ensure_ascii=False) + '</script>')

# =====================================================================
# KINDERKRIPPE
# =====================================================================
krippe_tour = [
    ("img/p2160110.jpg", "Unser Gruppenraum", "unterteilt in verschiedene Bereiche"),
    ("img/bauecke2.jpg", "Unser Gruppenraum", "die Bauecke"),
    ("img/puppenecke.jpg", "Unser Gruppenraum", "die Puppenecke"),
    ("img/puppenecke2.jpg", "Unser Gruppenraum", "die Puppenecke"),
    ("img/puppenecke3.jpg", "Unser Gruppenraum", "die Puppenecke"),
    ("img/vorleseecke.jpg", "Unser Gruppenraum", "die Bücherecke"),
    ("img/esstisch.jpg", "Unser Gruppenraum", "für die gemeinsamen Mahlzeiten"),
    ("img/p2160131.jpg", "Unser Gruppenraum", "die Entspannungsecke"),
    ("img/nebenraum2.jpg", "Unser Nebenraum", "Der Nebenraum ist dem Gruppenraum direkt angegliedert"),
    ("img/nebenraum.jpg", "Unser Nebenraum", "Er wird täglich zum Freispiel genutzt mit wechselndem Spielmaterial (Polsterbausteine, Parkhaus, kl. Bällebad, …) oder auch zur angeleiteten Kleingruppenarbeit."),
    ("img/schlafen.jpg", "Unser Schlafraum", "Ausgestattet mit einem Bett für jedes Kind zum täglichen Mittagsschlaf. Das Zimmer kann durch Rollo, bzw. mit Vorhang angenehm abgedunkelt werden um eine gemütliche Schlafatmosphäre zu ermöglichen."),
    ("img/img_6791.jpg", "Unser Wickelraum", "In geschützter Atmosphäre bietet der Wickeltisch, eine auf Kleinkindgröße ausgerichtete sehr niedrige Kindertoilette, sowie Töpfchen und ein Waschbecken angemessene Möglichkeit zur Körperhygiene und -pflege."),
    ("img/p2160031.jpg", "Unser weißer Raum", WEISSER_RAUM),
    ("img/turnraum.jpg", "Unser Turnraum", "Die wöchentliche Bewegungseinheit findet im gut ausgestatteten Turnraum statt. In Kleingruppen werden spielerisch Balance, Reaktion und Kraft gefördert."),
    ("img/img_6768.jpg", "Unser Flur", "Der Flurbereich mit den Kindergarderoben wird ebenfalls als Spielbereich angeboten. Hier lädt das Fahren mit BobbyCar, kl. Rädchen usw. ein. Der täglich ausgelegte Teppich ist der Platz von Morgen- und Mittagskreis, zum Singen und Musizieren."),
    ("img/p2160054.jpg", "Unsere hauseigene Küche", "Hier wird täglich frisch gekocht"),
]
krippe = page_hero("Kinderkrippe", "Herzlich Willkommen beim Kath. Kinder- und Jugendhort Grombühl – geborgen ankommen, spielen, entdecken.",
                   "img/p2160110.jpg", "Sonnen- &amp; Sternengruppe",
                   [("ueberblick", "Überblick"), ("raeume", "Räumlichkeiten"), ("rundgang", "Virtueller Rundgang"), ("tagesablauf", "Tagesablauf"), ("auszeichnung", "Das zeichnet uns aus"), ("fragen", "Fragen"), ("ferienplan", "Ferienplan")],
                   alt="Gruppenraum der Kinderkrippe")
krippe += section("ueberblick", "Auf einen Blick", "Die Kinderkrippe", "", info_cards([
    ("users", "Zielgruppe", "ab 11 Monaten", "<p>Die Kinderkrippe besuchen Kinder ab dem Alter von 11 Monaten bis zum August des Jahres, in dem sie 3 Jahre alt werden.</p>"),
    ("clock", "Öffnungszeiten", "6:45 – 16:30 Uhr", "<p>Bringzeit von 6:45 bis 9:00 Uhr, Abholen ab 14:00 Uhr entsprechend der gebuchten Stunden. Um 16:30 Uhr schließt die Kinderkrippe.</p>"),
    ("pot", "Küche", "frisch &amp; regional", f"<p>{KUECHE}</p>"),
]))
krippe += section("raeume", "Räumlichkeiten", "Viel Platz für die Kleinsten", "", '''<div class="groups"><span class="muted">Die Kinderkrippe umfasst zwei Gruppen:</span>
<span class="group-chip"><span class="emoji" aria-hidden="true">☀️</span>Sonnengruppe</span>
<span class="group-chip"><span class="emoji" aria-hidden="true">⭐</span>Sternengruppe</span></div>''' + rooms([
    ("Gruppenraum", "Unterteilt in verschiedene Bereiche: wie z. B. Bauecke, Puppenwohnung, Bücherecke und mit dem großen Tisch für die gemeinsamen Mahlzeiten. Die bodentiefen Fenster fluten die Räume mit viel Licht und bieten eine schöne Aussicht in den Garten. Das Spielen auf dem Boden ist durch die Fußbodenheizung besonders einladend.", "img/p2160110.jpg"),
    ("Nebenraum", "Der Nebenraum ist dem Gruppenraum direkt angegliedert. Er wird täglich zum Freispiel genutzt mit wechselndem Spielmaterial (Polsterbausteine, Parkhaus, kl. Bällebad, …) oder auch zur angeleiteten Kleingruppenarbeit.", "img/nebenraum.jpg"),
    ("Schlafraum", "Ausgestattet mit einem Bett für jedes Kind zum täglichen Mittagsschlaf. Das Zimmer kann durch Rollo, bzw. mit Vorhang angenehm abgedunkelt werden um eine gemütliche Schlafatmosphäre zu ermöglichen.", "img/schlafen.jpg"),
    ("Flur", "Der Flurbereich mit den Kindergarderoben wird ebenfalls als Spielbereich angeboten. Hier lädt das Fahren mit BobbyCar, kl. Rädchen usw. ein. Der täglich ausgelegte Teppich ist der Platz von Morgen- und Mittagskreis, zum Singen und Musizieren.", "img/img_6768.jpg"),
    ("Wickelraum", "In geschützter Atmosphäre bietet der Wickeltisch, eine auf Kleinkindgröße ausgerichtete sehr niedrige Kindertoilette, sowie Töpfchen und ein Waschbecken angemessene Möglichkeit zur Körperhygiene und -pflege.", "img/img_6791.jpg"),
    ("Turnraum", "Die wöchentliche Bewegungseinheit findet im gut ausgestatteten Turnraum statt. In Kleingruppen werden spielerisch Balance, Reaktion und Kraft gefördert.", "img/turnraum.jpg"),
    ("Weißer Raum", WEISSER_RAUM, "img/p2160031.jpg"),
    ("Eingangsbereich", "Der Eingangsbereich bietet tagsüber Möglichkeit zum Abstellen des Kinderwagens.", None),
    ("Außenbereich", "Die Kinderkrippe hat direkt vor dem Eingang einen eigenen Außenspielbereich mit Sandkasten, Nestschaukel, Tipi, Terrasse und Rasenfläche. Am Vormittag nutzt die Kinderkrippe gerne auch die restliche, sehr weitläufige Spielfläche mit dem großen, teils überdachten Sandkasten, die Ruheinsel und den Fußballhof.", None),
]), cls="alt")
krippe += section("rundgang", "Virtueller Rundgang", "Möchten Sie mehr von der Kinderkrippe sehen?",
                  "Herzlich Willkommen bei unserem virtuellen Rundgang! Klicken Sie auf ein Bild, um es groß anzusehen.", tour("krippe", krippe_tour))
krippe += section("tagesablauf", "Tagesablauf", "Der Tagesablauf der Kinderkrippe", "", timeline([
    ("6:45 – 9:00 Uhr", "Bringzeit, die Kinder kommen in der Kita an."),
    ("9:30 Uhr", "Freispiel"),
    ("9:30 – 10:00 Uhr", "Gemeinsames Frühstück – zubereitet durch die hauseigene Küche"),
    ("10:00 – 11:15 Uhr", "Morgenkreis, Singen, Fingerspiele, Geburtstagsfeiern, Zeit für gezielte Angebote, z. B. Turnen, kreative Angebote, musikalische Erziehung …"),
    ("10:45 Uhr", "Feste, routinemäßige Wickelzeit – selbstverständlich zu jeder Zeit bei Bedarf"),
    ("11:15 Uhr", "Gemeinsames Mittagessen – zubereitet durch die hauseigene Küche"),
    ("11:50 Uhr", "Körperpflege nach dem Essen; Hände und Mund abwaschen"),
    ("12:00 Uhr", "Mittagsschlaf, die Kinder dürfen schlafen, so lange sie möchten, anschließend routinemäßige Wickelzeit"),
    ("ab 14:00 Uhr", "Abholen möglich, entsprechend der gebuchten Stunden"),
    ("14:30 Uhr", "Gemeinsamer Nachmittagssnack, i. d. R. Obst"),
    ("ab 15:00 Uhr", "Freispiel am Nachmittag mit gruppenübergreifendem Spielen – meist im Freien"),
    ("16:30 Uhr", "Die Kinderkrippe schließt"),
]), cls="alt")
krippe += section("auszeichnung", "Das zeichnet uns aus", "Was unsere Krippe besonders macht", "", features([
    "Einfühlsame, mit den Eltern gemeinsam geplante Eingewöhnungszeit des Kindes. Dauer der vollständigen Eingewöhnung ca. 4 Wochen",
    "Behutsame Begleitung der Kinder in Pflegesituationen, bei Mahlzeiten, Ruhen und Schlafen",
    "Portfolio als Instrument der Dokumentation über den Entwicklungsverlauf des Kindes",
    "Hohe Fachkraftquote",
    "Mit Krippe, Kindergarten und Hort unter einem Dach können wir Kindern und ihren Familien ein einheitliches Konzept und einen nahtlosen Übergang gewährleisten",
    "Sehr großes Außengelände mit altem Baumbestand, trotz Stadtlage",
    "30 Schließtage im Jahr",
    "Hauseigene Küche mit zwei Köchinnen, die täglich abwechslungsreiches und saisonales Essen frisch zubereiten",
    "Das Waschen von Bettwäsche wird von der Kita übernommen",
], [("Begleitung &amp; Team", [0, 1, 2, 3]), ("Haus &amp; Garten", [4, 5, 7]), ("Alltag", [6, 8])]))
krippe += section("fragen", "Meist gestellte Fragen", "Häufige Fragen zur Kinderkrippe", "", faq([
    ("Müssen wir Windeln usw. für unser Kind mitbringen?", "Ja, jede Familie bringt fürs eigene Kind Windeln, Feuchttücher und ggf. Wundschutzcreme etc. mit, damit jedes Kind mit seinen eigenen Produkten gewickelt werden kann. Bei Bedarf bekommen Sie beim Abholen einen Notizzettel mit der Bitte, neue Produkte mitzubringen, mit nach Hause."),
    ("Gibt es die Möglichkeit für mein Kind zum Schlafen?", "Der Tagesablauf ist speziell auf die Bedürfnisse von Kleinstkindern abgestimmt und sieht somit täglich eine Ruhezeit nach dem Mittagessen vor. In heimeliger Atmosphäre werden die Kinder in ihr Bett gelegt und zum Einschlafen begleitet."),
    ("Ist die Zugehörigkeit zur katholischen Kirche notwendig?", "Wir sind eine katholische Einrichtung, feiern die Feste des christlichen Kirchenjahres, sind aber weltoffen für alle Religionen und Kulturen."),
    ("Gibt es eine Eingewöhnungszeit?", "Einfühlsame, mit den Eltern gemeinsam geplante Eingewöhnungszeit des Kindes. Dauer der vollständigen Eingewöhnung ca. vier Wochen."),
]), cls="alt")
krippe += abc_section("KrippenABC", "Zum Downloadbereich")
krippe += ferienplan_section()
page("kinderkrippe.html", "Kinderkrippe", "Kinderkrippe im Kath. Kinder- und Jugendhort Grombühl, Würzburg: Sonnen- und Sternengruppe für Kinder ab 11 Monaten – mit virtuellem Rundgang, Tagesablauf und FAQ.", "kinderkrippe.html", krippe, "theme-krippe")

# =====================================================================
# KINDERGARTEN
# =====================================================================
kiga_tour = [
    ("img/blick-vom-nebenraum-in-den-gruppenraum.jpg", "Unser Gruppenraum", "unterteilt in verschiedene Bereiche"),
    ("img/blick-vom-fenster-in-den-raum.jpg", "Unser Gruppenraum", "Frühstücks- und Esstische"),
    ("img/p2170270.jpg", "Unser Gruppenraum", "die Bauecke"),
    ("img/p2170268.jpg", "Unser Gruppenraum", "die Bauecke"),
    ("img/p2160168.jpg", "Unser Gruppenraum", "die Puppenecke"),
    ("img/p2160167.jpg", "Unser Gruppenraum", "die Puppenecke"),
    ("img/blick-aus-der-puppenecke.jpg", "Unser Gruppenraum", "Blick aus der Puppenecke"),
    ("img/lesecke.jpg", "Unser Gruppenraum", "die Leseecke"),
    ("img/maltisch.jpg", "Unser Gruppenraum", "der Kreativtisch"),
    ("img/p2160149.jpg", "Unser Zimmer Kunterbunt", "Im Zimmer Kunterbunt findet für alle Mittelkinder (4- bis 5-Jährige) einmal wöchentlich am Vormittag eine Kleingruppenarbeit statt. Die Kinder starten mit dem Morgenkreis und einem gemeinsamen Frühstück."),
    ("img/p2160152.jpg", "Unser Zimmer Kunterbunt", "Hier werden verschiedene Beschäftigungen passend zur Jahreszeit oder zum Projektthema angeboten. Dies sind beispielsweise kreative Angebote, Bilderbuchbetrachtungen, Fingerspiele oder das Singen von Liedern."),
    ("img/p2160031.jpg", "Unser weißer Raum", WEISSER_RAUM),
    ("img/turnraum.jpg", "Unser Turnraum", "Der große, hohe Raum bietet den Kindern die Möglichkeit zum Toben und Rennen. Hier finden Bewegungsangebote und -spiele zu speziellen Wünschen und Themen der Kinder statt."),
    ("img/p2170222.jpg", "Unser Flur", "Unser großer Außenspielbereich im Flur"),
    ("img/p2170225.jpg", "Unser Flur", "mit wechselnden Spielmaterialien"),
    ("img/p2160054.jpg", "Unsere hauseigene Küche", "Hier wird täglich frisch gekocht."),
]
kiga = page_hero("Kindergarten", "Spielen, forschen, Freunde finden – in großen, hellen Räumen und einem riesigen Garten mitten in der Stadt.",
                 "img/blick-vom-fenster-in-den-raum.jpg", "Bären-, Bienen- &amp; Spatzengruppe",
                 [("ueberblick", "Überblick"), ("raeume", "Räumlichkeiten"), ("rundgang", "Virtueller Rundgang"), ("tagesablauf", "Tagesablauf"), ("auszeichnung", "Das zeichnet uns aus"), ("fragen", "Fragen"), ("ferienplan", "Ferienplan")],
                 alt="Gruppenraum im Kindergarten")
kiga += section("ueberblick", "Auf einen Blick", "Der Kindergarten", "", info_cards([
    ("users", "Zielgruppe", "3 Jahre bis Einschulung", "<p>Den Kindergarten besuchen Kinder im Alter von 3 Jahren bis zur Einschulung.</p>"),
    ("clock", "Öffnungszeiten", "6:45 – 16:30 Uhr", "<p>Der Kindergarten öffnet um 6:45 Uhr. Bis 8:00 Uhr wird die gruppenübergreifende Frühbetreuung angeboten. Um 16:30 Uhr schließt der Kindergarten. Es kann nach Bedarf der Spätdienst im Hort bis 17:30 Uhr dazugebucht werden.</p>"),
    ("pot", "Küche", "frisch &amp; regional", f"<p>{KUECHE}</p>"),
]))
kiga += section("raeume", "Räumlichkeiten", "Große, helle Räume zum Spielen und Lernen", "", '''<div class="groups"><span class="muted">Es gibt drei Kindergartengruppen:</span>
<span class="group-chip"><span class="emoji" aria-hidden="true">🐻</span>Bärengruppe</span>
<span class="group-chip"><span class="emoji" aria-hidden="true">🐝</span>Bienengruppe</span>
<span class="group-chip"><span class="emoji" aria-hidden="true">🐦</span>Spatzengruppe</span></div>''' + rooms([
    ("Gruppenraum", "In unseren großen, hellen Gruppenräumen befinden sich jeweils eine Leseecke, eine Bauecke, eine Puppen-, Rollenspielecke, ein Kreativtisch, ein Frühstücks- und Esstisch für das warme frisch zubereitete Mittagessen sowie Spieltische für Brettspiele und Puzzle. Zu jeder Gruppe gehört ein Nebenraum, dort finden altersspezifische Angebote in Kleingruppen statt. Außerdem hat jede Gruppe einen großen Außenspielbereich im Flur mit wechselnden Spielmaterialien.", "img/blick-vom-fenster-in-den-raum.jpg"),
    ("Turnraum", "Der große, hohe Raum bietet den Kindern die Möglichkeit zum Toben und Rennen. Hier finden Bewegungsangebote und -spiele zu speziellen Wünschen und Themen der Kinder statt.", "img/turnraum.jpg"),
    ("Weißer Raum", WEISSER_RAUM, "img/p2160031.jpg"),
    ("Zimmer Kunterbunt", "Im Zimmer Kunterbunt findet für alle Mittelkinder (4- bis 5-Jährige) einmal wöchentlich am Vormittag eine Kleingruppenarbeit statt. Die Kinder starten mit dem Morgenkreis und einem gemeinsamen Frühstück. Hier werden verschiedene Beschäftigungen passend zur Jahreszeit oder zum Projektthema angeboten. Dies sind beispielsweise kreative Angebote, Bilderbuchbetrachtungen, Fingerspiele oder das Singen von Liedern.", "img/p2160149.jpg"),
    ("Garten", "Am Schiff, im Tipi, im Sandkasten und auf dem Fußballhof kann sich das Kind täglich an der frischen Luft bewegen. Für den Sandkasten gibt es Spielsachen, die dem Kind täglich zur Verfügung gestellt werden, und es hat die Möglichkeit, mit dem Laufrad, Fahrrad oder anderen Fahrzeugen zu fahren.", None),
]), cls="alt")
kiga += section("rundgang", "Virtueller Rundgang", "Möchten Sie mehr von unserem Kindergarten sehen?",
                "Herzlich Willkommen bei unserem virtuellen Rundgang! Klicken Sie auf ein Bild, um es groß anzusehen.", tour("kiga", kiga_tour))
kiga += section("tagesablauf", "Tagesablauf", "Der Tagesablauf des Kindergartens", "", timeline([
    ("6:45 – 8:00 Uhr", "Gruppenübergreifende Frühbetreuung in wechselnden Gruppen"),
    ("8:00 – 9:00 Uhr", "Bringzeit, Ankommen in der eigenen Gruppe, Freispiel, begleitendes Frühstück; jedes Kind darf entscheiden, wann es in dieser Zeit frühstücken möchte"),
    ("9:00 Uhr", "Bringzeit Ende"),
    ("10:00 – 11:00 Uhr", "Gezielte Angebote, je nach Wochentag: Gruppenzusammensetzung in altersspezifischen Kleingruppen, Turnen, Spaziergang, Englisch, Geburtstagsfeiern, Feste feiern"),
    ("11:00 – 11:30 Uhr", "Morgenkreis, themenbezogener Kreis"),
    ("11:30 Uhr", "Freispielzeit im Garten"),
    ("12:00 Uhr", "Erste Abholzeit möglich, je nach gebuchten Stunden"),
    ("12:30 Uhr", "Warmes Mittagessen von unserer hauseigenen Küche"),
    ("13:00 – 13:30 Uhr", "Entspannung, Kreisspiele, Geschichten vorlesen"),
    ("13:30 – 15:30 Uhr", "Freispielzeit im Garten oder im Gruppenraum"),
    ("15:30 Uhr", "Brotzeit"),
    ("16:00 – 16:30 Uhr", "Freispiel, Abholzeit"),
    ("16:30 – 17:30 Uhr", "Spätdienst – gruppenübergreifende Betreuung von Hort und Kindergarten"),
]), cls="alt")
kiga += section("auszeichnung", "Das zeichnet uns aus", "Was unseren Kindergarten besonders macht", "", features([
    "Mit langen Öffnungszeiten entlasten wir vor allem berufstätige Eltern, auch in den Ferien",
    "Nur max. 30 Schließtage im Jahr",
    "Hohe Fachkraftquote",
    "Mit Krippe, Kindergarten und Hort unter einem Dach können wir Kindern und Familien ein einheitliches Konzept und einen nahtlosen Wechsel gewährleisten",
    "Enge Zusammenarbeit mit der Grundschule, um den Kindern den Übergang in die Schule so angenehm wie möglich zu gestalten",
    "Hauseigene Küche, in der täglich von zwei Köchinnen mit regionalen Zutaten frisch gekocht wird",
    "Weißer Raum zum Entspannen",
    "Sehr großes Außengelände mit verschiedenen Spielmöglichkeiten, trotz Stadtlage",
    "Großzügige Räume zum Spielen und Lernen",
    "Kurze Wege in die Natur für Spaziergänge und Spielplatzbesuche",
    "Büchereibesuche, Exkursionen (Feuerwehrbesuch, Bäckereibesuch), Jahresausflug",
    "Übernachtung im Kindergarten für die Kinder, die in die Schule kommen",
    "Ab dem Vorschulalter arbeiten wir mit dem Würzburger Trainingsprogramm „Hören, Lauschen, Lernen“",
], [("Betreuung &amp; Team", [0, 1, 2, 3, 4]), ("Haus &amp; Küche", [5, 6, 7, 8]), ("Erleben &amp; Lernen", [9, 10, 11, 12])]) + '''<h3 class="sub-head">Besondere Vorzüge unserer Einrichtung</h3>
<div class="pill-list">
  <div class="reveal"><h3>Projektarbeit</h3><p>Wir arbeiten im Kindergarten projektbezogen. Das Thema orientiert sich an den Interessen der Kinder, es wird von ihnen ausgewählt und abgestimmt. Die Projektarbeit bietet eine kindgerechte Form des Lernens: Die Kinder können eigene Ideen einbringen und gestalten den Lernprozess mit.</p></div>
  <div class="reveal"><h3>Englisch</h3><p>Hier lernen die Kinder spielerisch die Farben, die Körperteile des Menschen, verschiedene Tiere und singen englische Lieder. Ziel ist es, den Kindern eine Grundlage und einen vertrauten Umgang mit der englischen Sprache zu vermitteln.</p></div>
  <div class="reveal"><h3>Vorkurs Deutsch</h3><p>Der Vorkurs Deutsch ist für Vorschulkinder, die im sprachlichen Bereich eine zusätzliche schulvorbereitende Förderung benötigen. Die Förderung bezieht sich auf die Grammatik, das Sprachverständnis und die Erweiterung des Wortschatzes.</p></div>
</div>''')
kiga += section("fragen", "Meist gestellte Fragen", "Häufige Fragen zum Kindergarten", "", faq([
    ("Arbeitet der Kindergarten nach dem offenen Konzept?", "Wir haben feste Gruppen mit festen Bezugspersonen. Bei verschiedenen Aktionen und Aktivitäten arbeiten wir gruppenübergreifend."),
    ("Muss mein Kind für den Kindergarten sauber sein?", "Falls Ihr Kind noch eine Windel benötigt, unterstützen wir es auf dem Weg zum Sauberwerden."),
    ("Wie verläuft die Eingewöhnung im Kindergarten?", "Die Eingewöhnungsphase verläuft für jedes Kind unterschiedlich. Das pädagogische Personal geht auf jedes Kind bedürfnisorientiert ein, um diese Phase in Absprache mit den Eltern bestmöglich zu gestalten. Bitte nehmen Sie sich am Anfang Zeit, Ihr Kind gemeinsam mit dem Fachpersonal in den Kindergartenalltag einzugewöhnen."),
    ("Inwieweit muss ich für die Verpflegung meines Kindes sorgen?", "Das warme Mittagessen wird von unserer hauseigenen Küche zubereitet. Für das Frühstück und den Nachmittagssnack, je nach Buchungszeit, richten Sie für Ihr Kind eine Brotzeit und eine Trinkflasche mit Wasser im Mehrwegbehälter."),
    ("Ist die Zugehörigkeit zur katholischen Kirche notwendig?", "Nein. Wir sind eine katholische Einrichtung, feiern die Feste des christlichen Kirchenjahres, beten vor dem Mittagessen, sind aber weltoffen für alle Religionen und Kulturen."),
    ("Sind die Schließtage in allen Abteilungen des Kinder- und Jugendhorts Grombühl gleich?", "Ja, wir haben in allen Abteilungen des Hauses an maximal 30 gleichen Tagen geschlossen."),
]), cls="alt")
kiga += abc_section("KindergartenABC", "Zum Downloadbereich")
kiga += ferienplan_section()
page("kindergarten.html", "Kindergarten", "Kindergarten im Kath. Kinder- und Jugendhort Grombühl, Würzburg: Bären-, Bienen- und Spatzengruppe für Kinder von 3 Jahren bis zur Einschulung.", "kindergarten.html", kiga, "theme-kiga")

# =====================================================================
# KINDERHORT
# =====================================================================
hort_tour = [
    ("img/kreatviraum-5-1.jpg", "Unser Kreativraum", "Freizeitbereich der Hortkinder"),
    ("img/kreatviraum-4.jpg", "Unser Kreativraum", "Freizeitbereich der Hortkinder"),
    ("img/img_4956.jpg", "Unser Kreativraum", "Freizeitbereich der Hortkinder"),
    ("img/krativraum-2-1.jpg", "Unser Kreativraum", "Freizeitbereich der Hortkinder"),
    ("img/bauecke-2.jpg", "Unser Kreativraum", "die Bauecke"),
    ("img/baueckenstadion.jpg", "Unser Kreativraum", "ein Bauwerk unserer Kinder"),
    ("img/img_1378.jpg", "Unser Kreativraum", "ein Werk unserer Kinder"),
    ("img/baellebad.jpg", "Unser Kreativraum", "das Bällebad"),
    ("img/img_1222.jpg", "Unsere Hausaufgabenräume", "Nach Alter und Klassenstufen getrennt fertigt jedes Kind hier eigenständig seine Hausaufgaben an"),
    ("img/img_1225.jpg", "Unsere Hausaufgabenräume", "Jedes Kind erhält die Hilfe und Unterstützung, die es für seine Aufgaben benötigt"),
    ("img/p2160027.jpg", "Unsere Hausaufgabenräume", "Hier werden die Hausaufgaben jedes Kindes von den Erziehern korrigiert und auf Vollständigkeit überprüft"),
    ("img/hausaufgaben1.jpg", "Unsere Hausaufgabenräume", "Hier werden die Hausaufgaben jedes Kindes von den Erziehern korrigiert und auf Vollständigkeit überprüft"),
    ("img/chilloutarea.jpg", "Unsere Chillout-Ecke", "Bereich der ganz Großen: Kinder ab der 6. Klasse haben hier einen eigenen gemütlichen Bereich zum Chillen."),
    ("img/turnraum.jpg", "Unser Turnraum", "Hier spielen, turnen und toben die Kinder. Sie können diesen Raum bei gezielten Angeboten und in ihrer Freizeit nutzen."),
    ("img/p2160031.jpg", "Unser weißer Raum", WEISSER_RAUM),
    ("img/img_1288.jpg", "Unser Spielflur", "Hier hat jedes Kind seinen eigenen Spind für Büchertasche und persönliches Eigentum."),
    ("img/p2160035.jpg", "Unser Spielflur", "Im Spielflur gibt es eine Bibliothek mit Büchern für jedes Lesealter"),
    ("img/p2160042.jpg", "Unser Spielflur", "der Tischkicker"),
    ("img/img_1251.jpg", "Unser Bistro", "Im Bistro nehmen die Kinder täglich nach der Schule in entspannter Atmosphäre gemeinsam mit ihren Freunden ein leckeres frisch gekochtes Mittagessen ein"),
    ("img/p2160052.jpg", "Unser Bistro", "Das Mittagessen wird in unserer hauseigenen Küche frisch zubereitet"),
    ("img/werkraum.jpg", "Unser Werkraum", "Hier können die Kinder erste handwerkliche Erfahrungen sammeln"),
    ("img/p2160054.jpg", "Unsere hauseigene Küche", "Hier wird täglich frisch gekocht"),
    ("img/img_2423.jpg", "Unser Kreativraum", "Ein Werk unserer Kinder"),
    ("img/img_8912.jpg", "Ein Kunstwerk unserer Kinder", "Gestaltet im Kinderhort"),
]
hort = page_hero("Kinderhort", "Nach der Schule ankommen, Hausaufgaben mit Unterstützung erledigen und Freizeit selbst gestalten – von 6:45 bis 18:00 Uhr.",
                 "img/kreatviraum-5-1.jpg", "Für alle Schulformen",
                 [("ueberblick", "Überblick"), ("raeume", "Räumlichkeiten"), ("rundgang", "Virtueller Rundgang"), ("tagesablauf", "Tagesablauf"), ("auszeichnung", "Das zeichnet uns aus"), ("schulen", "Zusammenarbeit mit Schulen"), ("fragen", "Fragen"), ("ferienplan", "Ferienplan")],
                 alt="Kreativraum im Kinderhort")
hort += section("ueberblick", "Auf einen Blick", "Der Kinderhort", "", info_cards([
    ("users", "Zielgruppe", "ab der Einschulung", "<p>Den Kinderhort besuchen Kinder ab der Einschulung. Gerne begleiten wir die Kinder über die Grundschulzeit hinaus. Wir sind offen für alle Schulformen, wie z. B. Mittelschulen, Realschulen, Gymnasien sowie auch Förderschulen. Jedes Kind darf den Kinderhort so lange besuchen, wie es möchte und es seiner Entwicklung angemessen ist.</p>"),
    ("clock", "Öffnungszeiten", "6:45 – 18:00 Uhr", "<p>Während der Schulzeit von 6:45 bis 8:00 Uhr und vom jeweiligen Unterrichtsende bis 18:00 Uhr. Während der Schulferien, in denen der Hort geöffnet ist, können die Kinder ganztags durchgängig von 6:45 bis 18:00 Uhr betreut werden. Eltern buchen die Zeiten, die sie für die Betreuung ihres Kindes benötigen.</p>"),
    ("pot", "Küche", "frisch &amp; regional", f"<p>{KUECHE}</p>"),
]))
hort += section("raeume", "Räumlichkeiten", "Räume für Hausaufgaben, Kreativität und Erholung", "", rooms([
    ("Kreativraum", "Freizeitbereich der Hortkinder, in dem eine Puppenecke, eine Bauecke, ein Piratenausguck, mehrere Spielteppiche, ein Billardtisch und ein Kreativbereich mit unterschiedlichsten Materialien zur Verfügung stehen.", "img/kreatviraum-4.jpg"),
    ("Hausaufgabenräume", "Nach Alter und Klassenstufen getrennt fertigt jedes Kind hier eigenständig seine Hausaufgaben an. Jedes Kind erhält die Hilfe und Unterstützung, die es für seine Aufgaben benötigt. Hier werden die Hausaufgaben jedes Kindes von den Erziehern korrigiert und auf Vollständigkeit überprüft.", "img/img_1222.jpg"),
    ("Spielflur", "Hier hat jedes Kind seinen eigenen Spind für Büchertasche und persönliches Eigentum. Im Spielflur gibt es eine Bibliothek mit Büchern für jedes Lesealter, eine gemütliche Lesetreppe, einen Spielbereich mit Spieltischen und einen Tischkicker.", "img/p2160035.jpg"),
    ("Bistro", "Im Bistro nehmen die Kinder täglich nach der Schule in entspannter Atmosphäre gemeinsam mit ihren Freunden ein leckeres frisch gekochtes Mittagessen ein, das in unserer hauseigenen Küche zubereitet wurde.", "img/img_1251.jpg"),
    ("Turnraum", "Hier spielen, turnen und toben die Kinder. Sie können diesen Raum bei gezielten Angeboten und in ihrer Freizeit nutzen.", "img/turnraum.jpg"),
    ("Weißer Raum", WEISSER_RAUM, "img/p2160031.jpg"),
    ("Werkraum", "Handwerkliche und gestalterische Aktionen finden regelmäßig im Werkraum statt.", "img/werkraum.jpg"),
    ("Bereich der ganz Großen", "Kinder ab der 6. Klasse haben hier einen eigenen gemütlichen Bereich zum Chillen.", "img/chilloutarea.jpg"),
]), cls="alt")
hort += section("rundgang", "Virtueller Rundgang", "Möchten Sie mehr vom Kinderhort sehen?",
                "Herzlich Willkommen bei unserem virtuellen Rundgang! Klicken Sie auf ein Bild, um es groß anzusehen.", tour("hort", hort_tour))
hort += section("tagesablauf", "Tagesablauf", "Der Tagesablauf des Kinderhorts", "", timeline([
    ("6:45 – 8:00 Uhr", "In der Frühbetreuung können die Kinder vor der Schule schon spielen oder sich noch ein wenig ausruhen. Gemeinsam gehen die Schulkinder dann zu Unterrichtsbeginn in die Schule."),
    ("11:15 Uhr", "Jetzt haben die ersten Kinder bereits Schulschluss und im Hort die Möglichkeit, draußen zu spielen, das Gespräch zum Erzieher zu suchen oder sich nach dem anstrengenden Schultag erst einmal auszuruhen und zu entspannen."),
    ("12:00 – 13:45 Uhr", "Gleitendes Mittagessen in gemütlicher Runde. Gleichzeitig stehen den Kindern in dieser Zeit alle Bereiche des Hortes zum Spielen zur Verfügung."),
    "Montag bis Donnerstag",
    ("13:45 – 14:00 Uhr", "Für jede Hausaufgabengruppe findet in dieser Zeit ein Spiel- und Gesprächskreis statt. Jedes Kind darf in diesem Kreis auch seinen eigenen Geburtstag feiern."),
    ("14:00 – 15:30 Uhr", "In dieser Zeit erledigt jedes Kind seine Hausaufgaben in seiner Hausaufgabengruppe. Ab 15:00 Uhr dürfen die Kinder, die bereits fertig sind, schon zum Spielen gehen."),
    ("15:00 – 16:00 Uhr", "Freizeit für alle Hortkinder. Die Kinder können sich entscheiden, wo und mit wem sie spielen. Ab 15:30 Uhr findet ein angekündigtes Angebot statt, an dem sich die Kinder freiwillig beteiligen können."),
    "Freitags",
    ("14:00 Uhr", "In der wöchentlichen Kinderkonferenz besprechen die Kinder wichtige Informationen und aktuelle Themen, wie z. B. Freitagsausflüge. Ferienpläne werden von den Kindern abgestimmt."),
    ("14:30 – 16:30 Uhr", "Immer freitags findet ein Ausflug im Stadtgebiet von Würzburg statt. Die Teilnahme am Ausflug ist für die Kinder freiwillig. Freitags findet keine Hausaufgabenbetreuung im Hort statt."),
    "Täglich",
    ("16:30 – 18:00 Uhr", "Je nach gebuchter Zeit können die Kinder bis 18:00 Uhr im Hort bleiben."),
]), cls="alt")
hort += section("auszeichnung", "Das zeichnet uns aus", "Der Kath. Kinder- und Jugendhort Grombühl bietet mehr als Betreuung …", "", f'''
<div class="split split-top">
  <div class="reveal"><p>Wir betrachten jedes Kind stärkenorientiert. Wir fördern die Selbstständigkeit der Schulkinder durch unser gruppenübergreifendes Konzept, das den Kindern die Möglichkeit gibt, selbst zu bestimmen, wo und mit wem sie spielen oder wie sie ihre Freizeit gestalten. Altersübergreifende Kontakte zu Jüngeren und Älteren stärken die Kinder in Verantwortungsübernahme, Rücksicht und Eigenverantwortlichkeit. Zahlreiche Partizipationsmöglichkeiten zeigen den Kindern, wie sie Einfluss auf ihren Alltag im Kinderhort nehmen und diesen selbst mitbestimmen können, z. B. in Kinderkonferenzen, Kinderbefragungen und Gruppengesprächen mit den Erziehern.</p></div>
  <div class="reveal"><p>Unsere Fachkraftquote beträgt <strong>100 Prozent</strong>, das heißt, dass die Hortkinder ausschließlich von ausgebildeten, staatlich anerkannten Erziehern betreut werden. Wir sind Ausbildungsstätte und beschäftigen regelmäßig Studierende, die sich in der Ausbildung zum Erzieher befinden.</p>
  <div class="stats three">
    <div class="stat"><b>100 %</b><span>Fachkraftquote</span></div>
    <div class="stat"><b>75 %</b><span>Übertritt an weiterführende Schulen 2021</span></div>
    <div class="stat"><b data-from="6">1,4</b><span>Zufriedenheitsnote in der Elternbefragung</span></div>
  </div></div>
</div>''' + features([
    "Großzügige Räume zum Spielen und Lernen",
    "Weißer Raum zum Entspannen",
    "Überlange Öffnungszeiten von 6:45 Uhr bis 18:00 Uhr, auch in den Schulferien",
    "Hauseigene Küche, in der täglich von zwei Köchinnen mit regionalen Zutaten frisch gekocht wird",
    "Tägliche Aktionen während der Schulferien mit Erlebnischarakter",
    "Begleitete, korrigierte Hausaufgaben",
    "Hohe Übertrittsquote an weiterführende Schulen (Quelle: Übertritt an weiterführende Schulen 2021: 75 %)",
    "Großer Garten zum Toben",
    "Tägliche Aktionen für Kinder, z. B. Kinderyoga, Mathespiele, Bewegungsspiele …",
    "Ferienbetreuung",
    "Ausflug an jedem Freitag, z. B. Stadtbücherei, Museum …",
    "Hohe Elternzufriedenheit mit dem Hort (Quelle: Elternbefragung, Zufriedenheitsnote 1,4)",
], [("Räume &amp; Küche", [0, 1, 3, 7]), ("Zeiten &amp; Ferien", [2, 4, 9, 10]), ("Lernen &amp; Qualität", [5, 6, 8, 11])]))
hort += section("schulen", "Zusammenarbeit mit den Schulen", "Gemeinsam mit den Schulen", "", f'''
<div class="split">
  <figure class="reveal"><a href="img/zusammenarbeit.jpg" data-full="img/zusammenarbeit.jpg" data-group="schule" data-title="Zusammenarbeit mit den Schulen" data-text="Besuch des Hortes auf dem Adventszauber der Josefschule">{img("img/zusammenarbeit.jpg", "Besuch des Hortes auf dem Adventszauber der Josefschule")}</a>
  <figcaption>Besuch des Hortes auf dem Adventszauber der Josefschule</figcaption></figure>
  <div class="reveal"><p>Wir pflegen eine enge Zusammenarbeit mit den Schulen unserer Hortkinder – zum Beispiel beim Besuch des Hortes auf dem Adventszauber der Josefschule.</p>
  <p>Wir sind offen für alle Schulformen: Grundschulen, Mittelschulen, Realschulen, Gymnasien sowie Förderschulen.</p></div>
</div>''', cls="alt")
hort += section("fragen", "Meist gestellte Fragen", "Häufige Fragen zum Kinderhort", "", faq([
    ("Hat der Hort auch in den Schulferien geöffnet?", "In den Schulferien hat der Hort von 6:45 bis 18:00 Uhr geöffnet. Die Kinder können entsprechend der von den Eltern gebuchten Ferientage und Ferienstunden den Hort besuchen. Die Schließtage des Hortes betragen maximal 30 pro Jahr."),
    ("Ich habe mehrere Kinder in dieser Kita – ist die Kita in den Ferien für alle Kinder geöffnet?", "Kinderkrippe, Kindergarten und Kinderhort haben gleiche Ferientage."),
    ("Braucht mein Kind im Hort eine Brotzeit?", "Im Hort erhält jedes Kind ein Mittagessen. Falls Ihr Kind am Nachmittag noch einmal Hunger bekommt, ist es ratsam, eine Brotzeit und eine Trinkflasche mit Wasser mitzuschicken."),
    ("Was passiert, wenn mein Kind im Kinder- und Jugendhort Grombühl keine Hausaufgaben machen möchte?", "Die Hausaufgabenzeit im Hort ist ein fester Bestandteil des Tages. Sie beginnt für alle Kinder zur gleichen Zeit. Mit Ihrem Kind gehen alle anderen Kinder gemeinsam als Gruppe in die Hausaufgabenzeit. Dadurch sind die Hausaufgaben für jedes Kind selbstverständlich und wichtig."),
    ("Kann ich mein Kind abholen, wann ich möchte?", "Die von Ihnen gebuchten Stunden stellen die Grundlage für die Förderung der Kita durch den Freistaat Bayern dar und müssen auch in diesem Umfang genutzt werden."),
    ("Kann ich mein Kind vor der Hausaufgabenzeit abholen?", "Unsere Mindestbuchungszeit beträgt 4 bis 5 Stunden, somit ist die Hausaufgabenzeit Bestandteil des Hortalltages. Ausnahmen bilden hier wichtige Arzttermine."),
    ("Mein Kind kann nicht in die Einrichtung kommen (z. B. wegen Krankheit). Was muss ich tun?", f'Bitte geben Sie uns in diesem Fall telefonisch oder per E-Mail Bescheid – am einfachsten mit unserer <a href="{KRANK_MAIL}">vorbereiteten Krankmeldung per E-Mail</a>.'),
    ("Sie arbeiten mit einem gruppenübergreifenden Konzept. Was bedeutet das?", "Bei uns im Hort gibt es, abgesehen von der Hausaufgabenzeit, keine festen Gruppen. Die Kinder suchen sich ihre Spielbereiche und -partner selbst. Jeder Bereich ist mit einem Erzieher besetzt. So stehen den Kindern jederzeit alle Bereiche, wie etwa Garten oder Kreativraum, zur Verfügung."),
]))
hort += abc_section("KinderhortABC", "KinderhortABC herunterladen")
hort += ferienplan_section()
page("kinderhort.html", "Kinderhort", "Kinderhort im Kath. Kinder- und Jugendhort Grombühl, Würzburg: Betreuung für Schulkinder aller Schulformen von 6:45 bis 18:00 Uhr – mit Hausaufgabenbetreuung, Ferienprogramm und Freitagsausflügen.", "kinderhort.html", hort, "theme-hort")

# =====================================================================
# AKTUELLES
# =====================================================================
akt = page_hero("Aktuelles", "Hier finden Sie aktuelle Termine und Informationen.", "img/bauecke-2.jpg", "Termine &amp; Infos",
                [("termine", "Termine"), ("elternbrief", "Liebe Eltern"), ("ferienplan", "Ferienplan")], alt="Bauecke im Kinderhort")
akt += section("termine", "Vormerktermine", "Aktuelle Termine", "Vormerktermine für Sie, liebe Eltern:", f'''
<div class="notes-grid">
  <div>
  <div class="view-switch no-print" role="group" aria-label="Ansicht der Termine"><span class="vs-knob" aria-hidden="true"></span>
    <button type="button" data-view="list" aria-pressed="true">{icon("list", 18)} Liste</button><button type="button" data-view="cal" aria-pressed="false">{icon("grid", 18)} Kalender</button></div>
  <div class="month-cal" hidden></div>
  <ul class="event-list">
    {"".join(ev(r) for r in TERMINE)}
  </ul>
  <p class="events-empty muted" hidden>Aktuell stehen keine weiteren Termine an.</p>
  <div class="btn-row"><a class="btn btn-ghost" href="downloads/termine.ics" download>{icon("calendar", 20)} Alle in den Kalender</a></div>
  <div class="saved-row" hidden><button class="btn btn-primary js-saved-ics" type="button">{icon("calendar", 20)} Gemerkte Termine in den Kalender (<span class="saved-n">0</span>)</button></div>
  </div>
  <div class="note-card reveal">
    <h3>Sankt Martin</h3>
    <p>Der Sankt-Martins-Umzug / das Martinssingen findet auch in diesem Jahr wieder im kleinen Rahmen in den einzelnen Gruppen statt.</p>
    <h3 class="mt-2">Schließtage</h3>
    <p>Die nächsten Schließtage und alle Ferienzeiten für 2026/2027 finden Sie im <a href="#ferienplan">Ferienplan</a> unten.</p>
    <a class="btn btn-primary" href="downloads.html">{icon("file", 20)} Zu den Downloads</a>
  </div>
</div>''')
BRIEFE = read_csv("elternbriefe.csv")
def brief(i, r):
    paras = "".join(f"<p>{p.strip()}</p>" for p in r["Text"].split("||") if p.strip())
    gruss = f'<p class="sign-off">{r["Gruß"].replace("||", "<br>")}</p>' if r.get("Gruß") else ""
    return (f'<details class="brief reveal"{" open" if i == 0 else ""} data-such="{e((r["Titel"] + " " + r["Text"]).lower())}">'
            f'<summary><span class="brief-t">{e(r["Titel"])}</span><small>{e(r["Stand"])}</small></summary><div>{paras}{gruss}</div></details>')
akt += section("elternbrief", "Elternbriefe", "Liebe Eltern!", "Alle Elternbriefe an einem Ort – der neueste steht oben.", f'''
<div class="briefe">
  <div class="faq-search brief-search reveal"{" hidden" if len(BRIEFE) < 2 else ""}><label class="visually-hidden" for="brief-suche">Elternbriefe durchsuchen</label>{icon("search", 20)}<input type="search" id="brief-suche" placeholder="Elternbriefe durchsuchen" autocomplete="off" enterkeyhint="search"><span class="faq-count" aria-live="polite"></span></div>
  {"".join(brief(i, r) for i, r in enumerate(BRIEFE))}
  <p class="brief-empty muted" hidden>Kein Elternbrief gefunden.</p>
</div>''', cls="alt")
akt += ferienplan_section(cls="")
page("aktuelles.html", "Aktuelles", "Aktuelle Termine, Vormerktermine und Schließtage des Kath. Kinder- und Jugendhorts Grombühl in Würzburg.", "aktuelles.html", akt)

# =====================================================================
# DOWNLOADS
# =====================================================================
def copy_btn(value, label):
    return f'<button class="copy-btn" type="button" data-copy="{e(value)}" data-label="{e(label)}" aria-label="{e(label)} kopieren"><span class="ic ic-copy">{icon("copy", 18)}</span><span class="ic ic-done">{icon("check", 18)}</span></button>'

NEU_SEIT = {"downloads/Ferienplan_2026_27.pdf": "2026-11-15"}   # „neu“-Hinweis 30 Tage lang
def pdf_meta(href):
    p = os.path.join(W, href)
    size = os.path.getsize(p)
    raw = open(p, "rb").read()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", raw)) or 1
    thumb = "img/dl-" + os.path.splitext(os.path.basename(href))[0].lower().replace("_", "-") + ".webp"
    tp = os.path.join(W, thumb)
    if not os.path.exists(tp) or os.path.getmtime(tp) < os.path.getmtime(p):
        try:
            import subprocess, tempfile
            from PIL import Image
            with tempfile.TemporaryDirectory() as td:
                subprocess.run(["pdftoppm", "-png", "-r", "40", "-f", "1", "-l", "1", "-singlefile", p, os.path.join(td, "s")], check=True, capture_output=True)
                Image.open(os.path.join(td, "s.png")).convert("RGB").save(tp, "WEBP", quality=72)
        except Exception:
            thumb = None
    return size, pages, thumb if thumb and os.path.exists(tp) else None

def dl(href, title, kind):
    size, pages, thumb = pdf_meta(href)
    sub = f"{kind} · PDF, {round(size / 1024)} KB, {pages} {'Seite' if pages == 1 else 'Seiten'}"
    neu = f'<span class="new" data-neu="{NEU_SEIT[href]}" hidden>neu</span>' if href in NEU_SEIT else ""
    peek = f'<span class="peek" aria-hidden="true"><img src="{thumb}" alt="" loading="lazy" width="120" height="170"></span>' if thumb else ""
    return f'<li><a class="dl-link" href="{href}" download><span class="ficon">PDF</span><span>{title}{neu}<small>{sub}</small></span>{peek}</a></li>'
plan_dl = dl("downloads/Ferienplan_2026_27.pdf", "Schließtage 2026/2027", "Ferienplan")
downl = page_hero("Downloads", "Hier finden Sie weitere Informationsblätter.", "img/p2160170.jpg", "Infoblätter &amp; Formulare", alt="Spielbereich")
def lotse(q, text, links):
    return (f'<details class="lotse-item" name="lotse"><summary>{q}</summary><div><p>{text}</p><div class="lotse-links">' +
            "".join(f'<a class="btn {"btn-primary" if i == 0 else "btn-ghost"}" href="{h}"{" download" if h.endswith((".pdf", ".ics")) else ""}>{icon(ic, 20)} {t}</a>' for i, (h, ic, t) in enumerate(links)) + "</div></div></details>")
downl += section("lotse", "Schnell zum Ziel", "Was möchten Sie tun?", "Eine Frage antippen – und Sie bekommen genau das passende Formular oder den richtigen Weg.", '<div class="lotse reveal">' + "".join([
    lotse("Mein Kind ist krank", "Bitte melden Sie Ihr Kind per E-Mail oder telefonisch direkt in der Gruppe ab.", [(KRANK_MAIL, "mail", "Krankmeldung per E-Mail"), ("kontakt.html#durchwahl-finden", "phone", "Durchwahl der Gruppe")]),
    lotse("Mein Kind braucht Medikamente", "Medikamente können wir nur mit einer unterschriebenen Medikamentenvereinbarung geben.", [("downloads/Medikamentenvereinbarung.pdf", "file", "Medikamentenvereinbarung")]),
    lotse("Ich möchte wissen, wann geschlossen ist", "Alle Schließtage stehen im Ferienplan – auch als Kalenderdatei fürs Handy.", [("downloads/Ferienplan_2026_27.pdf", "file", "Ferienplan als PDF"), ("downloads/schliesstage.ics", "calendar", "Schließtage in den Kalender")]),
    lotse("Ich habe Fragen zum Hort", "Viele Antworten stehen im KinderhortABC – oder Sie fragen uns direkt.", [("downloads/HortABC.pdf", "file", "KinderhortABC"), ("kontakt.html#frag", "search", "Schnelle Antwort finden")]),
    lotse("Ich möchte einen Platz anfragen", "Die vorbereitete E-Mail enthält alle Angaben, die wir für Ihre Anfrage brauchen.", [(PLATZ_MAIL, "mail", "Platz anfragen")]),
]) + "</div>", cls="tight")
downl += section("dateien", "Downloads", "Informationsblätter zum Herunterladen", "", f'''
<div class="downloads">
  <div class="dl-group theme-krippe reveal"><h3>Kinderkrippe</h3><ul>{plan_dl}</ul></div>
  <div class="dl-group theme-kiga reveal"><h3>Kindergarten</h3><ul>{plan_dl}</ul></div>
  <div class="dl-group theme-hort reveal"><h3>Kinderhort</h3><ul>{plan_dl}
    {dl("downloads/HortABC.pdf", "KinderhortABC", "Alles Wichtige von A bis Z")}
    {dl("downloads/Medikamentenvereinbarung.pdf", "Medikamentenvereinbarung", "Formular zum Ausfüllen")}</ul></div>
</div>''')
def ics_dl(href, title, sub):
    return f'<li><a class="dl-link" href="{href}" download><span class="ficon">ICS</span><span>{title}<small>{sub}</small></span></a></li>'
downl += section("kalender", "Kalender", "Termine direkt ins Handy übernehmen", "Die Kalenderdateien lassen sich mit einem Tipp in den Kalender von iPhone, Android oder Outlook übernehmen.", f'''
<div class="downloads two">
  <div class="dl-group reveal"><h3>Schließtage</h3><ul>{ics_dl("downloads/schliesstage.ics", f"Schließtage {PLAN_JAHR}", "Kalenderdatei für alle Bereiche")}</ul></div>
  <div class="dl-group reveal"><h3>Termine</h3><ul>{ics_dl("downloads/termine.ics", "Termine &amp; Veranstaltungen", "Kalenderdatei")}</ul></div>
</div>
<div class="abo reveal" id="abo">
  <div class="abo-head"><h3>Noch einfacher: Kalender abonnieren</h3><p>Dann erscheinen neue Termine und Schließtage <strong>von selbst</strong> in Ihrem Kalender – ohne erneutes Herunterladen.</p></div>
  <div class="abo-tabs" role="tablist" aria-label="Gerät wählen"><span class="vs-knob" aria-hidden="true"></span>
    <button type="button" role="tab" id="abo-t1" aria-controls="abo-ios" aria-selected="true">iPhone / iPad</button><button type="button" role="tab" id="abo-t2" aria-controls="abo-android" aria-selected="false" tabindex="-1">Android</button><button type="button" role="tab" id="abo-t3" aria-controls="abo-pc" aria-selected="false" tabindex="-1">Outlook</button></div>
  <div class="abo-panel" role="tabpanel" id="abo-ios" aria-labelledby="abo-t1"><ol><li>Unten auf „Termine abonnieren“ oder „Schließtage abonnieren“ tippen.</li><li>„Abonnieren“ bestätigen.</li><li>Fertig – neue Einträge erscheinen automatisch im Kalender.</li></ol></div>
  <div class="abo-panel" role="tabpanel" id="abo-android" aria-labelledby="abo-t2" hidden><ol><li>Abo-Adresse unten kopieren.</li><li>Am Computer Google Kalender öffnen: „Weitere Kalender“ → „Per URL“ → Adresse einfügen.</li><li>Fertig – der Kalender erscheint auch auf dem Handy.</li></ol></div>
  <div class="abo-panel" role="tabpanel" id="abo-pc" aria-labelledby="abo-t3" hidden><ol><li>Abo-Adresse unten kopieren.</li><li>In Outlook: „Kalender hinzufügen“ → „Aus dem Internet abonnieren“ → Adresse einfügen.</li><li>Fertig – Outlook holt neue Termine von selbst.</li></ol></div>
  <div class="abo-links">
    <a class="btn btn-primary" href="webcal://{SITE.split("//", 1)[1].rstrip("/")}/downloads/termine.ics">{icon("calendar", 20)} Termine abonnieren</a>{copy_btn(SITE + "downloads/termine.ics", "Abo-Adresse Termine")}
    <a class="btn btn-ghost" href="webcal://{SITE.split("//", 1)[1].rstrip("/")}/downloads/schliesstage.ics">{icon("calendar", 20)} Schließtage abonnieren</a>{copy_btn(SITE + "downloads/schliesstage.ics", "Abo-Adresse Schließtage")}
  </div>
</div>''', cls="alt")
downl += section("", "Aktuelles", "Hier finden Sie alle aktuellen Termine", "",
                 f'<a class="btn btn-primary" href="aktuelles.html">Zu den Terminen {icon("arrow", 20)}</a>', cls="tight")
page("downloads.html", "Downloads", "Downloads des Kath. Kinder- und Jugendhorts Grombühl: Ferienplan, KinderhortABC und Medikamentenvereinbarung.", "downloads.html", downl)

# =====================================================================
# KONTAKT
# =====================================================================

def tel(label, num_display, num):
    return f'<li><span>{label}</span><a href="tel:{num}">{num_display.replace(" ", "&nbsp;")}</a></li>'
kon = simple_hero("Kontakt", "Wir freuen uns auf Sie und Ihr Kind – rufen Sie direkt in der Gruppe an oder schreiben Sie uns.", "So erreichen Sie uns")
kon += f'''<section class="section tight" id="schnell">
  <div class="container">
    <div class="quick-grid">
      <a class="quick-card reveal" href="{KRANK_MAIL}">
        <span class="quick-icon">{icon("mail", 26)}</span>
        <span><strong>Kind krankmelden</strong><span>Öffnet eine vorbereitete E-Mail – nur noch Name, Gruppe und Zeitraum eintragen. Gerne auch telefonisch in der Gruppe.</span></span>
      </a>
      <a class="quick-card reveal" href="{PLATZ_MAIL}">
        <span class="quick-icon">{icon("users", 26)}</span>
        <span><strong>Platz anfragen</strong><span>Öffnet eine vorbereitete E-Mail mit allen Angaben, die wir für Ihre Anfrage brauchen.</span></span>
      </a>
      <div class="quick-card status-mini reveal" id="status-kontakt" hidden>
        <span class="quick-icon">{icon("clock", 26)}</span>
        <span><strong class="status-today"></strong><span class="status-sub"></span></span>
      </div>
    </div>
  </div>
</section>'''
kon += section("frag", "Schnelle Antwort", "Fragen Sie einfach", "Tippen Sie Ihre Frage ein – die Antwort kommt aus unseren häufigen Fragen. Findet sich nichts, rufen Sie uns gern an.", f'''
<div class="ask reveal">
  <div class="ask-log" aria-live="polite"><div class="msg bot">Hallo! Was möchten Sie wissen?<div class="sugg"><button type="button">Brotzeit</button><button type="button">Eingewöhnung</button><button type="button">Schulferien</button><button type="button">Windeln</button></div></div></div>
  <form class="ask-form"><label class="visually-hidden" for="ask-in">Ihre Frage</label><input id="ask-in" type="text" autocomplete="off" enterkeyhint="send" placeholder="Ihre Frage, z. B. „Braucht mein Kind eine Brotzeit?“"><button class="btn btn-primary" type="submit">Fragen</button></form>
</div>''', cls="tight alt")
kon += f'''<section class="section">
  <div class="container contact-grid">
    <div>
      <h2 class="visually-hidden">Durchwahlen der Gruppen</h2>
      <div class="dial reveal" id="durchwahl-finden">
        <label for="durchwahl">Durchwahl finden</label>
        <div class="dial-field">{icon("search", 20)}<input id="durchwahl" type="text" placeholder="Gruppe eingeben, z. B. Spatzen" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search"></div>
        <div class="dial-out" aria-live="polite"></div>
      </div>
      <div class="phone-card theme-krippe reveal"><h3><span class="dot"></span>Kinderkrippe</h3><ul class="phone-list">
        {tel("Sternengruppe", "0931 2789892 15", "+49931278989215")}
        {tel("Sonnengruppe", "0931 2789892 14", "+49931278989214")}
      </ul></div>
      <div class="phone-card theme-kiga reveal"><h3><span class="dot"></span>Kindergarten</h3><ul class="phone-list">
        {tel("Bienengruppe", "0931 2789892 13", "+49931278989213")}
        {tel("Spatzengruppe", "0931 2789892 12", "+49931278989212")}
        {tel("Bärengruppe", "0931 2789892 11", "+49931278989211")}
      </ul></div>
      <div class="phone-card theme-hort reveal"><h3><span class="dot"></span>Kinderhort</h3><ul class="phone-list">
        {tel("Allgemein", "0931 2789892 0", "+4993127898920")}
        <li><span>Mail</span><a href="mailto:kinderhort.grombuehl@t-online.de">kinderhort.grombuehl@t-online.de</a></li>
      </ul></div>
    </div>
    <aside class="address-card reveal" id="anschrift">
      <h2>Anschrift</h2>
      <address>
        <div class="contact-row">{icon("pin")}<span>{ORG}<br>Lindleinstraße 20<br>97080 Würzburg</span></div>
        <div class="contact-row">{icon("phone")}<a href="tel:+4993127898920">0931&nbsp;2789892&nbsp;0</a>{copy_btn("0931 2789892 0", "Telefonnummer")}</div>
        <div class="contact-row">{icon("mail")}<a href="mailto:kinderhort.grombuehl@t-online.de">kinderhort.grombuehl@t-online.de</a>{copy_btn(MAIL, "E-Mail-Adresse")}</div>
      </address>
      <div class="btn-row">
        <a class="btn btn-primary" href="downloads/kinderhort-grombuehl.vcf" download>{icon("users", 20)} Kontakt aufs Handy speichern</a>
        <a class="btn btn-ghost" href="https://www.openstreetmap.org/search?query=Lindleinstra%C3%9Fe%2020%2C%2097080%20W%C3%BCrzburg" target="_blank" rel="noopener">{icon("pin", 20)} Auf der Karte anzeigen</a>
      </div>
      <p class="vcf-note muted">Legt den Kinderhort mit allen Durchwahlen im Adressbuch an.</p>
    </aside>
  </div>
</section>'''
page("kontakt.html", "Kontakt", "Kontakt zum Kath. Kinder- und Jugendhort Grombühl, Lindleinstraße 20, 97080 Würzburg – Telefonnummern aller Gruppen und E-Mail.", "kontakt.html", kon)

# =====================================================================
# IMPRESSUM
# =====================================================================
imp = simple_hero("Impressum", "Angaben gemäß § 5 DDG", "Rechtliches")
imp += f'''<section class="section"><div class="container"><div class="prose">
<h2>Angaben gemäß § 5 DDG</h2>
<p>{ORG}<br>Lindleinstr. 20<br>97080 Würzburg</p>
<p>Vereinsregister: VR 187<br>Registergericht: Amtsgericht Würzburg Registergericht</p>
<p><strong>Vertreten durch:</strong><br>Helmut Burmester</p>
<h2>Kontakt</h2>
<p>Telefon: <a href="tel:+4993127898920">0931&nbsp;27898920</a><br>E-Mail: <a href="mailto:kinderhort.grombuehl@t-online.de">kinderhort.grombuehl@t-online.de</a></p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>Petra Lachnit<br>{ORG}<br>Lindleinstr. 20<br>97080 Würzburg</p>
<h2>Verbraucherstreitbeilegung / Universalschlichtungsstelle</h2>
<p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h3>Haftung für Inhalte</h3>
<p>Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG sind wir als Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.</p>
<p>Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden von entsprechenden Rechtsverletzungen werden wir diese Inhalte umgehend entfernen.</p>
<h3>Haftung für Links</h3>
<p>Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar.</p>
<p>Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.</p>
<h3>Urheberrecht</h3>
<p>Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.</p>
<p>Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Inhalte umgehend entfernen.</p>
</div></div></section>'''
page("impressum.html", "Impressum", "Impressum des Kath. Kinder- und Jugendhorts Grombühl e. V., Würzburg.", "impressum.html", imp)

# =====================================================================
# DATENSCHUTZ (Vorlage – vom Träger zu prüfen und zu ergänzen)
# =====================================================================
dsg = simple_hero("Datenschutz", "Informationen zum Umgang mit Ihren Daten auf dieser Webseite", "Rechtliches")
dsg += f'''<section class="section"><div class="container"><div class="prose">
<p class="todo-hinweis"><strong>Hinweis für den Träger:</strong> Diese Datenschutzerklärung ist eine Vorlage. Bitte die markierten Stellen ergänzen und den Text vor der Veröffentlichung prüfen lassen (z. B. durch den Datenschutzbeauftragten der Diözese).</p>
<h2>1. Verantwortliche Stelle</h2>
<p>{ORG}<br>Lindleinstr. 20<br>97080 Würzburg<br>Telefon: 0931 27898920<br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a><br>Vertreten durch: Helmut Burmester</p>
<h2>2. Datenschutzbeauftragte/r</h2>
<p><mark>[Bitte ergänzen: Name und Kontakt der/des zuständigen Datenschutzbeauftragten]</mark></p>
<p>Als katholische Einrichtung unterliegen wir dem Gesetz über den Kirchlichen Datenschutz (KDG).</p>
<h2>3. Hosting und Server-Protokolle</h2>
<p>Diese Webseite wird bei <mark>[Bitte ergänzen: Name und Anschrift des Hosting-Anbieters]</mark> betrieben. Beim Aufruf der Seiten speichert der Server automatisch technisch notwendige Informationen (z. B. IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp). Diese Daten dienen ausschließlich dem sicheren Betrieb der Webseite und werden nach <mark>[Bitte ergänzen: Speicherdauer, z. B. 7 Tagen]</mark> gelöscht.</p>
<h2>4. Keine Cookies, kein Tracking</h2>
<p>Diese Webseite setzt keine Cookies, verwendet keine Analyse- oder Werbedienste und bindet keine Inhalte von Drittanbietern ein. Schriftarten werden direkt von unserem Server geladen; es findet keine Verbindung zu Google oder anderen Anbietern statt.</p>
<h2>5. Kontakt per E-Mail und Telefon</h2>
<p>Wenn Sie uns per E-Mail oder Telefon kontaktieren (z. B. für eine Krankmeldung oder Platzanfrage), verarbeiten wir Ihre Angaben ausschließlich zur Bearbeitung Ihres Anliegens. Die Buttons „Kind krankmelden“ und „Platz anfragen“ öffnen lediglich Ihr eigenes E-Mail-Programm; über diese Webseite selbst werden keine Daten übertragen oder gespeichert.</p>
<h2>6. Externe Links</h2>
<p>Der Link „Auf der Karte anzeigen“ führt zu OpenStreetMap. Erst wenn Sie ihn anklicken, wird eine Verbindung zu den Servern der OpenStreetMap Foundation hergestellt; dort gelten deren Datenschutzbestimmungen.</p>
<h2>7. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung Ihrer Daten sowie ein Widerspruchsrecht. Zudem können Sie sich bei der zuständigen kirchlichen Datenschutzaufsicht beschweren: <mark>[Bitte ergänzen: zuständige Datenschutzaufsicht, z. B. Gemeinsame Datenschutzaufsicht der bayerischen (Erz-)Diözesen]</mark>.</p>
<p class="muted">Stand: <mark>[Datum ergänzen]</mark></p>
</div></div></section>'''
page("datenschutz.html", "Datenschutz", "Datenschutzerklärung des Kath. Kinder- und Jugendhorts Grombühl e. V., Würzburg.", "datenschutz.html", dsg)

# =====================================================================
# FEHLERSEITE (404)
# =====================================================================
nf = f'''<section class="section e404">
  <div class="container">
    <div class="e404-card">
      <div class="num4" aria-label="404"><span>4</span><i aria-hidden="true"></i><span>4</span></div>
      <h1>Hoppla, diese Seite gibt es nicht (mehr).</h1>
      <p>Vielleicht hat sich die Adresse geändert – unsere Webseite ist neu. Eines davon hilft bestimmt weiter:</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="index.html">{icon("home", 20)} Startseite</a>
        <a class="btn btn-ghost" href="aktuelles.html#termine">{icon("calendar", 20)} Termine</a>
        <a class="btn btn-ghost" href="kontakt.html">{icon("phone", 20)} Kontakt</a>
        <button class="btn btn-ghost js-search" type="button">{icon("search", 20)} Suchen</button>
      </div>
    </div>
  </div>
</section>'''
page("404.html", "Seite nicht gefunden", "Diese Seite gibt es leider nicht.", "", nf, head='\n<meta name="robots" content="noindex">\n<base href="/">')
PAGES_WRITTEN.remove("404.html")

# ---------- Einblicke ins Haus (gemeinsame Galerie mit Filter) ----------
def einblicke():
    pick = [("krippe", "Krippe", krippe_tour[:4]), ("kiga", "Kindergarten", kiga_tour[:4]), ("hort", "Hort", hort_tour[:4])]
    figs = []
    for k in range(4):
        for key, name, items in pick:
            if k < len(items):
                im, t, sub = items[k]
                figs.append(f'<figure class="gal-item" data-cat="{key}"><button type="button" data-full="{im}" data-group="einblicke" data-title="{e(t)}" data-text="{e(name + " – " + sub)}" aria-label="{e(t)} – {e(sub)}, {name} (Bild vergrößern)">{img(im, t + " – " + sub, sizes="(max-width: 700px) 50vw, 25vw")}</button><figcaption>{name}</figcaption></figure>')
    chips = "".join(f'<button type="button" data-cat="{k}" aria-pressed="{"true" if k == "alle" else "false"}">{n}</button>' for k, n in [("alle", "Alle"), ("krippe", "Krippe"), ("kiga", "Kindergarten"), ("hort", "Hort")])
    return section("einblicke", "Einblicke", "Ein Blick in alle drei Bereiche", "Wählen Sie einen Bereich – die Fotos sortieren sich neu. Ein Klick vergrößert das Bild.",
                   f'<div class="gal-chips no-print" role="group" aria-label="Bereich wählen">{chips}</div><div class="gal-grid">{"".join(figs)}</div>')
_p = os.path.join(W, "index.html")
_h = open(_p, encoding="utf-8").read()
assert "<!--EINBLICKE-->" in _h
open(_p, "w", encoding="utf-8").write(_h.replace("<!--EINBLICKE-->", glossar(einblicke())))

# ---------- Alle häufigen Fragen für den Fragen-Helfer ----------
FAQ_ALLE = []
for _pg, _name in [("kinderkrippe.html", "Kinderkrippe"), ("kindergarten.html", "Kindergarten"), ("kinderhort.html", "Kinderhort")]:
    _h = open(os.path.join(W, _pg), encoding="utf-8").read()
    for _q, _a in re.findall(r'<details class="reveal"><summary>(.*?)</summary><div><p>(.*?)</p></div></details>', _h, flags=re.S):
        FAQ_ALLE.append({"q": re.sub(r"<[^>]+>", "", _q), "a": re.sub(r"<[^>]+>", "", _a), "u": _pg + "#fragen", "b": _name})

# ---------- Kontakt fürs Adressbuch (.vcf) ----------
VCF_NUMMERN = [("Zentrale", "+4993127898920")]
for _lab, _num in re.findall(r'<li><span>([^<]+)</span><a href="tel:([^"]+)">', open(os.path.join(W, "kontakt.html"), encoding="utf-8").read()):
    if (_lab, _num) not in VCF_NUMMERN and _num != "+4993127898920": VCF_NUMMERN.append((_lab, _num))
_v = ["BEGIN:VCARD", "VERSION:3.0", "N:;;;;", "FN:Kinderhort Grombühl", f"ORG:{ORG}", f"EMAIL;TYPE=WORK:{MAIL}",
      "ADR;TYPE=WORK:;;Lindleinstraße 20;Würzburg;;97080;Deutschland", f"URL:{SITE}", "X-ABShowAs:COMPANY"]
for _i, (_lab, _num) in enumerate(VCF_NUMMERN, 1):
    _v += [f"item{_i}.TEL:{_num}", f"item{_i}.X-ABLabel:{_lab}"]
_v.append("END:VCARD")
with open(os.path.join(W, "downloads/kinderhort-grombuehl.vcf"), "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(_v) + "\r\n")

# ---------- Web-App-Manifest („Als App auf den Startbildschirm“) ----------
with open(os.path.join(W, "manifest.webmanifest"), "w", encoding="utf-8") as f:
    json.dump({"name": ORG, "short_name": "Kinderhort", "description": "Termine, Schließtage, Krankmeldung und Kontakt des Kinderhorts Grombühl.",
               "lang": "de", "start_url": "./index.html", "scope": "./", "display": "standalone", "background_color": "#A8C5C0", "theme_color": "#A8C5C0",
               "icons": [{"src": "img/app-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "img/app-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": "img/app-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
               "shortcuts": [{"name": "Termine", "url": "./aktuelles.html#termine"}, {"name": "Kind krankmelden", "url": "./kontakt.html#schnell"}]},
              f, ensure_ascii=False, indent=1)

# ---------- Suchindex (Schnellsuche, Strg+K) ----------
def _bereich(page, name, extra):
    secs = [("ueberblick", "Zielgruppe & Öffnungszeiten", "alter uhrzeit zeiten wann geöffnet küche essen mittagessen"),
            ("raeume", "Räumlichkeiten", "räume gruppenraum turnraum weißer raum garten gruppen"),
            ("rundgang", "Virtueller Rundgang", "fotos bilder galerie ansehen"),
            ("tagesablauf", "Tagesablauf", "ablauf bringzeit abholzeit abholen mittagsschlaf hausaufgaben"),
            ("auszeichnung", "Das zeichnet uns aus", "vorteile besonderheiten konzept fachkraft"),
            ("fragen", "Häufige Fragen", "faq fragen antworten windeln eingewöhnung brotzeit krank ferien katholisch"),
            ("ferienplan", "Ferienplan & Schließtage", "ferien schließtage urlaub geschlossen")]
    out = [(name, "Bereich", page, extra)]
    out += [(t, name, f"{page}#{a}", k) for a, t, k in secs]
    return out

SUCHE = [("Startseite", "Überblick", "index.html", "home start willkommen")]
SUCHE += _bereich("kinderkrippe.html", "Kinderkrippe", "krippe baby kleinkind 11 monate sonnengruppe sternengruppe u3")
SUCHE += _bereich("kindergarten.html", "Kindergarten", "kiga 3 jahre vorschule bärengruppe bienengruppe spatzengruppe englisch")
SUCHE += _bereich("kinderhort.html", "Kinderhort", "hort schulkind schule hausaufgaben ferienbetreuung mittagsbetreuung")
SUCHE += [
    ("Zusammenarbeit mit den Schulen", "Kinderhort", "kinderhort.html#schulen", "schule josefschule grundschule"),
    ("Aktuelle Termine", "Aktuelles", "aktuelles.html#termine", "termine veranstaltungen kalender weihnachtsmarkt nikolaus martin"),
    ("Elternbriefe", "Aktuelles", "aktuelles.html#elternbrief", "brief briefe eltern elternbrief archiv überstunden schließzeit"),
    ("Was möchten Sie tun?", "Downloads · Formular-Lotse", "downloads.html#lotse", "formular welches formular medikamente krank lotse hilfe"),
    ("Kalender abonnieren", "Downloads", "downloads.html#abo", "abo abonnieren webcal kalender automatisch outlook google iphone"),
    ("Fragen Sie einfach", "Kontakt · Schnelle Antwort", "kontakt.html#frag", "frage antwort hilfe chat"),
    ("Einblicke ins Haus", "Startseite · Fotos", "index.html#einblicke", "fotos bilder galerie räume"),
    ("Ferienplan & Schließtage", "Aktuelles", "aktuelles.html#ferienplan", "ferien schließtage urlaub geschlossen weihnachten ostern pfingsten sommer"),
    ("Downloads", "Unterlagen", "downloads.html", "pdf formulare unterlagen herunterladen"),
    ("KinderhortABC", "Download · PDF", "downloads/HortABC.pdf", "hort abc infos a bis z"),
    ("Medikamentenvereinbarung", "Download · PDF", "downloads/Medikamentenvereinbarung.pdf", "medikamente formular arznei"),
    ("Ferienplan als PDF", "Download · PDF", "downloads/Ferienplan_2026_27.pdf", "ferien schließtage aushang"),
    ("Kalenderdateien", "Downloads", "downloads.html#kalender", "ics kalender handy termine schließtage"),
    ("Kontakt aufs Handy speichern", "Kontakt · Adressbuch", "kontakt.html#anschrift", "adressbuch kontakt speichern vcard visitenkarte handy telefonbuch"),
    ("Kontakt & Durchwahlen", "Telefon, E-Mail, Anschrift", "kontakt.html", "telefon telefonnummer anrufen email mail adresse anschrift anfahrt lindleinstraße sternengruppe sonnengruppe bienengruppe spatzengruppe bärengruppe"),
    ("Kind krankmelden", "Vorbereitete E-Mail", "kontakt.html#schnell", "krank krankmeldung abwesend fehlt entschuldigen"),
    ("Platz anfragen", "Vorbereitete E-Mail", "kontakt.html#schnell", "anmeldung anmelden platz kitaplatz bewerbung aufnahme"),
    ("Impressum", "Rechtliches", "impressum.html", "impressum verein vorstand"),
    ("Datenschutz", "Rechtliches", "datenschutz.html", "datenschutz dsgvo kdg cookies"),
]

# ---------- Daten für Status-Anzeige (js/daten.js) ----------
kita = {
    "schliesszeiten": [{"name": r["Anlass"], "von": d(r["erster Schließtag"]).isoformat(), "bis": d(r["letzter Schließtag"]).isoformat(), "tage": int(r["Schließtage"])} for r in SCHLIESSTAGE],
    "feiertage": [{"datum": d(r["Datum"]).isoformat(), "name": r["Feiertag"]} for r in FEIERTAGE],
    "planEnde": d(SCHLIESSTAGE[-1]["wieder geöffnet"]).isoformat(),
    "oeffnung": "06:45", "schluss": "18:00",
    "termine": [{"von": d(r["von"]).isoformat(), "bis": d(r["bis"] or r["von"]).isoformat(), "titel": r["Titel"]} for r in TERMINE],
    "suche": [{"t": t, "s": sub, "u": u, "k": k} for t, sub, u, k in SUCHE],
    "glossar": GLOSSAR,
    "faq": FAQ_ALLE,
}
with open(os.path.join(W, "js/daten.js"), "w", encoding="utf-8") as f:
    f.write("/* Automatisch erzeugt aus daten/*.csv – nicht von Hand ändern, sondern build.py ausführen. */\n")
    f.write("window.KITA = " + json.dumps(kita, ensure_ascii=False, indent=1) + ";\n")

# ---------- Kalenderdateien (.ics) ----------
def ics(events, name, slug):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    def esc(t): return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kinderhort Grombuehl//Webseite//DE", "CALSCALE:GREGORIAN",
           "METHOD:PUBLISH", f"X-WR-CALNAME:{esc(name)}", "X-WR-TIMEZONE:Europe/Berlin"]
    for i, (start, end, title, desc) in enumerate(events):
        out += ["BEGIN:VEVENT", f"UID:{slug}-{start:%Y%m%d}-{i}@kinderhort-grombuehl.de", f"DTSTAMP:{stamp}",
                f"DTSTART;VALUE=DATE:{start:%Y%m%d}", f"DTEND;VALUE=DATE:{end + dt.timedelta(days=1):%Y%m%d}",
                f"SUMMARY:{esc(title)}", f"DESCRIPTION:{esc(desc)}", "TRANSP:TRANSPARENT", "END:VEVENT"]
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"

with open(os.path.join(W, "downloads/schliesstage.ics"), "w", encoding="utf-8", newline="") as f:
    f.write(ics([(d(r["erster Schließtag"]), d(r["letzter Schließtag"]), f"Kita geschlossen ({r['Anlass']})",
                  f"Kinderkrippe, Kindergarten und Kinderhort geschlossen. Wieder geöffnet am {r['wieder geöffnet']}.") for r in SCHLIESSTAGE],
                "Kinderhort Grombühl – Schließtage", "schliesstag"))
with open(os.path.join(W, "downloads/termine.ics"), "w", encoding="utf-8", newline="") as f:
    f.write(ics([(d(r["von"]), d(r["bis"] or r["von"]), r["Titel"], r["Beschreibung"]) for r in TERMINE],
                "Kinderhort Grombühl – Termine", "termin"))

# ---------- SEO: sitemap.xml, robots.txt ----------
today = dt.date.today().isoformat()
with open(os.path.join(W, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for pg in PAGES_WRITTEN:
        f.write(f"  <url><loc>{SITE}{'' if pg == 'index.html' else pg}</loc><lastmod>{today}</lastmod></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(W, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nDisallow: /entwurf/\nDisallow: /daten/\n\nSitemap: {SITE}sitemap.xml\n")

# ---------- Service Worker: schnelle Wiederbesuche, auch bei schlechtem Netz ----------
SW = '''/* Automatisch erzeugt von build.py */
const CACHE = "kita-__VERSION__";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(
  caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  const fresh = () => fetch(req).then((res) => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); }
    return res;
  });
  if (req.mode === "navigate") {
    /* Seiten: immer aktuell, Kopie nur als Rückfall ohne Netz */
    e.respondWith(fresh().catch(() => caches.match(req).then((r) => r || caches.match("index.html"))));
  } else {
    /* Bilder, Schriften, CSS, JS: sofort aus dem Speicher, im Hintergrund auffrischen */
    e.respondWith(caches.match(req).then((hit) => { const net = fresh().catch(() => hit); return hit || net; }));
  }
});
'''
with open(os.path.join(W, "sw.js"), "w", encoding="utf-8") as f:
    f.write(SW.replace("__VERSION__", dt.datetime.now().strftime("%Y%m%d%H%M")))

# Favicon
with open(os.path.join(W, "img/favicon.svg"), "w", encoding="utf-8") as f:
    f.write(BRAND_MARK.replace('class="brand-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ''))
print("ok")
