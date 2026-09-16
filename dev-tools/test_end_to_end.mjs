import { chromium } from 'playwright';
const browser = await chromium.launch();
const PHONE = '09123456789';

// ── اپ شهروندی ──
const app = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
const errors = [];
app.on('pageerror', e => errors.push(e.message));
await app.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await app.waitForTimeout(1200);
await app.evaluate(p => { document.getElementById('loginPhoneInput').value = p; sendOtp(); }, PHONE);
await app.waitForTimeout(900);
await app.evaluate(() => { document.querySelectorAll('.otp-box').forEach(i => i.value='1'); verifyOtp(); });
await app.waitForTimeout(2000);
await app.evaluate(async () => { await window.syncLiveContent(); });
await app.waitForTimeout(600);

const before = await app.evaluate(() => newsData.map(n => n.title));
console.log('پیش از افزودن — تعداد اخبار در اپ:', before.length);

// ── ادمین: افزودن خبر جدید ──
const admin = await (await browser.newContext()).newPage();
await admin.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await admin.fill('input[name="username"]','admin');
await admin.fill('input[name="password"]','admin123');
await admin.click('button[type="submit"].btn-login');
await admin.waitForTimeout(1400);

const TITLE = 'افتتاح کتابخانه مرکزی جدید ورامین';
await admin.goto('http://127.0.0.1:8081/news_add.php', { waitUntil: 'networkidle' });
await admin.fill('#title', TITLE);
await admin.fill('#summary', 'کتابخانه مرکزی با ظرفیت ۵۰ هزار جلد کتاب افتتاح شد.');
await admin.fill('#body', 'کتابخانه مرکزی ورامین با زیربنای سه هزار متر مربع و ظرفیت بیش از پنجاه هزار جلد کتاب، با حضور مسئولان استانی افتتاح شد. بخش کودک، سالن مطالعه و بخش مرجع از جمله بخش‌های این مجموعه هستند.');
await admin.fill('#icon', '📚');
await admin.fill('#sort_order', '0');
await admin.click('button[type="submit"].btn-primary');
await admin.waitForTimeout(1600);
console.log('افزودن خبر از ادمین:', admin.url().includes('success') ? '✅ موفق' : '❌ ' + admin.url());

// ── همگام‌سازی اپ ──
await app.evaluate(async () => { await window.syncLiveContent(); });
await app.waitForTimeout(900);
const after = await app.evaluate(() => newsData.map(n => n.title));
console.log('پس از افزودن — تعداد اخبار در اپ:', after.length);
console.log('خبر جدید در اپ نمایش داده می‌شود:', after.includes(TITLE) ? '✅ بله' : '❌ خیر');

// ── ارسال اعلان گروهی ──
await admin.goto('http://127.0.0.1:8081/notifications.php', { waitUntil: 'networkidle' });
await admin.fill('#title', 'قطعی برنامه‌ریزی‌شده آب');
await admin.fill('#body', 'به اطلاع می‌رساند آب برخی مناطق فردا از ساعت ۸ تا ۱۴ قطع خواهد بود.');
await admin.evaluate(() => { window.confirm = () => true; });
await admin.click('button[type="submit"].btn-primary');
await admin.waitForTimeout(1800);
console.log('ارسال اعلان گروهی:', admin.url().includes('sent=') ? '✅ ' + admin.url().split('sent=')[1] + ' گیرنده' : '❌');

await app.evaluate(async () => { await window.syncLiveContent(); });
await app.waitForTimeout(900);
const notifs = await app.evaluate(() => notifications.map(n => n.title));
console.log('اعلان در اپ:', notifs.includes('قطعی برنامه‌ریزی‌شده آب') ? '✅ دریافت شد' : '❌ دریافت نشد');
console.log('فهرست اعلان‌های اپ:', JSON.stringify(notifs));

// ── نمایش نهایی ──
await app.evaluate(() => { showScreen('screen-news'); switchNewsTab('news'); });
await app.waitForTimeout(1000);
await app.screenshot({ path: '/home/user/shots/APP-final-news.png' });
await admin.goto('http://127.0.0.1:8081/news.php', { waitUntil: 'networkidle' });
await admin.screenshot({ path: '/home/user/shots/ADMIN-final-news.png' });

console.log(errors.length ? '\n❌ خطا: ' + errors.join(' | ') : '\n✅ بدون خطای JS');
await browser.close();
