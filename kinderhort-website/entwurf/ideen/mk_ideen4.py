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

/* 25 Sprachen */
.lang { width: 280px; display: grid; gap: 8px; }
.lang .tile { min-height: 64px; }
/* 26 Vorlesen */
.read { width: 290px; display: grid; gap: 10px; }
.read .tile mark { background: #F1E5E3; border-radius: 4px; }
/* 27 Schrift */
.fz { width: 290px; display: grid; gap: 10px; }
.fz .tile { transition: font-size .2s; }
/* 28 Speiseplan */
.menu { width: 290px; display: grid; gap: 8px; }
.menu .tile { min-height: 70px; }
/* 29 Fundsachen */
.lost { width: 100%; max-width: 380px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.lost div { background: #F3F8F7; color: #1E3B44; border-radius: 12px; padding: 8px; font-size: .72rem; text-align: center; }
.lost i { display: block; height: 54px; border-radius: 8px; margin-bottom: 6px; background: linear-gradient(135deg, #D4B5B0, #A8C5C0); }
.lost div:nth-child(2) i { background: linear-gradient(135deg, #2D6A6A, #A8C5C0); } .lost div:nth-child(3) i { background: linear-gradient(135deg, #F3E9C9, #D4B5B0); }
/* 30 Packliste */
.pack { width: 280px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 12px 14px; font-size: .82rem; display: grid; gap: 6px; }
.pack label { display: flex; gap: 8px; align-items: center; cursor: pointer; }
.pack input { accent-color: #2D6A6A; width: 18px; height: 18px; }
.pack .pb { height: 6px; border-radius: 3px; background: rgba(30,59,68,.12); overflow: hidden; }
.pack .pb span { display: block; height: 100%; width: 0; background: #7FD6A4; transition: width .3s EZ; }
/* 31 Erster Tag */
.first { width: 290px; display: grid; gap: 8px; color: #F3F8F7; text-align: center; }
.first b { font-size: 2rem; color: #D4B5B0; font-variant-numeric: tabular-nums; }
/* 32 Abholzeit */
.calc { width: 290px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 14px; font-size: .82rem; display: grid; gap: 8px; }
.calc input { width: 100%; accent-color: #2D6A6A; }
.calc .res { font-size: 1.1rem; font-weight: 700; }
/* 33 Erinnerung */
.remind { width: 290px; display: grid; gap: 10px; justify-items: center; }
.notif { width: 100%; background: rgba(243,248,247,.95); color: #1E3B44; border-radius: 16px; padding: 10px 12px; font-size: .78rem; box-shadow: 0 10px 24px rgba(0,0,0,.3); opacity: 0; translate: 0 -10px; transition: opacity .3s EZ, translate .3s EZ; }
.notif.on { opacity: 1; translate: 0 0; }
.notif b { display: block; }
/* 34 Kunstwerke */
.art { width: 100%; max-width: 380px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.art div { background: #fff; padding: 6px 6px 18px; border-radius: 3px; box-shadow: 0 6px 14px rgba(0,0,0,.3); rotate: -2deg; }
.art div:nth-child(2) { rotate: 2deg; } .art div:nth-child(3) { rotate: -1deg; }
.art svg { width: 100%; aspect-ratio: 1; display: block; background: #FBF7EF; }
/* 35 Rückmeldung Elternabend */
.rsvp { width: 290px; display: grid; gap: 8px; }
.mailprev { background: #fff; color: #1E3B44; border-radius: 12px; padding: 10px 12px; font: .74rem/1.5 ui-monospace, Menlo, monospace; min-height: 70px; }
/* 36 Lesezeit */
.rt { width: 290px; display: grid; gap: 6px; }
.rt .tile small { display: inline-block; margin-left: 6px; padding: 1px 7px; border-radius: 6px; background: #E6EFED; font-size: .7rem; }
/* 37 Vibration */
.vib { display: grid; justify-items: center; gap: 10px; color: #F3F8F7; }
.vib button { border: 0; border-radius: 14px; padding: 12px 22px; background: #D4B5B0; color: #1E3B44; font-weight: 700; cursor: pointer; }
.vib button.pulse { animation: vib .3s linear; }
@keyframes vib { 20%, 60% { translate: -2px 0; } 40%, 80% { translate: 2px 0; } }
/* 38 Leichte Sprache */
.easy { width: 300px; display: grid; gap: 8px; }
/* 39 ABC-Karten */
.abc { position: relative; width: 240px; height: 150px; }
.abc .k { position: absolute; inset: 0; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 14px 16px; box-shadow: 0 10px 20px rgba(0,0,0,.25); font-size: .8rem; touch-action: pan-y; cursor: grab; user-select: none; }
.abc .k b { display: block; font-size: 1.6rem; color: #2D6A6A; }
.abc .k:nth-child(2) { rotate: 3deg; translate: 0 4px; } .abc .k:nth-child(3) { rotate: -3deg; translate: 0 8px; }
/* 40 Kühlschrank-Zettel */
.fridge { width: 200px; aspect-ratio: 210 / 297; background: #fff; color: #1E3B44; border-radius: 4px; padding: 10px; box-shadow: 0 10px 24px rgba(0,0,0,.35); font-size: .56rem; display: grid; gap: 4px; align-content: start; position: relative; }
.fridge::before { content: ""; position: absolute; top: -8px; left: 50%; width: 22px; height: 22px; margin-left: -11px; border-radius: 50%; background: #D4B5B0; box-shadow: 0 3px 6px rgba(0,0,0,.3); }
.fridge h6 { margin: 6px 0 2px; font-size: .78rem; }
.fridge div { display: flex; justify-content: space-between; border-bottom: 1px solid rgba(30,59,68,.12); padding: 2px 0; }

/* 41 Suche antwortet */
.srch { width: 300px; background: #142A31; color: #F3FAF8; border-radius: 16px; padding: 10px; display: grid; gap: 8px; font-size: .8rem; }
.srch .in { background: rgba(243,248,247,.1); border-radius: 10px; padding: 9px 12px; }
.srch .ans { background: #F3F8F7; color: #1E3B44; border-radius: 10px; padding: 9px 12px; }
.srch .hit { padding: 6px 12px; opacity: .85; }
/* 42 Jetzt im Tagesablauf */
.tl4 { width: 290px; display: grid; gap: 6px; }
.tl4 div { display: grid; grid-template-columns: 52px 1fr; gap: 10px; align-items: center; padding: 7px 10px; border-radius: 10px; background: rgba(243,248,247,.08); color: #F3FAF8; font-size: .8rem; transition: background .3s EZ; }
.tl4 time { font-variant-numeric: tabular-nums; opacity: .8; }
.tl4 div.now { background: #D4B5B0; color: #1E3B44; font-weight: 700; }
.tl4 div.now time { opacity: 1; }
/* 43 Bringzeit */
.bz { width: 290px; display: grid; gap: 8px; }
.bz .tile b { display: flex; align-items: center; gap: 8px; }
.bz i { width: 10px; height: 10px; border-radius: 50%; background: #7FD6A4; display: inline-block; }
/* 44/45 Filter nach Bereich */
.evf { width: 300px; display: grid; gap: 6px; }
.evf .tile { display: flex; justify-content: space-between; gap: 8px; }
.evf .tile span { font-size: .7rem; padding: 1px 7px; border-radius: 6px; background: #E6EFED; align-self: center; }
/* 46 Feiertage im Kalender */
.mcal { width: 280px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 12px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; font-size: .74rem; text-align: center; }
.mcal b { font-size: .66rem; opacity: .6; }
.mcal span { aspect-ratio: 1; display: grid; place-items: center; border-radius: 8px; font-weight: 600; }
.mcal .zu { background: #F1E5E3; } .mcal .fe { background: #F6D9D3; color: #7E3B31; box-shadow: inset 0 0 0 1.5px #B8574A; } .mcal .ev { background: #1E3B44; color: #F3F8F7; }
.mleg { grid-column: 1 / -1; display: flex; gap: 10px; justify-content: center; font-size: .68rem; margin-top: 4px; }
/* 47 Brief teilen */
.bshare { width: 290px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 12px 14px; font-size: .8rem; display: grid; gap: 8px; }
.bshare .row { display: flex; gap: 6px; }
.bshare .row span { padding: 6px 10px; border-radius: 9px; background: #E6EFED; font-weight: 600; font-size: .74rem; }
/* 48 Vollmacht */
.voll { width: 290px; background: #fff; color: #1E3B44; border-radius: 12px; padding: 12px 14px; font: .74rem/1.55 ui-monospace, Menlo, monospace; box-shadow: 0 10px 22px rgba(0,0,0,.3); }
/* 49 Kontakt-Karte */
.vcard { width: 260px; background: #F3F8F7; color: #1E3B44; border-radius: 18px; padding: 14px; display: grid; justify-items: center; gap: 6px; font-size: .8rem; text-align: center; }
.vcard .av { width: 56px; height: 56px; border-radius: 50%; background: #E6EFED; display: grid; place-items: center; }
/* 50 Eilmeldung */
.alarm { width: 100%; max-width: 420px; display: grid; gap: 10px; }
.alarm .bar { background: #B8574A; color: #fff; border-radius: 12px; padding: 10px 14px; font-size: .82rem; font-weight: 600; display: flex; gap: 10px; align-items: center; }
.alarm .bar i { width: 10px; height: 10px; border-radius: 50%; background: #fff; flex: none; }
.alarm .page { background: rgba(243,248,247,.1); border-radius: 12px; height: 70px; }
/* 51 Alle Fragen */
.allq { width: 300px; display: grid; gap: 6px; }
/* 52 Team */
.team { width: 100%; max-width: 400px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.team div { background: #F3F8F7; color: #1E3B44; border-radius: 14px; padding: 10px; text-align: center; font-size: .72rem; }
.team .ph { width: 52px; height: 52px; border-radius: 50%; margin: 0 auto 6px; background: #D4B5B0; display: grid; place-items: center; font-weight: 700; font-size: .9rem; }
/* 53 Eingang finden */
.door { width: 100%; max-width: 380px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; color: #F3FAF8; font-size: .76rem; }
.door figure { margin: 0; } .door img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 10px; display: block; margin-bottom: 4px; }
.door b { color: #D4B5B0; }
/* 54 Meinten Sie */
.mean { width: 290px; background: #142A31; color: #F3FAF8; border-radius: 16px; padding: 10px; display: grid; gap: 8px; font-size: .8rem; }
.mean .in { background: rgba(243,248,247,.1); border-radius: 10px; padding: 9px 12px; }
.mean u { text-decoration-color: #F2A196; text-decoration-style: wavy; }
.mean a { color: #D4B5B0; font-weight: 700; }
/* 55 Neuigkeiten-Abo */
.news { width: 290px; background: #F3F8F7; color: #1E3B44; border-radius: 16px; padding: 14px; display: grid; gap: 8px; font-size: .8rem; }
.news .f { border: 1.5px solid rgba(30,59,68,.2); border-radius: 10px; padding: 9px 12px; color: rgba(30,59,68,.55); }
.news .b { background: #D4B5B0; border-radius: 10px; padding: 9px 12px; text-align: center; font-weight: 700; }
/* 56 Geschichte */
.hist { width: 100%; max-width: 420px; display: grid; grid-auto-flow: column; gap: 0; align-items: start; color: #F3FAF8; font-size: .72rem; position: relative; }
.hist::before { content: ""; position: absolute; left: 6%; right: 6%; top: 9px; height: 2px; background: rgba(243,248,247,.3); }
.hist div { display: grid; justify-items: center; gap: 6px; text-align: center; position: relative; padding: 0 4px; }
.hist div::before { content: ""; width: 18px; height: 18px; border-radius: 50%; background: #D4B5B0; border: 3px solid #2D6A6A; }
.hist b { font-size: .86rem; }
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


add('alltag', 'impeccable harden', 'Das Wichtigste auch in anderen Sprachen', 'Krankmelden, Öffnungszeiten und Schließtage gibt es zusätzlich kurz auf Englisch, Türkisch, Arabisch und Ukrainisch – für Familien, die gerade Deutsch lernen. Arabisch läuft richtig von rechts nach links.',
    'harden: Seiten müssen auch mit anderen Sprachen funktionieren. Die Übersetzungen müssten geprüft werden.',
    '<div class="demo"><div class="lang"><div class="chips" id="lg"><button aria-pressed="true" data-l="de">Deutsch</button><button aria-pressed="false" data-l="en">English</button><button aria-pressed="false" data-l="tr">Türkçe</button><button aria-pressed="false" data-l="ar">العربية</button><button aria-pressed="false" data-l="uk">Українська</button></div><div class="tile" id="lgt"><b>Kind krank?</b>Bitte rufen Sie in der Gruppe an.</div></div></div>')
add('alltag', 'web-design-guidelines', 'Texte vorlesen lassen', 'Ein kleiner Lautsprecher-Knopf an Elternbriefen und Hinweisen: Der Browser liest den Text vor und markiert das gerade gelesene Wort. Ohne fremden Dienst, die Stimme kommt vom Gerät.',
    'Hilft beim Lesen auf dem Weg, bei Leseschwäche und für Familien, die Deutsch lernen.',
    '<div class="demo"><div class="read"><div class="tile" id="rdt">Am Freitag ist unser Laternenfest. Wir treffen uns um 17 Uhr im Garten.</div><button class="chip" id="rdb" type="button">Vorlesen</button></div></div>')
add('alltag', 'impeccable adapt', 'Schrift größer stellen', 'Zwei kleine Knöpfe „A“ und „A+“ im Fußbereich: die ganze Seite wird größer, ohne dass etwas überläuft. Für Großeltern und alle, die ungern zoomen.',
    'adapt: Die Seite verträgt schon 200 % Zoom – das macht es nur leichter zu finden.',
    '<div class="demo"><div class="fz"><div class="chips" id="fzc"><button aria-pressed="true" data-z=".8rem">A</button><button aria-pressed="false" data-z="1rem">A+</button><button aria-pressed="false" data-z="1.2rem">A++</button></div><div class="tile" id="fzt"><b>Heute geöffnet</b>Krippe und Kindergarten bis 16:30 Uhr, Hort bis 18:00 Uhr.</div></div></div>')
add('alltag', 'ui-ux-pro-max', 'Was gibt es heute zu essen?', 'Die eigene Küche ist ein Stolz des Hauses – der Wochen-Speiseplan gehört deshalb auf die Seite. Heute ist vorausgewählt, Allergene stehen klein darunter. Gepflegt wie die Termine in einer Tabelle.',
    'Braucht eine kleine Tabelle „speiseplan.csv“ von der Küche.',
    '<div class="demo"><div class="menu"><div class="chips" id="mn"><button aria-pressed="false">Mo</button><button aria-pressed="true">Di</button><button aria-pressed="false">Mi</button><button aria-pressed="false">Do</button><button aria-pressed="false">Fr</button></div><div class="tile" id="mnt"><b>Gemüselasagne</b>Apfelkompott · <span class="small">enthält Gluten, Milch</span></div></div></div>')
add('team', 'impeccable delight', 'Fundsachen-Ecke', 'Mützen, Brotdosen, Turnbeutel: Das Team fotografiert Fundsachen, sie erscheinen mit „abholen bis …“ auf der Seite. Nach Ablauf verschwinden sie automatisch.',
    'Ein kleiner Dienst für Eltern, der viel Sucherei erspart.',
    '<div class="demo"><div class="lost"><div><i></i>Blaue Mütze<br><span class="small">bis 30.11.</span></div><div><i></i>Brotdose<br><span class="small">bis 28.11.</span></div><div><i></i>Turnbeutel<br><span class="small">bis 04.12.</span></div></div></div>')
add('neu', 'impeccable onboard', 'Packliste für den ersten Tag', 'Für jeden Bereich eine Liste zum Abhaken: Wechselkleidung, Hausschuhe, Windeln, Trinkflasche … Der Fortschritt bleibt im eigenen Browser gespeichert. Nimmt neuen Eltern Unsicherheit.',
    'Die Inhalte der Liste kommen vom Hort.',
    '<div class="demo"><div class="pack" id="pk"><b>Krippe: erster Tag</b><label><input type="checkbox"> Wechselkleidung</label><label><input type="checkbox"> Hausschuhe</label><label><input type="checkbox"> Windeln und Feuchttücher</label><label><input type="checkbox"> Kuscheltier</label><div class="pb"><span></span></div></div></div>')
add('neu', 'impeccable delight', 'Countdown bis zum ersten Tag', 'Neue Eltern tragen den ersten Tag ihres Kindes ein und sehen, wie viele Tage es noch sind – mit drei kleinen Tipps zur Eingewöhnung. Am Tag selbst gibt es einen herzlichen Gruß.',
    'Ein seltener, emotionaler Moment – hier darf es etwas mehr Freude sein.',
    '<div class="demo"><div class="first"><span>Noch</span><b id="ftn">5</b><span id="ftt">Tage bis zum ersten Tag</span><input type="range" id="ftr" min="0" max="10" value="5" aria-label="Tage" style="accent-color:#D4B5B0"></div></div>')
add('alltag', 'impeccable clarify', 'Abholzeit-Rechner', 'Bringzeit und gebuchte Stunden einstellen – die Seite sagt: „Abholen bis 14:15 Uhr“. Gerade im Hort mit Mindestbuchungszeit eine häufige Frage.',
    'Rechnet nur, was ohnehin gilt; Sonderfälle klärt weiter das Team.',
    '<div class="demo"><div class="calc"><label>Bringzeit: <b id="cbz">7:30</b><input type="range" id="cbr" min="0" max="12" value="3"></label><label>Gebuchte Stunden: <b id="chz">6</b><input type="range" id="chr" min="4" max="10" value="6"></label><div class="res" id="cres">Abholen bis 13:30 Uhr</div></div></div>')
add('alltag', 'mobile-native', 'Erinnerung am Vortag', 'Beim Merken eines Termins ein Häkchen „Am Vortag erinnern“: Die Kalenderdatei bekommt dann eine Erinnerung mit, und das Handy meldet sich am Abend vorher.',
    'Steckt in der Kalenderdatei (VALARM) – keine App, kein Konto.',
    '<div class="demo"><div class="remind"><div class="notif" id="ntf"><b>Morgen: Laternenfest</b>17:00 Uhr, Garten · Kinderhort Grombühl</div><button class="chip" id="ntb" type="button">Merken mit Erinnerung</button></div></div>')
add('gestalt', 'impeccable delight', 'Kunstwerk der Woche', 'Jede Woche drei Bilder der Kinder als kleine Ausstellung – eingescannt, ohne Namen, mit Einverständnis der Eltern. Macht die Seite lebendig und zeigt, was im Alltag entsteht.',
    'Echte Kinderbilder statt gezeichneter Platzhalter – hier nur angedeutet.',
    '<div class="demo"><div class="art"><div><svg viewBox="0 0 60 60"><circle cx="20" cy="18" r="9" fill="#F3C98B"/><path d="M6 50 Q30 30 54 50" stroke="#7FD6A4" stroke-width="5" fill="none"/></svg></div><div><svg viewBox="0 0 60 60"><rect x="16" y="24" width="28" height="24" fill="#D4B5B0"/><path d="M12 26 L30 10 L48 26" fill="#2D6A6A"/></svg></div><div><svg viewBox="0 0 60 60"><path d="M10 40 C 20 10, 40 10, 50 40" stroke="#5B8DEF" stroke-width="4" fill="none"/><circle cx="30" cy="44" r="6" fill="#F2A196"/></svg></div></div></div>')
add('alltag', 'impeccable clarify', 'Zum Elternabend zu- oder absagen', 'Unter Terminen mit Anmeldung zwei Knöpfe: „Ich komme“ und „Ich komme nicht“. Es öffnet sich eine fertige E-Mail mit Termin und Platz für den Namen – kein Formular, kein Server.',
    'Wie bei Krankmelden und Platz anfragen.',
    '<div class="demo"><div class="rsvp"><div class="chips" id="rs"><button aria-pressed="false" data-r="ja">Ich komme</button><button aria-pressed="false" data-r="nein">Ich komme nicht</button></div><div class="mailprev" id="rsm">Betreff: …</div></div></div>')
add('alltag', 'humanizer', 'Lesezeit an Elternbriefen', 'Jeder Brief zeigt, wie lange er zu lesen ist: „1 Min.“ oder „4 Min.“. Eltern entscheiden, ob sie jetzt lesen oder später.',
    'Wird beim Bauen der Seite aus der Textlänge berechnet.',
    '<div class="demo"><div class="rt"><div class="tile"><b>Schließtage und Fortbildungen<small>2 Min.</small></b></div><div class="tile"><b>Läuse<small>unter 1 Min.</small></b></div><div class="tile"><b>Ferienbetreuung im Hort<small>3 Min.</small></b></div></div></div>')
add('gestalt', 'apple-design', 'Spürbares Merken', 'Auf Android-Handys gibt es beim Merken eines Termins ein ganz kurzes Vibrieren – wie bei einer echten App. Wer „Bewegung reduzieren“ eingestellt hat, bekommt es nicht.',
    'Ein Tick von 10 Millisekunden, nur bei Bestätigungen.',
    '<div class="demo"><div class="vib"><button type="button" id="vb">Merken</button><span class="small">Am Handy spürbar, hier sichtbar</span></div></div>')
add('neu', 'humanizer', 'Leichte Sprache', 'Die Seiten zu Krippe, Kindergarten und Hort gibt es zusätzlich in Leichter Sprache: kurze Sätze, ein Gedanke pro Zeile, schwierige Wörter erklärt. Ein Schalter oben wechselt hin und her.',
    'Leichte Sprache sollte von geübten Menschen geprüft werden.',
    '<div class="demo"><div class="easy"><div class="chips" id="ez"><button aria-pressed="true">Normal</button><button aria-pressed="false">Leichte Sprache</button></div><div class="tile" id="ezt">Die Kinderkrippe betreut Kinder ab 11 Monaten bis zum August des Jahres, in dem sie 3 Jahre alt werden.</div></div></div>')
add('alltag', 'gestures', 'Eltern-ABC als Karten zum Wischen', 'Das KrippenABC, KindergartenABC und HortABC als Kartenstapel: oben die Karte, mit dem Finger weggewischt kommt die nächste. Statt eines langen PDFs zum Durchblättern in der Wartezeit.',
    'Zusätzlich bleibt das PDF zum Herunterladen.',
    '<div class="demo"><div class="abc" id="ab"><div class="k"><b>W</b>Wechselkleidung – bitte immer ein Set im Fach.</div><div class="k"><b>B</b>Brotzeit – eine Trinkflasche mit Wasser genügt.</div><div class="k"><b>A</b>Abholen – bitte bis zur gebuchten Zeit.</div></div></div>')
add('team', 'impeccable harden', 'Kühlschrank-Zettel zum Ausdrucken', 'Eine einzige Seite mit allem für die Pinnwand zu Hause: Durchwahlen aller Gruppen, Öffnungszeiten, Schließtage des Jahres. Ein Knopf „Für den Kühlschrank drucken“.',
    'Wie der Jahresposter, nur noch knapper.',
    '<div class="demo"><div class="fridge"><h6>Kinderhort Grombühl</h6><div><span>Zentrale</span><b>2789892 0</b></div><div><span>Sternengruppe</span><b>… 15</b></div><div><span>Bienengruppe</span><b>… 13</b></div><div><span>Öffnungszeiten</span><b>6:45–18:00</b></div><h6>Schließtage</h6><div><span>Weihnachten</span><b>24.12.–08.01.</b></div><div><span>Ostern</span><b>25.–30.03.</b></div></div></div>')


add('alltag', 'impeccable clarify', 'Die Suche beantwortet Fragen', 'Wer in die Suche (Lupe oben) eine Frage tippt – „morgen offen?“, „Nummer Bienen“ – bekommt die Antwort direkt oben über den Treffern, wie im Fragen-Helfer. Ohne erst zur Kontaktseite zu wechseln.',
    'Nutzt denselben schlauen Helfer, der auf „Kontakt“ schon antwortet.',
    '<div class="demo"><div class="srch"><div class="in"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="vertical-align:-2px;margin-right:6px"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg>Nummer Bienen</div><div class="ans"><b>Bienengruppe</b> · 0931 2789892 13</div><div class="hit">Kontakt &amp; Durchwahlen</div><div class="hit">Kindergarten · Bereich</div></div></div>')
add('alltag', 'dataviz', '„Jetzt gerade“ im Tagesablauf', 'Im Tagesablauf jeder Bereichsseite ist der Abschnitt hervorgehoben, der gerade läuft – etwa „Mittagessen“ oder „Hausaufgabenzeit“. Eltern sehen, ob jetzt ein guter Moment zum Anrufen ist.',
    'Rechnet mit den Uhrzeiten, die im Tagesablauf schon stehen.',
    '<div class="demo"><div class="tl4" id="tl4"><div data-t="405"><time>6:45</time>Ankommen, Frühstück</div><div data-t="540"><time>9:00</time>Morgenkreis, Projekte</div><div data-t="690"><time>11:30</time>Mittagessen</div><div data-t="750"><time>12:30</time>Ruhezeit</div><div data-t="870"><time>14:30</time>Garten, Abholzeit</div></div></div>')
add('alltag', 'impeccable clarify', 'Bring- und Abholzeit als Hinweis', 'Unter „Jetzt geöffnet“ steht zur passenden Zeit ein kleiner Satz: „Bringzeit bis 9:00 Uhr“ morgens oder „Abholzeit Krippe und Kindergarten bis 16:30“ am Nachmittag.',
    'Nur zu den Zeiten, in denen er wirklich hilft.',
    '<div class="demo"><div class="bz"><div class="chips" id="bzc"><button aria-pressed="true" data-h="8">8:00</button><button aria-pressed="false" data-h="12">12:00</button><button aria-pressed="false" data-h="16">16:00</button></div><div class="tile"><b><i></i><span id="bzt">Bringzeit bis 9:00 Uhr</span></b></div></div></div>')
add('alltag', 'ui-ux-pro-max', 'Termine nach Bereich filtern', 'Über den Terminen kleine Knöpfe: Alle · Krippe · Kindergarten · Hort. Ein Tipp, und nur noch die Termine für den eigenen Bereich stehen da. Termine fürs ganze Haus bleiben immer sichtbar.',
    'Braucht in der Termin-Tabelle eine kleine Spalte „Bereich“.',
    '<div class="demo"><div class="evf"><div class="chips" id="evc"><button aria-pressed="true" data-b="alle">Alle</button><button aria-pressed="false" data-b="krippe">Krippe</button><button aria-pressed="false" data-b="kiga">Kindergarten</button><button aria-pressed="false" data-b="hort">Hort</button></div><div class="tile" data-b="haus">Weihnachtsmarkt <span>ganzes Haus</span></div><div class="tile" data-b="kiga">Elternabend Kindergarten <span>Kiga</span></div><div class="tile" data-b="hort">Ferienfreizeit <span>Hort</span></div><div class="tile" data-b="krippe">Eingewöhnungs-Café <span>Krippe</span></div></div></div>')
add('alltag', 'mobile-native', 'Kalender-Abo nur für den eigenen Bereich', 'Neben dem Abo für alle Termine gibt es eines nur für Krippe, eines für Kindergarten, eines für Hort. Im Handy-Kalender stehen dann nur die Termine, die einen betreffen – und sie aktualisieren sich von selbst.',
    'Baut auf der Spalte „Bereich“ aus der vorigen Idee auf.',
    '<div class="demo"><div class="evf"><div class="tile">Alle Termine <span>abonnieren</span></div><div class="tile">Nur Krippe <span>abonnieren</span></div><div class="tile">Nur Kindergarten <span>abonnieren</span></div><div class="tile">Nur Hort <span>abonnieren</span></div></div></div>')
add('alltag', 'dataviz', 'Feiertage im Monatskalender', 'Im Kalender auf „Aktuelles“ sind Feiertage eigens markiert und mit Namen versehen, zusätzlich zu Schließtagen und Terminen. So sieht man auf einen Blick, warum ein Tag frei ist.',
    'Die Feiertage stehen schon in feiertage.csv.',
    '<div class="demo"><div class="mcal"><b>Mo</b><b>Di</b><b>Mi</b><b>Do</b><b>Fr</b><b>Sa</b><b>So</b><span></span><span></span><span></span><span></span><span></span><span></span><span class="fe" title="Allerheiligen">1</span><span class="zu">2</span><span class="zu">3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span class="ev">11</span><span>12</span><span>13</span><span>14</span><span>15</span><div class="mleg"><span>■ Termin</span><span style="color:#B8574A">■ Feiertag</span><span style="color:#C9A49E">■ geschlossen</span></div></div></div>')
add('alltag', 'web-design-guidelines', 'Elternbrief teilen und drucken', 'Jeder Elternbrief bekommt „Teilen“ (z. B. an den Partner per Nachricht) und „Drucken“ – gedruckt nur der Brief, sauber auf einer Seite, ohne Menü und Fußbereich.',
    'Wie „Termin teilen“, das es schon gibt.',
    '<div class="demo"><div class="bshare"><b>Schließtage, Fortbildungen und Überstunden</b><span class="small">Kita-Jahr 2026/27</span><div class="row"><span>Teilen</span><span>Drucken</span><span>Link kopieren</span></div></div></div>')
add('alltag', 'impeccable clarify', 'Abholvollmacht als Vorlage', 'Wenn Oma oder ein Nachbar das Kind abholt: eine fertige E-Mail-Vorlage mit allen nötigen Angaben – Name des Kindes, wer abholt, an welchem Tag. Spart Rückfragen an der Tür.',
    'Wie Krankmelden und Platz anfragen; ob eine E-Mail reicht oder eine Unterschrift nötig ist, entscheidet der Hort.',
    '<div class="demo"><div class="voll">Betreff: Abholung durch eine andere Person<br><br>Name des Kindes: …<br>Gruppe: …<br>Abholung am: …<br>Abholende Person: …<br>Ausweis wird mitgebracht: ja</div></div>')
add('alltag', 'mobile-native', 'Die eigene Gruppe als Kontakt speichern', 'Neben jeder Durchwahl ein kleiner Knopf: „Als Kontakt speichern“. Im Handy steht dann „Kita – Bienengruppe“ mit der richtigen Nummer – gefunden in einer Sekunde.',
    'Es gibt schon die Kontaktkarte fürs ganze Haus; das hier ist eine je Gruppe.',
    '<div class="demo"><div class="vcard"><div class="av"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#1E3B44" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="14.5" rx="5" ry="6"/><path d="M7.4 12.5h9.2M7.4 16.5h9.2"/></svg></div><b>Kita – Bienengruppe</b><span>0931 2789892 13</span><span style="margin-top:4px;padding:7px 12px;border-radius:10px;background:#1E3B44;color:#F3F8F7;font-weight:700;font-size:.74rem">Als Kontakt speichern</span></div></div>')
add('team', 'impeccable harden', 'Wichtiger Hinweis auf allen Seiten', 'Für Ausnahmen – Schließung wegen Unwetter, Wasserrohrbruch, Streik – trägt das Team einen „wichtigen Hinweis“ ein. Er erscheint auffällig oben auf jeder Seite, bis das Datum vorbei ist.',
    'Eine Zeile mehr in hinweise.csv mit „wichtig“.',
    '<div class="demo"><div class="alarm"><div class="bar"><i></i>Heute (Do) wegen Sturmwarnung ab 13 Uhr geschlossen.</div><div class="page"></div></div></div>')
add('neu', 'impeccable distill', 'Alle Fragen auf einer Seite', 'Die häufigen Fragen aus Krippe, Kindergarten und Hort gesammelt auf einer eigenen Seite – mit Suche und den Themen-Knöpfen. Für Eltern, die sich noch nicht für einen Bereich entschieden haben.',
    'Die Fragen bleiben auch auf den Bereichsseiten.',
    '<div class="demo"><div class="allq"><div class="chips"><button aria-pressed="true">Alle</button><button aria-pressed="false">Krippe</button><button aria-pressed="false">Kindergarten</button><button aria-pressed="false">Hort</button></div><div class="tile">Gibt es eine Eingewöhnungszeit? <span class="small">· Krippe</span></div><div class="tile">Braucht mein Kind eine Brotzeit? <span class="small">· Hort</span></div></div></div>')
add('neu', 'landing-page-design', 'Unser Team', 'Eine kleine Seite mit Fotos (oder Namen) und Rollen: Leitung, Gruppenleitungen, Küche. Neue Eltern wissen vorher, wen sie treffen – das schafft Vertrauen.',
    'Nur mit Einverständnis des Teams; Fotos liefert der Hort.',
    '<div class="demo"><div class="team"><div><div class="ph">PL</div><b>Petra Lachnit</b><br>Einrichtungsleitung</div><div><div class="ph">?</div><b>Name</b><br>Bienengruppe</div><div><div class="ph">?</div><b>Name</b><br>Küche</div></div></div>')
add('neu', 'impeccable onboard', 'Eingang finden – mit Fotos', 'Für den ersten Tag: wo ist welcher Eingang, wo ist die Krippe, wo die Garderobe? Zwei, drei Fotos mit kurzen Sätzen nehmen die Unsicherheit beim ersten Bringen.',
    'Fotos vom Eingangsbereich liefert der Hort.',
    f'<div class="demo"><div class="door"><figure><img src="{IMG("p2160110")}" alt=""><b>1</b> Haupteingang Lindleinstraße, Klingel „Krippe“</figure><figure><img src="{IMG("lesecke")}" alt=""><b>2</b> Garderobe links, Hausschuhe ins Fach</figure></div></div>')
add('alltag', 'impeccable clarify', '„Meinten Sie …?“ in der Suche', 'Bei Tippfehlern in der Suche – „Feinplan“, „Krankmedlung“ – erscheint „Meinten Sie: Ferienplan?“. Ein Tipp, und die richtigen Treffer sind da.',
    'Gleiche Tippfehler-Toleranz wie in „Durchwahl finden“.',
    '<div class="demo"><div class="mean"><div class="in"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="vertical-align:-2px;margin-right:6px"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg><u>Krankmedlung</u></div><div>Meinten Sie: <a>Krankmeldung</a>?</div></div></div>')
add('team', 'pinme-email', 'Neuigkeiten per E-Mail (später)', 'Eltern tragen ihre E-Mail ein und bekommen eine kurze Nachricht, wenn ein neuer Elternbrief oder Termin erscheint. Braucht einen kleinen Dienst beim Hosting – erst sinnvoll, wenn der Webspace steht.',
    'Datenschutz: Einwilligung und Abmelde-Link sind Pflicht.',
    '<div class="demo"><div class="news"><b>Neuigkeiten per E-Mail</b><div class="f">ihre@adresse.de</div><div class="b">Anmelden</div><span class="small">Abmelden jederzeit mit einem Klick.</span></div></div>')
add('gestalt', 'impeccable delight', 'Unsere Geschichte als Zeitleiste', 'Eine kleine Zeitleiste: Gründung, Umbau, neue Krippe, Auszeichnungen. Zeigt, dass hier seit Jahrzehnten Kinder groß werden. Die Jahreszahlen kommen vom Hort.',
    'Hier mit Platzhaltern.',
    '<div class="demo"><div class="hist"><div><b>19__</b>Gründung</div><div><b>19__</b>Hort</div><div><b>20__</b>Krippe</div><div><b>20__</b>Umbau</div><div><b>heute</b>3 Bereiche</div></div></div>')

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

  /* 25 Sprachen */
  (function () { var T = { de: ["Kind krank?", "Bitte rufen Sie in der Gruppe an."], en: ["Child is ill?", "Please call your child’s group."], tr: ["Çocuğunuz hasta mı?", "Lütfen grubu arayın."], ar: ["طفلك مريض؟", "يرجى الاتصال بالمجموعة."], uk: ["Дитина захворіла?", "Будь ласка, зателефонуйте до групи."] };
    $("#lg").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#lg button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); var t = T[b.dataset.l], el = $("#lgt"); el.innerHTML = "<b></b>"; $("b", el).textContent = t[0]; el.appendChild(document.createTextNode(t[1])); el.dir = b.dataset.l === "ar" ? "rtl" : "ltr"; el.lang = b.dataset.l; }); })();
  /* 26 Vorlesen */
  (function () { var el = $("#rdt"), txt = el.textContent, b = $("#rdb");
    b.addEventListener("click", function () {
      if (!("speechSynthesis" in window)) { b.textContent = "Vorlesen hier nicht verfügbar"; return; }
      speechSynthesis.cancel(); var u = new SpeechSynthesisUtterance(txt); u.lang = "de-DE";
      u.onboundary = function (ev) { var i = ev.charIndex, j = txt.indexOf(" ", i); if (j < 0) j = txt.length; el.innerHTML = ""; el.append(txt.slice(0, i)); var m = document.createElement("mark"); m.textContent = txt.slice(i, j); el.append(m, txt.slice(j)); };
      u.onend = function () { el.textContent = txt; }; speechSynthesis.speak(u); }); })();
  /* 27 Schrift */
  $("#fzc").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#fzc button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); $("#fzt").style.fontSize = b.dataset.z; });
  /* 28 Speiseplan */
  (function () { var M = { Mo: ["Kartoffelsuppe mit Würstchen", "Obst · enthält Sellerie"], Di: ["Gemüselasagne", "Apfelkompott · enthält Gluten, Milch"], Mi: ["Fischstäbchen mit Kartoffelbrei", "Rohkost · enthält Fisch, Milch"], Do: ["Linsen-Dal mit Reis", "Joghurt · enthält Milch"], Fr: ["Pfannkuchen", "Apfelmus · enthält Ei, Gluten, Milch"] };
    $("#mn").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#mn button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); var m = M[b.textContent]; $("#mnt").innerHTML = "<b></b><span class=\"small\"></span>"; $("#mnt b").textContent = m[0]; $("#mnt span").textContent = m[1]; }); })();
  /* 30 Packliste */
  (function () { var bx = $$("#pk input"), bar = $("#pk .pb span"); function u() { bar.style.width = (bx.filter(function (x) { return x.checked; }).length / bx.length * 100) + "%"; } bx.forEach(function (x) { x.addEventListener("change", u); }); })();
  /* 31 Erster Tag */
  $("#ftr").addEventListener("input", function () { var n = +this.value; $("#ftn").textContent = n ? n : "Heute"; $("#ftt").textContent = n ? (n === 1 ? "Tag bis zum ersten Tag" : "Tage bis zum ersten Tag") : "ist der erste Tag – willkommen!"; });
  /* 32 Abholzeit */
  (function () { function f(m) { return Math.floor(m / 60) + ":" + String(m % 60).padStart(2, "0"); }
    function u() { var b = 405 + 15 * +$("#cbr").value, h = +$("#chr").value, e = Math.min(1080, b + h * 60); $("#cbz").textContent = f(b); $("#chz").textContent = h; $("#cres").textContent = "Abholen bis " + f(e) + " Uhr"; }
    $("#cbr").addEventListener("input", u); $("#chr").addEventListener("input", u); u(); })();
  /* 33 Erinnerung */
  $("#ntb").addEventListener("click", function () { var n = $("#ntf"); n.classList.remove("on"); void n.offsetWidth; setTimeout(function () { n.classList.add("on"); }, 400); });
  /* 35 Zusage */
  $("#rs").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#rs button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); $("#rsm").textContent = "Betreff: Elternabend 20.01. – " + (b.dataset.r === "ja" ? "Zusage" : "Absage") + "\nName: …\nGruppe: …"; $("#rsm").style.whiteSpace = "pre-line"; });
  /* 37 Vibration */
  $("#vb").addEventListener("click", function () { var b = this; if (navigator.vibrate && !reduced) navigator.vibrate(10); b.classList.remove("pulse"); void b.offsetWidth; b.classList.add("pulse"); b.textContent = b.textContent === "Merken" ? "Gemerkt" : "Merken"; });
  /* 38 Leichte Sprache */
  $("#ez").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#ez button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); $("#ezt").innerHTML = b.textContent === "Normal" ? "Die Kinderkrippe betreut Kinder ab 11 Monaten bis zum August des Jahres, in dem sie 3 Jahre alt werden." : "Die Krippe ist für kleine Kinder.<br>Ihr Kind kann ab 11 Monaten kommen.<br>Es bleibt, bis es 3 Jahre alt ist."; });
  /* 39 Karten wischen */
  (function () { var st = $("#ab");
    function top() { var ks = $$(".k", st); return ks[ks.length - 1]; }
    st.addEventListener("pointerdown", function (e) { var k = top(); if (!k || !k.contains(e.target)) return; var x0 = e.clientX; k.setPointerCapture(e.pointerId); k.style.transition = "none";
      function mv(ev) { var dx = ev.clientX - x0; k.style.translate = dx + "px 0"; k.style.rotate = (dx / 12) + "deg"; }
      function up(ev) { k.removeEventListener("pointermove", mv); k.removeEventListener("pointerup", up); var dx = ev.clientX - x0; k.style.transition = "translate .3s cubic-bezier(.23,1,.32,1), rotate .3s, opacity .3s";
        if (Math.abs(dx) > 70) { k.style.translate = (dx > 0 ? 300 : -300) + "px 0"; k.style.opacity = 0; setTimeout(function () { k.style.transition = "none"; k.style.translate = ""; k.style.rotate = ""; k.style.opacity = ""; st.prepend(k); }, 300); } else { k.style.translate = ""; k.style.rotate = ""; } }
      k.addEventListener("pointermove", mv); k.addEventListener("pointerup", up); });
    st.tabIndex = 0; st.setAttribute("aria-label", "Karten: Pfeiltaste rechts für die nächste"); st.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { var k = top(); st.prepend(k); } }); })();

  /* 42 jetzt im Tagesablauf */
  (function () { var n = new Date(), m = n.getHours() * 60 + n.getMinutes(), rows = $$("#tl4 div"), cur = null; rows.forEach(function (r) { if (+r.dataset.t <= m) cur = r; }); (cur || rows[2]).classList.add("now"); })();
  /* 43 Bringzeit */
  $("#bzc").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#bzc button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); var h = +b.dataset.h; $("#bzt").textContent = h < 9 ? "Bringzeit bis 9:00 Uhr" : h < 15 ? "Mittagszeit – Anrufe am besten nach 14:30 Uhr" : "Abholzeit: Krippe und Kindergarten bis 16:30 Uhr"; });
  /* 44 Filter */
  $("#evc").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; $$("#evc button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); var f = b.dataset.b; $$(".evf .tile[data-b]").forEach(function (t) { t.hidden = !(f === "alle" || t.dataset.b === "haus" || t.dataset.b === f); }); });
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
