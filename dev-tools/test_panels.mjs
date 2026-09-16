import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 } });
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.fill('#loginPhoneInput', '09123456789');
await page.evaluate(() => sendOtp());
await page.waitForTimeout(500);
await page.evaluate(() => {
  document.querySelectorAll('#screen-otp .otp-box').forEach((b, i) => { b.value = String(i + 1); });
  verifyOtp();
});
await page.waitForTimeout(1100);

// 1) ساختار صفحه خدمات
const struct = await page.evaluate(() => {
  showScreen('screen-services');
  const w = document.getElementById('servicesListWrap');
  return {
    quickTiles: w.querySelectorAll('.services-grid .service-card').length,
    quickLabels: Array.from(w.querySelectorAll('.services-grid .service-card h3')).map(h => h.textContent.trim()),
    panels: w.querySelectorAll('.svc-panel').length,
    panelTitles: Array.from(w.querySelectorAll('.svc-panel-head-text h3')).map(h => h.textContent.trim()),
    rows: w.querySelectorAll('.svc-row').length,
    rowTitles: Array.from(w.querySelectorAll('.svc-row-body h4')).map(h => h.textContent.trim()),
  };
});
console.log(JSON.stringify(struct, null, 1));

// 2) زدن روی هدر هر کادر → ورود به همان بخش
for (const cat of ['finance', 'business-cat', 'environment', 'smart', 'transport']) {
  const r = await page.evaluate(c => {
    showScreen('screen-services');
    const head = Array.from(document.querySelectorAll('#servicesListWrap .svc-panel-head'));
    const target = head.find(h => h.getAttribute('onclick').includes("'" + c + "'"));
    if (!target) return { err: 'head not found' };
    target.click();
    const w = document.getElementById('serviceCategoryWrap');
    return {
      active: document.querySelector('.screen.active')?.id,
      title: w.querySelector('h2')?.textContent.trim(),
      cards: w.querySelectorAll('.svc-card').length,
    };
  }, cat);
  await page.waitForTimeout(400);
  const ok = r.active === 'screen-service-category' && r.cards > 0;
  console.log((ok ? 'PASS ' : 'FAIL ') + cat + ' → ' + JSON.stringify(r));
}

// 3) زدن روی یک سطر داخل کادر → صفحه همان سرویس (و نه صفحه بخش)
const rowNav = await page.evaluate(() => {
  showScreen('screen-services');
  const row = document.querySelector('#servicesListWrap .svc-row');
  const label = row.querySelector('h4').textContent.trim();
  row.click();
  return { label, active: document.querySelector('.screen.active')?.id, title: document.querySelector('#serviceDetailWrap h2')?.textContent.trim() };
});
await page.waitForTimeout(400);
console.log((rowNav.active === 'screen-service-detail' ? 'PASS ' : 'FAIL ') + 'row → ' + JSON.stringify(rowNav));

// 4) کارت دسترسی سریع
const quick = await page.evaluate(() => {
  showScreen('screen-services');
  const tile = document.querySelector('#servicesListWrap .services-grid .service-card');
  const label = tile.querySelector('h3').textContent.trim();
  tile.click();
  return { label, active: document.querySelector('.screen.active')?.id };
});
await page.waitForTimeout(400);
console.log((quick.active === 'screen-service-detail' ? 'PASS ' : 'FAIL ') + 'quick tile → ' + JSON.stringify(quick));

// 5) اندازه‌گیری: سرریز و تراز
const geo = await page.evaluate(() => {
  showScreen('screen-services');
  const frame = document.querySelector('.phone-frame').getBoundingClientRect();
  const bad = [];
  document.querySelectorAll('#servicesListWrap *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return;
    if (r.left < frame.left - 1 || r.right > frame.right + 1) {
      bad.push({ cls: el.className.toString().slice(0, 30), l: Math.round(r.left), r: Math.round(r.right) });
    }
  });
  const panel = document.querySelector('#servicesListWrap .svc-panel').getBoundingClientRect();
  return {
    outsideFrame: bad.slice(0, 6),
    panel: { w: Math.round(panel.width), h: Math.round(panel.height), l: Math.round(panel.left) },
    frameL: Math.round(frame.left), frameR: Math.round(frame.right),
  };
});
console.log('geometry:', JSON.stringify(geo));

// 6) حالت روز
await page.evaluate(() => { applyTheme(true); showScreen('screen-services'); });
await page.waitForTimeout(500);
console.log('day mode rendered, panels:', await page.evaluate(() => document.querySelectorAll('.svc-panel').length));

console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'NO JS ERRORS');
await browser.close();
