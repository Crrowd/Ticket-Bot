"""Live-Vorschau: fünf Varianten für das Öffnen und Schließen des Handy-Menüs (plus „Heute“)."""
import os, re
D = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(D + "leiste-live.html", encoding="utf-8").read()
# Bausteine aus der Leisten-Vorschau übernehmen (gleiche Optik, gleiche Fotos)
inhalt = src[src.index('<div class="inhalt">'):src.index('</div>\n  </div></div>\n</figure>')]
bar = re.search(r'<header class="bar">.*?</header>', src, re.S).group(0)
bar = bar.replace('<span class="btn">', '<button class="btn menu-auf" type="button" aria-label="Menü öffnen">', 1) if False else bar
# Menü-Knopf anklickbar machen
bar = re.sub(r'<span class="btn">(<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>)</span>', r'<button class="btn menu-auf" type="button" aria-label="Menü öffnen">\1</button>', bar)
css_alt = src[src.index("<style>") + 7:src.index("</style>")]
css_alt = css_alt.split("/* Heute */")[0] + css_alt[css_alt.index("/* ---------- Seiteninhalt im Handy ---------- */"):]

PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'
X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
MENUE = f'''<nav class="menue" aria-label="Menü" hidden><button class="btn menu-zu" type="button" aria-label="Menü schließen">{X}</button>
<ul><li><a>Startseite <i>→</i></a></li><li><a>Bereiche <i>↓</i></a></li><li><a>Aktuelles <i>→</i></a></li><li><a>Downloads <i>→</i></a></li><li class="cta"><a>Kontakt</a></li>
<li class="extra"><b>Wir sind für Sie da</b><a class="q"><span class="kic">{PHONE}</span><span><b>0931 2789892 0</b><small>Anrufen, Mo–Fr ab 6:45 Uhr</small></span></a><a class="q"><span class="kic">{MAIL}</span><span><b>E-Mail schreiben</b><small>kinderhort.grombuehl@t-online.de</small></span></a></li></ul></nav>'''

def phone(v, name, text):
    return f'''<figure class="phone" data-v="{v}" id="p-{v}">
  <figcaption><b>{name}</b><span>{text}</span></figcaption>
  <div class="frame"><div class="screen" tabindex="0" aria-label="Handy-Vorschau {name}">{bar}{inhalt}</div></div><div class="schirm">{MENUE}</div></div>
</figure>'''

VARIANTEN = [
    ("heute", "Heute · Kreis aus dem Knopf", "Öffnet sich als Kreis aus dem Menü-Knopf oben rechts"),
    ("a", "A · Blatt von oben", "Gleitet wie ein Blatt von oben herein und wieder hinaus"),
    ("b", "B · Von der Seite", "Schiebt sich von rechts herein, die Seite dahinter wird leicht abgedunkelt"),
    ("c", "C · Weich aufblühen", "Blendet ein und wächst dabei ganz leicht aus der Ecke des Knopfs"),
    ("d", "D · Aus der Leiste wachsen", "Die Leiste selbst dehnt sich zum ganzen Menü aus"),
    ("e", "E · Vorhang", "Fällt wie ein Vorhang mit runder Unterkante herunter"),
]
PHONES = "".join(phone(*v) for v in VARIANTEN)
TABS = "".join(f'<button type="button" data-z="{v}" aria-pressed="{"true" if i == 0 else "false"}">{n.split(" · ")[0]}</button>' for i, (v, n, _) in enumerate(VARIANTEN))

