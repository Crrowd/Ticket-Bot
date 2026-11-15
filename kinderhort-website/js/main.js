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
    return '<svg width="' + (size || 20) + '" height="' + (size || 20) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + "</svg>";
  }
  var ICON = {
    x: '<path d="M6 6l12 12M18 6L6 18"/>', left: '<path d="M15 5l-7 7 7 7"/>', right: '<path d="M9 5l7 7-7 7"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>', search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.8-3.8"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'
  };
  /* Gummiband: hinter einer Grenze folgt das Element dem Finger mit wachsendem Widerstand */
  function rubber(x, d) { var s = x < 0 ? -1 : 1; x = Math.abs(x); return s * (1 - 1 / (x * 0.55 / d + 1)) * d; }
  var EASE_IO = "cubic-bezier(.65, 0, .35, 1)", EASE_OUT = "cubic-bezier(.23, 1, .32, 1)";
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
  function onScroll() {
    if (!header) return;
    var y = window.scrollY, dy = y - lastY;
    lastY = y;
    header.classList.toggle("scrolled", y > 8);
    if (y < 120 || busy()) { header.classList.remove("hide"); travel = 0; return; }
    /* erst nach ein paar Pixeln in dieselbe Richtung reagieren – kein Flackern bei kleinen Bewegungen */
    travel = (travel > 0) === (dy > 0) ? travel + dy : dy;
    if (travel > 24) header.classList.add("hide");
    else if (travel < -12) header.classList.remove("hide");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (header) header.addEventListener("focusin", function () { header.classList.remove("hide"); });

  /* Handy-Tastatur: Höhe messen, damit nichts unter ihr verschwindet */
  var vv = window.visualViewport;
  function onViewport() {
    var kb = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop));
    root.style.setProperty("--kb", kb + "px");
    root.style.setProperty("--vvh", Math.round(vv.height) + "px");
    root.classList.toggle("kb-open", kb > 80);
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
      var open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function () {
    $$(".has-drop.open").forEach(function (li) {
      if (document.body.classList.contains("nav-open")) return;
      li.classList.remove("open");
      $(".drop-toggle", li).setAttribute("aria-expanded", "false");
    });
  });

  /* ---------- Sprungmarken: aktuellen Abschnitt hervorheben ---------- */
  /* Ein Marker für alle Einträge, der von Punkt zu Punkt gleitet */
  function knobTo(ul, a) {
    var k = $(".subnav-knob", ul), first = !k;
    if (first) { k = document.createElement("li"); k.className = "subnav-knob"; k.setAttribute("aria-hidden", "true"); ul.insertBefore(k, ul.firstChild); }
    var moved = !first && k.style.getPropertyValue("--kx") !== a.offsetLeft + "px";
    if (first) k.style.transition = "none";
    k.style.setProperty("--kx", a.offsetLeft + "px");
    k.style.setProperty("--ky", a.offsetTop + "px");
    k.style.setProperty("--kw", a.offsetWidth + "px");
    k.style.setProperty("--kh", a.offsetHeight + "px");
    if (first) { void k.offsetWidth; k.style.transition = ""; k.classList.add("on"); }
    else if (moved && !reduced) { k.classList.remove("moving"); void k.offsetWidth; k.classList.add("moving"); }
  }
  window.addEventListener("resize", function () {
    $$(".subnav ul").forEach(function (ul) { var a = $('a[aria-current="true"]', ul), k = $(".subnav-knob", ul); if (a && k) { k.style.transition = "none"; knobTo(ul, a); void k.offsetWidth; k.style.transition = ""; } });
  });
  var subLinks = $$(".subnav a");
  if (subLinks.length && "IntersectionObserver" in window) {
    var pairs = [];
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = pairs.filter(function (p) { return p[0] === en.target; })[0][1], ul = a.closest("ul");
        $$("a", ul).forEach(function (l) { l.removeAttribute("aria-current"); });
        a.setAttribute("aria-current", "true");
        knobTo(ul, a);
        /* nur verschieben, wenn der aktive Eintrag nicht ganz zu sehen ist – dann mittig */
        if (a.offsetLeft < ul.scrollLeft || a.offsetLeft + a.offsetWidth > ul.scrollLeft + ul.clientWidth)
          ul.scrollTo({ left: a.offsetLeft - (ul.clientWidth - a.offsetWidth) / 2, behavior: reduced ? "auto" : "smooth" });
      });
    }, { rootMargin: "-140px 0px -65% 0px" });
    subLinks.forEach(function (a) {
      var id = a.getAttribute("href").split("#").pop().split(":").pop();
      var sec = (a.closest(".spa-page") || document).querySelector('[id="' + id + '"]');
      if (sec) { pairs.push([sec, a]); spy.observe(sec); }
    });
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
      track.animate([{ translate: "0 0" }, { translate: (dir * 18) + "px 0" }, { translate: "0 0" }], { duration: 360, easing: EASE_OUT });
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
  function show(i, dir) {
    zoomReset();
    var prev = lbImg.classList.contains("ready") && lb.classList.contains("open") ? lbImg.getBoundingClientRect() : null;
    if (prev && !reduced) {
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
    if (prev && dir && !reduced) lbImg.animate([{ opacity: 0, transform: "translateX(" + dir * 24 + "px)" }, { opacity: 1, transform: "none" }], { duration: 250, easing: EASE_OUT });
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
    if (e.key === "ArrowLeft") show(idx - 1, -1);
    if (e.key === "ArrowRight") show(idx + 1, 1);
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
  function recentList() { try { return JSON.parse(store("zuletzt") || "[]"); } catch (e) { return []; } }
  function remember(t, sub, u) {
    if (!t || !u) return;
    var l = recentList().filter(function (r) { return r.u !== u; });
    l.unshift({ t: t, s: sub || "", u: u }); store("zuletzt", JSON.stringify(l.slice(0, 6)));
  }
  (function () {
    var page = location.pathname.split("/").pop() || "index.html", h1 = $("main h1");
    if (page === "404.html" || !h1) return;
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
      '<input type="text" id="suche" role="combobox" aria-expanded="true" aria-haspopup="listbox" aria-autocomplete="list" aria-controls="suchliste" aria-label="Suchbegriff" placeholder="Wonach suchen Sie? z. B. Ferien, krank, Telefon" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search">' +
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
        var oft = ["Kind krankmelden", "Kontakt & Durchwahlen", "Aktuelle Termine", "Ferienplan & Schließtage", "Platz anfragen", "Downloads"];
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
    var render = function () {
      hits = search(input.value);
      sel = 0;
      input.setAttribute("aria-expanded", hits.length ? "true" : "false");
      if (hits.length) input.setAttribute("aria-activedescendant", "treffer-0"); else input.removeAttribute("aria-activedescendant");
      if (!hits.length) { list.innerHTML = '<li><p class="search-empty">Nichts gefunden. Versuchen Sie einen anderen Begriff – oder rufen Sie uns an: 0931 2789892 0.</p></li>'; return; }
      list.innerHTML = hits.map(function (h, i) {
        return '<li role="presentation" style="--n:' + i + '"><a role="option" id="treffer-' + i + '" href="' + h.u + '" aria-selected="' + (i === 0) + '"><span></span><small></small></a></li>';
      }).join("");
      $$("a", list).forEach(function (a, i) {
        $("span", a).textContent = hits[i].t; $("small", a).textContent = hits[i].s;
        if (hits[i].recent) { var tg = document.createElement("span"); tg.className = "recent-tag"; tg.textContent = "Zuletzt"; $("span", a).prepend(tg); }
        a.addEventListener("click", function () { remember(hits[i].t, hits[i].s, hits[i].u); });
      });
    };
    var mark = function (n) {
      var as = $$("a", list);
      if (!as.length) return;
      sel = (n + as.length) % as.length;
      as.forEach(function (a, i) { a.setAttribute("aria-selected", i === sel); });
      as[sel].scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", "treffer-" + sel);
    };
    var openSearch = function (ev) {
      if (dlg.open) return;
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
      if (e.key === "Enter") { var a = $$("a", list)[sel]; if (a) { e.preventDefault(); a.click(); } }
    });
    searchBtns.forEach(function (b) { b.addEventListener("click", openSearch); });
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); if (dlg.open) dlg.close(); else openSearch(); }
      if (e.key === "/" && !/INPUT|TEXTAREA/.test(document.activeElement.tagName) && !dlg.open) { e.preventDefault(); openSearch(); }
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
  function fmt(d) { return String(d.getDate()).padStart(2, "0") + "." + String(d.getMonth() + 1).padStart(2, "0") + "." + d.getFullYear(); }
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

  /* ---------- Hinweis auf den nächsten Termin, ausblendbar mit „Rückgängig“ ---------- */
  var note = document.getElementById("hinweis");
  if (note && K && K.termine) {
    var nextEv = K.termine.filter(function (t) { return t.bis >= heute; })[0];
    if (nextEv) {
      var key = "hinweis-aus", id = nextEv.von + nextEv.titel;
      var a = parse(nextEv.von), b2 = parse(nextEv.bis);
      note.innerHTML = '<div class="container announce-inner">' + svg(ICON.calendar, 20) +
        '<p><strong></strong> <span></span></p><a href="aktuelles.html#termine">Alle Termine</a>' +
        '<button type="button" class="icon-btn" aria-label="Hinweis ausblenden">' + svg(ICON.x, 18) + "</button></div>";
      $("strong", note).textContent = "Nächster Termin:";
      $("p span", note).textContent = nextEv.titel + " – " + (nextEv.von === nextEv.bis ? fmtLong(a) : fmt(a) + " bis " + fmt(b2));
      var dleft = Math.round((Date.UTC(a.getFullYear(), a.getMonth(), a.getDate()) - Date.UTC(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())) / 864e5);
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
        note.hidden = true;
        store(key, id);
        toast("Hinweis ausgeblendet", "Rückgängig", function () { note.hidden = false; store(key, null); });
      });
    }
  }
  if (note && !note.firstChild) note.hidden = true;

  /* ---------- Termine merken: Datum fliegt im Bogen zum Zähler, gemerkte als Kalenderdatei ---------- */
  var SAVED_KEY = "gemerkt";
  function savedList() { try { return JSON.parse(store(SAVED_KEY) || "[]"); } catch (e) { return []; } }
  function setSaved(list) { store(SAVED_KEY, JSON.stringify(list)); }
  function calTarget() {
    var m = $(".mobile-bar .cal-target");
    if (m && m.offsetParent) return m;
    return $('.main-nav a[href="aktuelles.html"]') || $('.main-nav a[href="#aktuelles"]');
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
      row.hidden = !n; $(".saved-n", row).textContent = n;
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
          "SUMMARY:" + icsEsc(li.getAttribute("data-titel")), "DESCRIPTION:" + icsEsc(li.getAttribute("data-text")), "END:VEVENT");
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
      var cur = Math.min(ylen - 1, Math.max(0, ti)), dragging = false;
      function showDay(i, x) {
        cur = i;
        pin.style.left = x !== undefined ? x : (i + .5) / ylen * 100 + "%";
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

  /* ---------- Durchwahl finden ---------- */
  (function () {
    var inp = $("#durchwahl");
    if (!inp) return;
    var box = inp.closest(".dial"), out = $(".dial-out", box), timer = null, last = "";
    var norm = function (s) { return s.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9 ]/g, " ").trim(); };
    var dir = [];
    $$(".phone-card").forEach(function (card) {
      var area = $("h3", card).textContent.trim();
      $$(".phone-list li", card).forEach(function (li) {
        var a = $("a", li); if (!a || !/^tel:/.test(a.getAttribute("href"))) return;
        var label = $("span", li).textContent.trim();
        /* Kurzformen: „Krippe“, „Kiga“, „Hort“ finden den Bereich */
        var alias = /krippe/i.test(area) ? " krippe" : /garten/i.test(area) ? " kiga garten" : /hort/i.test(area) ? " hort schule" : "";
        dir.push({ keys: norm(label + " " + area + " " + label.replace(/gruppe$/i, "") + alias).split(" "), label: label + " · " + area, num: a.textContent.replace(/ /g, " "), href: a.getAttribute("href") });
      });
    });
    function show(html) {
      if (html === last) return; last = html;
      if (reduced) { out.innerHTML = html; return; }
      out.classList.add("swap");
      setTimeout(function () { out.innerHTML = html; out.classList.remove("swap"); }, 150);
    }
    inp.addEventListener("input", function () {
      clearTimeout(timer); inp.parentNode.classList.remove("err");
      var v = norm(inp.value);
      if (!v) { show(""); return; }
      var hits = dir.filter(function (d) { return v.split(" ").every(function (w) { return d.keys.some(function (k) { return k.indexOf(w) === 0; }); }); });
      if (hits.length) {
        show(hits.slice(0, 3).map(function (h) { return '<p><a href="' + h.href + '">' + h.num.replace(/ /g, "&nbsp;") + "</a><span>" + h.label + "</span></p>"; }).join(""));
        return;
      }
      /* erst nach einer kurzen Tipp-Pause bemängeln, dann kurz wackeln */
      timer = setTimeout(function () {
        inp.parentNode.classList.add("err");
        if (!reduced) { inp.parentNode.classList.remove("shake"); void inp.parentNode.offsetWidth; inp.parentNode.classList.add("shake"); }
        show('<p><a href="tel:+4993127898920">0931&nbsp;2789892&nbsp;0</a><span>Keine Gruppe gefunden – die Zentrale verbindet Sie gern.</span></p>');
      }, 650);
    });
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
  $$(".event .save").forEach(function (b) { b.addEventListener("click", function () { if (b.classList.contains("on")) confetti(b); }); });

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
    k.style.width = btn.offsetWidth + "px"; k.style.translate = btn.offsetLeft + "px 0";
    if (!anim || reduced) { void k.offsetWidth; k.style.transition = ""; }
  }

  /* ---------- Termine als Liste oder Kalender (mit Schließtagen) ---------- */
  (function () {
    var sw = $(".view-switch"), cal = $(".month-cal");
    if (!sw || !cal || !K) return;
    var list = $(".event-list", sw.parentNode), extra = [$(".events-empty", sw.parentNode)];
    var MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
    var now = new Date(), y = now.getFullYear(), m = now.getMonth(), end = parse(K.planEnde), maxI = end.getFullYear() * 12 + end.getMonth(), minI = y * 12 + m;
    K.termine.forEach(function (t) { var d = parse(t.bis); maxI = Math.max(maxI, d.getFullYear() * 12 + d.getMonth()); });
    function evOn(s) { return K.termine.filter(function (t) { return s >= t.von && s <= t.bis; }); }
    function render(dir) {
      var first = new Date(y, m, 1), off = (first.getDay() + 6) % 7, n = new Date(y, m + 1, 0).getDate(), cells = "";
      for (var i = 0; i < off; i++) cells += "<span></span>";
      for (var d = 1; d <= n; d++) {
        var dt = new Date(y, m, d), s = iso(dt), wd = dt.getDay(), why = closedReason(dt), evs = evOn(s), cls = [];
        if (wd === 0 || wd === 6) cls.push("we"); else if (why) cls.push("zu");
        if (s === heute) cls.push("today");
        var label = d + ". " + MON[m] + (why && wd !== 0 && wd !== 6 ? ", geschlossen (" + why + ")" : "") + (evs.length ? ", " + evs.map(function (e) { return e.titel; }).join(", ") : "");
        if (evs.length) cells += '<button type="button" class="ev ' + cls.join(" ") + '" data-d="' + s + '" aria-pressed="false" aria-label="' + label.replace(/"/g, "&quot;") + '">' + d + "</button>";
        else cells += '<span class="' + cls.join(" ") + '" aria-label="' + label.replace(/"/g, "&quot;") + '">' + d + "</span>";
      }
      var i0 = y * 12 + m, zu = K.schliesszeiten.filter(function (z) { var a = z.von.slice(0, 7), b = z.bis.slice(0, 7), c = y + "-" + String(m + 1).padStart(2, "0"); return a <= c && b >= c; });
      cal.innerHTML = '<div class="mc-head"><button type="button" class="mc-prev" aria-label="Voriger Monat"' + (i0 <= minI ? " disabled" : "") + ">" + svg(ICON.left, 20) + "</button><b aria-live=\"polite\">" + MON[m] + " " + y +
        '</b><button type="button" class="mc-next" aria-label="Nächster Monat"' + (i0 >= maxI ? " disabled" : "") + ">" + svg(ICON.right, 20) + "</button></div>" +
        '<div class="mc-wd" aria-hidden="true"><span>Mo</span><span>Di</span><span>Mi</span><span>Do</span><span>Fr</span><span>Sa</span><span>So</span></div><div class="mc-grid">' + cells + "</div>" +
        '<div class="mc-legend"><span><i style="background:var(--ink)"></i>Termin</span><span><i style="background:var(--rose-soft);box-shadow:inset 0 0 0 1px var(--rose-deep)"></i>geschlossen</span></div>' +
        '<p class="mc-note" aria-live="polite">' + (zu.length ? zu.map(function (z) { return "<b>" + z.name + ": " + fmt(parse(z.von)) + (z.von === z.bis ? "" : " – " + fmt(parse(z.bis))) + "</b>"; }).join("") : "") + "</p>";
      $(".mc-prev", cal).addEventListener("click", function () { step(-1); });
      $(".mc-next", cal).addEventListener("click", function () { step(1); });
      $$(".ev", cal).forEach(function (b) { b.addEventListener("click", function () {
        $$(".ev", cal).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        $(".mc-note", cal).innerHTML = evOn(b.getAttribute("data-d")).map(function (e) { var a = parse(e.von); return "<b>" + e.titel + "</b>" + (e.von === e.bis ? fmtLong(a) : fmt(a) + " – " + fmt(parse(e.bis))); }).join("");
      }); });
      if (dir && !reduced) $(".mc-grid", cal).animate([{ opacity: 0, translate: (dir * 24) + "px 0" }, { opacity: 1, translate: "0 0" }], { duration: 260, easing: "cubic-bezier(.23,1,.32,1)" });
    }
    function step(dd) { var i = y * 12 + m + dd; if (i < minI || i > maxI) return; y = Math.floor(i / 12); m = i % 12; render(dd); var f = $(dd > 0 ? ".mc-next" : ".mc-prev", cal); if (f && !f.disabled) f.focus(); else $(dd > 0 ? ".mc-prev" : ".mc-next", cal).focus(); }
    var sx = null; cal.addEventListener("pointerdown", function (e) { sx = e.clientX; });
    cal.addEventListener("pointerup", function (e) { if (sx === null) return; var dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); });
    function show(v, anim) {
      var showCal = v === "cal", out = showCal ? list : cal, inn = showCal ? cal : list;
      if (showCal) render(0);
      var swap = function () { out.hidden = true; inn.hidden = false; extra.forEach(function (x) { if (x && showCal) x.dataset.wasHidden = x.hidden, x.hidden = true; else if (x && x.dataset.wasHidden) x.hidden = x.dataset.wasHidden === "true"; }); };
      if (!anim || reduced || !out.animate) { swap(); return; }
      out.animate([{ opacity: 1 }, { opacity: 0, scale: .98 }], { duration: 140, easing: "ease-in" }).onfinish = function () { swap(); inn.animate([{ opacity: 0, scale: 1.02 }, { opacity: 1, scale: 1 }], { duration: 240, easing: "cubic-bezier(.23,1,.32,1)" }); };
    }
    var btns = $$("button", sw);
    btns.forEach(function (b) { b.addEventListener("click", function () {
      if (b.getAttribute("aria-pressed") === "true") return;
      btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); slideKnob(sw, b, true); show(b.getAttribute("data-view"), true); store("termine-ansicht", b.getAttribute("data-view"));
    }); });
    var pref = store("termine-ansicht") === "cal" ? btns[1] : btns[0];
    btns.forEach(function (x) { x.setAttribute("aria-pressed", x === pref); });
    requestAnimationFrame(function () { slideKnob(sw, pref, false); });
    if (pref === btns[1]) show("cal", false);
    addEventListener("resize", function () { slideKnob(sw, $('[aria-pressed="true"]', sw), false); });
  })();

  /* ---------- Elternbriefe durchsuchen ---------- */
  (function () {
    var inp = document.getElementById("brief-suche"); if (!inp) return;
    var briefe = $$(".brief"), cnt = $(".brief-search .faq-count"), empty = $(".brief-empty");
    function norm(t) { return t.toLowerCase().replace(/ä/g, "a").replace(/ö/g, "o").replace(/ü/g, "u").replace(/ß/g, "ss"); }
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
    var items = $$(".gal-item", grid), busy = false;
    chips.forEach(function (c) { c.addEventListener("click", function () {
      if (busy || c.getAttribute("aria-pressed") === "true") return;
      chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c); });
      var cat = c.getAttribute("data-cat"), keep = function (f) { return cat === "alle" || f.getAttribute("data-cat") === cat; };
      var first = new Map(); items.forEach(function (f) { if (!f.hidden) first.set(f, f.getBoundingClientRect()); });
      var leaving = items.filter(function (f) { return !f.hidden && !keep(f); });
      if (reduced || !grid.animate) { items.forEach(function (f) { f.hidden = !keep(f); }); return; }
      busy = true; leaving.forEach(function (f) { f.classList.add("leave"); });
      setTimeout(function () {
        items.forEach(function (f) { f.classList.remove("leave"); f.hidden = !keep(f); });
        items.forEach(function (f) {
          if (f.hidden) return; var a = first.get(f), b = f.getBoundingClientRect();
          if (a) f.animate([{ translate: (a.left - b.left) + "px " + (a.top - b.top) + "px" }, { translate: "0 0" }], { duration: 420, easing: EASE_IO });
          else f.animate([{ opacity: 0, scale: .92 }, { opacity: 1, scale: 1 }], { duration: 300, delay: 100, easing: EASE_OUT, fill: "backwards" });
        });
        busy = false;
      }, leaving.length ? 150 : 0);
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
      tabs.forEach(function (x) { var on = x === t; x.setAttribute("aria-selected", on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute("aria-controls")).hidden = !on; });
      slideKnob(tl, t, anim); if (focus) t.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { pick(t, false, true); });
      t.addEventListener("keydown", function (e) {
        var j = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : e.key === "Home" ? 0 : e.key === "End" ? tabs.length - 1 : null;
        if (j === null) return; e.preventDefault(); pick(tabs[(j + tabs.length) % tabs.length], true, true);
      });
    });
    var ua = navigator.userAgent, start = /Android/i.test(ua) ? tabs[1] : /iPhone|iPad|Macintosh/.test(ua) ? tabs[0] : /Windows/.test(ua) ? tabs[2] : tabs[0];
    requestAnimationFrame(function () { pick(start, false, false); });
    addEventListener("resize", function () { slideKnob(tl, $('[aria-selected="true"]', tl), false); });
  })();

  /* ---------- Fragen-Helfer (Antworten aus den häufigen Fragen) ---------- */
  (function () {
    var box = $(".ask"); if (!box || !K || !K.faq) return;
    var log = $(".ask-log", box), inp = $("#ask-in", box), F = K.faq;
    function norm(t) { return t.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9 ]/g, " "); }
    var STOP = " der die das und ist ein eine einen mein meine meinem kind kinder wir ich sie es zu in im fuer mit auch noch wie was gibt muss muessen kann koennen hat haben den dem des von auf an bei oder ihr ihre unser unsere wann wo wer ";
    function stems(t) { return norm(t).split(/\s+/).filter(function (w) { return w.length > 2 && STOP.indexOf(" " + w + " ") < 0; }).map(function (w) { return w.length > 5 ? w.slice(0, -2) : w; }); }
    function best(q) {
      var st = stems(q), top = null, sc = 0;
      var idf = st.map(function (s) { var df = F.filter(function (f) { return norm(f.q + " " + f.a).indexOf(s) >= 0; }).length; return df ? Math.log(1 + F.length / df) : 0; });
      F.forEach(function (f) { var q2 = norm(f.q), a2 = norm(f.a), v = 0; st.forEach(function (s, k) { v += idf[k] * ((q2.indexOf(s) >= 0 ? 2 : 0) + (a2.indexOf(s) >= 0 ? 1 : 0)); }); if (v > sc) { sc = v; top = f; } });
      return sc >= 1 ? top : null;
    }
    function add(cls, node) { var m = document.createElement("div"); m.className = "msg " + cls; if (typeof node === "string") m.textContent = node; else m.appendChild(node); log.appendChild(m); log.scrollTop = log.scrollHeight; return m; }
    function ask(q) {
      add("me", q);
      var ty = add("bot typing", document.createDocumentFragment()); ty.innerHTML = "<i></i><i></i><i></i>"; ty.setAttribute("aria-label", "Antwort wird gesucht");
      setTimeout(function () {
        ty.remove(); var f = best(q), frag = document.createDocumentFragment();
        if (f) {
          frag.appendChild(document.createTextNode(f.a));
          var a = document.createElement("a"); a.href = f.u; a.textContent = "Aus: „" + f.q + "“ (" + f.b + ")"; frag.appendChild(document.createElement("br")); frag.appendChild(a);
        } else {
          frag.appendChild(document.createTextNode("Dazu habe ich in unseren häufigen Fragen leider nichts gefunden. Rufen Sie uns gern an: "));
          var t = document.createElement("a"); t.href = "tel:+4993127898920"; t.textContent = "0931 2789892 0"; frag.appendChild(t);
        }
        add("bot", frag);
      }, reduced ? 0 : 650);
    }
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
      pop.innerHTML = "<strong>" + st.today + "</strong>" + rows + '<p class="next">' + (reason || m >= h ? st.sub : st.next) + "</p>";
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

  /* ---------- Jahreszeiten im Auftakt (höchstens 18 Teilchen, 8 Sekunden) ---------- */
  (function () {
    var cv = $(".season-fx"); if (!cv || reduced || !cv.getContext) return;
    var box = cv.parentNode, ctx = cv.getContext("2d"), W = 0, H = 0, parts = [], t0 = 0, run = false;
    var mo = new Date().getMonth(), kind = mo < 2 || mo === 11 ? "winter" : mo < 5 ? "fruehling" : mo < 8 ? "sommer" : "herbst";
    function size() { var r = box.getBoundingClientRect(), d = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height; cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); }
    function make() { parts = []; for (var i = 0; i < 18; i++) parts.push({ x: Math.random() * W, y: kind === "sommer" ? H * (.3 + Math.random() * .7) : -20 - Math.random() * H * .8, s: 4 + Math.random() * 5, v: .4 + Math.random() * .6, a: Math.random() * 6.28, w: .01 + Math.random() * .02, c: i % 3 }); }
    function draw(p) {
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
      if (kind === "winter") { ctx.fillStyle = "rgba(255,255,255,.95)"; ctx.beginPath(); ctx.arc(0, 0, p.s * .45, 0, 6.28); ctx.fill(); }
      else if (kind === "fruehling") { ctx.fillStyle = ["#F1E5E3", "#D4B5B0", "#FFFFFF"][p.c]; ctx.beginPath(); ctx.ellipse(0, 0, p.s * .5, p.s * .9, 0, 0, 6.28); ctx.fill(); }
      else if (kind === "herbst") { ctx.fillStyle = ["#C98F7E", "#D4B5B0", "#B9876F"][p.c]; ctx.beginPath(); ctx.moveTo(0, -p.s); ctx.quadraticCurveTo(p.s, 0, 0, p.s); ctx.quadraticCurveTo(-p.s, 0, 0, -p.s); ctx.fill(); }
      else { var g = ctx.createRadialGradient(0, 0, 0, 0, 0, p.s); g.addColorStop(0, "rgba(255,248,230,.95)"); g.addColorStop(1, "rgba(255,248,230,0)"); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, p.s, 0, 6.28); ctx.fill(); }
      ctx.restore();
    }
    function frame(t) {
      var age = (t - t0) / 1000, fade = age > 7 ? Math.max(0, 1 - (age - 7)) : Math.min(1, age * 2);
      ctx.clearRect(0, 0, W, H); ctx.globalAlpha = fade;
      parts.forEach(function (p) {
        p.a += p.w;
        if (kind === "sommer") { p.y -= p.v * .4; p.x += Math.sin(p.a) * .4; } else { p.y += p.v * (kind === "winter" ? .9 : 1.15); p.x += Math.sin(p.a) * (kind === "winter" ? .4 : .9); }
        draw(p);
      });
      if (fade > 0 && run && !document.hidden) requestAnimationFrame(frame); else { ctx.clearRect(0, 0, W, H); run = false; }
    }
    setTimeout(function () { size(); make(); t0 = performance.now(); run = true; requestAnimationFrame(frame); }, 900);
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

  /* ---------- Weg durch den Tag: der Tagesablauf zeichnet sich beim Scrollen ---------- */
  (function () {
    var tls = $$(".timeline"); if (!tls.length || reduced) return;
    tls.forEach(function (t) { t.classList.add("tl-draw"); });
    var ticking = false;
    function upd() {
      ticking = false; var mid = innerHeight * .6;
      tls.forEach(function (t) {
        var r = t.getBoundingClientRect(); if (r.bottom < -200 || r.top > innerHeight + 200) return;
        var p = Math.max(0, Math.min(1, (mid - r.top - 14) / Math.max(1, r.height - 28)));
        t.style.setProperty("--tl", p.toFixed(3));
        $$("li", t).forEach(function (li) { var lr = li.getBoundingClientRect(); li.classList.toggle("on", lr.top + 24 <= mid); });
      });
    }
    addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    addEventListener("resize", upd); upd();
  })();

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
      if (!el.matches(":focus-visible") || el.closest("dialog, .lightbox, .story-view") || el === document.body) { off(); return; }
      var first = !ring.classList.contains("on"); cur = el; place(first || reduced); ring.classList.add("on"); root.classList.add("fring");
    });
    function off() { cur = null; ring.classList.remove("on"); root.classList.remove("fring"); }
    document.addEventListener("focusout", function (e) { if (!e.relatedTarget) off(); });
    document.addEventListener("pointerdown", off, true);
    addEventListener("scroll", function () { if (cur) place(true); }, { passive: true });
    addEventListener("resize", function () { if (cur) place(true); });
  })();

  /* ---------- Wimpel-Ladeanzeige bei langsamem Seitenwechsel ---------- */
  (function () {
    var l = document.createElement("div"); l.className = "nav-loader"; l.setAttribute("role", "status"); l.setAttribute("aria-label", "Seite wird geladen");
    l.innerHTML = '<span style="--i:0"></span><span style="--i:1"></span><span style="--i:2"></span><span style="--i:3"></span><span style="--i:4"></span>';
    document.body.appendChild(l);
  })();

  /* ---------- Fotos mit Tiefe beim Scrollen ---------- */
  (function () {
    if (reduced) return;
    var imgs = $$(".page-hero-card > img, .teaser > img"); if (!imgs.length) return;
    imgs.forEach(function (im) { im.classList.add("depth"); });
    var ticking = false;
    function upd() {
      ticking = false; var h = innerHeight;
      imgs.forEach(function (im) {
        var box = im.parentNode.getBoundingClientRect(); if (box.bottom < 0 || box.top > h) return;
        var p = (box.top + box.height / 2 - h / 2) / h, max = box.height * (im.closest(".teaser") ? .05 : .08);
        im.style.setProperty("--py", Math.max(-max, Math.min(max, -p * max * 1.6)).toFixed(1) + "px");
      });
    }
    addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  })();

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
      if (sub) t = sub.getBoundingClientRect().bottom + 6; else t = hidden ? 8 : (hdr ? hdr.getBoundingClientRect().bottom + 6 : 8);
      made.forEach(function (st) {
        st.style.setProperty("--st-top", Math.max(8, Math.round(t)) + "px");
        /* sichtbar, sobald die eigentliche Überschrift oben verschwunden ist */
        st.classList.toggle("on", st._h.getBoundingClientRect().bottom < t);
      });
    }
    var tick = false;
    addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; top(); }); } }, { passive: true });
    addEventListener("resize", top); top();
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
      h += '</div><div class="leg"><span><i></i>Schließtag</span><span style="color:#B8574A;font-weight:600">12</span><span>= Feiertag</span><span>' + total + ' Schließtage im Kita-Jahr</span></div><p class="foot">Stand: ' + fmt(new Date()) + " · Alle Termine aktuell auf der Webseite unter „Aktuelles“</p>";
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

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
