"""Ideenkatalog 4 – jede Idee aus einem der installierten Skills, mit Demo und Abstimmung (Sammlung „ideen4“)."""
import re, os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(D + 'ideen-3.html', encoding='utf-8').read()
head = src[:src.index('\n/* 1 Weg durch den Tag */')].replace('<title>Hort-Webseite Ideenkatalog 3</title>', '<title>Hort-Webseite Ideen 4</title>')
vote_css = src[src.index('/* Auswahl je Idee */'):src.index('</style>')]
helpers = src[src.index('<script>'):src.index('  /* A Weg durch den Tag */')]
vote_js = src[src.index('  /* Auswahl: Ja / Merken / Nein'):src.rfind('})();\n</script>')]
for a, b in [('collection("auswahl")', 'collection("ideen4")'), ('"ideen3-wahl"', '"ideen4-wahl"'), ('"idee-"', '"i4-"')]:
    assert a in vote_js, a
    vote_js = vote_js.replace(a, b)

EZ = 'cubic-bezier(.23,1,.32,1)'
CSS = r'''
.skill { font-size: .76rem; font-weight: 600; padding: 3px 10px; border-radius: 6px; background: #E6EFED; color: #1E3B44; font-family: ui-monospace, Menlo, monospace; }
.where { font-size: .86rem; color: var(--ink-soft); }
.filter { max-width: 100%; overflow-x: auto; scrollbar-width: none; } .filter::-webkit-scrollbar { display: none; }
.demo { width: 100%; display: grid; place-items: center; }
.ph5 { width: 230px; border-radius: 26px; border: 6px solid #0E1E23; background: #A8C5C0; padding: 12px; display: grid; gap: 8px; color: #1E3B44; }
.tile { background: #F3F8F7; color: #1E3B44; border-radius: 14px; padding: 10px 12px; font-size: .8rem; text-align: left; }
.tile b { display: block; font-size: .92rem; }
.dk2 { background: #2D6A6A; color: #F3FAF8; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
.chips button { border: 0; border-radius: 10px; padding: 7px 10px; background: rgba(243,248,247,.85); color: #1E3B44; font: 600 .78rem var(--font, inherit); cursor: pointer; }
.chips button[aria-pressed="true"] { background: #1E3B44; color: #F3F8F7; }
.bigcall { display: flex; align-items: center; justify-content: center; gap: 8px; border-radius: 14px; background: #D4B5B0; color: #1E3B44; font-weight: 700; padding: 12px; font-size: .9rem; transition: background .2s; }
.small { font-size: .74rem; opacity: .85; }
/* 3 App-Kurzbefehle */
.homescreen { width: 230px; height: 250px; border-radius: 26px; border: 6px solid #0E1E23; background: linear-gradient(160deg, #4a6d74, #1E3B44); position: relative; display: grid; place-items: center; }
.appicon { width: 58px; height: 58px; border-radius: 15px; background: #1E3B44 url("img/apple-touch-icon.png") center / cover; box-shadow: 0 6px 16px rgba(0,0,0,.4); transition: scale .25s EZ; cursor: pointer; border: 0; }
.homescreen.hold .appicon { scale: 1.08; }
.qa { position: absolute; left: 50%; top: 18px; translate: -50% 0; width: 180px; border-radius: 14px; background: rgba(243,248,247,.96); color: #1E3B44; font-size: .8rem; overflow: hidden; opacity: 0; scale: .9; transform-origin: 50% 100%; transition: opacity .2s EZ, scale .25s EZ; }
.homescreen.hold .qa { opacity: 1; scale: 1; }
.qa div { padding: 9px 12px; border-bottom: 1px solid rgba(30,59,68,.12); font-weight: 600; } .qa div:last-child { border: 0; }
/* 4 neu seit Besuch */
.newlist { width: 260px; display: grid; gap: 6px; }
.newlist div { background: #2D6A6A; color: #F3FAF8; border-radius: 10px; padding: 9px 12px; font-size: .8rem; display: flex; gap: 8px; align-items: center; }
.newlist i { width: 8px; height: 8px; border-radius: 50%; background: #7FD6A4; flex: none; transition: scale .3s EZ; }
.newlist div:not(.isnew) i { scale: 0; }
/* 5 Ablaufdatum */
.exp { width: 260px; display: grid; gap: 10px; }
.exp .tile { transition: opacity .4s EZ, translate .4s EZ; }
.exp .tile.gone { opacity: .25; translate: 0 4px; text-decoration: line-through; }
.exp input { width: 100%; accent-color: #2D6A6A; }
/* 6 wischen */
.swrow { position: relative; width: 270px; border-radius: 14px; overflow: hidden; background: #7FD6A4; touch-action: pan-y; }
.swrow .under { position: absolute; inset: 0; display: flex; align-items: center; padding-left: 16px; font-weight: 700; color: #142A31; font-size: .82rem; }
.swrow .front { position: relative; background: #F3F8F7; color: #1E3B44; font-weight: 600; padding: 12px 14px; font-size: .82rem; cursor: grab; user-select: none; touch-action: pan-y; }
.swrow .front.saved::after { content: "✓ gemerkt"; float: right; color: #7FD6A4; font-weight: 700; }
/* 7 Tagesbalken */
.dayb { width: 100%; max-width: 420px; display: grid; gap: 8px; font-size: .78rem; color: #F3FAF8; }
.dayb .row { display: grid; grid-template-columns: 92px 1fr; gap: 8px; align-items: center; }
.dayb .bar { position: relative; height: 18px; border-radius: 6px; background: rgba(243,248,247,.12); }
.dayb .bar span { position: absolute; top: 0; bottom: 0; border-radius: 6px; background: #D4B5B0; }
.dayb .bar span.late { background: rgba(212,181,176,.5); }
.dayb .now { position: absolute; top: -4px; bottom: -4px; width: 2px; background: #7FD6A4; }
.dayb .axis { display: flex; justify-content: space-between; margin-left: 100px; opacity: .7; font-variant-numeric: tabular-nums; }
/* 8 Wimpel-Countdown */
.wc { display: grid; justify-items: center; gap: 10px; color: #F3FAF8; }
.wc svg { width: 300px; height: 70px; overflow: visible; }
.wc .f { fill: rgba(243,248,247,.18); transition: fill .4s EZ; }
.wc .f.on { fill: #D4B5B0; }
.wc .f.on.x { fill: #A8C5C0; }
/* 9 Ruhige Ansicht */
.calm { display: grid; justify-items: center; gap: 14px; }
.calm .ball { width: 40px; height: 40px; border-radius: 12px; background: #D4B5B0; animation: bob 1.6s ease-in-out infinite alternate; }
.calm.off .ball { animation: none; }
@keyframes bob { to { translate: 0 -18px; } }
.switch { background: none; border: 0; font: inherit; display: inline-flex; align-items: center; gap: 10px; color: #F3FAF8; font-size: .85rem; font-weight: 600; cursor: pointer; }
.switch i { width: 42px; height: 24px; border-radius: 999px; background: rgba(243,248,247,.25); position: relative; transition: background .2s; }
.switch i::after { content: ""; position: absolute; top: 3px; left: 3px; width: 18px; height: 18px; border-radius: 50%; background: #fff; transition: translate .2s EZ; }
.switch[aria-checked="true"] i { background: #7FD6A4; } .switch[aria-checked="true"] i::after { translate: 18px 0; }
/* 10 Tastatur */
.keys { width: 280px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 14px; font-size: .82rem; display: grid; gap: 8px; }
.keys div { display: flex; justify-content: space-between; align-items: center; }
.keys kbd { font: 600 .74rem ui-monospace, monospace; padding: 3px 7px; border-radius: 6px; background: #E6EFED; border: 1px solid rgba(30,59,68,.15); }
/* 11 Auftakt */
.hero4 { width: 100%; max-width: 420px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; align-items: center; color: #F3FAF8; }
.hero4 h4 { margin: 0; font-size: 1.2rem; line-height: 1.15; }
.hero4 .st { margin-top: 8px; font-size: .74rem; background: rgba(243,248,247,.15); border-radius: 8px; padding: 6px 8px; }
.pola { position: relative; height: 140px; }
.pola img { position: absolute; width: 96px; height: 76px; object-fit: cover; border: 4px solid #fff; border-radius: 4px; box-shadow: 0 8px 16px rgba(0,0,0,.35); }
.pola img:nth-child(1) { left: 0; top: 10px; rotate: -6deg; } .pola img:nth-child(2) { left: 70px; top: 0; rotate: 5deg; } .pola img:nth-child(3) { left: 40px; top: 60px; rotate: -2deg; }
/* 12 Film */
.film { width: 100%; max-width: 380px; aspect-ratio: 16 / 9; border-radius: 14px; overflow: hidden; position: relative; background: #142A31; }
.film img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; scale: 1.08; transition: opacity .6s EZ, scale 3.2s linear; }
.film img.on { opacity: 1; scale: 1; }
.film .cap { position: absolute; left: 12px; bottom: 16px; color: #fff; font-weight: 700; font-size: 1rem; text-shadow: 0 2px 10px rgba(0,0,0,.6); }
.film .prog { position: absolute; left: 0; bottom: 0; height: 4px; background: #D4B5B0; width: 0; }
/* 13 drei Schritte */
.steps3 { width: 100%; max-width: 440px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; counter-reset: s; }
.steps3 div { background: #F3F8F7; color: #1E3B44; border-radius: 14px; padding: 12px; font-size: .78rem; position: relative; }
.steps3 div b { display: block; font-size: .86rem; margin: 6px 0 2px; }
.steps3 div::before { counter-increment: s; content: counter(s); display: grid; place-items: center; width: 26px; height: 26px; border-radius: 8px; background: #D4B5B0; font-weight: 700; }
/* 14 Gute Gründe */
.proof { width: 100%; max-width: 440px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.proof div { background: rgba(243,248,247,.1); border: 1px solid rgba(243,248,247,.2); color: #F3FAF8; border-radius: 12px; padding: 10px 12px; font-size: .76rem; }
.proof b { display: block; font-size: 1.15rem; color: #D4B5B0; font-variant-numeric: tabular-nums; }
/* 15 Weiche */
.fork { width: 260px; display: grid; gap: 8px; }
/* 16 Hauskarte */
.plan4 { width: 100%; max-width: 420px; display: grid; grid-template-columns: 1fr 130px; gap: 12px; align-items: center; }
.plan4 svg { width: 100%; }
.plan4 rect { fill: rgba(243,248,247,.12); stroke: rgba(243,248,247,.5); stroke-width: 1.5; cursor: pointer; transition: fill .2s; }
.plan4 rect.on { fill: #D4B5B0; }
.plan4 text { fill: #F3FAF8; font-size: 9px; font-weight: 600; pointer-events: none; }
.plan4 figure { margin: 0; color: #F3FAF8; font-size: .76rem; }
.plan4 figure img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 10px; display: block; margin-bottom: 4px; }
/* 17 Klartext */
.letter { width: 100%; max-width: 400px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 14px 16px; font-size: .82rem; line-height: 1.5; }
.letter .sum { background: #F1E5E3; border-radius: 10px; padding: 8px 10px; margin-bottom: 8px; font-weight: 600; }
/* 18 Aushang */
.ag { width: 100%; max-width: 440px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(110px, 150px); gap: 12px; align-items: start; }
.ag label { display: grid; gap: 3px; font-size: .74rem; color: #F3FAF8; margin-bottom: 6px; }
.ag input { width: 100%; min-width: 0; border: 0; border-radius: 8px; padding: 7px 9px; font: 500 .82rem inherit; }
.a4 { aspect-ratio: 210 / 297; background: #fff; border-radius: 4px; padding: 12px 10px; color: #1E3B44; box-shadow: 0 10px 24px rgba(0,0,0,.35); display: grid; align-content: start; gap: 6px; text-align: center; overflow: hidden; }
.a4 .bunt { height: 12px; background: repeating-conic-gradient(from 0deg, transparent 0 0); }
.a4 h5 { margin: 4px 0 0; font-size: .95rem; line-height: 1.15; overflow-wrap: anywhere; }
.a4 .dt { font-weight: 700; font-size: .78rem; background: #D4B5B0; border-radius: 6px; padding: 3px; }
.a4 p { margin: 0; font-size: .6rem; }
/* 19 Daten-Wächter */
.guard { width: 100%; max-width: 420px; background: #142A31; color: #F3FAF8; border-radius: 14px; padding: 12px 14px; font: .74rem/1.6 ui-monospace, Menlo, monospace; }
.guard .ok { color: #7FD6A4; } .guard .warn { color: #F3C98B; } .guard .err { color: #F2A196; }
/* 20 Punktraster */
.dots { background: #0d0d0d; border-radius: 14px; padding: 14px; display: grid; gap: 10px; justify-items: center; }
.dots canvas { image-rendering: pixelated; }
.dots small { color: #bbb; font: .7rem ui-monospace, monospace; letter-spacing: .08em; }
/* 21 Gruppenfarben */
.gc { width: 270px; display: grid; gap: 6px; }
.gc div { display: flex; align-items: center; gap: 10px; background: #F3F8F7; color: #1E3B44; border-radius: 10px; padding: 8px 10px; font-size: .8rem; }
.gc i { width: 26px; height: 26px; border-radius: 8px; flex: none; display: grid; place-items: center; font-style: normal; font-size: .7rem; font-weight: 700; }
/* 22 Merkliste-Blatt */
.sheetdemo { width: 230px; height: 280px; border-radius: 26px; border: 6px solid #0E1E23; background: #A8C5C0; position: relative; overflow: hidden; display: grid; place-items: center; }
.sheet { position: absolute; left: 0; right: 0; bottom: 0; height: 190px; background: #F3F8F7; border-radius: 18px 18px 0 0; padding: 18px 14px 12px; translate: 0 100%; transition: translate .4s cubic-bezier(.32,.72,0,1); color: #1E3B44; font-size: .78rem; display: grid; gap: 6px; align-content: start; touch-action: none; }
.sheet::before { content: ""; position: absolute; top: 7px; left: 50%; width: 36px; height: 4px; margin-left: -18px; border-radius: 3px; background: rgba(30,59,68,.25); }
.sheetdemo.open .sheet { translate: 0 0; }
.sheet div { background: #2D6A6A; color: #F3FAF8; border-radius: 10px; padding: 8px 10px; }
/* 23 Was passiert jetzt */
.next3 { width: 270px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 14px; font-size: .8rem; display: grid; gap: 8px; }
.next3 ol { margin: 0; padding-left: 18px; display: grid; gap: 4px; }
/* 24 Morgen offen? */
.ask2 { width: 270px; display: grid; gap: 8px; }
.bubble { background: #F3F8F7; color: #1E3B44; border-radius: 14px; padding: 10px 12px; font-size: .82rem; min-height: 40px; }
'''.replace('EZ', EZ)

