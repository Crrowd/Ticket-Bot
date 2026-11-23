# Verbesserungen aus dem Stresstest (23.11.2026). Wendet alle Änderungen auf einen Website-Ordner an:
#   python3 entwurf/stresstest/verbessern.py <ordner>
# 1 Semikolon im Text: Daten-Prüfung meldet es und hängt den abgeschnittenen Rest wieder an
# 2 Termine über mehrere Monate: Datumsfeld „27.11.“ / „bis 15.01.27“ statt „27.1 / 1.– / Jan 2027“
# 3 Hover-Effekte nur bei Geräten mit Maus (kein „hängender“ Zustand nach dem Antippen auf dem Handy)
# 4 Knopfbeschriftungen nicht markierbar
# 5 Wichtiger Hinweis: auf dem Handy höchstens drei Zeilen mit „Weiterlesen“, Warnung ab 220 Zeichen
import os, re, sys

Z = sys.argv[1]
def patch(rel, pairs):
    p = os.path.join(Z, rel); s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        if b in s and a not in s: continue          # schon angewendet
        assert s.count(a) == 1, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)

# ---------- 1 und 5: build.py ----------
patch("build.py", [
('''def read_csv(name):
    with open(os.path.join(W, "daten", name), encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter=";") if any((v or "").strip() for v in r.values())]''',
'''def read_csv(name):
    with open(os.path.join(W, "daten", name), encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter=";")
        rows = []
        for n, r in enumerate(rd, start=2):
            rest = r.pop(None, None)
            if rest and any((x or "").strip() for x in rest):
                # ein Semikolon im Text teilt die Zeile: den Rest wieder an die letzte Spalte hängen und melden
                letzte = rd.fieldnames[-1]
                r[letzte] = ";".join([r.get(letzte) or ""] + rest)
                (_melde if "_melde" in globals() else lambda *x: CSV_HINWEISE.append(x))("!", name, n, f"Semikolon im Text der Spalte „{letzte}“ – die Zeile wurde zusammengefügt. Bitte Semikolon im Text durch Komma oder Punkt ersetzen.")
            if any((v or "").strip() for v in r.values() if isinstance(v, str)):
                rows.append(r)
        return rows
CSV_HINWEISE = []'''),
('''def _melde(art, datei, zeile, text): PRUEFUNG.append((art, datei, zeile, text))''',
'''def _melde(art, datei, zeile, text): PRUEFUNG.append((art, datei, zeile, text))
PRUEFUNG.extend(CSV_HINWEISE)'''),
('''DRINGEND = gueltig("dringend.csv", read_csv("dringend.csv"), ["von", "bis"], ["von", "Text"]) if os.path.exists(os.path.join(W, "daten/dringend.csv")) else []''',
'''DRINGEND = gueltig("dringend.csv", read_csv("dringend.csv"), ["von", "bis"], ["von", "Text"]) if os.path.exists(os.path.join(W, "daten/dringend.csv")) else []
for _n, _r in enumerate(DRINGEND, start=2):
    if len(_r["Text"]) > 220:
        _melde("!", "dringend.csv", _n, f"Hinweis ist {len(_r['Text'])} Zeichen lang – auf dem Handy erscheinen nur die ersten drei Zeilen, der Rest hinter „Weiterlesen“. Kürzer ist besser (bis etwa 200 Zeichen).")'''),
# 2 Datumsfeld bei Terminen über mehrere Monate
('''    day = f"{a.day:02d}" if a == b else (f"{a.day:02d}.–{b.day:02d}." if a.month == b.month else f"{a.day:02d}.{a.month:02d}.–")
    mon = f"{MONATE[b.month - 1]} {b.year}"''',
'''    lang = a.month != b.month or a.year != b.year
    day = f"{a.day:02d}" if a == b else (f"{a.day:02d}.–{b.day:02d}." if not lang else f"{a.day:02d}.{a.month:02d}.")
    mon = f"{MONATE[b.month - 1]} {b.year}" if not lang else (f"bis {b:%d.%m.}" if a.year == b.year else f"bis {b:%d.%m.%y}")'''),
('''            f'<div class="date"><b>{day}</b><span>{mon}</span></div>\'''',
'''            f'<div class="date{" lang" if lang else ""}"><b>{day}</b><span>{mon}</span></div>\''''),
])

# ---------- 5: main.js ----------
patch("js/main.js", [
('''    var mainEl = document.querySelector("main"); if (mainEl) mainEl.prepend(dBand);''',
'''    var mainEl = document.querySelector("main"); if (mainEl) mainEl.prepend(dBand);
    /* langer Hinweis: auf schmalen Bildschirmen drei Zeilen, Rest hinter „Weiterlesen“ */
    var dP = $("p", dBand);
    requestAnimationFrame(function () {
      if (dP.scrollHeight <= dP.clientHeight + 2) return;
      var mehr = document.createElement("button"); mehr.type = "button"; mehr.className = "dringend-mehr"; mehr.textContent = "Weiterlesen"; mehr.setAttribute("aria-expanded", "false");
      mehr.addEventListener("click", function () { var auf = dBand.classList.toggle("offen"); mehr.textContent = auf ? "Weniger" : "Weiterlesen"; mehr.setAttribute("aria-expanded", String(auf)); });
      $(".dringend-in", dBand).appendChild(mehr);
    });'''),
])

