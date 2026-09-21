import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
const errors = [];
page.on('pageerror', e => errors.push(e.message));

await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
await page.evaluate(() => { document.getElementById('loginPhoneInput').value = '09123456789'; sendOtp(); });
await page.waitForTimeout(900);
await page.evaluate(() => { document.querySelectorAll('.otp-box').forEach(i => i.value='1'); verifyOtp(); });
await page.waitForTimeout(2000);
await page.evaluate(async () => { await window.syncLiveContent(); });
await page.waitForTimeout(800);

// نمایش صفحه اعلان‌ها
await page.evaluate(() => showScreen('screen-notifications'));
await page.waitForTimeout(900);
const ui = await page.evaluate(() => {
  const w = document.getElementById('notifListWrap');
  return {
    items: w ? w.children.length : -1,
    text: w ? w.textContent.replace(/\s+/g,' ').trim().slice(0, 250) : '',
    dot: (document.getElementById('homeNotifDot') || {}).style?.display || 'n/a',
  };
});
console.log('=== صفحه اعلان‌ها در اپ ===');
console.log('  تعداد آیتم‌ها:', ui.items);
console.log('  متن:', ui.text);
await page.screenshot({ path: '/home/user/shots/APP-notifications.png' });

// ارسال گروهی به همه کاربران
const admin = await (await browser.newContext()).newPage();
await admin.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await admin.fill('input[name="username"]','admin');
await admin.fill('input[name="password"]','admin123');
await admin.click('button[type="submit"].btn-login');
await admin.waitForTimeout(1400);
await admin.goto('http://127.0.0.1:8081/notifications.php', { waitUntil: 'networkidle' });
await admin.fill('#title','اطلاعیه عمومی شهروندان');
await admin.fill('#body','این پیام برای همه کاربران ارسال می‌شود.');
await admin.evaluate(() => { window.confirm = () => true; });
await admin.click('button[type="submit"].btn-primary');
await admin.waitForTimeout(2000);
console.log('\nارسال گروهی (همه کاربران):', admin.url());

// بررسی تاریخچه ارسال
await admin.goto('http://127.0.0.1:8081/notifications.php', { waitUntil: 'networkidle' });
const rows = await admin.evaluate(() => [...document.querySelectorAll('tbody tr')].map(r => r.textContent.replace(/\s+/g,' ').trim().slice(0,70)));
console.log('تاریخچه ارسال‌ها:'); rows.forEach(r => console.log('  •', r));
await admin.screenshot({ path: '/home/user/shots/ADMIN-notifications.png' });

// مشاهده گیرندگان
await admin.goto('http://127.0.0.1:8081/notification_view.php?id=1', { waitUntil: 'networkidle' });
const recips = await admin.evaluate(() => [...document.querySelectorAll('tbody tr')].length);
console.log('گیرندگان ارسال شماره ۱:', recips, 'ردیف');
await admin.screenshot({ path: '/home/user/shots/ADMIN-notification-view.png' });

console.log(errors.length ? '\n❌ خطا: ' + errors.join(' | ') : '\n✅ بدون خطا');
await browser.close();
