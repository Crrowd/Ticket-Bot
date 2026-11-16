# 002 — Liste/Kalender: Abgang mit ease-out statt ease-in

- **Status**: DONE
- **Commit**: 1d9b6ec
- **Severity**: HIGH
- **Category**: Easing & duration
- **Estimated scope**: 1 file (`js/main.js`), 1 Zeile

## Problem

Beim Umschalten der Termine zwischen „Liste“ und „Kalender“ blendet die alte Ansicht mit `ease-in` aus. `ease-in` startet langsam und verzögert genau den Moment, auf den man schaut – der Umschalter wirkt kurz „hängend“.

```js
// kinderhort-website/js/main.js:1286 — current
out.animate([{ opacity: 1 }, { opacity: 0, scale: .98 }], { duration: 140, easing: "ease-in" }).onfinish = function () { swap(); inn.animate([{ opacity: 0, scale: 1.02 }, { opacity: 1, scale: 1 }], { duration: 240, easing: "cubic-bezier(.23,1,.32,1)" }); };
```

## Target

Abgang mit der starken ease-out-Kurve `cubic-bezier(0.23, 1, 0.32, 1)` und 120 ms; Auftritt unverändert (240 ms, gleiche Kurve), aber über die vorhandene Konstante.

```js
// target
out.animate([{ opacity: 1 }, { opacity: 0, scale: .98 }], { duration: 120, easing: EASE_OUT }).onfinish = function () { swap(); inn.animate([{ opacity: 0, scale: 1.02 }, { opacity: 1, scale: 1 }], { duration: 240, easing: EASE_OUT }); };
```

## Repo conventions to follow

- `js/main.js:22` definiert `var EASE_IO = "cubic-bezier(.65, 0, .35, 1)", EASE_OUT = "cubic-bezier(.23, 1, .32, 1)";` – diese Konstanten verwenden.
- Vorbild: `js/main.js:829` `d.animate([...], { duration: 250, easing: EASE_OUT })`.

## Steps

1. In `js/main.js` in der Funktion `show(v, anim)` (Abschnitt „Termine als Liste oder Kalender“) die oben zitierte Zeile durch die Ziel-Zeile ersetzen.

## Boundaries

- Nichts anderes in `show()` ändern; die Logik von `swap()` bleibt.
- Den Abschnitt „Übergang 16 – Inhalt gleitet in die Richtung des Reiters“ (setzt `.slide-from-r` / `.slide-from-l`) NICHT anfassen.
- Bei Abweichung des Codes STOPP und melden.

## Verification

- **Mechanical**: `node -e "new Function(require('fs').readFileSync('js/main.js','utf8'))"` ohne Fehler; `python3 build.py` läuft.
- **Feel check**: `aktuelles.html` öffnen, mehrfach zwischen Liste und Kalender wechseln:
  - Die alte Ansicht beginnt sofort zu verblassen, kein Zögern am Anfang.
  - DevTools → Animations auf 10 %: Der Abgang ist schnell los, sanft am Ende. Achten, ob Auftritt (scale) und die Gleit-Klasse aus Übergang 16 zusammen unruhig wirken – falls ja, im Bericht erwähnen, nicht selbst ändern.
- **Done when**: `grep -n '"ease-in"' js/main.js` findet nichts.
