"""Live-Vorschau Runde 3: drei kleine Stellen, vorher / nachher."""
import os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
alt = open(D + "animationen-live.html", encoding="utf-8").read()
BASIS = alt[alt.index("<style>") + 7:alt.index("/* ---------- Aufklapp-Kästen")]

def demo(nr, titel, text, inhalt):
    return f'''<section class="demo" aria-labelledby="t{nr}">
    <div class="demo-kopf"><span class="nr">{nr}</span><h2 id="t{nr}">{titel}</h2><p>{text}</p></div>
    <div class="paar">
      <div class="seite" data-art="vor"><span class="etikett">Vorher</span>{inhalt}</div>
      <div class="seite nach" data-art="nach"><span class="etikett">Nachher</span>{inhalt}</div>
    </div>
  </section>'''

STATUS = '''<div class="status"><div class="st-row"><i></i><b>Jetzt geöffnet – heute bis 18:00 Uhr</b></div>
<p class="st-sub">Krippe und Kindergarten bis 16:30 Uhr, Hort bis 18:00 Uhr.</p>
<div class="ask"><button type="button" data-q="morgen" aria-pressed="false">Morgen offen?</button><button type="button" data-q="woche" aria-pressed="false">Nächste Woche?</button><button type="button" data-q="ferien" aria-pressed="false">Nächste Ferien?</button></div>
<div class="ans-box"><p class="ans" aria-live="polite"></p></div></div>'''

def tage():
    zellen = '<span></span>' * 6 + '<span class="fe">1</span>'
    for d in range(2, 31):
        if d in (2, 3): zellen += f'<span class="zu">{d}</span>'
        elif d in (18, 26): zellen += f'<button type="button" class="ev" data-d="{d}">{d}</button>'
        else: zellen += f'<span>{d}</span>'
    return zellen
KAL = f'''<div class="kal"><b class="mon">November 2026</b><div class="wd"><span>Mo</span><span>Di</span><span>Mi</span><span>Do</span><span>Fr</span><span>Sa</span><span>So</span></div>
<div class="grid">{tage()}</div><p class="note">Tippen Sie auf einen dunklen Tag.</p></div>'''

FILTER = '''<div class="fl"><div class="filter" role="group" aria-label="Termine nach Bereich"><button type="button" data-b="alle" aria-pressed="true">Alle</button><button type="button" data-b="krippe" aria-pressed="false">Krippe</button><button type="button" data-b="hort" aria-pressed="false">Hort</button></div>
<p class="leer" hidden>Für diesen Bereich stehen gerade keine eigenen Termine an. Termine für das ganze Haus sehen Sie unter „Alle“.</p>
<ul class="liste3"><li><b>Weihnachtsmarkt</b> · 04.12.</li><li data-b="hort"><b>Ferienfreizeit</b> · 06.09. <span class="tag">Hort</span></li></ul></div>'''

SEITE = "".join([
    demo(1, "Fragen unter „Jetzt geöffnet“", "Tippen Sie nacheinander auf die drei Fragen. Heute springt die Antwort hinein und die Karte ändert ruckartig die Höhe. Nachher blendet die Antwort ein und die Karte wächst mit.", STATUS),
    demo(2, "Kalender: Tag antippen", "Tippen Sie abwechselnd auf den 18. und den 26. Nachher blendet der Text unter dem Kalender weich über.", KAL),
    demo(3, "Hinweis beim Bereichs-Filter", "Tippen Sie auf „Krippe“. Für die Krippe gibt es hier keinen eigenen Termin, deshalb erscheint ein Hinweis – nachher blendet er weich ein.", FILTER),
])

