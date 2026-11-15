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
  function show(i, dir) {
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
    group = $$('[data-full][data-group="' + el.getAttribute("data-group") + '"]');
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
    if (e.key === "Escape") closeLb();
    if (e.key === "ArrowLeft") show(idx - 1, -1);
    if (e.key === "ArrowRight") show(idx + 1, 1);
  });
  /* Wischen: Das Bild folgt dem Finger 1:1, ohne Übergang. Nach oben und bei nur einem Bild seitlich: Gummiband */
  var t0 = null;
  lb.addEventListener("touchstart", function (e) { t0 = { x: e.touches[0].clientX, y: e.touches[0].clientY, axis: null }; lbFig.style.transition = "none"; }, { passive: true });
  lb.addEventListener("touchmove", function (e) {
    if (!t0) return;
    var dy = e.touches[0].clientY - t0.y, dx = e.touches[0].clientX - t0.x;
    if (!t0.axis && Math.abs(dx) + Math.abs(dy) > 8) t0.axis = Math.abs(dx) > Math.abs(dy) ? "x" : "y";
    if (t0.axis === "y") lbFig.style.setProperty("--drag", (dy > 0 ? dy : rubber(dy, 60)) + "px");
    if (t0.axis === "x") lbFig.style.setProperty("--dx", (group.length > 1 ? dx : rubber(dx, 60)) + "px");
  }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (!t0) return;
    var dx = e.changedTouches[0].clientX - t0.x, dy = e.changedTouches[0].clientY - t0.y, axis = t0.axis;
    lbFig.style.transition = "translate .3s " + EASE_OUT;
    lbFig.style.removeProperty("--drag"); lbFig.style.removeProperty("--dx");
    if (axis === "y" && dy > 110) closeLb();
    else if (axis === "x" && Math.abs(dx) > 50 && group.length > 1) show(idx + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
    t0 = null;
  });

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
        /* ohne Eingabe: die am häufigsten gebrauchten Wege zuerst */
        var oft = ["Kind krankmelden", "Kontakt & Durchwahlen", "Aktuelle Termine", "Ferienplan & Schließtage", "Platz anfragen", "Downloads"];
        return oft.map(function (t) { return index.filter(function (e) { return e.it.t === t && !/^Kinder/.test(e.it.s); })[0]; }).filter(Boolean).map(function (e) { return e.it; });
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
      $$("a", list).forEach(function (a, i) { $("span", a).textContent = hits[i].t; $("small", a).textContent = hits[i].s; });
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

  /* ---------- Schnelle Wiederbesuche ---------- */
  if ("serviceWorker" in navigator && /^https?:$/.test(location.protocol)) {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () { /* ohne geht es auch */ }); });
  }

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
