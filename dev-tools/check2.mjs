import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 } });
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.evaluate(() => { applyTheme(false); showScreen('screen-services'); });
await page.waitForTimeout(700);

const res = await page.evaluate(() => {
  const out = {};
  const box = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), sw: e.scrollWidth, cw: e.clientWidth }; };
  out.hero = box('#screen-services .svc-hero');
  out.heroP = box('#screen-services .svc-hero p');
  out.emblem = box('#screen-services .svc-hero-emblem');
  out.cardBody = box('#servicesListWrap .svc-card .svc-card-body');
  out.chips = box('#servicesListWrap .svc-card .svc-chips');
  out.card = box('#servicesListWrap .svc-card');
  out.go = box('#servicesListWrap .svc-card .svc-go');
  // overlap test
  function overlap(a, b) {
    if (!a || !b) return null;
    const ix = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const iy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    return { ix: Math.round(ix), iy: Math.round(iy) };
  }
  out.emblemVsText = overlap(out.emblem, out.heroP);
  // detail button
  showScreen('screen-services'); openServiceDetail('transit');
  return out;
});
console.log(JSON.stringify(res, null, 1));

await page.waitForTimeout(600);
const res2 = await page.evaluate(() => {
  const b = document.querySelector('#serviceDetailWrap .svc-action-btn');
  const wrap = document.querySelector('#serviceDetailWrap');
  const r = b.getBoundingClientRect();
  const frame = document.querySelector('.phone-frame').getBoundingClientRect();
  return {
    btn: { x: Math.round(r.x), w: Math.round(r.width), right: Math.round(r.right) },
    wrapW: Math.round(wrap.getBoundingClientRect().width),
    frameX: Math.round(frame.x), frameR: Math.round(frame.right),
    overflowRight: Math.round(r.right - frame.right),
    overflowLeft: Math.round(frame.x - r.x),
  };
});
console.log(JSON.stringify(res2, null, 1));
await browser.close();
