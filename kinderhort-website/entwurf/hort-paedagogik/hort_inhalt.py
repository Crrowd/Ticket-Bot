import sys
B = sys.argv[1].rstrip('/') + '/'
def patch(path, pairs):
    s = open(B + path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:80])
        s = s.replace(a, b)
    open(B + path, 'w', encoding='utf-8').write(s)

PAED = r'''
def paed_item(titel, html):
    return f'<details class="lotse-item paed-item" name="paed"><summary>{titel}</summary><div>{html}</div></details>'

def liste(punkte, nummeriert=False):
    tag = "ol" if nummeriert else "ul"
    return f'<{tag} class="paed-liste">' + "".join(f"<li>{p}</li>" for p in punkte) + f"</{tag}>"

LERNBEREICHE = ["Ethik und Religion", "Sprache und Literacy", "Mathematik", "Naturwissenschaft und Technik", "Umwelt und Natur", "Medien und IT",
                "Ästhetik und Kunst", "Musik", "Bewegung", "Gesundheit", "Demokratie", "Mitbestimmung und Partizipation"]

PAED_HORT = (
  '<div class="paed-lern reveal"><p class="paed-lern-t">Wir orientieren uns an diesen Lernbereichen:</p><ul class="paed-chips">'
  + "".join(f"<li>{x}</li>" for x in LERNBEREICHE) + '</ul></div>'
  + '<div class="lotse paed reveal">'
  + paed_item("Lernen durch Handeln",
      "<p>Ganzheitliche Bildung bedeutet für uns, dass Lernen über das Handeln geschieht. Nach Pestalozzi ist die Anschauung das Fundament aller Erkenntnis. "
      "Nach diesem Prinzip arbeiten wir: Zu einem Thema veranstalten wir mit den Kindern zum Beispiel eine Exkursion, betrachten ein Bilderbuch, recherchieren im Internet, "
      "befragen Experten, studieren einen Tanz ein oder gestalten eine künstlerische Gemeinschaftsarbeit.</p>"
      "<p>Unsere Angebote richten sich an der Motivation der Kinder aus. Sie sind freiwillig, damit die Kinder wissbegierig teilnehmen, Fragen stellen und das Gelernte auf ihr Leben übertragen.</p>")
  + paed_item("Hausaufgaben",
      "<p>Von Montag bis Donnerstag erledigt jedes Kind seine Hausaufgaben im Hort. Nach Alter, Reife und Klasse sind die Kinder in zwei Hausaufgabengruppen eingeteilt. "
      "Von 14:00 bis 15:00 Uhr arbeiten alle Kinder leise an ihrem Platz. Wer um 15:00 Uhr noch nicht fertig ist, kann in der Resthausaufgabenzeit bis 15:30 Uhr weiterarbeiten.</p>"
      "<p>Die pädagogischen Fachkräfte helfen bei Bedarf und erklären, wenn nötig. Fertige Hausaufgaben werden auf Vollständigkeit und Richtigkeit korrigiert: "
      "Fehler bekommen einen <strong>grünen Punkt</strong>, das Kind verbessert sie und lässt die Verbesserung erneut korrigieren. Ist alles richtig, stempelt die Erzieherin die Aufgabe ab und unterschreibt.</p>"
      "<p>Wird ein Kind auch in der Resthausaufgabenzeit nicht fertig, kleben wir einen <strong>roten Zettel</strong> ins Heft. Er zeigt Eltern und Lehrkräften, dass die Aufgabe nicht fertig wurde, obwohl das Kind 90 Minuten gearbeitet hat. "
      "Ob die Aufgabe zu Hause noch fertig gemacht wird, entscheiden die Eltern.</p>"
      '<div class="paed-zwei"><div><p class="paed-sub">Die drei Regeln der Hausaufgabenzeit</p>' + liste(["Ruhig arbeiten", "Am Platz sitzen", "Bei Fragen melden"], True) + "</div>"
      '<div><p class="paed-sub">Das hat jedes Kind an seinem Platz</p>' + liste(["einen eigenen Schreibtisch und Stuhl", "Hilfsmittel und Anschauungsmaterial wie Hundertertafel, Rechenschieber, Spielgeld oder Uhr", "Arbeitsblätter, Lernspiele und Bücher zur Unterstützung"]) + "</div></div>")
  + paed_item("Freizeit und offene Arbeit",
      "<p>Die Freizeitgestaltung ist ein wesentlicher Schwerpunkt unserer Arbeit und ein wichtiger Ausgleich zum schulischen Lernen. Wir arbeiten nach einem offenen Konzept: "
      "Außerhalb der Hausaufgabenzeit bewegen sich die Kinder frei in allen Räumen und wählen ihren Spielort nach ihren eigenen Interessen. "
      "Sie spielen allein, in kleinen und großen Gruppen, malen, basteln, konstruieren oder schlüpfen ins Rollenspiel. "
      "Zum Ausruhen gibt es den Weißen Raum mit Lichtdusche, Wasserbett und Wassersäulen, ein Bällebad und eine gemütliche Leseecke, für Bewegung die Turnhalle und ein großzügiges Außengelände.</p>"
      + liste(["Die Kinder entscheiden selbst, welche Spielbereiche sie nutzen, und wählen ihre Spielpartner.",
               "Es entstehen altersübergreifende Kontakte zu allen Kindern des Hortes.",
               "Montag bis Donnerstag bietet jeden Tag eine Erzieherin oder ein Erzieher ein anderes Angebot an, z. B. Fußballspiel, Kuchen backen, Yoga oder Malen auf Leinwand. Die Teilnahme ist freiwillig.",
               "Freitag ist Freizeittag ohne Hausaufgaben, mit einem Ausflug, z. B. in die Bücherei, zur Schnitzeljagd oder auf den Abenteuerspielplatz.",
               "Einmal im Jahr gibt es ein größeres Projekt, dessen Thema die Kinder selbst wählen, außerdem längere Projekte in Kleingruppen, z. B. Foto, Theater oder Entspannung."]))
  + paed_item("Streberclub",
      "<p>Von Montag bis Donnerstag findet von 16:30 bis 17:00 Uhr der Streberclub statt. Jedes Hortkind kann ihn mit seiner eigenen Mitgliedskarte besuchen. "
      "Hier begleiten wir das Lernen zusätzlich und spielerisch, zum Beispiel mit:</p>"
      + liste(["Knobelspielen", "Internetrecherche", "Mathematik-Tricks und -Rätseln", "Lesetraining", "Sprachspielen", "der Geschichtenwerkstatt"]))
  + paed_item("Kinderkonferenz und Mitbestimmung",
      "<p>Jeden Freitag treffen sich alle Hortkinder und Erzieher im Turnraum zur Kinderkonferenz. Sie beginnt immer mit der „Lobhudelei“: "
      "Besondere Leistungen einzelner oder mehrerer Kinder aus der Woche werden vor allen gelobt. Danach werden aktuelle Themen besprochen, Informationen weitergegeben und die Ausflüge für den Nachmittag vorgestellt. "
      "Die Kinder gestalten ihren Hortalltag aktiv mit, zum Beispiel stimmen sie über den Ferienplan oder das Projektthema ab.</p>"
      + liste(["Kinderkonferenz jeden Freitag", "Abstimmung des Ferienprogramms", "Schriftliche Kinderbefragung", "Einmal im Monat ein „feines“ Mittagessen mit Wunschessen der Kinder und besonders schön gedecktem Tisch"]))
  + paed_item("Ferien und Ferienfreizeit",
      "<p>In den Schulferien wird die gemeinsame Freizeit noch wichtiger: Die Kinder bauen Schulstress ab und gehen ihren eigenen Interessen nach. "
      "Das Ferienprogramm schlagen die Hortkinder selbst vor und wählen es in der Kinderkonferenz gemeinsam aus. Oft beginnt der Ferientag mit einem Frühstücksbuffet, zu dem jedes Kind etwas beisteuert.</p>"
      + liste(["Verlässlich geöffnet in den Schulferien von 6:45 bis 18:00 Uhr, höchstens 30 Schließtage im Jahr",
               "Tägliche Aktionen, z. B. Schwimmbad, Eisbahn, Zoo, Kegeln, Kinderkino oder Fußballturnier",
               "Gemeinsames Frühstück und Mittagessen"])
      + "<p><strong>Ferienfreizeit in Österreich:</strong> Ein Höhepunkt im Hortjahr ist die einwöchige Ferienfreizeit am Ende der Sommerferien. "
      "Für viele Kinder ist es die erste Reise ohne Eltern. Am Fuße des Wilden Kaisers steht unsere Berghütte. Von dort aus wandern wir in den Bergen, erkunden das Landleben und kochen jeden Abend selbst. "
      "Zur Hütte gehören ein Hüttenhund, zwei Esel und sogar ein kleiner Swimmingpool.</p>")
  + paed_item("Mittagessen aus der eigenen Küche",
      "<p>Als eine der wenigen Kitas in Bayern haben wir eine hauseigene Küche: Zwei Köchinnen kochen täglich frisch und kindgerecht, überwiegend mit regionalen Lebensmitteln. "
      "Was morgens gekocht wird, steht mittags auf dem Tisch. Die Kinder essen in gemütlicher Runde im Bistro.</p>"
      '<p class="paed-sub">Unsere Qualitätskriterien</p>'
      + liste(["Lebensmittel überwiegend aus regionalem Anbau, keine Fertigprodukte",
               "20-mal im Monat Gemüse oder Salat",
               "8-mal im Monat Speisen mit Fleisch",
               "Mehrmals im Monat kindgerechte Fischgerichte, kein Pressfisch",
               "Auch Vollkornprodukte und Hülsenfrüchte",
               "Rücksicht auf die Besonderheiten anderer Religionen",
               "Viele Nachspeisen aus frischem Obst",
               "Butter und hochwertige Speiseöle, kein Palmöl",
               "Keine Geschmacksverstärker",
               "Rücksicht auf ärztlich nachgewiesene Lebensmittelunverträglichkeiten",
               "Aktuelle Speisepläne hängen an mehreren Stellen in der Kita aus",
               "Einhaltung der HACCP-Richtlinien, Allergene werden ausgewiesen"], True))
  + paed_item("Zusammenarbeit mit den Eltern",
      "<p>Schon vor dem ersten Schultag laden wir die Eltern der künftigen Hortkinder zu einem Schnuppertag ein, mit wichtigen Informationen zum Hortalltag und zur Einschulung. "
      "Kurz nach der Einschulung gibt es einen Elternabend für die Eltern der neuen Erstklässler zum Schuleinstieg und zum ersten Lesen, Schreiben und Rechnen. "
      "Im Laufe des Hortjahres folgen zwei Elternabende mit Einzelgesprächen über den schulischen Stand und die Freizeit Ihres Kindes im Hort.</p>"
      + liste(["Gespräche zwischen Tür und Angel jederzeit, feste Sprechstunden nach Absprache",
               "Auf Wunsch begleiten wir Sie zu Gesprächen mit der Lehrkraft in die Schule",
               "Elternbeirat, jedes Jahr neu gewählt: Er vertritt alle Eltern, berät und wird in wichtige Entscheidungen einbezogen",
               "Elternbriefe mit Terminen und Neuigkeiten, Handzettel zu Ausflügen",
               "Feste und Feiern gestalten wir gemeinsam, Ihre Mithilfe ist dabei herzlich willkommen"]))
  + "</div>"
)
'''

