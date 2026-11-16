# 001 — Fokusrahmen springt sofort statt zu gleiten

- **Status**: DONE
- **Commit**: 1d9b6ec
- **Severity**: HIGH
- **Category**: Purpose & frequency
- **Estimated scope**: 1 file (`css/style.css`), 2 Zeilen

## Problem

Der Fokusrahmen für die Tastatur gleitet bei **jedem Tab-Druck** 220 ms zum nächsten Element. Tastatur-Aktionen gehören zu den häufigsten Bedienungen überhaupt (100+ Mal am Tag für Tastaturnutzer) und dürfen nicht animieren: Wer schnell tabbt, sieht den Rahmen hinterherlaufen, der Fokus wirkt träge. Außerdem werden `width` und `height` animiert (Layout-Eigenschaften).

```css
/* kinderhort-website/css/style.css:1437–1440 — current */
.focus-ring { position: fixed; left: 0; top: 0; z-index: 2000; pointer-events: none; border: 3px solid var(--ink); border-radius: 12px; box-shadow: 0 0 0 4px rgba(212, 181, 176, .55); opacity: 0;
  transition: translate .22s var(--ease-out), width .22s var(--ease-out), height .22s var(--ease-out), opacity .15s; }
.focus-ring.on { opacity: 1; }
.focus-ring.jump { transition: opacity .15s; }
```

Das Skript (`kinderhort-website/js/main.js:1513–1534`, Abschnitt „Gleitender Fokus-Rahmen für die Tastatur“) setzt bei jedem `focusin` `translate`, `width`, `height` und `borderRadius` und schaltet die Klasse `jump` nur beim ersten Fokus ein.

## Target

Der Rahmen steht sofort am neuen Element. Nur das erste Erscheinen und das Verschwinden blenden kurz über (Deckkraft, 150 ms, `ease-out`).

```css
/* target */
.focus-ring { position: fixed; left: 0; top: 0; z-index: 2000; pointer-events: none; border: 3px solid var(--ink); border-radius: 12px; box-shadow: 0 0 0 4px rgba(212, 181, 176, .55); opacity: 0;
  transition: opacity 150ms var(--ease-out); }
.focus-ring.on { opacity: 1; }
.focus-ring.jump { transition: opacity 150ms var(--ease-out); }
```

`--ease-out` ist in `:root` definiert als `cubic-bezier(.23, 1, .32, 1)`.

## Repo conventions to follow

- Bewegungs-Tokens stehen in `:root` am Anfang von `css/style.css` (`--ease-out`, `--ease-in-out`, `--fast`, `--t-enter`, `--t-exit`).
- Vorbild für „nur Deckkraft“: `.focus-ring.jump { transition: opacity .15s; }` (dieselbe Datei).

## Steps

1. In `css/style.css` die Zeile `transition: translate .22s var(--ease-out), width .22s var(--ease-out), height .22s var(--ease-out), opacity .15s; }` ersetzen durch `transition: opacity 150ms var(--ease-out); }`.
2. Die Zeile `.focus-ring.jump { transition: opacity .15s; }` ersetzen durch `.focus-ring.jump { transition: opacity 150ms var(--ease-out); }`.

## Boundaries

- `js/main.js` NICHT ändern (Platzierung, `jump`-Klasse und Scroll-Nachführung bleiben).
- Keine anderen Fokus-Stile anfassen.
- Wenn die Zeilen nicht so im Code stehen (Abweichung seit Commit), STOPP und melden.

## Verification

- **Mechanical**: `cd kinderhort-website && python3 build.py` läuft ohne Fehler.
- **Feel check**: Seite öffnen, mehrfach schnell Tab drücken:
  - Der Rahmen steht bei jedem Tab sofort am neuen Element, ohne Weg dazwischen.
  - Beim ersten Tab blendet er kurz ein; Mausklick blendet ihn aus.
  - DevTools → Animations auf 10 %: Es ist keine `translate`-, `width`- oder `height`-Transition mehr zu sehen.
- **Done when**: `grep -n "focus-ring {" -A1 css/style.css` zeigt nur noch `transition: opacity 150ms var(--ease-out)`.
