import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.fill('input[name="username"]', 'admin');
await page.fill('input[name="password"]', 'admin123');
await page.click('button[type="submit"].btn-login');
await page.waitForTimeout(1600);
for (const t of ['light', 'dark']) {
  await page.evaluate(x => document.documentElement.setAttribute('data-theme', x), t);
  await page.waitForTimeout(700);
  const info = await page.evaluate(() => {
    const brand = document.querySelector('.sidebar .brand');
    const imgs = [...document.querySelectorAll('.sidebar .brand img')].map(i => ({
      src: i.getAttribute('src').split('/').pop(),
      display: getComputedStyle(i).display,
      h: Math.round(i.getBoundingClientRect().height),
    }));
    return { brandH: Math.round(brand.getBoundingClientRect().height), brandPad: getComputedStyle(brand).padding, imgs,
             navTop: Math.round(document.querySelector('.sidebar nav').getBoundingClientRect().top) };
  });
  console.log(t, JSON.stringify(info));
}
await browser.close();
