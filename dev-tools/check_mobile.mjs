import { chromium } from 'playwright';
const BASE = 'http://127.0.0.1:8081';
const b = await chromium.launch();
for (const w of [420, 768]) {
  const ctx = await b.newContext({ viewport: { width: w, height: 900 }, locale: 'fa-IR' });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(BASE + '/login.php', { waitUntil: 'networkidle' });
  await p.fill('input[name="username"]', 'admin');
  await p.fill('input[name="password"]', 'admin123');
  await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('button[type="submit"]')]);
  console.log(`\n--- عرض ${w}px ---`);
  for (const page of ['index.php', 'users.php', 'reports.php']) {
    await p.goto(BASE + '/' + page, { waitUntil: 'networkidle' });
    const r = await p.evaluate(() => ({
      sw: document.documentElement.scrollWidth,
      iw: window.innerWidth,
      main: Math.round(document.querySelector('.main').getBoundingClientRect().width),
      donut: document.querySelector('svg.donut') ? Math.round(document.querySelector('svg.donut').getBoundingClientRect().width) : null,
    }));
    console.log(`  ${page.padEnd(12)} scrollWidth=${String(r.sw).padStart(4)} | main=${String(r.main).padStart(4)} | نمودار=${r.donut ?? '—'} ${r.sw <= r.iw + 2 ? '✅ مناسب' : '❌ سرریز'}`);
  }
  if (errs.length) console.log('  خطا:', errs.join(' | '));
  await ctx.close();
}
await b.close();
