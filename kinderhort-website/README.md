# Webseite – Kath. Kinder- und Jugendhort Grombühl e. V.

Neu gestaltete, statische Webseite mit allen Inhalten, Bildern und Downloads der bisherigen Seite
kinderhort-grombuehl.de.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite: Bereiche, Begrüßung der Einrichtungsleitung, Highlights, Ferienplan |
| `kinderkrippe.html` | Zielgruppe, Öffnungszeiten, Räume, virtueller Rundgang, Tagesablauf, FAQ |
| `kindergarten.html` | dto. für den Kindergarten |
| `kinderhort.html` | dto. für den Kinderhort, inkl. Zusammenarbeit mit den Schulen |
| `aktuelles.html` | Vormerktermine, Elternbrief, Schließtage 2026/2027 |
| `downloads.html` | Ferienplan, KinderhortABC, Medikamentenvereinbarung (PDF) |
| `kontakt.html` | Durchwahlen aller Gruppen, Anschrift, E-Mail |
| `impressum.html` | Impressum (DDG) |
| `datenschutz.html` | Datenschutzerklärung – **Vorlage, markierte Stellen ergänzen** |

## Ansehen

Ordner auf einen beliebigen Webspace hochladen – fertig. Lokal z. B.:

```bash
cd kinderhort-website
python3 -m http.server 8000   # dann http://localhost:8000 öffnen
```

Kein CMS, keine Datenbank, keine externen Dienste: Schriften (Nunito, Fredoka – SIL Open Font License)
liegen lokal in `fonts/`, es werden keine Google-Server oder Tracker geladen.

## Termine, Schließtage, Feiertage pflegen

Ohne Programmierkenntnisse: die Dateien in `daten/` (CSV, mit Excel/LibreOffice oder Texteditor) ändern
und danach `python3 build.py` ausführen – siehe `daten/LIESMICH.txt`. Daraus entstehen automatisch:
Ferienplan-Tabelle, Terminliste (vergangene Termine werden ausgeblendet), die Anzeige
„Heute geöffnet / nächste Schließzeit“ (`js/daten.js`) und die Kalenderdateien `downloads/*.ics`.

## Veröffentlichen

- Webadresse steht in `build.py` (`SITE`) – wird für Google-Vorschau, `sitemap.xml` und Teilen-Bild genutzt.
- `.htaccess` leitet die alten WordPress-Adressen auf die neuen Seiten um (Apache-Webspace) und sperrt
  die Arbeitsordner `entwurf/` und `daten/`. Auf anderen Servern die Weiterleitungen entsprechend einrichten.
- Nicht mit hochladen müssen: `entwurf/`, `daten/`, `build.py`, `build_vorschau.py`, `vorschau.html`, `NOTIZEN.md`.

## Inhalte ändern

Alle Seiten werden aus `build.py` erzeugt (gemeinsamer Kopf-/Fußbereich, Texte, Tagesabläufe,
FAQ, Ferienplan in `PLAN`). Text in `build.py` anpassen und neu erzeugen:

```bash
pip install pillow   # einmalig
python3 build.py
```

Neue Bilder in `img/` ablegen (am besten max. 1600 px breit), neue PDFs in `downloads/`.

## Hinweis

Die bisherige Seite hat keine Datenschutzerklärung verlinkt. Vor dem Livegang sollte eine
Datenschutzerklärung ergänzt werden.