IMG = lambda n: f'img/{n}-800.webp'
def card(n, k, skill, title, text, where, stage):
    return f'''
    <article class="card" data-k="{k}">
      <div class="stage">{stage}</div>
      <div class="about"><div class="meta"><span class="skill">{skill}</span></div>
        <h2>{n} · {title}</h2><p>{text}</p><p class="where">{where}</p></div>
    </article>
'''
C = []
def add(*a): C.append(card(len(C) + 1, *a))

add('alltag', 'ui-ux-pro-max', 'Mein Tag: die Eltern-Übersicht', 'Für Eltern, deren Kind schon da ist, zeigt die Startseite oben eine kleine Übersicht: Ist heute offen und bis wann, die Durchwahl der eigenen Gruppe, der nächste Termin. Die Gruppe wählt man einmal, sie bleibt im eigenen Browser gespeichert.',
    'ui-ux-pro-max empfiehlt für Kitas ein „Parent Dashboard“. Alles kommt aus Daten, die die Seite schon hat.',
    '<div class="demo"><div class="ph5" id="d1"><div class="chips" data-g="d1"><button aria-pressed="false">Sonnen</button><button aria-pressed="true">Bienen</button><button aria-pressed="false">Hort</button></div><div class="tile"><b>Heute geöffnet</b>bis <span class="d1t">16:30</span> Uhr</div><div class="tile dk2"><b>Meine Gruppe: <span class="d1g">Bienengruppe</span></b><span class="small">anrufen: … <span class="d1n">13</span></span></div><div class="tile"><b>Nächster Termin</b>Nikolaus · 07.12.</div></div></div>')