patch('build.py', [
 # Bausteine vor der Kinderhort-Seite definieren
 ('hort = page_hero("Kinderhort",', PAED + '\nhort = page_hero("Kinderhort",'),
 # Leiste „Auf dieser Seite“: Pädagogik ergänzen
 ('[("ueberblick", "Überblick"), ("raeume", "Räumlichkeiten"), ("rundgang", "Virtueller Rundgang"), ("tagesablauf", "Tagesablauf"), ("auszeichnung", "Das zeichnet uns aus"), ("schulen", "Zusammenarbeit mit Schulen"),',
  '[("ueberblick", "Überblick"), ("paedagogik", "Pädagogik"), ("raeume", "Räumlichkeiten"), ("rundgang", "Virtueller Rundgang"), ("tagesablauf", "Tagesablauf"), ("auszeichnung", "Das zeichnet uns aus"), ("schulen", "Zusammenarbeit mit Schulen"),'),
 # neuer Abschnitt nach „Auf einen Blick“
 ('hort += section("raeume", "Räumlichkeiten", "Räume für Hausaufgaben, Kreativität und Erholung", "", rooms([',
  'hort += section("paedagogik", "Pädagogik", "So arbeiten wir im Hort", "Unser Ziel ist es, jedem Kind eine ganzheitliche Handlungs-, Leistungs- und Lernfähigkeit zu vermitteln. Bildung ist für uns nicht nur Förderung, sondern etwas ganz Alltägliches: Wie erfolgreich Kinder in der Schule lernen, hängt entscheidend davon ab, wie neugierig und motiviert sie sind und wie viel Spaß sie am Lernen haben.", PAED_HORT)\n'
  'hort += section("raeume", "Räumlichkeiten", "Räume für Hausaufgaben, Kreativität und Erholung", "", rooms(['),
 # Tagesablauf nach dem neuen Text
 ('''    ("15:00 – 16:00 Uhr", "Freizeit für alle Hortkinder. Die Kinder können sich entscheiden, wo und mit wem sie spielen. Ab 15:30 Uhr findet ein angekündigtes Angebot statt, an dem sich die Kinder freiwillig beteiligen können."),''',
  '''    ("15:30 – 16:30 Uhr", "Freispiel und Angebotszeit: Alle Bereiche stehen den Kindern offen. Zusätzlich gibt es jeden Tag ein anderes Angebot, z. B. Werken, Häkeln oder Bewegungsspiele, an dem die Kinder freiwillig teilnehmen können."),
    ("16:30 – 17:00 Uhr", "Streberclub: spielerische Lerngruppe für interessierte Hortkinder, z. B. Knobelspiele, Mathe-Rätsel, Lesetraining oder Geschichtenwerkstatt."),'''),
 ('''    ("14:00 Uhr", "In der wöchentlichen Kinderkonferenz besprechen die Kinder wichtige Informationen und aktuelle Themen, wie z. B. Freitagsausflüge. Ferienpläne werden von den Kindern abgestimmt."),
    ("14:30 – 16:30 Uhr", "Immer freitags findet ein Ausflug im Stadtgebiet von Würzburg statt. Die Teilnahme am Ausflug ist für die Kinder freiwillig. Freitags findet keine Hausaufgabenbetreuung im Hort statt."),''',
  '''    ("14:00 – 14:15 Uhr", "In der Kinderkonferenz treffen sich alle Hortkinder und Erzieher: Lob für die Woche, wichtige Informationen und gemeinsame Entscheidungen, z. B. über den Ferienplan oder das „feine Mittagessen“."),
    ("14:30 – 17:00 Uhr", "Freitagsausflug und Freispielzeit: Je nach Interessen, Jahreszeit oder Gruppenthema geht es in die Stadt, in die Natur, zu Veranstaltungen, zum Spielen oder zum Sport. Die Teilnahme ist freiwillig, wer nicht mitkommt, wird im Hort betreut. Freitags gibt es keine Hausaufgaben."),'''),
 ('''    ("16:30 – 18:00 Uhr", "Je nach gebuchter Zeit können die Kinder bis 18:00 Uhr im Hort bleiben."),''',
  '''    ("17:00 – 18:00 Uhr", "Die allgemeine Hortzeit endet um 17:00 Uhr. Kinder, deren Eltern mehr Zeit gebucht haben, besuchen bis 18:00 Uhr den Spätdienst."),'''),
 # Zusammenarbeit mit den Schulen ergänzen
 ('''  <p>Wir sind offen für alle Schulformen: Grundschulen, Mittelschulen, Realschulen, Gymnasien sowie Förderschulen.</p></div>''',
  '''  <p>In den ersten sechs Wochen des Schuljahres holt die zuständige Erzieherin die Erstklässler täglich direkt vor dem Klassenzimmer ab. So sind in der Anfangszeit jeden Tag kurze Absprachen mit der Lehrkraft möglich.</p>
  <p>Danach besuchen unsere Fachkräfte zweimal im Jahr die Lehrersprechstunden und sprechen über jedes Hortkind: Wie können wir es noch besser fördern und begleiten? Bei Bedarf tauschen wir uns jederzeit mit den Lehrkräften aus oder begleiten Sie in die Sprechstunde.</p>
  <p>Wir sind offen für alle Schulformen: Grundschulen, Mittelschulen, Realschulen, Gymnasien sowie Förderschulen.</p></div>'''),
])

open(B + 'css/style.css', 'a', encoding='utf-8').write('''
/* ===== Kinderhort: Abschnitt „Pädagogik“ (21.11.2026) ===== */
.paed-lern { margin: 0 0 24px; }
.paed-lern-t, .paed-sub { margin: 0 0 10px; font: 600 .9rem/1.4 var(--font-body); color: var(--ink); }
.paed-chips { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 8px; }
.paed-chips li { padding: 6px 12px; border-radius: 999px; background: var(--paper); color: var(--ink); font-size: .9rem; font-weight: 500; box-shadow: inset 0 0 0 1px rgb(var(--ink-rgb) / .12); }
.paed-liste { margin: 0 0 14px; padding-left: 1.2em; display: grid; gap: 6px; }
.paed-liste li { line-height: 1.5; }
.paed-item > div > p { max-width: 70ch; }
.paed-zwei { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 8px; }
@media (max-width: 700px) { .paed-zwei { grid-template-columns: minmax(0, 1fr); } }
''')
print('ok')
