import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 }, deviceScaleFactor: 1 });
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1000);

async function measure(mode) {
  await page.evaluate(d => applyTheme(d), mode === 'day');
  await page.evaluate(() => { showScreen('screen-services'); });
  await page.waitForTimeout(700);

  return await page.evaluate(() => {
    const r = {};
    const frame = document.querySelector('.phone-frame');
    r.frame = frame ? { w: Math.round(frame.getBoundingClientRect().width) } : null;

    // overflow checks
    const overflow = [];
    document.querySelectorAll('#screen-services *').forEach(el => {
      if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0) {
        overflow.push({ cls: el.className.toString().slice(0, 40), sw: el.scrollWidth, cw: el.clientWidth });
      }
    });
    r.horizontalOverflow = overflow.slice(0, 8);

    // nav bar geometry
    const nav = document.querySelector('#screen-services .nav-bar');
    const items = Array.from(document.querySelectorAll('#screen-services .nav-item'));
    r.nav = {
      navW: Math.round(nav.getBoundingClientRect().width),
      scrollW: nav.scrollWidth,
      clientW: nav.clientWidth,
      items: items.map(i => ({
        t: i.textContent.trim(),
        w: Math.round(i.getBoundingClientRect().width),
        sw: i.scrollWidth,
        cw: i.clientWidth,
      })),
    };

    // first card geometry
    const card = document.querySelector('#servicesListWrap .svc-card');
    const cb = card.getBoundingClientRect();
    r.card = { w: Math.round(cb.width), h: Math.round(cb.height) };
    const title = card.querySelector('h3');
    r.cardTitle = { w: Math.round(title.getBoundingClientRect().width), sw: title.scrollWidth, cw: title.clientWidth };
    const chips = Array.from(card.querySelectorAll('.svc-chip')).map(c => Math.round(c.getBoundingClientRect().width));
    r.chips = chips;

    // contrast sample: hero title vs page bg
    const cs = el => getComputedStyle(el);
    function lum(c) {
      const m = c.match(/\d+(\.\d+)?/g).map(Number);
      const [R, G, B] = m.slice(0, 3).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
      return 0.2126 * R + 0.7152 * G + 0.0722 * B;
    }
    function contrast(fg, bg) {
      const a = lum(fg), b = lum(bg);
      const [hi, lo] = a > b ? [a, b] : [b, a];
      return +(((hi + 0.05) / (lo + 0.05)).toFixed(2));
    }
    const pageBg = cs(document.body).backgroundColor;
    const h2 = document.querySelector('#screen-services .svc-hero h2');
    r.contrast = {
      heroTitle: contrast(cs(h2).color, pageBg),
      cardTitle: contrast(cs(title).color, pageBg),
      chip: contrast(cs(card.querySelector('.svc-chip')).color, pageBg),
      cardSub: contrast(cs(card.querySelector('p')).color, pageBg),
    };

    // content height / scrollability
    const sc = document.querySelector('#screen-services .screen-content');
    r.content = { scrollH: sc.scrollHeight, clientH: sc.clientHeight };
    return r;
  });
}

console.log('=== NIGHT ===');
console.log(JSON.stringify(await measure('night'), null, 1));
console.log('=== DAY ===');
console.log(JSON.stringify(await measure('day'), null, 1));

// detail screen geometry
await page.evaluate(() => { applyTheme(false); openServiceDetail('superapp'); });
await page.waitForTimeout(600);
const det = await page.evaluate(() => {
  const w = document.querySelector('#serviceDetailWrap');
  const btn = w.querySelector('.svc-action-btn');
  const mods = Array.from(w.querySelectorAll('.svc-module')).map(m => ({
    w: Math.round(m.getBoundingClientRect().width),
    h: Math.round(m.getBoundingClientRect().height),
    sw: m.scrollWidth, cw: m.clientWidth
  }));
  return {
    modules: mods,
    btn: btn ? { w: Math.round(btn.getBoundingClientRect().width), h: Math.round(btn.getBoundingClientRect().height) } : null,
    scrollH: document.querySelector('#screen-service-detail .screen-content').scrollHeight,
    clientH: document.querySelector('#screen-service-detail .screen-content').clientHeight,
  };
});
console.log('=== DETAIL (superapp) ===');
console.log(JSON.stringify(det, null, 1));

await browser.close();
