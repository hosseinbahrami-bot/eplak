import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
const errors = [];
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

const PHONE = '09123456789';

// ---- ورود به اپ ----
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1500);
await page.evaluate((phone) => {
  document.getElementById('loginPhoneInput').value = phone;
  if (typeof sendOtp === 'function') sendOtp();
}, PHONE);
await page.waitForTimeout(1200);
await page.evaluate(() => {
  document.querySelectorAll('.otp-box').forEach(i => { i.value = '1'; });
  if (typeof verifyOtp === 'function') verifyOtp();
});
await page.waitForTimeout(2200);
const phone = await page.evaluate(() => (typeof userProfile !== 'undefined' ? userProfile.rawPhone : ''));
console.log('وضعیت ورود:', phone || '(ناموفق)');

// ---- همگام‌سازی دستی ----
const sync = await page.evaluate(async () => {
  if (typeof window.syncLiveContent !== 'function') return 'no-function';
  return await window.syncLiveContent();
});
console.log('نتیجه همگام‌سازی:', JSON.stringify(sync));

// ---- بررسی تب اخبار ----
const newsInfo = await page.evaluate(() => ({
  count: (typeof newsData !== 'undefined') ? newsData.length : -1,
  titles: (typeof newsData !== 'undefined') ? newsData.map(n => n.title) : [],
  listHtml: (document.getElementById('newsListWrap') || {}).innerHTML?.length || 0,
}));
console.log('\n=== تب «اخبار و اطلاعات» ===');
console.log('  تعداد:', newsInfo.count, '| طول HTML:', newsInfo.listHtml);
newsInfo.titles.forEach(t => console.log('   •', t));

// ---- بررسی تب دانستنی‌ها ----
await page.evaluate(() => { if (typeof showScreen === 'function') showScreen('screen-news'); });
await page.waitForTimeout(800);
await page.evaluate(() => { if (typeof switchNewsTab === 'function') switchNewsTab('knowledge'); });
await page.waitForTimeout(900);
const tips = await page.evaluate(() => {
  const w = document.getElementById('knowledgeListWrap');
  return { cards: w ? w.children.length : -1, text: w ? w.textContent.replace(/\s+/g, ' ').trim().slice(0, 220) : '' };
});
console.log('\n=== تب «دانستنی‌های ورامین» ===');
console.log('  تعداد کارت‌های مدیریت‌شده:', tips.cards);
console.log('  متن:', tips.text);

// ---- بررسی نوار آخرین اخبار در پیشخوان ----
await page.evaluate(() => { if (typeof showScreen === 'function') showScreen('screen-dashboard'); });
await page.waitForTimeout(1200);
const dash = await page.evaluate(() => {
  const w = document.getElementById('dashNewsWrap');
  return { cards: w ? w.children.length : -1, text: w ? w.textContent.replace(/\s+/g, ' ').trim().slice(0, 160) : '' };
});
console.log('\n=== نوار «آخرین اخبار» در پیشخوان ===');
console.log('  تعداد:', dash.cards, '|', dash.text);

// ---- ارسال اعلان جدید از ادمین و بررسی دریافت در اپ ----
const adminCtx = await browser.newContext();
const admin = await adminCtx.newPage();
await admin.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await admin.fill('input[name="username"]', 'admin');
await admin.fill('input[name="password"]', 'admin123');
await admin.click('button[type="submit"].btn-login');
await admin.waitForTimeout(1500);
await admin.goto('http://127.0.0.1:8081/notifications.php', { waitUntil: 'networkidle' });
await admin.fill('#title', 'اعلان تستی زنده');
await admin.fill('#body', 'این اعلان باید بلافاصله در اپلیکیشن دیده شود.');
await admin.check('input[value="selected"]');
await admin.waitForTimeout(400);
await admin.check(`input[name="phones[]"][value="${PHONE}"]`);
await admin.evaluate(() => { window.confirm = () => true; });
await admin.click('button[type="submit"].btn-primary');
await admin.waitForTimeout(2000);
console.log('\nارسال اعلان از ادمین:', admin.url().includes('sent=') ? '✅ موفق' : '❌ ناموفق');

// ---- همگام‌سازی دوباره در اپ ----
await page.evaluate(async () => { await window.syncLiveContent(); });
await page.waitForTimeout(1000);
const notifs = await page.evaluate(() => (typeof notifications !== 'undefined' ? notifications.map(n => ({ id: n.id, title: n.title, read: n.read })) : []));
console.log('اعلان‌های دریافت‌شده در اپ:', JSON.stringify(notifs, null, 1));

await page.screenshot({ path: '/home/user/shots/APP-live-news.png' });
console.log('\n' + (errors.length ? '❌ خطاها:\n' + errors.slice(0, 5).join('\n') : '✅ بدون خطای JS'));
await browser.close();
