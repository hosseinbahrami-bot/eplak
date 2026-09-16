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

// پیمایش با منوی پایین از هر صفحه
const routes = [
  ['screen-home', 'پیشخوان', 'screen-dashboard'],
  ['screen-dashboard', 'خدمات', 'screen-services'],
  ['screen-services', 'گزارش‌ها', 'screen-reports'],
  ['screen-reports', 'پروفایل', 'screen-profile'],
  ['screen-profile', 'خانه', 'screen-home'],
];
for (const [from, label, expect] of routes) {
  const ok = await page.evaluate(([f, l]) => {
    showScreen(f);
    const item = Array.from(document.querySelectorAll(`#${f} .nav-item`)).find(n => n.textContent.trim() === l);
    if (!item) return { err: 'nav item not found' };
    item.click();
    return { active: document.querySelector('.screen.active')?.id };
  }, [from, label]);
  await page.waitForTimeout(500);
  const active = await page.evaluate(() => document.querySelector('.screen.active')?.id);
  console.log((active === expect ? 'PASS ' : 'FAIL ') + `${from} → ${label} → ${active} (expected ${expect})`);
}

// صفحات دیگر
const screens = ['screen-report', 'screen-track', 'screen-news', 'screen-payment', 'screen-map',
  'screen-notifications', 'screen-favorites', 'screen-settings', 'screen-contact', 'screen-profile-edit'];
for (const s of screens) {
  const r = await page.evaluate(id => {
    try { showScreen(id); return { active: document.querySelector('.screen.active')?.id, ok: true }; }
    catch (e) { return { ok: false, err: e.message }; }
  }, s);
  console.log((r.active === s ? 'PASS ' : 'FAIL ') + s + (r.err ? ' :: ' + r.err : ''));
  await page.waitForTimeout(250);
}

// بررسی محتوای صفحات کلیدی
const content = await page.evaluate(() => {
  showScreen('screen-dashboard');
  const dash = document.getElementById('dashActivityWrap')?.children.length;
  showScreen('screen-reports');
  const reps = document.getElementById('reportsListWrap')?.children.length;
  showScreen('screen-payment');
  const pay = document.getElementById('paymentListWrap')?.children.length;
  showScreen('screen-services');
  const svc = document.querySelectorAll('#servicesListWrap .svc-card').length;
  return { dashActivity: dash, reports: reps, payment: pay, services: svc };
});
console.log('content counts:', JSON.stringify(content));
console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'NO JS ERRORS');
await browser.close();
