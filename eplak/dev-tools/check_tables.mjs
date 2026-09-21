import { chromium } from 'playwright';
const BASE = 'http://127.0.0.1:8081';
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 420, height: 900 }, locale: 'fa-IR' });
const p = await ctx.newPage();
await p.goto(BASE + '/login.php', { waitUntil: 'networkidle' });
await p.fill('input[name="username"]', 'admin');
await p.fill('input[name="password"]', 'admin123');
await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('button[type="submit"]')]);

for (const page of ['users.php', 'reports.php']) {
  await p.goto(BASE + '/' + page, { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => {
    const t = document.querySelector('table');
    if (!t) return { noTable: true };
    const panel = t.closest('.panel') || t.parentElement;
    return {
      tableW: Math.round(t.getBoundingClientRect().width),
      panelW: Math.round(panel.getBoundingClientRect().width),
      overflow: getComputedStyle(panel).overflowX,
      scrollable: panel.scrollWidth > panel.clientWidth + 2,
      rows: t.querySelectorAll('tbody tr').length,
    };
  });
  console.log(`${page}: جدول=${r.tableW}px درون پنل=${r.panelW}px | overflow-x=${r.overflow} | اسکرول داخلی=${r.scrollable ? 'دارد ✅' : 'ندارد'} | ردیف‌ها=${r.rows}`);
}
await p.screenshot({ path: '/home/user/shots/MOBILE-users-fixed.png' });
await b.close();
