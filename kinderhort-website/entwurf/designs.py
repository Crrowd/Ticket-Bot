# Erzeugt 5 helle Farb-Entwürfe (CSS-Varianten) aus css/style.css.
# Aufruf:  python3 entwurf/designs.py   -> entwurf/designs/design-N.css
# Einen Entwurf übernehmen: Datei nach css/style.css kopieren und build.py
# mit denselben Farbwerten anpassen (siehe BASE unten).
import os

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Farbwerte des aktuellen Stylesheets (Entwurf 9) – css/style.css enthält zusätzlich LIGHT + DARK_CARDS
BASE = dict(bg="#A8C5C0", alt="#B6D0CB", paper="#2D6A6A", line="#C9DCD8", ink="#1E3B44", soft="#2C4A52",
            dark="#142A31", acc="#D4B5B0", accsoft="#F1E5E3", hover="#C9A49E", even="#F3F8F7")

DESIGNS = [
    dict(n=1, name="Salbei & Pfirsich", text="Ruhig, natürlich, warm",
         bg="#EEF4EC", alt="#E1EBDE", paper="#FFFFFF", line="#D3E0CF", ink="#2F3E36", soft="#5A6B61",
         dark="#22302A", acc="#F4A688", accsoft="#FDE6DC", hover="#EE9272", even="#F6F9F5"),
    dict(n=2, name="Vanille & Rosé", text="Freundlich, herzlich, verspielt",
         bg="#FFF8EC", alt="#FBEEDB", paper="#FFFFFF", line="#F1E2CB", ink="#3A2E4F", soft="#655A78",
         dark="#2A2140", acc="#F28BA0", accsoft="#FDE1E7", hover="#EC7189", even="#FFFBF4"),
    dict(n=3, name="Himmel & Sonne", text="Frisch, klar, sonnig",
         bg="#EAF4FB", alt="#DCECF7", paper="#FFFFFF", line="#CBE0EF", ink="#1F3A5F", soft="#4D6585",
         dark="#162B47", acc="#FFC24B", accsoft="#FFEDC7", hover="#F5B02C", even="#F4F9FD"),
    dict(n=4, name="Lavendel & Minze", text="Sanft, modern, ausgeglichen",
         bg="#F3F0FA", alt="#E8E3F5", paper="#FFFFFF", line="#DCD5EE", ink="#2E2A47", soft="#5D5875",
         dark="#211E36", acc="#5CC8A8", accsoft="#D7F2E9", hover="#45B993", even="#F9F7FD"),
    dict(n=5, name="Sand & Terrakotta", text="Geborgen, erdig, gemütlich",
         bg="#FAF4EA", alt="#F2E8D8", paper="#FFFFFF", line="#E8DBC6", ink="#3B2F2A", soft="#6A5A52",
         dark="#2B221E", acc="#E8956B", accsoft="#FBE2D4", hover="#E07F51", even="#FDF9F3"),
    dict(n=6, name="Lavendelgrau & Honig", text="Hintergrund aus dem Porträt der Einrichtungsleitung",
         bg="#9B98A8", alt="#A7A4B3", paper="#FFFFFF", line="#C9C6D3", ink="#24203A", soft="#34304A",
         dark="#1A172B", acc="#F3C969", accsoft="#FBEBC4", hover="#EDB940", even="#F6F5F9"),
    dict(n=7, name="Salbeitürkis & Zitrone", text="Hintergrund aus dem Begrüßungsbereich der bisherigen Seite",
         bg="#A8C5C0", alt="#B6D0CB", paper="#FFFFFF", line="#C9DCD8", ink="#1E3B44", soft="#2C4A52",
         dark="#142A31", acc="#F4E04D", accsoft="#FBF3BE", hover="#EDD52B", even="#F3F8F7"),
    dict(n=8, name="Salbeitürkis & Grau-Rosé", text="Wie Entwurf 7, Akzent in gedecktem Rosé",
         bg="#A8C5C0", alt="#B6D0CB", paper="#FFFFFF", line="#C9DCD8", ink="#1E3B44", soft="#2C4A52",
         dark="#142A31", acc="#D4B5B0", accsoft="#F1E5E3", hover="#C9A49E", even="#F3F8F7"),
    dict(n=9, name="Salbeitürkis, Grau-Rosé & dunkles Türkis", text="Wie Entwurf 8, Karten in dunklem Türkis statt Weiß",
         bg="#A8C5C0", alt="#B6D0CB", paper="#2D6A6A", line="#C9DCD8", ink="#1E3B44", soft="#2C4A52",
         dark="#142A31", acc="#D4B5B0", accsoft="#F1E5E3", hover="#C9A49E", even="#F3F8F7", extra="DARK_CARDS"),
]

