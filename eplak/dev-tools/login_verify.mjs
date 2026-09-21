import { chromium } from 'playwright';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, bypassCSP: true });
const page = await ctx.newPage();
const seen = [];
page.on('response', r => { if (r.url().includes('assets/style.css') || r.url().includes('theme.js')) seen.push(r.url().split('/').pop()); });
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
const info = await page.evaluate(async () => {
  await document.fonts.ready;
  const img = [...document.querySelectorAll('.brand-logo img')].find(i => getComputedStyle(i).display !== 'none');
  const r = img.getBoundingClientRect();
  const container = document.querySelector('.brand-logo').getBoundingClientRect();
  return {
    cssVersion: [...document.styleSheets].map(s => (s.href || 'inline').split('/').pop()).slice(0, 3),
    logoRendered: `${Math.round(r.width)}×${Math.round(r.height)}`,
    containerSize: `${Math.round(container.width)}×${Math.round(container.height)}`,
    containerBg: getComputedStyle(document.querySelector('.brand-logo')).backgroundImage,
    bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0],
    iranSans: document.fonts.check('16px IranianSans'),
    toggle: !!document.querySelector('.theme-toggle'),
  };
});
console.log('منابع بارگیری‌شده:', seen.join('، '));
console.log(JSON.stringify(info, null, 1));
await browser.close();