add('alltag', 'impeccable critique', 'Krankmelden mit einem Tipp', 'Wer seine Gruppe einmal gewählt hat, sieht statt der Auswahlliste nur noch einen großen Knopf „Bienengruppe anrufen“ – und darunter die E-Mail. Morgens um sieben, eine Hand am Kind: ein Tipp statt vier.',
    'Die Frage aus der Critique: „Die eigene Gruppe merken, damit es mit einem Tipp geht.“',
    '<div class="demo"><div class="ph5"><div class="chips" data-g="d2"><button aria-pressed="false">Sterne</button><button aria-pressed="true">Spatzen</button><button aria-pressed="false">Bären</button></div><div class="bigcall"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg> <span class="d2g">Spatzengruppe</span> anrufen</div><div class="tile" style="text-align:center">E-Mail mit Vorlage</div></div></div>')
add('alltag', 'mobile-native', 'Kurzbefehle am App-Symbol', 'Wer die Seite als App aufs Handy gelegt hat, drückt lange auf das Symbol und bekommt direkt: „Kind krankmelden“, „Termine“, „Anrufen“. Das ist ein Eintrag in der App-Beschreibung, kein Programmieraufwand.',
    'Funktioniert auf Android und ab iOS 17 teilweise. Halten Sie das Symbol gedrückt.',
    '<div class="demo"><div class="homescreen" id="hs"><div class="qa"><div>Kind krankmelden</div><div>Termine</div><div>Anrufen</div></div><button class="appicon" type="button" aria-label="App-Symbol gedrückt halten"></button></div><p class="small" style="color:#F3FAF8">Symbol gedrückt halten</p></div>')
