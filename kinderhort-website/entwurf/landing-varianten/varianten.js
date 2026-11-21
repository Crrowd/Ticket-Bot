/* Startseiten-Varianten: Umschalter und Einblendung des Startbereichs mit einer GSAP-Timeline.
   Läuft einmal beim Laden und beim Umschalten; nichts hängt am Scrollen. Bei „Bewegung reduzieren“ keine Bewegung. */
(function () {
  var NAMEN = { 1: "Bühne", 2: "Papier", 3: "Zentriert" };
  var root = document.documentElement, tl = null;
  function lies() { try { return localStorage.getItem("landing-variante"); } catch (e) { return null; } }
  function merke(v) { try { localStorage.setItem("landing-variante", v); } catch (e) {} }

  function einblenden(v) {
    var hero = document.querySelector("#seite-index .hero");
    if (!hero || !window.gsap) return;
    if (tl) tl.progress(1).kill();
    var mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: no-preference)", function () {
      var text = hero.querySelectorAll(".hero-grid > div:first-child > *");
      var fotos = hero.querySelectorAll(".hero-collage figure");
      var badge = hero.querySelector(".hero-badge");
      var foto = v === "2" ? { x: 48, autoAlpha: 0 } : v === "3" ? { y: 56, autoAlpha: 0 } : { scale: .9, autoAlpha: 0 };
      tl = gsap.timeline({ defaults: { duration: .7, ease: "power3.out" } });
      tl.addLabel("text")
        .from(text, { y: 24, autoAlpha: 0, stagger: .08 }, "text")
        .addLabel("fotos", v === "3" ? "text+=.35" : "text+=.15")
        .from(fotos, Object.assign({ stagger: .09, duration: .8, clearProps: "transform,opacity,visibility" }, foto), "fotos")
        .from(badge, { scale: 0, autoAlpha: 0, duration: .5, ease: "back.out(2)", clearProps: "transform,opacity,visibility" }, ">-0.2");
      return function () { tl && tl.progress(1); };
    });
  }

  function setze(v, animiert) {
    root.setAttribute("data-variante", v);
    document.querySelectorAll(".v-schalter button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.v === v)); });
    merke(v);
    if (animiert) einblenden(v);
  }

  var leiste = document.createElement("div");
  leiste.className = "v-schalter"; leiste.setAttribute("role", "group"); leiste.setAttribute("aria-label", "Variante der Startseite");
  leiste.innerHTML = "<span>Startseite:</span>" + Object.keys(NAMEN).map(function (k) { return '<button type="button" data-v="' + k + '">' + k + " · " + NAMEN[k] + "</button>"; }).join("");
  document.body.appendChild(leiste);
  leiste.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (!document.querySelector("#seite-index.active")) location.hash = "#index";
    setze(b.dataset.v, true); scrollTo(0, 0);
  });
  var start = lies(); if (!NAMEN[start]) start = "1";
  setze(start, true);
})();
