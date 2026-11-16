# Animations-Pläne

Erstellt mit `improve-animations` (Emil Kowalskis Bewegungs-Philosophie) am 16.11.2026, Commit `1d9b6ec`.
Jeder Plan ist eigenständig ausführbar: genaue Stellen, aktueller Code, Zielwerte, Schritte, Grenzen und Fühl-Prüfung.

| # | Titel | Stufe | Status |
|---|---|---|---|
| [001](001-fokusrahmen-ohne-gleiten.md) | Fokusrahmen springt sofort statt zu gleiten | HIGH | DONE |
| [002](002-kalender-wechsel-ohne-ease-in.md) | Liste/Kalender: Abgang mit ease-out statt ease-in | HIGH | DONE |
| [003](003-sprungmarken-marker-ohne-width.md) | Sprungmarken-Marker: clip-path statt width, 250 ms | MEDIUM | DONE |
| [004](004-umschalter-und-menue-strich-ohne-width.md) | Umschalter-Knopf und Menü-Strich ohne width-Animation | MEDIUM | DONE |
| [005](005-kurzmeldungen-unterbrechbar.md) | Kurzmeldungen per Transition statt Keyframes | MEDIUM | DONE |
| [006](006-hover-bewegung-nur-mit-maus.md) | Bewegung beim Überfahren nur mit echter Maus | MEDIUM | DONE |
| [007](007-bereichsmenue-schneller-staffeln.md) | Bereichsmenü: nur Spalten staffeln, Zeilen sofort | MEDIUM | DONE |
| [008](008-kopfleiste-nur-deckkraft.md) | Kopfleiste wird fester per Deckkraft | MEDIUM | DONE |
| [009](009-viewport-werte-nur-bei-aenderung.md) | Viewport-Werte nur bei echter Änderung schreiben | LOW | DONE |
| [010](010-eine-ease-out-kurve.md) | Eine ease-out-Kurve, JS liest die Tokens | LOW | DONE |

## Empfohlene Reihenfolge

1. **001, 002** – klein, größte Wirkung auf das Gefühl.
2. **006, 005, 007** – je eine Datei, unabhängig voneinander.
3. **003, dann 004** – 004 übernimmt die `clip-path`-Technik aus 003.
4. **008, 009** – Leistung beim Scrollen.
5. **010** zuletzt – es ändert `--io`, das in vielen Regeln steckt; nach den anderen Plänen ist die Prüfung am einfachsten.

## Abhängigkeiten

- 004 baut auf dem Muster von 003 auf (gleiche Technik, andere Stellen) – getrennt ausführbar, aber nacheinander leichter zu prüfen.
- 002 und 010 berühren beide Kurven im JavaScript: 002 nutzt `EASE_OUT`, 010 lässt `EASE_OUT` aus dem CSS lesen – in dieser Reihenfolge ausführen.
- Nach jedem Plan: `python3 build.py` und die Vorschau neu bauen (`python3 build_vorschau.py`).
