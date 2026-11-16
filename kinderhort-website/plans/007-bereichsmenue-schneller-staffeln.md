# 007 — Bereichsmenü: nur Spalten staffeln, Zeilen sofort

- **Status**: TODO
- **Commit**: 1d9b6ec
- **Severity**: MEDIUM
- **Category**: Purpose & frequency
- **Estimated scope**: 1 file (`css/style.css`), 3 Regeln

## Problem

Das große Bereichsmenü (Computer, Überfahren von „Bereiche“) wird täglich oft geöffnet. Spalten **und** jede Zeile darin erscheinen versetzt: Verzögerung = (Spalte + Zeile) × 30 ms. Die letzte Zeile der dritten Spalte startet erst nach (2 + 5) × 30 = 210 ms und ist nach 210 + 250 = 460 ms fertig – bei jedem Überfahren.

```css
/* kinderhort-website/css/style.css:216–221 — current */
.mega-col, .mega-visual, .mega li { opacity: 0; translate: 0 6px; transition: opacity var(--t-drop-exit) var(--ease-out), translate var(--t-drop-exit) var(--ease-out), background var(--fast); }
/* Erst die Spalten, dann ihre Zeilen – jeweils 30 ms versetzt */
.has-drop:is(:hover, :focus-within, .open) :is(.mega-col, .mega-visual, .mega li) { opacity: 1; translate: 0 0; transition-duration: var(--t-enter); transition-delay: calc((var(--c, 0) + var(--r, 0)) * var(--stagger)); }
.mega-col:nth-child(2) { --c: 1; } .mega-col:nth-child(3) { --c: 2; } .mega-visual { --c: 3; }
.mega li:nth-child(1) { --r: 1; } .mega li:nth-child(2) { --r: 2; } .mega li:nth-child(3) { --r: 3; } .mega li:nth-child(4) { --r: 4; } .mega li:nth-child(5) { --r: 5; }
.mega-col:nth-child(2) li { --c: 1; } .mega-col:nth-child(3) li { --c: 2; }
```

## Target

Eine Auftritts-Bewegung pro Spalte; die Zeilen erscheinen mit ihrer Spalte. Versatz 40 ms je Spalte (innerhalb 30–80 ms), Auftritt 200 ms. Letzte Spalte (Bild) fertig nach 3 × 40 + 200 = 320 ms.

```css
/* target */
.mega-col, .mega-visual { opacity: 0; translate: 0 6px; transition: opacity var(--t-drop-exit) var(--ease-out), translate var(--t-drop-exit) var(--ease-out), background var(--fast); }
/* Spalten erscheinen 40 ms versetzt, ihre Zeilen kommen mit */
.has-drop:is(:hover, :focus-within, .open) :is(.mega-col, .mega-visual) { opacity: 1; translate: 0 0; transition-duration: var(--t-drop); transition-delay: calc(var(--c, 0) * 40ms); }
.mega-col:nth-child(2) { --c: 1; } .mega-col:nth-child(3) { --c: 2; } .mega-visual { --c: 3; }
```

Werte: `--t-drop: .2s`, `--t-drop-exit: .14s`, `--ease-out: cubic-bezier(.23, 1, .32, 1)` (alle in `:root`).

## Repo conventions to follow

- Tokens `--t-drop`, `--t-drop-exit`, `--stagger` in `:root` (`css/style.css` oben). `--stagger` wird danach hier nicht mehr gebraucht – NICHT löschen, nur nicht mehr verwenden.

## Steps

1. In `css/style.css` die sechs zitierten Zeilen 216–221 durch die vier Zeilen des Ziels ersetzen.
2. Prüfen, dass `.mega li` sonst keine `opacity: 0` mehr hat (`grep -n "\.mega li" css/style.css`).

## Boundaries

- Handy-Menü (`@media (max-width: 1180px)`-Regeln für `.main-nav .mega…`) NICHT ändern.
- Bildwechsel im Menü (`.mega-visual .mv-x`) NICHT ändern.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`.
- **Feel check** (Computer 1280 px):
  - Über „Bereiche“ fahren: drei Spalten erscheinen kurz nacheinander, alle Links einer Spalte gleichzeitig; nach rund 0,3 s steht alles.
  - Maus schnell rein/raus: Menü kehrt sauber um, keine nachzuckelnden Zeilen.
  - DevTools → Animations auf 10 %: kein Element startet später als 120 ms.
- **Done when**: `grep -n "var(--r, 0)" css/style.css` findet nichts.
