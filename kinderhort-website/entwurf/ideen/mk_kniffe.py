import re
D = __import__("os").path.dirname(__import__("os").path.abspath(__file__)) + "/"
src = open(D + 'ideen-3.html', encoding='utf-8').read()
head = src[:src.index('\n/* 1 Weg durch den Tag */')].replace('<title>Hort-Webseite Ideenkatalog 3</title>', '<title>Hort-Webseite Design-Kniffe</title>')
vote_css = src[src.index('/* Auswahl je Idee */'):src.index('</style>')]
helpers = src[src.index('<script>'):src.index('  /* A Weg durch den Tag */')]
vote_js = src[src.index('  /* Auswahl: Ja / Merken / Nein'):src.rfind('})();\n</script>')]
for a, b in [('collection("auswahl")', 'collection("kniffe")'), ('"ideen3-wahl"', '"kniffe-wahl"'), ('"idee-"', '"kniff-"')]:
    assert a in vote_js, a
    vote_js = vote_js.replace(a, b)

EZ = 'cubic-bezier(.22,1,.36,1)'
CSS = r'''
.status { font-size: .76rem; font-weight: 700; padding: 3px 10px; border-radius: 6px; }
.st-fehlt { background: #F6D9D3; color: #7E3B31; } .st-teil { background: #F3E9C9; color: #6B5317; } .st-da { background: #DDF3E6; color: #1F6B43; }
.where { font-size: .86rem; color: var(--ink-soft); }
.where b { color: var(--ink); }
.vn { position: absolute; top: 12px; left: 12px; z-index: 5; }
.vn.seg button { padding: 6px 12px; min-height: 32px; font-size: .8rem; }
.stage.kn { padding-top: 58px; }
.demo { width: 100%; display: grid; place-items: center; }
.filter { max-width: 100%; overflow-x: auto; scrollbar-width: none; } .filter::-webkit-scrollbar { display: none; }

/* 1 Concentric radius */
.cc { width: 280px; background: #F3F8F7; border-radius: 28px; padding: 12px; display: grid; gap: 12px; box-shadow: 0 16px 30px -16px rgba(0,0,0,.55); color: var(--ink); }
.cc img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; display: block; border-radius: 28px; transition: border-radius .3s EZ; }
.cc .row { display: flex; gap: 8px; }
.cc .row span { flex: 1; text-align: center; padding: 9px 0; border-radius: 22px; background: #D4B5B0; font-weight: 600; font-size: .84rem; border-radius: 28px; transition: border-radius .3s EZ; }
.after .cc img, .after .cc .row span { border-radius: 16px; }
.cc-note { margin-top: 12px; font-size: .8rem; color: var(--on-soft); text-align: center; }
.cc-note b { color: var(--on); }

/* 2 Alpha borders */
.ab { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); width: 100%; max-width: 460px; border-radius: 14px; overflow: hidden; }
.ab > div { padding: 16px 12px; display: grid; gap: 10px; justify-items: center; }
.ab .b1 { background: #A8C5C0; color: #1E3B44; } .ab .b2 { background: #F3F8F7; color: #1E3B44; } .ab .b3 { background: #2D6A6A; color: #F3F8F7; }
.ab .box { width: 100%; height: 44px; border-radius: 10px; border: 1.5px solid #8FA9A4; transition: border-color .3s EZ; }
.ab .pill2 { padding: 6px 12px; border-radius: 10px; border: 1.5px solid #8FA9A4; font-size: .78rem; font-weight: 600; transition: border-color .3s EZ; }
.after .ab .box, .after .ab .pill2 { border-color: color-mix(in oklab, currentColor 18%, transparent); }

/* 3 OKLCH palettes */
.pal { width: 100%; max-width: 460px; display: grid; gap: 8px; }
.pal .lbl2 { font-size: .74rem; color: var(--on-soft); font-weight: 600; }
.pal .sw { display: grid; grid-template-columns: repeat(7, 1fr); border-radius: 10px; overflow: hidden; }
.pal .sw span { height: 42px; display: grid; place-items: center; font-size: .66rem; font-weight: 700; font-variant-numeric: tabular-nums; }

/* 4 OKLCH gradients */
.gr { width: 100%; max-width: 460px; display: grid; gap: 10px; }
.gr .bar { height: 54px; border-radius: 12px; background: linear-gradient(90deg, #1E3B44, #D4B5B0); }
.after .gr .bar { background: linear-gradient(in oklch 90deg, #1E3B44, #D4B5B0); }
.gr .bar.b2 { background: linear-gradient(90deg, #A8C5C0, #D4B5B0); } .after .gr .bar.b2 { background: linear-gradient(in oklch 90deg, #A8C5C0, #D4B5B0); }
.gr .photo { position: relative; height: 130px; border-radius: 12px; overflow: hidden; }
.gr .photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.gr .photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,42,49,0) 10%, rgba(20,42,49,.86) 100%); }
.after .gr .photo::after { background: linear-gradient(in oklab 180deg, oklch(26% .03 215 / 0) 10%, oklch(26% .03 215 / .86) 100%); }
.gr .photo b { position: absolute; left: 14px; bottom: 10px; z-index: 1; color: #fff; font-size: 1.1rem; }

/* 5 Matched icon weight */
.iw { width: 100%; max-width: 440px; display: grid; grid-template-columns: repeat(4, 1fr); background: #142A31; border-radius: 16px; padding: 8px; }
.iw div { display: grid; justify-items: center; gap: 4px; color: #F3F8F7; font-weight: 600; font-size: .72rem; padding: 8px 0; }
.iw svg { fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; transition: stroke-width .3s EZ, width .3s, height .3s; }
.iw .i1 svg { width: 18px; height: 18px; stroke-width: 1.4; } .iw .i2 svg { width: 24px; height: 24px; stroke-width: 2.4; } .iw .i3 svg { width: 22px; height: 22px; stroke-width: 2; } .iw .i4 svg { width: 20px; height: 20px; stroke-width: 1.5; }
.after .iw svg { width: 21px !important; height: 21px !important; stroke-width: 1.8 !important; }
.iw-note { margin-top: 10px; text-align: center; font-size: .8rem; color: var(--on-soft); }

/* 6 Masked edges */
.me { width: 100%; max-width: 420px; display: grid; gap: 12px; }
.me .strip { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding: 6px; border-radius: 14px; background: rgba(243,248,247,.9); }
.me .strip::-webkit-scrollbar { display: none; }
.me .strip span { flex: none; padding: 9px 14px; border-radius: 10px; font-weight: 600; font-size: .86rem; color: #1E3B44; }
.me .strip span:first-child { background: #D4B5B0; }
.after .me .strip { -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 var(--ml, 0px), #000 calc(100% - var(--mr, 0px)), transparent 100%); mask-image: linear-gradient(90deg, transparent 0, #000 var(--ml, 0px), #000 calc(100% - var(--mr, 0px)), transparent 100%); }
.me .track { display: flex; gap: 10px; overflow-x: auto; scrollbar-width: none; }
.me .track::-webkit-scrollbar { display: none; }
.me .track img { flex: none; width: 150px; height: 100px; object-fit: cover; border-radius: 12px; }
.after .me .track { -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 var(--ml, 0px), #000 calc(100% - var(--mr, 0px)), transparent 100%); mask-image: linear-gradient(90deg, transparent 0, #000 var(--ml, 0px), #000 calc(100% - var(--mr, 0px)), transparent 100%); }

/* 7 Blurred icon swaps */
.sw7 { display: flex; gap: 14px; justify-content: center; }
.sw7 button { display: inline-flex; align-items: center; gap: 10px; border: 0; border-radius: 12px; padding: 10px 16px; background: #F3F8F7; color: #1E3B44; font: 600 .9rem var(--font); cursor: pointer; }
.sw7 .ic2 { position: relative; width: 22px; height: 22px; }
.sw7 .ic2 svg { position: absolute; inset: 0; width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.sw7 .ic2 .b { opacity: 0; }
.sw7 button.on .ic2 .a { opacity: 0; } .sw7 button.on .ic2 .b { opacity: 1; }
.after .sw7 .ic2 svg { transition: opacity .2s EZ, filter .2s EZ, transform .2s EZ; }
.after .sw7 .ic2 .b { filter: blur(4px); transform: scale(.5); }
.after .sw7 button.on .ic2 .a { filter: blur(4px); transform: scale(.5); } .after .sw7 button.on .ic2 .b { filter: blur(0); transform: none; }

/* 8 Dark mode depth */
.dk { width: 100%; max-width: 440px; border-radius: 16px; padding: 16px; background: oklch(20% .025 215); display: grid; gap: 10px; color: oklch(94% .01 190); }
.dk .s1, .dk .s2, .dk .s3 { border-radius: 12px; padding: 12px 14px; font-size: .86rem; background: oklch(20% .025 215); box-shadow: 0 10px 24px -8px rgba(0,0,0,.6); transition: background .3s EZ, box-shadow .3s EZ; }
.dk .s2 { margin-left: 16px; } .dk .s3 { margin-left: 32px; }
.dk small { display: block; color: oklch(75% .02 200); margin-top: 2px; }
.after .dk .s1 { background: oklch(25% .028 210); box-shadow: inset 0 1px 0 oklch(100% 0 0 / .06); }
.after .dk .s2 { background: oklch(29% .03 205); box-shadow: inset 0 1px 0 oklch(100% 0 0 / .08); }
.after .dk .s3 { background: oklch(33% .032 200); box-shadow: inset 0 1px 0 oklch(100% 0 0 / .1); }

/* 9 Dynamic viewport */
.dv { display: flex; gap: 16px; align-items: center; justify-content: center; flex-wrap: wrap; }
.phone2 { position: relative; width: 190px; height: 360px; border-radius: 28px; border: 6px solid #0E1E23; background: #A8C5C0; overflow: hidden; }
.phone2 .hero2 { position: absolute; left: 0; right: 0; top: 0; height: var(--h, 348px); background: url("img/p2160110-800.webp") center / cover; display: flex; align-items: flex-end; padding: 12px; transition: height .3s EZ; }
.phone2 .hero2 span { background: #D4B5B0; color: #1E3B44; font-weight: 600; font-size: .76rem; padding: 8px 12px; border-radius: 10px; }
.phone2 .bbar { position: absolute; left: 0; right: 0; bottom: 0; height: 52px; background: rgba(240,240,240,.95); display: grid; place-items: center; font-size: .66rem; color: #555; translate: 0 100%; transition: translate .3s EZ; z-index: 2; }
.phone2.bar .bbar { translate: 0 0; }
.dv-side { display: grid; gap: 10px; max-width: 200px; } .dv-side p { font-size: .84rem; color: var(--on-soft); }

/* 10 Multiply */
.mp { width: 100%; max-width: 440px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 12px; align-items: center; background: #A8C5C0; border-radius: 16px; padding: 16px; color: #1E3B44; }
.mp img { width: 100%; display: block; border-radius: 6px; rotate: -2deg; box-shadow: 0 10px 20px -10px rgba(0,0,0,.4); transition: box-shadow .3s; }
.after .mp img { mix-blend-mode: multiply; box-shadow: none; }
.mp p { font-size: .86rem; } .mp b { display: block; font-size: 1rem; margin-bottom: 4px; }
'''.replace('EZ', EZ)