add('alltag', 'impeccable onboard', 'Neu seit Ihrem letzten Besuch', 'Die Seite merkt sich im eigenen Browser, wann man zuletzt da war. Termine und Elternbriefe, die seitdem dazugekommen sind, bekommen einen kleinen grünen Punkt.',
    'Kein Konto, keine Daten beim Hort – nur ein Datum im eigenen Browser.',
    '<div class="demo"><div class="newlist" id="nl"><div class="isnew"><i></i>Elternabend Kindergarten · 20.01.</div><div class="isnew"><i></i>Elternbrief „Fasching“</div><div><i></i>Nikolaus · 07.12.</div><div><i></i>Weihnachtsmarkt · 04.12.</div></div><button class="chip" id="nlb" type="button">Letzter Besuch: vor 2 Wochen</button></div>')
add('team', 'impeccable critique', 'Hinweise mit Ablaufdatum', 'Hinweis-Karten wie „Sankt Martin“ bekommen ein Datum, bis wann sie gelten. Danach verschwinden sie von selbst – keine veralteten Ankündigungen mehr, auch wenn niemand daran denkt.',
    'Aus der Critique: Die undatierte Karte „Sankt Martin“ wirkt im November schnell veraltet.',
    '<div class="demo"><div class="exp"><div class="tile" id="ex1"><b>Sankt Martin</b>gilt bis 11.11.</div><div class="tile" id="ex2"><b>Weihnachtsmarkt</b>gilt bis 04.12.</div><label style="color:#F3FAF8;font-size:.78rem">Heute: <b id="exd">01.11.</b><input type="range" id="exr" min="0" max="50" value="0" aria-label="Datum verschieben"></label></div></div>')
add('alltag', 'gestures', 'Termin zur Seite wischen = merken', 'Am Handy schiebt man einen Termin mit dem Finger nach rechts, darunter erscheint „Merken“. Ab der Hälfte rastet er ein, davor federt er zurück. Der Knopf „Merken“ bleibt für alle, die lieber tippen.',
    'Mit Gummiband an den Grenzen und Tastatur-Alternative.',
    '<div class="demo"><div class="swrow"><div class="under">Merken</div><div class="front" id="sw">Elternabend Kindergarten · 20.01.</div></div><p class="small" style="color:#F3FAF8">Nach rechts ziehen</p></div>')
add('alltag', 'dataviz', 'Betreuungszeiten als Tagesbalken', 'Statt Uhrzeiten im Text: ein Balken je Bereich von 6:45 bis 18:00, der Spätdienst heller, dazu eine grüne Linie für „jetzt“. Man sieht auf einen Blick, wer wann betreut wird.',
    'Nach den dataviz-Regeln: eine Farbe für Betreuung, eine Abstufung für Spätdienst, Text statt Legende.',
    '<div class="demo"><div class="dayb" id="db"><div class="row"><span>Krippe</span><div class="bar"><span style="left:0;width:86.7%"></span><span class="late" style="left:86.7%;width:8.9%"></span><i class="now"></i></div></div><div class="row"><span>Kindergarten</span><div class="bar"><span style="left:0;width:86.7%"></span><span class="late" style="left:86.7%;width:8.9%"></span><i class="now"></i></div></div><div class="row"><span>Hort</span><div class="bar"><span style="left:0;width:100%"></span><i class="now"></i></div></div><div class="axis"><span>6:45</span><span>12:00</span><span>18:00</span></div></div></div>')
add('gestalt', 'impeccable delight', 'Ferien-Countdown als Wimpelkette', 'Je näher die nächsten Schließtage rücken, desto mehr Wimpel einer kleinen Kette färben sich ein. Ist die Kette voll, ist Ferienbeginn. Passt zum Leitbild „Die Wimpelkette“.',
    'Ein kleines Detail im Kita-Jahr-Zeitstrahl.',
    '<div class="demo"><div class="wc"><svg viewBox="0 0 300 70" id="wcs"></svg><span id="wct">noch 38 Tage bis Weihnachten</span><input type="range" id="wcr" min="0" max="40" value="2" aria-label="Tage verschieben" style="width:220px;accent-color:#D4B5B0"></div></div>')
add('gestalt', 'remove-animations', 'Ruhige Ansicht zum Einschalten', 'Ein kleiner Schalter im Fußbereich: „Bewegung aus“. Für alle, denen die Seite zu lebendig ist, ohne dass sie die Einstellung ihres Handys kennen müssen. Gemerkt im eigenen Browser.',
    'remove-animations: weniger ist für manche Menschen mehr.',
    '<div class="demo"><div class="calm" id="cm"><div class="ball"></div><button class="switch" id="cms" role="switch" aria-checked="false" type="button"><i></i>Bewegung aus</button></div></div>')
add('gestalt', 'web-design-guidelines', 'Tastatur-Hilfe mit „?“', 'Wer am Computer „?“ drückt, sieht alle Kürzel: Strg K für die Suche, Pfeiltasten in der Bildansicht, Esc zum Schließen. Hilft Menschen, die ohne Maus arbeiten.',
    'Richtlinie: Tastaturbedienung sichtbar machen.',
    '<div class="demo"><div class="keys"><div>Suche öffnen<kbd>Strg K</kbd></div><div>Bild weiter<kbd>→</kbd></div><div>Schließen<kbd>Esc</kbd></div><div>Diese Hilfe<kbd>?</kbd></div></div></div>')
