import { chromium } from 'playwright';

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await ctx.newPage();

await page.route('**/*', async route => {
  const res = await route.fetch();
  const headers = { ...res.headers() };
  delete headers['set-cookie'];
  delete headers['Set-Cookie'];
  await route.fulfill({ response: res, headers });
});

page.on('request', r => {
  if (r.url().includes('8081') && r.method() === 'POST') {
    console.log('POST ->', r.url(), '| body:', r.postData());
  }
});
page.on('response', async r => {
  if (r.url().includes('8081')) {
    const loc = r.headers()['location'];
    console.log('RESP', r.status(), r.url().replace('http://127.0.0.1:8081', ''), loc ? '| Location: ' + loc : '');
  }
});

await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(800);

// آیا فرم شامل فیلد مخفی نشست هست؟
const hidden = await page.evaluate(() => {
  const inp = document.querySelector('input[name="eplak_admin"]');
  return inp ? inp.value : null;
});
console.log('hidden session field in form:', hidden ? hidden.slice(0, 10) + '...' : 'NONE');

await page.fill('input[name="username"]', 'admin');
await page.fill('input[name="password"]', 'admin123');
await page.click('button[type="submit"].btn-login');
await page.waitForTimeout(2000);
console.log('final url:', page.url().replace('http://127.0.0.1:8081', ''));

await browser.close();
