import { chromium } from 'playwright';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();

await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
const loginLogo = await page.evaluate(() => {
  const img = [...document.querySelectorAll('.brand-logo img')].find(i => getComputedStyle(i).display !== 'none');
  const r = img.getBoundingClientRect();
  return { w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top), src: img.getAttribute('src').split('/').pop() };
});
console.log('لوگوی صفحه ورود:', JSON.stringify(loginLogo));

await page.fill('input[name="username"]', 'admin');
await page.fill('input[name="password"]', 'admin123');
await page.click('button[type="submit"].btn-login');
await page.waitForTimeout(1600);

for (const theme of ['light', 'dark']) {
  await page.evaluate(t => { document.documentElement.setAttribute('data-theme', t); localStorage.setItem('eplak_admin_theme', t); }, theme);
  await page.waitForTimeout(600);
  const info = await page.evaluate(() => {
    const img = [...document.querySelectorAll('.sidebar .brand img')].find(i => getComputedStyle(i).display !== 'none');
    const r = img.getBoundingClientRect();
    const nav = document.querySelector('.sidebar nav').getBoundingClientRect();
    return {
      logo: { w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top), right: Math.round(r.right) },
      navTop: Math.round(nav.top),
      sidebarWidth: Math.round(document.querySelector('.sidebar').getBoundingClientRect().width),
      file: img.getAttribute('src').split('/').pop(),
    };
  });
  console.log(`سایدبار (${theme}):`, JSON.stringify(info));
}
await browser.close();