CSS = css_alt + '''
[hidden] { display: none !important; }
.phones { grid-template-columns: repeat(3, minmax(0, 340px)); justify-content: center; gap: 28px 32px; }
@media (max-width: 1100px) { .phones { grid-template-columns: repeat(2, minmax(0, 340px)); } }
.frame { position: relative; }
.schirm { position: absolute; inset: 10px; z-index: 20; border-radius: 32px; overflow: hidden; pointer-events: none; }
.schirm > * { pointer-events: auto; }
.menu-auf, .menu-zu { border: 0; cursor: pointer; padding: 0; }
.menu-auf:focus-visible, .menu-zu:focus-visible { outline: 3px solid #C9A49E; outline-offset: 2px; }
/* das Menü liegt über dem Bildschirm des Handys */
.menue { position: absolute; inset: 0; z-index: 2; background: #A8C5C0; overflow: hidden; padding: 74px 14px 16px; color: #1E3B44; }
.menue .menu-zu { position: absolute; top: 16px; right: 16px; background: #F3F8F7; box-shadow: 0 6px 18px -10px rgba(30,59,68,.5); }
.menue ul { list-style: none; margin: 0; padding: 0; display: grid; }
.menue li > a { display: flex; justify-content: space-between; align-items: center; min-height: 52px; padding: 0 8px; border-bottom: 1px solid rgba(30,59,68,.14); font-weight: 600; font-size: 1.2rem; letter-spacing: -.02em; }
.menue li > a i { font-style: normal; opacity: .45; }
.menue .cta a { margin-top: 12px; justify-content: center; border: 0; border-radius: 14px; background: #1E3B44; color: #F3F8F7; font-size: 1rem; min-height: 48px; }
.menue .extra { margin-top: 14px; padding: 12px; border-radius: 22px; background: #F3F8F7; display: grid; gap: 8px; }
.menue .extra > b { font-size: .8rem; color: #4A6670; font-weight: 600; }
.menue .q { display: flex; gap: 10px; align-items: center; padding: 8px; border-radius: 14px; background: rgba(30,59,68,.06); font-size: .82rem; }
.menue .q b { display: block; font-size: .9rem; } .menue .q small { color: #4A6670; overflow-wrap: anywhere; }
.kic { width: 38px; height: 38px; flex: none; display: grid; place-items: center; border-radius: 10px; background: #D4B5B0; }
.kic svg, .menue .menu-zu svg { width: 18px; height: 18px; fill: none; stroke: #1E3B44; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.dimm { position: absolute; inset: 0; z-index: 1; background: rgba(14,30,35,.35); pointer-events: none; }
'''

