import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

// ۱) صفحه ورود
await page.goto('http://127.0.0.1:8081/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
console.log('landing url:', page.url());
await page.screenshot({ path: '/home/user/shots/ADMIN-1-login.png' });

// ۲) ورود
await page.fill('input[name="username"]', 'admin');
await page.fill('input[name="password"]', 'admin123');
await page.click('button[type="submit"].btn-login');
await page.waitForTimeout(1600);
console.log('after login url:', page.url());
await page.screenshot({ path: '/home/user/shots/ADMIN-2-dashboard.png' });

// ۳) بررسی آمار داشبورد
const stats = await page.evaluate(() => {
  const out = {};
  document.querySelectorAll('.stat-card, .card, .panel, section').forEach(c => {
    const t = (c.textContent || '').replace(/\s+/g, ' ').trim();
    if (t.length > 4 && t.length < 120) out[t.slice(0, 60)] = true;
  });
  return Object.keys(out).slice(0, 8);
});
console.log('dashboard snippets:', JSON.stringify(stats, null, 1));

// ۴) پیمایش همه بخش‌ها
const pages = [
  ['reports.php', 'ADMIN-3-reports'],
  ['users.php', 'ADMIN-4-users'],
  ['tickets.php', 'ADMIN-5-tickets'],
  ['departments.php', 'ADMIN-6-departments'],
  ['settings.php', 'ADMIN-7-settings'],
];
for (const [url, name] of pages) {
  await page.goto('http://127.0.0.1:8081/' + url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  const info = await page.evaluate(() => ({
    title: document.title,
    rows: document.querySelectorAll('tbody tr').length,
    h1: (document.querySelector('h1, h2')?.textContent || '').trim().slice(0, 40),
    bodyOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  }));
  console.log(name, JSON.stringify(info));
  await page.screenshot({ path: `/home/user/shots/${name}.png` });
}

// ۵) جزئیات یک گزارش (بررسی عمق عملکرد)
await page.goto('http://127.0.0.1:8081/reports.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(800);
const firstLink = await page.evaluate(() => {
  const a = document.querySelector('tbody tr a[href*="report_detail"], tbody tr a');
  return a ? a.getAttribute('href') : null;
});
if (firstLink) {
  await page.goto('http://127.0.0.1:8081/' + firstLink, { waitUntil: 'networkidle' });
  await page.waitForTimeout(900);
  await page.screenshot({ path: '/home/user/shots/ADMIN-8-report-detail.png' });
  console.log('report detail opened:', firstLink);
}

console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'NO JS/PHP ERRORS');
await browser.close();
