import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 430, height: 940 }, deviceScaleFactor: 2 });
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);

// --- login like a real user ---
await page.fill('#loginPhoneInput', '09123456789');
await page.click('#screen-login button[type="submit"], #screen-login .btn-teal, #screen-login form button');
await page.waitForTimeout(800);
const boxes = await page.$$('#screen-otp .otp-box');
for (let i = 0; i < boxes.length; i++) await boxes[i].fill(String(i + 1));
await page.waitForTimeout(300);
// click verify button (last button in otp screen)
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll('#screen-otp button'));
  const b = btns.find(x => /تأیید|ورود|ادامه/.test(x.textContent));
  (b || btns[btns.length - 1]).click();
});
await page.waitForTimeout(1200);
const afterLogin = await page.evaluate(() => document.querySelector('.screen.active')?.id);
console.log('active screen after login:', afterLogin);
await page.screenshot({ path: '/home/user/shots/A-home-after-login.png' });

// --- tap خدمات in the bottom nav of home ---
await page.evaluate(() => {
  const item = Array.from(document.querySelectorAll('#screen-home .nav-item')).find(n => n.textContent.trim() === 'خدمات');
  item.click();
});
await page.waitForTimeout(900);
const navWorked = await page.evaluate(() => document.querySelector('.screen.active')?.id);
console.log('active screen after tapping خدمات:', navWorked);
await page.screenshot({ path: '/home/user/shots/B-services-list.png' });

// --- open every service, verify content ---
const ids = await page.evaluate(() => EPLAK_SERVICES.map(s => s.id));
console.log('services:', ids.join(', '));
for (const id of ids) {
  const info = await page.evaluate(sid => {
    showScreen('screen-services');
    openServiceDetail(sid);
    const w = document.querySelector('#serviceDetailWrap');
    return {
      active: document.querySelector('.screen.active')?.id,
      title: w.querySelector('h2')?.textContent.trim(),
      introLen: (w.querySelector('.svc-intro-card p')?.textContent || '').trim().length,
      caps: w.querySelectorAll('.svc-cap').length,
      modules: w.querySelectorAll('.svc-module').length,
      btn: w.querySelector('.svc-action-btn span')?.textContent.trim(),
    };
  }, id);
  const ok = info.active === 'screen-service-detail' && info.introLen > 100 && (info.caps > 0 || info.modules > 0) && !!info.btn;
  console.log((ok ? 'PASS ' : 'FAIL ') + id + ' → ' + JSON.stringify(info));
}

// --- action buttons ---
await page.evaluate(() => { showScreen('screen-services'); openServiceDetail('payment'); });
await page.waitForTimeout(500);
await page.evaluate(() => document.querySelector('#serviceDetailWrap .svc-action-btn').click());
await page.waitForTimeout(800);
console.log('payment action →', await page.evaluate(() => document.querySelector('.screen.active')?.id));
await page.screenshot({ path: '/home/user/shots/C-payment-from-services.png' });

await page.evaluate(() => { showScreen('screen-services'); openServiceDetail('recycling'); });
await page.waitForTimeout(400);
await page.evaluate(() => document.querySelector('#serviceDetailWrap .svc-action-btn').click());
await page.waitForTimeout(800);
console.log('recycling action →', await page.evaluate(() => document.querySelector('.screen.active')?.id));
console.log('toast visible:', await page.evaluate(() => document.getElementById('globalToast')?.classList.contains('show')));

// --- day mode services ---
await page.evaluate(() => { applyTheme(true); showScreen('screen-services'); });
await page.waitForTimeout(800);
await page.screenshot({ path: '/home/user/shots/D-services-day.png' });

console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'NO JS ERRORS');
await browser.close();
