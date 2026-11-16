# 009 — Viewport-Werte nur bei echter Änderung schreiben

- **Status**: DONE
- **Commit**: 1d9b6ec
- **Severity**: LOW
- **Category**: Performance
- **Estimated scope**: 1 file (`js/main.js`), 1 Funktion

## Problem

`onViewport` läuft bei jedem `resize` **und** `scroll` des sichtbaren Bereichs (`visualViewport`) und schreibt jedes Mal `--kb` und `--vvh` auf `<html>`. Eine geänderte Custom Property an der Wurzel kann die Stile der ganzen Seite neu berechnen lassen – auch wenn sich der Wert gar nicht geändert hat.

```js
// kinderhort-website/js/main.js:72–79 — current
var vv = window.visualViewport;
function onViewport() {
  var kb = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop));
  root.style.setProperty("--kb", kb + "px");
  root.style.setProperty("--vvh", Math.round(vv.height) + "px");
  root.classList.toggle("kb-open", kb > 80);
}
if (vv) { vv.addEventListener("resize", onViewport); vv.addEventListener("scroll", onViewport); onViewport(); }
```

## Target

```js
// target
var vv = window.visualViewport, lastKb = -1, lastVvh = -1;
function onViewport() {
  var kb = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop)), h = Math.round(vv.height);
  if (kb !== lastKb) { lastKb = kb; root.style.setProperty("--kb", kb + "px"); root.classList.toggle("kb-open", kb > 80); }
  if (h !== lastVvh) { lastVvh = h; root.style.setProperty("--vvh", h + "px"); }
}
if (vv) { vv.addEventListener("resize", onViewport); vv.addEventListener("scroll", onViewport); onViewport(); }
```

## Repo conventions to follow

- ES5-Stil (`var`, `function`), wie im ganzen `js/main.js`.

## Steps

1. In `js/main.js` den zitierten Block (Abschnitt „Handy-Tastatur: Höhe messen …“) durch den Ziel-Block ersetzen.

## Boundaries

- Die folgende `focusin`-Logik („Eingabefeld beim Antippen in den sichtbaren Bereich holen“) NICHT ändern.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: JS-Syntaxprüfung `node -e "new Function(require('fs').readFileSync('js/main.js','utf8'))"`; `python3 build.py`.
- **Feel check** (Handy, echtes Gerät oder Emulation):
  - Suche öffnen, Tastatur erscheint: das Suchfenster sitzt über der Tastatur wie vorher.
  - Seite scrollen: in DevTools → Performance keine wiederholten „Recalculate Style“ auf `html` durch `--kb`.
- **Done when**: `onViewport` schreibt nur noch innerhalb der beiden `if`-Zweige.
