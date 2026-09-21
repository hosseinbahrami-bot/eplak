import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });

for (const t of ['light', 'dark']) {
  await page.evaluate(x => document.documentElement.setAttribute('data-theme', x), t);
  await page.waitForTimeout(800);
  const c = await page.evaluate(() => {
    const cs = (s, p) => { const e = document.querySelector(s); return e ? getComputedStyle(e)[p] : '---'; };
    return {
      'بدنه': cs('body', 'backgroundColor'),
      'کارت ورود': cs('.login-box', 'backgroundColor'),
      'عنوان اصلی': cs('.brand-name', 'color'),
      'زیرعنوان': cs('.brand-sub', 'color'),
      'برچسب فیلد': cs('.form-group label', 'color'),
      'زمینه فیلد': cs('input[name="username"]', 'backgroundColor'),
      'متن فیلد': cs('input[name="username"]', 'color'),
      'خط جداکننده': cs('.divider', 'color'),
      'دکمه ورود': cs('.btn-login', 'backgroundColor'),
      'متن دکمه ورود': cs('.btn-login', 'color'),
      'گزینه‌ها': cs('.form-options .remember-me', 'color'),
      'پیوند فراموشی': cs('.forgot-link', 'color'),
      'پیوندهای پایین': cs('.footer-links a', 'color'),
      'نسخه': cs('.version', 'color'),
      'کلید تم (زمینه)': cs('.theme-toggle', 'backgroundColor'),
      'کلید تم (متن)': cs('.theme-toggle', 'color'),
    };
  });
  console.log(`\n===== ${t} =====`);
  for (const [k, v] of Object.entries(c)) console.log(`  ${k.padEnd(18)} ${v}`);
}
await browser.close();