# Dunkle Karten: helle Schrift innerhalb aller Flächen in --paper
DARK_CARDS = """
/* Entwurf: dunkle Karten mit heller Schrift */
.info-card, .room, .tour-item, .timeline .tl-body, .faq details, .table-wrap, .note-card, .event, .dl-group,
.phone-card, .address-card, .prose, .area-card, .pill-list > div, .features li, .stat, .group-chip,
.subnav a, .hero-tags li, .dropdown, .main-nav .dropdown a, .status-card, .quick-card {
  --ink: #F3FAF8; --ink-soft: #CFE3E0; --green: #F3FAF8; --green-dark: #FFFFFF; --line: rgba(255,255,255,.16);
  color: var(--ink);
}
.features li { box-shadow: none; }
.subnav a { border-color: transparent; }
.subnav a:hover, .main-nav .dropdown a:hover { --ink: #1E3B44; }
.info-card .icon, .faq summary::after, .dl-link .ficon, .event .date, .area-card .age,
table.plan thead th, table.plan tfoot td { color: #1E3B44; }
.timeline li::before { border-color: #1E3B44; }
.dl-link { background: rgba(255,255,255,.1); }
.dl-link:hover { background: rgba(255,255,255,.2); }
table.plan tbody tr:nth-child(even) { background: rgba(255,255,255,.06); }
table.plan th, table.plan td { border-color: rgba(255,255,255,.14); }
.area-card .age { background: #fff; }
.room .txt p, .area-card .body p { color: var(--ink-soft); }
/* Lange Texte hell hinterlegt (besser lesbar) */
.prose, .faq details > div {
  --ink: #1E3B44; --ink-soft: #2C4A52; --green: #1E3B44; --green-dark: #142A31;
  background: #F3F8F7; color: var(--ink);
}
.faq details > div { padding-top: 18px; border-top: 1px solid rgba(255,255,255,.2); }
.faq details > div a { color: #1E3B44; }
.status-card .status-sub, .quick-card span span { color: var(--ink-soft); }
.quick-icon { color: #1E3B44; }
"""

def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def recolor(text, d):
    for k, v in BASE.items():
        text = text.replace(v, d[k]).replace(v.lower(), d[k]).replace("%23" + v[1:], "%23" + d[k][1:])
    br, d_ = rgb(BASE["bg"]), rgb(d["bg"])
    text = text.replace(f"rgba({br[0]}, {br[1]}, {br[2]}, .92)", f"rgba({d_[0]}, {d_[1]}, {d_[2]}, .92)")
    bi, di = rgb(BASE["ink"]), rgb(d["ink"])
    text = text.replace(f"rgba({bi[0]}, {bi[1]}, {bi[2]},", f"rgba({di[0]}, {di[1]}, {di[2]},")
    text = text.replace(f"rgba({bi[0]},{bi[1]},{bi[2]},", f"rgba({di[0]},{di[1]},{di[2]},")
    return text

# Hellere Variante der dunklen Abschnitte (statt Vollflächen in Schriftfarbe)
LIGHT = """
/* Entwurf: helle Highlight-Abschnitte */
.section.green { background: var(--accent-soft); color: var(--ink); }
.section.green h2, .section.green h3 { color: var(--ink); }
.section.green .section-head p { color: var(--ink-soft); }
.stat { background: var(--paper); border: 0; box-shadow: var(--shadow); }
.stat b { color: var(--ink); box-shadow: inset 0 -.3em 0 var(--sun); display: inline-block; }
.stat span { color: var(--ink-soft); display: block; margin-top: 6px; }
.section.green .teaser h3 { color: #fff; }
.page-hero.simple .page-hero-card { background: var(--accent-soft); color: var(--ink); }
.page-hero.simple .page-hero-content h1 { color: var(--ink); }
.address-card { background: var(--paper); color: var(--ink); border-top: 8px solid var(--sun); }
.address-card h2, .address-card h3, .address-card a { color: var(--ink); }
table.plan thead th { background: var(--sun); color: var(--ink); }
"""

if __name__ == "__main__":
    css = open(os.path.join(W, "css/style.css"), encoding="utf-8").read().replace(DARK_CARDS, "").replace(LIGHT, "")
    os.makedirs(os.path.join(W, "entwurf/designs"), exist_ok=True)
    for d in DESIGNS:
        out = os.path.join(W, f"entwurf/designs/design-{d['n']}.css")
        open(out, "w", encoding="utf-8").write(f"/* Entwurf {d['n']}: {d['name']} – Hintergrund {d['bg']}, Schrift {d['ink']}, Akzent {d['acc']} */\n" + recolor(css, d) + LIGHT + (globals()[d["extra"]] if d.get("extra") else ""))
        print(out)
