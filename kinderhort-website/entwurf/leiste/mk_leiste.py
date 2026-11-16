"""Live-Vorschau: vier Varianten, wie die obere Leiste beim Scrollen verschwindet."""
import base64, os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
IMG = os.path.join(D, "../../img/")
def b64(n): return "data:image/webp;base64," + base64.b64encode(open(IMG + n + "-800.webp", "rb").read()).decode()
FOTO = {k: b64(k) for k in ["p2160110", "lesecke", "turnraum"]}

MARK = ('<svg class="mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#1E3B44"/>'
        '<path d="M6 17 Q24 25 42 17" fill="none" stroke="#fff" stroke-width="1.6"/>'
        '<path d="M9 18.3 L15 21 L11.2 29Z" fill="#D4B5B0"/><path d="M16.5 21.6 L22.5 23 L19 31.5Z" fill="#A8C5C0"/>'
        '<path d="M24.5 23 L30.5 21.8 L28.6 31.4Z" fill="#D4B5B0"/><path d="M32 21.3 L38.5 18.4 L37.6 28.3Z" fill="#A8C5C0"/></svg>')
LUPE = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.8-3.8"/></svg>'
MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

INHALT = f'''
<div class="hero"><img src="{FOTO["p2160110"]}" alt=""><div class="hero-t"><span class="kick">Bereich</span><h3>Die Kinderkrippe</h3><p>Für Kinder von 11 Monaten bis 3 Jahren – in der Sonnen- und Sternengruppe.</p></div></div>
<div class="chips"><span class="on">Überblick</span><span>Räume</span><span>Tagesablauf</span><span>Fragen</span></div>
<section><span class="kick">Auf einen Blick</span><h4>Das Wichtigste in Kürze</h4>
<ul><li>Geöffnet Mo–Fr ab 6:45 Uhr</li><li>Zwei Gruppen mit je 12 Kindern</li><li>Frisch gekochtes Mittagessen</li><li>Eingewöhnung in kleinen Schritten</li></ul></section>
<section><span class="kick">Räumlichkeiten</span><h4>Viel Platz zum Entdecken</h4><img src="{FOTO["lesecke"]}" alt=""><p>Die Lesecke lädt zum Vorlesen und Ausruhen ein. Jede Gruppe hat einen eigenen Schlafraum.</p></section>
<section><span class="kick">Tagesablauf</span><h4>Ein Tag bei uns</h4>
<ol><li><b>6:45</b> Ankommen und Frühstück</li><li><b>9:00</b> Morgenkreis</li><li><b>11:15</b> Mittagessen</li><li><b>12:00</b> Schlafen und Ruhen</li><li><b>14:30</b> Brotzeit und Garten</li></ol></section>
<section><span class="kick">Bewegung</span><h4>Der Turnraum</h4><img src="{FOTO["turnraum"]}" alt=""><p>Klettern, rutschen, toben – auch wenn es draußen regnet.</p></section>
<section><span class="kick">Fragen</span><h4>Häufige Fragen</h4><p class="q">Wie läuft die Eingewöhnung?</p><p class="q">Was braucht mein Kind?</p><p class="q">Wann ist geschlossen?</p></section>
<div class="end">Ende der Seite</div>
'''

def phone(v, name, text):
    griff = '<span class="griff" aria-hidden="true"></span>' if v == "c" else ""
    return f'''<figure class="phone" data-v="{v}" id="p-{v}">
  <figcaption><b>{name}</b><span>{text}</span></figcaption>
  <div class="frame"><div class="screen" tabindex="0" aria-label="Handy-Vorschau {name}, zum Scrollen">
    <header class="bar">{griff}<div class="pill"><span class="brand">{MARK}<span class="name">Kinderkrippe</span></span><span class="tools"><span class="btn lupe">{LUPE}</span><span class="btn">{MENU}</span></span></div></header>
    <div class="inhalt">{INHALT}</div>
  </div></div>
</figure>'''

PHONES = "".join([
    phone("heute", "Heute", "Leiste rutscht ganz nach oben weg"),
    phone("a", "A · Weich auflösen", "Gleitet ein Stück hoch, wird unscharf und blasser"),
    phone("b", "B · Mini-Pille", "Name und Lupe verschwinden, Logo und Menü bleiben"),
    phone("c", "C · Folgt dem Finger", "Wandert genau mit dem Scrollen, kleiner Griff bleibt"),
])

