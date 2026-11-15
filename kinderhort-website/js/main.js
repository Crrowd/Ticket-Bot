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
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

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
        ul.scrollTo({ left: a.offsetLeft - 16, behavior: reduced ? "auto" : "smooth" });
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