JS = r'''
(function () {
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var OUT = "cubic-bezier(.23,1,.32,1)", IO = "cubic-bezier(.77,0,.175,1)", DRAWER = "cubic-bezier(.32,.72,0,1)";
  var phones = Array.prototype.slice.call(document.querySelectorAll(".phone"));
  phones[0].classList.add("zeigen");
  /* je Variante: Öffnen und Schließen als Web-Animation (läuft auch in Safari) */
  var V = {
    heute: { auf: [{ clipPath: "circle(0px at calc(100% - 37px) 37px)" }, { clipPath: "circle(150% at calc(100% - 37px) 37px)" }], zu: null, msAuf: 500, msZu: 400, eAuf: OUT, eZu: IO },
    a: { auf: [{ translate: "0 -100%" }, { translate: "0 0" }], zu: null, msAuf: 450, msZu: 300, eAuf: DRAWER, eZu: "cubic-bezier(.4,0,1,1)" },
    b: { auf: [{ translate: "100% 0" }, { translate: "0 0" }], zu: null, msAuf: 420, msZu: 280, eAuf: DRAWER, eZu: "cubic-bezier(.4,0,1,1)", dimm: true },
    c: { auf: [{ opacity: 0, scale: .96, transformOrigin: "calc(100% - 37px) 37px" }, { opacity: 1, scale: 1, transformOrigin: "calc(100% - 37px) 37px" }], zu: null, msAuf: 260, msZu: 180, eAuf: OUT, eZu: "ease-in" },
    d: { auf: [{ clipPath: "inset(0px 0px calc(100% - 64px) 0px round 18px)" }, { clipPath: "inset(0px 0px 0px 0px round 32px)" }], zu: null, msAuf: 460, msZu: 340, eAuf: IO, eZu: IO, inhaltSpaeter: true },
    e: { auf: [{ clipPath: "inset(0 0 100% 0 round 0 0 48px 48px)" }, { clipPath: "inset(0 0 0% 0 round 0 0 0px 0px)" }], zu: null, msAuf: 460, msZu: 320, eAuf: "cubic-bezier(.45,0,.2,1)", eZu: "cubic-bezier(.55,0,.75,.3)" }
  };
  phones.forEach(function (ph) {
    var v = V[ph.getAttribute("data-v")], frame = ph.querySelector(".frame"), m = ph.querySelector(".menue"), auf = ph.querySelector(".menu-auf"), zu = ph.querySelector(".menu-zu"), dimm = null, lauf = null, offen = false;
    function items() { return Array.prototype.slice.call(m.querySelectorAll("ul > li")); }
    function oeffne() {
      if (offen) return; offen = true; if (lauf) lauf.cancel();
      m.hidden = false;
      if (v.dimm) { dimm = document.createElement("div"); dimm.className = "dimm"; m.parentNode.insertBefore(dimm, m); if (!reduced) dimm.animate([{ opacity: 0 }, { opacity: 1 }], { duration: v.msAuf, easing: "ease-out" }); }
      if (reduced) { m.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 150 }); return; }
      lauf = m.animate(v.auf, { duration: v.msAuf, easing: v.eAuf });
      items().forEach(function (li, i) { li.animate([{ opacity: 0, translate: "0 10px" }, { opacity: 1, translate: "0 0" }], { duration: 320, delay: (v.inhaltSpaeter ? 180 : 90) + i * 35, easing: OUT, fill: "backwards" }); });
      zu.animate([{ opacity: 0, rotate: "-90deg" }, { opacity: 1, rotate: "0deg" }], { duration: 300, delay: 120, easing: OUT, fill: "backwards" });
      zu.focus({ preventScroll: true });
    }
    function schliesse() {
      if (!offen) return; offen = false; if (lauf) lauf.cancel();
      var fertig = function () { m.hidden = true; if (dimm) { dimm.remove(); dimm = null; } auf.focus({ preventScroll: true }); };
      if (reduced) { m.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 120 }).onfinish = fertig; return; }
      var keys = v.auf.slice().reverse();
      items().forEach(function (li) { li.animate([{ opacity: 1 }, { opacity: 0 }], { duration: Math.min(160, v.msZu), easing: "ease-in", fill: "forwards" }); });
      if (dimm) dimm.animate([{ opacity: 1 }, { opacity: 0 }], { duration: v.msZu, fill: "forwards" });
      lauf = m.animate(keys, { duration: v.msZu, easing: v.eZu, fill: "forwards" });
      lauf.onfinish = function () { items().forEach(function (li) { li.getAnimations().forEach(function (a) { a.cancel(); }); }); lauf.cancel(); lauf = null; fertig(); };
    }
    ph.oeffne = oeffne; ph.schliesse = schliesse;
    auf.addEventListener("click", oeffne); zu.addEventListener("click", schliesse);
    m.addEventListener("keydown", function (e) { if (e.key === "Escape") schliesse(); });
  });
  function warte(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  var laeuft = false;
  document.getElementById("vor").addEventListener("click", function () {
    if (laeuft) return; laeuft = true; var b = this; b.textContent = "Läuft …";
    var sicht = phones.filter(function (p) { return p.getClientRects().length && getComputedStyle(p).display !== "none"; });
    sicht.forEach(function (p) { p.schliesse(); });
    warte(500).then(function () { sicht.forEach(function (p) { p.oeffne(); }); return warte(1600); })
      .then(function () { sicht.forEach(function (p) { p.schliesse(); }); return warte(900); })
      .then(function () { sicht.forEach(function (p) { p.oeffne(); }); return warte(1400); })
      .then(function () { sicht.forEach(function (p) { p.schliesse(); }); return warte(600); })
      .then(function () { laeuft = false; b.textContent = "Automatisch vorführen"; });
  });
  Array.prototype.forEach.call(document.querySelectorAll(".tabs button"), function (t, i, all) {
    t.addEventListener("click", function () {
      Array.prototype.forEach.call(all, function (x) { x.setAttribute("aria-pressed", x === t); });
      phones.forEach(function (p) { p.classList.toggle("zeigen", p.getAttribute("data-v") === t.getAttribute("data-z")); });
    });
  });
})();
'''

html = f'''<title>Menü öffnen und schließen</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<style>{CSS}</style>
<main class="wrap">
  <header>
    <h1>Handy-Menü öffnen und schließen</h1>
    <p class="lead">Tippen Sie in einem Handy oben rechts auf das Menü-Symbol und schließen Sie es mit dem Kreuz wieder. Oder drücken Sie „Automatisch vorführen“: Dann öffnen und schließen alle gleichzeitig.</p>
  </header>
  <div class="ctl"><button class="go" type="button" id="vor">Automatisch vorführen</button></div>
  <div class="tabs" role="group" aria-label="Variante wählen">{TABS}</div>
  <div class="phones">{PHONES}</div>
</main>
<script>{JS}</script>
'''
open(D + "menu-live.html", "w", encoding="utf-8").write(html)
print("ok", len(html) // 1024, "KB")
