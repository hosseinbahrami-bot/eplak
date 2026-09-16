import { chromium } from 'playwright';

const shots = [
  { name: '01-home', act: null },
  { name: '02-services', act: "showScreen('screen-services')" },
  { name: '03-detail-superapp', act: "showScreen('screen-services'); openServiceDetail('superapp')" },
  { name: '04-detail-transit', act: "showScreen('screen-services'); openServiceDetail('transit')" },
  { name: '05-detail-ruralmap', act: "showScreen('screen-services'); openServiceDetail('ruralmap')" },
  { name: '06-day-services', act: "showScreen('screen-services')", day: true },
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 }, deviceScaleFactor: 2 });
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);

for (const s of shots) {
  if (s.day) await page.evaluate(() => applyTheme(true));
  if (!s.day) await page.evaluate(() => applyTheme(false));
  if (s.act) {
    await page.evaluate(a => { eval(a); }, s.act);
    await page.waitForTimeout(900);
  }
  await page.screenshot({ path: `/home/user/shots/${s.name}.png`, fullPage: false });
  console.log('shot:', s.name);
}

// sanity checks
await page.evaluate(() => { showScreen('screen-services'); });
await page.waitForTimeout(600);
const info = await page.evaluate(() => {
  const cards = document.querySelectorAll('#servicesListWrap .svc-card');
  const groups = document.querySelectorAll('#servicesListWrap .svc-group');
  const navItems = document.querySelectorAll('#screen-services .nav-item');
  return {
    cards: cards.length,
    groups: groups.length,
    navItems: Array.from(navItems).map(n => n.textContent.trim()),
    activeNav: (document.querySelector('#screen-services .nav-item.active') || {}).textContent?.trim(),
    homeCards: Array.from(document.querySelectorAll('#screen-home .services-grid .service-card h3')).map(h => h.textContent.trim()),
    dashCards: Array.from(document.querySelectorAll('#screen-dashboard .services-grid .service-card h3')).map(h => h.textContent.trim()),
  };
});
console.log(JSON.stringify(info, null, 2));

// detail content check
await page.evaluate(() => openServiceDetail('business'));
await page.waitForTimeout(600);
const detail = await page.evaluate(() => ({
  title: document.querySelector('#serviceDetailWrap h2')?.textContent,
  caps: document.querySelectorAll('#serviceDetailWrap .svc-cap').length,
  chips: document.querySelectorAll('#serviceDetailWrap .svc-chip').length,
  intro: document.querySelector('#serviceDetailWrap .svc-intro-card p')?.textContent.slice(0, 60),
}));
console.log(JSON.stringify(detail, null, 2));

console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'NO JS ERRORS');
await browser.close();
