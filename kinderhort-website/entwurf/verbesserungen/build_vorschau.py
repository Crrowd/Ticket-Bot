# Private Vorschau „Verbesserungen“: vorschau.html + verbesserungen.css + umbau.py
#   python3 entwurf/verbesserungen/build_vorschau.py <Zieldatei>
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, H); from umbau import umbau
h = open(os.path.join(W, "vorschau.html"), encoding="utf-8").read()
css = open(os.path.join(H, "verbesserungen.css"), encoding="utf-8").read()
i = h.index("</style>"); h = umbau(h[:i] + "\n" + css + h[i:], "#index:krankmelden")
# in der Vorschau öffnet der Link den Kasten selbst (auf der echten Seite macht das main.js über #krankmelden)
h = h.replace("</body>", "<script>document.addEventListener('click',function(e){var a=e.target.closest('.hero-krank');if(!a)return;var k=document.getElementById('krankmelden');if(!k)return;e.preventDefault();k.open=true;k.scrollIntoView({block:'center'});})</script></body>", 1)
tmp = sys.argv[1] + ".quelle.html"; open(tmp, "w", encoding="utf-8").write(h)
src = open(os.path.join(W, "build_entwurf_seite.py"), encoding="utf-8").read()
src = src.replace('open(os.path.join(W, "vorschau.html"), encoding="utf-8")', 'open(' + repr(tmp) + ', encoding="utf-8")')
src = src.replace('<title>Kinderhort Grombühl Entwurf</title>', '<title>Kinderhort Grombühl Verbesserungen</title>')
exec(compile(src, "build_entwurf_seite.py", "exec"), {"__file__": os.path.join(W, "build_entwurf_seite.py"), "__name__": "__main__"})
os.remove(tmp)
