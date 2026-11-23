# Vorschau „Wichtiger Hinweis“: die normale Vorschau mit einem Beispiel-Eintrag in dringend.csv (nur in der Vorschau)
#   python3 entwurf/dringend/build_vorschau.py <Zieldatei>
import os, sys, json, datetime as dt
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
heute = dt.date.today()
bsp = [{"von": heute.isoformat(), "bis": (heute + dt.timedelta(days=30)).isoformat(),
        "text": "Beispiel: Wegen eines Wasserschadens bleibt die Kinderkrippe am Mittwoch geschlossen. Kindergarten und Hort haben normal geöffnet."}]
a = '"dringend": []'; assert h.count(a) == 1
h = h.replace(a, '"dringend": ' + json.dumps(bsp, ensure_ascii=False))
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Wichtiger Hinweis</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
