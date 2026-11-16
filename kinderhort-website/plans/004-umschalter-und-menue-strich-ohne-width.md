# 004 — Umschalter-Knopf und Menü-Strich ohne width-Animation

- **Status**: DONE
- **Commit**: 1d9b6ec
- **Severity**: MEDIUM
- **Category**: Performance + Easing & duration
- **Estimated scope**: 2 files (`css/style.css`, `js/main.js`), ca. 12 Zeilen

## Problem

Zwei gleitende Markierungen animieren `width` (Layout-Eigenschaft):

1. Der dunkle Knopf in den Umschaltern „Liste/Kalender“ (`aktuelles.html`) und „iPhone/Android/Outlook“ (`downloads.html`), 350 ms – über dem Budget für kleine Bedienelemente (150–250 ms).

```css
/* kinderhort-website/css/style.css:1318 — current */
.vs-knob { position: absolute; z-index: 0; top: 4px; left: 0; height: calc(100% - 8px); border-radius: 8px; background: var(--ink); transition: translate .35s var(--ease-in-out), width .35s var(--ease-in-out); }
```

```js
// kinderhort-website/js/main.js:1237–1242 — current
function slideKnob(group, btn, anim) {
  var k = $(".vs-knob", group); if (!k || !btn) return;
  if (!anim || reduced) k.style.transition = "none";
  k.style.width = btn.offsetWidth + "px"; k.style.translate = btn.offsetLeft + "px 0";
  if (!anim || reduced) { void k.offsetWidth; k.style.transition = ""; }
}
```

2. Der rosé Strich, der im Hauptmenü am Computer der Maus folgt (Abschnitt „Übergang 35 – Strich wandert im Menü mit“ in `js/main.js`, ab ca. Zeile 1936):

```css
/* kinderhort-website/css/style.css:1750 — current */
.nav-line { position: absolute; left: 0; bottom: 4px; height: 2px; border-radius: 3px; background: var(--rose-deep); width: 0; opacity: 0; pointer-events: none; transition: translate .25s var(--io), width .25s var(--io), opacity .2s var(--io); }
```

```js
// js/main.js, function to(el) im Abschnitt „Übergang 35“ — current
line.style.width = (r.width - pad * 2) + "px"; line.style.translate = (r.left - u.left + pad) + "px 0"; line.style.opacity = 1;
```

## Target

**Umschalter-Knopf:** volle Breite der Gruppe, per `clip-path` auf den aktiven Knopf zugeschnitten; 200 ms `var(--ease-in-out)`.

```css
/* target */
.vs-knob { position: absolute; z-index: 0; top: 4px; left: 0; width: 100%; height: calc(100% - 8px); background: var(--ink);
  clip-path: inset(0 calc(100% - var(--vx, 0px) - var(--vw, 0px)) 0 var(--vx, 0px) round 8px);
  transition: clip-path 200ms var(--ease-in-out); }
```

```js
// target – in slideKnob statt der width/translate-Zeile:
k.style.setProperty("--vx", btn.offsetLeft + "px"); k.style.setProperty("--vw", btn.offsetWidth + "px");
```

**Menü-Strich:** 1 px breit, per `scale` auf die Wortbreite gezogen (Ursprung links); 200 ms `var(--ease-in-out)`.

```css
/* target */
.nav-line { position: absolute; left: 0; bottom: 4px; height: 2px; width: 1px; transform-origin: 0 50%; background: var(--rose-deep); opacity: 0; pointer-events: none; transition: translate 200ms var(--ease-in-out), scale 200ms var(--ease-in-out), opacity 200ms var(--ease-out); }
```

```js
// target – in function to(el):
line.style.scale = (r.width - pad * 2) + " 1"; line.style.translate = (r.left - u.left + pad) + "px 0"; line.style.opacity = 1;
```

## Repo conventions to follow

- Tokens: `--ease-in-out: cubic-bezier(.65, 0, .35, 1)`, `--ease-out: cubic-bezier(.23, 1, .32, 1)` in `:root`.
- Vorbild `clip-path` mit Rundung: Plan 003 (`.subnav-knob`) bzw. `css/style.css:997`.

## Steps

1. `css/style.css:1318`: Regel `.vs-knob { … }` durch die Ziel-Regel ersetzen.
2. `js/main.js` in `slideKnob`: Zeile `k.style.width = btn.offsetWidth + "px"; k.style.translate = btn.offsetLeft + "px 0";` ersetzen durch `k.style.setProperty("--vx", btn.offsetLeft + "px"); k.style.setProperty("--vw", btn.offsetWidth + "px");`.
3. `css/style.css:1750`: Regel `.nav-line { … }` durch die Ziel-Regel ersetzen (die Folgezeile `@media (max-width: 1180px) { .nav-line { display: none; } }` bleibt).
4. `js/main.js` Abschnitt „Übergang 35“, in `function to(el)`: `line.style.width = (r.width - pad * 2) + "px";` ersetzen durch `line.style.scale = (r.width - pad * 2) + " 1";`.

## Boundaries

- Nur `.vs-knob`, `.nav-line`, `slideKnob` und `to(el)` ändern.
- Klick-/Tastaturlogik der Umschalter (`aria-pressed`, `aria-selected`) NICHT ändern.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`; JS-Syntaxprüfung wie in Plan 003.
- **Feel check**:
  - `aktuelles.html`: Liste ↔ Kalender schnell hin und her: Knopf gleitet in 200 ms, dreht mitten in der Bewegung sauber um, Ecken bleiben 8 px rund.
  - `downloads.html#abo`: Reiter per Pfeiltasten wechseln – Knopf folgt, Text bleibt lesbar (weiß auf dunkel).
  - Computer: mit der Maus über die Menüpunkte fahren – Strich wächst/schrumpft auf Wortbreite ohne Ruckeln.
  - DevTools → Animations auf 10 %: keine `width`-Transition mehr.
- **Done when**: `grep -n "width .35s\|width .25s" css/style.css` findet nichts.