CSS = BASIS + '''
[hidden] { display: none !important; }
button:focus-visible { outline: 3px solid var(--rose-deep); outline-offset: 2px; }
/* 1 Status-Karte */
.status { background: var(--card); color: var(--on); border-radius: 20px; padding: 16px; display: grid; gap: 8px; }
.st-row { display: flex; gap: 10px; align-items: center; } .st-row i { width: 10px; height: 10px; border-radius: 50%; background: #7FD6A4; flex: none; }
.st-sub { margin: 0; font-size: .86rem; opacity: .85; }
.ask { display: flex; flex-wrap: wrap; gap: 6px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,.18); }
.ask button { min-height: 38px; padding: 0 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,.3); background: transparent; color: var(--on); font: 600 .84rem var(--font); cursor: pointer; transition: scale .16s var(--ease-out), background .15s; }
.ask button:active { scale: .97; } .ask button[aria-pressed="true"] { background: var(--on); color: var(--ink); }
.ans-box { overflow: hidden; }
.ans { margin: 0; font-size: .9rem; min-height: 0; }
.ans:not(:empty) { padding-top: 2px; }
/* 2 Kalender */
.kal { background: var(--paper); color: var(--ink); border-radius: 18px; padding: 14px; display: grid; gap: 6px; }
.kal .mon { text-align: center; }
.kal .wd, .kal .grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 3px; text-align: center; font-size: .82rem; }
.kal .wd { font-size: .7rem; color: var(--soft); font-weight: 600; }
.kal .grid > * { aspect-ratio: 1; display: grid; place-items: center; border-radius: 8px; font: 600 .82rem var(--font); border: 0; background: none; color: inherit; padding: 0; }
.kal .zu { background: var(--rose-soft); } .kal .fe { box-shadow: inset 0 0 0 2px var(--rose-deep); background: var(--rose-soft); }
.kal .ev { background: var(--ink); color: var(--on); cursor: pointer; } .kal .ev[aria-pressed="true"] { box-shadow: 0 0 0 3px var(--rose-deep); }
.kal .note { margin: 6px 0 0; min-height: 3em; font-size: .88rem; }
.kal .note b { display: block; }
/* 3 Filter */
.fl { display: grid; gap: 10px; }
.filter { display: inline-flex; flex-wrap: wrap; gap: 2px; padding: 4px; border-radius: 12px; background: var(--chip); justify-self: start; }
.filter button { min-height: 40px; padding: 0 12px; border: 0; border-radius: 8px; background: none; color: var(--ink); font: 600 .88rem var(--font); cursor: pointer; transition: background .15s, scale .16s var(--ease-out); }
.filter button:active { scale: .97; } .filter button[aria-pressed="true"] { background: var(--ink); color: var(--on); }
.leer { margin: 0; color: var(--ink); font-size: .9rem; }
.nach .leer { transition: opacity .18s var(--ease-out), translate .18s var(--ease-out); }
@starting-style { .nach .leer:not([hidden]) { opacity: 0; translate: 0 4px; } }
.liste3 { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
.liste3 li { padding: 12px 14px; border-radius: 14px; background: var(--card); color: var(--on); font-size: .9rem; }
.liste3 .tag { margin-left: 6px; padding: 0 7px; border-radius: 6px; background: rgba(255,255,255,.16); font-size: .72rem; font-weight: 600; }
@media (prefers-reduced-motion: reduce) { .nach .leer { transition-duration: .01s; } }
'''

JS = r'''
(function () {
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches, EOUT = "cubic-bezier(.23,1,.32,1)";
  function q(s, el) { return (el || document).querySelector(s); }
  function qa(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  var ANTWORT = { morgen: "Ja, morgen (Dienstag) haben wir ganz normal geöffnet.", woche: "Nächste Woche geschlossen: Freitag (Konzeptionstag).", ferien: "Weihnachten: geschlossen vom 24.12.2026 bis 08.01.2027 (7 Schließtage)." };
  var NOTIZ = { "18": "<b>Buß- und Bettag</b>Mittwoch, 18.11.2026 – für Hortkinder ein Ferientag.", "26": "<b>Laternen basteln</b>Donnerstag, 26.11.2026 – in allen Gruppen am Vormittag." };
  qa(".seite").forEach(function (seite) {
    var nach = seite.getAttribute("data-art") === "nach" && !reduced;
    /* 1 Status-Fragen */
    var box = q(".ans-box", seite);
    if (box) { var ans = q(".ans", seite);
      qa(".ask button", seite).forEach(function (b) { b.addEventListener("click", function () {
        qa(".ask button", seite).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var von = box.offsetHeight; ans.textContent = ANTWORT[b.getAttribute("data-q")];
        if (!nach) return;
        var bis = box.offsetHeight;
        box.animate([{ height: von + "px" }, { height: bis + "px" }], { duration: 220, easing: EOUT });
        ans.animate([{ opacity: 0, translate: "0 4px" }, { opacity: 1, translate: "0 0" }], { duration: 200, easing: EOUT });
      }); });
    }
    /* 2 Kalender */
    var note = q(".kal .note", seite);
    if (note) qa(".kal .ev", seite).forEach(function (b) { b.addEventListener("click", function () {
      qa(".kal .ev", seite).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      note.innerHTML = NOTIZ[b.getAttribute("data-d")];
      if (nach) note.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 150, easing: "ease-out" });
    }); });
    /* 3 Filter-Hinweis */
    var leer = q(".leer", seite);
    if (leer) qa(".filter button", seite).forEach(function (b) { b.addEventListener("click", function () {
      qa(".filter button", seite).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      var f = b.getAttribute("data-b");
      qa(".liste3 li", seite).forEach(function (li) { var k = li.getAttribute("data-b"); li.hidden = !(f === "alle" || !k || k === f); });
      leer.hidden = f !== "krippe";
    }); });
  });
})();
'''

html = f'''<title>Feinschliff Bewegung 3</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<style>{CSS}</style>
<main class="wrap">
  <header class="kopf"><h1>Feinschliff Bewegung, dritte Runde</h1>
  <p>Drei letzte kleine Stellen, jeweils links wie heute, rechts mit Bewegung. Tippen Sie in beiden Spalten dasselbe an und vergleichen Sie.</p></header>
  {SEITE}
</main>
<script>{JS}</script>
'''
open(D + "animationen-3.html", "w", encoding="utf-8").write(html)
print("ok", len(html) // 1024, "KB")
