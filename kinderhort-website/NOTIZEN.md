# Offene Punkte & Ideen – Webseite Kinderhort Grombühl

Stand: 13.11.2026

## Design-Stand
- Webseite nutzt aktuell **Entwurf 1 „Salbei & Pfirsich“**.
- Varianten (CSS in `entwurf/designs/`, Screenshots in `entwurf/`):
  1 Salbei & Pfirsich · 2 Vanille & Rosé · 3 Himmel & Sonne · 4 Lavendel & Minze · 5 Sand & Terrakotta ·
  6 Lavendelgrau & Honig · 7 Salbeitürkis & Zitrone · 8 Salbeitürkis & Grau-Rosé ·
  **9 Salbeitürkis, Grau-Rosé & dunkles Türkis** (Karten #2D6A6A, Hintergrund #A8C5C0, Schrift #1E3B44, Akzent #D4B5B0)
- **Entscheidung offen:** welcher Entwurf fest eingebaut wird (Favorit zuletzt: 8/9).

## 1. Vor dem Livegang (Pflicht)
- [ ] Datenschutzerklärung anlegen (Angaben zu Hoster/Verantwortlichen vom Hort)
- [ ] Impressum: TMG-Verweise auf DDG (Digitale-Dienste-Gesetz, seit Mai 2024) umstellen
- [ ] Weiterleitungen alter URLs (`/kinderkrippe/`, `/kindergarten/`, `/kinderhort/`, `/aktuelles/`, `/downloads/`, `/kontakt/`, `/impressum/`, `?page_id=…`) auf die neuen Seiten

## 2. Inhalte – vom Hort benötigt
- [ ] KrippenABC und KindergartenABC (PDF) – fehlen auch auf der alten Seite
- [ ] Abschnitt „Anmeldung & Platzanfrage“ (Ablauf, Ansprechpartner, Besichtigung)
- [ ] Team-Seite (Gruppenleitungen, ggf. Fotos)
- [ ] Öffnungszeiten der Krippe bestätigen (abgeleitet: 6:45–16:30 Uhr)
- [ ] Optional: Konzeption (PDF), Elternbeirat, Stellenangebote
- [ ] Mehr Fotos: Garten, Feste, Team (ohne erkennbare Kindergesichter)

## 3. Pflege & Technik
- [ ] Vergangene Termine automatisch ausblenden
- [ ] Bilder als WebP + `srcset` (Handy lädt ca. halb so viel)
- [ ] SEO: strukturierte Daten (schema.org ChildCare), Open-Graph-Vorschaubild, sitemap.xml
- [ ] `vorschau.html` nach Design-Entscheidung neu erzeugen

## 4. Design-Feinschliff
- [ ] Footer-Logo: grüne Wimpel in Entwurfsfarben umfärben
- [ ] Bei dunklen Karten (Entwurf 9): lange Texte (Elternbrief, Impressum, FAQ-Antworten) hell hinterlegen

## 5. Funktionen (Ideen)
- [ ] „Nächster Schließtag“ auf der Startseite + Hinweis „heute geöffnet/geschlossen“
- [ ] Termine & Schließtage als Kalenderdatei (.ics) zum Übernehmen ins Handy
- [ ] Krankmeldung-Button (E-Mail mit Vorlage: Name, Gruppe, Zeitraum)
- [ ] Platzanfrage als vorausgefüllte E-Mail (kein Server nötig, datensparsam)
- [ ] Wöchentlicher Speiseplan (Bild/PDF hochladen)
- [ ] Termine/Ferienplan aus einer einfachen Datei pflegen, damit das Team ohne Programmierkenntnisse aktualisieren kann (optional einfaches CMS, z. B. Decap CMS)
- [ ] Druckansicht für den Ferienplan
- [ ] Karte mit Zwei-Klick-Lösung (Datenschutz) oder statisches Kartenbild
- [ ] Optional: Elternbereich mit Passwort (Elternbriefe), abhängig vom Webspace
- [ ] Optional: Kerninfos auf Englisch (ggf. weitere Sprachen) für mehrsprachige Familien