def card(k, num_status, title, text, where, stage):
    lab = {"fehlt": ("st-fehlt", "Fehlt noch"), "teil": ("st-teil", "Teilweise da"), "da": ("st-da", "Schon da")}[num_status]
    return f'''
    <article class="card" data-k="{k}">
      <div class="stage kn"><div class="seg vn" role="group" aria-label="Vorher oder nachher"><span class="knob" aria-hidden="true"></span><button type="button" data-v="0" aria-pressed="false">Vorher</button><button type="button" data-v="1" aria-pressed="true">Nachher</button></div><div class="demo after">{stage}</div></div>
      <div class="about"><div class="meta"><span class="status {lab[0]}">{lab[1]}</span></div>
        <h2>{title}</h2><p>{text}</p><p class="where">{where}</p></div>
    </article>
'''
SV = lambda p: f'<svg viewBox="0 0 24 24">{p}</svg>'
PH = '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>'
ML = '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'
CA = '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'
SE = '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.8-3.8"/>'
CHIPS = "".join(f'<span>{t}</span>' for t in ["Überblick", "Räumlichkeiten", "Virtueller Rundgang", "Tagesablauf", "Das zeichnet uns aus", "Fragen", "Ferienplan"])
TRACK = "".join(f'<img src="img/{p}-800.webp" alt="">' for p in ["p2160110", "turnraum", "kreatviraum-5-1", "lesecke", "werkraum"])