# ---------- 3: Hover-Regeln nur bei Maus ----------
def hover_nur_mit_maus(css):
    out, stack, i, n = [], [], 0, len(css)
    def oben_teilen(sel):
        teile, tiefe, akt = [], 0, ""
        for ch in sel:
            if ch in "([": tiefe += 1
            elif ch in ")]": tiefe -= 1
            if ch == "," and tiefe == 0: teile.append(akt); akt = ""
            else: akt += ch
        teile.append(akt); return [t.strip() for t in teile if t.strip()]
    gezaehlt = 0
    while i < n:
        if css.startswith("/*", i):
            j = css.index("*/", i) + 2; out.append(css[i:j]); i = j; continue
        j = i
        while j < n and css[j] not in "{};" and not css.startswith("/*", j):
            if css[j] in "\"'":
                q = css[j]; j += 1
                while css[j] != q: j += 1
            j += 1
        if j >= n: out.append(css[i:]); break
        if css.startswith("/*", j): out.append(css[i:j]); i = j; continue
        ch = css[j]
        if ch == ";": out.append(css[i:j + 1]); i = j + 1; continue
        if ch == "}": out.append(css[i:j + 1]); stack and stack.pop(); i = j + 1; continue
        vor = css[i:j]; p = vor.strip()
        if p.startswith("@"):
            out.append(css[i:j + 1]); stack.append(p); i = j + 1; continue
        k, tiefe = j + 1, 1
        while tiefe:
            if css[k] == "{": tiefe += 1
            elif css[k] == "}": tiefe -= 1
            k += 1
        koerper = css[j + 1:k - 1]
        schon = any(s.startswith("@media") and "hover" in s for s in stack) or any(s.startswith("@keyframes") for s in stack)
        if ":hover" in p and not schon:
            sels = oben_teilen(p)
            # :hover nur innerhalb von :is(…, :focus-within) o. Ä. bleibt (Tastatur/Antippen braucht es auch)
            hov = [s for s in sels if ":hover" in re.sub(r":is\([^()]*\)", lambda m: "" if "," in m.group(0) else m.group(0), s)]
            rest = [s for s in sels if s not in hov]
            lead = vor[:len(vor) - len(vor.lstrip())]
            stueck = ""
            if rest: stueck += lead + ", ".join(rest) + " {" + koerper + "}"
            if hov:
                stueck += (" " if rest else lead) + "@media (hover: hover) and (pointer: fine) { " + ", ".join(hov) + " {" + koerper + "} }"
                gezaehlt += 1
            out.append(stueck)
        else:
            out.append(css[i:k])
        i = k
    return "".join(out), gezaehlt

p = os.path.join(Z, "css/style.css"); css = open(p, encoding="utf-8").read()
neu, zahl = hover_nur_mit_maus(css)
assert neu.count("{") == neu.count("}"), "Klammern"
zusatz = '''
/* ===== Stresstest (23.11.2026) ===== */
/* 4 Knopfbeschriftungen beim langen Drücken nicht markieren (Inhalte bleiben kopierbar) */
button, .btn, .round-btn, .copy-btn, .icon-btn, .subnav a, .nav-toggle, [role="tab"] { -webkit-user-select: none; user-select: none; -webkit-touch-callout: none; }
/* 2 Termine über mehrere Monate: „27.11.“ / „bis 15.01.“ */
.event .date.lang b { font-size: 1.15rem; }
.event .date.lang span { font-size: .78rem; line-height: 1.25; display: block; }
/* 5 Langer wichtiger Hinweis: auf dem Handy drei Zeilen, Rest hinter „Weiterlesen“ */
.dringend-mehr { flex: none; align-self: flex-end; min-height: 44px; padding: 0 4px; border: 0; background: none; color: var(--ink); font: 600 .95rem var(--font-body); text-decoration: underline; text-underline-offset: 4px; cursor: pointer; }
@media (max-width: 700px) {
  .dringend-in { flex-wrap: wrap; }
  .dringend:not(.offen) .dringend-in p { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
  .dringend-in p { flex: 1 1 0; min-width: 0; }
  .dringend-mehr { flex-basis: 100%; margin-left: 44px; align-self: flex-start; text-align: left; min-height: 36px; }
}
@media (min-width: 701px) { .dringend-mehr { display: none; } }
/* 3 Rückmeldung beim Antippen statt hängendem Hover */
@media (hover: none) { .btn:active, .round-btn:active, a.quick-card:active, .dl-link:active { opacity: .82; } }
'''
if "Stresstest (23.11.2026)" not in neu: neu += zusatz
open(p, "w", encoding="utf-8").write(neu)
print("Hover-Regeln auf Maus beschränkt:", zahl)
