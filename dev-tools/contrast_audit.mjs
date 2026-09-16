import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });

for (const t of ['light', 'dark']) {
  await page.evaluate(x => document.documentElement.setAttribute('data-theme', x), t);
  await page.waitForTimeout(800);
  const res = await page.evaluate(() => {
    function parse(c) {
      const m = c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
      return m ? { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] } : null;
    }
    function lum({ r, g, b }) {
      const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    }
    // رنگ واقعیِ پس‌زمینه مؤثر (بالا رفتن در درخت تا یافتن رنگ غیرشفاف)
    function effBg(el) {
      let e = el;
      while (e) {
        const c = parse(getComputedStyle(e).backgroundColor);
        if (c && c.a > 0.5) return c;
        e = e.parentElement;
      }
      return { r: 255, g: 255, b: 255, a: 1 };
    }
    function ratio(fg, bg) {
      const L1 = lum(fg), L2 = lum(bg);
      return ((Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05));
    }
    const targets = [
      ['.brand-name', 'عنوان اصلی'],
      ['.brand-sub', 'زیرعنوان'],
      ['.divider span', 'متن جداکننده'],
      ['.form-group label', 'برچسب فیلد'],
      ['input[name="username"]', 'متن فیلد'],
      ['.form-options .remember-me', 'مرا به خاطر بسپار'],
      ['.forgot-link', 'فراموشی رمز'],
      ['.footer-links a', 'پیوندهای پایین'],
      ['.version', 'نسخه'],
      ['.theme-toggle', 'کلید تم'],
      ['.btn-login', 'متن دکمه ورود'],
      ['.toggle-password', 'آیکون چشم'],
      ['.input-icon', 'آیکون فیلد'],
    ];
    const out = [];
    for (const [sel, label] of targets) {
      const el = document.querySelector(sel);
      if (!el) { out.push({ label, missing: true }); continue; }
      const fg = parse(getComputedStyle(el).color);
      const bg = effBg(el);
      out.push({ label, ratio: +ratio(fg, bg).toFixed(2), fg: getComputedStyle(el).color });
    }
    return out;
  });
  console.log(`\n===== ${t} =====`);
  res.forEach(r => {
    if (r.missing) return console.log(`  ⚪ ${r.label}: یافت نشد`);
    const flag = r.ratio < 3 ? '❌ ناخوانا' : r.ratio < 4.5 ? '⚠️  کم' : '✅';
    console.log(`  ${r.label.padEnd(20)} نسبت ${String(r.ratio).padStart(6)}  ${flag}`);
  });
}
await browser.close();
