# Offene Punkte & Ideen – Webseite Kinderhort Grombühl

Stand: 13.11.2026

## Design-Stand
- Webseite nutzt **Entwurf 9** (Salbeitürkis, Grau-Rosé, dunkles Türkis) – fest eingebaut.
- Varianten (CSS in `entwurf/designs/`, Screenshots in `entwurf/`):
  1 Salbei & Pfirsich · 2 Vanille & Rosé · 3 Himmel & Sonne · 4 Lavendel & Minze · 5 Sand & Terrakotta ·
  6 Lavendelgrau & Honig · 7 Salbeitürkis & Zitrone · 8 Salbeitürkis & Grau-Rosé ·
  **9 Salbeitürkis, Grau-Rosé & dunkles Türkis** (Karten #2D6A6A, Hintergrund #A8C5C0, Schrift #1E3B44, Akzent #D4B5B0)


## 1. Vor dem Livegang (Pflicht)
- [ ] **Impressum vom Träger bestätigen lassen:** (1) Vertretung des Vereins – steht nur Helmut Burmester im Vereinsregister, oder vertreten mehrere Vorstandsmitglieder gemeinsam? Dann alle nennen. (2) Aufsichtsbehörde eingetragen: Stadt Würzburg, Fachbereich Jugend und Familie, Karmelitenstraße 43, 97070 Würzburg (Anschrift aus einem städtischen Formular – beim Livegang kurz gegenprüfen).
- [ ] **Nur das Upload-Paket hochladen** (`kinderhort-webseite.zip`, entsteht bei `python3 build.py`), nicht den ganzen Projektordner.
- [ ] **Sicherheit beim Umzug (.htaccess):** HTTPS-Weiterleitung und Strict-Transport-Security einschalten, sobald das SSL-Zertifikat läuft (Zeilen sind vorbereitet, nur # entfernen). Falls der Hoster „Options -Indexes“ nicht erlaubt (Fehler 500), diese Zeile auskommentieren. Nach dem Umzug einmal prüfen: https://securityheaders.com
- [ ] PDFs vor dem Hochladen: Autor-Feld in den Dateieigenschaften prüfen (Medikamentenvereinbarung enthält einen Personennamen).
- [x] Datenschutzerklärung anlegen – Vorlage steht; **offen: Hoster und Datum ergänzen, Speicherdauer der Server-Protokolle beim Hoster auf 7 Tage stellen, prüfen lassen**
- [x] Impressum: TMG-Verweise auf DDG (Digitale-Dienste-Gesetz, seit Mai 2024) umstellen
- [x] Weiterleitungen alter URLs (`/kinderkrippe/`, `/kindergarten/`, `/kinderhort/`, `/aktuelles/`, `/downloads/`, `/kontakt/`, `/impressum/`, `?page_id=…`) auf die neuen Seiten

## To-do (Wünsche, noch offen)
- [x] **Untere Handy-Leiste entfernen** (erledigt 15.11.: Lupe sitzt oben neben dem Menü-Knopf, der Name steht zweizeilig, der Zähler gemerkter Termine sitzt als Abzeichen am Menü-Knopf und das Datum fliegt dorthin; Kurzmeldungen und „Nach oben“ wieder unten am Rand) (Anrufen · Krankmelden · Termine · Suche, im Screenshot vom 15.11. markiert). Dabei mitdenken: Die Suche ist am Handy bisher nur unten erreichbar → Lupe wieder oben in die Kopfleiste; der Zähler für gemerkte Termine braucht ein neues Ziel (Menüpunkt „Aktuelles“); die Abstände unten (Kurzmeldungen, „Nach oben“-Knopf) wieder anpassen.

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

## Durchwahl finden und „Fragen Sie einfach“ (16.11.2026)
- **Durchwahl finden:** Beim Tippen bleiben nur die passenden Einträge in ihrem türkisen Kasten stehen, die anderen Gruppen und Bereiche verschwinden; Feld leeren zeigt wieder alle. Versteht Tippfehler (Spazen, Sonnengrupe), Kurzformen (Kiga, Krippe, Hort, Büro/Zentrale/Leitung) und Endungen („15“). Esc leert das Feld.
- **Fragen Sie einfach:** keine dicke Markierung mehr um das Feld beim Tippen (nur der Rand wird etwas dunkler; der gleitende Fokusrahmen lässt Eingabefelder generell aus).
- **Schlauer:** beantwortet zuerst aus den Daten der Seite – Öffnungszeiten (heute/morgen), Schließtage und Ferien (auch nach Namen, z. B. Weihnachten), Durchwahl einer Gruppe, Krankmelden, Platz/Anmeldung (je Bereich), nächste Termine, Adresse. Sonst aus den häufigen Fragen, jetzt mit Tippfehler-Toleranz, Vorschlägen schon beim Tippen und „Auch passend“.

## Ja-Ideen Katalog 4, zweite Runde (16.11.2026)
- **46 Feiertage im Monatskalender:** Feiertage haben einen eigenen Rahmen, stehen in der Legende und mit Namen unter dem Kalender.
- **47 Elternbrief teilen und drucken:** Jeder Brief hat „Teilen“ (Handy-Teilen oder Link kopieren, Link öffnet den Brief) und „Drucken“ (nur der Brief, mit Kopfzeile).
- **54 „Meinten Sie …?“ in der Suche:** bei Tippfehlern ein Vorschlag (z. B. Feinplan → Ferienplan); Tipp oder Enter übernimmt ihn.
- **63 Wimpelkette im Jahreslauf:** Die Wimpel im Fußbereich wechseln die Farben mit der Jahreszeit, nur Farbtöne aus der Familie.
- **65 Fehlt ein Foto:** Statt eines kaputten Bildes erscheint ein ruhiges Salbei-Muster mit der Bildbeschreibung.
- **73 Weg zu uns:** „Route öffnen“ jetzt auch im Fußbereich jeder Seite (Apple Karten auf Apple-Geräten, sonst Google Maps). Offen: nächste Haltestelle und Parken – Angaben vom Hort.
- **75 Tag der offenen Tür:** Band auf der Startseite sechs Wochen vor einem passenden Termin (siehe daten/LIESMICH.txt).
- **82 Kaputte Links finden:** Link-Prüfung beim Bauen (Dateien und Sprungziele).
- **95 Nummer kopieren am Computer:** Am Computer kopiert ein Klick auf eine Telefonnummer die Nummer; am Handy wird wie gewohnt angerufen.
- **96 Monatskalender zum Wischen:** Das Monatsraster folgt jetzt dem Finger und federt zurück, wenn man nicht weit genug wischt.
- **79 Kinderzeichnungen:** erst als Entwurf (`entwurf/zeichnungen/kinderzeichnungen.html`, private Vorschau https://claude.ai/artifact/XTvjDPfxfeqSaNMbVq6HE6) – Einbau nach Rückmeldung.

## Handy-Menü, Datenschutz, Merken-Ideen (16.11.2026)
- **Handy-Menü:** „Kind krankmelden“ im Kasten „Wir sind für Sie da“ entfernt; Telefon und E-Mail sehen jetzt aus wie die Krankmelde-Karte (heller Kasten, rosé Symbolkachel).
- **Fotos:** geprüft – alle JPG sind schon höchstens 1600 px groß und optimiert; Browser laden ohnehin die kleineren WebP-Fassungen. Nichts zu tun.
- **Datenschutz:** ergänzt um Rechtsgrundlagen (KDG), Abschnitt „Was die Seite in Ihrem Browser speichert“ und die Aufsicht (Katholisches Datenschutzzentrum Bayern, Nürnberg). Datenschutzbeauftragte: Katrin Hofmann; Server-Protokolle: 7 Tage (beim Hoster so einstellen). Offen: Hoster, Datum; ggf. eigene E-Mail-Adresse für Frau Hofmann.
- **Termine nach Bereich (44):** neue Spalte „Bereich“ in termine.csv; Knöpfe Alle · Krippe · Kindergarten · Hort auf „Aktuelles“ (Liste und Kalender); Termine fürs ganze Haus bleiben immer sichtbar.
- **Abholvollmacht (48) und Abwesenheit (86):** E-Mail-Vorlagen auf „Kontakt“ und im Formular-Lotsen bei „Downloads“.
- **Krankmelden mit einem Tipp (2):** Die zuletzt angerufene Gruppe steht beim nächsten Mal als großer Knopf oben (nur im eigenen Browser gespeichert).
- **Sprungleiste (Überblick … Schließtage):** Der Punkt wechselt erst, wenn die Überschrift des Abschnitts oben unter der Leiste angekommen ist (vorher zu früh). Gilt für alle Seiten mit dieser Leiste.

## Prüfung „7 UI-Fehler“ (17.11.2026)
- Gemessen auf allen Seiten am Handy: keine dünne Schrift (alles mindestens 400), keine vagen Knopftexte („Ja/Nein/OK“), Auswahl immer deutlich (dunkler oder rosé Hintergrund).
- Tippflächen auf mindestens 44 × 44 px gebracht: Umschalter Liste/Kalender, Bereichs-Filter, Abo-Reiter, Fragen-Themen, Vorschläge im Fragen-Helfer, Logo, „Alle Termine“-Link im Hinweis, „Route öffnen“, „Als App“, „Bewegung aus“. Fließtext-Links und Begriffs-Erklärungen im Text sind (wie in den Richtlinien) ausgenommen.
- Verschachtelte Rundungen: Symbolkacheln innen kleiner gerundet als ihre Karte (Krankmelden 8 px, Gruppenzeichen 4 px, PDF-Kachel 6 px, Kontakt-Kacheln 12 px).
- Symbol-Knöpfe ohne Text zeigen ihre Beschriftung jetzt auch als Hinweis beim Darüberfahren.

## Korrektur gelesen (16.11.2026)
- Rechtschreibung/Grammatik: „Herzlich willkommen“, „Platz im Kindergarten/Kinderhort“, Kommas (Schlafraum, Wickelraum), Dativ (Außenbereich Krippe), „Meistgestellte Fragen“, „Inhouse-Schulungen“, „freinehmen“.
- Sprache geglättet: Bobbycars/kleine Räder, „kleines Bällebad“, „etwa vier Wochen“ (einheitlich), „Puppen- und Rollenspielecke“, „Lange Öffnungszeiten“, Hausaufgaben-Satz, „Erzieherinnen und Erziehern“, „Webseite“ statt „Homepage“.
- Vom Hort bestätigt: Kindergarten „Spielbereich im Flur“ (nicht Außenspielbereich), Krippen-Tagesablauf „9:00 Uhr Freispiel“.

## Schneller laden (16.11.2026)
- Server komprimiert jetzt (Brotli/Gzip in .htaccess). CSS/JS tragen eine Versionsnummer (?v=…) und dürfen deshalb ein Jahr im Browser bleiben – nach jeder Änderung lädt der Browser trotzdem sofort die neue Fassung (vorher bis zu eine Woche alt möglich). HTML wird nie zwischengespeichert.
- Upload-Paket enthält verkleinerte CSS/JS (−94 KB), wenn esbuild vorhanden ist (optional; ohne esbuild einfach unverkleinert).
- Dabei gefunden und behoben: Das neue Menü-Hereinschieben machte die Seite am Handy nach dem ersten Antippen doppelt so breit. Jetzt wird die Fläche freigelegt statt verschoben – gleiches Aussehen, keine Verbreiterung.

## Handy-Menü (16.11.2026)
- Fehler behoben: Das Menü spannte sich nur innerhalb der Leiste auf (Ursache: will-change an der Leiste).
- Öffnen/Schließen jetzt Variante B: schiebt sich von rechts herein (0,42 s), Seite dahinter wird leicht abgedunkelt, Schließen schneller (0,28 s). Verworfene Varianten: entwurf/leiste/menu-live.html.

## Feinschliff Bewegung (16.11.2026)
- Krankmelden, Formular-Lotse, Elternbriefe und häufige Fragen klappen weich auf und zu – per Skript, damit es auch in Safari/iPhone läuft (vorher nur Chrome). Lotse besonders ruhig (0,48 s, Inhalt geht zuerst, kommt zuletzt; immer nur ein Punkt offen).
- Termine nach Bereich: gehende Termine blenden aus, die übrigen gleiten an ihren Platz.
- „… anrufen“-Knopf blendet weich ein; Bereichs-Knöpfe geben beim Drücken nach.
- Mit „Bewegung reduzieren“ klappt alles sofort. Live-Vergleich: entwurf/animationen/.
- Runde 2: Handy-Menü „Bereiche“ gleitet auf (Einträge nacheinander); Hinweis wegklicken/Rückgängig zieht sich weich zusammen/auf; Kalender-Abo-Reiter gleicht die Höhe an; Merkliste-Zeile zieht sich beim Entfernen zusammen; „Alle … Termine anzeigen“ blendet nacheinander ein; „Gemerkte Termine“-Zeile schiebt den Inhalt weich nach unten, Knöpfe nacheinander, Zahl springt kurz auf, klappt beim letzten Entfernen weich zu.
- Runde 3: Antworten unter „Jetzt geöffnet“ blenden ein (Karte wächst mit); Kalender-Notiz blendet über; Hinweis beim Bereichs-Filter blendet ein. Damit ist die Bewegung fertig – weitere Animationen würden eher unruhig machen.

## Obere Leiste (16.11.2026)
- Verhalten wie bisher (verschwindet beim Herunterscrollen ganz, kommt beim Hochscrollen zurück), aber weicher: sanftere Kurve, 0,5 s statt 0,2 s, blendet am Ende leise aus; die Sprungleiste rückt im selben Takt nach. Reagiert etwas gelassener (erst nach 32 px nach unten, 16 px nach oben). Verworfene Varianten: entwurf/leiste/.

## Sicherheits-Check nach der 20-Punkte-Liste (16.11.2026)
- Geprüft: keine Schlüssel/Passwörter in der ganzen Git-Geschichte, keine .env-Dateien, keine fremden Pakete oder Skripte, keine Cookies, kein Debug-Code, keine Formulare, die etwas senden; XSS-Schutz, Sicherheits-Header und gesperrte interne Dateien sind da.
- Nicht zutreffend (statische Seite): Anmeldung, Benutzerrechte, Admin-Bereich, Datenbank/SQL, Rate-Limit, Kostenbremse, Datei-Uploads, CSRF, CORS.
- Neu: **Upload-Paket** `kinderhort-webseite.zip` (neben dem Ordner) wird bei jedem `python3 build.py` neu erzeugt und enthält nur öffentliche Dateien – genau diesen Inhalt auf den Webspace laden. Das alte Paket enthielt noch Notizen und eine ungeschützte .htaccess.
- HTTPS-Weiterleitung in .htaccess vorbereitet (mit Schutz gegen Endlosschleife), nach dem Umzug einschalten.

## Sicherheit (16.11.2026)
- **Erste Runde:** interne Dateien (Notizen, Pläne, Vorschau, Hilfsprogramme) per .htaccess gesperrt; Sicherheits-Header; Tabellentexte überall maskiert; gespeicherte Gruppe wird geprüft.
- **Zweite Runde („noch sicherer“):** Die Schutzregel (CSP) erlaubt jetzt auch keine eingebettete Gestaltung mehr (`style-src 'self'` ohne `'unsafe-inline'`); Vorschaubilder, Wortwolke und Reihenfolgen stehen in `css/erzeugt.css` (wird von build.py erzeugt). Zusätzliche Header: Cross-Origin-Resource-Policy, X-Permitted-Cross-Domain-Policies, upgrade-insecure-requests, form-action. Externe Links mit `noopener noreferrer`. Der Offline-Speicher nimmt nur eigene, unveränderte Antworten auf. `/.well-known/security.txt` mit Kontakt für Sicherheitshinweise (läuft 16.11.2027 ab – dann Datum erneuern).
- **Automatische Prüfung beim Bauen:** meldet unter „Daten-Prüfung“, wenn jemand eingebettete Gestaltung, eingebettete Skripte ohne Freigabe, `on…=`-Code oder unsichere neue Tabs einbaut.

## Wünsche aus Screenshots (16.11.2026)
- Kopfleiste: „Geöffnet“-Anzeige und „Strg K“ entfernt (Öffnungsstatus bleibt im Auftakt der Startseite).
- Kein Lichtstreifen mehr über Knöpfen; kein Konfetti beim Merken.
- Fotos im Auftakt bewegen sich beim Überfahren nicht mehr.
- Licht, das der Maus auf dunklen Karten folgt, viel schwächer (Deckkraft 3,5 % statt 9 %).
- Bereichsmenü wieder so breit wie die Kopfleiste (war seit dem Menü-Strich auf 571 px geschrumpft) und deckender.

## Ideenkatalog 4 (16.11.2026)
Seite: `entwurf/ideen/ideen-4.html` (gebaut mit `entwurf/ideen/mk_ideen4.py`, private Vorschau: https://claude.ai/artifact/S14G9MoJv8azSS2Sifxeoq), Auswahl in der Sammlung `ideen4` (ids `i4-01` … `i4-99`). 99 Ideen; Knopf „Zu den neuen Ideen“ und Filter „Neu dazu“ zeigen immer die jüngste Runde (zuletzt 86–99) (41–56 in einer dritten Runde: Suche mit Antworten, „Jetzt gerade“ im Tagesablauf, Termine nach Bereich, Feiertage im Kalender, Abholvollmacht, wichtiger Hinweis, Team, Eingang finden u. a.), jede mit dem Skill, aus dem sie stammt (ui-ux-pro-max, impeccable, mobile-native, gestures, dataviz, remove-animations, web-design-guidelines, choreograph, explainer, landing-page-design, humanizer, figma-designer, break-ui, nothing-design, apple-design). Nicht genutzt, weil für diese Seite unpassend: pinme (fremdes Hosting), write-swift/animate-expo (native Apps), sound-effects/motion-broll/object-separation (Video/Freistellen am eigenen Rechner), caveman.

Eingebaut (Ja): 3, 4, 5, 6, 9, 11, 19, 21, 22, 23, 24, 33, 37.
- **3 Kurzbefehle am App-Symbol:** Kind krankmelden (öffnet den Abschnitt auf der Startseite, `#krankmelden`), Termine, Durchwahlen.
- **4 Neu seit dem letzten Besuch:** grünes „neu“ an Terminen und Elternbriefen. Wann ein Eintrag zuerst auftauchte, merkt sich `daten/erstmals.json` (wird beim Bauen gepflegt – bitte mit hochladen); der letzte Besuch steht nur im Browser der Eltern.
- **5 Hinweise mit Datum:** neue Tabelle `daten/hinweise.csv` (Datum; Titel; Text). Es steht nur das Datum dabei, am Tag danach verschwindet der Hinweis. „Sankt Martin“ (11.11.) ist deshalb schon weg.
- **6 Termin nach rechts wischen = merken** (nur am Handy), **37** kurzes Vibrieren beim Merken (Android).
- **9 „Bewegung aus“** im Fußbereich, gilt für alle Seiten und wird gemerkt.
- **11 Auftakt:** beim ersten Besuch erst der Name, dann fallen die Fotos, zuletzt „Jetzt geöffnet“ und Krankmelden; bei späteren Besuchen sofort.
- **19 Daten-Wächter:** `python3 build.py` meldet am Ende Fehler in den Tabellen in Klartext (Datum unlesbar, Ende vor Anfang, doppelt, mehr als 30 Schließtage, fehlende Felder) und überspringt kaputte Zeilen statt abzubrechen.
- **21 Gruppen-Symbole** an Terminen (wenn eine Gruppe genannt ist), Durchwahlen und Krankmelden.
- **22 „Gemerkte ansehen“:** Blatt von unten mit allen gemerkten Terminen, einzeln entfernbar, nach unten ziehen schließt.
- **23 „So geht es weiter“** erscheint nach Platz anfragen / Kennenlernen.
- **24 Kurz gefragt** unter „Jetzt geöffnet“: Morgen offen? Nächste Woche? Nächste Ferien?
- **33 Erinnerung am Vorabend (18 Uhr)** in allen Kalenderdateien (Termine, Schließtage, gemerkte Termine).

## Stresstest, Critique, Handy (16.11.2026)
**break-ui** (Grenzfall-Daten in Kopien der Seite: Worst Case, leer, eins, viele) – behoben:
- Gruß im Elternbrief: **fett** mit `**…**` (alte `<strong>`-Schreibweise wird weiter verstanden). War seit der Sicherheitskorrektur als Text sichtbar.
- Leere `schliesstage.csv` bricht den Bau nicht mehr ab („Der Ferienplan für das nächste Kita-Jahr folgt in Kürze.“); Zeilen werden nach Datum sortiert, das Kita-Jahr läuft September–August.
- Keine Elternbriefe → Abschnitt und Sprungmarke entfallen; keine kommenden Termine → kein „Alle in den Kalender“.
- Internet- und E-Mail-Adressen in Terminen und Elternbriefen sind anklickbar; ab 12 Terminen „Alle N Termine anzeigen“.
- Datum steht oben neben langen Terminen; Anführungszeichen der Elternstimmen über dem Text.
- Ferienplan: zweites „Pfingsten“ (28.05.2027) heißt jetzt „Brückentag nach Fronleichnam“.
- Fokusrahmen umrandet bei Suchfeldern das sichtbare Feld.

**impeccable critique** (27/40) – umgesetzt nach Wahl:
- **Kind krankmelden** auf der Startseite (unter „Jetzt geöffnet“) und im Handy-Menü: aufklappbar, jede Gruppe direkt anrufen oder E-Mail mit Vorlage. Hinweis „Bitte geben Sie möglichst früh am Morgen Bescheid.“ – **vom Hort prüfen lassen, ob es eine feste Uhrzeit gibt.**
- **Anmeldung** auf jeder Bereichsseite („So bekommen Sie einen Platz“): Platz anfragen (Vorlage mit Bereich) und Kennenlernen vereinbaren, eigene Sprungmarke. Warteliste/Fristen/Kosten kommen dazu, sobald der Hort sie nennt.
- **Kürzer:** Startseite und Bereichsseiten zeigen nur noch den Zeitstrahl mit nächster Schließzeit + „Ganzen Ferienplan ansehen“; der volle Plan steht auf „Aktuelles“ und ist am Handy als Karten statt breiter Tabelle. Wortwolke entfernt, drei statt vier Kennzahlen. „Das zeichnet uns aus“: zwei Punkte je Gruppe, Rest über „Alle N Punkte anzeigen“.
- Aktiver Punkt im Handy-Menü: Fläche statt rosé Streifen.
- Noch offen aus der Critique: undatierte Karte „Sankt Martin“ auf Aktuelles, Kennzahl „75 % Übertritt … 2021“.

**mobile-native:** keine graue Tipp-Fläche (eigene Rückmeldung beim Drücken), Hover-Bewegung auf Touch abgefangen, keine Textauswahl auf Knöpfen, Kalender-Wischen, `color-scheme: light`. Eingabefelder ≥ 16 px (kein iPhone-Zoom). Am echten Handy prüfen: Tipp-Rückmeldung, Wischen im Kalender, Statusleiste der installierten App.

## Animationen nach Emil Kowalski (16.11.2026)
Audit mit `improve-animations`, zehn Pläne in `plans/` (alle DONE), umgesetzt von einem eigenen Agenten, danach geprüft:
- Fokusrahmen springt bei Tab sofort (keine Bewegung bei Tastatur-Aktionen).
- Liste/Kalender: Abgang 120 ms ease-out statt ease-in.
- Sprungmarken-Marker, Umschalter-Knopf: per `clip-path` statt `width`, 250 bzw. 200 ms; Menü-Strich per `scale`.
- Kurzmeldungen erscheinen per Transition (`@starting-style`), unterbrechbar.
- Hover-Bewegung nur mit echter Maus (`hover: hover` und `pointer: fine`).
- Bereichsmenü: nur Spalten 40 ms versetzt, Zeilen sofort (fertig nach ca. 0,3 s).
- Kopfleiste wird fester über eine zweite Ebene mit Deckkraft (kein Neuzeichnen beim Scrollen).
- Viewport-Werte nur bei Änderung; eine ease-out-Kurve (`--io` = `--ease-out` = `cubic-bezier(.23, 1, .32, 1)`), JS liest die Tokens.
- Nachgebessert: zwei Fehler in den Plänen 006/008 (Reihenfolge der CSS-Regeln) – Pfeil in Bereichskarten und Zoom der Raumfotos wie vorher, alte „scrolled“-Regel der Kopfleiste entfernt.

## Web Interface Guidelines (16.11.2026)
Geprüft gegen die Vercel-Richtlinien und behoben:
- Schmuck-Bewegung läuft höchstens 5 s von selbst (WCAG 2.2.2): Status- und Geöffnet-Punkt pulsieren 2×, die Welle bewegt sich kurz beim Erscheinen des Fußbereichs, Ring ums Leitungsfoto und Wortwolke bewegen sich nur beim Überfahren. Bildwechsel im Bereichskopf hat einen Pause-Knopf (oben rechts).
- Zustand in der Adresse: `?thema=essen` (Fragen), `?ansicht=kalender` (Termine), `?abo=android` (Kalender-Abo) – teilbar und neu ladbar.
- Felder mit `name`, Platzhalter mit „…“, Ladehinweise mit „…“, Datum über `Intl.DateTimeFormat`.
- Fokus im Fragen-Helfer über `:focus-visible`; keine verdeckte `transition: all` mehr.
- Überlagerungen (Bildansicht, Geschichte, App-Fenster, Suche, Handy-Menü) geben das Scrollen nicht an die Seite weiter; schnelles Tippen ohne Zoom-Verzögerung, ruhige Tipp-Markierung.

## impeccable: polish · harden · document · typeset (16.11.2026)
Audit vorher 14/20. Umgesetzt:
- **polish:** keine Feder-Kurven mehr (Download-Haken, App-Symbol); Etikett am Handy 0.8rem ohne Sperrung; farbige Streifen an runden Karten entfernt (Downloads, Anschrift, Kurzinfo, Hinweis, Räume ohne Bild); Auswahlfarbe, Cursor, Scrollleiste, Unterstreichung im Palettenton.
- **harden:** „Bewegung reduzieren“ nimmt nur Bewegung im Raum weg, Farb- und Deckkraft-Rückmeldung bleibt; lange Wörter in Überschriften trennen sauber; Bereichskopf am Handy stärker abgedunkelt (Untertitel war auf hellen Fotostellen schwer lesbar).
- **document:** `DESIGN.md` (Leitbild „Die Wimpelkette“, Wirkung „ruhig und verlässlich“) und `.impeccable/design.json`. Feste Farben als Tokens: `--ink-rgb`, `--deep-rgb`, `--paper-rgb`, `--night-rgb`, `--white-rgb`, Zustandsfarben `--state-*`, Wortwolke, Ferienplan-Tönungen.
- **typeset:** Schriftgrößen auf eine Skala (0.75 · 0.84 · 0.92 · 1 · 1.0625 · 1.15 · 1.3 · 1.6 rem + Display/Ziffern), Rundungen auf eine Skala (3 · 6 · 8 · 10 · 12 · 14/22 · 16 · 20 · 28 · 999); Lesetexte höchstens 34em; Datei-Kürzel 0.75rem; Platzhalter-Kontrast ≥ 4.5:1.
- **Entscheidung:** Die Rosé-Etiketten über Überschriften bleiben (impeccable würde sie entfernen).
- Detektor danach: nur noch die bewusst so gestalteten Symbol-Kacheln der Info-Karten.

## Sicherheitsdurchsicht (16.11.2026)
Ganze Seite geprüft (statische Seite ohne Server-Code, keine Formulare, keine fremden Skripte). Abgesichert:
- Elternbrief-Texte und Grüße aus `elternbriefe.csv` werden jetzt als reiner Text ausgegeben (vorher wurde HTML übernommen). **Folge: In der Tabelle wirkt kein HTML mehr – Absätze weiter mit `||`.**
- Termintitel im Kalender, Durchwahl-Treffer und Suchtreffer werden maskiert; „Zuletzt angesehen“ übernimmt aus dem Browser-Speicher nur Links auf eigene Seiten und merkt sich keine Fehlerseiten.
- Inhalts-Sicherheitsregel (CSP) als `<meta>` in jeder Seite: nur eigene Skripte (plus Prüfsummen der zwei eingebetteten Skripte), Bilder, Schriften, keine fremden Server. Beim Hosting zusätzlich als HTTP-Kopfzeile setzen, dazu `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` und HTTPS mit HSTS.
- Nebenbei: Markierung in der Elternbrief-Suche saß bei „ß“ verschoben.
In Ordnung waren: Service Worker (nur eigene GET-Anfragen), externe Links mit `rel="noopener"`, Kalender-Dateien maskieren Sonderzeichen, Daten als eigene Datei statt eingebettet.

## Raster (15.11.2026)
Nach dem Spickzettel „Steal this grid“: Handy 4 Spalten, 16 px Rand, 16 px Abstand · Tablet (ab 701 px) 8 Spalten, 32 px Rand, 24 px Abstand · Computer 12 Spalten, Rand automatisch (Inhalt mittig, max. 1180 px), 24 px Abstand. Umgesetzt mit `--margin` und `--gutter` für `.container` und alle Karten-Raster.
- Behoben: Der Seitenname in der Leiste (Übergang 53) blieb in der Vorschau nach dem Wechsel von „Aktuelles“ zur Startseite stehen; er richtet sich jetzt immer nach der gerade sichtbaren Seite.

## Ja-Runde Kniffe, Ideen und Übergänge (15.11.2026)
Eingebaut nach der Abstimmung in den Sammlungen `kniffe`, `auswahl` (89–112) und `uebergaenge`.
- **Kniffe:** 1 verschachtelte Rundungen (Sprungmarken 14, Termine 22/10, Alters-Etikett 6, Kontaktkarte 28) · 2 Ränder aus der Textfarbe (`--rule` = `color-mix(currentColor 16 %)`, Knöpfe 50–55 %) · 3 OKLCH war schon da · 4 Foto-Verläufe in OKLab · 5 alle Symbole Strichstärke 1,8 · 6 weiche Kanten an Sprungmarken, Rundgang, Tabellen · 7 Symbolwechsel mit Unschärfe (Merken, Teilen, Downloads, Menü) · 9 `dvh` statt `vh` · 10 Original-Aushang als Vorschaubild mit `mix-blend-mode: multiply`. Nein: 8 Dunkelmodus.
- **Ideen:** 91 Themen-Knöpfe über den Fragen · 92 Bereichskarten kippen zur Maus · 97 Hinweis ohne Internet · 101 Welle zum Fußbereich · 102 Gruppensymbole bewegen sich · 106 Leitsatz schreibt sich (nur erster Besuch, 22 ms je Buchstabe) · 107 Schwung unter der Unterschrift · 109 Bilder im Bereichsmenü blättern.
- **Übergänge:** Seitenwechsel je nach Richtung (2 seitlich nach Menü-Reihenfolge, 7 Karte für Impressum/Datenschutz, 48 nach oben aus dem Kontakt-Band, 36 sonst ruhig) · 14 Fotos öffnen sich wie ein Fenster · 15/18 schon da · 16 Reiter-Inhalt gleitet mit · 17 Fenster wächst aus dem Knopf · 19 Bereichskopf wechselt Bilder mit Kamerafahrt · 25 Zeilen steigen auf · 27 Abschnitte schieben sich heran (auf Notiz-Wunsch) · 29 Lichtkante · 30 Pfeil fliegt durch · 31 Karten heben sich · 32 Häkchen zeichnet sich · 35 Strich im Menü · 42 Menü ohne Federn (200/140 ms) · 43 Knöpfe nur Farbe + 97 % · 44 Leiste wird nach und nach fester und verschwindet weiter beim Runterscrollen · 45 Wörter rollen um · 51 Linie unter Abschnittsköpfen · 52 Rundgang als Welle · 53 Titel in der Leiste (Kopf nur auf 92 % verkleinert) · 55 Telefon klingelt · 58 Platzhalter atmen · 59 Wimpel im Logo.
- Noch offen in der Abstimmung: Katalog 112, Übergänge 34 und 47 ohne Wahl; „Merken“ bleibt liegen.

## Design-Kniffe (15.11.2026)
Seite: `entwurf/ideen/kniffe.html` (gebaut mit `entwurf/ideen/mk_kniffe.py`, private Vorschau: https://claude.ai/artifact/XX628G1RyVpLSaSQwT7A8Z), Auswahl in der Datenbank-Sammlung `kniffe` (ids `kniff-1` … `kniff-10`). Die zehn Kniffe aus dem Bild, jeweils mit Vorher/Nachher an einem echten Bauteil der Seite. Bildvergleiche in `entwurf/kniffe/vorher-nachher/`.
- Schon da: 3 OKLCH-Farbstufen.
- Teilweise: 1 verschachtelte Rundungen, 2 durchsichtige Ränder, 7 Symbolwechsel mit Unschärfe (nur Kopieren-Knopf), 9 dvh (nur Handy-Suche).
- Fehlt: 4 OKLCH-Verläufe, 5 Symbol-Strichstärke 1,8 passend zu Schrift 600, 6 weiche Kanten an Wischreihen, 8 Dunkelmodus-Tiefe (nur falls je ein Dunkelmodus kommt), 10 Aushang mit `mix-blend-mode: multiply`.
- Noch nichts eingebaut – wartet auf die Abstimmung.

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

## Diese Woche auf einen Blick (17.11.2026)
- Startseite, Bereich „Aktuelles“: Wochenleiste Mo–Fr über den Terminen.
- Zeigt je Tag Feiertag, Schließtag (rosé) oder Termin (petrol), sonst „geöffnet“; heute ist umrandet.
- Pfeile blättern bis 30 Wochen vor; am Wochenende steht dort schon die kommende Woche.
- Daten kommen automatisch aus Schliesszeiten.csv, Feiertage und Termine.csv, keine eigene Pflege nötig.
- Höhe ist vorab reserviert (kein Springen), Handy: Tage untereinander.

## Bereichsseiten: Leiste & Kurzinfo (17.11.2026)
- Leiste „Auf dieser Seite“ enger (Abstand, Innenrand, Schrift .9rem), damit beim Kinderhort alle 9 Punkte ab ca. 1180 px Fensterbreite ganz sichtbar sind; schmaler wird weiter gewischt.
- „Das Wichtigste in Kürze“ auf Krippe, Kindergarten, Hort mittig.
- Rundgang (Maus): Bildtitel steht immer ganz sichtbar, Beschreibung klappt beim Darüberfahren darunter auf (vorher war der Titel abgeschnitten).
- Leiste „Auf dieser Seite“: sichtbar beim Scrollen, blendet 1,4 s nach dem Anhalten aus (nur wenn sie oben klebt; bleibt bei Maus darüber oder Tastaturfokus).
- Bereiche-Menü (Computer): schließt nach Klick auf einen Eintrag; öffnet erst wieder, wenn die Maus erneut auf „Bereiche“ zeigt.
- Fußzeile: „Bewegung aus“ steht jetzt in der Spalte „Seiten“ unter „Als App aufs Handy“; rechts unten Platz für den Nach-oben-Knopf (verdeckte vorher den Datenschutz-Link).
- Vorschau: Datenschutz-Seite aufgenommen (Link führte dort ins Leere).
- Leiste „Auf dieser Seite“: weicheres Verschwinden (0,7–0,8 s, sanfte Kurve, 14 px nach oben, minimal kleiner); Zurückkommen zügig (0,3–0,4 s).
- Leiste „Auf dieser Seite“: Klick setzt den Balken sofort auf den gewählten Punkt; er bleibt dort, bis man ca. 160 px weiterscrollt (vorher blieb er beim Punkt davor).

## Animations-Review umgesetzt (18.11.2026)
- Suche per „/“ oder Strg+K: sofort da (per Klick weiter mit Einblenden).
- Bildansicht per Pfeiltasten: sofort wechseln, 120 ms Überblenden (per Klick/Wischen wie bisher).
- Leiste „Auf dieser Seite“ und Abschnittstitel: kein top-Übergang mehr; beim Ein-/Ausblenden der Kopfleiste gleiten sie per translate (250 ms). Ausblenden der Leiste 0,5 s.
- Zuklappen: ease-out statt ease-in. Rundgang-Federn 240 ms, Bildunterschrift 250 ms.
- Pfeile in Knöpfen: 3 px Nachrutschen statt Flug. Menüpunkte rutschen per translate statt padding.
- Jahresband-Nadel per translate. Runde Knöpfe/Teilen 97 %. Neu-Punkt aus 50 % + Einblenden. Menü-Striche per translate.
- Galerie-Filter (Baustein einblicke(), derzeit auf keiner Seite eingebunden): 280 ms, unterbrechbar.

## Animations-Audit Runde 2 umgesetzt (18.11.2026)
- Handy-Menü schließt mit ease-out 240 ms (vorher ease-in 280 ms). Öffnen unverändert.
- Leiste „Auf dieser Seite“ und Abschnittstitel gleiten im Takt der Kopfleiste (500 ms, Kurven --ease-kopf-weg / --ease-kopf-da). Kopfleiste selbst unverändert (abgenommen).
- Bereichskarten heben sich sanft an (250 ms; translate fehlte im Übergang).
- Bilder im Bereiche-Menü: Einblenden 200 ms, Zoom 300 ms. Foto-Zoom beim Darüberfahren 450 ms (Aufdecken beim Scrollen bleibt 800 ms).
- Aufgeräumt: tote Übergangsregeln der Leiste entfernt, ease-in-Kurven ersetzt, Kopfleisten-Kurven als Werte.
- Logo-Fund zurückgenommen: die Drehung greift nicht (spätere Regel setzt sie auf 0).
- Drück-Rückmeldung (97 %, 160 ms) jetzt auch für „Morgen offen?“-Fragen, Vorschlags-Knöpfe auf Kontakt und den Pause-Knopf der Bildwechsel.

## Feinschliff nach Unslop-Prüfung (18.11.2026)
- Kein Lichtstreifen mehr über den Hauptknöpfen (Hover = Farbänderung).
- Bereichskarten: Kippen zur Maus entfernt, Anheben 3 px, Foto-Zoom 1,03.
- Große Fotos bewegen sich nicht mehr mit dem Scrollen; Welle über der Fußzeile ruhig.
- Hervorhebungen im Fließtext und „Das Wichtigste in Kürze“ Gewicht 500; Überschriften, Knöpfe und Status-Zeile unverändert.
- Nicht übernommen (bewusst): Einstieg der Startseite bleibt, rosé Schilder vor Abschnitten bleiben.

## Animations-Audit Runde 4 umgesetzt (18.11.2026)
- Tiefen-Effekt beim Scrollen entfernt (Startseiten-Fotos, Titelfoto der Bereichsseiten), samt Zusatz-Zoom 110 %.
- Große Startseiten-Fotos: Hover-Zoom 103 % (vorher 116 %).
- Telefon-Symbole (Gruppen-Knöpfe bei „Kind krankmelden“, Handy-Menü) wackeln nicht mehr beim Darüberfahren.
- Abschnitte gleiten nicht mehr an das Scrollen gekoppelt heran, Seitentitel schrumpft nicht mehr; einmaliges Einblenden bleibt.
- Aufgeräumt: tote Regeln von Tiefen-Effekt und Karten-Kippen entfernt. Handy-Menü: Einträge 300 ms mit abnehmendem Versatz (0/30/55/75/90/100 ms).

## Design-Review mit Taste Skill umgesetzt (20.11.2026)
- „Kontakt“ in der Kopfleiste/im Handy-Menü mit Rand statt gefüllt (gefüllt nur die Hauptaktion).
- Foto-Karten „Weißer Raum“/„Hauseigene Küche“ verlinken auf das Foto statt auf „#“ (Bildansicht öffnet weiter per Skript).
- Begrüßung oben bündig. „Jetzt geöffnet“-Karte: Farbe unverändert (neues Dunkeltürkis zurückgenommen, passte nicht zur Palette), Text in Papierweiß (5,9 : 1).
- Zwischenüberschriften (Foto-Karten, Bereichskarten, Wochenleiste) einheitlich 1,25rem.
- Fokus-Ring ohne Einblenden. Jahreszeiten-Teilchen im Startbereich entfernt.
- Offen zur Entscheidung: Text auf Fotos (1), Startbereich-Collage (2).
- Foto-Karten der Startseite: ganzes Foto (4 : 3), Text darunter (große Karten Petrol, Rundgang hell).
- Startbereich Mittelweg: Fotos leicht gekippt im 2×2-Raster ohne Überlappung, kleiner „3“-Sticker, oben bündig; Weißer-Raum-Foto in der Collage durch Leseecke ersetzt.
- „Ein Haus für jedes Alter“ linksbündig; „Alle Termine“ im Band als Rand-Knopf (Handy: eigene Zeile); Textlinks halbfett mit feiner Linie; Fußzeilen-Links am Handy 44 px; Schließtage-Knöpfe über dem Jahresband.
- Nach-oben-Knopf: am Handy 44 px, halbdurchsichtig solange er über Text liegt.
- Korrektur: „Kontakt“ in der Kopfleiste auf der Kontakt-Seite war nach der Rand-Umstellung fast unlesbar (1,74 : 1), jetzt 6,5 : 1.

## Unterseiten-Prüfung umgesetzt (20.11.2026)
- Titelbild der Unterseiten: kräftigerer Verlauf (Variante A).
- Rundgang-Bildtext auf Petrol-Fläche. Türkis-Karten (Info/Hinweis) Text in Papierweiß.
- „Zum Downloadbereich“ im rosé Band mit Rand. Geöffnete Seite im Menü (Computer) in Rosé.
- Tagesablauf: Linie steht fest (kein Zeichnen beim Scrollen mehr).
- „Alle Termine“ im Hinweisband am Handy über die volle Breite.
- „Das Wichtigste in Kürze“ und Karten-Titel (Zielgruppe …) als Beschriftung statt Überschrift ausgezeichnet.
- Rosé Hauptknöpfe mit feinem Petrol-Rand (auf Salbei sonst fast gleich hell). Einleitungstexte unter Abschnittsüberschriften in Vordergrundfarbe (Petrol, 6,5 : 1). Fehlerseite ebenso.
- Suchfelder (Fragen-Suche, Frage-Feld Kontakt) mit sichtbarer Beschriftung. Vorschlags-Knöpfe auf Kontakt mit Rand statt weiß.
- Impressum, Datenschutz, 404 mit Taste Skill geprüft: nur Hausregeln, außer dem 404-Text.

## Kinderhort: Pädagogik-Inhalte eingebaut (21.11.2026)
- Quelle: Text vom Hort (bisher auf der Seite der Josef-Grundschule), leicht bearbeitet, keine Bilder übernommen.
- Neuer Abschnitt „Pädagogik – So arbeiten wir im Hort“ (12 Lernbereiche + 8 aufklappbare Themen), in der Leiste „Auf dieser Seite“.
- Tagesablauf: Mo–Do 15:30–16:30 Freispiel/Angebot; Hortzeit endet 17:00, Spätdienst bis 18:00; Fr 14:00–14:15 Kinderkonferenz, 14:30–16:30 Ausflug.
- Zusammenarbeit mit Schulen: Erstklässler-Abholung (6 Wochen), Lehrersprechstunden 2× jährlich.
- Bestätigt vom Hort: Ferienfreizeit Österreich, zwei Köchinnen.
- Fotos: Hortgebäude (img/hortgebaeude.jpg, Galerie-Pfeil abgeschnitten) als 1. Foto der Collage; Berghütte (img/berghuette.jpg, rechter Ausschnitt ohne Personen) im Ferien-Thema. Gebäudefoto ist vom Hort selbst gemacht (Bildrechte geklärt).
- Sticker „3 Bereiche unter einem Dach“ wieder mit Text in der Mitte der Collage.

## Leiste „Auf dieser Seite“ (21.11.2026)
- Leiste auf allen Bereichsseiten mittig statt linksbündig.
- Kinderhort (10 Punkte): etwas enger gesetzt, damit „Schließtage“ ab 1180 px Breite wieder ganz sichtbar ist. „Zusammenarbeit mit Schulen“ bleibt ausgeschrieben.
- Schmaler als 1180 px (Tablet, Handy) lässt sich die Hort-Leiste wie bisher seitlich wischen.

## Foto Ferienfreizeit Österreich (21.11.2026)
- Neues Foto der Berghütte (von der Leitung geschickt) unter „Ferien und Ferienfreizeit“. Ganzes Foto, ohne Zuschnitt. Etwas größer angezeigt (bis 460 px).

## Streberclub entfernt (21.11.2026)
- Den Streberclub gibt es nicht mehr: Abschnitt unter „Pädagogik“ und Eintrag im Tagesablauf entfernt. Freispiel- und Angebotszeit Mo–Do bleibt 15:30–16:30 Uhr. Hütte: „am Fuße des Wilden Kaisers“ war falsch, jetzt nur „in Österreich“.

## Entwurf „Design neu“ (21.11.2026)
- Wunsch: gleicher Aufbau, gleiche Schrift (Plus Jakarta Sans), gleiche Farbpalette, nur schöner und hochwertiger. Liegt in `entwurf/design-neu/design-neu.css` und wird nach `css/style.css` geladen; Vorschau mit `entwurf/design-neu/build_vorschau_neu.py`.
- Abschnitte wechseln Salbei/Papier, Karten hell (Papier) mit Petrol-Schrift und feinem Rand, Zahlen ohne Kästen, Fotos mit Text darunter, gerade Collage, Hauptknöpfe Petrol.
- Gilt als gemerkte Richtung für weitere Gestaltung. Noch nicht in die echte Seite eingebaut.
- Zweiter Entwurf „Design neu 2“ (`entwurf/design-neu-2/`): Startbereich nur Text, Fotos wie im ersten Entwurf (Haus quer oben, drei Raumfotos darunter); Status-Karte und „Kind krankmelden“ stehen unter „Termine & Unterlagen“ (Verschiebung im HTML über `umbau.py`).

## Startseite: Fotos und Kästen nach Entwurf „Design neu 2“ (21.11.2026)
- Nur auf der Startseite und nur zwei Dinge übernommen, sonst bleibt alles im bisherigen Design:
  - Fotos im Startbereich: Haus groß und quer oben, drei Raumfotos darunter, gerade; „3 Bereiche“-Kreis rosé oben rechts.
  - Status-Karte und „Kind krankmelden“ aus dem Startbereich unter „Termine & Unterlagen“ (über der Wochenübersicht) verschoben. Sprungmarke `#krankmelden` bleibt.

## Verbesserungen eingebaut (21.11.2026)
- Link „Kind krankmelden →“ im Startbereich unter den Knöpfen; öffnet den Kasten unter „Termine & Unterlagen“ (auch beim zweiten Klick).
- Status-Karte und Krankmeldung dort hell und gleich hoch.
- Hinweisband „Nächster Termin“ nur, wenn der Termin in höchstens 3 Tagen ist.
- Kinderhort-Leiste „Auf dieser Seite“ zwischen 700 und 1180 px zweizeilig.
- „Hort“-Schildchen in der Terminliste mit dunklerem Grund (Kontrast).
- Punkt 5 (hellere Karten): vier Entwürfe in `entwurf/karten-varianten/` (A Papier, B Offen, C Rahmen, D Gemischt), Vergleich als Vorschau.

## Kartenstil A „Papier-Karten“ eingebaut (21.11.2026)
- Alle Karten der Website hell (Papier) mit Petrol-Schrift, feinem Rand und weichem Schatten statt dunklem Türkis; Fotos sitzen mit schmalem Rand in der Karte, Text darunter. Aus `entwurf/karten-varianten/` (hell-basis + a-papier).
- Türkis bleibt für Hinweisband, Schließtage-Leiste und Fußbereich.
- Ferienplan-Tabelle angepasst: vergangene Zeilen gedämpft in Petrol, auf dem Handy helle Zeilen.
- Startseiten-Varianten (`entwurf/landing-varianten/`): 1 Bühne (Startbereich Petrol), 2 Papier (heller Start, Fotos auf Salbei-Fläche), 3 Zentriert (Text mittig, Fotos in einer Reihe); Einblendung beim Laden per GSAP-Timeline (GSAP-Skills), nichts am Scrollen; Umschalter nur in der Vorschau.
  - Entscheidung 21.11.2026: keine der drei Varianten, die jetzige Startseite bleibt.

## Web Interface Guidelines umgesetzt (21.11.2026)
- Sichtbarer Fokus im Suchfenster und im Frage-Feld (Kontakt), Sprungziele auf Seiten ohne Leiste nur 96 px versetzt, Suchfeld ohne Rechtschreibprüfung, „Grombühl“ mit translate="no", Tage bis zum Termin mit einem einzigen „jetzt“ berechnet.
- Vorschau „Weniger Vorlage“ (`entwurf/muster/`): redundante Etiketten weg, Rundgang als offene Fotoreihe, nur noch Kreis um „Qualität“, Zahlen als Satz, Kontakt mit großer Krankmeldung und Liste, Abschluss ohne Kasten, genauere Linktexte. Noch nicht eingebaut.

## Weniger Vorlage eingebaut (22.11.2026)
- Startseite: Etiketten „Das zeichnet uns aus“, „Virtueller Rundgang“, „Aktuelles“, „Schließtage“ entfernt (section() lässt leeres Etikett weg); Zahlen als Satz (`.fakten`); Rundgang als offene Fotoreihe (`.rundgang-reihe`); nur Kreis um „Qualität“; Abschluss ohne Kasten (`.cta-offen`); Linktexte „Zur Kinderkrippe“ usw.
- Kontakt: „Kind krankmelden“ groß in Rosé, übrige Wege als Liste.
- Vorschau Kinderhort-Etiketten (`entwurf/hort-etiketten/`): 6 von 10 entfallen (Räumlichkeiten, Tagesablauf, Das zeichnet uns aus, Zusammenarbeit mit den Schulen, Meistgestellte Fragen, Schließtage).
- Etiketten auf den Bereichsseiten aufgeräumt (22.11.2026): entfallen sind Tagesablauf, Das zeichnet uns aus, Meistgestellte Fragen, Schließtage (alle drei), Räumlichkeiten (Kindergarten, Kinderhort) und Zusammenarbeit mit den Schulen (Kinderhort). Bei der Krippe bleibt „Räumlichkeiten“, weil die Überschrift „Viel Platz für die Kleinsten“ die Räume nicht nennt.

## Handy-Menü und Rundgang (22.11.2026)
- Kasten „Wir sind für Sie da“ (Telefon, E-Mail, Anschrift) aus dem Handy-Menü entfernt (NAV_EXTRA wird nicht mehr eingesetzt).
- Kontakt-Knopf im Handy-Menü Petrol gefüllt.
- Rundgang auf Touch-Geräten: kein dunkler Verlauf mehr hinter dem Bildtext; weiche Kanten der Fotoreihe 16 statt 32 px.
- Kontakt (23.11.2026): Telefon der Zentrale und allgemeine E-Mail als erste Einträge der Liste unter „Kind krankmelden“.
- Vorschau „Kontakt kompakt“ (`entwurf/kontakt-kompakt/`): Telefon/E-Mail als große Knopfzeile ganz oben, Status klein daneben, darunter vier gleiche Einträge (Kind krankmelden, Platz anfragen, Abholung, Abwesenheit) in einer Reihe. Noch nicht eingebaut.
- Vorschau „Verbesserungen 2“ (`entwurf/verbesserungen-2/`): Kontakt kompakt + Anschrift ohne Telefon/E-Mail; Rundgang-Titel aus den Bildtexten („die Puppenecke“ → „Puppenecke“ / „im Gruppenraum“, 20 Bilder). Zeitangaben-Liste (55 Angaben) und Ladezeitmessung erstellt. Hausfoto: es gibt kein größeres Original.

## Kontakt kompakt, Rundgang-Titel, schnellere Startseite eingebaut (23.11.2026)
- Kontakt: Telefon/E-Mail als Knopfzeile mit Öffnungsstatus, darunter vier gleiche Einträge (Kind krankmelden, Platz anfragen, Abholung, Abwesenheit); Anschrift nur mit Adresse, Route und vCard.
- Rundgang: `tour_titel()` macht aus kurzen Bildtexten den Titel („Puppenecke“ – „im Gruppenraum“).
- Startseite: nur das Hausfoto lädt sofort (fetchpriority high), die drei kleinen Fotos verzögert und in passender Größe. Gemessen auf schwachem 3G: größtes Element 10,6 → 7,4 s (ohne Komprimierung), gutes 4G 2,1 → 1,8 s.
- Offen: Zeitangaben – die Leitung schickt die richtigen Uhrzeiten (drei Rückfragen in der Liste).
- Vorschau „Verbesserungen 3“ (`entwurf/verbesserungen-3/`): Aktuelles ohne „Vormerktermine“/„Schließtage“-Etikett, Kontakt mit Links zu den Fragen je Bereich, Downloads: Dateien nur einmal („Für alle Bereiche“, „Nur Kinderhort“), ruhigere Dateizeilen, ohne Etiketten „Downloads“/„Kalender“ und ohne Schlussabschnitt. Noch nicht eingebaut.
- Start-Checkliste für die Leitung erstellt (Uhrzeiten, 4 Kreativraum-Fotos benennen, Impressum, Datenschutz, Foto-Einverständnis, PDF-Autor, Domain/Umzug, HTTPS, Handy-Test, spätere Wünsche).

## Verbesserungen 3 eingebaut, Fragefeld schlauer (23.11.2026)
- Aktuelles ohne Etiketten „Vormerktermine“/„Schließtage“; Kontakt mit Links zu den Fragen je Bereich; Downloads: „Für alle Bereiche“ + „Nur Kinderhort“, helle Dateizeilen, ohne Etiketten „Downloads“/„Kalender“ und ohne Schlussabschnitt.
- „Fragen Sie einfach“: versteht jetzt Wochentage und Daten („Haben Sie am 24.12. offen?“), Medikamente, Abholung durch andere Personen, Abwesenheit/Urlaub des Kindes, Fragen nach Kosten (Verweis auf persönliches Gespräch), Telefonnummer je Bereich; Synonyme (Essen/Mittagessen/Brotzeit, Schlaf/Ruhezeit, Windel/Wickeln …); bevorzugt Antworten aus dem genannten Bereich. Bereichswörter allein („Krippe“) lösen keine Durchwahl mehr aus.
- Wichtiger Hinweis (`daten/dringend.csv`, Spalten von;bis;Text): eingebaut, aber leer – ohne Eintrag ändert sich nichts. Erscheint oben auf allen Seiten und in der Status-Anzeige. Vorschau mit Beispiel: `entwurf/dringend/`.
- Aushang A4 mit QR-Codes (Website, Kind krankmelden, Termine abonnieren): `entwurf/aushang/aushang.pdf`, erzeugt mit `aushang.py` (Paket qrcode). QR-Codes vor dem Aushängen mit einem Handy testen, sobald die Domain läuft.
- Fehlerseite und Weiterleitungen alter WordPress-Adressen gab es schon (404.html, .htaccess).
- Team-Anleitung aktualisiert (23.11.2026): neuer Schritt 6 „Wichtiger Hinweis“ (dringend.csv), Übersicht ergänzt, neue Bildschirmfotos im hellen Kartenstil; PDF neu: Anleitung-Webseite-pflegen.pdf (8 Seiten).

## Generalprobe (23.11.2026)
- Alle 10 Seiten × 5 Breiten (320, 390, 768, 1280, 1920): keine Skriptfehler, keine fehlenden Dateien oder Bilder, alle Bilder mit Alt-Text, 306 interne Links und alle Sprungziele vorhanden, Telefon- und E-Mail-Links korrekt, Druck des Ferienplans ohne Kopfleiste, offline erreichbar (Service Worker), Fragefeld 16 Beispielfragen.
- Behoben: Downloads ragten bei 320 px über den Rand („Medikamentenvereinbarung“); Kalenderdateien falten lange Zeilen jetzt nach RFC 5545 (für Outlook).
- Kreativraum-Fotos benannt (23.11.2026): „Blick aus der Bauecke – in den Kreativraum“, „Unser Kreativraum – Freizeitbereich der Hortkinder“, „Piratenausguck – im Kreativraum“, „Blick über den ganzen Raum – im Kreativraum“. Alt-Text des Piratenausguck-Fotos auf der Startseite korrigiert (hieß fälschlich „Kind an der Weltkarte“).
- Startseite „Termine & Unterlagen“ (23.11.2026): Krankmelde-Kasten wird nicht mehr auf die Höhe der Status-Karte gestreckt (wirkte leer).
- „Kind krankmelden“ von der Startseite entfernt (23.11.2026): steht nur noch auf der Kontaktseite. Links (Startseite, Fragefeld, App-Verknüpfung, Aushang-QR, alte „#krankmelden“-Links) führen zu kontakt.html#schnell. Datenschutz: Hinweis auf gespeicherte „zuletzt angerufene Gruppe“ entfernt. Rahmen der Status-Karte heißt jetzt .heute-zeile (die alte Klasse .heute verstellte den heutigen Tag in der Wochenübersicht).
- Stresstest (23.11.2026, Skills mobile-native + break-ui, Testkopie mit extremen Daten): Funde 1 Semikolon im CSV-Text schneidet still ab, 2 Termine über mehrere Monate im Datumsfeld zerbrochen, 3 85 Hover-Effekte ohne Maus-Abfrage (bleiben auf dem Handy hängen), 4 Knopftexte markierbar, 5 langer Wichtiger Hinweis füllt den Handy-Bildschirm. Behebung als Skript `entwurf/stresstest/verbessern.py <ordner>` – am 23.11.2026 eingebaut (82 Hover-Regeln jetzt nur mit Maus). Hinweis zu Semikolons in LIESMICH.txt.
- Kleine Änderungen 1 und 2 eingebaut (23.11.2026): Krippe-Räume ohne Foto als offene Textzeilen; Küchentext gekürzt („Zwei Köchinnen kochen täglich frisch und mit regionalen Zutaten – nach aktuellen ernährungswissenschaftlichen Grundsätzen.“). Punkt 3 (Mail-Zeile bei Durchwahlen) bleibt.
- Handy-Runde (23.11.2026): A Bereichskarten der Startseite auf dem Handy kompakt (Foto ~38 % links, voller Text rechts); B Knöpfe oben auf dem Handy gleich breit, nur so breit wie der längere Text. C (doppelte Infos Kurz-Kasten / Auf einen Blick) als Vorschau mit Varianten a/b/c, Entscheidung offen.
