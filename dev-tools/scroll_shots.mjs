import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 }, deviceScaleFactor: 2 });
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.fill('#loginPhoneInput', '09123456789');
await page.evaluate(() => sendOtp());
await page.waitForTimeout(600);
await page.evaluate(() => {
  document.querySelectorAll('#screen-otp .otp-box').forEach((b, i) => { b.value = String(i + 1); });
  verifyOtp();
});
await page.waitForTimeout(1200);

async function scrollShots(baseName, screenSel, openFn, count) {
  await page.evaluate(openFn);
  await page.waitForTimeout(700);
  const max = await page.evaluate(s => {
    const sc = document.querySelector(s);
    return sc.scrollHeight - sc.clientHeight;
  }, screenSel);
  for (let i = 0; i < count; i++) {
    const top = Math.round((max * i) / (count - 1 || 1));
    await page.evaluate(([s, t]) => { document.querySelector(s).scrollTop = t; }, [screenSel, top]);
    await page.waitForTimeout(450);
    await page.screenshot({ path: `/home/user/shots/${baseName}-${i}.png` });
  }
  console.log(baseName, 'maxScroll', max);
}

await scrollShots('L-services', '#screen-services .screen-content', () => { applyTheme(false); showScreen('screen-services'); }, 4);
await scrollShots('M-superapp', '#screen-service-detail .screen-content', () => { applyTheme(false); showScreen('screen-services'); openServiceDetail('superapp'); }, 3);
await scrollShots('N-recycling', '#screen-service-detail .screen-content', () => { applyTheme(false); showScreen('screen-services'); openServiceDetail('recycling'); }, 3);
await scrollShots('P-services-day', '#screen-services .screen-content', () => { applyTheme(true); showScreen('screen-services'); }, 2);

await browser.close();
