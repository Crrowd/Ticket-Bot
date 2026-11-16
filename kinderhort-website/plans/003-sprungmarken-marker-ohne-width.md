# 003 — Sprungmarken-Marker: clip-path statt width, 250 ms

- **Status**: DONE
- **Commit**: 1d9b6ec
- **Severity**: MEDIUM
- **Category**: Performance + Easing & duration
- **Estimated scope**: 2 files (`css/style.css`, `js/main.js`), ca. 10 Zeilen

## Problem

Der rosé Marker in den Sprungmarken unter dem Seitenkopf (Bereichsseiten) gleitet beim Scrollen von Eintrag zu Eintrag. Er animiert `width` (Layout-Eigenschaft, kostet bei jedem Bild Layout + Paint) und braucht 380 ms – über dem UI-Budget von höchstens 300 ms. Weil der Marker beim Scrollen ständig mitläuft (Scroll-Spy), ist das eine sehr häufige Bewegung. Zusätzlich startet bei jedem Wechsel eine `@keyframes`-Dehnung neu (nicht unterbrechbar).

```css
/* kinderhort-website/css/style.css:433–437 — current */
.subnav-knob { position: absolute; left: 0; top: 0; z-index: 0; width: var(--kw, 0px); height: var(--kh, 0px); translate: var(--kx, 0px) var(--ky, 0px); border-radius: 12px; background: var(--rose); box-shadow: 0 4px 12px -6px rgb(var(--deep-rgb) / .5); opacity: 0; list-style: none; pointer-events: none;
  transition: translate .38s var(--ease-in-out), width .38s var(--ease-in-out), opacity .2s; }
.subnav-knob.on { opacity: 1; }
.subnav-knob.moving { animation: knob-stretch .38s var(--ease-in-out); }
@keyframes knob-stretch { 45% { scale: 1.12 .94; } }
```

```js
// kinderhort-website/js/main.js:127–138 — current (function knobTo)
function knobTo(ul, a) {
  var k = $(".subnav-knob", ul), first = !k;
  if (first) { k = document.createElement("li"); k.className = "subnav-knob"; k.setAttribute("aria-hidden", "true"); ul.insertBefore(k, ul.firstChild); }
  var moved = !first && k.style.getPropertyValue("--kx") !== a.offsetLeft + "px";
  if (first) k.style.transition = "none";
  k.style.setProperty("--kx", a.offsetLeft + "px");
  k.style.setProperty("--ky", a.offsetTop + "px");
  k.style.setProperty("--kw", a.offsetWidth + "px");
  k.style.setProperty("--kh", a.offsetHeight + "px");
  if (first) { void k.offsetWidth; k.style.transition = ""; k.classList.add("on"); }
  else if (moved && !reduced) { k.classList.remove("moving"); void k.offsetWidth; k.classList.add("moving"); }
}
```

Hinweis: In derselben Datei überschreibt ein späterer Block die Rundung: `.subnav a, .subnav .sn-knob { border-radius: 14px; }` – die Rundung des Markers soll 14 px sein (20 px Leiste − 6 px Innenabstand).

## Target

Der Marker ist so breit wie der ganze Inhalt der Leiste und wird per `clip-path` auf den aktiven Eintrag zugeschnitten. `clip-path` ist die dokumentierte Ausnahme neben `transform`/`opacity`. Dauer 250 ms, Kurve `var(--ease-in-out)` (= `cubic-bezier(.65, 0, .35, 1)`, Bewegung auf dem Bildschirm). Keine Dehnungs-Keyframes mehr; der Schatten entfällt (er würde vom Zuschnitt abgeschnitten).

```css
/* target */
.subnav-knob { position: absolute; left: 0; top: var(--ky, 0px); z-index: 0; width: var(--sw, 0px); height: var(--kh, 0px); background: var(--rose); opacity: 0; list-style: none; pointer-events: none;
  clip-path: inset(0 calc(var(--sw, 0px) - var(--kx, 0px) - var(--kw, 0px)) 0 var(--kx, 0px) round 14px);
  transition: clip-path 250ms var(--ease-in-out), opacity 200ms var(--ease-out); }
.subnav-knob.on { opacity: 1; }
```

```js
// target (function knobTo) – nur Änderungen: --sw setzen, keine "moving"-Klasse
k.style.setProperty("--sw", ul.scrollWidth + "px");
k.style.setProperty("--kx", a.offsetLeft + "px");
k.style.setProperty("--ky", a.offsetTop + "px");
k.style.setProperty("--kw", a.offsetWidth + "px");
k.style.setProperty("--kh", a.offsetHeight + "px");
if (first) { void k.offsetWidth; k.style.transition = ""; k.classList.add("on"); }
```

## Repo conventions to follow

- Tokens in `:root` (`css/style.css` oben): `--ease-in-out: cubic-bezier(.65, 0, .35, 1)`, `--ease-out: cubic-bezier(.23, 1, .32, 1)`.
- Vorbild für `clip-path`-Übergänge: `css/style.css:997` (`.js .reveal … clip-path: inset(0 0 0 0); transition: clip-path .8s var(--ease-out)`).
- Reduced-Motion-Regel `css/style.css:1024` (`.subnav-knob, .subnav-knob.moving … transition: none !important`) bleibt bestehen.

## Steps

1. `css/style.css`: Die zwei Zeilen der Regel `.subnav-knob { … transition: … opacity .2s; }` (Zeilen 433–434) durch die Ziel-Regel ersetzen.
2. `css/style.css`: Die Zeilen `.subnav-knob.moving { animation: knob-stretch .38s var(--ease-in-out); }` und `@keyframes knob-stretch { 45% { scale: 1.12 .94; } }` löschen.
3. `css/style.css`: Den Kommentar darüber (`/* Gleitender Marker: bewegt sich mit ease-in-out und dehnt sich unterwegs um 12 % */`) ersetzen durch `/* Gleitender Marker: per clip-path auf den aktiven Eintrag zugeschnitten (kein Layout) */`.
4. `js/main.js` in `knobTo`: vor `k.style.setProperty("--kx", …)` die Zeile `k.style.setProperty("--sw", ul.scrollWidth + "px");` einfügen.
5. `js/main.js` in `knobTo`: die Zeile `else if (moved && !reduced) { k.classList.remove("moving"); void k.offsetWidth; k.classList.add("moving"); }` löschen und die Variable `moved` samt ihrer Zeile `var moved = …` entfernen.

## Boundaries

- Nur `.subnav-knob`-Regeln und die Funktion `knobTo` ändern.
- Die Regel `.subnav:not(:has(.subnav-knob.on)) a[aria-current="true"]` (Fallback ohne Skript) NICHT ändern.
- Keine Markup-Änderungen in `build.py`.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`; JS-Syntax mit `node -e "new Function(require('fs').readFileSync('js/main.js','utf8'))"` prüfen.
- **Feel check** auf `kinderhort.html` (Computer 1280 px und Handy 390 px):
  - Langsam scrollen: Der Marker gleitet in 250 ms zum nächsten Eintrag, ohne Dehnung, Ecken bleiben 14 px rund.
  - Sprungmarke anklicken während der Marker noch läuft: er dreht sauber um, kein Neustart.
  - Am Handy seitlich wischen (Leiste scrollt): Marker bleibt am Eintrag.
  - DevTools → Performance beim Scrollen: keine „Layout“-Einträge durch den Marker.
- **Done when**: `grep -n "knob-stretch\|width .38s" css/style.css` findet nichts.
