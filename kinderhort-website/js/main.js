/* Kath. Kinder- und Jugendhort Grombühl – Interaktionen */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  /* Header-Schatten beim Scrollen */
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile Navigation */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".main-nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Dropdown "Virtueller Rundgang" */
  document.querySelectorAll(".has-drop").forEach(function (li) {
    var btn = li.querySelector(".drop-toggle");
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function () {
    document.querySelectorAll(".has-drop.open").forEach(function (li) {
      li.classList.remove("open");
      li.querySelector(".drop-toggle").setAttribute("aria-expanded", "false");
    });
  });

  /* Rundgang: Pfeil-Buttons */
  document.querySelectorAll(".tour").forEach(function (tour) {
    var track = tour.querySelector(".tour-track");
    var items = track.querySelectorAll(".tour-item");
    var count = tour.querySelector(".count");
    function step() { return items.length > 1 ? items[1].offsetLeft - items[0].offsetLeft : track.clientWidth; }
    tour.querySelector(".tour-prev").addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: "smooth" }); });
    tour.querySelector(".tour-next").addEventListener("click", function () { track.scrollBy({ left: step(), behavior: "smooth" }); });
    function update() {
      if (!count) return;
      var s = step();
      var i = s > 0 ? Math.round(track.scrollLeft / s) + 1 : 1;
      count.textContent = "Bild " + Math.min(i, items.length) + " von " + items.length;
    }
    track.addEventListener("scroll", update, { passive: true });
    update();
  });

  /* Lightbox */
  var lb = document.createElement("div");
  lb.className = "lightbox";
  lb.setAttribute("role", "dialog");
  lb.setAttribute("aria-modal", "true");
  lb.setAttribute("aria-label", "Bildansicht");
  lb.innerHTML =
    '<span class="lb-count"></span>' +
    '<button type="button" class="lb-btn lb-close" aria-label="Schließen"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
    '<button type="button" class="lb-btn lb-prev" aria-label="Vorheriges Bild"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></button>' +
    '<button type="button" class="lb-btn lb-next" aria-label="Nächstes Bild"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></button>' +
    '<figure><img alt=""><figcaption><strong></strong><span></span></figcaption></figure>';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector("img"), lbTitle = lb.querySelector("figcaption strong"),
      lbText = lb.querySelector("figcaption span"), lbCount = lb.querySelector(".lb-count");
  var group = [], idx = 0, lastFocus = null;

  function show(i) {
    idx = (i + group.length) % group.length;
    var el = group[idx];
    lbImg.classList.remove("ready");
    lbImg.onload = function () { lbImg.classList.add("ready"); };
    lbImg.src = el.getAttribute("data-full");
    if (lbImg.complete) lbImg.classList.add("ready");
    lbImg.alt = el.getAttribute("data-title") || "";
    lbTitle.textContent = el.getAttribute("data-title") || "";
    lbText.textContent = el.getAttribute("data-text") || "";
    lbCount.textContent = group.length > 1 ? (idx + 1) + " / " + group.length : "";
    lb.querySelector(".lb-prev").style.display = group.length > 1 ? "" : "none";
    lb.querySelector(".lb-next").style.display = group.length > 1 ? "" : "none";
  }
  function open(el) {
    var g = el.getAttribute("data-group");
    group = Array.prototype.slice.call(document.querySelectorAll('[data-full][data-group="' + g + '"]'));
    lastFocus = el;
    show(group.indexOf(el));
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
    lb.querySelector(".lb-close").focus();
  }
  function close() {
    lb.classList.remove("open");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-full]");
    if (el) { e.preventDefault(); open(el); }
  });
  lb.querySelector(".lb-close").addEventListener("click", close);
  lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
  lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
  document.addEventListener("keydown", function (e) {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(idx - 1);
    if (e.key === "ArrowRight") show(idx + 1);
  });
  var touchX = null;
  lb.addEventListener("touchstart", function (e) { touchX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
    touchX = null;
  });

  /* Sanftes Einblenden beim Scrollen, Geschwister leicht versetzt */
  var reveals = document.querySelectorAll(".reveal");
  function shown(el) {
    el.classList.add("visible");
    /* danach gelten wieder die eigenen Hover-Übergänge der Karte */
    setTimeout(function () { el.classList.remove("reveal"); el.style.removeProperty("--i"); }, 1400);
  }
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
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

  /* ---------- Datumshilfen ---------- */
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function parse(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  var TAGE = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
  function fmt(d) { return String(d.getDate()).padStart(2, "0") + "." + String(d.getMonth() + 1).padStart(2, "0") + "." + d.getFullYear(); }
  function fmtLong(d) { return TAGE[d.getDay()] + ", " + fmt(d); }

  /* ---------- Vergangene Termine ausblenden ---------- */
  var heute = iso(new Date());
  var events = document.querySelectorAll(".event[data-ende]");
  if (events.length) {
    var left = 0;
    events.forEach(function (ev) { if (ev.getAttribute("data-ende") < heute) ev.hidden = true; else left++; });
    var empty = document.querySelector(".events-empty");
    if (empty && !left) empty.hidden = false;
  }

  /* ---------- Heute geöffnet / nächster Schließtag ---------- */
  var K = window.KITA;
  function closedReason(d) {
    if (!K) return null;
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
    var open = !reason && hm >= K.oeffnung && hm < K.schluss;
    var today, sub;
    if (open) {
      today = "Jetzt geöffnet – heute bis " + K.schluss + " Uhr";
      sub = "Krippe und Kindergarten bis 16:30 Uhr, Spätdienst bis 17:30 Uhr, Hort bis 18:00 Uhr.";
    } else if (!reason && hm < K.oeffnung) {
      today = "Heute geöffnet ab " + K.oeffnung + " Uhr";
      sub = "Krippe und Kindergarten bis 16:30 Uhr, Hort bis 18:00 Uhr.";
    } else {
      var n = nextOpen(now);
      today = reason ? "Heute geschlossen (" + reason + ")" : "Für heute geschlossen";
      sub = "Wir sind wieder da am " + fmtLong(n) + " ab " + K.oeffnung + " Uhr.";
    }
    var next = "";
    for (var i = 0; i < K.schliesszeiten.length; i++) {
      var z = K.schliesszeiten[i];
      if (z.bis < iso(now)) continue;
      var v = parse(z.von), b = parse(z.bis);
      var range = z.von === z.bis ? fmtLong(v) : fmt(v) + " – " + fmt(b);
      next = (iso(now) >= z.von ? "Aktuelle Schließzeit: " : "Nächste Schließzeit: ") + z.name + ", " + range +
             " (" + z.tage + (z.tage === 1 ? " Schließtag)" : " Schließtage)");
      break;
    }
    if (!next) next = "Der Ferienplan für das nächste Kita-Jahr folgt in Kürze.";
    return { open: open, today: today, sub: sub, next: next };
  }
  if (K) {
    var st = status();
    ["status", "status-kontakt"].forEach(function (id) {
      var box = document.getElementById(id);
      if (!box) return;
      box.querySelector(".status-today").textContent = st.today;
      box.querySelector(".status-sub").textContent = st.sub;
      var nx = box.querySelector(".status-next span");
      if (nx) nx.textContent = st.next;
      box.classList.toggle("is-closed", !st.open);
      box.hidden = false;
    });
  }

  /* ---------- Ferienplan drucken ---------- */
  document.querySelectorAll(".js-print-plan").forEach(function (b) {
    b.addEventListener("click", function () {
      document.body.classList.add("print-plan");
      document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("visible"); });
      window.print();
    });
  });
  window.addEventListener("afterprint", function () { document.body.classList.remove("print-plan"); });

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
