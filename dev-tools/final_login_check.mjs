import { chromium } from 'playwright';
const browser = await chromium.launch();

for (const [w, h, theme, label] of [[1440,900,'light','desktop-light'], [1440,900,'dark','desktop-dark'], [390,844,'light','mobile-light']]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
  await page.evaluate(t => { document.documentElement.setAttribute('data-theme', t); localStorage.setItem('eplak_admin_theme', t); }, theme);
  await page.waitForTimeout(1200);
  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin123');
  await page.waitForTimeout(500);

  const r = await page.evaluate(() => {
    const inp = document.querySelector('input[name="username"]').getBoundingClientRect();
    return { x: Math.round(inp.left), y: Math.round(inp.top), width: Math.round(inp.width), height: Math.round(inp.height) };
  });
  await page.screenshot({ path: `/home/user/shots/FINAL-login-${label}.png`, clip: r });
  await page.screenshot({ path: `/home/user/shots/FULL-login-${label}.png` });
  console.log(`${label}: ناحیه فیلد نام کاربری ذخیره شد ${JSON.stringify(r)}`);
  await ctx.close();
}
await browser.close();
