import { chromium } from 'playwright';
const BASE = 'http://127.0.0.1:8081';
const b = await chromium.launch();
for (const [theme, w] of [['light', 1400], ['dark', 1400], ['light', 420]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: 1200 }, locale: 'fa-IR' });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(BASE + '/login.php', { waitUntil: 'networkidle' });
  await p.fill('input[name="username"]', 'admin');
  await p.fill('input[name="password"]', 'admin123');
  await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('button[type="submit"]')]);
  await p.goto(BASE + '/index.php', { waitUntil: 'networkidle' });
  await p.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
  await p.waitForTimeout(2200);

  const r = await p.evaluate(() => {
    const R = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect();
      return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) }; };
    const bars = [...document.querySelectorAll('.hbar-fill')].map(f => Math.round(f.getBoundingClientRect().width));
    const tb = [...document.querySelectorAll('.trend-bar')].map(r => ({
      h: Math.round(r.getBoundingClientRect().height), fill: getComputedStyle(r).fill }));
    return {
      twoCol: R('.charts-2col'), col1: R('.chart-col'),
      hbars: bars, trend: tb,
      overflow: document.documentElement.scrollWidth > window.innerWidth + 2,
      donut: R('svg.donut')?.w,
      trendSvg: R('.trend-chart'),
    };
  });
  console.log(`\n=== ${w}px / ${theme} ===`);
  console.log('دو ستونه:', JSON.stringify(r.twoCol), '| ستون۱:', r.col1?.w);
  console.log('عرض میله‌های واحدها:', r.hbars.join(', '));
  console.log('ارتفاع میله‌های روند:', r.trend.map(t => t.h).join(', '));
  console.log('رنگ میلهٔ فعال:', r.trend.find(t => t.h > 10)?.fill || '—');
  console.log('عرض SVG روند:', r.trendSvg?.w, '| نمودار دایره‌ای:', r.donut);
  console.log('سرریز افقی:', r.overflow ? '❌ دارد' : '✅ ندارد');
  console.log('خطاها:', errs.length ? errs.join(' | ') : 'هیچ ✅');
  const tag = w < 600 ? 'mobile' : 'desktop';
  await p.screenshot({ path: `/home/user/shots/CHARTS2-${tag}-${theme}.png` });
  await ctx.close();
}
await b.close();
