/* Kath. Kinder- und Jugendhort Grombühl – Interaktionen */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.remove("no-js");
  root.classList.add("js");
  var K = window.KITA || null;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var isMac = /Mac|iPhone|iPad/.test(navigator.platform || "");
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function svg(path, size) {
    return '<svg width="' + (size || 20) + '" height="' + (size || 20) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + "</svg>";
  }
  var ICON = {
    x: '<path d="M6 6l12 12M18 6L6 18"/>', left: '<path d="M15 5l-7 7 7 7"/>', right: '<path d="M9 5l7 7-7 7"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>', search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.8-3.8"/>', phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'
  };
  /* Gummiband: hinter einer Grenze folgt das Element dem Finger mit wachsendem Widerstand */
  function rubber(x, d) { var s = x < 0 ? -1 : 1; x = Math.abs(x); return s * (1 - 1 / (x * 0.55 / d + 1)) * d; }
  var CSSV = getComputedStyle(document.documentElement);
  var EASE_IO = CSSV.getPropertyValue("--ease-in-out").trim() || "cubic-bezier(.65, 0, .35, 1)",
      EASE_OUT = CSSV.getPropertyValue("--ease-out").trim() || "cubic-bezier(.23, 1, .32, 1)";
  /* Zustand in der Adresse (teilen, neu laden, zurück) */
  function getParam(k) { try { return new URLSearchParams(location.search).get(k); } catch (e) { return null; } }
  function setParam(k, v) { try { var u = new URL(location.href); if (v) u.searchParams.set(k, v); else u.searchParams.delete(k); history.replaceState(history.state, "", u); } catch (e) { /* file:// */ } }
  /* Text sicher in HTML einsetzen */
  function escH(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  /* nur eigene Seiten als Link zulassen (z. B. „kontakt.html#frag“) */
  function safeHref(u) { return /^(?:[a-z0-9-]+\.html)?(?:#[\w:-]*)?$/i.test(u || "") && u ? u : "index.html"; }
  function store(key, val) {
    try { if (val === undefined) return localStorage.getItem(key); if (val === null) localStorage.removeItem(key); else localStorage.setItem(key, val); } catch (e) { /* privates Fenster */ }
    return null;
  }

  /* ---------- Überlagerungen: „Zurück“ schließt Bildansicht, Suche und Menü ---------- */
  var closeTop = null;
  function overlayOpened(closeFn) { closeTop = closeFn; try { history.pushState({ overlay: true }, ""); } catch (e) { /* file:// */ } }
  function overlayClosed() {
    if (!closeTop) return;
    closeTop = null;
    if (history.state && history.state.overlay) history.back();
  }
  window.addEventListener("popstate", function () {
    if (closeTop) { var f = closeTop; closeTop = null; f(); }
  });

  /* ---------- Kopfbereich ---------- */
  var header = $(".site-header");
  /* Leiste blendet sich beim Runterscrollen aus und kommt beim Hochscrollen zurück */
  var lastY = window.scrollY, travel = 0;
  function busy() {
    return document.body.classList.contains("nav-open") || $(".has-drop.open") || $(".search-panel[open]") ||
      (header && header.matches(":focus-within, :hover")) || ($(".lightbox") && $(".lightbox").classList.contains("open"));
  }
  /* Kopfleiste ein-/ausblenden. Klebende Leisten springen an ihre neue Stelle und gleiten per translate hin
     (läuft auf der Grafikkarte, statt „top“ zu animieren) */
  function kopf(weg) {
    if (!header || header.classList.contains("hide") === weg) return;
    var mit = $$(".subnav, .sticky-title").filter(function (el) { return el.getClientRects().length; }).map(function (el) { return [el, el.getBoundingClientRect().top]; });
    header.classList.toggle("hide", weg);
    document.dispatchEvent(new Event("kopfwechsel"));
    if (reduced) return;
    mit.forEach(function (p) {
      var d = p[1] - p[0].getBoundingClientRect().top;
      /* im selben Takt wie die Kopfleiste selbst, sonst schiebt sich die Leiste unter die noch sichtbare Kopfleiste */
      if (Math.abs(d) > 1 && Math.abs(d) < 200) p[0].animate([{ translate: "0 " + d + "px" }, { translate: "0 0" }], { duration: 500, easing: CSSV.getPropertyValue(weg ? "--ease-kopf-weg" : "--ease-kopf-da").trim(), composite: "add" });
    });
  }
  function onScroll() {
    if (!header) return;
    var y = window.scrollY, dy = y - lastY;
    lastY = y;
    header.classList.toggle("scrolled", y > 8);
    if (y < 120 || busy()) { kopf(false); travel = 0; return; }
    /* erst nach ein paar Pixeln in dieselbe Richtung reagieren – kein Flackern bei kleinen Bewegungen */
    travel = (travel > 0) === (dy > 0) ? travel + dy : dy;
    if (travel > 32) kopf(true);
    else if (travel < -16) kopf(false);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (header) header.addEventListener("focusin", function () { kopf(false); });

  /* Handy-Tastatur: Höhe messen, damit nichts unter ihr verschwindet */
  var vv = window.visualViewport, lastKb = -1, lastVvh = -1;
  function onViewport() {
    var kb = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop)), h = Math.round(vv.height);
    if (kb !== lastKb) { lastKb = kb; root.style.setProperty("--kb", kb + "px"); root.classList.toggle("kb-open", kb > 80); }
    if (h !== lastVvh) { lastVvh = h; root.style.setProperty("--vvh", h + "px"); }
  }
  if (vv) { vv.addEventListener("resize", onViewport); vv.addEventListener("scroll", onViewport); onViewport(); }
  /* Eingabefeld beim Antippen in den sichtbaren Bereich holen */
  document.addEventListener("focusin", function (e) {
    if (!/INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || window.innerWidth > 700) return;
    setTimeout(function () { e.target.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" }); }, 300);
  });

  var toggle = $(".nav-toggle");
  function setMenu(open) {
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = !document.body.classList.contains("nav-open");
      setMenu(open);
      if (open) overlayOpened(function () { setMenu(false); }); else overlayClosed();
    });
    $$(".main-nav a").forEach(function (a) {
      a.addEventListener("click", function () { if (document.body.classList.contains("nav-open")) { setMenu(false); closeTop = null; } });
    });
  }
  /* Höhe weich ändern (Klappen, Ein- und Ausblenden); danach wieder frei */
  function hoehe(el, von, bis, ms, ease, fertig) {
    if (el._hoehe) { el._hoehe.onfinish = null; el._hoehe.cancel(); }
    el.style.overflow = "hidden";
    var a = el.animate([{ height: von + "px" }, { height: bis + "px" }], { duration: ms, easing: ease });
    el._hoehe = a;
    a.onfinish = function () { el._hoehe = null; el.style.overflow = ""; if (fertig) fertig(); };
    return a;
  }
  var EIO_ = "cubic-bezier(.77,0,.175,1)";
  $$(".has-drop").forEach(function (li) {
    var btn = $(".drop-toggle", li), mega = $(".mega", li);
    function origin() {
      if (!mega || !mega.offsetParent) return;
      var b = btn.getBoundingClientRect(), p = mega.offsetParent.getBoundingClientRect();
      mega.style.setProperty("--origin", Math.round(b.left + b.width / 2 - p.left) + "px");
    }
    li.addEventListener("mouseenter", origin);
    li.addEventListener("focusin", origin);
    btn.addEventListener("click", function (e) {
      origin();
      e.stopPropagation();
      var handy = document.body.classList.contains("nav-open") && mega && !reduced;
      if (handy && li.classList.contains("open")) {
        /* zuklappen: erst weich zusammen, dann zu */
        btn.setAttribute("aria-expanded", "false");
        mega.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 160, fill: "forwards" });
        hoehe(mega, mega.offsetHeight, 0, 240, EIO_, function () { li.classList.remove("open"); mega.getAnimations().forEach(function (a) { a.cancel(); }); });
        return;
      }
      var open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if (handy && open) {
        hoehe(mega, 0, mega.offsetHeight, 280, EIO_);
        $$(".mega li a, a.mega-title", mega).forEach(function (a, i) { a.animate([{ opacity: 0, translate: "0 6px" }, { opacity: 1, translate: "0 0" }], { duration: 220, delay: 80 + i * 30, easing: EASE_OUT, fill: "backwards" }); });
      }
    });
  });
  document.addEventListener("click", function () {
    $$(".has-drop.open").forEach(function (li) {
      if (document.body.classList.contains("nav-open")) return;
      li.classList.remove("open");
      $(".drop-toggle", li).setAttribute("aria-expanded", "false");
    });
  });

  /* Bereiche-Menü (Computer): nach Klick auf einen Eintrag schließen, auch wenn die Maus noch darüber ist */
  $$(".has-drop").forEach(function (li) {
    $$(".mega a", li).forEach(function (a) {
      a.addEventListener("click", function () {
        if (document.body.classList.contains("nav-open")) return;
        li.classList.remove("open"); li.classList.add("zu");
        $(".drop-toggle", li).setAttribute("aria-expanded", "false");
        a.blur();
      });
    });
    $(".drop-toggle", li).addEventListener("mouseenter", function () { li.classList.remove("zu"); });
    $(".drop-toggle", li).addEventListener("click", function () { li.classList.remove("zu"); });
  });

  /* ---------- Sprungmarken: aktuellen Abschnitt hervorheben ---------- */
  /* Ein Marker für alle Einträge, der von Punkt zu Punkt gleitet */
  function knobTo(ul, a) {
    var k = $(".subnav-knob", ul), first = !k;
    if (first) { k = document.createElement("li"); k.className = "subnav-knob"; k.setAttribute("aria-hidden", "true"); ul.insertBefore(k, ul.firstChild); }
    if (first) k.style.transition = "none";
    k.style.setProperty("--sw", ul.scrollWidth + "px");
    k.style.setProperty("--kx", a.offsetLeft + "px");
    k.style.setProperty("--ky", a.offsetTop + "px");
    k.style.setProperty("--kw", a.offsetWidth + "px");
    k.style.setProperty("--kh", a.offsetHeight + "px");
    if (first) { void k.offsetWidth; k.style.transition = ""; k.classList.add("on"); }
  }
  window.addEventListener("resize", function () {
    $$(".subnav ul").forEach(function (ul) { var a = $('a[aria-current="true"]', ul), k = $(".subnav-knob", ul); if (a && k) { k.style.transition = "none"; knobTo(ul, a); void k.offsetWidth; k.style.transition = ""; } });
  });
  var subLinks = $$(".subnav a");
  if (subLinks.length) {
    /* Ein Punkt wird erst aktiv, wenn seine Überschrift oben unter der Leiste angekommen ist */
    var pairs = [];
    subLinks.forEach(function (a) {
      var id = a.getAttribute("href").split("#").pop().split(":").pop();
      var sec = (a.closest(".spa-page") || document).querySelector('[id="' + id + '"]');
      if (sec) pairs.push({ sec: sec, a: a, mark: sec.querySelector("h1, h2, .eyebrow, .kicker") || sec });
    });
    var aktiv = null, spyQ = false;
    function setze(a) {
      if (a === aktiv) return; aktiv = a; var ul = a.closest("ul");
      $$("a", ul).forEach(function (l) { l.removeAttribute("aria-current"); });
      a.setAttribute("aria-current", "true");
      knobTo(ul, a);
      /* nur verschieben, wenn der aktive Eintrag nicht ganz zu sehen ist – dann mittig */
      if (a.offsetLeft < ul.scrollLeft || a.offsetLeft + a.offsetWidth > ul.scrollLeft + ul.clientWidth)
        ul.scrollTo({ left: a.offsetLeft - (ul.clientWidth - a.offsetWidth) / 2, behavior: reduced ? "auto" : "smooth" });
    }
    function spy() {
      spyQ = false;
      var sicht = pairs.filter(function (p) { return p.sec.getClientRects().length > 0; });
      if (!sicht.length) return;
      var nav = sicht[0].a.closest(".subnav"), unten = nav ? nav.getBoundingClientRect().bottom : 120;
      var grenze = Math.max(unten, 0) + 32, wahl = null;
      sicht.forEach(function (p) { if (p.mark.getBoundingClientRect().top <= grenze) wahl = p; });
      /* nach einem Klick in der Leiste bleibt der gewählte Punkt, bis man ein Stück weiterscrollt */
      if (halt) { if (Math.abs(scrollY - halt.y) < 160) { setze(halt.a); return; } halt = null; }
      /* ganz unten angekommen: der letzte sichtbare Abschnitt zählt, auch wenn er nicht bis oben reicht */
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) {
        var last = sicht[sicht.length - 1]; if (last.mark.getBoundingClientRect().top < innerHeight) wahl = last;
      }
      if (wahl) setze(wahl.a);
    }
    /* Nach Klick: Balken sofort auf den gewählten Punkt, bis das Scrollen zur Ruhe kommt */
    var gesperrt = false, sperrT = 0, halt = null, geklickt = null;
    function frei() { clearTimeout(sperrT); sperrT = setTimeout(function () { gesperrt = false; halt = { a: geklickt, y: scrollY }; }, 180); }
    function plane() { if (gesperrt) { frei(); return; } if (!spyQ) { spyQ = true; requestAnimationFrame(spy); } }
    addEventListener("scroll", plane, { passive: true }); addEventListener("resize", plane);
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest(".subnav a"); if (!a) return;
      setze(a); geklickt = a; halt = null; gesperrt = true; frei();
    });
    spy();
  }

  /* ---------- Kurzmeldungen ---------- */
  var toasts = document.createElement("div");
  toasts.className = "toasts";
  toasts.setAttribute("role", "status");
  toasts.setAttribute("aria-live", "polite");
  document.body.appendChild(toasts);
  function toast(text, undoLabel, undo) {
    var t = document.createElement("div");
    t.className = "toast";
    t.innerHTML = '<span class="toast-ok">' + svg(ICON.check, 18) + "</span><span></span>";
    t.querySelector("span:not(.toast-ok)").textContent = text;
    function leave() { t.classList.add("leaving"); setTimeout(function () { t.remove(); }, 200); }
    if (undo) {
      var b = document.createElement("button");
      b.type = "button"; b.textContent = undoLabel;
      b.addEventListener("click", function () { undo(); leave(); });
      t.appendChild(b);
    }
    while (toasts.children.length > 1) toasts.firstChild.remove();
    toasts.appendChild(t);
    setTimeout(leave, undo ? 7000 : 2600);
  }

  /* ---------- Kopieren mit sofortiger Rückmeldung ---------- */
  $$(".copy-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-copy"), label = b.getAttribute("data-label");
      /* Rückmeldung sofort zeigen, nicht erst auf die Zwischenablage warten */
      b.classList.add("done");
      setTimeout(function () { b.classList.remove("done"); }, 1200);
      var ok = function () { toast(label + " kopiert"); };
      var fail = function () { toast(label + ": " + text); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fail); else fail();
    });
  });

  /* ---------- Rundgang: Pfeile und Zähler ---------- */
  $$(".tour").forEach(function (tour) {
    var track = $(".tour-track", tour), items = $$(".tour-item", track), count = $(".count", tour);
    function step() { return items.length > 1 ? items[1].offsetLeft - items[0].offsetLeft : track.clientWidth; }
    /* Ist das erste bzw. letzte Bild schon ganz zu sehen? */
    function atEdge(item, side) {
      var t = track.getBoundingClientRect(), r = item.getBoundingClientRect();
      return side < 0 ? r.left >= t.left - 2 : r.right <= t.right + 2;
    }
    function bounds(dir) {
      if (reduced || !track.animate) return;
      track.animate([{ translate: "0 0" }, { translate: (dir * 18) + "px 0" }, { translate: "0 0" }], { duration: 240, easing: EASE_OUT });
    }
    $(".tour-prev", tour).addEventListener("click", function () {
      if (atEdge(items[0], -1)) bounds(1); else track.scrollBy({ left: -step(), behavior: "smooth" });
    });
    $(".tour-next", tour).addEventListener("click", function () {
      if (atEdge(items[items.length - 1], 1)) bounds(-1); else track.scrollBy({ left: step(), behavior: "smooth" });
    });
    function update() {
      if (!count) return;
      var s = step(), i = s > 0 ? Math.round(track.scrollLeft / s) + 1 : 1;
      count.textContent = "Bild " + Math.min(i, items.length) + " von " + items.length;
    }
    track.addEventListener("scroll", update, { passive: true });
    update();
  });

  /* ---------- Bildansicht ---------- */
  var lb = document.createElement("div");
  lb.className = "lightbox";
  lb.setAttribute("role", "dialog");
  lb.setAttribute("aria-modal", "true");
  lb.setAttribute("aria-label", "Bildansicht");
  lb.innerHTML =
    '<span class="lb-count"></span>' +
    '<button type="button" class="lb-btn lb-close" aria-label="Schließen">' + svg(ICON.x, 22) + "</button>" +
    '<button type="button" class="lb-btn lb-prev" aria-label="Vorheriges Bild">' + svg(ICON.left, 22) + "</button>" +
    '<button type="button" class="lb-btn lb-next" aria-label="Nächstes Bild">' + svg(ICON.right, 22) + "</button>" +
    '<figure><img alt=""><figcaption><strong></strong><span></span></figcaption></figure>' +
    '<div class="lb-hints" aria-hidden="true"><span><kbd>←</kbd> <kbd>→</kbd> blättern</span><span><kbd>Esc</kbd> schließen</span></div>';
  document.body.appendChild(lb);
  var lbFig = $("figure", lb), lbImg = $("img", lb), lbTitle = $("figcaption strong", lb), lbText = $("figcaption span", lb), lbCount = $(".lb-count", lb);
  var group = [], idx = 0, lastFocus = null, flight = null;
  function thumbOf(el) { return el ? (el.querySelector("img") || el) : null; }
  function setSrc(el) {
    /* Sofort das schon geladene Vorschaubild zeigen, das große Bild still nachladen und tauschen */
    var full = el.getAttribute("data-full"), th = el.querySelector("img"), quick = th && th.complete && th.naturalWidth ? (th.currentSrc || th.src) : null;
    lbImg.onload = null;
    if (quick) {
      lbImg.src = quick; lbFig.classList.remove("loading");
      lbImg.style.transition = "none"; lbImg.classList.add("ready"); void lbImg.offsetWidth; lbImg.style.transition = "";
      var hi = new Image();
      hi.onload = function () { if (group[idx] === el) lbImg.src = full; };
      hi.src = full;
    } else {
      lbImg.classList.remove("ready"); lbFig.classList.add("loading");
      lbImg.onload = function () { lbImg.classList.add("ready"); lbFig.classList.remove("loading"); };
      lbImg.src = full;
      if (lbImg.complete && lbImg.naturalWidth) lbImg.onload();
    }
  }
  /* Doppeltipp-Zoom: genau die angetippte Stelle vergrößern, dann verschieben */
  var zoom = { on: false, s: 2.5, tx: 0, ty: 0 }, lastTap = 0, pan = null;
  function zoomApply() { lbImg.style.scale = zoom.on ? zoom.s : ""; lbImg.style.translate = zoom.on ? zoom.tx + "px " + zoom.ty + "px" : ""; lb.classList.toggle("zoomed", zoom.on); }
  function zoomClamp() { var w = lbImg.offsetWidth, h = lbImg.offsetHeight, mx = (zoom.s - 1) * w / 2, my = (zoom.s - 1) * h / 2; zoom.tx = Math.max(-mx, Math.min(mx, zoom.tx)); zoom.ty = Math.max(-my, Math.min(my, zoom.ty)); }
  function zoomReset() { if (!zoom.on) return; zoom.on = false; lb.classList.add("unzoom"); zoomApply(); setTimeout(function () { lb.classList.remove("unzoom"); }, 320); }
  function zoomToggle(x, y) {
    if (zoom.on) { zoomReset(); return; }
    var r = lbImg.getBoundingClientRect(), px = x - (r.left + r.width / 2), py = y - (r.top + r.height / 2);
    zoom.on = true; zoom.tx = -px * (zoom.s - 1); zoom.ty = -py * (zoom.s - 1); zoomClamp(); zoomApply();
  }
  lbImg.addEventListener("dblclick", function (e) { e.preventDefault(); zoomToggle(e.clientX, e.clientY); });
  lbImg.addEventListener("mousedown", function (e) { if (!zoom.on) return; e.preventDefault(); pan = { x: e.clientX, y: e.clientY, tx: zoom.tx, ty: zoom.ty }; lb.classList.add("panning"); });
  addEventListener("mousemove", function (e) { if (!pan) return; zoom.tx = pan.tx + e.clientX - pan.x; zoom.ty = pan.ty + e.clientY - pan.y; zoomClamp(); zoomApply(); });
  addEventListener("mouseup", function () { if (pan) { pan = null; lb.classList.remove("panning"); } });
  function show(i, dir, taste) {
    zoomReset();
    var prev = lbImg.classList.contains("ready") && lb.classList.contains("open") ? lbImg.getBoundingClientRect() : null;
    if (prev && !reduced && !taste) {
      /* Altes und neues Bild überlappen: das alte blendet aus, während das neue einblendet */
      var g = lbImg.cloneNode();
      g.className = "lb-ghost";
      g.style.cssText = "left:" + prev.left + "px;top:" + prev.top + "px;width:" + prev.width + "px;height:" + prev.height + "px";
      lb.appendChild(g);
      g.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateX(" + (dir || 0) * -24 + "px)" }], { duration: 200, easing: EASE_OUT, fill: "forwards" }).onfinish = function () { g.remove(); };
    }
    idx = (i + group.length) % group.length;
    var el = group[idx];
    setSrc(el);
    /* per Pfeiltaste: sofort wechseln, nur kurz überblenden – wer schnell blättert, soll nicht warten */
    if (prev && dir && !reduced) lbImg.animate(taste ? [{ opacity: .35 }, { opacity: 1 }] : [{ opacity: 0, transform: "translateX(" + dir * 24 + "px)" }, { opacity: 1, transform: "none" }], { duration: taste ? 120 : 250, easing: EASE_OUT });
    lbImg.alt = el.getAttribute("data-title") || "";
    lbTitle.textContent = el.getAttribute("data-title") || "";
    lbText.textContent = el.getAttribute("data-text") || "";
    lbCount.textContent = group.length > 1 ? (idx + 1) + " / " + group.length : "";
    $(".lb-prev", lb).hidden = $(".lb-next", lb).hidden = group.length < 2;
    if (group.length > 1) { var pre = new Image(); pre.src = group[(idx + 1) % group.length].getAttribute("data-full"); }
  }
  /* FLIP: Position und Ausschnitt der Vorschau berechnen und das große Bild von dort aus- bzw. dorthin zurückfliegen lassen */
  function flip(el, back) {
    var th = thumbOf(el);
    if (!th || reduced || !lbImg.animate) return null;
    var t = th.getBoundingClientRect(), f = lbImg.getBoundingClientRect();
    if (!t.width || !f.width || t.bottom < 0 || t.top > innerHeight || t.right < 0 || t.left > innerWidth) return null;
    var s = Math.max(t.width / f.width, t.height / f.height);
    var dx = t.left + t.width / 2 - (f.left + f.width / 2), dy = t.top + t.height / 2 - (f.top + f.height / 2);
    var ix = Math.max(0, (f.width - t.width / s) / 2), iy = Math.max(0, (f.height - t.height / s) / 2), r = 18 / s;
    var small = { transform: "translate(" + dx + "px," + dy + "px) scale(" + s + ")", clipPath: "inset(" + iy + "px " + ix + "px round " + r + "px)" };
    var big = { transform: "none", clipPath: "inset(0px 0px round 12px)" };
    return lbImg.animate(back ? [big, small] : [small, big], { duration: back ? 300 : 380, easing: EASE_IO, fill: back ? "forwards" : "backwards" });
  }
  function fadePop(back) {
    if (reduced || !lbImg.animate) return null;
    var a = { opacity: 0, transform: "scale(.95)" }, b = { opacity: 1, transform: "none" };
    return lbImg.animate(back ? [b, a] : [a, b], { duration: back ? 200 : 250, easing: EASE_OUT, fill: back ? "forwards" : "none" });
  }
  function hideLb() {
    var el = group[idx];
    zoom.on = false; zoomApply();
    if (flight) flight.cancel();
    /* Zurück in die Vorschau: falls sie in der Reihe verborgen ist, erst dorthin scrollen */
    if (el && el.closest(".tour-track")) el.scrollIntoView({ block: "nearest", inline: "nearest" });
    var anim = flip(el, true) || fadePop(true);
    lb.classList.remove("open");
    document.body.style.overflow = "";
    lbFig.style.removeProperty("--drag"); lbFig.style.removeProperty("--dx");
    /* Nach der Landung unsichtbar machen und erst dann zurücksetzen – kein Aufblitzen */
    if (anim) anim.onfinish = function () { lbImg.style.transition = "none"; lbImg.classList.remove("ready"); anim.cancel(); requestAnimationFrame(function () { lbImg.style.transition = ""; }); };
    else lbImg.classList.remove("ready");
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }
  function closeLb() { hideLb(); overlayClosed(); }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-full]");
    if (!el) return;
    e.preventDefault();
    group = $$('[data-full][data-group="' + el.getAttribute("data-group") + '"]').filter(function (x) { return !x.closest("[hidden]"); });
    lastFocus = el;
    lbImg.getAnimations && lbImg.getAnimations().forEach(function (a) { a.cancel(); });
    show(group.indexOf(el));
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
    flight = flip(el, false) || fadePop(false);
    $(".lb-close", lb).focus({ preventScroll: true });
    overlayOpened(hideLb);
  });
  $(".lb-close", lb).addEventListener("click", closeLb);
  $(".lb-prev", lb).addEventListener("click", function () { show(idx - 1, -1); });
  $(".lb-next", lb).addEventListener("click", function () { show(idx + 1, 1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener("keydown", function (e) {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") { if (zoom.on) { zoomReset(); return; } closeLb(); }
    if (e.key === "ArrowLeft") show(idx - 1, -1, true);
    if (e.key === "ArrowRight") show(idx + 1, 1, true);
  });
  /* Wischen: Das Bild folgt dem Finger 1:1, ohne Übergang. Nach oben und bei nur einem Bild seitlich: Gummiband */
  var t0 = null;
  lb.addEventListener("touchstart", function (e) {
    t0 = { x: e.touches[0].clientX, y: e.touches[0].clientY, axis: null, t: Date.now(), tx: zoom.tx, ty: zoom.ty, multi: e.touches.length > 1 };
    lbFig.style.transition = "none"; if (zoom.on) lb.classList.add("panning");
  }, { passive: true });
  lb.addEventListener("touchmove", function (e) {
    if (!t0) return;
    if (zoom.on) { zoom.tx = t0.tx + e.touches[0].clientX - t0.x; zoom.ty = t0.ty + e.touches[0].clientY - t0.y; zoomClamp(); zoomApply(); return; }
    var dy = e.touches[0].clientY - t0.y, dx = e.touches[0].clientX - t0.x;
    if (!t0.axis && Math.abs(dx) + Math.abs(dy) > 8) t0.axis = Math.abs(dx) > Math.abs(dy) ? "x" : "y";
    if (t0.axis === "y") lbFig.style.setProperty("--drag", (dy > 0 ? dy : rubber(dy, 60)) + "px");
    if (t0.axis === "x") lbFig.style.setProperty("--dx", (group.length > 1 ? dx : rubber(dx, 60)) + "px");
  }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (!t0) return;
    var dx = e.changedTouches[0].clientX - t0.x, dy = e.changedTouches[0].clientY - t0.y, axis = t0.axis;
    lb.classList.remove("panning");
    /* kurzer Tipp ohne Bewegung: zweimal kurz hintereinander = Zoom */
    if (Math.abs(dx) < 10 && Math.abs(dy) < 10 && Date.now() - t0.t < 250 && e.target === lbImg) {
      if (Date.now() - lastTap < 320) { zoomToggle(e.changedTouches[0].clientX, e.changedTouches[0].clientY); lastTap = 0; } else lastTap = Date.now();
      t0 = null; lbFig.style.removeProperty("--drag"); lbFig.style.removeProperty("--dx"); return;
    }
    if (zoom.on) { t0 = null; return; }
    lbFig.style.transition = "translate .3s " + EASE_OUT;
    lbFig.style.removeProperty("--drag"); lbFig.style.removeProperty("--dx");
    if (axis === "y" && dy > 110) closeLb();
    else if (axis === "x" && Math.abs(dx) > 50 && group.length > 1) show(idx + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
    t0 = null;
  });

  /* ---------- Zuletzt angesehen (nur im eigenen Browser) ---------- */
  function recentList() { try { var l = JSON.parse(store("zuletzt") || "[]"); return Array.isArray(l) ? l.filter(function (r) { return r && typeof r.t === "string" && typeof r.u === "string" && safeHref(r.u) === r.u; }) : []; } catch (e) { return []; } }
  function remember(t, sub, u) {
    if (!t || !u) return;
    var l = recentList().filter(function (r) { return r.u !== u; });
    l.unshift({ t: t, s: sub || "", u: u }); store("zuletzt", JSON.stringify(l.slice(0, 6)));
  }
  (function () {
    var page = location.pathname.split("/").pop() || "index.html", h1 = $("main h1");
    if (page === "404.html" || !h1 || $('meta[name="robots"][content*="noindex"]') || safeHref(page) !== page) return;
    var names = { "index.html": "Startseite", "aktuelles.html": "Aktuelles", "downloads.html": "Downloads", "kontakt.html": "Kontakt" };
    remember(names[page] || h1.textContent.replace(/\s+/g, " ").trim(), "Seite", page);
  })();

  /* ---------- Schnellsuche (Strg+K) ---------- */
  var searchBtns = $$(".js-search");
  if (K && K.suche && window.HTMLDialogElement) {
    $$(".search-btn kbd").forEach(function (k) { k.textContent = isMac ? "⌘ K" : "Strg K"; });
    var dlg = document.createElement("dialog");
    dlg.className = "search-panel";
    dlg.setAttribute("aria-label", "Suche");
    dlg.innerHTML =
      '<span class="search-grip" aria-hidden="true"></span>' +
      '<div class="search-head">' + svg(ICON.search, 20) +
      '<input type="text" id="suche" spellcheck="false" role="combobox" aria-expanded="true" aria-haspopup="listbox" aria-autocomplete="list" aria-controls="suchliste" aria-label="Suchbegriff" name="suche" placeholder="Wonach suchen Sie? z. B. Ferien, krank, Telefon …" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search">' +
      "<kbd>Esc</kbd></div>" +
      '<ul class="search-list" id="suchliste" role="listbox" aria-label="Treffer"></ul>' +
      '<div class="search-foot" aria-hidden="true"><span><kbd>↑</kbd><kbd>↓</kbd> auswählen</span><span><kbd>↵</kbd> öffnen</span><span><kbd>Esc</kbd> schließen</span></div>';
    document.body.appendChild(dlg);
    var input = $("input", dlg), list = $(".search-list", dlg), sel = 0, hits = [];
    /* großzügig bei der Eingabe: Groß/Klein, Umlaute, ß und kleine Tippfehler spielen keine Rolle */
    var norm = function (s) { return s.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9 ]+/g, " "); };
    var near = function (a, b) {
      if (Math.abs(a.length - b.length) > 1) return false;
      var i = 0, j = 0, miss = 0;
      if (a.length === b.length) {   /* Buchstabendreher: „Ferein“ → „Ferien“ */
        for (var k = 0; k < a.length - 1; k++) {
          if (a[k] !== b[k]) return a[k] === b[k + 1] && a[k + 1] === b[k] && a.slice(k + 2) === b.slice(k + 2) || a.slice(k + 1) === b.slice(k + 1);
        }
        return true;
      }
      while (i < a.length && j < b.length) {
        if (a[i] === b[j]) { i++; j++; continue; }
        if (++miss > 1) return false;
        if (a.length > b.length) i++; else if (b.length > a.length) j++; else { i++; j++; }
      }
      return true;
    };
    var index = K.suche.map(function (it) {
      var t = norm(it.t), all = norm(it.t + " " + it.s + " " + it.k);
      return { it: it, t: t, all: all, words: all.split(" ") };
    });
    var search = function (q) {
      var tokens = norm(q).split(" ").filter(Boolean);
      if (!tokens.length) {
        /* ohne Eingabe: zuerst die zuletzt angesehenen Seiten, dann die am häufigsten gebrauchten Wege */
        var here = location.pathname.split("/").pop() || "index.html";
        var zuletzt = recentList().filter(function (r) { return r.u !== here; }).slice(0, 3).map(function (r) { return { t: r.t, s: r.s, u: r.u, recent: true }; });
        var oft = ["Kind krankmelden", "Kontakt & Durchwahlen", "Aktuelle Termine", "Schließtage", "Platz anfragen", "Downloads"];
        var basis = oft.map(function (t) { return index.filter(function (e) { return e.it.t === t && !/^Kinder/.test(e.it.s); })[0]; }).filter(Boolean).map(function (e) { return e.it; });
        return zuletzt.concat(basis.filter(function (b) { return !zuletzt.some(function (z) { return z.u === b.u; }); })).slice(0, 8);
      }
      return index.map(function (e) {
        var score = 0;
        for (var n = 0; n < tokens.length; n++) {
          var tk = tokens[n];
          if (e.t.indexOf(tk) >= 0) score += 3;
          else if (e.all.indexOf(tk) >= 0) score += 2;
          else if (tk.length >= 4 && e.t.split(" ").some(function (w) { return near(w.slice(0, tk.length), tk) || near(w, tk); })) score += 1.5;
          else if (tk.length >= 4 && e.words.some(function (w) { return near(w.slice(0, tk.length + 1), tk) || near(w, tk); })) score += 1;
          else return null;
        }
        return { it: e.it, score: score };
      }).filter(Boolean).sort(function (a, b) { return b.score - a.score; }).slice(0, 8).map(function (r) { return r.it; });
    };
    /* „Meinten Sie …?“: Wörter, die so nirgends vorkommen, gegen den Wortschatz der Suche prüfen */
    var abst = function (a, b) {
      var prev = [], cur, i, j; for (j = 0; j <= b.length; j++) prev[j] = j;
      for (i = 1; i <= a.length; i++) { cur = [i]; for (j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1) - (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1] ? 1 : 0)); prev = cur; }
      return prev[b.length];
    };
    var wortschatz = {};
    K.suche.forEach(function (it) { (it.t + " " + it.k).split(/[\s,&·–-]+/).forEach(function (w) { var n = norm(w).trim(); if (n.length >= 4 && n.indexOf(" ") < 0 && !wortschatz[n]) wortschatz[n] = w.replace(/[^\wäöüÄÖÜß-]/g, ""); }); });
    var korr = function (q) {
      var ws = norm(q).split(" ").filter(Boolean), out = [], neu = false;
      ws.forEach(function (w) {
        if (w.length < 4 || index.some(function (e) { return e.all.indexOf(w) >= 0; })) { out.push(w); return; }
        var best = null, bd = w.length >= 8 ? 3 : 2;
        Object.keys(wortschatz).forEach(function (k) { var d = Math.min(abst(w, k), k.length > w.length ? abst(w, k.slice(0, w.length)) + .5 : 99); if (d < bd || (d === bd && best && k.length < best.length)) { bd = d; best = k; } });
        if (best && bd <= (w.length >= 8 ? 2.5 : 1.5)) { var vw = wortschatz[best]; out.push(vw.charAt(0).toUpperCase() + vw.slice(1)); neu = true; } else out.push(w);
      });
      return neu ? out.join(" ") : null;
    };
    var meant = null;
    var bindMeant = function () { var b = $(".sr-meant button", list); if (b) b.addEventListener("click", function () { input.value = b.textContent; render(); input.focus(); }); };
    var render = function () {
      hits = search(input.value);
      meant = input.value.trim() ? korr(input.value) : null;
      var meantLi = meant ? '<li role="presentation" class="sr-meant"><p>Meinten Sie: <button type="button">' + escH(meant) + "</button>?</p></li>" : "";
      sel = 0;
      input.setAttribute("aria-expanded", hits.length ? "true" : "false");
      if (hits.length) input.setAttribute("aria-activedescendant", "treffer-0"); else input.removeAttribute("aria-activedescendant");
      if (!hits.length) { list.innerHTML = meantLi + '<li><p class="search-empty">Nichts gefunden. Versuchen Sie einen anderen Begriff – oder rufen Sie uns an: 0931 2789892 0.</p></li>'; bindMeant(); return; }
      list.innerHTML = hits.map(function (h, i) {
        return '<li role="presentation"><a role="option" id="treffer-' + i + '" href="' + escH(h.u) + '" aria-selected="' + (i === 0) + '"><span></span><small></small></a></li>';
      }).join("");
      $$("li", list).forEach(function (li, i) { li.style.setProperty("--n", i); });
      $$("a", list).forEach(function (a, i) {
        $("span", a).textContent = hits[i].t; $("small", a).textContent = hits[i].s;
        if (hits[i].recent) { var tg = document.createElement("span"); tg.className = "recent-tag"; tg.textContent = "Zuletzt"; $("span", a).prepend(tg); }
        a.addEventListener("click", function () { remember(hits[i].t, hits[i].s, hits[i].u); });
      });
      if (meantLi) { list.insertAdjacentHTML("afterbegin", meantLi); bindMeant(); }
    };
    var mark = function (n) {
      var as = $$("a", list);
      if (!as.length) return;
      sel = (n + as.length) % as.length;
      as.forEach(function (a, i) { a.setAttribute("aria-selected", i === sel); });
      as[sel].scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", "treffer-" + sel);
    };
    var openSearch = function (ev, perTaste) {
      if (dlg.open) return;
      /* per Tastenkürzel ohne Einblenden: sofort tippen können */
      dlg.classList.toggle("sofort", !!perTaste);
      if (perTaste) requestAnimationFrame(function () { requestAnimationFrame(function () { dlg.classList.remove("sofort"); }); });
      if (document.body.classList.contains("nav-open")) { setMenu(false); closeTop = null; }
      /* Das Suchfenster wächst aus dem Knopf, der es geöffnet hat */
      var src = ev && ev.currentTarget && ev.currentTarget.getBoundingClientRect ? ev.currentTarget : $(".search-btn");
      if (innerWidth > 700 && src) {
        var r = src.getBoundingClientRect(), w = Math.min(620, innerWidth - 32), left = (innerWidth - w) / 2, top = innerHeight * 0.12;
        dlg.style.setProperty("--origin", Math.round(r.left + r.width / 2 - left) + "px " + Math.round(r.top + r.height / 2 - top) + "px");
      } else dlg.style.removeProperty("--origin");
      input.value = "";
      list.classList.add("fresh");
      setTimeout(function () { list.classList.remove("fresh"); }, 500);
      render();
      dlg.showModal();
      input.focus();
      overlayOpened(function () { dlg.close(); });
    };
    dlg.addEventListener("close", function () { dlg.style.removeProperty("--drag"); overlayClosed(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    list.addEventListener("click", function (e) { if (e.target.closest("a")) { closeTop = null; dlg.close(); } });
    list.addEventListener("mousemove", function (e) { var a = e.target.closest("a"); if (a) mark($$("a", list).indexOf(a)); });
    input.addEventListener("input", render);
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); mark(sel + 1); }
      if (e.key === "ArrowUp") { e.preventDefault(); mark(sel - 1); }
      if (e.key === "Enter") { var a = $$("a", list)[sel]; if (a) { e.preventDefault(); a.click(); } else if (meant) { e.preventDefault(); input.value = meant; render(); } }
    });
    searchBtns.forEach(function (b) { b.addEventListener("click", openSearch); });
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); if (dlg.open) dlg.close(); else openSearch(null, true); }
      if (e.key === "/" && !/INPUT|TEXTAREA/.test(document.activeElement.tagName) && !dlg.open) { e.preventDefault(); openSearch(null, true); }
    });
    /* Handy: Blatt nach unten wischen zum Schließen */
    var s0 = null;
    dlg.addEventListener("touchstart", function (e) { s0 = list.scrollTop <= 0 || !e.target.closest(".search-list") ? e.touches[0].clientY : null; if (s0 !== null) dlg.style.transition = "none"; }, { passive: true });
    dlg.addEventListener("touchmove", function (e) { if (s0 === null) return; var dy = e.touches[0].clientY - s0; dlg.style.setProperty("--drag", (dy > 0 ? dy : rubber(dy, 40)) + "px"); }, { passive: true });
    dlg.addEventListener("touchend", function (e) {
      if (s0 === null) return;
      var dy = e.changedTouches[0].clientY - s0;
      dlg.style.transition = "";
      if (dy > 120) dlg.close(); else dlg.style.removeProperty("--drag");
      s0 = null;
    });
  } else {
    searchBtns.forEach(function (b) { b.hidden = true; });
  }

  /* ---------- Sanftes Einblenden beim Scrollen ---------- */
  var reveals = $$(".reveal");
  function shown(el) {
    el.classList.add("visible");
    setTimeout(function () { el.classList.remove("reveal"); el.style.removeProperty("--i"); }, 1100);
  }
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      var n = 0;
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.style.setProperty("--i", Math.min(n++, 5));
        shown(en.target);
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---------- Datum ---------- */
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function parse(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  var TAGE = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
  var DF = new Intl.DateTimeFormat("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
  function fmt(d) { return DF.format(d); }
  function fmtLong(d) { return TAGE[d.getDay()] + ", " + fmt(d); }
  var heute = iso(new Date());

  /* Vergangene Termine ausblenden, auf der Startseite nur die nächsten zeigen */
  $$(".event-list").forEach(function (ul) {
    var max = +ul.getAttribute("data-max") || 99, left = 0;
    $$(".event[data-ende]", ul).forEach(function (ev) {
      if (ev.getAttribute("data-ende") < heute || left >= max) ev.hidden = true; else left++;
    });
    var empty = ul.parentNode.querySelector(".events-empty");
    if (empty && !left) empty.hidden = false;
    /* keine kommenden Termine: auch kein „Alle in den Kalender“ */
    if (!left) $$(".js-ics-all", ul.closest("section") || document).forEach(function (a) { a.hidden = true; });
    /* lange Liste: erst 12 zeigen, Rest auf Wunsch */
    var shown = $$(".event[data-ende]", ul).filter(function (ev) { return !ev.hidden; });
    if (!ul.hasAttribute("data-max") && shown.length > 12) {
      var rest = shown.slice(12); rest.forEach(function (ev) { ev.hidden = true; ev.classList.add("more-later"); });
      var more = document.createElement("button"); more.type = "button"; more.className = "btn btn-ghost more-events";
      more.textContent = "Alle " + shown.length + " Termine anzeigen";
      ul.after(more);
      more.addEventListener("click", function () { rest.forEach(function (ev, i) { ev.hidden = false; ev.classList.remove("reveal");
        if (!reduced && ev.animate) ev.animate([{ opacity: 0, translate: "0 8px" }, { opacity: 1, translate: "0 0" }], { duration: 250, delay: Math.min(i, 7) * 40, easing: EASE_OUT, fill: "backwards" }); }); more.remove(); rest[0].querySelector("button, a") && rest[0].querySelector("button, a").focus(); });
    }
  });

  /* ---------- Heute geöffnet / nächste Schließzeit ---------- */
  function closedReason(d) {
    var s = iso(d);
    if (d.getDay() === 0 || d.getDay() === 6) return "Wochenende";
    for (var i = 0; i < K.feiertage.length; i++) if (K.feiertage[i].datum === s) return K.feiertage[i].name;
    for (var j = 0; j < K.schliesszeiten.length; j++) {
      var z = K.schliesszeiten[j];
      if (s >= z.von && s <= z.bis) return "Schließzeit " + z.name;
    }
    return null;
  }
  function nextOpen(from) {
    var d = new Date(from.getFullYear(), from.getMonth(), from.getDate() + 1);
    for (var i = 0; i < 60 && closedReason(d); i++) d.setDate(d.getDate() + 1);
    return d;
  }
  function status() {
    var now = new Date(), reason = closedReason(now);
    var hm = String(now.getHours()).padStart(2, "0") + ":" + String(now.getMinutes()).padStart(2, "0");
    var open = !reason && hm >= K.oeffnung && hm < K.schluss, today, sub;
    if (open) {
      today = "Jetzt geöffnet – heute bis " + K.schluss + " Uhr";
      sub = "Krippe und Kindergarten bis 16:30 Uhr, Spätdienst bis 17:30 Uhr, Hort bis 18:00 Uhr.";
    } else if (!reason && hm < K.oeffnung) {
      today = "Heute geöffnet ab " + K.oeffnung + " Uhr";
      sub = "Krippe und Kindergarten bis 16:30 Uhr, Hort bis 18:00 Uhr.";
    } else {
      today = reason ? "Heute geschlossen (" + reason + ")" : "Für heute geschlossen";
      sub = "Wir sind wieder da am " + fmtLong(nextOpen(now)) + " ab " + K.oeffnung + " Uhr.";
    }
    var next = "Der Ferienplan für das nächste Kita-Jahr folgt in Kürze.";
    for (var i = 0; i < K.schliesszeiten.length; i++) {
      var z = K.schliesszeiten[i];
      if (z.bis < heute) continue;
      var v = parse(z.von), b = parse(z.bis);
      next = (heute >= z.von ? "Aktuelle Schließzeit: " : "Nächste Schließzeit: ") + z.name + ", " +
             (z.von === z.bis ? fmtLong(v) : fmt(v) + " – " + fmt(b)) + " (" + z.tage + (z.tage === 1 ? " Schließtag)" : " Schließtage)");
      break;
    }
    return { open: open, today: today, sub: sub, next: next };
  }
  if (K) {
    var st = status();
    ["status", "status-kontakt"].forEach(function (id) {
      var box = document.getElementById(id);
      if (!box) return;
      $(".status-today", box).textContent = st.today;
      $(".status-sub", box).textContent = st.sub;
      var nx = $(".status-next span", box);
      if (nx) nx.textContent = st.next;
      box.classList.toggle("is-closed", !st.open);
      box.hidden = false;
    });
  }

  /* ---------- Wichtiger Hinweis (daten/dringend.csv): oben auf jeder Seite und in der Status-Anzeige ---------- */
  var dringend = K && K.dringend ? K.dringend.filter(function (x) { return x.von <= heute && x.bis >= heute; })[0] : null;
  if (dringend) {
    var dBand = document.createElement("div"); dBand.className = "dringend"; dBand.setAttribute("role", "status");
    dBand.innerHTML = '<div class="container dringend-in"><span class="dringend-ic" aria-hidden="true">!</span><p><strong>Wichtiger Hinweis:</strong> <span></span></p></div>';
    $("p span", dBand).textContent = dringend.text;
    var mainEl = document.querySelector("main"); if (mainEl) mainEl.prepend(dBand);
    /* langer Hinweis: auf schmalen Bildschirmen drei Zeilen, Rest hinter „Weiterlesen“ */
    var dP = $("p", dBand);
    requestAnimationFrame(function () {
      if (dP.scrollHeight <= dP.clientHeight + 2) return;
      var mehr = document.createElement("button"); mehr.type = "button"; mehr.className = "dringend-mehr"; mehr.textContent = "Weiterlesen"; mehr.setAttribute("aria-expanded", "false");
      mehr.addEventListener("click", function () { var auf = dBand.classList.toggle("offen"); mehr.textContent = auf ? "Weniger" : "Weiterlesen"; mehr.setAttribute("aria-expanded", String(auf)); });
      $(".dringend-in", dBand).appendChild(mehr);
    });
    ["status", "status-kontakt"].forEach(function (id) { var bx = document.getElementById(id); if (!bx) return; var sub = $(".status-sub", bx); if (sub) { sub.textContent = dringend.text; sub.classList.add("ist-dringend"); } });
  }

  /* ---------- Hinweis auf den nächsten Termin, ausblendbar mit „Rückgängig“ ---------- */
  var note = document.getElementById("hinweis");
  if (note && K && K.termine) {
    var nextEv = K.termine.filter(function (t) { return t.bis >= heute; })[0];
    /* das Band nur, wenn der nächste Termin in höchstens 3 Tagen ist; sonst steht er schon unter „Termine & Unterlagen“ */
    if (nextEv && (parse(nextEv.von) - new Date()) / 864e5 > 3) nextEv = null;
    if (nextEv) {
      var key = "hinweis-aus", id = nextEv.von + nextEv.titel;
      var a = parse(nextEv.von), b2 = parse(nextEv.bis);
      note.innerHTML = '<div class="container announce-inner">' + svg(ICON.calendar, 20) +
        '<p><strong></strong> <span></span></p><a href="aktuelles.html#termine">Alle Termine</a>' +
        '<button type="button" class="icon-btn" aria-label="Hinweis ausblenden">' + svg(ICON.x, 18) + "</button></div>";
      $("strong", note).textContent = "Nächster Termin:";
      $("p span", note).textContent = nextEv.titel + " – " + (nextEv.von === nextEv.bis ? fmtLong(a) : fmt(a) + " bis " + fmt(b2));
      var jetzt = new Date();
      var dleft = Math.round((Date.UTC(a.getFullYear(), a.getMonth(), a.getDate()) - Date.UTC(jetzt.getFullYear(), jetzt.getMonth(), jetzt.getDate())) / 864e5);
      if (dleft > 0) {
        var when = document.createElement("span"); when.className = "announce-in";
        when.innerHTML = 'in <span class="roll"></span> ' + (dleft === 1 ? "Tag" : "Tagen");
        $("p", note).appendChild(when);
        var rl = $(".roll", when); roll(rl, 0);
        if ("IntersectionObserver" in window) new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { setTimeout(function () { roll(rl, dleft); }, 400); o.disconnect(); } }).observe(note);
        else roll(rl, dleft);
      }
      note.hidden = store(key) === id;
      if (!note.hidden) root.classList.remove("no-hint");
      $("button", note).addEventListener("click", function () {
        store(key, id);
        var weg = function () { note.hidden = true; note.getAnimations().forEach(function (a) { a.cancel(); }); };
        if (reduced) weg();
        else { note.animate([{ opacity: 1, scale: 1 }, { opacity: 0, scale: .98 }], { duration: 180, fill: "forwards" }); hoehe(note, note.offsetHeight, 0, 250, EIO_, weg); }
        toast("Hinweis ausgeblendet", "Rückgängig", function () {
          note.hidden = false; store(key, null);
          if (!reduced) { hoehe(note, 0, note.offsetHeight, 250, EIO_); note.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220, delay: 80, fill: "backwards" }); }
        });
      });
    }
  }
  if (note && !note.firstChild) note.hidden = true;

  /* ---------- Termine merken: Datum fliegt im Bogen zum Zähler, gemerkte als Kalenderdatei ---------- */
  var SAVED_KEY = "gemerkt";
  function savedList() { try { return JSON.parse(store(SAVED_KEY) || "[]"); } catch (e) { return []; } }
  function setSaved(list) { store(SAVED_KEY, JSON.stringify(list)); }
  function calTarget() {
    var m = $('.main-nav a[href="aktuelles.html"]') || $('.main-nav a[href="#aktuelles"]');
    if (m && m.getBoundingClientRect().width) return m;
    return $(".nav-toggle") || m;   /* Handy: Menü zu – der Zähler sitzt am Menü-Knopf */
  }
  function refreshSaved(pulse) {
    var list = savedList();
    $$(".nav-badge").forEach(function (b) {
      b.textContent = list.length ? list.length : "";
      b.classList.toggle("show", list.length > 0);
      if (pulse) { b.classList.remove("pulse"); void b.offsetWidth; b.classList.add("pulse"); }
    });
    /* je Terminliste zählen, wie viele ihrer Termine gemerkt sind */
    $$(".saved-row").forEach(function (row) {
      var n = $$(".event[data-von]", row.closest("section") || document).filter(function (li) { return list.indexOf($(".save", li).getAttribute("data-key")) >= 0 && !li.hidden; }).length;
      var war = row.hidden ? 0 : +$(".saved-n", row).textContent || 0, zahl = $(".saved-n", row);
      var weich = row.dataset.bereit && !reduced && row.animate && row.closest("section") && row.closest("section").getClientRects().length;
      row.dataset.bereit = "1";
      if (!weich) { row.hidden = !n; zahl.textContent = n; return; }
      if (n && !war) {
        /* erscheint: Platz weich öffnen, Knöpfe kurz nacheinander */
        row.hidden = false; zahl.textContent = n;
        if (row._zu) { row._zu = false; row.getAnimations().forEach(function (a) { a.cancel(); }); }
        hoehe(row, 0, row.offsetHeight, 260, EIO_);
        $$(".btn", row).forEach(function (b, i) { b.animate([{ opacity: 0, translate: "0 6px" }, { opacity: 1, translate: "0 0" }], { duration: 220, delay: 60 + i * 50, easing: EASE_OUT, fill: "backwards" }); });
      } else if (!n && war) {
        /* verschwindet: weich zuklappen */
        row._zu = true;
        row.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 160, fill: "forwards" });
        hoehe(row, row.offsetHeight, 0, 220, EIO_, function () { if (row._zu) { row.hidden = true; row._zu = false; } row.getAnimations().forEach(function (a) { a.cancel(); }); });
      } else if (n !== war) {
        /* Zahl ändert sich: kurz aufspringen */
        zahl.textContent = n;
        zahl.animate([{ scale: 1.35, color: "var(--rose-deep)" }, { scale: 1 }], { duration: 300, easing: EASE_OUT });
      }
    });
  }
  $$(".event .save").forEach(function (btn) {
    var key = btn.getAttribute("data-key"), li = btn.closest(".event"), title = li.getAttribute("data-titel");
    function paint(on) {
      btn.classList.toggle("on", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.setAttribute("aria-label", title + (on ? " gemerkt – nicht mehr merken" : " merken"));
    }
    paint(savedList().indexOf(key) >= 0);
    btn.addEventListener("click", function () {
      var list = savedList(), on = list.indexOf(key) < 0;
      if (on) list.push(key); else list.splice(list.indexOf(key), 1);
      setSaved(list);
      paint(on);   /* sofort umschalten, erst danach die Flug-Animation */
      var t = calTarget(), date = $(".date", li);
      if (on && t && !reduced && date.animate) {
        var a = date.getBoundingClientRect(), b = t.getBoundingClientRect();
        var f = date.cloneNode(true);
        f.className = "date flyer";
        f.style.cssText = "left:" + a.left + "px;top:" + a.top + "px;width:" + a.width + "px;height:" + a.height + "px";
        document.body.appendChild(f);
        var dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
        /* Bogen: Mittelpunkt liegt höher als die direkte Linie */
        f.animate([
          { transform: "translate(0,0) scale(1)", opacity: 1 },
          { transform: "translate(" + dx * 0.5 + "px," + (dy * 0.5 - 90) + "px) scale(.7)", opacity: 1, offset: .5 },
          { transform: "translate(" + dx + "px," + dy + "px) scale(.2)", opacity: .2 }
        ], { duration: 600, easing: EASE_IO }).onfinish = function () { f.remove(); refreshSaved(true); };
      } else refreshSaved(on);
      toast(on ? "Termin gemerkt" : "Nicht mehr gemerkt", "Rückgängig", function () { btn.click(); });
    });
  });
  refreshSaved(false);
  function icsEsc(s) { return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n"); }
  $$(".js-saved-ics").forEach(function (b) {
    b.addEventListener("click", function () {
      var list = savedList(), stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
      var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kinderhort Grombuehl//Webseite//DE", "CALSCALE:GREGORIAN", "METHOD:PUBLISH"];
      var seen = {};
      $$(".event[data-von]", b.closest("section") || document).forEach(function (li, i) {
        var k = $(".save", li).getAttribute("data-key");
        if (list.indexOf(k) < 0 || seen[k]) return;
        seen[k] = 1;
        var von = li.getAttribute("data-von").replace(/-/g, ""), bis = parse(li.getAttribute("data-ende"));
        bis.setDate(bis.getDate() + 1);
        lines.push("BEGIN:VEVENT", "UID:gemerkt-" + von + "-" + i + "@kinderhort-grombuehl.de", "DTSTAMP:" + stamp,
          "DTSTART;VALUE=DATE:" + von, "DTEND;VALUE=DATE:" + iso(bis).replace(/-/g, ""),
          "SUMMARY:" + icsEsc(li.getAttribute("data-titel")), "DESCRIPTION:" + icsEsc(li.getAttribute("data-text")),
          "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:Morgen: " + icsEsc(li.getAttribute("data-titel")), "TRIGGER:-PT6H", "END:VALARM", "END:VEVENT");
      });
      lines.push("END:VCALENDAR");
      var url = URL.createObjectURL(new Blob([lines.join("\r\n") + "\r\n"], { type: "text/calendar" }));
      var a = document.createElement("a"); a.href = url; a.download = "gemerkte-termine.ics"; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      toast("Kalenderdatei erstellt");
    });
  });

  /* ---------- Kita-Jahr als Zeitstrahl ---------- */
  if (K && K.schliesszeiten && K.schliesszeiten.length) {
    var first = parse(K.schliesszeiten[0].von), y0 = first.getMonth() >= 8 ? first.getFullYear() : first.getFullYear() - 1;
    var DAYMS = 864e5, ystart = Date.UTC(y0, 8, 1), ylen = Math.round((Date.UTC(y0 + 1, 8, 1) - ystart) / DAYMS);
    var dayIdx = function (dt) { return Math.round((Date.UTC(dt.getFullYear(), dt.getMonth(), dt.getDate()) - ystart) / DAYMS); };
    var MON = ["Sep", "Okt", "Nov", "Dez", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug"];
    $$("[data-yearline]").forEach(function (box) {
      box.innerHTML = '<div class="yl-head"><strong>Das Kita-Jahr ' + y0 + "/" + (y0 + 1) + '</strong><span class="yl-legend"><i class="lg-closed"></i>geschlossen <i class="lg-today"></i>heute</span></div>' +
        '<div class="yl-bar" role="slider" tabindex="0" aria-label="Tag im Kita-Jahr wählen" aria-valuemin="0" aria-valuemax="' + (ylen - 1) + '"><span class="yl-pin"></span></div>' +
        '<div class="yl-months" aria-hidden="true">' + MON.map(function (m) { return "<span>" + m + "</span>"; }).join("") + "</div>" +
        '<p class="yl-info" aria-live="polite"></p>';
      var bar = $(".yl-bar", box), pin = $(".yl-pin", box), info = $(".yl-info", box);
      var nextLine = document.createElement("span"), noneLine = document.createElement("span");
      nextLine.innerHTML = 'Nächste Schließzeit: <span class="yl-next"></span> in <span class="roll"></span><span class="yl-unit"></span>';
      noneLine.textContent = "Danach gilt der neue Ferienplan.";
      var nextName = $(".yl-next", nextLine), rollEl = $(".roll", nextLine), unit = $(".yl-unit", nextLine);
      K.schliesszeiten.forEach(function (z) {
        var s = dayIdx(parse(z.von)), e = dayIdx(parse(z.bis)) + 1, el = document.createElement("span");
        el.className = "yl-closed"; el.title = z.name;
        el.style.left = (s / ylen * 100) + "%"; el.style.width = Math.max(.5, (e - s) / ylen * 100) + "%";
        bar.appendChild(el);
      });
      var ti = dayIdx(new Date());
      if (ti >= 0 && ti < ylen) { var tm = document.createElement("span"); tm.className = "yl-today"; tm.style.left = (ti / ylen * 100) + "%"; bar.appendChild(tm); }
      var cur = Math.min(ylen - 1, Math.max(0, ti)), dragging = false, pinAnteil = null;
      /* Nadel per translate (Grafikkarte) statt „left“; Pixel aus der Breite des Bands */
      function pinSetzen(x) { pin.style.translate = (x !== undefined ? x : pinAnteil * bar.clientWidth + "px") + " 0"; }
      if (window.ResizeObserver) new ResizeObserver(function () { if (pinAnteil === null || dragging) return; pin.style.transition = "none"; pinSetzen(); void pin.offsetWidth; pin.style.transition = ""; }).observe(bar);
      function showDay(i, x) {
        cur = i;
        if (x === undefined) pinAnteil = (i + .5) / ylen;
        pinSetzen(x);
        var dt = new Date(y0, 8, 1 + i), s = iso(dt), hit = null, next = null;
        K.schliesszeiten.forEach(function (z) { if (s >= z.von && s <= z.bis) hit = z; if (!next && z.von > s) next = z; });
        var reason = closedReason(dt), label = fmtLong(dt);
        bar.setAttribute("aria-valuenow", i);
        bar.setAttribute("aria-valuetext", label);
        var b = $("strong", info);
        if (!b) { b = document.createElement("strong"); info.appendChild(b); }
        b.textContent = label + (hit ? " – geschlossen (" + hit.name + ")" : reason ? " – geschlossen (" + reason + ")" : " – geöffnet");
        nextLine.hidden = !next; noneLine.hidden = !!next;
        if (next) {
          var n = dayIdx(parse(next.von)) - i;
          nextName.textContent = next.name; roll(rollEl, n); unit.textContent = n === 1 ? " Tag" : " Tagen";
          box.classList.toggle("dragging", dragging);
        }
        if (!nextLine.parentNode) { info.appendChild(nextLine); info.appendChild(noneLine); }
      }
      function at(e) {
        var r = bar.getBoundingClientRect(), x = e.clientX - r.left, inside = Math.min(r.width, Math.max(0, x));
        showDay(Math.min(ylen - 1, Math.floor(inside / r.width * ylen)), (inside + rubber(x - inside, 24)) + "px");
      }
      bar.addEventListener("pointerdown", function (e) { dragging = true; bar.setPointerCapture(e.pointerId); pin.style.transition = "none"; at(e); });
      bar.addEventListener("pointermove", function (e) { if (dragging) at(e); });
      function release() { if (!dragging) return; dragging = false; pin.style.transition = ""; showDay(cur); }
      bar.addEventListener("pointerup", release);
      bar.addEventListener("pointercancel", release);
      bar.addEventListener("keydown", function (e) {
        var k = { ArrowRight: 1, ArrowLeft: -1, PageUp: 7, PageDown: -7, Home: -999, End: 999 }[e.key];
        if (!k) return;
        e.preventDefault();
        showDay(Math.min(ylen - 1, Math.max(0, cur + k)));
      });
      showDay(cur);
    });
  }

  /* ---------- Fragen durchsuchen: Treffer rücken weich zusammen ---------- */
  $$(".faq").forEach(function (faqBox) {
    var input = $("#faq-suche", faqBox);
    if (!input) return;
    var items = $$("details", faqBox), count = $(".faq-count", faqBox), empty = $(".faq-empty", faqBox);
    var norm = function (s) { return s.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss"); };
    items.forEach(function (d) { var sm = $("summary", d); sm.setAttribute("data-q", sm.textContent); });
    function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    input.addEventListener("keydown", function (e) { if (e.key === "Escape" && input.value) { e.preventDefault(); input.value = ""; input.dispatchEvent(new Event("input")); } });
    input.addEventListener("input", function () {
      var v = input.value.trim(), nv = norm(v), before = new Map(), shown = 0;
      items.forEach(function (d) { if (!d.hidden) before.set(d, d.getBoundingClientRect()); });
      items.forEach(function (d) {
        var sm = $("summary", d), q = sm.getAttribute("data-q"), hay = norm(q + " " + $("div", d).textContent);
        var hit = !nv || nv.split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; });
        d.hidden = !hit;
        if (hit) shown++;
        var at = nv ? norm(q).indexOf(nv) : -1;
        /* Umlaute ändern die Länge nicht, wenn wir im Original suchen; sonst nur ohne Markierung */
        var raw = v ? q.toLowerCase().indexOf(v.toLowerCase()) : -1;
        sm.innerHTML = raw >= 0 ? esc(q.slice(0, raw)) + "<mark>" + esc(q.slice(raw, raw + v.length)) + "</mark>" + esc(q.slice(raw + v.length)) : esc(q);
        if (at < 0 && raw < 0) sm.innerHTML = esc(q);
      });
      empty.hidden = shown > 0;
      count.textContent = nv ? shown + (shown === 1 ? " Frage" : " Fragen") : "";
      if (reduced) return;
      items.forEach(function (d) {
        if (d.hidden) return;
        var a = before.get(d), b = d.getBoundingClientRect();
        if (!a) d.animate([{ opacity: 0, transform: "scale(.95)" }, { opacity: 1, transform: "none" }], { duration: 250, easing: EASE_OUT });
        else if (Math.abs(a.top - b.top) > 1) d.animate([{ transform: "translateY(" + (a.top - b.top) + "px)" }, { transform: "none" }], { duration: 300, easing: EASE_IO });
      });
    });
  });

  /* ---------- Lesefortschritt und „Nach oben“ ---------- */
  (function () {
    var prog = document.createElement("div");
    prog.className = "read-progress";
    prog.setAttribute("aria-hidden", "true");
    document.body.appendChild(prog);
    var up = document.createElement("button");
    up.type = "button";
    up.className = "to-top";
    up.setAttribute("aria-label", "Nach oben");
    up.innerHTML = '<svg class="ring" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22"/></svg>' + svg('<path d="M6 14l6-6 6 6"/>', 20);
    document.body.appendChild(up);
    var ring = $(".ring circle", up), C = 2 * Math.PI * 22;
    ring.style.strokeDasharray = C;
    function upd() {
      var doc = document.documentElement, max = doc.scrollHeight - innerHeight;
      var long = doc.scrollHeight > innerHeight * 2.2, p = max > 0 ? Math.min(1, scrollY / max) : 0;
      prog.style.scale = (long ? p : 0) + " 1";
      ring.style.strokeDashoffset = C * (1 - p);
      up.classList.toggle("show", long && p > 1 / 3);
    }
    addEventListener("scroll", upd, { passive: true });
    addEventListener("resize", upd);
    upd();
    up.addEventListener("click", function () {
      scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
      /* Tastatur-Nutzer landen wieder am Seitenanfang */
      var brand = $(".brand"); if (brand) setTimeout(function () { brand.focus({ preventScroll: true }); }, reduced ? 0 : 450);
    });
  })();

  /* ---------- Seitenwechsel bei langsamer Verbindung ---------- */
  /* unter 1 s nichts zeigen, ab 1 s Ladebalken, ab 10 s ein Hinweis */
  (function () {
    var t1 = null, t2 = null;
    function reset() { clearTimeout(t1); clearTimeout(t2); document.body.classList.remove("nav-loading"); }
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === "_blank" || a.hasAttribute("download")) return;
      var url = new URL(a.href, location.href);
      if (url.origin !== location.origin || !/\.html$|\/$/.test(url.pathname) || (url.pathname === location.pathname && url.hash)) return;
      reset();
      t1 = setTimeout(function () { document.body.classList.add("nav-loading"); }, 1000);
      t2 = setTimeout(function () { toast("Die Verbindung ist gerade langsam – die Seite lädt noch."); }, 10000);
    });
    addEventListener("pageshow", reset);
    addEventListener("pagehide", function () { clearTimeout(t2); });
  })();

  /* ---------- Rollende Ziffern (Zählwerk) ---------- */
  function roll(el, n) {
    var s = String(Math.max(0, n)), cols = $$(".roll-col", el);
    /* Vorleser bekommen die Zahl als Text, die Ziffernwalzen sind nur Optik */
    var sr = $(".visually-hidden", el);
    if (!sr) { sr = document.createElement("span"); sr.className = "visually-hidden"; el.appendChild(sr); }
    sr.textContent = s; el.dataset.value = s;
    while (cols.length < s.length) {
      var d = document.createElement("span"); d.className = "roll-digit"; d.setAttribute("aria-hidden", "true");
      var c = document.createElement("span"); c.className = "roll-col";
      for (var k = 0; k < 10; k++) { var x = document.createElement("span"); x.textContent = k; c.appendChild(x); }
      var g = document.createElement("span"); g.className = "roll-ghost"; g.textContent = "0"; /* hält die Schriftlinie */
      d.appendChild(g); d.appendChild(c); el.insertBefore(d, el.firstChild); cols.unshift(c);
    }
    while (cols.length > s.length) { el.firstChild.remove(); cols.shift(); }
    cols.forEach(function (c, i) { c.style.setProperty("--i", i); c.style.translate = "0 " + (-s[i] * 1.2) + "em"; });
  }

  /* ---------- Überschriften steigen Wort für Wort auf ---------- */
  if (!reduced && "IntersectionObserver" in window) {
    var hio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("go"); hio.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -10% 0px" });
    $$(".section-head h2").forEach(function (h) {
      var n = 0, label = h.textContent.replace(/\s+/g, " ").trim();
      (function wrap(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var frag = document.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function (w) {
              if (!w) return;
              if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(" ")); return; }
              var o = document.createElement("span"), i = document.createElement("span");
              o.className = "hw"; i.textContent = w; i.style.setProperty("--w", n++); o.appendChild(i); frag.appendChild(o);
            });
            c.replaceWith(frag);
          } else if (c.nodeType === 1) wrap(c);
        });
      })(h);
      h.setAttribute("aria-label", label);
      $$(".hw", h).forEach(function (w) { w.setAttribute("aria-hidden", "true"); });
      h.classList.add("words");
      hio.observe(h);
    });
  }

  /* ---------- Zahlen zählen hoch ---------- */
  (function () {
    var els = $$(".stat b");
    if (!els.length || reduced || !("IntersectionObserver" in window)) return;
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var el = e.target, final = el.textContent, parts = final.split(/(\d+(?:,\d+)?)/), t0 = null, from = el.getAttribute("data-from");
        el.setAttribute("aria-label", final);
        el.style.minWidth = el.offsetWidth + "px";
        function frame(t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1200), k = 1 - Math.pow(1 - p, 4);
          el.textContent = parts.map(function (tok, i) {
            if (i % 2 === 0) return tok;
            var dec = (tok.split(",")[1] || "").length, to = parseFloat(tok.replace(",", ".")), f = from !== null ? parseFloat(from) : 0;
            var v = (f + (to - f) * k).toFixed(dec).replace(".", ",");
            if (/:$/.test(parts[i - 1])) v = v.padStart(tok.length, "0");   /* Uhrzeit: 6:05 statt 6:5 */
            return v;
          }).join("");
          if (p < 1) requestAnimationFrame(frame); else { el.textContent = final; el.style.minWidth = ""; }
        }
        requestAnimationFrame(frame);
      });
    }, { threshold: .6 });
    els.forEach(function (el) { cio.observe(el); });
  })();

  /* ---------- Wimpelkette weht beim Scrollen (reines Schmuck-Element, darf nachschwingen) ---------- */
  (function () {
    var flags = $$(".site-footer .bunting .flag");
    if (!flags.length || reduced) return;
    var st = flags.map(function (f, i) { return { el: f, a: 0, v: 0, k: .8 + (i % 3) * .15 }; });
    var lastY = scrollY, lastT = performance.now(), wind = 0, running = false, visible = false;
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(flags[0].ownerSVGElement);
    function tick() {
      var still = true;
      st.forEach(function (f) {
        var target = Math.max(-28, Math.min(28, wind * f.k));
        f.v += (target - f.a) * .06; f.v *= .86; f.a += f.v;
        f.el.style.transform = "rotate(" + f.a.toFixed(2) + "deg)";
        if (Math.abs(f.v) > .02 || Math.abs(f.a) > .05) still = false;
      });
      wind *= .88;
      if (Math.abs(wind) > .05) still = false;
      if (still) { running = false; st.forEach(function (f) { f.el.style.transform = ""; }); return; }
      requestAnimationFrame(tick);
    }
    addEventListener("scroll", function () {
      var now = performance.now(), dy = scrollY - lastY, dt = Math.max(16, now - lastT);
      lastY = scrollY; lastT = now;
      if (!visible) return;
      wind = Math.max(-30, Math.min(30, wind + dy / dt * 9));
      if (!running) { running = true; requestAnimationFrame(tick); }
    }, { passive: true });
  })();

  /* ---------- Licht folgt der Maus auf dunklen Karten ---------- */
  if (matchMedia("(hover: hover) and (pointer: fine)").matches && !reduced) {
    var SPOT = ".info-card, .room, .area-card, .quick-card, .dl-group, .phone-card, .note-card, .stat, .pill-list > div, .tl-body, .event, .address-card, .status-card, .faq summary";
    var lit = null, raf = 0, pe = null;
    document.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      pe = e;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var el = pe.target.closest && pe.target.closest(SPOT);
        if (lit && lit !== el) { lit.style.removeProperty("--mx"); lit.style.removeProperty("--my"); }
        lit = el;
        if (!el) return;
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", (pe.clientX - r.left) + "px");
        el.style.setProperty("--my", (pe.clientY - r.top) + "px");
      });
    }, { passive: true });
  }

  /* ---------- Magnetische Hauptknöpfe (bewusst schwach) ---------- */
  if (matchMedia("(hover: hover) and (pointer: fine)").matches && !reduced) {
    $$(".js-magnet").forEach(function (m) {
      var zone = m.parentNode;
      zone.addEventListener("pointermove", function (e) {
        var r = m.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2), d = Math.hypot(dx, dy), R = 90;
        if (d < R) { var k = 1 - d / R; m.classList.add("near"); m.style.translate = (dx * .1 * k).toFixed(1) + "px " + (dy * .14 * k).toFixed(1) + "px"; }
        else { m.classList.remove("near"); m.style.translate = ""; }
      });
      zone.addEventListener("pointerleave", function () { m.classList.remove("near"); m.style.translate = ""; });
    });
  }

  /* ---------- Licht nach Tageszeit im Auftakt der Startseite ---------- */
  (function () {
    var hero = $(".hero");
    if (!hero) return;
    var d = new Date(), m = d.getHours() * 60 + d.getMinutes(), p = Math.min(1, Math.max(0, (m - 405) / (1080 - 405)));
    var night = m < 405 || m >= 1080;
    /* Das Licht wandert im Bogen von links (morgens) über oben (mittags) nach rechts (abends) */
    hero.style.setProperty("--gx", (10 + p * 80).toFixed(1) + "%");
    hero.style.setProperty("--gy", (8 - Math.sin(p * Math.PI) * 26).toFixed(1) + "%");
    var warm = [255, 226, 196], noon = [241, 229, 227], eve = [214, 210, 236], c;
    if (night) c = [196, 212, 232];
    else if (p < .5) c = warm.map(function (v, i) { return Math.round(v + (noon[i] - v) * p * 2); });
    else c = noon.map(function (v, i) { return Math.round(v + (eve[i] - v) * (p - .5) * 2); });
    hero.style.setProperty("--glow", "rgba(" + c.join(",") + "," + (night ? .45 : .8) + ")");
    hero.classList.add("lit");
  })();

  /* ---------- Fachbegriffe: Erklärung wächst aus dem Wort ---------- */
  (function () {
    var terms = $$(".term");
    if (!terms.length || !K || !K.glossar) return;
    var pop = document.createElement("div");
    pop.className = "term-pop"; pop.id = "begriff"; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Erklärung");
    pop.innerHTML = "<strong></strong><p></p>";
    document.body.appendChild(pop);
    var open = null;
    function close(back) { if (!open) return; var t = open; open = null; pop.classList.remove("open"); t.setAttribute("aria-expanded", "false"); if (back) t.focus(); }
    terms.forEach(function (t) {
      t.setAttribute("aria-expanded", "false"); t.setAttribute("aria-controls", "begriff");
      t.addEventListener("click", function (e) {
        e.stopPropagation();
        if (open === t) { close(); return; }
        close();
        var key = t.getAttribute("data-term");
        $("strong", pop).textContent = key; $("p", pop).textContent = K.glossar[key] || "";
        var r = t.getBoundingClientRect(), w = Math.min(300, innerWidth - 32);
        var left = Math.max(16, Math.min(innerWidth - w - 16, r.left + r.width / 2 - w / 2));
        var below = r.bottom + 10, top = below + 160 > innerHeight && r.top > 180 ? r.top - 10 : below;
        pop.style.width = w + "px"; pop.style.left = (left + scrollX) + "px";
        pop.classList.toggle("above", top !== below);
        pop.style.top = (top + scrollY) + "px";
        pop.style.transformOrigin = (r.left + r.width / 2 - left) + "px " + (top !== below ? "100%" : "0");
        void pop.offsetWidth;
        pop.classList.add("open"); t.setAttribute("aria-expanded", "true"); open = t;
      });
    });
    document.addEventListener("click", function (e) { if (open && !pop.contains(e.target)) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && open) close(true); });
    addEventListener("resize", function () { close(); });
  })();

  /* ---------- Gemeinsam: Durchwahlen der Seite und unscharfes Suchen ---------- */
  function normDe(s) { return String(s).toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim(); }
  /* Tippfehler verzeihen: Abstand höchstens 1 (ab 4 Buchstaben) bzw. 2 (ab 8) */
  function nah(a, b) {
    if (a === b) return true;
    var max = b.length >= 10 ? 2 : b.length >= 4 ? 1 : 0; if (!max || Math.abs(a.length - b.length) > max) return false;
    var prev = [], cur, i, j; for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) { cur = [i]; for (j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); prev = cur; }
    return prev[b.length] <= max;
  }
  /* passt ein getipptes Wort zu einem Schlüsselwort? (Anfang oder kleiner Tippfehler) */
  function passt(w, k) { return k.indexOf(w) === 0 || (w.length >= 4 && (nah(w, k) || nah(w, k.slice(0, w.length)))); }
  var DW_ALIAS = { kiga: "kindergarten", garten: "kindergarten", kita: "", krabbel: "kinderkrippe", krippe: "kinderkrippe", hort: "kinderhort", schule: "kinderhort", hausaufgaben: "kinderhort",
    zentrale: "allgemein", buero: "allgemein", verwaltung: "allgemein", leitung: "allgemein", anmeldung: "allgemein", haupt: "allgemein", sonne: "sonnengruppe", stern: "sternengruppe", sterne: "sternengruppe",
    baer: "baerengruppe", baeren: "baerengruppe", biene: "bienengruppe", bienen: "bienengruppe", spatz: "spatzengruppe", spatzen: "spatzengruppe" };
  function durchwahlen() {
    var dir = [];
    $$(".phone-card").forEach(function (card) {
      var area = $("h3", card).textContent.trim();
      $$(".phone-list li", card).forEach(function (li) {
        var a = $("a", li); if (!a || !/^tel:/.test(a.getAttribute("href"))) return;
        var label = $("span", li).textContent.trim(), num = a.textContent.replace(/\s+/g, " ").trim(), endung = num.split(" ").pop();
        dir.push({ li: li, label: label, area: area, num: num, href: a.getAttribute("href"), endung: endung,
          keys: normDe(label + " " + area + " " + label.replace(/gruppe$/i, "") + (/allgemein/i.test(label) ? " zentrale buero leitung" : "")).split(" ") });
      });
    });
    return dir;
  }
  function suche(dir, q) {
    var ws = normDe(q).split(" ").filter(Boolean).map(function (w) { return DW_ALIAS[w] !== undefined ? DW_ALIAS[w] : w; }).filter(Boolean);
    if (!ws.length) return [];
    var exakt = normDe(q).split(" ").filter(Boolean).map(function (w) { return DW_ALIAS[w] !== undefined; });
    return dir.filter(function (d) { return ws.every(function (w, i) { if (exakt[i]) return d.keys.some(function (k) { return k.indexOf(w) === 0; }); return /^\d+$/.test(w) ? d.endung === w || d.num.replace(/\D/g, "").slice(-w.length) === w : d.keys.some(function (k) { return passt(w, k); }); }); });
  }

  /* ---------- Durchwahl finden: Treffer im Kasten, die Listen darunter treten zurück ---------- */
  (function () {
    var inp = $("#durchwahl");
    if (!inp) return;
    var box = inp.closest(".dial"), out = $(".dial-out", box), timer = null, last = "", wrap = box.parentNode;
    var dir = durchwahlen();
    function show(html) {
      if (html === last) return; last = html;
      if (reduced) { out.innerHTML = html; return; }
      out.classList.add("swap");
      setTimeout(function () { out.innerHTML = html; out.classList.remove("swap"); }, 120);
    }
    function row(h) { return '<p><a href="' + escH(h.href) + '">' + escH(h.num).replace(/ /g, "&nbsp;") + "</a><span>" + escH(h.label + " · " + h.area) + "</span></p>"; }
    inp.addEventListener("input", function () {
      clearTimeout(timer); inp.parentNode.classList.remove("err");
      var v = inp.value.trim();
      wrap.classList.toggle("dial-searching", !!v);
      if (!v) { show(""); dir.forEach(function (d) { d.li.hidden = false; }); $$(".phone-card", wrap).forEach(function (c) { c.hidden = false; }); return; }
      var hits = suche(dir, v);
      /* Treffer bleiben in ihrem türkisen Kasten, alles andere tritt zurück */
      dir.forEach(function (d) { d.li.hidden = hits.indexOf(d) < 0; });
      $$(".phone-card", wrap).forEach(function (c) { c.hidden = !$$(".phone-list li", c).some(function (li) { return !li.hidden && $('a[href^="tel:"]', li); }); });
      if (hits.length) { show(""); return; }
      timer = setTimeout(function () {
        inp.parentNode.classList.add("err");
        if (!reduced) { inp.parentNode.classList.remove("shake"); void inp.parentNode.offsetWidth; inp.parentNode.classList.add("shake"); }
        show('<p><a href="tel:+4993127898920">0931&nbsp;2789892&nbsp;0</a><span>Keine Gruppe gefunden – die Zentrale verbindet Sie gern.</span></p>');
      }, 500);
    });
    inp.addEventListener("keydown", function (e) { if (e.key === "Escape" && inp.value) { inp.value = ""; inp.dispatchEvent(new Event("input")); } });
  })();

  /* ---------- Rundgang als Geschichte ---------- */
  (function () {
    var openers = $$(".story-open");
    if (!openers.length) return;
    var view = document.createElement("div");
    view.className = "story-view"; view.setAttribute("role", "dialog"); view.setAttribute("aria-modal", "true"); view.setAttribute("aria-label", "Rundgang als Geschichte");
    view.innerHTML = '<div class="story-card"><div class="story-bars"></div><div class="story-imgs"></div>' +
      '<div class="story-cap"><strong></strong><span></span></div><span class="story-paused">Pause</span>' +
      '<button type="button" class="story-close lb-btn" aria-label="Schließen">' + svg(ICON.x, 22) + "</button>" +
      '<button type="button" class="story-zone prev" aria-label="Vorheriges Bild"></button><button type="button" class="story-zone next" aria-label="Nächstes Bild"></button></div>';
    document.body.appendChild(view);
    var card = $(".story-card", view), barsEl = $(".story-bars", view), imgsEl = $(".story-imgs", view), cap = $(".story-cap", view);
    var items = [], fills = [], imgs = [], i = 0, p = 0, last = null, hold = false, active = false, DUR = 5000, opener = null;
    function show(n) {
      if (n >= items.length) { closeStory(); return; }
      i = Math.max(0, n); p = 0;
      imgs.forEach(function (im, k) { im.classList.toggle("on", k === i); });
      fills.forEach(function (f, k) { f.style.width = k < i ? "100%" : "0"; });
      $("strong", cap).textContent = items[i].title; $("span", cap).textContent = items[i].text;
      if (imgs[i + 1] && !imgs[i + 1].src) imgs[i + 1].src = items[i + 1].full;
    }
    function frame(t) {
      if (!active) return;
      if (last !== null && !hold && !reduced) {
        p += (t - last) / DUR;
        if (p >= 1) show(i + 1); else fills[i].style.width = (p * 100) + "%";
      }
      last = t; requestAnimationFrame(frame);
    }
    function hideStory() {
      active = false; view.classList.remove("open"); document.body.style.overflow = "";
      if (opener) opener.focus({ preventScroll: true });
    }
    function closeStory() { hideStory(); overlayClosed(); }
    openers.forEach(function (b) {
      b.addEventListener("click", function () {
        opener = b;
        var els = $$('[data-full][data-group="' + b.getAttribute("data-group") + '"]');
        items = els.map(function (el) { var th = el.querySelector("img"); return { full: el.getAttribute("data-full"), quick: th && th.complete && th.naturalWidth ? th.currentSrc || th.src : "", title: el.getAttribute("data-title"), text: el.getAttribute("data-text") }; });
        barsEl.innerHTML = ""; imgsEl.innerHTML = ""; fills = []; imgs = [];
        items.forEach(function (it, k) {
          var bar = document.createElement("i"), f = document.createElement("b"); bar.appendChild(f); barsEl.appendChild(bar); fills.push(f);
          var im = document.createElement("img"); im.alt = ""; if (k < 2) im.src = it.quick || it.full;
          if (it.quick) { var hi = new Image(); hi.onload = function () { if (im.src) im.src = it.full; }; hi.src = it.full; }
          imgsEl.appendChild(im); imgs.push(im);
        });
        /* Die Geschichte wächst aus dem Knopf heraus */
        var r = b.getBoundingClientRect();
        view.style.setProperty("--ox", (r.left + r.width / 2) + "px"); view.style.setProperty("--oy", (r.top + r.height / 2) + "px");
        show(0); active = true; last = null; hold = false;
        view.classList.add("open"); document.body.style.overflow = "hidden";
        requestAnimationFrame(frame);
        $(".story-close", view).focus({ preventScroll: true });
        overlayOpened(hideStory);
      });
    });
    $(".story-close", view).addEventListener("click", closeStory);
    /* kurz tippen = blättern, gedrückt halten = Pause (der Balken steht sofort) */
    var downAt = 0;
    $$(".story-zone", view).forEach(function (z) {
      z.addEventListener("pointerdown", function () { hold = true; downAt = performance.now(); card.classList.add("hold"); });
      z.addEventListener("pointerup", function () { hold = false; card.classList.remove("hold"); if (performance.now() - downAt < 250) show(i + (z.classList.contains("next") ? 1 : -1)); });
      z.addEventListener("pointerleave", function () { hold = false; card.classList.remove("hold"); });
      z.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(i + (z.classList.contains("next") ? 1 : -1)); } });
    });
    view.addEventListener("click", function (e) { if (e.target === view) closeStory(); });
    document.addEventListener("keydown", function (e) {
      if (!view.classList.contains("open")) return;
      if (e.key === "Escape") closeStory();
      if (e.key === "ArrowRight") show(i + 1);
      if (e.key === "ArrowLeft") show(i - 1);
      if (e.key === " " && e.target === document.body) { e.preventDefault(); hold = !hold; card.classList.toggle("hold", hold); }
    });
  })();

  /* ---------- Ferienplan drucken ---------- */
  $$(".js-print-plan").forEach(function (b) {
    b.addEventListener("click", function () {
      document.body.classList.add("print-plan");
      $$(".reveal").forEach(function (el) { el.classList.add("visible"); });
      window.print();
    });
  });
  window.addEventListener("afterprint", function () { document.body.classList.remove("print-plan"); });


  /* =====================================================================
     Ideenkatalog 3 – eingebaute Ideen
     ===================================================================== */

  /* ---------- Kleine Feier bei Erfolg (Konfetti in den Farben der Seite) ---------- */
  function confetti(from) {
    if (reduced || !from || !document.body.animate) return;
    var r = from.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    var cols = ["#D4B5B0", "#1E3B44", "#7FD6A4", "#F1E5E3", "#2D6A6A"];
    for (var i = 0; i < 16; i++) {
      var c = document.createElement("span");
      c.className = "confetti" + (i % 3 === 0 ? " round" : "");
      c.style.background = cols[i % cols.length]; c.style.left = cx + "px"; c.style.top = cy + "px";
      document.body.appendChild(c);
      var ang = -Math.PI / 2 + (Math.random() - .5) * 2.2, sp = 60 + Math.random() * 80, dx = Math.cos(ang) * sp, dy = Math.sin(ang) * sp, rot = (Math.random() - .5) * 720;
      c.animate([{ translate: "-50% -50%", rotate: "0deg", opacity: 1 },
        { translate: "calc(-50% + " + dx + "px) calc(-50% + " + dy + "px)", rotate: rot / 2 + "deg", opacity: 1, offset: .45 },
        { translate: "calc(-50% + " + dx * 1.3 + "px) calc(-50% + " + (dy + 110) + "px)", rotate: rot + "deg", opacity: 0 }],
        { duration: 850 + Math.random() * 250, easing: "cubic-bezier(.2,.7,.4,1)" }).onfinish = (function (el) { return function () { el.remove(); }; })(c);
    }
  }

  /* ---------- Termin teilen ---------- */
  $$(".event .share").forEach(function (b) {
    b.addEventListener("click", function () {
      var li = b.closest(".event"), t = li.getAttribute("data-titel"), v = parse(li.getAttribute("data-von")), bis = parse(li.getAttribute("data-ende"));
      var when = li.getAttribute("data-von") === li.getAttribute("data-ende") ? fmtLong(v) : fmt(v) + " – " + fmt(bis);
      var url = new URL("aktuelles.html#termine", location.href).href, text = "Kinderhort Grombühl: " + t + ", " + when;
      function ok(msg) { b.classList.add("done"); setTimeout(function () { b.classList.remove("done"); }, 1800); toast(msg); }
      if (navigator.share) { navigator.share({ title: t, text: text, url: url }).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(text + " – " + url).then(function () { ok("Link zum Termin kopiert"); }, function () { ok("Link: " + url); });
      else ok("Link: " + url);
    });
  });

  /* ---------- Gleitender Knopf in Umschaltern ---------- */
  function slideKnob(group, btn, anim) {
    var k = $(".vs-knob", group); if (!k || !btn) return;
    if (!anim || reduced) k.style.transition = "none";
    k.style.setProperty("--vx", btn.offsetLeft + "px"); k.style.setProperty("--vw", btn.offsetWidth + "px");
    if (!anim || reduced) { void k.offsetWidth; k.style.transition = ""; }
  }

  /* ---------- Termine als Liste oder Kalender (mit Schließtagen) ---------- */
  (function () {
    var sw = $(".view-switch"), cal = $(".month-cal");
    if (!sw || !cal || !K) return;
    var host = sw.closest("section") || document, list = $(".event-list", host), extra = [$(".events-empty", host)];
    var MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
    var now = new Date(), y = now.getFullYear(), m = now.getMonth(), end = parse(K.planEnde), maxI = end.getFullYear() * 12 + end.getMonth(), minI = y * 12 + m;
    K.termine.forEach(function (t) { var d = parse(t.bis); maxI = Math.max(maxI, d.getFullYear() * 12 + d.getMonth()); });
    function evOn(s) { return K.termine.filter(function (t) { return s >= t.von && s <= t.bis && (BEREICH === "alle" || !t.bereich || !t.bereich.length || t.bereich.indexOf(BEREICH) >= 0); }); }
    document.addEventListener("bereich", function () { if (!cal.hidden) render(0); });
    function feierName(s) { for (var i = 0; i < K.feiertage.length; i++) if (K.feiertage[i].datum === s) return K.feiertage[i].name; return null; }
    function render(dir) {
      var first = new Date(y, m, 1), off = (first.getDay() + 6) % 7, n = new Date(y, m + 1, 0).getDate(), cells = "";
      for (var i = 0; i < off; i++) cells += "<span></span>";
      for (var d = 1; d <= n; d++) {
        var dt = new Date(y, m, d), s = iso(dt), wd = dt.getDay(), why = closedReason(dt), evs = evOn(s), cls = [], fe = feierName(s);
        if (wd === 0 || wd === 6) cls.push("we"); if (fe) cls.push("fe"); else if (why && wd !== 0 && wd !== 6) cls.push("zu");
        if (s === heute) cls.push("today");
        var label = d + ". " + MON[m] + (fe ? ", Feiertag: " + fe : why && wd !== 0 && wd !== 6 ? ", geschlossen (" + why + ")" : "") + (evs.length ? ", " + evs.map(function (e) { return e.titel; }).join(", ") : "");
        if (evs.length) cells += '<button type="button" class="ev ' + cls.join(" ") + '" data-d="' + s + '" aria-pressed="false" aria-label="' + escH(label) + '">' + d + "</button>";
        else cells += '<span class="' + cls.join(" ") + '" aria-label="' + escH(label) + '"' + (fe ? ' title="' + escH(fe) + '"' : "") + ">" + d + "</span>";
      }
      var mPre = y + "-" + String(m + 1).padStart(2, "0"), feM = K.feiertage.filter(function (f) { return f.datum.slice(0, 7) === mPre; });
      var i0 = y * 12 + m, zu = K.schliesszeiten.filter(function (z) { var a = z.von.slice(0, 7), b = z.bis.slice(0, 7), c = y + "-" + String(m + 1).padStart(2, "0"); return a <= c && b >= c; });
      cal.innerHTML = '<div class="mc-head"><button type="button" class="mc-prev" aria-label="Voriger Monat"' + (i0 <= minI ? " disabled" : "") + ">" + svg(ICON.left, 20) + "</button><b aria-live=\"polite\">" + MON[m] + " " + y +
        '</b><button type="button" class="mc-next" aria-label="Nächster Monat"' + (i0 >= maxI ? " disabled" : "") + ">" + svg(ICON.right, 20) + "</button></div>" +
        '<div class="mc-wd" aria-hidden="true"><span>Mo</span><span>Di</span><span>Mi</span><span>Do</span><span>Fr</span><span>Sa</span><span>So</span></div><div class="mc-grid">' + cells + "</div>" +
        '<div class="mc-legend"><span><i class="lg-ev"></i>Termin</span><span><i class="lg-zu"></i>geschlossen</span><span><i class="lg-fe"></i>Feiertag</span></div>' +
        '<p class="mc-note" aria-live="polite">' + zu.map(function (z) { return "<b>" + escH(z.name) + ": " + fmt(parse(z.von)) + (z.von === z.bis ? "" : " – " + fmt(parse(z.bis))) + "</b>"; }).join("") +
        feM.map(function (f) { return '<span class="mc-fe">' + escH(f.name) + ": " + fmtLong(parse(f.datum)) + "</span>"; }).join("") + "</p>";
      $(".mc-prev", cal).addEventListener("click", function () { step(-1); });
      $(".mc-next", cal).addEventListener("click", function () { step(1); });
      $$(".ev", cal).forEach(function (b) { b.addEventListener("click", function () {
        $$(".ev", cal).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var mn = $(".mc-note", cal);
        mn.innerHTML = evOn(b.getAttribute("data-d")).map(function (e) { var a = parse(e.von); return "<b>" + escH(e.titel) + "</b>" + (e.von === e.bis ? fmtLong(a) : fmt(a) + " – " + fmt(parse(e.bis))); }).join("");
        if (!reduced && mn.animate) mn.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 150, easing: "ease-out" });
      }); });
      if (dir && !reduced) $(".mc-grid", cal).animate([{ opacity: 0, translate: (dir * 24) + "px 0" }, { opacity: 1, translate: "0 0" }], { duration: 260, easing: "cubic-bezier(.23,1,.32,1)" });
    }
    function step(dd) { var i = y * 12 + m + dd; if (i < minI || i > maxI) return; y = Math.floor(i / 12); m = i % 12; render(dd); var f = $(dd > 0 ? ".mc-next" : ".mc-prev", cal); if (f && !f.disabled) f.focus(); else $(dd > 0 ? ".mc-prev" : ".mc-next", cal).focus(); }
    /* Wischen: das Monatsraster folgt dem Finger, loslassen blättert oder federt zurück */
    var sx = null, sy = 0, drag = false;
    cal.addEventListener("pointerdown", function (e) { if (e.target.closest(".mc-head")) return; sx = e.clientX; sy = e.clientY; drag = false; });
    cal.addEventListener("pointermove", function (e) {
      if (sx === null) return; var dx = e.clientX - sx, g = $(".mc-grid", cal);
      if (!drag && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(e.clientY - sy)) { drag = true; try { cal.setPointerCapture(e.pointerId); } catch (x) {} }
      if (drag && g && !reduced) { var i = y * 12 + m + (dx < 0 ? 1 : -1), edge = i < minI || i > maxI; g.style.translate = (edge ? dx * .25 : dx * .9) + "px 0"; g.style.opacity = 1 - Math.min(.5, Math.abs(dx) / 400); }
    });
    function endDrag(e) {
      if (sx === null) return; var dx = e.clientX - sx, g = $(".mc-grid", cal); sx = null;
      if (!drag) return; drag = false;
      var go = Math.abs(dx) > 50 && !(e.type === "pointercancel");
      var i = y * 12 + m + (dx < 0 ? 1 : -1);
      if (go && i >= minI && i <= maxI) { if (g) { g.style.translate = ""; g.style.opacity = ""; } step(dx < 0 ? 1 : -1); return; }
      if (g) { if (!reduced && g.animate) g.animate([{ translate: g.style.translate || "0 0", opacity: g.style.opacity || 1 }, { translate: "0 0", opacity: 1 }], { duration: 260, easing: EASE_OUT }); g.style.translate = ""; g.style.opacity = ""; }
    }
    cal.addEventListener("pointerup", endDrag); cal.addEventListener("pointercancel", endDrag);
    function show(v, anim) {
      var showCal = v === "cal", out = showCal ? list : cal, inn = showCal ? cal : list;
      if (showCal) render(0);
      var swap = function () { out.hidden = true; inn.hidden = false; extra.forEach(function (x) { if (x && showCal) x.dataset.wasHidden = x.hidden, x.hidden = true; else if (x && x.dataset.wasHidden) x.hidden = x.dataset.wasHidden === "true"; }); };
      if (!anim || reduced || !out.animate) { swap(); return; }
      out.animate([{ opacity: 1 }, { opacity: 0, scale: .98 }], { duration: 120, easing: EASE_OUT }).onfinish = function () { swap(); inn.animate([{ opacity: 0, scale: 1.02 }, { opacity: 1, scale: 1 }], { duration: 240, easing: EASE_OUT }); };
    }
    var btns = $$("button", sw);
    btns.forEach(function (b) { b.addEventListener("click", function () {
      if (b.getAttribute("aria-pressed") === "true") return;
      btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); slideKnob(sw, b, true); show(b.getAttribute("data-view"), true); store("termine-ansicht", b.getAttribute("data-view")); setParam("ansicht", b.getAttribute("data-view") === "cal" ? "kalender" : null);
    }); });
    var want = getParam("ansicht"), pref = (want ? want === "kalender" : store("termine-ansicht") === "cal") ? btns[1] : btns[0];
    btns.forEach(function (x) { x.setAttribute("aria-pressed", x === pref); });
    requestAnimationFrame(function () { slideKnob(sw, pref, false); });
    if (pref === btns[1]) show("cal", false);
    addEventListener("resize", function () { slideKnob(sw, $('[aria-pressed="true"]', sw), false); });
  })();

  /* ---------- Elternbriefe durchsuchen ---------- */
  (function () {
    var inp = document.getElementById("brief-suche"); if (!inp) return;
    var briefe = $$(".brief"), cnt = $(".brief-search .faq-count"), empty = $(".brief-empty");
    function norm(t) { return t.toLowerCase().replace(/ä/g, "a").replace(/ö/g, "o").replace(/ü/g, "u"); }
    briefe.forEach(function (b) { b._orig = $("div", b).innerHTML; b._t = $(".brief-t", b).textContent; });
    function mark(html, q) {
      if (!q) return html;
      return html.replace(/>([^<]+)</g, function (m0, txt) {
        var n = norm(txt), out = "", i = 0, k;
        while ((k = n.indexOf(q, i)) >= 0) { out += txt.slice(i, k) + "<mark>" + txt.slice(k, k + q.length) + "</mark>"; i = k + q.length; }
        return ">" + out + txt.slice(i) + "<";
      });
    }
    inp.addEventListener("input", function () {
      var q = norm(inp.value.trim()), n = 0;
      briefe.forEach(function (b) {
        var hit = !q || norm(b._t + " " + $("div", b).textContent).indexOf(q) >= 0;
        b.hidden = !hit; if (hit) n++;
        $("div", b).innerHTML = mark(b._orig, q); if (q && hit) b.open = true;
      });
      empty.hidden = n > 0; cnt.textContent = q ? n + (n === 1 ? " Brief" : " Briefe") : "";
    });
  })();

  /* ---------- Einblicke: Fotos nach Bereich filtern (weiches Umsortieren) ---------- */
  (function () {
    var chips = $$(".gal-chips button"), grid = $(".gal-grid"); if (!grid) return;
    var items = $$(".gal-item", grid), wechsel = 0;
    chips.forEach(function (c) { c.addEventListener("click", function () {
      if (c.getAttribute("aria-pressed") === "true") return;
      /* ein neuer Klick mitten in der Bewegung lenkt einfach um: Positionen von jetzt messen, dann neu starten */
      clearTimeout(wechsel);
      chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c); });
      var cat = c.getAttribute("data-cat"), keep = function (f) { return cat === "alle" || f.getAttribute("data-cat") === cat; };
      var first = new Map(); items.forEach(function (f) { if (!f.hidden) first.set(f, f.getBoundingClientRect()); });
      items.forEach(function (f) { f.getAnimations().forEach(function (a) { a.cancel(); }); f.classList.remove("leave"); });
      var leaving = items.filter(function (f) { return !f.hidden && !keep(f); });
      if (reduced || !grid.animate) { items.forEach(function (f) { f.hidden = !keep(f); }); return; }
      leaving.forEach(function (f) { f.classList.add("leave"); });
      wechsel = setTimeout(function () {
        items.forEach(function (f) { f.classList.remove("leave"); f.hidden = !keep(f); });
        items.forEach(function (f) {
          if (f.hidden) return; var a = first.get(f), b = f.getBoundingClientRect();
          if (a) f.animate([{ translate: (a.left - b.left) + "px " + (a.top - b.top) + "px" }, { translate: "0 0" }], { duration: 280, easing: EASE_OUT });
          else f.animate([{ opacity: 0, scale: .92 }, { opacity: 1, scale: 1 }], { duration: 220, delay: 40, easing: EASE_OUT, fill: "backwards" });
        });
      }, leaving.length ? 120 : 0);
    }); });
  })();

  /* ---------- Downloads: „neu“ 30 Tage lang ---------- */
  $$(".dl-link .new[data-neu]").forEach(function (n) {
    var a = parse(n.getAttribute("data-neu")), until = new Date(a.getFullYear(), a.getMonth(), a.getDate() + 30);
    n.hidden = new Date() > until;
  });

  /* ---------- Knopf mit Rückmeldung bei Downloads ---------- */
  $$('a[download], .js-saved-ics').forEach(function (a) {
    a.addEventListener("click", function () {
      if (a.classList.contains("got")) return;
      var ic = a.classList.contains("dl-link") ? $(".ficon", a) : null, old = ic ? ic.textContent : null, sv = !ic && $("svg", a), oldSvg = sv ? sv.outerHTML : null;
      a.classList.add("got");
      if (ic) ic.textContent = "✓"; else if (sv) sv.outerHTML = svg(ICON.check, 20);
      setTimeout(function () { a.classList.remove("got"); if (ic) ic.textContent = old; else if (oldSvg) { var s2 = $("svg", a); if (s2) s2.outerHTML = oldSvg; } }, 2200);
    });
  });

  /* ---------- Kalender-Abo: Gerät wählen (Reiter) ---------- */
  (function () {
    var tl = $(".abo-tabs"); if (!tl) return;
    var tabs = $$('[role="tab"]', tl);
    function pick(t, focus, anim) {
      var alt = $$('[role="tab"][aria-selected="true"]', tl).map(function (x) { return document.getElementById(x.getAttribute("aria-controls")); })[0], von = alt && !alt.hidden ? alt.offsetHeight : 0;
      tabs.forEach(function (x) { var on = x === t; x.setAttribute("aria-selected", on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute("aria-controls")).hidden = !on; });
      var neu = document.getElementById(t.getAttribute("aria-controls"));
      if (anim && !reduced && von && neu !== alt && Math.abs(neu.offsetHeight - von) > 2) hoehe(neu, von, neu.offsetHeight, 200, EASE_OUT);
      slideKnob(tl, t, anim); if (focus) t.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { pick(t, false, true); setParam("abo", t.textContent.trim().toLowerCase().split(/\s|\//)[0]); });
      t.addEventListener("keydown", function (e) {
        var j = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : e.key === "Home" ? 0 : e.key === "End" ? tabs.length - 1 : null;
        if (j === null) return; e.preventDefault(); pick(tabs[(j + tabs.length) % tabs.length], true, true);
      });
    });
    var wantTab = getParam("abo"), byParam = wantTab && tabs.filter(function (t) { return t.textContent.trim().toLowerCase().indexOf(wantTab) === 0; })[0];
    var ua = navigator.userAgent, start = byParam ? byParam : /Android/i.test(ua) ? tabs[1] : /iPhone|iPad|Macintosh/.test(ua) ? tabs[0] : /Windows/.test(ua) ? tabs[2] : tabs[0];
    requestAnimationFrame(function () { pick(start, false, false); });
    addEventListener("resize", function () { slideKnob(tl, $('[aria-selected="true"]', tl), false); });
  })();

  /* ---------- Fragen-Helfer: erst eigene Daten (Zeiten, Schließtage, Durchwahlen, Termine …), dann die häufigen Fragen ---------- */
  (function () {
    var box = $(".ask"); if (!box || !K || !K.faq) return;
    var log = $(".ask-log", box), inp = $("#ask-in", box), F = K.faq, dir = durchwahlen();
    var STOP = " der die das und ist ein eine einen mein meine meinem kind kinder wir ich sie es zu in im fuer mit auch noch wie was gibt muss muessen kann koennen hat haben den dem des von auf an bei oder ihr ihre unser unsere wann wo wer sind bitte mir mich man ";
    function stems0(t) { return normDe(t).split(" ").filter(function (w) { return w.length > 2 && STOP.indexOf(" " + w + " ") < 0; }).map(function (w) { return w.length > 5 ? w.slice(0, -2) : w; }); }
    /* Wörter, die Eltern oft anders sagen als die Fragen: jedes Wort einer Gruppe findet auch die anderen */
    var SYN = [["essen", "mittagess", "brotzeit", "fruehstue", "verpflegu", "kueche", "mahlzeit", "snack"], ["schlaf", "mittagssch", "ruhezeit", "ausruh", "muede"],
      ["kost", "gebueh", "beitra", "preis", "bezahl", "geld"], ["windel", "wickel", "toilett", "topf"], ["abhol", "abholzei", "holen"], ["bring", "bringzei", "morgens"],
      ["hausaufga", "lernen", "schule"], ["eingewoeh", "anfang", "erste tag", "start"], ["medikame", "medizin", "tablett", "arznei"], ["allergi", "unvertraeg", "vegetar", "schweine"]];
    function stems(t) {
      var st = stems0(t), plus = [];
      st.forEach(function (w) { SYN.forEach(function (g) { if (g.some(function (x) { return w.indexOf(x) === 0 || x.indexOf(w) === 0; })) g.forEach(function (x) { if (st.indexOf(x) < 0 && plus.indexOf(x) < 0) plus.push(x); }); }); });
      return st.concat(plus);
    }
    function trifft(s, text) { if (text.indexOf(s) >= 0) return 1; if (s.length < 5) return 0; return text.split(" ").some(function (w) { return nah(s, w.slice(0, s.length)); }) ? .7 : 0; }
    function rang(q) {
      var st = stems(q);
      var idf = st.map(function (s) { var df = F.filter(function (f) { return trifft(s, normDe(f.q + " " + f.a)); }).length; return df ? Math.log(1 + F.length / df) : 0; });
      var nq = normDe(q), ber = /krippe/.test(nq) ? "Kinderkrippe" : /garten|kiga/.test(nq) ? "Kindergarten" : /hort|schulkind/.test(nq) ? "Kinderhort" : "";
      return F.map(function (f) { var q2 = normDe(f.q), a2 = normDe(f.a), v = 0; st.forEach(function (s, k) { v += idf[k] * (2 * trifft(s, q2) + trifft(s, a2)); }); if (ber && v && f.b === ber) v *= 1.6; return { f: f, v: v }; })
        .filter(function (x) { return x.v >= 1; }).sort(function (a, b) { return b.v - a.v; })
        .filter(function (x, i, all) { return all.findIndex(function (y) { return y.f.q === x.f.q; }) === i; });
    }
    function el(tag, text, attrs) { var e = document.createElement(tag); if (text) e.textContent = text; for (var k in attrs || {}) e.setAttribute(k, attrs[k]); return e; }
    function link(text, href) { return el("a", text, { href: href }); }
    function z(d) { return fmt(parse(d)); }
    /* Antworten aus den Daten der Seite */
    function eigene(q) {
      var n = " " + normDe(q) + " ", f = document.createDocumentFragment();
      function line(t) { f.appendChild(document.createTextNode(t)); }
      function br() { f.appendChild(el("br")); }
      /* Gruppen im Satz finden: jedes Wort einzeln, Füllwörter zählen nicht */
      var gruppen = dir.filter(function (d) { return !/allgemein/i.test(d.label) && normDe(q).split(" ").some(function (w) { var a = DW_ALIAS[w]; if (a) return /gruppe$/.test(a) && d.keys.some(function (k) { return k.indexOf(a) === 0; }); var gi = w.indexOf("gru"), w2 = gi >= 4 ? w.slice(0, gi) : w; return w2.length >= 4 && d.keys.some(function (k) { return /gruppe$/.test(k) && passt(w2, k.replace(/gruppe$/, "")); }); }); });
      if (/krank|fieber|abmeld| fehlt| nicht kommen|ausfall/.test(n)) {
        line("Bitte melden Sie Ihr Kind möglichst früh am Morgen ab – am schnellsten telefonisch direkt in der Gruppe oder per E-Mail mit unserer Vorlage."); br();
        f.appendChild(link("Kind krankmelden: Gruppe anrufen oder E-Mail", "kontakt.html#schnell")); return f;
      }
      if (/medikament|medizin|tablette|arznei|salbe|zaepfchen|notfallmedi/.test(n)) {
        line("Medikamente dürfen wir nur geben, wenn eine unterschriebene Medikamentenvereinbarung vorliegt."); br();
        f.appendChild(link("Medikamentenvereinbarung (PDF)", "downloads/Medikamentenvereinbarung.pdf")); return f;
      }
      if (/(oma|opa|nachbar|freund|tante|onkel|babysitter|andere person|jemand anders|jemand anderes|abholperson)/.test(n) && /abhol|holt|holen/.test(n)) {
        line("Das geht – schicken Sie uns vorher eine kurze E-Mail mit dem Namen der Person. Sie bringt bitte einen Ausweis mit."); br();
        f.appendChild(link("Abholung ankündigen (E-Mail-Vorlage)", "kontakt.html#schnell")); return f;
      }
      if (/ abwesen| verreis| (im|in den|in) urlaub (ist|sind|fahren|faehrt)| (nicht da|fehlt) (ist|von|vom|bis)| (kind|tochter|sohn) .*(urlaub|verreis|nicht da)/.test(n)) {
        line("Sagen Sie uns kurz Bescheid, von wann bis wann Ihr Kind nicht da ist – dann können wir Personal und Essen planen."); br();
        f.appendChild(link("Abwesenheit melden (E-Mail-Vorlage)", "kontakt.html#schnell")); return f;
      }
      var tagM = n.match(/ (montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag) /), datM = String(q).match(/(\d{1,2})\.\s?(\d{1,2})\.?(\d{2,4})?/);
      if ((tagM || datM) && / offen| geoeffnet| geschlossen| zu | auf | betreu| auf hat| zu hat| kommen/.test(n)) {
        var d = new Date(); d.setHours(12, 0, 0, 0);
        if (datM) { var jj = datM[3] ? +datM[3] : d.getFullYear(); if (jj < 100) jj += 2000; var d2 = new Date(jj, +datM[2] - 1, +datM[1], 12); if (!datM[3] && d2 < d) d2.setFullYear(jj + 1); d = d2; }
        else { var ziel = TAGE.map(normDe).indexOf(tagM[1]); var plus1 = (ziel - d.getDay() + 7) % 7; if (plus1 === 0 && / naechst/.test(n)) plus1 = 7; d.setDate(d.getDate() + plus1); }
        var grund = closedReason(d), wann = TAGE[d.getDay()] + ", " + fmt(d);
        line(grund ? wann + ": geschlossen – " + grund + "." : wann + ": ganz normal geöffnet, ab " + K.oeffnung + " Uhr; Krippe und Kindergarten bis 16:30 Uhr, Hort bis 18:00 Uhr."); return f;
      }
      if (/ kost| gebuehr| beitra| preis| bezahl/.test(n)) {
        line("Zu den Elternbeiträgen beraten wir Sie gern persönlich – rufen Sie uns an oder schreiben Sie uns."); br();
        f.appendChild(link("0931 2789892 0", "tel:+4993127898920")); line(" · "); f.appendChild(link("E-Mail schreiben", "mailto:kinderhort.grombuehl@t-online.de")); return f;
      }
      if (gruppen.length || / telefon| nummer| anruf| durchwahl| erreich/.test(n)) {
        var bArea = /krippe/.test(n) ? "Kinderkrippe" : /garten|kiga/.test(n) ? "Kindergarten" : /hort/.test(n) ? "Kinderhort" : "";
        var hs = gruppen.length ? gruppen : bArea ? dir.filter(function (d) { return d.area === bArea; }) : dir.filter(function (d) { return /allgemein/i.test(d.label); });
        hs.slice(0, 4).forEach(function (d, i) { if (i) br(); line(d.label + " (" + d.area + "): "); f.appendChild(link(d.num, d.href)); });
        if (!gruppen.length) { br(); f.appendChild(link("Alle Durchwahlen", "kontakt.html#durchwahl-finden")); }
        return f;
      }
      if (/ferien|schliess|geschlossen|urlaub|weihnacht|ostern|pfingst|sommer|fasching|herbst/.test(n)) {
        var zs = K.schliesszeiten.filter(function (s) { return s.bis >= heute; }), named = zs.filter(function (s) { return n.indexOf(" " + normDe(s.name).split(" ")[0].slice(0, 5)) >= 0; });
        var pick = named.length ? named : zs.slice(0, 2);
        if (!pick.length) { line("Der Ferienplan für das nächste Kita-Jahr folgt in Kürze."); return f; }
        pick.forEach(function (s, i) { if (i) br(); line(s.name + ": geschlossen " + (s.von === s.bis ? "am " + z(s.von) : "vom " + z(s.von) + " bis " + z(s.bis)) + " (" + s.tage + (s.tage === 1 ? " Schließtag)." : " Schließtage).")); });
        br(); f.appendChild(link("Ganzer Ferienplan", "aktuelles.html#ferienplan")); return f;
      }
      if (/ offen| geoeffnet| oeffnungszeit| bis wann| ab wann| uhrzeit| auf hat| zu hat/.test(n)) {
        if (/ morgen/.test(n)) { var m = new Date(); m.setDate(m.getDate() + 1); var r = closedReason(m); line(r ? "Morgen (" + TAGE[m.getDay()] + ") ist geschlossen – " + r + "." : "Morgen (" + TAGE[m.getDay()] + ") haben wir ganz normal geöffnet: ab " + K.oeffnung + " Uhr, Krippe und Kindergarten bis 16:30 Uhr, Hort bis 18:00 Uhr."); return f; }
        var st = status(); line(st.today + ". " + st.sub); return f;
      }
      if (/platz|anmeld|aufnahme|warteliste|besichtig|kennenlern|bewerb/.test(n)) {
        var ber = /krippe/.test(n) ? ["Kinderkrippe", "kinderkrippe.html"] : /garten|kiga/.test(n) ? ["Kindergarten", "kindergarten.html"] : /hort/.test(n) ? ["Kinderhort", "kinderhort.html"] : null;
        line("Schreiben Sie uns, ab wann Sie einen Platz suchen – gern zeigen wir Ihnen vorher unser Haus."); br();
        f.appendChild(link(ber ? "Platz anfragen: " + ber[0] : "So bekommen Sie einen Platz", ber ? ber[1] + "#anmeldung" : "kinderkrippe.html#anmeldung")); return f;
      }
      if (/termin|elternabend| fest |feier|veranstalt| naechst|ausflug/.test(n)) {
        var ts = K.termine.filter(function (t) { return t.bis >= heute; }).slice(0, 3);
        if (!ts.length) { line("Aktuell stehen keine weiteren Termine an."); return f; }
        line("Die nächsten Termine:"); ts.forEach(function (t) { br(); line("• " + z(t.von) + (t.von !== t.bis ? "–" + z(t.bis) : "") + ": " + t.titel); });
        br(); f.appendChild(link("Alle Termine", "aktuelles.html#termine")); return f;
      }
      if (/ adresse| anfahrt| wo ist| wo sind| wo liegt| parken| bus | strassenbahn| lindlein/.test(n)) {
        line("Lindleinstraße 20, 97080 Würzburg-Grombühl."); br(); f.appendChild(link("Anschrift und Route", "kontakt.html#anschrift")); return f;
      }
      return null;
    }
    function add(cls, node) { var m = document.createElement("div"); m.className = "msg " + cls; if (typeof node === "string") m.textContent = node; else m.appendChild(node); log.appendChild(m); log.scrollTop = log.scrollHeight; return m; }
    function ask(q) {
      add("me", q); vor.innerHTML = "";
      var ty = add("bot typing", document.createDocumentFragment()); ty.innerHTML = "<i></i><i></i><i></i>"; ty.setAttribute("aria-label", "Antwort wird gesucht …");
      setTimeout(function () {
        ty.remove(); var own = eigene(q);
        if (own) { add("bot", own); return; }
        var r = rang(q), frag = document.createDocumentFragment();
        if (r.length) {
          frag.appendChild(document.createTextNode(r[0].f.a));
          frag.appendChild(el("br")); frag.appendChild(link("Aus: „" + r[0].f.q + "“ (" + r[0].f.b + ")", r[0].f.u));
          var more = r.slice(1, 3).filter(function (x) { return x.v >= r[0].v * .5; });
          if (more.length) { var s2 = el("div", "", { class: "sugg" }); more.forEach(function (x) { var b = el("button", x.f.q, { type: "button" }); b.addEventListener("click", function () { ask(x.f.q); }); s2.appendChild(b); }); frag.appendChild(el("p", "Auch passend:", { class: "also" })); frag.appendChild(s2); }
        } else {
          frag.appendChild(document.createTextNode("Dazu habe ich leider nichts gefunden. Rufen Sie uns gern an: "));
          frag.appendChild(link("0931 2789892 0", "tel:+4993127898920"));
        }
        add("bot", frag);
      }, reduced ? 0 : 450);
    }
    /* Vorschläge schon beim Tippen */
    var vor = el("div", "", { class: "ask-vor", "aria-live": "polite" }); $(".ask-form", box).before(vor);
    var vt = null;
    inp.addEventListener("input", function () {
      clearTimeout(vt);
      vt = setTimeout(function () {
        vor.innerHTML = ""; var v = inp.value.trim(); if (v.length < 3) return;
        rang(v).slice(0, 3).forEach(function (x) { var b = el("button", x.f.q, { type: "button" }); b.addEventListener("click", function () { inp.value = ""; ask(x.f.q); }); vor.appendChild(b); });
      }, 180);
    });
    $$(".sugg button", box).forEach(function (b) { b.addEventListener("click", function () { ask(b.textContent); }); });
    $(".ask-form", box).addEventListener("submit", function (e) { e.preventDefault(); var q = inp.value.trim(); if (!q) return; inp.value = ""; ask(q); });
  })();

  /* ---------- Geöffnet-Anzeige in der Leiste ---------- */
  (function () {
    var wrap = $(".open-wrap"); if (!wrap || !K) return;
    var pill = $(".open-pill", wrap), pop = $(".open-pop", wrap), txt = $(".open-txt", wrap);
    function hm(m) { return Math.floor(m / 60) + ":" + String(m % 60).padStart(2, "0"); }
    function update() {
      var now = new Date(), reason = closedReason(now), m = now.getHours() * 60 + now.getMinutes(), o = 405, kk = 990, h = 1080, cls = "", t;
      if (reason) { cls = "closed"; t = "Heute geschlossen"; }
      else if (m < o) { cls = "closed"; t = "Öffnet um 6:45"; }
      else if (m < kk - 30) t = "Geöffnet";
      else if (m < kk) { cls = "soon"; t = "Krippe & Kiga bis 16:30"; }
      else if (m < h - 30) t = "Hort geöffnet";
      else if (m < h) { cls = "soon"; t = "Schließt um 18:00"; }
      else { cls = "closed"; t = "Für heute geschlossen"; }
      pill.className = "open-pill " + cls; txt.textContent = t; pill.setAttribute("aria-label", t + " – Öffnungszeiten anzeigen");
      var rows = [["Kinderkrippe", o, kk], ["Kindergarten", o, kk], ["Kinderhort", o, h]].map(function (r) {
        return '<div class="row' + (!reason && m >= r[2] ? " done" : "") + '"><span>' + r[0] + "</span><b>" + hm(r[1]) + " – " + hm(r[2]) + " Uhr</b></div>"; }).join("");
      var st = status();
      pop.innerHTML = "<strong>" + escH(st.today) + "</strong>" + rows + '<p class="next">' + escH(reason || m >= h ? st.sub : st.next) + "</p>";
    }
    function setOpen(on) {
      pop.hidden = !on; pill.setAttribute("aria-expanded", on);
      if (on) { overlayOpened(function () { setOpen(false); }); } else if (closeTop) overlayClosed();
    }
    pill.addEventListener("click", function () { var on = pop.hidden; if (on) update(); setOpen(on); });
    document.addEventListener("click", function (e) { if (!pop.hidden && !e.target.closest(".open-wrap")) setOpen(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !pop.hidden) { setOpen(false); pill.focus(); } });
    update(); wrap.hidden = false; setInterval(update, 60000);
  })();

  /* Jahreszeiten-Teilchen im Auftakt: entfernt (Design-Review 20.11.2026) */

  /* Nach-oben-Knopf: halbdurchsichtig, solange er über Text liegt (Design-Review 20.11.2026) */
  (function () {
    var b = $(".to-top"); if (!b || !document.elementsFromPoint) return;
    var q = false;
    function pruefe() {
      q = false; if (!b.classList.contains("show")) { b.classList.remove("ueber"); return; }
      var r = b.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2, drauf = false;
      document.elementsFromPoint(x, y).some(function (el) {
        if (el === b || b.contains(el)) return false;
        if (/^(P|LI|H[1-6]|A|SPAN|B|STRONG|SMALL|TD|DT|DD|LABEL|BUTTON|FIGCAPTION)$/.test(el.tagName) && el.textContent.trim()) { drauf = true; return true; }
        return /^(SECTION|MAIN|BODY|HTML|FOOTER)$/.test(el.tagName);
      });
      b.classList.toggle("ueber", drauf);
    }
    addEventListener("scroll", function () { if (!q) { q = true; requestAnimationFrame(pruefe); } }, { passive: true });
  })();

  /* ---------- Handgezeichnete Markierungen zeichnen sich beim Erscheinen ---------- */
  (function () {
    var ms = $$(".mark"); if (!ms.length) return;
    if (!("IntersectionObserver" in window)) { ms.forEach(function (m) { m.classList.add("go"); }); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("go"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -15% 0px" });
    ms.forEach(function (m) { io.observe(m); });
  })();

  /* ---------- Elternstimmen wechseln weich ---------- */
  (function () {
    var box = $(".quotes"); if (!box) return;
    var qs = $$(".quote", box), dots = $$(".q-dots button", box), i = 0;
    function show(n) { i = n; qs.forEach(function (q, k) { q.classList.toggle("on", k === n); q.setAttribute("aria-hidden", k !== n); }); dots.forEach(function (d, k) { d.classList.remove("on"); void d.offsetWidth; d.classList.toggle("on", k === n); d.setAttribute("aria-current", k === n); }); }
    dots.forEach(function (d, k) { d.addEventListener("click", function () { show(k); }); if (!reduced) $("i", d).addEventListener("animationend", function () { show((i + 1) % qs.length); }); });
    show(0);
  })();

  /* Tagesablauf zeichnet sich beim Scrollen: entfernt (Unterseiten-Prüfung 20.11.2026) – die Linie steht fest */

  /* ---------- Gleitender Fokus-Rahmen für die Tastatur ---------- */
  (function () {
    if (!CSS.supports || !CSS.supports("selector(:focus-visible)")) return;
    var ring = document.createElement("div"), cur = null; ring.className = "focus-ring"; ring.setAttribute("aria-hidden", "true"); document.body.appendChild(ring);
    function place(jump) {
      if (!cur) return; var r = cur.getBoundingClientRect(), cs = getComputedStyle(cur), rad = parseFloat(cs.borderTopLeftRadius) || 8;
      ring.classList.toggle("jump", !!jump);
      ring.style.translate = (r.left - 5) + "px " + (r.top - 5) + "px"; ring.style.width = (r.width + 10) + "px"; ring.style.height = (r.height + 10) + "px";
      ring.style.borderRadius = Math.min(rad + 5, (r.height + 10) / 2) + "px";
    }
    document.addEventListener("focusin", function (e) {
      var el = e.target;
      if (!el.matches(":focus-visible") || el.matches("input, textarea, select") || el.closest("dialog, .lightbox, .story-view") || el === document.body) { off(); return; }
      var first = !ring.classList.contains("on"); cur = el.closest(".faq-search, .dial-field, .ask-form, .search-head") || el; place(first || reduced); ring.classList.add("on"); root.classList.add("fring");
    });
    function off() { cur = null; ring.classList.remove("on"); root.classList.remove("fring"); }
    document.addEventListener("focusout", function (e) { if (!e.relatedTarget) off(); });
    document.addEventListener("pointerdown", off, true);
    addEventListener("scroll", function () { if (cur) place(true); }, { passive: true });
    addEventListener("resize", function () { if (cur) place(true); });
  })();

  /* ---------- Wimpel-Ladeanzeige bei langsamem Seitenwechsel ---------- */
  (function () {
    var l = document.createElement("div"); l.className = "nav-loader"; l.setAttribute("role", "status"); l.setAttribute("aria-label", "Seite wird geladen …");
    for (var li = 0; li < 5; li++) { var sp = document.createElement("span"); sp.style.setProperty("--i", li); l.appendChild(sp); }
    document.body.appendChild(l);
  })();

  /* Fotos mit Tiefe beim Scrollen: entfernt (Runde 4, 18.11.2026) – Fotos stehen ruhig */

  /* ---------- Als App auf den Startbildschirm ---------- */
  (function () {
    var deferred = null, links = $$(".js-app"); if (!links.length) return;
    addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); deferred = e; });
    if (matchMedia("(display-mode: standalone)").matches || navigator.standalone) { links.forEach(function (l) { l.closest("li").hidden = true; }); return; }
    var dlg = null;
    function open() {
      if (deferred) { deferred.prompt(); deferred.userChoice.then(function (c) { if (c.outcome === "accepted") toast("Als App gespeichert"); deferred = null; }); return; }
      var ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
      if (!dlg) {
        dlg = document.createElement("dialog"); dlg.className = "app-dialog"; dlg.setAttribute("aria-labelledby", "app-t");
        dlg.innerHTML = '<div><h2 id="app-t"><img src="img/apple-touch-icon.png" alt="" width="48" height="48">Als App aufs Handy</h2><p>Mit einem Symbol auf dem Startbildschirm sind Termine, Krankmelden und Kontakt nur einen Tipp entfernt.</p><ol class="app-steps"></ol><div class="btn-row"><button class="btn btn-primary" type="button" value="ok">Verstanden</button></div></div>';
        document.body.appendChild(dlg);
        $("button", dlg).addEventListener("click", function () { dlg.close(); });
        dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
      }
      $(".app-steps", dlg).innerHTML = ios
        ? "<li>Unten in Safari auf das Teilen-Symbol tippen.</li><li>„Zum Home-Bildschirm“ wählen.</li><li>„Hinzufügen“ antippen – fertig.</li>"
        : "<li>Im Browser das Menü (⋮) öffnen.</li><li>„App installieren“ oder „Zum Startbildschirm hinzufügen“ wählen.</li><li>Bestätigen – fertig.</li>";
      dlg.showModal();
    }
    links.forEach(function (l) { l.addEventListener("click", open); });
  })();


  /* ---------- Mitlaufende Abschnittstitel in langen Abschnitten ---------- */
  (function () {
    var made = [];
    $$("main .section").forEach(function (sec) {
      var h = $(".section-head h2", sec), box = $(".container", sec);
      if (!h || !box || sec.offsetHeight < innerHeight * 1.6) return;
      var st = document.createElement("div"); st.className = "sticky-title"; st.setAttribute("aria-hidden", "true");
      var sp = document.createElement("span"); sp.textContent = h.textContent.replace(/\s+/g, " ").trim(); st.appendChild(sp);
      box.insertBefore(st, box.firstChild); st._h = h; made.push(st);
    });
    if (!made.length) return;
    var sub = $(".subnav"), hdr = $(".site-header");
    function top() {
      var hidden = hdr && hdr.classList.contains("hide"), t;
      var sn = $$(".subnav").filter(function (n) { return n.getClientRects().length; })[0];
      if (sn) t = (parseFloat(getComputedStyle(sn).top) || 0) + sn.offsetHeight + 6; else t = hidden ? 8 : (hdr ? hdr.offsetHeight + 6 : 8);
      made.forEach(function (st) {
        st.style.setProperty("--st-top", Math.max(8, Math.round(t)) + "px");
        /* sichtbar, sobald die eigentliche Überschrift oben verschwunden ist */
        st.classList.toggle("on", st._h.getBoundingClientRect().bottom < t);
      });
    }
    var tick = false;
    addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; top(); }); } }, { passive: true });
    addEventListener("resize", top); document.addEventListener("kopfwechsel", top); top();
  })();

  /* =====================================================================
     Ideenkatalog 3 – Nachtrag 76–88
     ===================================================================== */

  /* ---------- Ferienplan mit Ampel ---------- */
  $$("table.plan tbody tr[data-von]").forEach(function (tr) {
    var von = tr.getAttribute("data-von"), bis = tr.getAttribute("data-bis"), th = $("th", tr), tag = null;
    if (bis < heute) tr.classList.add("past");
    else if (von <= heute) { tr.classList.add("now"); tag = "jetzt geschlossen"; }
    else if (!$("tr.next", tr.parentNode)) {
      tr.classList.add("next");
      var n = Math.round((Date.UTC(+von.slice(0, 4), +von.slice(5, 7) - 1, +von.slice(8, 10)) - Date.UTC(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())) / 864e5);
      tag = n === 1 ? "morgen" : "in " + n + " Tagen";
    }
    if (tag) { var s = document.createElement("span"); s.className = "amp-tag"; s.textContent = tag; th.appendChild(s); }
  });

  /* ---------- Wimpel weichen der Maus aus ---------- */
  (function () {
    var svgEl = $(".site-footer .bunting");
    if (!svgEl || reduced || !matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    var flags = $$(".flag", svgEl), st = flags.map(function (f) { return { el: f, a: 0, v: 0 }; }), running = false, lastX = null;
    function tick() {
      var still = true;
      st.forEach(function (f) { f.v += -f.a * .07; f.v *= .88; f.a += f.v; f.el.style.rotate = f.a.toFixed(2) + "deg"; if (Math.abs(f.v) > .02 || Math.abs(f.a) > .05) still = false; });
      if (still) { running = false; st.forEach(function (f) { f.el.style.rotate = ""; }); return; }
      requestAnimationFrame(tick);
    }
    svgEl.parentNode.addEventListener("pointermove", function (e) {
      var dx = lastX === null ? 0 : e.clientX - lastX; lastX = e.clientX;
      st.forEach(function (f) {
        var r = f.el.getBoundingClientRect(), d = r.left + r.width / 2 - e.clientX, near = 1 - Math.min(1, Math.abs(d) / 80);
        if (near > 0 && e.clientY < r.bottom + 70) f.v += Math.max(-6, Math.min(6, dx * .6)) * near;
      });
      if (!running) { running = true; requestAnimationFrame(tick); }
    });
    svgEl.parentNode.addEventListener("pointerleave", function () { lastX = null; });
  })();

  /* ---------- Foto-Collage neigt sich mit ---------- */
  (function () {
    var hero = $(".hero"), col = $(".hero-collage");
    if (!hero || !col || reduced) return;
    function set(x, y) { col.style.transform = "perspective(1100px) rotateX(" + (-y * 5).toFixed(2) + "deg) rotateY(" + (x * 6).toFixed(2) + "deg)"; }
    if (matchMedia("(hover: hover) and (pointer: fine)").matches) {
      hero.addEventListener("pointermove", function (e) { var r = col.getBoundingClientRect(); set(Math.max(-.5, Math.min(.5, (e.clientX - r.left) / r.width - .5)), Math.max(-.5, Math.min(.5, (e.clientY - r.top) / r.height - .5))); });
      hero.addEventListener("pointerleave", function () { set(0, 0); });
    } else if ("DeviceOrientationEvent" in window && typeof DeviceOrientationEvent.requestPermission !== "function") {
      /* Android: Neigen des Handys; iPhone bräuchte eine Erlaubnis-Abfrage – darauf verzichten wir bewusst */
      var tickO = false;
      addEventListener("deviceorientation", function (e) {
        if (e.gamma == null || tickO || scrollY > innerHeight) return; tickO = true;
        requestAnimationFrame(function () { tickO = false; set(Math.max(-.5, Math.min(.5, e.gamma / 50)), Math.max(-.5, Math.min(.5, ((e.beta || 45) - 45) / 60))); });
      });
    }
  })();

  /* ---------- Route mit der eigenen Karten-App ---------- */
  $$(".js-route").forEach(function (a) {
    var apple = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
    if (apple) { a.href = "https://maps.apple.com/?daddr=Lindleinstra%C3%9Fe%2020%2C%2097080%20W%C3%BCrzburg"; $("span", a).textContent = "Route mit Apple Karten"; }
    else $("span", a).textContent = "Route mit Google Maps";
  });

  /* ---------- Ferienplan als Jahresposter drucken ---------- */
  $$(".js-poster").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!K) return;
      var end = parse(K.planEnde), y1 = end.getFullYear() - 1, MN = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
      var feier = {}; K.feiertage.forEach(function (f) { feier[f.datum] = f.name; });
      var h = "<h1>Schließtage " + y1 + "/" + (y1 + 1) + "</h1><p class=\"sub\">Kath. Kinder- und Jugendhort Grombühl · Kinderkrippe, Kindergarten und Kinderhort</p><div class=\"months\">";
      for (var k = 0; k < 12; k++) {
        var y = k < 4 ? y1 : y1 + 1, m = (8 + k) % 12, off = (new Date(y, m, 1).getDay() + 6) % 7, n = new Date(y, m + 1, 0).getDate();
        var g = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"].map(function (w) { return '<span class="wd">' + w + "</span>"; }).join("");
        for (var i = 0; i < off; i++) g += "<span></span>";
        for (var d = 1; d <= n; d++) {
          var dt = new Date(y, m, d), s = iso(dt), wd = dt.getDay(), we = wd === 0 || wd === 6;
          var zu = !we && K.schliesszeiten.some(function (z) { return s >= z.von && s <= z.bis; });
          g += '<span class="' + (we ? "we" : feier[s] ? "f" : zu ? "z" : "") + '">' + d + "</span>";
        }
        h += '<div class="mo"><b>' + MN[m] + " " + y + '</b><div class="g">' + g + "</div></div>";
      }
      var total = K.schliesszeiten.reduce(function (a, z) { return a + z.tage; }, 0);
      h += '</div><div class="leg"><span><i></i>Schließtag</span><span class="f-num">12</span><span>= Feiertag</span><span>' + total + ' Schließtage im Kita-Jahr</span></div><p class="foot">Stand: ' + fmt(new Date()) + " · Alle Termine aktuell auf der Webseite unter „Aktuelles“</p>";
      var box = document.createElement("div"); box.className = "poster-print"; box.innerHTML = h; document.body.appendChild(box);
      document.body.classList.add("print-poster");
      var done = function () { document.body.classList.remove("print-poster"); box.parentNode && box.parentNode.removeChild(box); window.removeEventListener("afterprint", done); };
      window.addEventListener("afterprint", done);
      window.print();
    });
  });
  /* ---------- Schnelle Wiederbesuche ---------- */
  if ("serviceWorker" in navigator && /^https?:$/.test(location.protocol)) {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () { /* ohne geht es auch */ }); });
  }

  /* ==========================================================
     Abstimmung 15.11.: Design-Kniffe, Ideen 91–109, Übergänge
     ========================================================== */
  var finePtr = matchMedia("(hover: hover) and (pointer: fine)").matches;
  function seen(els, fn, margin) {
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) { els.forEach(fn); return; }
    var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { o.unobserve(e.target); fn(e.target); } }); }, { rootMargin: margin || "0px 0px -12% 0px" });
    els.forEach(function (el) { o.observe(el); });
  }

  /* Übergang 2, 7, 36, 48 – Richtung des Seitenwechsels */
  (function () {
    var ORDER = ["index", "kinderkrippe", "kindergarten", "kinderhort", "aktuelles", "downloads", "kontakt"];
    var EXTRA = ["impressum", "datenschutz", "404"];
    function nameOf(u) { var m = /([^\/]*?)(?:\.html)?(?:[?#].*)?$/.exec(new URL(u, location.href).pathname); return (m && m[1]) || "index"; }
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]"); if (!a) return;
      try { sessionStorage.setItem("vt-hoch", a.closest(".cta-band, [data-vt='hoch']") ? "1" : ""); } catch (x) {}
    });
    window.addEventListener("pagereveal", function (e) {
      if (!e.viewTransition) return;
      var from = null, back = false;
      try { from = navigation.activation.from && navigation.activation.from.url; back = navigation.activation.navigationType === "traverse" && navigation.activation.entry.index < navigation.activation.from.index; } catch (x) {}
      if (!from) return;
      var a = nameOf(from), b = nameOf(location.href), ia = ORDER.indexOf(a), ib = ORDER.indexOf(b), type = "";
      var hoch = false; try { hoch = sessionStorage.getItem("vt-hoch") === "1"; sessionStorage.removeItem("vt-hoch"); } catch (x) {}
      if (a === b) type = "";
      else if (EXTRA.indexOf(b) >= 0) type = "karte";
      else if (EXTRA.indexOf(a) >= 0) type = "karte-zu";
      else if (hoch && !back) type = "hoch";
      else if (ia >= 0 && ib >= 0) type = (ib > ia) !== back ? "vor" : "zurueck";
      if (back && type === "vor") type = "zurueck";
      if (!type) return;
      root.setAttribute("data-vt", type);
      e.viewTransition.finished.finally(function () { root.removeAttribute("data-vt"); });
    });
  })();

  /* Kniff 6 – weiche Kanten an Wischreihen */
  (function () {
    var els = $$(".subnav ul, .tour-track, .table-wrap, .gal-chips");
    function upd(el) {
      var max = el.scrollWidth - el.clientWidth;
      if (max < 2) { el.classList.remove("edge-mask"); return; }
      el.classList.add("edge-mask");
      el.style.setProperty("--ml", el.scrollLeft > 2 ? "16px" : "0px");
      el.style.setProperty("--mr", el.scrollLeft < max - 2 ? "16px" : "0px");
    }
    els.forEach(function (el) { el.addEventListener("scroll", function () { upd(el); }, { passive: true }); upd(el); });
    addEventListener("resize", function () { els.forEach(upd); });
    addEventListener("load", function () { els.forEach(upd); });
  })();

  /* Kniff 7 + Übergang 32 – Symbole tauschen weich, Häkchen zeichnet sich */
  function checkSvg(size) { return svg('<path pathLength="1" d="M5 12.5l4.5 4.5L19 7.5"/>', size).replace("<svg ", '<svg class="swap-in draw-check" '); }
  $$(".event .save").forEach(function (b) {
    b.addEventListener("click", function () { setTimeout(function () { var s = $(".b svg", b); if (s && b.classList.contains("on")) { s.outerHTML = checkSvg(16); } }, 0); });
  });
  $$(".event .share").forEach(function (b) {
    var ok = document.createElement("span"); ok.innerHTML = checkSvg(20).replace('class="swap-in draw-check"', 'class="ic-ok swap-in draw-check"'); b.appendChild(ok.firstChild);
    new MutationObserver(function () { var s = $(".ic-ok", b); if (b.classList.contains("done") && s) { var n = s.cloneNode(true); s.replaceWith(n); } }).observe(b, { attributes: true, attributeFilter: ["class"] });
  });
  $$('a[download], .js-saved-ics').forEach(function (a) {
    a.addEventListener("click", function () { setTimeout(function () { if (!a.classList.contains("got")) return; var s = $("svg", a); if (s) s.outerHTML = checkSvg(20); }, 0); });
  });
  if (toggle) toggle.addEventListener("click", function () { toggle.classList.add("swapping"); setTimeout(function () { toggle.classList.remove("swapping"); }, 200); });

  /* Idee 91 – Fragen nach Themen filtern */
  (function () {
    var faq = $(".faq"), input = faq && $("#faq-suche", faq); if (!input) return;
    var T = [["Essen", /verpflegung|brotzeit|essen|mittag|trink/], ["Zeiten & Ferien", /ferien|abhol|schließtag|geöffnet|uhr/], ["Eingewöhnung", /eingewöhn|sauber|windel|schlaf|kirche/], ["Alltag", /hausaufgab|konzept|gruppen|krank/]];
    var items = $$("details", faq), on = null;
    T = T.filter(function (t) { return items.filter(function (d) { return t[1].test(d.textContent.toLowerCase()); }).length >= 1; });
    if (T.length < 2) return;
    var box = document.createElement("div"); box.className = "faq-topics reveal visible"; box.setAttribute("role", "group"); box.setAttribute("aria-label", "Fragen nach Thema");
    box.innerHTML = '<button type="button" aria-pressed="true">Alle</button>' + T.map(function (t, i) { return '<button type="button" aria-pressed="false" data-t="' + i + '">' + t[0] + "</button>"; }).join("");
    $(".faq-search", faq).after(box);
    function apply() {
      var before = new Map(); items.forEach(function (d) { if (!d.hidden) before.set(d, d.getBoundingClientRect()); });
      input.dispatchEvent(new Event("input"));
      var n = 0;
      items.forEach(function (d) { if (on && !on[1].test(d.textContent.toLowerCase())) d.hidden = true; if (!d.hidden) n++; });
      $(".faq-empty", faq).hidden = n > 0;
      $(".faq-count", faq).textContent = on || input.value.trim() ? n + (n === 1 ? " Frage" : " Fragen") : "";
      if (reduced) return;
      items.forEach(function (d) {
        if (d.hidden) return; var a = before.get(d), b = d.getBoundingClientRect();
        if (!a) d.animate([{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }], { duration: 250, easing: EASE_OUT });
        else if (Math.abs(a.top - b.top) > 1) d.animate([{ transform: "translateY(" + (a.top - b.top) + "px)" }, { transform: "none" }], { duration: 300, easing: EASE_OUT });
      });
    }
    $$("button", box).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("button", box).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        on = b.dataset.t ? T[+b.dataset.t] : null; apply(); setParam("thema", on ? on[0].toLowerCase().split(" ")[0] : null);
      });
    });
    var wantT = getParam("thema");
    if (wantT) $$("button", box).forEach(function (b) { if (b.dataset.t && T[+b.dataset.t][0].toLowerCase().indexOf(wantT) === 0) b.click(); });
    input.addEventListener("input", function (e) { if (e.isTrusted && on) setTimeout(function () { items.forEach(function (d) { if (!on[1].test(d.textContent.toLowerCase())) d.hidden = true; }); }, 0); });
  })();

  /* Idee 92 (Karten kippen zur Maus) entfernt: Feinschliff 18.11.2026 */

  /* Idee 97 – Hinweis ohne Internet */
  (function () {
    var n = document.createElement("div"); n.className = "offline-note"; n.setAttribute("role", "status"); n.innerHTML = "<i></i><span></span>"; document.body.appendChild(n);
    var t = null;
    function show(txt, back) { clearTimeout(t); $("span", n).textContent = txt; n.classList.toggle("back", !!back); n.classList.add("show"); if (back) t = setTimeout(function () { n.classList.remove("show"); }, 2500); }
    addEventListener("offline", function () { show("Kein Internet – Sie sehen die zuletzt gespeicherte Fassung."); });
    addEventListener("online", function () { show("Wieder verbunden", true); });
    if (navigator.onLine === false) show("Kein Internet – Sie sehen die zuletzt gespeicherte Fassung.");
  })();

  /* Idee 106 – Leitsatz schreibt sich beim ersten Besuch */
  (function () {
    var ls = $(".leitsatz"); if (!ls || reduced || store("leitsatz")) return;
    store("leitsatz", "1");
    var n = 0, mark = $(".mark", ls);
    (function wrap(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) { var f = document.createDocumentFragment(); c.textContent.split("").forEach(function (ch) { var s = document.createElement("span"); s.className = "ch"; s.style.setProperty("--n", n++); s.textContent = ch; f.appendChild(s); }); c.replaceWith(f); }
        else if (c.nodeType === 1 && c.tagName !== "svg") wrap(c);
      });
    })(ls);
    ls.setAttribute("aria-label", "Weil Qualität zählt!");
    if (mark) { mark.classList.add("hold"); }
    requestAnimationFrame(function () { ls.classList.add("typing"); });
    setTimeout(function () { if (mark) { mark.classList.remove("hold"); mark.classList.add("go"); } }, n * 22 + 150);
    /* danach wieder normaler Text (Vorlesen, Kopieren) */
    setTimeout(function () { $$(".ch", ls).forEach(function (c) { c.replaceWith(c.textContent); }); ls.normalize(); ls.classList.remove("typing"); ls.removeAttribute("aria-label"); }, n * 22 + 400);
  })();

  /* Idee 101 – Welle bewegt sich kurz, wenn der Fußbereich erscheint (höchstens 5 s) */
  if (!reduced) seen($$(".foot-wave"), function (w) { w.classList.add("go"); }, "0px");

  /* „Das zeichnet uns aus“: weitere Punkte auf Wunsch */
  $$(".fx-more").forEach(function (b) {
    var g = b.previousElementSibling; b.hidden = false;
    b.addEventListener("click", function () { g.classList.add("all"); b.remove(); var f = $(".fx", g); if (f) f.setAttribute("tabindex", "-1"), f.focus({ preventScroll: true }); });
  });

  /* Idee 107 – Schwung unter der Unterschrift */
  seen($$(".sig-swash"), function (el) { el.classList.add("go"); });

  /* Idee 109 – im Bereichsmenü blättern die Fotos */
  (function () {
    if (reduced) return;
    var t = null, cur = null;
    function stop() { clearInterval(t); t = null; if (cur) $$(".mv-x", cur).forEach(function (x) { x.classList.remove("on"); }); cur = null; }
    function start(fig) {
      if (cur === fig) return; stop(); cur = fig;
      var xs = $$(".mv-x", fig), i = -1; if (!xs.length) return;
      t = setInterval(function () { xs.forEach(function (x) { x.classList.remove("on"); }); i = (i + 1) % (xs.length + 1); if (i < xs.length) xs[i].classList.add("on"); }, 1800);
    }
    $$(".mega-col").forEach(function (col) {
      var k = (/c-(\w+)/.exec(col.className) || [])[1]; if (!k) return;
      col.addEventListener("mouseenter", function () { var f = $(".mega-visual .v-" + k); if (f) start(f); });
    });
    $$(".mega").forEach(function (m) { m.addEventListener("mouseleave", stop); });
  })();

  /* Übergang 16 – Inhalt gleitet in die Richtung des Reiters */
  (function () {
    $$(".abo-tabs").forEach(function (tl) {
      var tabs = $$('[role="tab"]', tl), last = null;
      tabs.forEach(function (t, i) {
        t.addEventListener("click", function () { slideTo(i); });
        t.addEventListener("keydown", function () { setTimeout(function () { slideTo(tabs.indexOf($('[aria-selected="true"]', tl))); }, 0); });
      });
      function slideTo(i) {
        if (last === null) last = tabs.indexOf($('[aria-selected="true"]', tl));
        if (i === last || reduced) { last = i; return; }
        var p = document.getElementById(tabs[i].getAttribute("aria-controls"));
        p.classList.remove("slide-from-r", "slide-from-l"); void p.offsetWidth; p.classList.add(i > last ? "slide-from-r" : "slide-from-l"); last = i;
      }
    });
    var vs = $(".view-switch");
    if (vs) $$("button", vs).forEach(function (b, i) {
      b.addEventListener("click", function () {
        if (reduced) return;
        setTimeout(function () { var hs = vs.closest("section") || document, p = i === 0 ? $(".event-list", hs) : $(".month-cal", hs); if (!p || p.hidden) return; p.classList.remove("slide-from-r", "slide-from-l"); void p.offsetWidth; p.classList.add(i ? "slide-from-r" : "slide-from-l"); }, 0);
      });
    });
  })();

  /* Übergang 17 – Fenster wächst aus dem Knopf */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".js-app"); if (!b) return;
    setTimeout(function () { var d = $(".app-dialog"); if (!d) return; var r = b.getBoundingClientRect(), q = d.getBoundingClientRect(); d.style.setProperty("--from", Math.round(r.left + r.width / 2 - q.left) + "px " + Math.round(r.top + r.height / 2 - q.top) + "px"); }, 0);
  }, true);

  /* Übergang 19 – Bereichskopf: Bilder wechseln mit langsamer Kamerafahrt */
  (function () {
    var card = $(".page-hero:not(.simple) .page-hero-card"), main = card && $(":scope > img", card);
    var pics = $$("#rundgang .tour-item img").slice(0, 4);
    if (!main || pics.length < 2 || reduced) return;
    var layers = pics.map(function (p) { var im = document.createElement("img"); im.className = "kb"; im.alt = ""; im.setAttribute("aria-hidden", "true"); im.decoding = "async"; im.dataset.src = p.currentSrc || p.src; im.dataset.srcset = p.getAttribute("srcset") || ""; im.sizes = "100vw"; main.after(im); return im; });
    var i = -1, t = null;
    main.classList.add("cam");
    function next() {
      var nx = (i + 1) % layers.length, im = layers[nx];
      if (!im.src) { if (im.dataset.srcset) im.srcset = im.dataset.srcset; im.src = im.dataset.src; }
      function go() { layers.forEach(function (l) { l.classList.remove("on"); }); void im.offsetWidth; im.classList.add("on"); i = nx; }
      if (im.complete && im.naturalWidth) go(); else im.addEventListener("load", go, { once: true });
    }
    var paused = false, pb = document.createElement("button");
    pb.type = "button"; pb.className = "kb-pause"; pb.setAttribute("aria-pressed", "false"); pb.setAttribute("aria-label", "Bildwechsel anhalten");
    pb.innerHTML = '<svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg><svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.9l10-6.5a1 1 0 0 0 0-1.7l-10-6.6A1 1 0 0 0 8 5.5z"/></svg>';
    card.appendChild(pb);
    pb.addEventListener("click", function () { paused = !paused; pb.setAttribute("aria-pressed", paused); pb.setAttribute("aria-label", paused ? "Bildwechsel fortsetzen" : "Bildwechsel anhalten"); card.classList.toggle("kb-off", paused); run(!paused); });
    function run(on) { clearInterval(t); t = on && !paused ? setInterval(next, 6500) : null; }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { run(es[0].isIntersecting && !document.hidden); }).observe(card);
    document.addEventListener("visibilitychange", function () { run(!document.hidden && card.getBoundingClientRect().bottom > 0); });
  })();

  /* Übergang 25 – kurze Texte steigen Zeile für Zeile auf */
  (function () {
    var ps = $$(".section-head > p"); if (!ps.length || reduced) return;
    seen(ps, function (p) {
      var html = p.innerHTML, words = p.textContent.trim().split(/\s+/);
      if (p.children.length) return;
      p.innerHTML = words.map(function (w) { return "<span class=\"w\">" + w.replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }) + "</span>"; }).join(" ");
      var lines = [], top = null;
      $$(".w", p).forEach(function (s) { if (s.offsetTop !== top) { lines.push([]); top = s.offsetTop; } lines[lines.length - 1].push(s.textContent); });
      p.innerHTML = lines.map(function (l) { return '<span class="ln"><span>' + l.join(" ").replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }) + "</span></span>"; }).join("");
      $$(".ln > span", p).forEach(function (sp, n) { sp.style.setProperty("--n", n); });
      setTimeout(function () { p.innerHTML = html; }, 600 + lines.length * 60);
    }, "0px 0px -10% 0px");
  })();

  /* Übergang 35 – Strich wandert im Menü mit */
  (function () {
    var ul = $(".main-nav > ul"), hi = $(".header-inner"); if (!ul || !hi || !finePtr) return;
    var line = document.createElement("span"); line.className = "nav-line"; line.setAttribute("aria-hidden", "true"); hi.appendChild(line);
    function to(el) {
      if (!el || innerWidth <= 1180) { line.style.opacity = 0; return; }
      var r = el.getBoundingClientRect(), u = hi.getBoundingClientRect(), pad = 16;
      line.style.top = (r.bottom - u.top - 6) + "px"; line.style.bottom = "auto";
      line.style.scale = (r.width - pad * 2) + " 1"; line.style.translate = (r.left - u.left + pad) + "px 0"; line.style.opacity = 1;
    }
    $$(":scope > li > a:not(.nav-cta), :scope > li > .drop-toggle", ul).forEach(function (a) { a.addEventListener("mouseenter", function () { to(a); }); });
    ul.addEventListener("mouseleave", function () { line.style.opacity = 0; });
  })();

  /* Übergang 44 – Kopfleiste wird Pixel für Pixel fester */
  (function () {
    if (!header) return; var raf = 0;
    function upd() { raf = 0; header.style.setProperty("--hp", Math.min(1, Math.max(0, scrollY / 160)).toFixed(3)); }
    addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true }); upd();
  })();

  /* Übergang 45 – Wörter rollen um, wenn sich die Geöffnet-Anzeige ändert */
  (function () {
    var txt = $(".open-txt"); if (!txt || reduced) return;
    var last = txt.textContent, busy = false;
    new MutationObserver(function () {
      if (busy) return; var now = txt.textContent; if (now === last || !last) { last = now; return; }
      last = now; busy = true;
      txt.innerHTML = '<span class="roll-word">' + now.split("").map(function (c) { return '<span class="rc">' + (c === " " ? "&nbsp;" : escH(c)) + "</span>"; }).join("") + "</span>";
      $$(".rc", txt).forEach(function (sp, n) { sp.style.setProperty("--n", n); });
      setTimeout(function () { txt.textContent = now; busy = false; }, 400 + now.length * 18);
    }).observe(txt, { childList: true, characterData: true, subtree: true });
  })();

  /* Übergang 51 – Linie zeichnet sich unter Abschnittsköpfen */
  seen($$(".section-head"), function (el) { el.classList.add("drawn"); });

  /* Übergang 52 – Fotos des Rundgangs erscheinen als Welle */
  (function () {
    var tr = $$(".tour-track"); if (reduced) return;
    tr.forEach(function (t) { t.classList.add("wave-wait"); $$(".tour-item", t).forEach(function (it, i) { it.style.setProperty("--w", Math.min(i, 6)); }); });
    seen(tr, function (t) { t.classList.add("wave-go"); requestAnimationFrame(function () { t.classList.remove("wave-wait"); }); setTimeout(function () { t.classList.remove("wave-go"); }, 1200); }, "0px 0px -15% 0px");
  })();

  /* Übergang 53 – Seitentitel erscheint klein in der Leiste.
     Immer den Titel der gerade sichtbaren Seite nehmen (die Vorschau hat alle Seiten in einer Datei). */
  (function () {
    var brand = $(".brand"); if (!brand || !header) return;
    var t = document.createElement("span"); t.className = "b-page"; t.setAttribute("aria-hidden", "true"); brand.appendChild(t);
    var raf = 0;
    function upd() {
      raf = 0;
      var h = $$(".page-hero h1").filter(function (x) { return x.offsetParent !== null; })[0];
      var on = false;
      if (h) { var r = h.getBoundingClientRect(); on = r.height > 0 && r.bottom < 80; if (on && t.textContent !== h.textContent.trim()) t.textContent = h.textContent.trim(); }
      header.classList.toggle("show-page", on);
    }
    function later() { if (!raf) raf = requestAnimationFrame(upd); }
    addEventListener("scroll", later, { passive: true });
    addEventListener("hashchange", function () { header.classList.remove("show-page"); setTimeout(upd, 50); });
    addEventListener("resize", later);
    upd();
  })();

  /* Übergang 58 – Platzhalter atmen, wenn ein Bild länger als 1 s braucht */
  (function () {
    if (reduced) return;
    seen($$("img[loading=lazy]"), function (im) {
      if (im.complete && im.naturalWidth) return;
      var t = setTimeout(function () { if (!im.complete) im.classList.add("wait"); }, 1000);
      im.addEventListener("load", function () { clearTimeout(t); if (im.classList.contains("wait")) { im.classList.remove("wait"); im.classList.add("arrived"); } }, { once: true });
    }, "0px");
  })();

  /* ==========================================================
     Ideenkatalog 4 – Ja-Ideen (16.11.)
     ========================================================== */

  /* 3 Kurzbefehl „Kind krankmelden“: Abschnitt öffnen und zeigen */
  (function () { var k = $("#krankmelden");
    /* alte Links „…#krankmelden“ (Startseite, App-Verknüpfung) führen jetzt zur Kontaktseite */
    if (!k) { if (location.hash === "#krankmelden") location.replace("kontakt.html#schnell"); return; }
    function go() { if (location.hash === "#krankmelden") { k.open = true; k.scrollIntoView({ block: "center" }); $("summary", k).focus({ preventScroll: true }); } }
    go(); addEventListener("hashchange", go);
    /* Link „Kind krankmelden“ im Startbereich: auch beim zweiten Klick (Sprungmarke schon gesetzt) aufklappen */
    document.addEventListener("click", function (e) { var a = e.target.closest && e.target.closest(".hero-krank"); if (a) k.open = true; }); })();

  /* 4 Neu seit Ihrem letzten Besuch (nur im eigenen Browser) */
  (function () {
    var ref = null; try { ref = sessionStorage.getItem("besuch-ref"); } catch (e) {}
    if (ref === null) { ref = store("besuch") || ""; try { sessionStorage.setItem("besuch-ref", ref); } catch (e) {} }
    store("besuch", heute);
    if (!ref) return;   /* erster Besuch: nichts ist „neu“ */
    $$("[data-neu]").forEach(function (el) {
      if (el.getAttribute("data-neu") <= ref) return;
      el.classList.add("is-new");
      var t = el.matches(".event") ? $("strong", el) : $(".brief-t", el);
      if (t && !$(".new-tag", t)) { var s = document.createElement("span"); s.className = "new-tag"; s.textContent = "neu"; t.appendChild(s); }
    });
  })();

  /* 5 Hinweise verschwinden am Tag danach */
  $$(".hint[data-tag]").forEach(function (h) { if (h.getAttribute("data-tag") < heute) h.hidden = true; });

  /* 9 Ruhige Ansicht: Bewegung aus (gemerkt im eigenen Browser) */
  (function () {
    var calm = store("ruhig") === "1";
    if (calm) reduced = true;
    $$(".js-calm").forEach(function (b) {
      b.setAttribute("aria-checked", calm);
      b.textContent = calm ? "Bewegung an" : "Bewegung aus";
      b.addEventListener("click", function () {
        calm = !calm; store("ruhig", calm ? "1" : null); root.classList.toggle("calm", calm); reduced = calm || matchMedia("(prefers-reduced-motion: reduce)").matches;
        $$(".js-calm").forEach(function (x) { x.setAttribute("aria-checked", calm); x.textContent = calm ? "Bewegung an" : "Bewegung aus"; });
        toast(calm ? "Bewegung ausgeschaltet" : "Bewegung eingeschaltet");
      });
    });
    addEventListener("pagereveal", function (e) { if (e.viewTransition && root.classList.contains("calm")) e.viewTransition.skipTransition(); });
  })();

  /* 6 Termin zur Seite wischen = merken (nur Touch) */
  (function () {
    if (!matchMedia("(pointer: coarse)").matches) return;
    $$(".event-list").forEach(function (ul) {
      var under = document.createElement("span"); under.className = "swipe-under"; under.setAttribute("aria-hidden", "true"); ul.appendChild(under);
      $$(".event", ul).forEach(function (li) {
        var x0 = null, y0 = null, dx = 0, lock = null;
        li.addEventListener("pointerdown", function (e) { if (e.pointerType !== "touch" || e.target.closest("button, a")) return; x0 = e.clientX; y0 = e.clientY; dx = 0; lock = null; });
        li.addEventListener("pointermove", function (e) {
          if (x0 === null) return; var mx = e.clientX - x0, my = e.clientY - y0;
          if (lock === null && (Math.abs(mx) > 8 || Math.abs(my) > 8)) lock = Math.abs(mx) > Math.abs(my) && mx > 0 ? "x" : "y";
          if (lock !== "x") return;
          if (!li.classList.contains("swiping")) { li.classList.add("swiping"); try { li.setPointerCapture(e.pointerId); } catch (x) {}
            var on = $(".save", li).classList.contains("on"); under.textContent = on ? "Nicht mehr merken" : "Merken";
            under.style.top = li.offsetTop + "px"; under.style.height = li.offsetHeight + "px"; under.classList.add("show"); }
          dx = Math.max(0, mx); var w = li.offsetWidth, x = dx > w * .6 ? w * .6 + rubber(dx - w * .6, 40) : dx;
          li.style.translate = x + "px 0"; under.classList.toggle("ready", dx > w * .4);
        });
        function end() {
          if (x0 === null) return; x0 = null;
          if (li.classList.contains("swiping")) {
            li.classList.remove("swiping"); li.style.transition = "translate .3s " + EASE_OUT; li.style.translate = "0 0";
            setTimeout(function () { li.style.transition = ""; under.classList.remove("show", "ready"); }, 300);
            if (dx > li.offsetWidth * .4) $(".save", li).click();
          }
        }
        li.addEventListener("pointerup", end); li.addEventListener("pointercancel", end);
      });
    });
  })();

  /* 37 Spürbares Merken: kurzes Vibrieren beim Merken (Android) */
  $$(".event .save").forEach(function (b) { b.addEventListener("click", function () { if (b.classList.contains("on") && navigator.vibrate && !reduced) { try { navigator.vibrate(10); } catch (e) {} } }); });

  /* 22 Merkliste als Blatt von unten */
  (function () {
    var btns = $$(".js-saved-sheet"); if (!btns.length) return;
    var dlg = document.createElement("dialog"); dlg.className = "saved-sheet"; dlg.setAttribute("aria-labelledby", "ss-t");
    dlg.innerHTML = '<div class="ss-grip" aria-hidden="true"></div><h2 id="ss-t">Gemerkte Termine</h2><ul class="ss-list"></ul><p class="ss-empty" hidden>Noch nichts gemerkt.</p><div class="btn-row"><button class="btn btn-primary ss-ics" type="button">' + svg(ICON.calendar, 20) + ' Alle in den Kalender</button><button class="btn btn-ghost ss-close" type="button">Schließen</button></div>';
    document.body.appendChild(dlg);
    var src = null;
    function fill() {
      var list = savedList(), ul = $(".ss-list", dlg), seen = {}; ul.innerHTML = "";
      $$(".event[data-von]", src).forEach(function (li) {
        var k = $(".save", li).getAttribute("data-key"); if (list.indexOf(k) < 0 || seen[k]) return; seen[k] = 1;
        var row = document.createElement("li"), t = document.createElement("span"), d = document.createElement("small"), x = document.createElement("button");
        t.textContent = li.getAttribute("data-titel"); d.textContent = fmtLong(parse(li.getAttribute("data-von")));
        x.type = "button"; x.className = "ss-del"; x.setAttribute("aria-label", li.getAttribute("data-titel") + " nicht mehr merken"); x.innerHTML = svg(ICON.x, 18);
        x.addEventListener("click", function () {
          $(".save", li).click();
          var fertig = function () { row.remove(); if (!$("li", ul)) $(".ss-empty", dlg).hidden = false; };
          if (reduced) { fertig(); return; }
          row.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 140, fill: "forwards" });
          row.animate([{ paddingTop: getComputedStyle(row).paddingTop, paddingBottom: getComputedStyle(row).paddingBottom }, { paddingTop: "0px", paddingBottom: "0px" }], { duration: 200, easing: EASE_OUT, fill: "forwards" });
          hoehe(row, row.offsetHeight, 0, 200, EASE_OUT, fertig);
        });
        var tx = document.createElement("div"); tx.append(t, d); row.append(tx, x); ul.appendChild(row);
      });
      $(".ss-empty", dlg).hidden = !!$("li", ul);
    }
    function close() { dlg.classList.add("closing"); setTimeout(function () { dlg.classList.remove("closing"); dlg.close(); }, reduced ? 0 : 200); }
    btns.forEach(function (b) { b.addEventListener("click", function () { src = b.closest("section") || document; fill(); dlg.showModal(); }); });
    $(".ss-close", dlg).addEventListener("click", close);
    $(".ss-ics", dlg).addEventListener("click", function () { var s = $(".js-saved-ics", src); if (s) s.click(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
    /* nach unten ziehen schließt */
    var y0 = null;
    dlg.addEventListener("pointerdown", function (e) { if (!e.target.closest(".ss-grip, h2")) return; y0 = e.clientY; dlg.style.transition = "none"; dlg.setPointerCapture(e.pointerId); });
    dlg.addEventListener("pointermove", function (e) { if (y0 === null) return; var dy = e.clientY - y0; dlg.style.translate = "0 " + (dy > 0 ? dy : -rubber(-dy, 20)) + "px"; });
    function up(e) { if (y0 === null) return; var dy = e.clientY - y0; y0 = null; dlg.style.transition = ""; dlg.style.translate = ""; if (dy > 80) close(); }
    dlg.addEventListener("pointerup", up); dlg.addEventListener("pointercancel", up);
  })();

  /* 23 „Was passiert jetzt?“ nach Platz anfragen / Kennenlernen */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="mailto:"]'); if (!a) return;
    var h = decodeURIComponent(a.getAttribute("href")); if (!/Platzanfrage|Kennenlernen/.test(h)) return;
    var box = a.parentNode.querySelector(".next-steps"); if (box) return;
    box = document.createElement("div"); box.className = "next-steps"; box.setAttribute("role", "status");
    box.innerHTML = "<b>So geht es weiter</b><ol><li>Ihr E-Mail-Programm öffnet die vorbereitete Nachricht.</li><li>Sie ergänzen die Angaben und senden sie ab.</li><li>Wir melden uns bei Ihnen.</li></ol>";
    a.after(box);
  });

  /* 24 Kurz gefragt: morgen, nächste Woche, nächste Ferien */
  $$(".status-ask").forEach(function (box) {
    var out = $(".status-a", box);
    function day(d) { return TAGE[d.getDay()]; }
    $$("button", box).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("button", box).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var now = new Date(), q = b.dataset.q, t;
        if (q === "morgen") { var m = new Date(now); m.setDate(m.getDate() + 1); var r = closedReason(m); t = r ? "Nein, morgen (" + day(m) + ") ist geschlossen – " + r + "." : "Ja, morgen (" + day(m) + ") haben wir ganz normal geöffnet."; }
        else if (q === "woche") {
          var mo = new Date(now); mo.setDate(mo.getDate() + ((8 - mo.getDay()) % 7 || 7)); var zu = [];
          for (var i = 0; i < 5; i++) { var x = new Date(mo); x.setDate(mo.getDate() + i); var rr = closedReason(x); if (rr) zu.push(day(x) + " (" + rr + ")"); }
          t = zu.length ? "Nächste Woche geschlossen: " + zu.join(", ") + "." : "Ja, die ganze nächste Woche (ab " + fmt(mo) + ") ist offen.";
        } else {
          var nx = (K && K.schliesszeiten || []).filter(function (z) { return z.bis >= heute; })[0];
          t = nx ? (nx.von <= heute ? "Gerade ist Schließzeit (" + nx.name + ") bis " + fmt(parse(nx.bis)) + "." : nx.name + ": geschlossen " + (nx.von === nx.bis ? "am " + fmt(parse(nx.von)) : "vom " + fmt(parse(nx.von)) + " bis " + fmt(parse(nx.bis))) + ".") : "Der nächste Ferienplan folgt in Kürze.";
        }
        var von = out.offsetHeight; out.textContent = t;
        if (!reduced && out.animate) {
          hoehe(out, von, out.offsetHeight, 220, EASE_OUT);
          out.animate([{ opacity: 0, translate: "0 4px" }, { opacity: 1, translate: "0 0" }], { duration: 200, easing: EASE_OUT });
        }
      });
    });
  });




  /* ---------- Weiches Auf- und Zuklappen (Krankmelden, Formular-Lotse, Elternbriefe, Fragen) ----------
     Läuft per Skript, damit es auch in Safari geht. Ohne Skript oder mit „Bewegung reduzieren“ klappen die Kästen wie gewohnt sofort. */
  function sanft(d, o) {
    var s = $("summary", d); if (!s || d.dataset.sanft) return; d.dataset.sanft = "1";
    var inner = Array.prototype.filter.call(d.children, function (c) { return c.tagName !== "SUMMARY"; }), lauf = null, zu = false;
    var g = d.getAttribute("name"); if (g) { d.removeAttribute("name"); d.dataset.gruppe = g; }
    function fade(keys, opt) { inner.forEach(function (c) { c.getAnimations().forEach(function (a) { a.cancel(); }); c.animate(keys, opt); }); }
    function fahre(bis, fertig) {
      var von = d.getBoundingClientRect().height;
      if (lauf) { lauf.onfinish = null; lauf.cancel(); }
      d.style.overflow = "hidden";
      lauf = d.animate([{ height: von + "px" }, { height: bis + "px" }], { duration: o.ms, easing: o.ease });
      lauf.onfinish = function () { lauf = null; d.style.overflow = ""; if (fertig) fertig(); };
    }
    d.sanftAuf = function () {
      var von = d.getBoundingClientRect().height; zu = false;
      if (lauf) { lauf.onfinish = null; lauf.cancel(); }
      d.open = true; var bis = d.getBoundingClientRect().height;
      d.style.height = von + "px"; void d.offsetHeight; d.style.height = "";
      fade([{ opacity: 0 }, { opacity: 1 }], { duration: o.ms * .75, delay: o.ms * (o.spaet || .15), easing: "ease-out", fill: "backwards" });
      d.style.overflow = "hidden";
      lauf = d.animate([{ height: von + "px" }, { height: bis + "px" }], { duration: o.ms, easing: o.ease });
      lauf.onfinish = function () { lauf = null; d.style.overflow = ""; };
    };
    d.sanftZu = function () {
      zu = true;
      fade([{ opacity: 1 }, { opacity: 0 }], { duration: o.ms * (o.ausblenden || .5), easing: EASE_OUT, fill: "forwards" });
      fahre(s.getBoundingClientRect().height + (d.offsetHeight - d.clientHeight), function () {
        zu = false; d.open = false; inner.forEach(function (c) { c.getAnimations().forEach(function (a) { a.cancel(); }); });
      });
    };
    s.addEventListener("click", function (e) {
      if (reduced) return;
      e.preventDefault();
      if (d.open && !zu) { d.sanftZu(); return; }
      if (d.dataset.gruppe) $$('details[data-gruppe="' + d.dataset.gruppe + '"]').forEach(function (x) { if (x !== d && x.open && x.sanftZu) x.sanftZu(); });
      d.sanftAuf();
    });
  }
  var EIO = "cubic-bezier(.77,0,.175,1)";
  $$(".krank").forEach(function (d) { sanft(d, { ms: 250, ease: EIO }); });
  /* Lotse: ruhiger – etwas länger, weichere Kurve, Inhalt geht zuerst und kommt zuletzt */
  $$(".lotse-item").forEach(function (d) { sanft(d, { ms: 480, ease: "cubic-bezier(.45,0,.25,1)", spaet: .3, ausblenden: .4 }); });
  $$(".brief").forEach(function (d) { sanft(d, { ms: 350, ease: EIO }); });
  $$(".faq details").forEach(function (d) { sanft(d, { ms: 380, ease: EIO }); });

  /* ---------- Termine nach Bereich: Termine fürs ganze Haus bleiben immer sichtbar ---------- */
  var BEREICH = "alle";
  (function () {
    var box = $(".ev-filter"); if (!box) return;
    var list = $("#termine .event-list"), leer = $("#termine .ev-filter-empty");
    var busy = false;
    $$("button", box).forEach(function (b) { b.addEventListener("click", function () {
      if (busy || b.getAttribute("aria-pressed") === "true") return;
      BEREICH = b.getAttribute("data-b");
      $$("button", box).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      var evs = $$(".event", list), n = 0;
      function raus(ev) { var bs = (ev.getAttribute("data-bereich") || "").split(" ").filter(Boolean); return BEREICH !== "alle" && bs.length && bs.indexOf(BEREICH) < 0; }
      function sichtbar(ev) { return !ev.hidden && !ev.classList.contains("bf-out") && ev.getClientRects().length; }
      function anwenden() {
        evs.forEach(function (ev) { var aus = raus(ev); ev.classList.toggle("bf-out", !!aus); if (!aus && !ev.hidden && (ev.getAttribute("data-bereich") || "")) n++; });
        if (leer) leer.hidden = BEREICH === "alle" || n > 0;
        document.dispatchEvent(new CustomEvent("bereich"));
      }
      if (reduced || !list.animate || list.hidden) { anwenden(); return; }
      /* gehende blenden aus, übrige gleiten an ihren neuen Platz, kommende blenden ein */
      busy = true;
      var vorher = new Map(); evs.forEach(function (ev) { if (sichtbar(ev)) vorher.set(ev, ev.getBoundingClientRect()); });
      var gehen = evs.filter(function (ev) { return sichtbar(ev) && raus(ev); });
      gehen.forEach(function (ev) { ev.animate([{ opacity: 1, scale: 1 }, { opacity: 0, scale: .97 }], { duration: 150, easing: "ease-out", fill: "forwards" }); });
      setTimeout(function () {
        gehen.forEach(function (ev) { ev.getAnimations().forEach(function (a) { a.cancel(); }); });
        anwenden();
        evs.forEach(function (ev) {
          if (!sichtbar(ev)) return; var a = vorher.get(ev), r = ev.getBoundingClientRect();
          if (a) { if (Math.abs(a.top - r.top) > 1) ev.animate([{ translate: "0 " + (a.top - r.top) + "px" }, { translate: "0 0" }], { duration: 300, easing: EASE_OUT }); }
          else ev.animate([{ opacity: 0, scale: .97 }, { opacity: 1, scale: 1 }], { duration: 220, delay: 80, easing: EASE_OUT, fill: "backwards" });
        });
        busy = false;
      }, gehen.length ? 150 : 0);
    }); });
  })();

  /* ---------- Krankmelden mit einem Tipp: zuletzt angerufene Gruppe steht oben ---------- */
  (function () {
    var bloecke = $$(".krank"); if (!bloecke.length) return;
    function zeige() {
      var g = null; try { g = JSON.parse(store("krank-gruppe") || "null"); } catch (e) {}
      if (!g || typeof g.name !== "string" || !/^tel:\+?\d{6,16}$/.test(g.href || "")) g = null;
      bloecke.forEach(function (k) {
        var alt = $(".krank-last", k); if (alt) alt.parentNode.removeChild(alt);
        if (!g || !$('.krank-area a[href="' + g.href + '"]', k)) return;
        var a = document.createElement("a"); a.className = "btn btn-primary krank-last"; a.href = g.href;
        a.innerHTML = svg(ICON.phone, 20) + "<span></span>"; $("span", a).textContent = g.name + " anrufen";
        var body = $(".krank-body", k); body.insertBefore(a, $(".krank-groups", k));
        var sm = $("summary small", k); if (sm) { sm.dataset.orig = sm.dataset.orig || sm.textContent; sm.textContent = "Zuletzt: " + g.name; }
      });
    }
    bloecke.forEach(function (k) { $$('.krank-area a[href^="tel:"]', k).forEach(function (a) { a.addEventListener("click", function () {
      var name = a.textContent.replace(/….*$/, "").trim(); store("krank-gruppe", JSON.stringify({ name: name, href: a.getAttribute("href") })); setTimeout(zeige, 400);
    }); }); });
    zeige();
  })();

  /* ---------- Wimpelkette im Jahreslauf: leise Farben je Jahreszeit (nur Farbtöne) ---------- */
  (function () {
    var flags = $$(".bunting .flag"); if (!flags.length) return;
    var mo = new Date().getMonth(), P = mo >= 2 && mo <= 4 ? ["#A8C5C0", "#E8D9B5", "#D4B5B0", "#F3F8F7"]
      : mo >= 5 && mo <= 7 ? ["#D4B5B0", "#F3F8F7", "#8CC2B5", "#E8D9B5"]
      : mo >= 8 && mo <= 10 ? ["#D4B5B0", "#C9926F", "#A8C5C0", "#E3C6B8"]
      : ["#F3F8F7", "#A8C5C0", "#D4B5B0", "#B9CDD0"];
    document.documentElement.dataset.jahreszeit = ["winter", "winter", "fruehling", "fruehling", "fruehling", "sommer", "sommer", "sommer", "herbst", "herbst", "herbst", "winter"][mo];
    flags.forEach(function (f, i) { f.setAttribute("fill", P[i % P.length]); });
  })();

  /* ---------- Fehlt ein Foto, bleibt es ruhig: Muster in Salbei mit dem Namen ---------- */
  (function () {
    function fail(img) {
      if (img.dataset.fehlt) return; img.dataset.fehlt = "1";
      var box = img.parentNode && img.parentNode.tagName === "PICTURE" ? img.parentNode.parentNode : img.parentNode; if (!box) return;
      var name = img.getAttribute("alt") || (box.querySelector("figcaption") ? "" : "Foto folgt");
      img.classList.add("img-fehlt"); box.classList.add("img-ersatz");
      if (name) box.setAttribute("data-ersatz", name);
    }
    $$("img").forEach(function (img) {
      if (img.closest(".brand, .toast") || img.getAttribute("aria-hidden") === "true") return;
      if (img.complete && img.getAttribute("src") && img.naturalWidth === 0) fail(img);
      img.addEventListener("error", function () { fail(img); });
    });
  })();

  /* ---------- Am Computer: Telefonnummer kopieren statt wählen ---------- */
  (function () {
    if (!matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    function nummer(a) { var t = a.textContent.replace(/\s+/g, " ").trim(); return /\d{4}/.test(t) && /^[\d\s+/()-]+$/.test(t) ? t : a.getAttribute("href").replace(/^tel:/, "").replace(/^\+49/, "0"); }
    $$('a[href^="tel:"]').forEach(function (a) { a.classList.add("tel-copy"); if (!a.title) a.title = "Klicken zum Kopieren: " + nummer(a); });
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href^="tel:"]'); if (!a || e.ctrlKey || e.metaKey || e.shiftKey) return;
      e.preventDefault();
      var n = nummer(a), ok = function () { toast("Nummer kopiert: " + n); }, no = function () { toast("Nummer: " + n); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(n.replace(/\s/g, " ")).then(ok, no); else no();
    });
  })();

  /* ---------- Elternbrief teilen und drucken ---------- */
  $$(".js-brief-share").forEach(function (b) {
    b.addEventListener("click", function () {
      var br = b.closest(".brief"), t = $(".brief-t", br).textContent, url = location.href.split("#")[0] + "#" + br.id;
      if (navigator.share) { navigator.share({ title: t, text: "Elternbrief: " + t, url: url }).catch(function () {}); return; }
      var ok = function () { toast("Link zum Elternbrief kopiert"); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok, function () { toast(url); }); else toast(url);
    });
  });
  $$(".js-brief-print").forEach(function (b) {
    b.addEventListener("click", function () {
      var br = b.closest(".brief"), box = document.createElement("div");
      box.className = "brief-print";
      box.innerHTML = '<p class="bp-org">Kath. Kinder- und Jugendhort Grombühl · Lindleinstraße 20 · 97080 Würzburg</p><h1></h1><p class="bp-stand"></p>' + $("div", br).innerHTML;
      $("h1", box).textContent = $(".brief-t", br).textContent; $(".bp-stand", box).textContent = $("summary small", br) ? $("summary small", br).textContent : "";
      $$(".brief-acts, mark", box).forEach(function (x) { if (x.tagName === "MARK") x.outerHTML = x.innerHTML; else x.parentNode.removeChild(x); });
      document.body.appendChild(box); document.body.classList.add("print-brief");
      var done = function () { document.body.classList.remove("print-brief"); if (box.parentNode) box.parentNode.removeChild(box); removeEventListener("afterprint", done); };
      addEventListener("afterprint", done);
      window.print();
    });
  });
  /* Link auf einen Brief öffnet ihn */
  (function () { var h = location.hash.slice(1); if (!/^brief-/.test(h)) return; var br = document.getElementById(h); if (br && br.tagName === "DETAILS") br.open = true; })();

  /* ---------- Tag der offenen Tür / Info-Abend: Band auf der Startseite, sechs Wochen vorher ---------- */
  (function () {
    var hero = $(".hero"); if (!hero || !K || !K.termine) return;
    var heuteD = new Date(), bis = new Date(heuteD.getFullYear(), heuteD.getMonth(), heuteD.getDate() + 42), h = iso(heuteD), b = iso(bis);
    var t = K.termine.filter(function (x) { return /offene[nrs]?\s+t(ü|ue)r|info(rmations)?[\s-]?abend|schnupper|kennenlern/i.test(x.titel) && x.bis >= h && x.von <= b; })[0];
    if (!t) return;
    var a = parse(t.von), z = parse(t.bis), datum = t.von === t.bis ? fmtLong(a) : fmt(a) + " – " + fmt(z);
    var sec = document.createElement("section"); sec.className = "open-day"; sec.setAttribute("aria-label", t.titel);
    sec.innerHTML = '<div class="container open-day-inner"><div><span class="eyebrow"></span><h2></h2><p class="od-text"></p></div><div class="btn-row"><button class="btn btn-primary od-ics" type="button">' + svg(ICON.calendar, 20) + ' Im Kalender speichern</button><a class="btn btn-ghost" href="aktuelles.html#termine">Alle Termine</a></div></div>';
    $(".eyebrow", sec).textContent = t.titel; $("h2", sec).textContent = datum; $(".od-text", sec).textContent = (t.text || "").replace(/\*\*/g, "");
    hero.parentNode.insertBefore(sec, hero.nextSibling);
    $(".od-ics", sec).addEventListener("click", function () {
      var d1 = t.von.replace(/-/g, ""), e2 = parse(t.bis); e2.setDate(e2.getDate() + 1);
      var stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+/, "");
      var txt = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kinderhort Grombuehl//DE", "BEGIN:VEVENT", "UID:offene-tuer-" + d1 + "@kinderhort-grombuehl.de", "DTSTAMP:" + stamp,
        "DTSTART;VALUE=DATE:" + d1, "DTEND;VALUE=DATE:" + iso(e2).replace(/-/g, ""), "SUMMARY:" + icsEsc(t.titel), "DESCRIPTION:" + icsEsc((t.text || "").replace(/\*\*/g, "")),
        "LOCATION:" + icsEsc("Lindleinstraße 20, 97080 Würzburg"), "END:VEVENT", "END:VCALENDAR"].join("\r\n");
      var url = URL.createObjectURL(new Blob([txt], { type: "text/calendar" })), l = document.createElement("a");
      l.href = url; l.download = "tag-der-offenen-tuer.ics"; document.body.appendChild(l); l.click(); l.parentNode.removeChild(l);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000); toast("Kalenderdatei erstellt");
    });
  })();


  /* ---------- Diese Woche auf einen Blick (Startseite): Termine, Schließtage, Feiertage Mo–Fr ---------- */
  (function () {
    var box = $("[data-woche]"); if (!box || !K) return;
    var KURZ = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"], MON = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
    var versatz = 0, MAX = 30;
    function fe(s) { for (var i = 0; i < K.feiertage.length; i++) if (K.feiertage[i].datum === s) return K.feiertage[i].name; return null; }
    function zu(s) { for (var i = 0; i < K.schliesszeiten.length; i++) { var z = K.schliesszeiten[i]; if (s >= z.von && s <= z.bis) return z; } return null; }
    function kurz(d) { return String(d.getDate()).padStart(2, "0") + "." + String(d.getMonth() + 1).padStart(2, "0") + "."; }
    function zeige(richtung) {
      var jetzt = new Date(), m = new Date(jetzt.getFullYear(), jetzt.getMonth(), jetzt.getDate());
      /* am Wochenende zeigt „Diese Woche“ schon die kommende Woche */
      if (m.getDay() === 6) m.setDate(m.getDate() + 2); else if (m.getDay() === 0) m.setDate(m.getDate() + 1);
      m.setDate(m.getDate() - ((m.getDay() + 6) % 7) + versatz * 7);
      var fr = new Date(m); fr.setDate(m.getDate() + 4);
      var titel = versatz === 0 ? (jetzt.getDay() === 0 || jetzt.getDay() === 6 ? "Kommende Woche" : "Diese Woche") : versatz === 1 ? "Nächste Woche" : "Woche ab " + kurz(m);
      var tage = "";
      for (var i = 0; i < 5; i++) {
        var d = new Date(m); d.setDate(m.getDate() + i); var s = iso(d), e = "", f = fe(s), z = zu(s);
        if (f) e += '<span class="wo-e fe"><small>Feiertag</small>' + escH(f) + "</span>";
        else if (z) e += '<span class="wo-e zu"><small>geschlossen</small>' + escH(z.name) + "</span>";
        K.termine.forEach(function (t) { if (s >= t.von && s <= t.bis) e += '<span class="wo-e wo-t">' + escH(t.titel) + "</span>"; });
        tage += '<li class="wo-tag' + (s === heute ? " heute" : "") + '"' + (s === heute ? ' aria-current="date"' : "") + '><span class="wo-d">' + KURZ[d.getDay()] + " " + d.getDate() + ".<small>" + MON[d.getMonth()] + "</small></span><span class=\"wo-ein\">" + (e || '<span class="wo-frei">geöffnet</span>') + "</span></li>";
      }
      box.innerHTML = '<div class="wo-kopf"><button class="wo-pfeil" type="button" aria-label="Vorige Woche"' + (versatz <= 0 ? " disabled" : "") + ">" + svg(ICON.left, 20) + '</button><h3 aria-live="polite">' + titel + ' <span>' + kurz(m) + " – " + kurz(fr) + '</span></h3><button class="wo-pfeil" type="button" aria-label="Nächste Woche"' + (versatz >= MAX ? " disabled" : "") + ">" + svg(ICON.right, 20) + '</button></div><ul class="wo-tage">' + tage + "</ul>";
      var p = $$(".wo-pfeil", box);
      p[0].addEventListener("click", function () { if (versatz > 0) { versatz--; zeige(-1); $$(".wo-pfeil", box)[versatz > 0 ? 0 : 1].focus(); } });
      p[1].addEventListener("click", function () { if (versatz < MAX) { versatz++; zeige(1); $$(".wo-pfeil", box)[1].focus(); } });
      if (richtung && !reduced) $(".wo-tage", box).animate([{ opacity: 0, translate: (richtung * 16) + "px 0" }, { opacity: 1, translate: "0 0" }], { duration: 240, easing: EASE_OUT });
    }
    zeige(0);
  })();

  /* Leiste „Auf dieser Seite“: beim Scrollen da, kurz nach dem Anhalten ausgeblendet (nur wenn sie oben klebt) */
  $$(".subnav").forEach(function (nav) {
    var t = 0, PAUSE = 1400;
    function klebt() { var r = nav.getBoundingClientRect(); return r.height > 0 && r.top <= parseFloat(getComputedStyle(nav).top) + 1; }
    function ruhe() { if (klebt() && !nav.matches(":hover, :focus-within")) nav.classList.add("ruht"); }
    function spaeter() { clearTimeout(t); t = setTimeout(ruhe, PAUSE); }
    function wach(e) { if (e && e.target && e.target.nodeType === 1 && nav.contains(e.target)) return; nav.classList.remove("ruht"); spaeter(); }
    document.addEventListener("scroll", wach, { passive: true, capture: true });
    nav.addEventListener("mouseleave", spaeter);
    nav.addEventListener("focusin", function () { nav.classList.remove("ruht"); });
    nav.addEventListener("focusout", spaeter);
  });

  /* Symbol-Knöpfe ohne sichtbaren Text: Beschriftung auch als Hinweis beim Darüberfahren */
  $$("button[aria-label], a[aria-label]").forEach(function (el) { if (!el.title && !el.textContent.trim()) el.title = el.getAttribute("aria-label"); });

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