HTML = (
card('teil', 'teil', '1 · Verschachtelte Rundungen passen zueinander', 'Liegt etwas Rundes in etwas Rundem, gilt: innen = außen minus Abstand. Sonst wirken die Ecken „eingeklemmt“. Im Vorher haben Foto und Knöpfe dieselbe Rundung wie die Karte, im Nachher 28 − 12 = 16 Pixel.',
     'Auf der Seite: <b>Umschalter sind schon richtig</b>, offen sind z. B. Datumsfelder in den Terminen, Kalendertage und Fotos in Karten.',
     '<div><div class="cc"><img src="img/p2160110-800.webp" alt=""><div class="row"><span>Merken</span><span>Teilen</span></div></div><p class="cc-note">außen <b>28</b> − Abstand <b>12</b> = innen <b>16</b></p></div>')
+ card('teil', 'teil', '2 · Ränder aus durchsichtiger Textfarbe', 'Rahmen bekommen keine feste Grauton-Farbe, sondern die Textfarbe mit wenig Deckkraft. Dann passen sie auf jedem Hintergrund – Salbei, Papier und dunkles Türkis. Im Vorher wirkt derselbe Grauton auf jedem Grund anders.',
     'Auf der Seite: <b>feine Linien sind schon so</b>, offen sind die Rahmen der hellen Knöpfe und Eingabefelder.',
     '<div class="ab"><div class="b1"><span class="box"></span><span class="pill2">Kontakt</span></div><div class="b2"><span class="box"></span><span class="pill2">Kontakt</span></div><div class="b3"><span class="box"></span><span class="pill2">Kontakt</span></div></div>')
+ card('da', 'da', '3 · Farbabstufungen in OKLCH', 'Hellere und dunklere Stufen einer Farbe werden in OKLCH berechnet statt in HSL. Dann wirken die Schritte gleichmäßig, und der Farbton kippt nicht ins Gräuliche oder Bläuliche. Oben HSL, unten OKLCH – mit Vorher/Nachher wechselt die zweite Reihe.',
     'Auf der Seite: <b>schon umgesetzt</b> – die Farben sind in OKLCH hinterlegt. Diese Stufen könnten noch die restlichen festen Farbtöne ersetzen.',
     '<div class="pal" id="pal"></div>')
+ card('fehlt', 'fehlt', '4 · Farbverläufe in OKLCH', 'Ein Verlauf von Petrol zu Rosé wird normal durch ein trübes Grau gerechnet. In OKLCH bleibt die Mitte farbig und klar. Auch die dunklen Verläufe über Fotos werden weicher, ohne grauen Schleier.',
     'Auf der Seite: <b>fehlt noch</b> – betrifft die dunklen Verläufe über den Fotos (Kopfbilder, Rundgang, Teaser).',
     '<div class="gr"><div class="bar"></div><div class="bar b2"></div><div class="photo"><img src="img/kreatviraum-5-1-800.webp" alt=""><b>Kinderhort</b></div></div>')
+ card('fehlt', 'fehlt', '5 · Symbole so kräftig wie die Schrift', 'Seit die Schrift ruhiger ist (Stärke 600), passen manche Symbole nicht mehr dazu: mal zu dünn, mal zu dick, unterschiedlich groß. Im Nachher haben alle dieselbe Größe und eine Strichstärke, die zum Text passt.',
     'Auf der Seite: <b>fehlt noch</b> – die Symbole haben Strichstärke 2 (Buttons, Menü, Leiste) und 1,5 (Gruppen).',
     f'<div><div class="iw"><div class="i1">{SV(PH)}Anrufen</div><div class="i2">{SV(ML)}Krankmelden</div><div class="i3">{SV(CA)}Termine</div><div class="i4">{SV(SE)}Suche</div></div><p class="iw-note">Text 600 → Strich 1,8 · alle 21 Pixel</p></div>')
+ card('fehlt', 'fehlt', '6 · Weiche Kanten statt abgeschnitten', 'Wo man seitlich wischen kann, schneidet die Seite bisher hart ab – wie bei „Virtueller Rundg“ in deinem Screenshot. Mit weichen Kanten blendet der Rand aus, und nur dort, wo es weitergeht. Zum Ausprobieren wischen.',
     'Auf der Seite: <b>fehlt noch</b> – Sprungmarken unter dem Kopfbild, Rundgang-Fotos, Bildkarten-Reihen.',
     f'<div class="me"><div class="strip" data-mask>{CHIPS}</div><div class="track" data-mask>{TRACK}</div></div>')
+ card('teil', 'teil', '7 · Symbole wechseln mit Unschärfe', 'Wenn ein Symbol zu einem anderen wird – Menü zu Kreuz, Kopieren zu Haken – blendet das alte kurz unscharf und klein aus, das neue unscharf und klein ein. Im Vorher springt es einfach. Knöpfe antippen.',
     'Auf der Seite: <b>teilweise</b> – der Kopieren-Knopf macht es schon; Menü-Knopf, Merken und Teilen noch nicht.',
     '<div class="sw7"><button type="button"><span class="ic2"><svg class="a" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="b" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></span>Menü</button><button type="button"><span class="ic2"><svg class="a" viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg><svg class="b" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>Kopieren</button></div>')
+ card('fehlt', 'fehlt', '8 · Tiefe im Dunkelmodus', 'Nur falls es einmal einen Dunkelmodus geben soll: Im Dunkeln sieht man Schatten kaum. Höhere Ebenen werden deshalb heller statt schattiger, dazu eine feine Lichtkante oben. Im Vorher verschwimmen die Ebenen.',
     'Auf der Seite: <b>gibt es nicht</b> – die Seite hat keinen Dunkelmodus. Nur ein Entwurf, falls ihr einen möchtet.',
     '<div class="dk"><div class="s1">Seite<small>Grundfläche</small></div><div class="s2">Karte<small>eine Ebene höher</small></div><div class="s3">Menü<small>ganz oben</small></div></div>')
+ card('teil', 'teil', '9 · Höhe passt sich der Browserleiste an', 'Am Handy blendet der Browser seine Leiste ein und aus. Eine Fläche „so hoch wie der Bildschirm“ mit der alten Einheit 100vh rutscht dann unter die Leiste – der Knopf unten verschwindet. Mit der neuen Einheit 100dvh passt sie sich an.',
     'Auf der Seite: <b>teilweise</b> – die Suche am Handy passt sich schon an; Bildansicht und Geschichte nutzen noch die alte Einheit.',
     '<div class="dv"><div class="phone2" id="phone2"><div class="hero2"><span>Platz anfragen</span></div><div class="bbar">kinderhort-grombuehl.de</div></div><div class="dv-side"><p>Browserleiste ein- und ausblenden und auf den Knopf achten.</p><button type="button" class="btn" id="barBtn">Leiste einblenden</button></div></div>')
+ card('fehlt', 'fehlt', '10 · Papier verschmilzt mit dem Hintergrund', 'Der eingescannte Original-Aushang hat weißes Papier und liegt als weißes Rechteck auf dem Salbei. Mit „Multiplizieren“ nimmt das Papier den Farbton der Seite an, Schrift und Farben bleiben – als wäre der Aushang auf die Seite gedruckt.',
     'Auf der Seite: <b>fehlt noch</b> – betrifft den Original-Aushang beim Ferienplan und eingescannte Elternbriefe.',
     '<div class="mp"><img src="img/aushang-800.jpg" alt="Original-Aushang Ferienplan"><p><b>Ferienplan 2026/27</b>Original-Aushang mit Schließtagen und Vormerkterminen</p></div>')
)

