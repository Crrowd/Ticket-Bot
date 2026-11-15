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

## Bewegungssystem: 20 Animationsregeln + Lade-Regeln (16.11.2026)

| Regel | Umsetzung |
|---|---|
| Ease-out für Auftritte | Eigene Kurve `--ease-out` (cubic-bezier(.23, 1, .32, 1)) für alles, was erscheint |
| Aufklappmenüs 150–250 ms | Großes Menü: 200 ms auf, 160 ms zu |
| Listen 30 ms versetzt | Einblenden beim Scrollen, Menüspalten und -zeilen, Suchtreffer |
| Beim Drücken auf 0,97 | Alle Knöpfe, Karten-Links, Menüpunkte |
| Bewegter Marker dehnt sich 12 % | Gleitender Marker in der Sprungmarken-Leiste |
| Versetzt, bis Details sitzen | Menü: Spalten, dann Zeilen; Bildansicht: Bild, dann Unterschrift |
| Bewegung im Bogen | Fotos der Startseite fliegen im Bogen ein (x und y mit verschiedenen Kurven) |
| Puls bestätigt Erfolg | Kopieren-Knopf und Häkchen in Kurzmeldungen pulsieren einmal |
| Ease-in-out für Bewegungen | Marker, Bildflug, Handy-Menü beim Schließen |
| Aufklappendes startet bei 0,95 | Großes Menü, Suche, Kurzmeldungen |
| Aus dem Auslöser heraus | Menü wächst aus „Bereiche“, Suche aus dem Suchknopf, Bild aus der Vorschau |
| Zum Auslöser zurück | Bild fliegt beim Schließen in seine Vorschau zurück (Rundgang scrollt notfalls hin), Handy-Menü schrumpft in den Knopf |
| Kein Federn im Alltag | Alle Überschwinger entfernt |
| Nicht animieren, solange gehalten | Wischen: Bild und Suchblatt folgen dem Finger 1:1 ohne Übergang |
| Abgänge 20 % kürzer | 250 ms rein / 200 ms raus (Menü 200/160, Bild 380/300, Handy-Menü 500/400) |
| Alt und Neu überlappen | Beim Blättern in der Bildansicht blendet das alte Bild aus, während das neue einblendet |
| Masken für Aufdecken und Farbe | Fotos werden beim Scrollen per Maske aufgedeckt; umrandete Knöpfe füllen sich per Maske |
| Symbole überblenden mit Unschärfe | Kopieren-Symbol → Häkchen |
| Gummiband an Grenzen | Rundgang-Pfeile am Anfang/Ende, Bild und Suchblatt beim Ziehen über die Grenze |
| Dasselbe Element wiederverwenden | Vorschaubild wird zum großen Bild (FLIP); Bereichskarte wird Kopfbild; ein Marker für alle Sprungmarken |

| Ladezeit | Umsetzung |
|---|---|
| unter 1 s | nichts zeigen: Ladeanzeige der Bildansicht erscheint erst nach 1 s; vorhandenes Vorschaubild wird sofort gezeigt |
| 1–10 s | Gerüst: schimmernder Platzhalter in der Bildansicht, unscharfe Mini-Vorschau hinter jedem Foto |
| über 10 s | kommt auf der Seite nicht vor (größte Datei ca. 0,5 MB); PDF-Downloads zeigt der Browser selbst mit Fortschritt |
| Antippen | erst anzeigen, dann erledigen: Kopieren, Hinweis ausblenden |

Außerdem: Räume ohne Foto stehen gesammelt in einer eigenen Zeile, bei ungerader Zahl ist der letzte Raum mit Foto breit.

## Leiste und Tastatur (16.11.2026)
- Kopfleiste verschwindet beim Runterscrollen (ab 120 px, nach 24 px in eine Richtung) und kommt beim Hochscrollen (12 px) zurück; Sprungmarken rücken dann nach oben. Bleibt sichtbar bei offenem Menü, Suche, Bildansicht und Tastaturfokus.
- Handy-Tastatur: Höhe wird über `visualViewport` gemessen; Suchblatt sitzt direkt über der Tastatur, Schnellzugriff-Leiste wird ausgeblendet, Kurzmeldungen rücken hoch. Android/Chrome zusätzlich über `interactive-widget=resizes-content`.

