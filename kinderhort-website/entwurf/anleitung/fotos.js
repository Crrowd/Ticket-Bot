// Bildschirmfotos der echten Seite für die Team-Anleitung (Server muss auf Port 8765 laufen)
const { chromium } = require('playwright');
const path = require('path');
const D = __dirname;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 });
  async function foto(seite, sel, name, vorher) {
    await p.goto('http://localhost:8765/' + seite, { waitUntil: 'networkidle' });
    await p.addStyleTag({ content: '.site-header{display:none!important} .reveal{opacity:1!important;translate:none!important} *{animation:none!important;transition:none!important}' }).catch(() => {});
    if (vorher) await vorher();
    const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(400);
    await el.screenshot({ path: path.join(D, name) });
  }
  await foto('aktuelles.html', '#termine .notes-grid > div:first-child', 'f-termine.png');
  await foto('aktuelles.html', '#ferienplan .table-wrap, #ferienplan table', 'f-schliesstage.png');
  await foto('aktuelles.html', '.brief', 'f-brief.png');
  await foto('aktuelles.html', '.note-card', 'f-hinweis.png');
  await foto('kontakt.html', '.kontakt-zeile', 'f-status.png');
  await foto('index.html', '.dringend', 'f-dringend.png');
  await b.close();
})();
