import { chromium } from 'playwright';
import fs from 'fs';

const DSF = 2;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 }, deviceScaleFactor: DSF });
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.fill('#loginPhoneInput', '09123456789');
await page.evaluate(() => sendOtp());
await page.waitForTimeout(500);
await page.evaluate(() => {
  document.querySelectorAll('#screen-otp .otp-box').forEach((b, i) => { b.value = String(i + 1); });
  verifyOtp();
});
await page.waitForTimeout(1200);

async function capture(name, openFn, sel) {
  await page.evaluate(openFn);
  await page.waitForTimeout(800);
  const geo = await page.evaluate(s => {
    const sc = document.querySelector(s);
    const r = sc.getBoundingClientRect();
    return { x: r.x, y: r.y, w: r.width, h: sc.clientHeight, scrollH: sc.scrollHeight };
  }, sel);
  const maxScroll = Math.max(0, geo.scrollH - geo.h);
  const n = Math.max(1, Math.ceil(geo.scrollH / geo.h));
  const strips = [];
  for (let i = 0; i < n; i++) {
    const p = Math.min(i * geo.h, maxScroll);
    await page.evaluate(([s, t]) => { document.querySelector(s).scrollTop = t; }, [sel, p]);
    await page.waitForTimeout(400);
    const file = `/home/user/shots/tmp-${name}-${i}.png`;
    await page.screenshot({ path: file });
    const y0 = Math.round(geo.y * DSF);
    const x0 = Math.round(geo.x * DSF);
    const cropTop = Math.round((i * geo.h - p) * DSF);
    const keepH = Math.min(geo.h, geo.scrollH - i * geo.h);
    strips.push({ file, x0, y0: y0 + cropTop, w: Math.round(geo.w * DSF), h: Math.round(keepH * DSF) });
  }
  fs.writeFileSync(`/home/user/shots/${name}.json`, JSON.stringify(strips));
  console.log(name, 'strips:', strips.length, 'contentH:', geo.scrollH);
}

await capture('m2-services-night', () => { applyTheme(false); showScreen('screen-services'); }, '#screen-services .screen-content');
await capture('m2-transport', () => { applyTheme(false); showScreen('screen-services'); openServiceCategory('transport'); }, '#screen-service-category .screen-content');
await capture('m2-services-day', () => { applyTheme(true); showScreen('screen-services'); }, '#screen-services .screen-content');

await browser.close();
