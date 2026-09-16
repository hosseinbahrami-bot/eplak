import { chromium } from 'playwright';

const URL = process.argv[2] || 'http://127.0.0.1:8080/';
const LABEL = process.argv[3] || 'main';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 376, height: 786 } });
const errors = [];
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

await page.goto(URL, { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.fill('#loginPhoneInput', '09123456789');
await page.evaluate(() => sendOtp());
await page.waitForTimeout(500);
await page.evaluate(() => {
  document.querySelectorAll('#screen-otp .otp-box').forEach((b, i) => { b.value = String(i + 1); });
  verifyOtp();
});
await page.waitForTimeout(1100);

// اسکرول تا پنل «کسب‌وکار و بوم‌گردی» (همان نقطه‌ی تصویر کاربر)
await page.evaluate(() => {
  showScreen('screen-services');
  const sc = document.querySelector('#screen-services .screen-content');
  const panel = Array.from(document.querySelectorAll('.svc-panel')).find(p => p.textContent.includes('کسب‌وکار و بوم‌گردی'));
  if (panel && sc) sc.scrollTop = Math.max(0, panel.offsetTop - 150);
});
await page.waitForTimeout(700);

// بررسی سراسری: هیچ المانی نباید از قاب بیرون بزند یا اندازه غیرعادی داشته باشد
const problems = await page.evaluate(() => {
  const frame = document.querySelector('.phone-frame').getBoundingClientRect();
  const bad = [];
  document.querySelectorAll('.screen.active *').forEach(el => {
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    const cls = el.className.toString();
    if (cls.includes('bg-orb') || cls.includes('city-skyline') || cls.includes('vsc-') || cls.includes('hwy-')) return; // عناصر تزئینی
    if (r.width > 360 || r.height > 500 || r.left < frame.left - 2 || r.right > frame.right + 2) {
      bad.push({ tag: el.tagName, cls: cls.slice(0, 28), w: Math.round(r.width), h: Math.round(r.height), l: Math.round(r.left), r: Math.round(r.right) });
    }
  });
  return { frame: { l: Math.round(frame.left), r: Math.round(frame.right) }, bad: bad.slice(0, 10) };
});
console.log(LABEL, 'problems:', JSON.stringify(problems, null, 1));

await page.screenshot({ path: `/home/user/shots/verify-${LABEL}.png` });
console.log(LABEL, 'errors:', errors.length ? errors.join('; ') : 'none');
await browser.close();
