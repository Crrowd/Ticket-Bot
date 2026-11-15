# Offene Punkte & Ideen – Webseite Kinderhort Grombühl

Stand: 13.11.2026

## Design-Stand
- Webseite nutzt **Entwurf 9** (Salbeitürkis, Grau-Rosé, dunkles Türkis) – fest eingebaut.
- Varianten (CSS in `entwurf/designs/`, Screenshots in `entwurf/`):
  1 Salbei & Pfirsich · 2 Vanille & Rosé · 3 Himmel & Sonne · 4 Lavendel & Minze · 5 Sand & Terrakotta ·
  6 Lavendelgrau & Honig · 7 Salbeitürkis & Zitrone · 8 Salbeitürkis & Grau-Rosé ·
  **9 Salbeitürkis, Grau-Rosé & dunkles Türkis** (Karten #2D6A6A, Hintergrund #A8C5C0, Schrift #1E3B44, Akzent #D4B5B0)


## 1. Vor dem Livegang (Pflicht)
- [x] Datenschutzerklärung anlegen – Vorlage steht; **offen: Hoster, Datenschutzbeauftragte/r, Aufsicht, Datum ergänzen und prüfen lassen**
- [x] Impressum: TMG-Verweise auf DDG (Digitale-Dienste-Gesetz, seit Mai 2024) umstellen
- [x] Weiterleitungen alter URLs (`/kinderkrippe/`, `/kindergarten/`, `/kinderhort/`, `/aktuelles/`, `/downloads/`, `/kontakt/`, `/impressum/`, `?page_id=…`) auf die neuen Seiten

## 2. Inhalte – vom Hort benötigt
- [ ] KrippenABC und KindergartenABC (PDF) – fehlen auch auf der alten Seite
- [ ] Abschnitt „Anmeldung & Platzanfrage“ (Ablauf, Ansprechpartner, Besichtigung)
- [ ] Team-Seite (Gruppenleitungen, ggf. Fotos)
- [ ] Öffnungszeiten der Krippe bestätigen (abgeleitet: 6:45–16:30 Uhr)
- [ ] Optional: Konzeption (PDF), Elternbeirat, Stellenangebote
- [ ] Mehr Fotos: Garten, Feste, Team (ohne erkennbare Kindergesichter)

## 3. Pflege & Technik
- [x] Vergangene Termine automatisch ausblenden
- [x] Bilder als WebP + `srcset` (Handy lädt ca. halb so viel)
- [x] SEO: strukturierte Daten (schema.org ChildCare), Open-Graph-Vorschaubild, sitemap.xml
- [x] `vorschau.html` nach Design-Entscheidung neu erzeugen

## 4. Design-Feinschliff
- [x] Footer-Logo: grüne Wimpel in Entwurfsfarben umfärben
- [x] Bei dunklen Karten (Entwurf 9): lange Texte (Elternbrief, Impressum, FAQ-Antworten) hell hinterlegen

## 5. Funktionen (Ideen)
- [x] „Nächster Schließtag“ auf der Startseite + Hinweis „heute geöffnet/geschlossen“
- [x] Termine & Schließtage als Kalenderdatei (.ics) zum Übernehmen ins Handy
- [x] Krankmeldung-Button (E-Mail mit Vorlage: Name, Gruppe, Zeitraum)
- [x] Platzanfrage als vorausgefüllte E-Mail (kein Server nötig, datensparsam)
- [ ] Wöchentlicher Speiseplan (Bild/PDF hochladen)
- [x] Termine/Ferienplan aus einer einfachen Datei pflegen, damit das Team ohne Programmierkenntnisse aktualisieren kann (optional einfaches CMS, z. B. Decap CMS)
- [x] Druckansicht für den Ferienplan
- [ ] Karte mit Zwei-Klick-Lösung (Koordinaten der Einrichtung nötig) (Datenschutz) oder statisches Kartenbild
- [ ] Optional: Elternbereich mit Passwort (Elternbriefe), abhängig vom Webspace
- [ ] Optional: Kerninfos auf Englisch (ggf. weitere Sprachen) für mehrsprachige Familien

## Hinweise
- Status-Anzeige kennt Schließzeiten nur bis Ende des aktuellen Ferienplans; danach Hinweis „Ferienplan folgt“. Neuen Plan in `daten/schliesstage.csv` eintragen, Feiertage in `daten/feiertage.csv` ergänzen.
- Speiseplan: Bild/PDF vom Hort nötig.

## Feinschliff (14.11.2026)
- Stylesheet neu aufgebaut (eine saubere Datei statt übereinanderliegender Entwurfs-Schichten), Farben unverändert.
- Schriften: Fraunces (Überschriften) + Figtree (Text), lokal eingebunden.
- Animationen: Auftakt der Startseite, sanftes Einblenden beim Scrollen, weicher Seitenwechsel, Fragen klappen weich auf, Bildansicht blendet ein. Bei „Bewegung reduzieren“ im Gerät sind alle Animationen aus.
- Prüfung: axe-core (Barrierefreiheit/Kontrast) auf allen 9 Seiten in Desktop- und Handybreite ohne Befund; keine JavaScript-Fehler, keine defekten Bilder oder Links.

## Struktur, Schrift und die 40 UX-/UI-Prinzipien (15.11.2026)
- Schrift: Plus Jakarta Sans, überall mit gleich breiten Ziffern (`font-variant-numeric: tabular-nums` – entspricht „Plus Jakarta Sans Tab“).
- Navigation von 8 auf 5 Punkte: Startseite · Bereiche (Krippe, Kindergarten, Hort, Rundgang) · Aktuelles · Downloads · Kontakt, dazu Suche.
- Startseite neu geordnet: Auftakt mit Status → Hinweis nächster Termin → Bereiche → Kennzahlen → Begrüßung → Rundgang → Termine & Unterlagen → Ferienplan → Kontakt.
- Bereichsseiten: mitlaufende Sprungmarken-Leiste mit Markierung des aktuellen Abschnitts; Vorzüge in je 3 Gruppen.
- Handy: Leiste unten mit Anrufen, Krankmelden, Termine, Suche.

| Prinzip | Umsetzung |
|---|---|
| Skeleton loaders | Schimmer-Platzhalter in der Bildansicht, bis das Foto geladen ist |
| Optimistic updates | Kopieren-Knopf zeigt den Erfolg sofort; sonst nicht anwendbar (Seite speichert nichts auf einem Server) |
| Command menu | Schnellsuche über alle Seiten, Abschnitte, Downloads (Strg/⌘ + K oder „/“) |
| Shortcut hints | Tastenhinweise an Suche und Bildansicht |
| Undo toasts | Hinweis „Nächster Termin“ ausblenden → Meldung mit „Rückgängig“ |
| Stale-while-revalidate | Service Worker (`sw.js`): Bilder/Schriften/CSS sofort aus dem Speicher, im Hintergrund aufgefrischt; Seiten immer frisch |
| Pre-rendering | Statische Seiten + Speculation Rules (Zielseite wird beim Überfahren vorbereitet) |
| BlurHash placeholders | Unscharfe Mini-Vorschau hinter jedem Foto |
| View transitions | Weicher Seitenwechsel |
| Swipe-to-dismiss sheets | Suche als Blatt von unten (Handy) und Bildansicht: nach unten wischen schließt |
| Interruptible animations | Alle Bedien-Animationen sind CSS-Übergänge und jederzeit unterbrechbar |
| Predictive back | „Zurück“ schließt Bildansicht, Suche und Menü statt die Seite zu verlassen |
| Hit slop / Bigger hit areas / Fitts | Vergrößerte Trefferflächen kleiner Links, große Hauptknöpfe, Handy-Leiste in Daumenreichweite |
| Safe area insets | Ränder für Aussparung und Systemleisten (`viewport-fit=cover`, `env()`) |
| One-time code autofill | Nicht anwendbar – kein Login, keine Formulare |
| Tabular numbers | Überall gleich breite Ziffern |
| Balanced headlines | `text-wrap: balance` für Überschriften |
| Continuous corners | `corner-shape: squircle`, wo der Browser es unterstützt |
| Idempotency keys | Nicht anwendbar – keine Server-Anfragen, die doppelt ausgeführt werden könnten |
| Amazon safe triangle | Aufklappmenü bleibt beim schrägen Hinfahren offen (Brücke + kurze Schonfrist) |
| Squash & stretch / Exaggerated feedback | Knöpfe geben beim Drücken nach, Kopieren-Knopf und Plakette federn |
| Anticipation / Follow through / Slow in & out / Arcs | Auftakt: Fotos legen sich in einem Bogen ab und schwingen leicht nach |
| Staging / Pose to pose | Ein klarer Schwerpunkt je Ansicht; Überlagerungen dunkeln den Rest ab |
| Secondary action | Pfeile und Bildzoom begleiten das Anheben der Karten |
| Snappy timing / Doherty threshold | Rückmeldungen in ca. 0,2 s, Nachbarbild wird vorgeladen |
| Solid drawing / Appeal | Einheitliche Schatten-Ebenen, überlappende Fotos |
| Hick's law | 5 statt 8 Menüpunkte, 4 Wege in der Handy-Leiste |
| Miller's law | Vorzüge in Gruppen mit höchstens 5 Punkten, Startseite zeigt 3 Termine |
| Postel's law | Suche verzeiht Groß/Klein, Umlaute, ß und Tippfehler („Ferein“) |
| Jakob's law | Vertraute Muster: Logo führt zur Startseite, Menü oben, Kontakt rechts, Fußbereich mit Seitenübersicht |
| Frequency of use | Häufigstes zuerst: Öffnungsstatus, Krankmelden, Anrufen, Termine |

Hinweis: Service Worker und vorbereitende Seitenaufrufe wirken nur auf einem Webserver (https), nicht beim Öffnen der Datei vom Computer.

## 20 Gestaltungsbegriffe (15.11.2026)

| Begriff | Umsetzung |
|---|---|
| Kerning | Für Fließtext an; für Versal-Etiketten und Ziffernspalten aus, damit Zahlen exakt untereinander stehen |
| Optical centre | Plakette, Plus-Zeichen, Pfeile und Bildansicht sitzen leicht über bzw. neben der rechnerischen Mitte |
| Tabular numbers | Überall gleich breite Ziffern |
| Layout shift | Platz für Status-Karte und Terminhinweis wird freigehalten, Ersatzschrift hat angeglichene Maße; gemessen: CLS 0,000–0,003 (gut ist < 0,1) |
| Tracking | Große Überschriften enger, kleine Schrift und Versalien weiter |
| Optimistic update | Kopieren-Knopf bestätigt sofort (sonst speichert die Seite nichts) |
| x-height | Ersatzschrift auf 104,8 % skaliert – Breite und x-Höhe passen zur Hausschrift |
| Touch target | Mindestens 44 px: Sprungmarken, Knöpfe, vergrößerte Trefferflächen kleiner Links |
| Leading | Überschriften 1,06–1,14 · Text 1,62 · lange Lesetexte 1,72 |
| Origin-aware animation | Bildansicht wächst aus dem angeklickten Foto, Handy-Menü aus dem Menü-Knopf, Aufklappmenü aus seinem Menüpunkt |
| OKLCH | Dieselben Farben als OKLCH; Abstufungen (hell/dunkel) werden aus den Grundfarben berechnet |
| Widow | `text-wrap: pretty/balance` gegen einzelne Wörter in der letzten Zeile |
| Safe area | Ränder für Aussparung und Systemleisten |
| Stagger | Karten, Auftakt und Menüeinträge erscheinen leicht versetzt |
| Line length | Lesetexte höchstens 60–70 Zeichen je Zeile |
| Affordance | Vergrößerbare Fotos tragen ein Lupen-Zeichen, Links in Texten sind unterstrichen |
| Combobox | Suche folgt dem ARIA-Combobox-Muster (Vorlesehilfen sagen Treffer und Auswahl an) |
| Interruptible animation | Bedien-Animationen sind Übergänge und jederzeit unterbrechbar |
| Progressive disclosure | Gruß der Leitung zeigt zwei Absätze, Rest per „Den ganzen Gruß lesen“; Fragen klappen auf; Startseite zeigt 3 Termine |
| Shared element transition | Foto der Bereichskarte wird beim Seitenwechsel zum Kopfbild der Bereichsseite (nur auf dem Webserver, in Browsern mit View Transitions) |

Dafür geändert: Kopfbild der Kindergarten-Seite ist jetzt dasselbe Foto wie auf der Startseiten-Karte.

## Kopfleiste (15.11.2026)
- Schwebende, abgerundete Leiste aus Milchglas (Abstand zum Rand, 8 px Innenabstand, Unschärfe des Hintergrunds).
- „Bereiche“ öffnet ein großes Menü in voller Leistenbreite: 3 Spalten mit Sprungzielen, 4. Spalte zeigt das Foto des überfahrenen Bereichs.
- Sprungmarken der Bereichsseiten als eigene Glas-Leiste darunter.
- `view-transition-name` an der Leiste entfernt (ließ Inhalte durchscheinen).