add('gestalt', 'choreograph', 'Der Auftakt als eine Bewegung', 'Beim ersten Besuch erscheint die Startseite in einer einzigen, ruhigen Abfolge: erst der Name, dann fallen drei Fotos wie Polaroids auf den Tisch, zuletzt „Jetzt geöffnet“. Statt vieler einzelner Effekte eine Choreografie.',
    'choreograph: eine Bewegung pro Bereich, ungleichmäßige Abstände.',
    f'<div class="demo"><div class="hero4" id="h4"><div><h4>Kath. Kinder- und Jugendhort Grombühl</h4><div class="st">● Jetzt geöffnet</div></div><div class="pola"><img src="{IMG("p2160110")}" alt=""><img src="{IMG("kreatviraum-5-1")}" alt=""><img src="{IMG("turnraum")}" alt=""></div></div><button class="chip" id="h4b" type="button">Abspielen</button></div>')
add('neu', 'explainer-default', 'Ein Tag bei uns – Film in 60 Sekunden', 'Ein kurzer, stiller Film aus euren eigenen Fotos: Ankommen, Spielen, Mittagessen, Garten, Abholen – mit kurzen Texten und leiser Musik. Läuft nur auf Tipp, mit Untertiteln.',
    'Die Explainer-Skills bauen solche Filme aus Code und echten Fotos; hier ein Entwurf als Bildfolge.',
    f'<div class="demo"><div class="film" id="fm"><img class="on" src="{IMG("p2160110")}" alt=""><img src="{IMG("lesecke")}" alt=""><img src="{IMG("turnraum")}" alt=""><img src="{IMG("werkraum")}" alt=""><span class="cap">Ankommen</span><span class="prog"></span></div><button class="chip" id="fmb" type="button">Film abspielen</button></div>')
add('neu', 'landing-page-design', 'In 3 Schritten zum Platz – schon auf der Startseite', 'Für neue Eltern ein klarer Weg direkt auf der Startseite: Anfragen, Kennenlernen, Zusage. Jeder Schritt mit einem Satz, der erste mit Knopf.',
    'Die Startseite überzeugt schon; so wird aus Interesse ein nächster Schritt.',
    '<div class="demo"><div class="steps3"><div><b>Anfragen</b>Vorbereitete E-Mail</div><div><b>Kennenlernen</b>Haus ansehen</div><div><b>Zusage</b>Wir melden uns</div></div></div>')
add('neu', 'ui-ux-pro-max', 'Gute Gründe auf einen Blick', 'Eine schmale Leiste mit Belegen statt Behauptungen: 100 % Fachkräfte im Hort, Elternnote 1,4, eigene Küche, bis 18 Uhr offen. Gerade für Eltern, die Kitas vergleichen.',
    'ui-ux-pro-max: Für Kitas zählen Vertrauen und Belege. Alle Zahlen stehen schon auf der Seite.',
    '<div class="demo"><div class="proof"><div><b>100 %</b>Fachkräfte im Hort</div><div><b>1,4</b>Note in der Elternbefragung</div><div><b>2</b>Köchinnen, täglich frisch</div><div><b>18:00</b>Hort auch in den Ferien</div></div></div>')
add('neu', 'impeccable onboard', '„Ich bin neu hier“ oder „Mein Kind ist schon da“', 'Ganz oben eine kleine Weiche. Wer neu ist, sieht zuerst Bereiche, Rundgang und Anmeldung. Wer schon da ist, sieht Öffnungszeit, Krankmelden und Termine. Die Wahl bleibt gespeichert und lässt sich jederzeit ändern.',
    'Zwei Besuchergruppen mit ganz verschiedenen Fragen – eine Seite.',
    '<div class="demo"><div class="fork"><div class="chips" data-g="d15"><button aria-pressed="true">Ich bin neu hier</button><button aria-pressed="false">Mein Kind ist schon da</button></div><div class="tile d15a"><b>Unsere Bereiche</b>Krippe · Kindergarten · Hort</div><div class="tile d15b"><b>Platz anfragen</b>in 3 Schritten</div></div></div>')
add('neu', 'impeccable overdrive', 'Hauskarte zum Antippen', 'Ein einfacher Grundriss des Hauses: Räume antippen, Foto und zwei Sätze erscheinen. Ein zweiter Weg in den Rundgang – besonders für Eltern, die sich orientieren wollen.',
    'Klare Formen statt Zeichnung – ein Plan, kein Bild.',
    f'<div class="demo"><div class="plan4"><svg viewBox="0 0 220 150" id="hk"><rect x="5" y="5" width="100" height="65" rx="6" data-i="0" class="on"/><text x="14" y="22">Gruppenraum</text><rect x="110" y="5" width="105" height="65" rx="6" data-i="1"/><text x="119" y="22">Turnraum</text><rect x="5" y="75" width="70" height="70" rx="6" data-i="2"/><text x="14" y="92">Lesen</text><rect x="80" y="75" width="135" height="70" rx="6" data-i="3"/><text x="89" y="92">Werkraum</text></svg><figure><img id="hki" src="{IMG("p2160110")}" alt=""><span id="hkt">Gruppenraum: hell, mit Bauecke</span></figure></div></div>')
add('alltag', 'humanizer', 'Elternbriefe zuerst in zwei Sätzen', 'Jeder Elternbrief beginnt mit „Das Wichtigste“: zwei Sätze in Alltagssprache. Der ausführliche Text folgt darunter – so lesen Eltern am Handy das Entscheidende, ohne durch Paragrafen zu scrollen.',
    'humanizer: Amtsdeutsch in klare Sätze, ohne den Inhalt zu ändern.',
    '<div class="demo"><div class="letter"><div class="sum">Das Wichtigste: Wir haben höchstens 30 Tage im Jahr zu. In offenen Ferienwochen sind nicht alle Erzieherinnen da.</div>Nach dem BayKiBiG (Bayerisches Kinderbildungs- und Betreuungsgesetz) dürfen Kitas in Bayern an 30 Tagen im Jahr schließen …</div></div>')
