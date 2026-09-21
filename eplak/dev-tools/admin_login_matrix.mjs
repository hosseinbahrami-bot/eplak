import { chromium } from 'playwright';

const browser = await chromium.launch();

async function loginTest(label, { useFrame = false, blockCookies = false } = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();

  if (blockCookies) {
    // حذف کامل هدر Set-Cookie از همه پاسخ‌ها = شبیه‌سازی مرورگری که کوکی نمی‌پذیرد
    await page.route('**/*', async route => {
      const res = await route.fetch();
      const headers = { ...res.headers() };
      delete headers['set-cookie'];
      delete headers['Set-Cookie'];
      await route.fulfill({ response: res, headers });
    });
  }

  try {
    if (useFrame) {
      await page.goto('http://127.0.0.1:8090/', { waitUntil: 'networkidle' });
    } else {
      await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
    }
    await page.waitForTimeout(1000);

    const target = useFrame ? page.frames().find(f => f.url().includes('8081')) : page;
    if (!target) throw new Error('iframe not found');

    await target.fill('input[name="username"]', 'admin');
    await target.fill('input[name="password"]', 'admin123');
    await target.click('button[type="submit"].btn-login');
    await page.waitForTimeout(2200);

    const url = target.url();
    const ok = url.includes('index.php') && !url.includes('login.php');
    console.log(`${label}: ${ok ? '✅ ورود موفق' : '❌ ورود ناموفق'} → ${url.replace('http://127.0.0.1:8081', '')}`);
  } catch (e) {
    console.log(`${label}: ❌ خطا → ${e.message}`);
  }
  await ctx.close();
}

await loginTest('۱) تب مستقیم، کوکی فعال      ', { useFrame: false, blockCookies: false });
await loginTest('۲) تب مستقیم، کوکی مسدود     ', { useFrame: false, blockCookies: true });
await loginTest('۳) داخل iframe، کوکی فعال    ', { useFrame: true, blockCookies: false });
await loginTest('۴) داخل iframe، کوکی مسدود   ', { useFrame: true, blockCookies: true });

await browser.close();
