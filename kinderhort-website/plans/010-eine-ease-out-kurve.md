# 010 — Eine ease-out-Kurve statt zwei, JS liest die Tokens

- **Status**: TODO
- **Commit**: 1d9b6ec
- **Severity**: LOW
- **Category**: Cohesion & tokens
- **Estimated scope**: 2 files (`css/style.css`, `js/main.js`), 3 Zeilen

## Problem

Es gibt zwei fast gleiche starke ease-out-Kurven nebeneinander, dazu feste Kopien im JavaScript:

```css
/* kinderhort-website/css/style.css (:root, ca. Zeile 64) — current */
--ease-out: cubic-bezier(.23, 1, .32, 1);           /* Auftritte: schnell los, sanft landen */
--ease-in-out: cubic-bezier(.65, 0, .35, 1);        /* Bewegungen von A nach B */
/* kinderhort-website/css/style.css:1565 — current */
:root { --io: cubic-bezier(.22, 1, .36, 1); --rule: color-mix(in oklab, currentColor 16%, transparent); }
```

```js
// kinderhort-website/js/main.js:22 — current
var EASE_IO = "cubic-bezier(.65, 0, .35, 1)", EASE_OUT = "cubic-bezier(.23, 1, .32, 1)";
```

`--io` wird an 46 Stellen verwendet; der Unterschied zu `--ease-out` ist mit bloßem Auge nicht sichtbar, die Doppelung lädt aber zum weiteren Auseinanderdriften ein.

## Target

- `--io` wird ein Alias auf die eine Kurve: `--io: var(--ease-out);` (Wert: `cubic-bezier(.23, 1, .32, 1)`).
- JavaScript liest beide Kurven aus den CSS-Tokens, mit den heutigen Werten als Rückfall:

```js
// target
var CSSV = getComputedStyle(document.documentElement);
var EASE_IO = CSSV.getPropertyValue("--ease-in-out").trim() || "cubic-bezier(.65, 0, .35, 1)",
    EASE_OUT = CSSV.getPropertyValue("--ease-out").trim() || "cubic-bezier(.23, 1, .32, 1)";
```

```css
/* target, css/style.css:1565 */
:root { --io: var(--ease-out); --rule: color-mix(in oklab, currentColor 16%, transparent); }
```

## Repo conventions to follow

- Tokens in `:root` am Anfang von `css/style.css`; Kommentar auf Deutsch.
- DESIGN.md nennt als einzige Kurve `cubic-bezier(.22, 1, .36, 1)` (Abschnitt „Do's and Don'ts“). Nach diesem Plan ist die eine Kurve `cubic-bezier(.23, 1, .32, 1)` – den Wert in `DESIGN.md` und `.impeccable/design.json` (Eintrag `motion` → `io`) entsprechend auf `cubic-bezier(.23, 1, .32, 1)` ändern.

## Steps

1. `css/style.css:1565`: `--io: cubic-bezier(.22, 1, .36, 1);` ersetzen durch `--io: var(--ease-out);`.
2. `js/main.js:22`: die Zeile durch den Ziel-Block ersetzen (die Variable `root` ist erst danach definiert – deshalb `document.documentElement` verwenden).
3. `DESIGN.md`: im Satz „Do eine Bewegungskurve verwenden: `cubic-bezier(.22, 1, .36, 1)`“ den Wert auf `cubic-bezier(.23, 1, .32, 1)` ändern.
4. `.impeccable/design.json`: in `extensions.motion` beim Eintrag `"name": "io"` den `value` auf `"cubic-bezier(.23, 1, .32, 1)"` setzen.

## Boundaries

- Die Konfetti-Kurve `cubic-bezier(.2,.7,.4,1)` (`js/main.js:1218`, Wurfbahn) und `cubic-bezier(.5, 0, .2, 1)` (`css/style.css:378`, Bogen der Foto-Collage) bleiben – sie beschreiben Wurfbahnen, keine UI-Auftritte.
- Keine Dauern ändern.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`; JS-Syntaxprüfung; `node -e` nicht nötig für CSS. Im Browser: `getComputedStyle(document.documentElement).getPropertyValue("--io")` ergibt die `--ease-out`-Kurve.
- **Feel check**: Kurzmeldung, Bildansicht, Bereichsmenü, Handy-Menü öffnen – alles fühlt sich an wie vorher (der Unterschied der Kurven ist unter der Wahrnehmungsschwelle).
- **Done when**: `grep -n "cubic-bezier(.22, 1, .36, 1)" css/style.css js/main.js` findet nichts.
