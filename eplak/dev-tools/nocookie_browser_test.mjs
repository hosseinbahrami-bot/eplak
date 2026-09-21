import { chromium } from 'playwright';

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await ctx.newPage();

await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);

// شبیه‌سازی مرورگری که کوکی نشست را ذخیره/ارسال نمی‌کند
await ctx.clearCookies();
const cookies = await ctx.cookies();
console.log('کوکی‌های باقی‌مانده قبل از ارسال:', cookies.length);

await page.fill('input[name="username"]', 'admin');
await page.fill('input[name="password"]', 'admin123');
await page.click('button[type="submit"].btn-login');
await page.waitForTimeout(2200);

const url = page.url();
const inPanel = url.includes('index.php') && !url.includes('login.php');
console.log(`بدون کوکی: ${inPanel ? '✅ ورود موفق' : '❌ ورود ناموفق'}`);
console.log('نشانی نهایی:', url.replace('http://127.0.0.1:8081', ''));

if (inPanel) {
  // پیمایش داخل پنل بدون کوکی
  // کلیک روی لینک‌های سایدبار (رفتار واقعی کاربر)، نه تایپ مستقیم نشانی
  const links = await page.evaluate(() =>
    Array.from(document.querySelectorAll('a[href]'))
      .map(a => a.getAttribute('href'))
      .filter(h => /reports\.php|users\.php|departments\.php|tickets\.php/.test(h))
  );
  console.log('  نمونه لینک‌های سایدبار:', links.slice(0, 3));
  for (const label of ['گزارش‌ها', 'کاربران', 'واحدها']) {
    const link = page.locator(`a:has-text("${label}")`).first();
    if (await link.count() === 0) { console.log(`  ${label}: لینک یافت نشد`); continue; }
    await link.click();
    await page.waitForTimeout(1200);
    await ctx.clearCookies(); // همچنان بدون کوکی
    const t = await page.title();
    const back = t.includes('ورود');
    console.log(`  کلیک روی «${label}»: ${back ? '❌ بیرون افتاد' : '✅ در پنل'} — ${t}`);
    if (!back) await page.goBack({ waitUntil: 'domcontentloaded' }).catch(() => {});
    await page.waitForTimeout(600);
  }
  await page.screenshot({ path: '/home/user/shots/ADMIN-nocookie-reports.png' });
}
await browser.close();
