import { chromium } from 'playwright';

const browser = await chromium.launch();

async function tryLogin(label, contextOptions) {
  const ctx = await browser.newContext(contextOptions);
  const page = await ctx.newPage();
  // صفحه‌ی میزبان روی یک origin دیگر (پورت 8090) که ادمین را در iframe (پورت 8081) نمایش می‌دهد
  await page.goto('http://127.0.0.1:8090/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200);
  const frame = page.frames().find(f => f.url().includes('8081'));
  if (!frame) { console.log(label, '❌ iframe پیدا نشد'); await ctx.close(); return; }

  await frame.fill('input[name="username"]', 'admin');
  await frame.fill('input[name="password"]', 'admin123');
  await frame.click('button[type="submit"].btn-login');
  await page.waitForTimeout(2000);

  const url = frame.url();
  const ok = url.includes('index.php') && !url.includes('login.php');
  console.log(`${label}: ${ok ? '✅ ورود موفق' : '❌ ورود ناموفق'} → ${url}`);
  await ctx.close();
}

// ۱) حالت عادی کرومیوم (کوکی‌های شخص ثالث طبق پیش‌فرض مرورگر)
await tryLogin('پیش‌فرض مرورگر', { viewport: { width: 1280, height: 900 } });

// ۲) شبیه‌سازی مرورگرهایی که کوکی‌های شخص ثالث را مسدود می‌کنند (Safari / Firefox / Brave)
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
await ctx.addInitScript(() => {
  // مسدود کردن کامل کوکی: شبیه‌سازی رفتار مرورگرهای مسدودکننده
  Object.defineProperty(document, 'cookie', {
    get: () => '',
    set: () => {},
    configurable: true
  });
});
const page = await ctx.newPage();
await page.goto('http://127.0.0.1:8090/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
const frame = page.frames().find(f => f.url().includes('8081'));
if (frame) {
  await frame.fill('input[name="username"]', 'admin');
  await frame.fill('input[name="password"]', 'admin123');
  await frame.click('button[type="submit"].btn-login');
  await page.waitForTimeout(2000);
  const url = frame.url();
  const ok = url.includes('index.php') && !url.includes('login.php');
  console.log(`کوکی مسدود (شبیه‌سازی Safari/Firefox): ${ok ? '✅ ورود موفق' : '❌ ورود ناموفق'} → ${url}`);
}
await ctx.close();

await browser.close();