add('team', 'figma-designer', 'Aushang-Generator für das Team', 'Termin eintragen, und die Seite setzt daraus einen druckfertigen A4-Aushang im Stil der Webseite: Wimpel oben, Titel, Datum, kurzer Text. Für die Pinnwand im Eingang.',
    'Gleiche Schrift, Farben und Abstände wie die Seite – nach dem Vorbild eines Design-Systems.',
    '<div class="demo"><div class="ag"><div><label>Titel<input id="agt" value="Laternenfest"></label><label>Datum<input id="agd" value="11.11., 17 Uhr"></label><label>Text<input id="agx" value="Treffpunkt im Garten"></label></div><div class="a4"><svg viewBox="0 0 120 14" style="width:100%"><path d="M0 2 Q60 10 120 2" fill="none" stroke="#D4B5B0"/><path d="M10 4l8 1-4 7z M34 6l8 1-4 7z M58 7l8 0-4 7z M82 6l8-1-3 7z M104 4l8-1-3 7z" fill="#A8C5C0"/></svg><h5 id="agT">Laternenfest</h5><div class="dt" id="agD">11.11., 17 Uhr</div><p id="agX">Treffpunkt im Garten</p><p style="margin-top:auto;opacity:.6">Kath. Kinder- und Jugendhort Grombühl</p></div></div></div>')
add('team', 'break-ui', 'Daten-Wächter für die Tabellen', 'Beim Bauen der Seite prüft ein kleiner Wächter die Tabellen und sagt in Klartext, was nicht stimmt: Ende vor Anfang, Datum schon vorbei, doppelter Name, fehlendes Feld. Damit kein Tippfehler auf der Seite landet.',
    'Aus dem Stresstest: Eine leere Tabelle hat den ganzen Bau gestoppt.',
    '<div class="demo"><div class="guard"><div class="ok">✓ termine.csv: 5 Termine</div><div class="warn">! termine.csv Zeile 4: „Sankt Martin“ liegt in der Vergangenheit</div><div class="err">✗ schliesstage.csv Zeile 3: Ende (03.11.) vor Anfang (05.11.)</div><div class="warn">! schliesstage.csv: Summe 31 Schließtage (erlaubt 30)</div><div class="ok">✓ elternbriefe.csv: 1 Brief</div></div></div>')
add('gestalt', 'nothing-design', 'Anzeigetafel im Punktraster', 'Eine kleine Anzeige in Punktschrift, wie an einer Bushaltestelle: „OFFEN BIS 18:00“ – etwa im Fußbereich oder im App-Symbol. Ein Gegenpol zur weichen Gestaltung, nur als kleines Detail.',
    'nothing-design: Punktmatrix, Schwarz und Weiß, sehr reduziert.',
    '<div class="demo"><div class="dots"><canvas id="dm" width="220" height="40" aria-label="OFFEN BIS 18:00"></canvas><small>KITA GROMBÜHL · HEUTE</small></div></div>')
add('alltag', 'ui-ux-pro-max', 'Gruppen erkennt man an ihrem Zeichen', 'Termine, Durchwahlen und Hinweise für eine bestimmte Gruppe tragen deren Symbol: Sonne, Stern, Bär, Biene, Spatz. Eltern sehen sofort, was ihr Kind betrifft – Kinder erkennen ihre Gruppe auch.',
    'ui-ux-pro-max: Farbzuordnung je Familienmitglied; hier je Gruppe, in Tönen der Seite.',
    '<div class="demo"><div class="gc"><div><i style="background:#F3E9C9"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/></svg></i>Sonnengruppe · Ausflug 12.12.</div><div><i style="background:#E6EFED"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg></i>Sternengruppe · …15</div><div><i style="background:#F1E5E3"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="14.5" rx="5" ry="6"/><path d="M7.4 12.5h9.2M7.4 16.5h9.2"/></svg></i>Bienengruppe · Elternabend</div></div></div>')
add('alltag', 'apple-design', 'Merkliste als Blatt von unten', 'Wer Termine gemerkt hat, tippt auf „2 gemerkt“ und ein Blatt gleitet von unten herein – mit den Terminen und „Alle in den Kalender“. Mit dem Finger nach unten zieht man es wieder weg, wie in einer App.',
    'apple-design: Blätter mit Federkurve, folgen dem Finger.',
    '<div class="demo"><div class="sheetdemo" id="sd"><button class="chip" id="sdb" type="button">2 gemerkt</button><div class="sheet" id="sh"><b>Gemerkte Termine</b><div>Nikolaus · 07.12.</div><div>Elternabend · 20.01.</div><span class="small">Nach unten ziehen zum Schließen</span></div></div></div>')
add('neu', 'impeccable clarify', '„Was passiert jetzt?“ nach der Anfrage', 'Nach „Platz anfragen“ erscheint ein kurzer Hinweis: die E-Mail ist vorbereitet, Sie schicken sie ab, wir melden uns. Neue Eltern wissen, dass ihre Anfrage nicht im Leeren landet.',
    'Wie schnell der Hort antwortet, trägt er selbst ein.',
    '<div class="demo"><div class="next3"><b>So geht es weiter</b><ol><li>Ihr E-Mail-Programm öffnet die Vorlage.</li><li>Sie ergänzen und senden sie ab.</li><li>Wir melden uns bei Ihnen.</li></ol></div></div>')
add('alltag', 'impeccable clarify', '„Ist morgen offen?“ – eine Frage, eine Antwort', 'Unter „Jetzt geöffnet“ drei kleine Fragen zum Antippen: Morgen? Nächste Woche? In den Ferien? Die Antwort kommt sofort aus dem Ferienplan, in einem Satz.',
    'Nutzt die Daten, die die Seite schon hat.',
    '<div class="demo"><div class="ask2"><div class="chips" id="aq"><button data-a="Ja, morgen (Dienstag) haben wir ganz normal geöffnet." aria-pressed="false">Morgen?</button><button data-a="Ja, die ganze nächste Woche ist offen." aria-pressed="false">Nächste Woche?</button><button data-a="Zu von 24.12. bis 08.01. – ab 11.01. wieder offen." aria-pressed="false">Weihnachten?</button></div><div class="bubble" id="aqa" aria-live="polite">Tippen Sie eine Frage an.</div></div></div>')

