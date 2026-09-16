import { chromium } from 'playwright';

// رندر صفحه خدمات با CSS قدیمی (سناریوی کش) برای مقایسه با اسکرین‌شات کاربر
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 376, height: 786 } });
await page.goto('http://127.0.0.1:8099/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.fill('#loginPhoneInput', '09123456789');
await page.evaluate(() => sendOtp());
await page.waitForTimeout(500);
await page.evaluate(() => {
  document.querySelectorAll('#screen-otp .otp-box').forEach((b, i) => { b.value = String(i + 1); });
  verifyOtp();
});
await page.waitForTimeout(1100);

// رفتن به صفحه خدمات و اسکرول تا پنل «کسب‌وکار و بوم‌گردی» (مشابه تصویر کاربر)
await page.evaluate(() => {
  showScreen('screen-services');
  const sc = document.querySelector('#screen-services .screen-content');
  const panel = Array.from(document.querySelectorAll('.svc-panel')).find(p => p.textContent.includes('کسب‌وکار و بوم‌گردی'));
  if (panel && sc) sc.scrollTop = Math.max(0, panel.offsetTop - 160);
});
await page.waitForTimeout(700);
await page.screenshot({ path: '/home/user/shots/repro-old-css.png' });
console.log('saved repro-old-css.png');

// اندازه SVG‌های بدون محدودیت
const svgSizes = await page.evaluate(() => {
  const out = [];
  document.querySelectorAll('#servicesListWrap svg').forEach(s => {
    const r = s.getBoundingClientRect();
    if (r.width > 40 || r.height > 40) out.push({ w: Math.round(r.width), h: Math.round(r.height), parent: s.parentElement.className.toString().slice(0, 30) });
  });
  return out;
});
console.log('oversized svgs:', JSON.stringify(svgSizes));
await browser.close();
