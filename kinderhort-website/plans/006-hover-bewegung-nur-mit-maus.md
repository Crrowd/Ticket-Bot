# 006 — Bewegung beim Überfahren nur mit echter Maus

- **Status**: TODO
- **Commit**: 1d9b6ec
- **Severity**: MEDIUM
- **Category**: Accessibility
- **Estimated scope**: 1 file (`css/style.css`), 6 Regeln verschieben

## Problem

Mehrere Hover-Bewegungen sind nicht auf Geräte mit Maus begrenzt. Auf Touch-Geräten löst ein Antippen ein „falsches Hover“ aus: Die Karte hebt sich an oder das Foto zoomt und **bleibt so stehen**, bis man woanders hintippt.

```css
/* kinderhort-website/css/style.css — current */
/* :349 */ .hero-collage figure:hover { rotate: 0deg; scale: 1.03; z-index: 2; }
/* :453 */ .area-card:hover { translate: 0 -6px; box-shadow: var(--shadow-lg); }
/* :456 */ .area-card:hover .thumb img { scale: 1.06; }
/* :464 */ .area-card:hover .more svg { translate: 5px 0; }
/* :514 */ .room:hover img { scale: 1.05; }
/* :532 */ .tour-item button:hover img { scale: 1.05; }
```

## Target

Alle sechs Regeln stehen unverändert, aber innerhalb von:

```css
/* target */
@media (hover: hover) and (pointer: fine) {
  .hero-collage figure:hover { rotate: 0deg; scale: 1.03; z-index: 2; }
  .area-card:hover { translate: 0 -6px; box-shadow: var(--shadow-lg); }
  .area-card:hover .thumb img { scale: 1.06; }
  .area-card:hover .more svg { translate: 5px 0; }
  .room:hover img { scale: 1.05; }
  .tour-item button:hover img { scale: 1.05; }
}
```

## Repo conventions to follow

- Die Datei nutzt diese Abfrage schon, z. B. im Block „Übergang 31 – Karten heben sich an“: `@media (hover: hover) { .teaser:hover, .room:not(.no-img):hover { … } }` und „Idee 92“: `@media (hover: hover) and (pointer: fine) { … .area-card.tilt … }`.

## Steps

1. Jede der sechs Regeln an ihrer Stelle in `css/style.css` löschen (Zeilen 349, 453, 456, 464, 514, 532 – Inhalt wie oben zitiert).
2. Am Ende von `css/style.css` den Ziel-Block (mit Kommentar `/* Hover-Bewegung nur mit echter Maus (Touch löst falsches Hover aus) */`) anfügen. Am Dateiende stehen sie nach allen bisherigen Regeln, die Reihenfolge der Kaskade bleibt also gewahrt.

## Boundaries

- Werte NICHT ändern, nur verschieben.
- Andere `:hover`-Regeln (Farbwechsel ohne Bewegung) nicht anfassen.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`; in `css/style.css` stehen die sechs Selektoren genau einmal (innerhalb des neuen Blocks).
- **Feel check**:
  - Computer (1280 px, Maus): Bereichskarten heben sich an, Fotos zoomen wie vorher.
  - Handy-Emulation mit Touch (iPhone 13 in Playwright/DevTools): Bereichskarte antippen und zurück navigieren – keine Karte bleibt angehoben, kein Foto bleibt vergrößert.
- **Done when**: `grep -n "^\.area-card:hover {" css/style.css` findet nichts mehr außerhalb des Medien-Blocks.
