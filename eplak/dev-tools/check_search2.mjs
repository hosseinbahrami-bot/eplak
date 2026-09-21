import { chromium } from 'playwright';
const BASE = 'http://127.0.0.1:8081';
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1400, height: 1200 }, locale: 'fa-IR' });
const p = await ctx.newPage();
const errs = [];
p.on('pageerror', e => errs.push(e.message));
await p.goto(BASE + '/login.php', { waitUntil: 'networkidle' });
await p.fill('input[name="username"]', 'admin');
await p.fill('input[name="password"]', 'admin123');
await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('button[type="submit"]')]);
await p.goto(BASE + '/notifications.php', { waitUntil: 'networkidle' });

// فعال‌کردن حالت «کاربران منتخب»
await p.evaluate(() => {
  const el = document.querySelector('input[name="target"][value="selected"], #targetSelected');
  if (el) { el.checked = true; el.dispatchEvent(new Event('change', { bubbles: true })); }
});
await p.waitForTimeout(700);
const info = await p.evaluate(() => {
  const picker = document.querySelector('#userPicker');
  const inp = document.querySelector('input[oninput*="filterUsers"]');
  return { pickerVisible: picker ? picker.offsetParent !== null : false,
           inputVisible: inp ? inp.offsetParent !== null : false,
           count: document.querySelectorAll('#userPicker label').length };
});
console.log('فهرست کاربران:', JSON.stringify(info));

if (info.inputVisible) {
  const before = await p.evaluate(() => [...document.querySelectorAll('#userPicker label')].filter(l => l.style.display !== 'none').length);
  await p.fill('input[oninput*="filterUsers"]', '0912');
  await p.waitForTimeout(400);
  const after = await p.evaluate(() => [...document.querySelectorAll('#userPicker label')].filter(l => l.style.display !== 'none').length);
  console.log(`جستجوی لاتین «0912»: قبل=${before} بعد=${after} → ${after > 0 && after < before ? '✅ کار می‌کند' : (after === 0 ? '❌ هیچ نتیجه‌ای نیافت' : '⚠️ بدون تغییر')}`);
  // جستجوی فارسی هم امتحان شود
  await p.fill('input[oninput*="filterUsers"]', '۰۹۱۲');
  await p.waitForTimeout(400);
  const afterFa = await p.evaluate(() => [...document.querySelectorAll('#userPicker label')].filter(l => l.style.display !== 'none').length);
  console.log(`جستجوی فارسی «۰۹۱۲»: ${afterFa} نتیجه`);
  await p.fill('input[oninput*="filterUsers"]', '');
  await p.waitForTimeout(300);
  const shown = await p.evaluate(() => [...document.querySelectorAll('#userPicker label')].slice(0,3).map(l => ({ text: l.textContent.replace(/\s+/g,' ').trim(), phone: l.dataset.phone })));
  console.log('\nنمایش در فهرست (متن باید فارسی، dataset باید لاتین باشد):');
  shown.forEach(s => console.log(`   متن: ${s.text}  |  dataset.phone: ${s.phone}`));
}
console.log('\nخطاها:', errs.length ? errs.join(' | ') : 'هیچ ✅');
await b.close();
