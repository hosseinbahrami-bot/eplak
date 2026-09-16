import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 }, deviceScaleFactor: 2 });
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);

// login
await page.fill('#loginPhoneInput', '09123456789');
await page.evaluate(() => sendOtp());
await page.waitForTimeout(600);
await page.evaluate(() => {
  document.querySelectorAll('#screen-otp .otp-box').forEach((b, i) => { b.value = String(i + 1); });
  verifyOtp();
});
await page.waitForTimeout(1200);

async function fullShot(name, prep) {
  await page.evaluate(prep);
  await page.waitForTimeout(700);
  await page.screenshot({ path: `/home/user/shots/${name}.png`, fullPage: true });
  console.log('saved', name);
}

// 1) full services list (night)
await fullShot('F1-services-full-night', () => {
  applyTheme(false);
  showScreen('screen-services');
  const sc = document.querySelector('#screen-services .screen-content');
  sc.style.overflow = 'visible'; sc.style.maxHeight = 'none';
  document.querySelector('.phone-frame').style.maxHeight = 'none';
});

// 2) superapp detail (night)
await fullShot('F2-detail-superapp-night', () => {
  applyTheme(false);
  showScreen('screen-services');
  openServiceDetail('superapp');
  const sc = document.querySelector('#screen-service-detail .screen-content');
  sc.style.overflow = 'visible'; sc.style.maxHeight = 'none';
  document.querySelector('.phone-frame').style.maxHeight = 'none';
});

// 3) services list (day) — first part
await fullShot('F3-services-day', () => {
  applyTheme(true);
  showScreen('screen-services');
  const sc = document.querySelector('#screen-services .screen-content');
  sc.style.overflow = 'visible'; sc.style.maxHeight = 'none';
  document.querySelector('.phone-frame').style.maxHeight = 'none';
});

// 4) recycling detail (night) — نمونه‌ای با دکمه اقدام واقعی
await fullShot('F4-detail-recycling-night', () => {
  applyTheme(false);
  showScreen('screen-services');
  openServiceDetail('recycling');
  const sc = document.querySelector('#screen-service-detail .screen-content');
  sc.style.overflow = 'visible'; sc.style.maxHeight = 'none';
  document.querySelector('.phone-frame').style.maxHeight = 'none';
});

await browser.close();
