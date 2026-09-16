import { chromium } from 'playwright';
const browser = await chromium.launch();

async function audit(w, h, theme, label) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

  await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
  await page.evaluate(t => { document.documentElement.setAttribute('data-theme', t); localStorage.setItem('eplak_admin_theme', t); }, theme);
  await page.waitForTimeout(1400);

  const info = await page.evaluate(() => {
    const box = (s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), r: Math.round(r.right), b: Math.round(r.bottom) }; };
    const t = box('.theme-toggle'), lb = box('.login-box'), logo = box('.brand-logo');
    const overlap = (a, c) => !(a.r <= c.x || a.x >= c.r || a.b <= c.y || a.y >= c.b);
    return {
      toggle: t, loginBox: lb, logo,
      toggleInsideBox: t.x >= lb.x && t.r <= lb.r && t.y >= lb.y && t.b <= lb.b,
      toggleOverlapsLogo: logo ? overlap(t, logo) : null,
      overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    };
  });
  console.log(`\n===== ${label} =====`);
  console.log('  کلید:', JSON.stringify(info.toggle));
  console.log('  جعبه ورود:', JSON.stringify(info.loginBox));
  console.log('  کلید درون جعبه است:', info.toggleInsideBox, '| تداخل با لوگو:', info.toggleOverlapsLogo, '| سرریز افقی:', info.overflowX);

  // تست تعامل: نمایش رمز و ورود واقعی
  const pw = await page.evaluate(() => {
    const btn = document.querySelector('.toggle-password');
    if (!btn) return 'no-toggle';
    btn.click();
    return document.querySelector('input[name="password"]').type;
  });
  console.log('  نوع فیلد رمز پس از کلیک چشم:', pw);

  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin123');
  await page.click('button[type="submit"].btn-login');
  await page.waitForTimeout(1800);
  console.log('  ورود:', page.url().includes('index.php') ? '✅ موفق' : '❌ ناموفق → ' + page.url());
  if (errors.length) console.log('  خطاها:', errors.slice(0, 3).join(' | '));

  await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
  await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
  await page.waitForTimeout(1000);
  await page.screenshot({ path: `/home/user/shots/LOGIN2-${label}.png` });
  await ctx.close();
}

await audit(1440, 900, 'light', 'desktop-light');
await audit(1440, 900, 'dark', 'desktop-dark');
await audit(390, 844, 'light', 'mobile-light');
await audit(390, 844, 'dark', 'mobile-dark');
await browser.close();
