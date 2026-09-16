import { chromium } from 'playwright';

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
page.on('requestfailed', r => {
  if (r.url().includes('/assets/')) errors.push('REQUEST FAILED: ' + r.url());
});

// ---------- ورود ----------
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(1500);

const loginInfo = await page.evaluate(async () => {
  await document.fonts.ready;
  return {
    fontFamily: getComputedStyle(document.body).fontFamily,
    headingFont: getComputedStyle(document.querySelector('.brand-name')).fontFamily,
    yekanLoaded: document.fonts.check('16px YekanBakh'),
    iranSansLoaded: document.fonts.check('16px IranianSans'),
    loadedFonts: [...document.fonts].map(f => f.family + ':' + f.weight + ':' + f.status).slice(0, 8),
    logoVisible: !!document.querySelector('.brand-logo img') &&
      document.querySelector('.brand-logo img').naturalWidth > 0,
    toggleExists: !!document.querySelector('.theme-toggle'),
    toggleText: document.querySelector('.theme-toggle')?.textContent?.trim(),
  };
});
console.log('=== صفحه ورود ===');
console.log('  فونت بدنه:', loginInfo.fontFamily.slice(0, 60));
console.log('  فونت عنوان:', loginInfo.headingFont.slice(0, 60));
console.log('  یکان بارگذاری شده:', loginInfo.yekanLoaded, '| ایران‌سنس:', loginInfo.iranSansLoaded);
console.log('  فونت‌های فعال:', loginInfo.loadedFonts.join(', '));
console.log('  لوگو نمایش داده می‌شود:', loginInfo.logoVisible);
console.log('  کلید تم:', loginInfo.toggleExists, '|', loginInfo.toggleText);
await page.screenshot({ path: '/home/user/shots/ADMIN-new-login-light.png' });

// ---------- کلیک روی کلید تم (ورود) ----------
await page.click('.theme-toggle');
await page.waitForTimeout(900);
const afterToggle = await page.evaluate(() => ({
  theme: document.documentElement.getAttribute('data-theme'),
  stored: localStorage.getItem('eplak_admin_theme'),
  bodyBg: getComputedStyle(document.body).backgroundColor,
  toggleText: document.querySelector('.theme-toggle')?.textContent?.trim(),
  logoShown: [...document.querySelectorAll('.brand-logo img')].filter(i => getComputedStyle(i).display !== 'none').length,
}));
console.log('  پس از کلیک:', JSON.stringify(afterToggle));
await page.screenshot({ path: '/home/user/shots/ADMIN-new-login-dark.png' });

// برگشت به روز
await page.click('.theme-toggle');
await page.waitForTimeout(700);
console.log('  بازگشت به:', await page.evaluate(() => document.documentElement.getAttribute('data-theme')));

// ---------- ورود و بررسی پنل ----------
await page.fill('input[name="username"]', 'admin');
await page.fill('input[name="password"]', 'admin123');
await page.click('button[type="submit"].btn-login');
await page.waitForTimeout(1800);
console.log('\n=== داشبورد ===');
const dash = await page.evaluate(() => ({
  url: location.pathname,
  sidebarLogo: document.querySelector('.sidebar .brand img')?.naturalWidth > 0,
  toggleInTopbar: !!document.querySelector('.topbar .theme-toggle'),
  theme: document.documentElement.getAttribute('data-theme'),
}));
console.log(' ', JSON.stringify(dash));
await page.screenshot({ path: '/home/user/shots/ADMIN-new-dashboard-light.png' });

// فعال‌سازی حالت شب در داشبورد
await page.click('.theme-toggle');
await page.waitForTimeout(1000);
const darkDash = await page.evaluate(() => ({
  theme: document.documentElement.getAttribute('data-theme'),
  mainBg: getComputedStyle(document.querySelector('.main')).backgroundColor,
  cardBg: getComputedStyle(document.querySelector('.card')).backgroundColor,
  textColor: getComputedStyle(document.querySelector('.topbar h1')).color,
  logoIsLight: getComputedStyle(document.querySelector('.sidebar .brand .logo-dark')).display !== 'none',
}));
console.log('  حالت شب:', JSON.stringify(darkDash));
await page.screenshot({ path: '/home/user/shots/ADMIN-new-dashboard-dark.png' });

// ماندگاری پس از بارگیری مجدد
await page.reload({ waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
console.log('  پس از بارگیری مجدد:', await page.evaluate(() => document.documentElement.getAttribute('data-theme')));

// ---------- پیمایش صفحات در حالت شب ----------
for (const p of ['reports.php', 'users.php', 'departments.php', 'settings.php']) {
  await page.goto('http://127.0.0.1:8081/' + p, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(900);
  const info = await page.evaluate(() => ({
    title: document.title,
    theme: document.documentElement.getAttribute('data-theme'),
    rows: document.querySelectorAll('tbody tr').length,
    hasToggle: !!document.querySelector('.theme-toggle'),
    logo: document.querySelector('.sidebar .brand img')?.naturalWidth > 0,
  }));
  console.log(`  ${p}: ${JSON.stringify(info)}`);
}

await page.goto('http://127.0.0.1:8081/reports.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.screenshot({ path: '/home/user/shots/ADMIN-new-reports-dark.png' });

console.log('\n' + (errors.length ? '❌ خطاها:\n' + errors.join('\n') : '✅ بدون خطا'));
await browser.close();
