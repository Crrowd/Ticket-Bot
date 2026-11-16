/* Automatisch erzeugt von build.py */
const CACHE = "kita-202611161422";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(
  caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  const fresh = () => fetch(req).then((res) => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); }
    return res;
  });
  if (req.mode === "navigate") {
    /* Seiten: immer aktuell, Kopie nur als Rückfall ohne Netz */
    e.respondWith(fresh().catch(() => caches.match(req).then((r) => r || caches.match("index.html"))));
  } else {
    /* Bilder, Schriften, CSS, JS: sofort aus dem Speicher, im Hintergrund auffrischen */
    e.respondWith(caches.match(req).then((hit) => { const net = fresh().catch(() => hit); return hit || net; }));
  }
});