JS = r'''
  /* Vorher / Nachher je Karte */
  $$(".vn").forEach(function (g) { var demo = g.parentNode.querySelector(".demo"); segment(g, function (b) { demo.classList.toggle("after", b.dataset.v === "1"); updMasks(); }); });

  /* 3 Farbstufen: HSL gegen OKLCH */
  (function () {
    var box = $("#pal"), steps = [95, 85, 72, 60, 48, 36, 26];
    function row(name, hsl, okl) { return '<span class="lbl2">' + name + '</span><div class="sw">' + steps.map(function (l, i) { var bg = hsl(l, i), fg = l > 60 ? "#1E3B44" : "#F3F8F7"; return '<span style="background:' + bg + ';color:' + fg + '">' + l + "</span>"; }).join("") + "</div>"; }
    function render(after) {
      box.innerHTML = row("Petrol – HSL", function (l) { return "hsl(190 38% " + l + "%)"; }) + row(after ? "Petrol – OKLCH" : "Petrol – HSL (vorher)", after ? function (l) { return "oklch(" + l + "% 0.05 205)"; } : function (l) { return "hsl(190 38% " + l + "%)"; }) +
        row("Rosé – HSL", function (l) { return "hsl(8 30% " + l + "%)"; }) + row(after ? "Rosé – OKLCH" : "Rosé – HSL (vorher)", after ? function (l) { return "oklch(" + l + "% 0.04 28)"; } : function (l) { return "hsl(8 30% " + l + "%)"; });
    }
    render(true);
    new MutationObserver(function () { render(box.closest(".demo").classList.contains("after")); }).observe(box.closest(".demo"), { attributes: true, attributeFilter: ["class"] });
  })();

  /* 6 Weiche Kanten nur dort, wo es weitergeht */
  function updMasks() { $$("[data-mask]").forEach(function (el) { var l = el.scrollLeft > 2, r = el.scrollLeft + el.clientWidth < el.scrollWidth - 2; el.style.setProperty("--ml", l ? "36px" : "0px"); el.style.setProperty("--mr", r ? "36px" : "0px"); }); }
  $$("[data-mask]").forEach(function (el) { el.addEventListener("scroll", updMasks, { passive: true }); }); updMasks(); addEventListener("resize", updMasks);

  /* 7 Symbole tauschen */
  $$(".sw7 button").forEach(function (b) { b.addEventListener("click", function () { b.classList.toggle("on"); }); });

  /* 9 Browserleiste */
  (function () { var ph = $("#phone2"), btn = $("#barBtn"), hero = $(".hero2", ph), demo = ph.closest(".demo");
    function upd() { var bar = ph.classList.contains("bar"), after = demo.classList.contains("after"); hero.style.setProperty("--h", (after && bar ? 296 : 348) + "px"); }
    btn.addEventListener("click", function () { var o = !ph.classList.contains("bar"); ph.classList.toggle("bar", o); btn.textContent = o ? "Leiste ausblenden" : "Leiste einblenden"; upd(); });
    new MutationObserver(upd).observe(demo, { attributes: true, attributeFilter: ["class"] }); upd(); })();
'''