JS = r'''
  /* Gruppenwahl in den Demos */
  var GR = { "Sonnen": ["Sonnengruppe", "14", "16:30"], "Bienen": ["Bienengruppe", "13", "16:30"], "Hort": ["Kinderhort", "0", "18:00"], "Sterne": ["Sternengruppe"], "Spatzen": ["Spatzengruppe"], "Bären": ["Bärengruppe"] };
  $$(".chips[data-g]").forEach(function (g) {
    var id = g.dataset.g;
    g.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("button", g).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      var v = GR[b.textContent];
      if (id === "d1") { $(".d1g").textContent = v[0]; $(".d1n").textContent = v[1]; $(".d1t").textContent = v[2]; }
      if (id === "d2") { $(".d2g").textContent = v[0]; }
      if (id === "d15") { var neu = b.textContent.indexOf("neu") > 0; $(".d15a").innerHTML = neu ? "<b>Unsere Bereiche</b>Krippe · Kindergarten · Hort" : "<b>Heute geöffnet</b>bis 16:30 Uhr"; $(".d15b").innerHTML = neu ? "<b>Platz anfragen</b>in 3 Schritten" : "<b>Kind krankmelden</b>Gruppe anrufen"; }
    });
  });
  /* 3 Kurzbefehle: gedrückt halten */
  (function () { var hs = $("#hs"), t; var ic = $(".appicon", hs);
    function down() { t = setTimeout(function () { hs.classList.add("hold"); }, 400); }
    function up() { clearTimeout(t); }
    ic.addEventListener("pointerdown", down); ic.addEventListener("pointerup", up); ic.addEventListener("pointerleave", up);
    ic.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); hs.classList.toggle("hold"); } });
    document.addEventListener("pointerdown", function (e) { if (!hs.contains(e.target)) hs.classList.remove("hold"); });
  })();
  /* 4 letzter Besuch */
  (function () { var b = $("#nlb"), rows = $$("#nl div"), s = 0, T = ["vor 2 Wochen", "gestern", "vor 2 Monaten"], N = [2, 0, 4];
    b.addEventListener("click", function () { s = (s + 1) % 3; b.textContent = "Letzter Besuch: " + T[s]; rows.forEach(function (r, i) { r.classList.toggle("isnew", i < N[s]); }); }); })();
  /* 5 Ablaufdatum */
  (function () { var r = $("#exr"); function upd() { var d = new Date(2026, 10, 1 + +r.value); $("#exd").textContent = String(d.getDate()).padStart(2, "0") + "." + String(d.getMonth() + 1).padStart(2, "0") + "."; $("#ex1").classList.toggle("gone", d > new Date(2026, 10, 11)); $("#ex2").classList.toggle("gone", d > new Date(2026, 11, 4)); } r.addEventListener("input", upd); upd(); })();
  /* 6 Wischen mit Gummiband */
  (function () { var f = $("#sw"), w = f.parentNode, x0 = null, dx = 0, W;
    function rb(x, d) { return (1 - 1 / (x * .55 / d + 1)) * d; }
    f.addEventListener("pointerdown", function (e) { x0 = e.clientX; W = w.offsetWidth; f.setPointerCapture(e.pointerId); f.style.transition = "none"; });
    f.addEventListener("pointermove", function (e) { if (x0 === null) return; dx = e.clientX - x0; var x = dx < 0 ? -rb(-dx, 30) : dx > W * .7 ? W * .7 + rb(dx - W * .7, 40) : dx; f.style.translate = x + "px 0"; });
    function end() { if (x0 === null) return; x0 = null; f.style.transition = "translate .35s cubic-bezier(.23,1,.32,1)"; f.style.translate = "0 0"; if (dx > W * .45) f.classList.toggle("saved"); dx = 0; }
    f.addEventListener("pointerup", end); f.addEventListener("pointercancel", end);
    f.tabIndex = 0; f.addEventListener("keydown", function (e) { if (e.key === "Enter") f.classList.toggle("saved"); });
  })();
  /* 7 jetzt-Linie */
  (function () { var n = new Date(), m = n.getHours() * 60 + n.getMinutes(), p = Math.max(0, Math.min(1, (m - 405) / (1080 - 405))); $$("#db .now").forEach(function (l) { l.style.left = (p * 100) + "%"; }); })();
  /* 8 Wimpel-Countdown */
  (function () { var s = $("#wcs"), n = 12, h = "";
    for (var i = 0; i < n; i++) { var x0 = 10 + i * 24, y0 = 8 + 18 * Math.sin(Math.PI * i / (n - 1)) * .9, x1 = x0 + 18, y1 = 8 + 18 * Math.sin(Math.PI * (i + .75) / (n - 1)) * .9; h += '<path class="f' + (i % 2 ? " x" : "") + '" d="M' + x0 + " " + y0 + " L" + x1 + " " + y1 + " L" + ((x0 + x1) / 2) + " " + ((y0 + y1) / 2 + 26) + 'Z"/>'; }
    s.innerHTML = '<path d="M4 8 Q150 50 296 8" fill="none" stroke="rgba(243,248,247,.5)"/>' + h;
    var fl = $$(".f", s), r = $("#wcr");
    function upd() { var left = 40 - +r.value, k = Math.round((1 - left / 40) * n); fl.forEach(function (f, i) { f.classList.toggle("on", i < k); }); $("#wct").textContent = left ? "noch " + left + (left === 1 ? " Tag" : " Tage") + " bis Weihnachten" : "Ferienbeginn!"; }
    r.addEventListener("input", upd); upd(); })();
  /* 9 Ruhige Ansicht */
  $("#cms").addEventListener("click", function () { var on = this.getAttribute("aria-checked") !== "true"; this.setAttribute("aria-checked", on); $("#cm").classList.toggle("off", on); });
  /* 11 Auftakt */
  function h4play() { var h = $("#h4"); if (reduced) return;
    $("h4", h).animate([{ opacity: 0, transform: "translateY(10px)" }, { opacity: 1, transform: "none" }], { duration: 420, easing: "cubic-bezier(.23,1,.32,1)", fill: "both" });
    $$(".pola img", h).forEach(function (im, i) { im.animate([{ opacity: 0, transform: "translateY(-30px) scale(1.15)" }, { opacity: 1, transform: "none" }], { duration: 480, delay: 260 + [0, 70, 160][i], easing: "cubic-bezier(.23,1,.32,1)", fill: "both" }); });
    $(".st", h).animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, delay: 820, fill: "both" }); }
  $("#h4b").addEventListener("click", h4play);
  /* 12 Film */
  (function () { var f = $("#fm"), ims = $$("img", f), cap = $(".cap", f), pr = $(".prog", f), C = ["Ankommen", "Lesen & Ausruhen", "Toben im Turnraum", "Werken"], t = null;
    $("#fmb").addEventListener("click", function () { clearInterval(t); var i = 0; function go() { ims.forEach(function (im, j) { im.classList.toggle("on", j === i); }); cap.textContent = C[i]; pr.style.transition = "none"; pr.style.width = (i / 4 * 100) + "%"; void pr.offsetWidth; pr.style.transition = "width 2.4s linear"; pr.style.width = ((i + 1) / 4 * 100) + "%"; i++; if (i >= 4) clearInterval(t); } go(); t = setInterval(go, 2400); }); })();
  /* 16 Hauskarte */
  (function () { var P = [["p2160110", "Gruppenraum: hell, mit Bauecke"], ["turnraum", "Turnraum: Bewegung bei jedem Wetter"], ["lesecke", "Leseecke: Ruhe und Bücher"], ["werkraum", "Werkraum: Holz, Kleber, Ideen"]];
    $$("#hk rect").forEach(function (r) { r.addEventListener("click", function () { $$("#hk rect").forEach(function (x) { x.classList.toggle("on", x === r); }); var p = P[+r.dataset.i]; $("#hki").src = "img/" + p[0] + "-800.webp"; $("#hkt").textContent = p[1]; }); }); })();
  /* 18 Aushang */
  [["agt", "agT"], ["agd", "agD"], ["agx", "agX"]].forEach(function (p) { $("#" + p[0]).addEventListener("input", function () { $("#" + p[1]).textContent = this.value; }); });
  /* 20 Punktraster */
  (function () { var c = $("#dm"), x = c.getContext("2d"), txt = "OFFEN BIS 18:00", g = document.createElement("canvas"); g.width = 110; g.height = 12; var gx = g.getContext("2d");
    gx.fillStyle = "#fff"; gx.font = "bold 10px monospace"; gx.textBaseline = "top"; gx.fillText(txt, 1, 1); var d = gx.getImageData(0, 0, 110, 12).data;
    x.fillStyle = "#0d0d0d"; x.fillRect(0, 0, 220, 40);
    for (var yy = 0; yy < 12; yy++) for (var xx = 0; xx < 110; xx++) { var on = d[(yy * 110 + xx) * 4 + 3] > 120; x.fillStyle = on ? "#f2f2f2" : "#222"; x.beginPath(); x.arc(xx * 2 + 1, yy * 3 + 3, on ? .9 : .5, 0, 7); x.fill(); } })();
  /* 22 Blatt von unten */
  (function () { var sd = $("#sd"), sh = $("#sh"), y0 = null;
    $("#sdb").addEventListener("click", function () { sd.classList.add("open"); });
    sh.addEventListener("pointerdown", function (e) { y0 = e.clientY; sh.setPointerCapture(e.pointerId); sh.style.transition = "none"; });
    sh.addEventListener("pointermove", function (e) { if (y0 === null) return; var dy = e.clientY - y0; sh.style.translate = "0 " + (dy > 0 ? dy : -(1 - 1 / (-dy * .55 / 20 + 1)) * 20) + "px"; });
    function end(e) { if (y0 === null) return; var dy = e.clientY - y0; y0 = null; sh.style.transition = ""; sh.style.translate = ""; if (dy > 60) sd.classList.remove("open"); }
    sh.addEventListener("pointerup", end); sh.addEventListener("pointercancel", end);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") sd.classList.remove("open"); });
  })();
  /* 24 Fragen */
  $("#aq").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#aq button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); $("#aqa").textContent = b.dataset.a; });
'''