## Ideenkatalog – Entscheidung (16.11.2026)
Katalog: `entwurf/ideen/ideen.html` (private Vorschau: https://claude.ai/artifact/K4pRXWzjjUMzevc4t5RsS3)

**Eingebaut**
- [x] 2 Termine merken – „Merken“ an jedem Termin (Startseite, Aktuelles); Datum fliegt im Bogen zum Zähler an „Aktuelles“ (Computer) bzw. „Termine“ (Handy); gemerkte Termine bleiben im Browser gespeichert und lassen sich als Kalenderdatei laden; Meldung mit „Rückgängig“.
- [x] 3 Kita-Jahr als Zeitstrahl – über jeder Ferienplan-Tabelle; Schließzeiten aus `daten/schliesstage.csv`, „heute“-Linie, Zeiger ziehbar (Gummiband an den Enden) und per Pfeiltasten/Bild↑↓/Pos1/Ende bedienbar.
- [x] 8 Fragen durchsuchen – Suchfeld über den häufigen Fragen; sucht in Frage und Antwort, verzeiht Umlaute, markiert den Begriff, Treffer rücken weich zusammen; Esc leert.
- [x] 9 Lesefortschritt und „Nach oben“ – auf langen Seiten (über 2,2 Bildschirmhöhen) dünner Balken oben; ab einem Drittel Knopf mit Fortschrittsring; weicht am Handy Kurzmeldungen aus.
- [x] 12 Laden nach Dauer – Seitenwechsel: unter 1 s nichts, ab 1 s Ladebalken oben, ab 10 s Hinweis „Verbindung langsam“; Bildansicht wie gehabt.

**Gemerkt für später**
- [ ] 5 Krankmeldung in drei Tipps (Gruppe → Zeitraum → Bestätigen). Braucht einen echten Versandweg (Formular-Postfach beim Hoster oder datenschutzkonformer Formulardienst) – bis dahin bleibt die vorbereitete E-Mail.
- [ ] 7 Rundgang über den Grundriss. Braucht einen echten Grundriss des Hauses (Skizze reicht) und die Zuordnung der Fotos zu den Räumen.

**Nicht gewünscht:** 1 Öffnungsuhr, 4 Tagesablauf in Echtzeit, 6 Speiseplan-Stapel, 10 Schriftgröße, 11 Mehrsprachigkeit.

## Ideenkatalog 2 – Entscheidung (16.11.2026)
Katalog: `entwurf/ideen/ideen-2.html`, Bildschirmfotos der Umsetzung: `entwurf/runde2/`

**Eingebaut**
- [x] 1 Überschriften steigen Wort für Wort auf (Abschnittsüberschriften; Vorleser hören den ganzen Satz).
- [x] 2 Zahlen zählen hoch (Kennzahlen der Bereiche, sobald sichtbar).
- [x] 3 Rollende Ziffern bei „in N Tagen“ (Hinweisleiste, Kita-Jahr-Zeitstrahl).
- [x] 4 Licht folgt der Maus auf den dunklen Karten (nur Computer).
- [x] 5 Magnet-Knöpfe – bewusst schwach (max. ~10–14 % des Abstands, nur im Umkreis von 90 px, nur Computer).
- [x] 7 Wimpelkette im Fuß wiegt beim Scrollen (Federbewegung).
- [x] 9 Fachbegriffe erklären sich (Klick → kleine Erklärung wächst aus dem Wort). **Texte habe ich formuliert – bitte vom Hort prüfen lassen:** BayKiBiG, Inhouseschulungen, Portfolio, Vorkurs Deutsch, Fachkraftquote, Partizipationsmöglichkeiten, Kinderkonferenz, Mindestbuchungszeit, Projektarbeit (in `build.py`, `GLOSSAR`).
- [x] 10 Durchwahl finden (Kontakt): Gruppe oder Bereich tippen („Spatz“, „Krippe“, „Hort“) → passende Nummer; unbekannt → Feld schüttelt kurz.
- [x] 12 Licht nach Tageszeit im Startbereich (morgens warm links, mittags oben, abends kühl rechts).
- [x] 14 Rundgang als Geschichte (Vollbild, 5 s pro Bild, Halten pausiert, Tippen links/rechts, Esc/Zurück schließt).

**Gemerkt für später**
- [ ] 8 Bereichs-Finder (Alter des Kindes → passender Bereich).
- [ ] 13 Checkliste „Was braucht mein Kind?“ (abhakbar, bleibt gespeichert) – braucht die echte Liste vom Hort.

**Nicht gewünscht:** 6 Fotostreifen, 11 Gruppenkarten zum Umdrehen.

## Ideenkatalog 3 (15.11.2026)
Katalog: `entwurf/ideen/ideen-3.html` (private Vorschau: https://claude.ai/artifact/JpzTSnT8bN3T4MZeEu5NSt), Bildschirmfotos: `entwurf/ideen3/`

1 Weg durch den Tag · 2 Haus, in dem Fenster aufleuchten · 3 Jahreszeiten im Kopfbereich · 4 Anfahrt mit gezeichnetem Weg · 5 „Was zieht mein Kind heute an?“ · 6 Fotos nach Bereich filtern · 7 Platzanfrage in drei Schritten · 8 Downloads mit Vorschau · 9 Kleine Feier bei Erfolg · 10 Geöffnet-Anzeige in der Leiste · 11 Termin teilen · 12 Wimpel-Vorhang beim Seitenwechsel · 13 Link-Vorschau · 14 Aushang mit QR-Code · 15 Monatskalender mit Schließtagen · 16 Buchungszeit-Rechner · 17 Fotos mit Entdecker-Punkten · 18 Elternstimmen · 19 Handgezeichnete Markierungen · 20 Als App auf den Startbildschirm · 21 AG-Wochenplan im Hort · 22 Gruß am Seitenende · 23 Eingewöhnung Schritt für Schritt · 24 Team-Vorstellung · 25 Pinnwand mit Kinderbildern · 26 Wachsende Pflanze als Lesefortschritt · 27 Fragen-Helfer · 28 Bereiche im Vergleich · 29 Knopf mit Rückmeldung · 30 Eil-Hinweis für das Team · 31 Ferienprogramm des Hortes · 32 Bild in Ebenen · 33 Fotostapel zum Durchwischen · 34 Formular-Lotse · 35 Countdown zum Schulstart · 36 Kontakt-Knopf, der sich auffächert · 37 Wortwolke · 38 Bringzeit-Uhr · 39 Elternbrief-Archiv mit Suche · 40 Gleitender Fokus-Rahmen · 41 Vorher-Nachher-Regler · 42 Jahreskreis der Feste · 43 Suchspiel für Kinder · 44 Tastenkürzel-Hilfe · 45 Ein Jahr in Bildzeichen · 46 Bildkarten-Tagesplan · 47 Wimpel-Ladeanzeige · 48 Spürbare Rückmeldung · 49 Kindermund · 50 Spendenbarometer · 51 Wandernde Wimpel-Tapete · 52 Neu seit Ihrem letzten Besuch · 53 Zufallsfoto · 54 Kalender-Abo-Assistent · 55 Termine als Liste oder Kalender · 56 So wächst ein Kind bei uns · 57 Maskottchen Pip · 58 Freundliche Fehlerseite · 59 Kurze Elternumfrage · 60 Fotos mit Tiefe beim Scrollen · 61 Wochenrückblick · 62 Reaktionen auf Neuigkeiten

Auswahl: direkt im Katalog (Ja / Merken / Nein + Anmerkung je Idee), gespeichert in der Datenbank des Artefakts, Sammlung `auswahl`.

## Ideenkatalog 3 – Entscheidung (15.11.2026, Auswahl direkt im Katalog)
Auswahl gespeichert im Katalog (Datenbank `auswahl`): 23× Ja, 20× Merken, 15× Nein, 4 offen (32, 33, 41, 42).

**Eingebaut (Ja)**
- [x] 1 Weg durch den Tag – Tagesablauf-Linie zeichnet sich beim Scrollen, Stationen leuchten auf (alle drei Bereiche).
- [x] 3 Jahreszeiten im Auftakt – ein paar Blüten/Lichtpunkte/Blätter/Flocken je nach Monat, höchstens 18, nach 8 s vorbei.
- [x] 6 Fotos nach Bereich filtern – neuer Abschnitt „Einblicke“ auf der Startseite (je 4 Fotos pro Bereich, Bildansicht zeigt nur die gefilterten).
- [x] 8 Downloads mit Vorschau – echte Vorschaubilder der ersten PDF-Seite (automatisch erzeugt), Seitenzahl und Größe automatisch, „neu“ 30 Tage lang (`NEU_SEIT` in build.py).
- [x] 9 Kleine Feier – Konfetti beim Merken eines Termins.
- [x] 10 Geöffnet-Anzeige in der Leiste – Punkt (grün/rosé/grau) mit Text, Tipp zeigt Zeiten aller Bereiche; am Handy als Abzeichen am Logo.
- [x] 11 Termin teilen – Teilen-Knopf an jedem Termin (Handy: Teilen-Menü, Computer: Link kopieren).
- [x] 15 + 55 Termine als Liste oder Kalender – Monatskalender mit Terminen und Schließtagen, Wahl wird gemerkt.
- [x] 19 Handgezeichnete Markierungen – Kringel um „Qualität“ (Startseite), Unterstreichung „kennen“.
- [x] 20 Als App aufs Handy – Web-App-Manifest, App-Symbole, Link im Fuß mit Anleitung (Android: direkte Installation).
- [x] 27 Fragen-Helfer – Kontakt → „Fragen Sie einfach“, Antworten aus allen häufigen Fragen der drei Bereiche.
- [x] 29 Knopf mit Rückmeldung – Downloads/Kalenderdateien zeigen kurz einen grünen Haken.
- [x] 34 Formular-Lotse – Downloads → „Was möchten Sie tun?“.
- [x] 37 Wortwolke – Startseite, Abschnitt „Mehr als Betreuung“.
- [x] 39 Elternbrief-Archiv – Aktuelles, Briefe aus `daten/elternbriefe.csv`, Suche ab 2 Briefen.
- [x] 40 Gleitender Fokus-Rahmen – für Tastatur-Nutzer auf allen Seiten.
- [x] 47 Wimpel-Ladeanzeige – bei langsamem Seitenwechsel (ab 1 s).
- [x] 54 Kalender-Abo – Downloads → „Kalender abonnieren“ (webcal-Links, Anleitung je Gerät). Funktioniert erst, wenn die Seite unter kinderhort-grombuehl.de läuft.
- [x] 58 Freundliche Fehlerseite – `404.html`, in `.htaccess` eingetragen.
- [x] 60 Fotos mit Tiefe – große Kopfbilder und Teaser bewegen sich beim Scrollen leicht.

**Vorbereitet, wartet auf Inhalte**
- [ ] 18 Elternstimmen – erscheint automatisch, sobald `daten/elternstimmen.csv` echte Zitate enthält (nur mit Einverständnis, ohne Namen).

**Nicht umgesetzt (braucht einen Server)**
- [ ] 62 Reaktionen auf Neuigkeiten – gemeinsame Zähler für alle Besucher brauchen einen kleinen Dienst auf dem Server; außerdem gibt es noch keine Neuigkeiten-Beiträge.

**Merken:** 4, 5, 7, 13, 14, 16, 17, 21, 23, 24, 25, 31, 36, 38, 48, 49, 50, 51, 61
**Nein:** 2, 12, 22, 26, 28, 30, 35, 43, 44, 45, 46, 52, 53, 56, 57, 59

## Ideenkatalog 3 – Nachtrag 63–75 (15.11.2026)
63 Farbschimmer je Bereich · 64 Texte vorlesen lassen · 65 Mitlaufende Abschnittstitel · 66 „Jetzt gut erreichbar?“ · 67 Wimpel-Trenner · 68 „Zuletzt angesehen“ in der Suche · 69 Zwischen den Bereichen wischen · 70 Gelesen-Häkchen im Inhaltsverzeichnis · 71 Kontakt aufs Handy speichern · 72 Begrüßung nach Tageszeit · 73 „Morgen geschlossen“-Hinweis · 74 Notfallkarte fürs Portemonnaie · 75 Tipp-Welle in der Handy-Leiste

Entscheidung offen (Auswahl direkt im Katalog).

## E-Mail beim Umzug (Wunsch)
Geplant: info@, krippe@, kindergarten@kinderhort-grombuehl.de über das Webhosting-Paket (Hort über info@). Noch nicht in die Seite eingebaut – erst wenn die Postfächer stehen.

## Nachtrag 63–75 – Entscheidung (15.11.2026)
**Eingebaut:** 65 Mitlaufende Abschnittstitel (nur Abschnitte länger als 1,6 Bildschirme), 68 „Zuletzt angesehen“ in der Suche (nur im eigenen Browser), 71 Kontakt aufs Handy speichern (`downloads/kinderhort-grombuehl.vcf`, automatisch aus den Durchwahlen erzeugt).
**Merken:** 63, 64, 66, 67, 69, 70, 72, 73, 74 · **Nein:** 75

**Menü (Wunsch):** Beim geöffneten Menü auf Handy/Tablet verschwindet die Leiste mit dem Namen, es bleibt nur das Kreuz zum Schließen.

## Ideenkatalog 3 – Nachtrag 76–88 (15.11.2026)
76 Ferienplan mit Ampel · 77 Anrufen mit Gruppenauswahl · 78 Bildunterschriften gleiten hoch · 79 Doppeltipp-Zoom · 80 Wimpel weichen der Maus aus · 81 „Das Wichtigste in Kürze“ · 82 Ferienplan als Jahresposter · 83 Fotos legen sich wie Abzüge hin · 84 Foto-Collage neigt sich mit · 85 Route mit der Karten-App · 86 „Wie geht’s weiter?“ · 87 Abreißkalender · 88 Geöffnet-Punkt im Browser-Tab

Entscheidung offen (Auswahl direkt im Katalog).

## Nachtrag 76–88 – Entscheidung (15.11.2026)
**Eingebaut:** 76 Ferienplan mit Ampel (vergangen blass, aktuell rosé, nächste grün mit „in N Tagen“), 78 Bildunterschriften im Rundgang gleiten hoch (nur mit Maus), 79 Doppeltipp-/Doppelklick-Zoom in der Bildansicht, 80 Wimpel im Fuß weichen der Maus aus, 81 „Das Wichtigste in Kürze“ oben auf den drei Bereichsseiten (mit Symbolen statt Emojis), 82 Jahresposter drucken (Knopf beim Ferienplan, ein A4-Blatt), 84 Foto-Collage im Startbereich neigt sich mit der Maus (Android: beim Neigen), 85 „Route planen“ auf der Kontaktseite (iPhone: Apple Karten, sonst Google Maps; Datenschutztext angepasst).
**Merken:** 88 · **Nein:** 77, 83, 86, 87

**Entfernt (Wunsch):** Abschnitt „Einblicke in die 3 Bereiche“ auf der Startseite – war doppelt zum Rundgang.

## Ideenkatalog 3 – Nachtrag 89–100 (15.11.2026)
89 Weg zur Anmeldung · 90 Besichtigung mit Wunschzeiten · 91 Fragen nach Themen filtern · 92 Bereichskarten heben sich räumlich · 93 Schließtage als Balken · 94 Einzelne Schließzeit in den Kalender · 95 „Wann darf mein Kind wieder kommen?“ (Texte nur Beispiel – müsste der Hort festlegen) · 96 Familien-Ansicht für mehrere Kinder · 97 Hinweis ohne Internet · 98 Kurznachricht an die Gruppe · 99 Begriffe von A bis Z · 100 Seite per QR-Code zeigen

Entscheidung offen (Auswahl direkt im Katalog).

## Ideenkatalog 3 – Nachtrag 101–112 (15.11.2026)
101 Sanfte Welle zum Fußbereich · 102 Gruppensymbole, die lebendig werden · 103 Seiten merken · 104 Elternbeirat vorstellen (Namen Platzhalter) · 105 Verspielte Link-Unterstreichung · 106 Leitsatz schreibt sich · 107 Schwung unter dem Gruß · 108 „Einfach erklärt“ · 109 Bilder im Bereichsmenü wechseln · 110 Fotos in weichen Formen · 111 Bereich als Infoblatt drucken · 112 Telefonnummer am Computer (QR zum Anrufen)

Entscheidung offen (Auswahl direkt im Katalog).

## Übergänge-Katalog (15.11.2026)
Seite: `entwurf/ideen/uebergaenge.html` (private Vorschau: https://claude.ai/artifact/MwFfsnHZkLRnpvEW46xg52), Auswahl in der Datenbank-Sammlung `uebergaenge`.
Seitenwechsel: 1 Überblenden · 2 Seitlich gleiten · 3 Kreis aus dem Klickpunkt · 4 Aufsteigen aus der Unschärfe · 5 Hineinzoomen · 6 Rosé Vorhang · 7 Karte legt sich darüber · 8 Inhalte nacheinander · 9 Überschrift wandert mit · 10 Welle · 11 Mosaik
Abschnitte: 12 Abschnitte stapeln sich · 13 Schräge Kanten · 14 Bild öffnet sich wie ein Fenster · 15 Inhalte steigen auf (schon eingebaut)
Elemente: 16 Reiter mit mitgleitendem Inhalt · 17 Fenster wächst aus dem Knopf (schon eingebaut) · 18 Fragen klappen weich auf (schon eingebaut) · 19 Bilderwechsel mit Kamerafahrt

Entscheidung offen.

## Feinschliff nach „unslop“ (15.11.2026)
Bestandsaufnahme mit dem Plugin-Leitfaden „unslop“ (Polier-Modus, Farben/Schrift/Aufbau bleiben). Umgesetzt:
- Gruppensymbole: Emojis durch Liniensymbole ersetzt (Sonne, Stern, Bär, Biene, Spatz)
- Etiketten in normaler Schreibweise statt GROSSBUCHSTABEN mit Sperrung (10 Stellen)
- Schriftstärken 700/800 auf 600, Hierarchie über Größe
- „Schön, dass Sie da sind“ ohne Ausrufezeichen (Leitsatz und Briefanrede bleiben)
- Rundungen abgestuft: Knöpfe 12 px, Etiketten 8 px, Umschalter 12/8 px, kleine Marken 6 px
- 165 Abstände ins 4-Pixel-Raster
- Kopfleiste: Name am Computer zweizeilig, damit der Geöffnet-Punkt ihn nicht überdeckt
Bewusst behalten (vom Hort gewählt): Wortwolke, Jahreszeiten, Tiefe beim Scrollen, Collage-Neigung, Tageslicht, Licht unter der Maus, Magnet-Knöpfe, Konfetti, pulsierender Geöffnet-Punkt.
Vergleichsbilder: `entwurf/unslop/`

## Übergänge – Nachtrag 20–35 (15.11.2026)
Seitenwechsel: 20 Jalousie · 21 Seite blättert um · 22 Schräg wischen · 23 Seite öffnet sich wie eine Tür · 24 Weicher Schwenk
Abschnitte: 25 Text steigt Zeile für Zeile auf · 26 Fotoreihe rollt beim Scrollen · 27 Abschnitt schiebt sich heran · 28 Bild bleibt, Text wandert
Kleine Animationen: 29 Lichtkante über den Knopf · 30 Pfeil fliegt durch · 31 Karten heben sich an · 32 Häkchen zeichnet sich · 33 Fotos wischen herein · 34 Wimpel schwingen zur Begrüßung · 35 Strich wandert im Menü mit

Entscheidung offen.

## Übergänge – Nachtrag 36–46 (15.11.2026, nach dem Leitfaden „unslop“)
Verbesserung für alle Übergänge: eine Bewegungskurve `cubic-bezier(.22,1,.36,1)`, Menü-Strich (35) animiert nicht mehr die Breite.
36 Ruhig nach Lehrbuch (Empfehlung) · 37 Rasterpunkte · 38 Zweifarbig überblenden · 39 Wimpel als Ladeanzeige · 40 Foto baut sich aus Buchstaben auf · 41 Fotos laden als Rasterbild · 42 Menü klappt aus dem Knopf (Empfehlung) · 43 Knöpfe nach Lehrbuch (Empfehlung) · 44 Kopfleiste wird beim Scrollen fester · 45 Wörter rollen um · 46 Kringel um den aktiven Menüpunkt

Entscheidung offen.

## Übergänge – Nachtrag 47–59 (15.11.2026)
47 Foto wird zur Seite (schon eingebaut, Empfehlung) · 48 Nach oben schieben · 49 Wimpel öffnet die Seite · 50 Weicher Fokuswechsel · 51 Trennlinie zeichnet sich (Empfehlung) · 52 Fotos erscheinen als Welle (Empfehlung) · 53 Großer Titel wird zur Leiste · 54 Fotoreihe mit Vorschau · 55 Telefon klingelt kurz · 56 Link füllt sich mit Farbe · 57 Kalenderblatt blättert · 58 Platzhalter beim Laden · 59 Wimpel im Logo wehen

Entscheidung offen.