html = f'''<title>Leiste beim Scrollen</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<style>
/* Layout: oben kurze Erklärung und Steuerung, darunter vier Handys nebeneinander (am Handy eins mit Reitern) */
:root {{
  --bg: #E8F0EE; --fg: #1E3B44; --soft: #4A6670; --line: rgba(30,59,68,.14); --chip: rgba(30,59,68,.08); --accent: #D4B5B0;
  --font: "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif;
  /* Farben der Webseite im Handy – in beiden Themen gleich, wie auf der echten Seite */
  --s-bg: #A8C5C0; --s-paper: #F3F8F7; --s-ink: #1E3B44; --s-card: #2D6A6A; --s-rose: #D4B5B0;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #0F2128; --fg: #E3EEEC; --soft: #A9C1BE; --line: rgba(227,238,236,.16); --chip: rgba(227,238,236,.1); color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg: #0F2128; --fg: #E3EEEC; --soft: #A9C1BE; --line: rgba(227,238,236,.16); --chip: rgba(227,238,236,.1); color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font: 16px/1.55 var(--font); }}
.wrap {{ max-width: 1480px; margin: 0 auto; padding-block: 28px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 22px; }}
h1 {{ margin: 0; font-size: clamp(1.6rem, 3vw, 2.2rem); line-height: 1.15; text-wrap: balance; letter-spacing: -.02em; }}
.lead {{ margin: 6px 0 0; color: var(--soft); max-width: 44em; }}
.ctl {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
.ctl button {{ font: 600 .95rem var(--font); min-height: 44px; padding: 0 18px; border-radius: 12px; border: 1px solid var(--line); background: transparent; color: var(--fg); cursor: pointer; }}
.ctl .go {{ background: var(--accent); color: #1E3B44; border-color: transparent; }}
.ctl button:focus-visible, .tabs button:focus-visible, .screen:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}
.tabs {{ display: none; gap: 4px; padding: 4px; border-radius: 12px; background: var(--chip); justify-self: start; max-width: 100%; overflow-x: auto; }}
.wrap > * {{ min-width: 0; }}
.tabs button {{ font: 600 .9rem var(--font); min-height: 40px; padding: 0 14px; border: 0; border-radius: 8px; background: none; color: var(--fg); cursor: pointer; white-space: nowrap; }}
.tabs button[aria-pressed="true"] {{ background: var(--fg); color: var(--bg); }}
.phones {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }}
.phone {{ margin: 0; display: grid; gap: 10px; justify-items: center; min-width: 0; }}
.phone figcaption {{ display: grid; text-align: center; gap: 2px; min-height: 4.6em; align-content: start; }}
.phone figcaption span {{ color: var(--soft); font-size: .88rem; }}
.frame {{ box-sizing: border-box; width: min(100%, 340px); aspect-ratio: 340 / 690; border-radius: 42px; padding: 10px; background: #0E1A1F; box-shadow: 0 24px 50px -28px rgba(0,0,0,.6); }}
.screen {{ position: relative; height: 100%; overflow-y: auto; overscroll-behavior: contain; border-radius: 32px; background: var(--s-bg); color: var(--s-ink); scrollbar-width: none; }}
.screen::-webkit-scrollbar {{ display: none; }}

/* ---------- die Leiste im Handy (nachgebaut wie auf der Webseite) ---------- */
.bar {{ position: sticky; top: 0; z-index: 5; padding: 10px 10px 0; pointer-events: none; }}
.pill {{ pointer-events: auto; position: relative; display: flex; align-items: center; justify-content: space-between; gap: 10px; min-height: 54px; padding: 6px 6px 6px 10px; border-radius: 18px;
  background: rgba(243,248,247,.62); backdrop-filter: blur(16px) saturate(160%); -webkit-backdrop-filter: blur(16px) saturate(160%); border: 1px solid rgba(255,255,255,.6); box-shadow: 0 10px 30px -18px rgba(30,59,68,.5); margin-left: auto; max-width: 100%; }}
.brand {{ display: flex; align-items: center; gap: 10px; min-width: 0; }}
.mark {{ width: 36px; height: 36px; flex: none; }}
.name {{ font-weight: 600; font-size: .98rem; white-space: nowrap; overflow: hidden; }}
.tools {{ display: flex; gap: 6px; flex: none; }}
.btn {{ width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center; background: rgba(30,59,68,.08); overflow: hidden; }}
.btn svg {{ width: 20px; height: 20px; fill: none; stroke: #1E3B44; stroke-width: 1.8; stroke-linecap: round; }}

/* Heute */
.phone[data-v="heute"] .bar {{ transition: translate .25s cubic-bezier(.23,1,.32,1); }}
.phone[data-v="heute"] .bar.hide {{ translate: 0 calc(-100% - 8px); transition-duration: .2s; }}
/* A: weich auflösen */
.phone[data-v="a"] .bar {{ transition: translate .45s cubic-bezier(.23,1,.32,1), opacity .35s ease, filter .4s ease, scale .45s cubic-bezier(.23,1,.32,1); }}
.phone[data-v="a"] .bar.hide {{ translate: 0 -38%; opacity: 0; filter: blur(8px); scale: .95; pointer-events: none; }}
/* B: zur Mini-Pille */
.phone[data-v="b"] .pill {{ transition: max-width .45s cubic-bezier(.23,1,.32,1), padding .45s cubic-bezier(.23,1,.32,1), min-height .45s cubic-bezier(.23,1,.32,1); }}
.phone[data-v="b"] .name, .phone[data-v="b"] .lupe {{ transition: max-width .4s cubic-bezier(.23,1,.32,1), opacity .25s ease, width .4s cubic-bezier(.23,1,.32,1), margin .4s; max-width: 200px; }}
.phone[data-v="b"] .bar.hide .pill {{ max-width: 112px; min-height: 50px; padding: 4px 4px 4px 8px; }}
.phone[data-v="b"] .bar.hide .name {{ max-width: 0; opacity: 0; }}
.phone[data-v="b"] .bar.hide .lupe {{ width: 0; opacity: 0; margin-right: -6px; }}
/* C: folgt dem Finger */
.phone[data-v="c"] .bar {{ will-change: translate; }}
.griff {{ position: absolute; left: 50%; bottom: -12px; width: 46px; height: 5px; border-radius: 3px; translate: -50% 0; background: rgba(30,59,68,.5); opacity: var(--g, 0); }}

@media (prefers-reduced-motion: reduce) {{ .bar, .pill, .name, .lupe {{ transition-duration: .01s !important; }} }}

/* ---------- Seiteninhalt im Handy ---------- */
.inhalt {{ padding: 0 12px 24px; margin-top: -64px; display: grid; gap: 12px; font-size: .9rem; }}
.hero {{ position: relative; margin: 0 -12px; }}
.hero img {{ width: 100%; height: 300px; object-fit: cover; display: block; }}
.hero::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(14,30,35,0) 30%, rgba(14,30,35,.75)); }}
.hero-t {{ position: absolute; left: 14px; right: 14px; bottom: 14px; z-index: 1; color: #F3F8F7; }}
.hero-t h3 {{ margin: 4px 0; font-size: 1.5rem; line-height: 1.1; }}
.hero-t p {{ margin: 0; font-size: .85rem; opacity: .9; }}
.kick {{ display: inline-block; font-size: .7rem; font-weight: 700; padding: 2px 9px; border-radius: 999px; background: var(--s-rose); color: #1E3B44; }}
.chips {{ display: flex; gap: 6px; overflow: hidden; padding: 4px; border-radius: 14px; background: rgba(243,248,247,.7); }}
.chips span {{ padding: 6px 10px; border-radius: 10px; font-weight: 600; font-size: .8rem; white-space: nowrap; }}
.chips .on {{ background: var(--s-rose); }}
section {{ background: var(--s-card); color: #F3F8F7; border-radius: 18px; padding: 14px; display: grid; gap: 8px; }}
section h4 {{ margin: 0; font-size: 1.08rem; }}
section p, section ul, section ol {{ margin: 0; }}
section ul, section ol {{ padding-left: 18px; display: grid; gap: 4px; }}
section img {{ width: 100%; height: 150px; object-fit: cover; border-radius: 12px; display: block; }}
section .q {{ background: rgba(243,248,247,.12); border-radius: 10px; padding: 8px 10px; }}
.end {{ text-align: center; color: rgba(30,59,68,.6); font-size: .8rem; padding: 12px 0 4px; }}

@media (max-width: 1100px) {{ .phones {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
@media (max-width: 720px) {{
  .tabs {{ display: flex; flex-wrap: wrap; }}
  .phones {{ grid-template-columns: minmax(0, 1fr); }}
  .phone:not(.zeigen) {{ display: none; }}
  .frame {{ width: min(100%, 360px); }}
}}
</style>
<main class="wrap">
  <header>
    <h1>Obere Leiste beim Scrollen</h1>
    <p class="lead">Scrollen Sie in einem der Handys nach unten und wieder ein Stück nach oben. Oder drücken Sie „Automatisch vorführen“: Dann scrollen alle Handys gleichzeitig.</p>
  </header>
  <div class="ctl">
    <button class="go" type="button" id="vor">Automatisch vorführen</button>
    <button type="button" id="hoch">Alle nach oben</button>
  </div>
  <div class="tabs" role="group" aria-label="Variante wählen">
    <button type="button" data-z="heute" aria-pressed="true">Heute</button><button type="button" data-z="a" aria-pressed="false">A · Auflösen</button><button type="button" data-z="b" aria-pressed="false">B · Mini-Pille</button><button type="button" data-z="c" aria-pressed="false">C · Mit dem Finger</button>
  </div>
  <div class="phones">{PHONES}</div>
</main>
<script>
(function () {{
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var phones = Array.prototype.slice.call(document.querySelectorAll(".phone"));
  phones[0].classList.add("zeigen");

  phones.forEach(function (ph) {{
    var v = ph.getAttribute("data-v"), sc = ph.querySelector(".screen"), bar = ph.querySelector(".bar"), griff = ph.querySelector(".griff");
    var last = 0, travel = 0, off = 0;
    sc.addEventListener("scroll", function () {{
      var y = sc.scrollTop, dy = y - last; last = y;
      if (v === "c") {{
        var h = bar.offsetHeight + 4;
        off = Math.max(0, Math.min(h, off + dy)); if (y < 10) off = 0;
        bar.style.translate = "0 " + (-off) + "px";
        if (griff) griff.style.setProperty("--g", (off / h).toFixed(2));
        return;
      }}
      if (y < 80) {{ bar.classList.remove("hide"); travel = 0; return; }}
      travel = (dy > 0) === (travel > 0) ? travel + dy : dy;
      if (travel > 24) bar.classList.add("hide");
      else if (travel < -12) bar.classList.remove("hide");
    }}, {{ passive: true }});
  }});

  /* Vorführung: runter, kurz hoch, wieder runter, zurück nach oben */
  function fahre(sc, ziel, ms) {{
    return new Promise(function (res) {{
      var start = sc.scrollTop, t0 = performance.now();
      if (reduced) {{ sc.scrollTop = ziel; return setTimeout(res, 300); }}
      (function step(t) {{
        var k = Math.min(1, (t - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        sc.scrollTop = start + (ziel - start) * e;
        if (k < 1) requestAnimationFrame(step); else res();
      }})(t0);
    }});
  }}
  function warte(ms) {{ return new Promise(function (r) {{ setTimeout(r, ms); }}); }}
  var laeuft = false;
  document.getElementById("vor").addEventListener("click", function () {{
    if (laeuft) return; laeuft = true; var b = this; b.textContent = "Läuft …";
    var scs = phones.map(function (p) {{ return p.querySelector(".screen"); }});
    function alle(z, ms) {{ return Promise.all(scs.map(function (s) {{ return fahre(s, z, ms); }})); }}
    alle(0, 300).then(function () {{ return warte(400); }})
      .then(function () {{ return alle(520, 1600); }}).then(function () {{ return warte(900); }})
      .then(function () {{ return alle(380, 900); }}).then(function () {{ return warte(1100); }})
      .then(function () {{ return alle(900, 1500); }}).then(function () {{ return warte(900); }})
      .then(function () {{ return alle(0, 1400); }})
      .then(function () {{ laeuft = false; b.textContent = "Automatisch vorführen"; }});
  }});
  document.getElementById("hoch").addEventListener("click", function () {{ phones.forEach(function (p) {{ var s = p.querySelector(".screen"); s.scrollTo({{ top: 0, behavior: reduced ? "auto" : "smooth" }}); }}); }});
  Array.prototype.forEach.call(document.querySelectorAll(".tabs button"), function (t, i, all) {{
    t.addEventListener("click", function () {{
      Array.prototype.forEach.call(all, function (x) {{ x.setAttribute("aria-pressed", x === t); }});
      phones.forEach(function (p) {{ p.classList.toggle("zeigen", p.getAttribute("data-v") === t.getAttribute("data-z")); }});
    }});
  }});
}})();
</script>
'''
open(D + "leiste-live.html", "w", encoding="utf-8").write(html)
print("ok", len(html) // 1024, "KB")