out = (head + CSS + vote_css + '''</style>

<div class="wrap">
  <header class="intro">
    <span class="kicker">Ideen 4</span>
    <h1>Neue Ideen aus allen Skills</h1>
    <p>Jede Idee stammt aus einem der installierten Skills – das kleine Etikett zeigt, aus welchem. Die Beispiele lassen sich anfassen: tippen, ziehen, schieben. Darunter wie gewohnt <b>Ja</b>, <b>Merken</b> oder <b>Nein</b> und eine Anmerkung.</p>
  </header>
  <p class="sync-note">Ihre Auswahl wird gespeichert, und Claude kann sie direkt lesen.</p>

  <div class="filter" role="group" aria-label="Ideen filtern">
    <span class="knob" aria-hidden="true"></span>
    <button type="button" data-f="alle" aria-pressed="true">Alle</button>
    <button type="button" data-f="alltag" aria-pressed="false">Für Eltern im Alltag</button>
    <button type="button" data-f="neu" aria-pressed="false">Für neue Eltern</button>
    <button type="button" data-f="gestalt" aria-pressed="false">Gestaltung</button>
    <button type="button" data-f="team" aria-pressed="false">Für das Team</button>
    <button type="button" data-f="offen" aria-pressed="false">Noch offen</button>
  </div>

  <div class="grid">
''' + "".join(C) + '''  </div>
  <p class="foot">Alle Beispiele beachten „Bewegung reduzieren“. Nichts davon ist schon auf der Seite – sag einfach, welche Ideen eingebaut werden sollen.</p>
</div>

''' + helpers + JS + '\n' + vote_js + '})();\n</script>\n')

out = re.sub(r'(<div class="about"><div class="meta">.*?</div>\s*<h2>)(\d+) · ', lambda m: m.group(1) + '<span class="num">' + m.group(2) + '</span> ', out, flags=re.S)
assert out.count('class="num"') == len(C), out.count('class="num"')
open(D + 'ideen-4.html', 'w', encoding='utf-8').write(out)
print('ok', len(C), 'Ideen', len(out))
