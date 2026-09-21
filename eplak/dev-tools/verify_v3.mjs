import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
const loaded = [];
page.on('response', r => { const u = r.url(); if (u.includes('style.css') || u.includes('theme.js') || u.includes('fonts/')) loaded.push(u.split('/').slice(-2).join('/')); });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(1400);
const r = await page.evaluate(async () => {
  await document.fonts.ready;
  const inp = document.querySelector('input[name="username"]');
  const icon = document.querySelector('.input-icon');
  const cs = getComputedStyle(inp);
  return {
    css: [...document.styleSheets].map(s => (s.href||'inline').split('/').pop())[0],
    paddingRight: cs.paddingRight,
    gap: Math.round(icon.getBoundingClientRect().left - (inp.getBoundingClientRect().right - parseFloat(cs.paddingRight))),
    logo: (() => { const i = [...document.querySelectorAll('.brand-logo img')].find(x => getComputedStyle(x).display !== 'none'); return Math.round(i.getBoundingClientRect().width) + '×' + Math.round(i.getBoundingClientRect().height); })(),
    font: getComputedStyle(document.body).fontFamily.split(',').slice(0,3).join('،'),
    toggleInside: (() => { const t = document.querySelector('.theme-toggle'), lb = document.querySelector('.login-box'); const a=t.getBoundingClientRect(), b=lb.getBoundingClientRect(); return a.left>=b.left && a.right<=b.right && a.top>=b.top; })(),
  };
});
console.log('منابع:', loaded.join('، '));
console.log(JSON.stringify(r, null, 1));
console.log(errors.length ? '❌ خطا: ' + errors.join(' | ') : '✅ بدون خطا');
await page.screenshot({ path: '/home/user/shots/LOGIN-FINAL-light.png' });
await page.evaluate(() => { document.documentElement.setAttribute('data-theme','dark'); localStorage.setItem('eplak_admin_theme','dark'); });
await page.waitForTimeout(900);
await page.screenshot({ path: '/home/user/shots/LOGIN-FINAL-dark.png' });
await browser.close();