out = (head + CSS + vote_css + '''</style>

<div class="wrap">
  <header class="intro">
    <span class="kicker">Design-Kniffe</span>
    <h1>10 Kniffe für den letzten Schliff</h1>
    <p>Die zehn Design-Kniffe aus deinem Bild, jeweils an einem echten Bauteil der Seite. Oben auf jeder Karte zwischen <b>Vorher</b> und <b>Nachher</b> umschalten. Darunter steht, ob der Kniff auf der Seite schon umgesetzt ist, teilweise oder noch fehlt.</p>
  </header>
  <p class="sync-note">Unter jedem Kniff kannst du <b>Ja</b>, <b>Merken</b> oder <b>Nein</b> wählen und eine Anmerkung schreiben. Deine Auswahl wird gespeichert, und Claude kann sie direkt lesen.</p>

  <div class="filter" role="group" aria-label="Kniffe filtern">
    <span class="knob" aria-hidden="true"></span>
    <button type="button" data-f="alle" aria-pressed="true">Alle</button>
    <button type="button" data-f="fehlt" aria-pressed="false">Fehlt noch</button>
    <button type="button" data-f="teil" aria-pressed="false">Teilweise da</button>
    <button type="button" data-f="offen" aria-pressed="false">Noch offen</button>
  </div>

  <div class="grid">
''' + HTML + '''  </div>
  <p class="foot">Alle Beispiele beachten „Bewegung reduzieren“. Nichts davon ist schon geändert – sag einfach, welche Kniffe eingebaut werden sollen.</p>
</div>

''' + helpers + JS + '\n' + vote_js + '})();\n</script>\n')

# Nummern für die Auswahl (aus dem Titel „1 · …“)
out = re.sub(r'(<div class="about"><div class="meta">.*?</div>\s*<h2>)(\d+) · ', lambda m: m.group(1) + '<span class="num">' + m.group(2) + '</span> ', out, flags=re.S)
assert out.count('class="num"') == 10, out.count('class="num"')
open(D + 'kniffe.html', 'w', encoding='utf-8').write(out)
print('ok', len(out))
