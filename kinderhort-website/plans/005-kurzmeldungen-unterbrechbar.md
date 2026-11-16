# 005 — Kurzmeldungen erscheinen per Transition statt Keyframes

- **Status**: TODO
- **Commit**: 1d9b6ec
- **Severity**: MEDIUM
- **Category**: Interruptibility
- **Estimated scope**: 1 file (`css/style.css`), 3 Zeilen

## Problem

Kurzmeldungen („Link kopiert“, „Hinweis ausgeblendet · Rückgängig“) erscheinen über `@keyframes`. Keyframes starten bei jeder Unterbrechung von null; kommen zwei Meldungen schnell hintereinander oder wird eine sofort wieder geschlossen, springt der Auftritt. Der Abgang nutzt bereits Transitions – Auftritt und Abgang sind also uneinheitlich.

```css
/* kinderhort-website/css/style.css:823 — current (Ausschnitt) */
.toast { … animation: toast-in var(--t-enter) var(--ease-out) both; transition: opacity var(--t-exit) var(--ease-out), translate var(--t-exit) var(--ease-out), scale var(--t-exit) var(--ease-out); }
.toast.leaving { opacity: 0; translate: 0 8px; scale: .95; }
/* :829 */
@keyframes toast-in { from { opacity: 0; translate: 0 16px; scale: .95; } }
```

## Target

Auftritt per `@starting-style` + Transition (unterbrechbar, kehrt aus dem aktuellen Zustand um). Werte: Auftritt `var(--t-enter)` (= 250 ms), Abgang `var(--t-exit)` (= 200 ms), Kurve `var(--ease-out)` (= `cubic-bezier(.23, 1, .32, 1)`), Start `opacity: 0; translate: 0 16px; scale: .95` (nie `scale(0)`).

```css
/* target */
.toast { … transition: opacity var(--t-enter) var(--ease-out), translate var(--t-enter) var(--ease-out), scale var(--t-enter) var(--ease-out); }
@starting-style { .toast { opacity: 0; translate: 0 16px; scale: .95; } }
.toast.leaving { opacity: 0; translate: 0 8px; scale: .95; transition-duration: var(--t-exit); }
```

(„…“ = alle übrigen Deklarationen der Regel unverändert lassen.)

## Repo conventions to follow

- `@starting-style` wird schon verwendet: `css/style.css` bei `.app-dialog[open]` (`@starting-style { .app-dialog[open] { opacity: 0; scale: .95; translate: 0 8px; } }`).
- Tokens `--t-enter: .25s; --t-exit: .2s;` in `:root`.

## Steps

1. `css/style.css:823`: in der Regel `.toast { … }` den Teil `animation: toast-in var(--t-enter) var(--ease-out) both; ` entfernen und `transition: …` ersetzen durch `transition: opacity var(--t-enter) var(--ease-out), translate var(--t-enter) var(--ease-out), scale var(--t-enter) var(--ease-out);`.
2. Direkt danach einfügen: `@starting-style { .toast { opacity: 0; translate: 0 16px; scale: .95; } }`.
3. Regel `.toast.leaving { opacity: 0; translate: 0 8px; scale: .95; }` ersetzen durch `.toast.leaving { opacity: 0; translate: 0 8px; scale: .95; transition-duration: var(--t-exit); }`.
4. Zeile `@keyframes toast-in { from { opacity: 0; translate: 0 16px; scale: .95; } }` löschen.

## Boundaries

- `js/main.js` (Funktion `toast`) NICHT ändern – sie setzt `.leaving` und entfernt nach 200 ms.
- Die Reduced-Motion-Regeln (`.toast { animation: none !important; }` und `.toast { animation: rm-fade .2s ease both !important; }`) NICHT ändern.
- Bei Abweichung STOPP und melden.

## Verification

- **Mechanical**: `python3 build.py`.
- **Feel check**:
  - `kontakt.html`: E-Mail-Adresse mehrfach schnell kopieren – jede Meldung gleitet von unten ein, keine springt.
  - `index.html`: Hinweis-Banner ausblenden, sofort „Rückgängig“ – die Meldung kehrt mitten im Auftritt sauber um.
  - DevTools → Animations auf 10 %: Auftritt ist eine Transition (keine Keyframe-Animation „toast-in“).
  - Rendering → `prefers-reduced-motion: reduce`: Meldung blendet nur ein, ohne Bewegung.
- **Done when**: `grep -n "toast-in" css/style.css` findet nichts.
