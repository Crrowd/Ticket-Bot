# 008 — Kopfleiste wird fester per Deckkraft statt Neuberechnung

- **Status**: DONE
- **Commit**: 1d9b6ec
- **Severity**: MEDIUM
- **Category**: Performance
- **Estimated scope**: 2 files (`css/style.css`, `js/main.js` unverändert), 3 Regeln

## Problem

Beim Scrollen setzt `js/main.js:1953` pro Bild `--hp` (0…1) auf `.site-header`. Daraus berechnet `css/style.css:1760–1761` **Hintergrund und Schatten** der Glasleiste neu – auf einer Ebene mit `backdrop-filter: blur(18px)`. Das erzwingt bei jedem Scroll-Bild ein neues Zeichnen samt Unschärfe dahinter (teuer, besonders auf Handys und in Safari).

```css
/* kinderhort-website/css/style.css:1760–1761 — current */
.header-inner::before { background: rgb(var(--paper-rgb) / calc(.5 + var(--hp, 0) * .3)); box-shadow: 0 1px 0 rgb(var(--ink-rgb) / calc(var(--hp, 0) * .08)), 0 calc(10px + var(--hp, 0) * 8px) calc(30px + var(--hp, 0) * 10px) -18px rgb(var(--deep-rgb) / calc(.3 + var(--hp, 0) * .3)); transition: none; }
.scrolled .header-inner::before { background: rgb(var(--paper-rgb) / calc(.5 + var(--hp, 0) * .3)); box-shadow: 0 1px 0 rgb(var(--ink-rgb) / calc(var(--hp, 0) * .08)), 0 calc(10px + var(--hp, 0) * 8px) calc(30px + var(--hp, 0) * 10px) -18px rgb(var(--deep-rgb) / calc(.3 + var(--hp, 0) * .3)); }
```

```js
// kinderhort-website/js/main.js:1953 — current (bleibt)
function upd() { raf = 0; header.style.setProperty("--hp", Math.min(1, Math.max(0, scrollY / 160)).toFixed(3)); }
```

## Target

Zwei feste Ebenen: `::before` = Glas im Ruhezustand (unverändert aus `css/style.css:141–147`), `::after` = der „feste“ Zustand (Papier 80 %, Linie, tiefer Schatten), dessen **`opacity`** `--hp` folgt. Nur `opacity` ändert sich pro Bild → der Compositor blendet über, nichts wird neu gezeichnet.

```css
/* target – ersetzt die zwei Regeln oben */
.header-inner::after {
  content: ""; position: absolute; inset: 0; z-index: -1; border-radius: inherit; pointer-events: none;
  background: rgb(var(--paper-rgb) / .3);
  box-shadow: 0 1px 0 rgb(var(--ink-rgb) / .08), 0 18px 40px -18px rgb(var(--deep-rgb) / .6);
  opacity: var(--hp, 0);
}
.nav-open .header-inner::after { opacity: 0; }
```

(Papier 50 % aus `::before` + 30 % aus `::after` ergibt optisch die frühere Deckkraft von rund 80 % bei `--hp = 1`.)

## Repo conventions to follow

- Die Glasebene steht in `css/style.css:141–147` (`.header-inner::before { … backdrop-filter: blur(18px) saturate(160%); … }`) – sie bleibt.
- Im Handy-Menü wird die Leiste ausgeblendet über `.nav-open .header-inner::before { opacity: 0; }` (Block `@media (max-width: 1180px)`); die neue Ebene braucht dasselbe.

## Steps

1. `css/style.css:1760–1761`: die beiden zitierten Regeln löschen.
2. Die Regel `.nav-open .header-inner::before { opacity: 0; }` direkt darunter (Zeile 1762) stehen lassen.
3. An derselben Stelle den Ziel-Block einfügen.
4. Prüfen, dass `.header-inner::after` sonst nirgends definiert ist (`grep -n "header-inner::after" css/style.css` → nur die neue Regel).

## Boundaries

- `js/main.js` NICHT ändern (setzt `--hp` weiterhin).
- Ausblenden der Leiste beim Runterscrollen (`.hide`) NICHT ändern.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`.
- **Feel check**:
  - Langsam von ganz oben 200 px runter scrollen: Leiste wird gleichmäßig fester, Schatten wächst, kein Sprung.
  - Handy-Menü öffnen: Leiste verschwindet, nur das Kreuz bleibt (wie vorher).
  - DevTools → Rendering → „Paint flashing“ beim Scrollen: die Kopfleiste blinkt nicht mehr bei jedem Bild.
- **Done when**: `grep -n "calc(.5 + var(--hp" css/style.css` findet nichts.
