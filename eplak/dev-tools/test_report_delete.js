/* dev-tools/test_report_delete.js
   تست رگرسیون: «گزارش حذف‌شده نباید با همگام‌سازی پس‌زمینه برگردد»

   - ماژول‌های واقعی اپ (state/storage/reports) داخل jsdom بارگذاری می‌شوند
   - یک بک‌اند ساختگی با همان قرارداد api/reports.php شبیه‌سازی می‌شود
   - سناریوها: حذف عادی، حذف هم‌زمان با polling، حذف هنگام قطع سرور، حذف گزارش تازه‌ثبت‌شده

   اجرا:  node dev-tools/test_report_delete.js
*/
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const ROOT = path.join(__dirname, '..', 'eplak-fixed');
const read = (p) => fs.readFileSync(path.join(ROOT, p), 'utf8');

/* ── بک‌اند ساختگی ─────────────────────────────────────────────── */
function makeBackend() {
  const state = { rows: [], nextId: 1, offline: false, deleteCalls: [], listCalls: 0, delayMs: 0 };
  const owner = '09120000001';
  state.rows.push({ id: state.nextId++, user_phone: owner, title: 'چراغ خیابان خراب', description: 'x', status: 'pending', created_at: '2026-09-20 10:00:00' });
  state.rows.push({ id: state.nextId++, user_phone: owner, title: 'چاله در معبر', description: 'y', status: 'pending', created_at: '2026-09-21 10:00:00' });
  state.rows.push({ id: state.nextId++, user_phone: '09120000002', title: 'گزارش شخص دیگر', description: 'z', status: 'pending', created_at: '2026-09-21 11:00:00' });

  const json = (obj, status = 200) => ({
    ok: status >= 200 && status < 300, status,
    json: async () => obj, text: async () => JSON.stringify(obj)
  });
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));

  async function fetchImpl(url, opts = {}) {
    if (state.offline) throw new TypeError('Failed to fetch');
    if (state.delayMs) await sleep(state.delayMs);
    const u = new URL(String(url), 'http://mock/');
    const method = (opts.method || 'GET').toUpperCase();
    let body = {};
    try { body = opts.body ? JSON.parse(opts.body) : {}; } catch (e) { body = {}; }

    if (u.pathname.endsWith('/reports.php')) {
      const isDelete = method === 'DELETE' || u.searchParams.get('action') === 'delete' || body.action === 'delete';
      if (method === 'GET') {
        state.listCalls++;
        const phone = u.searchParams.get('phone') || '';
        if (!/^09\d{9}$/.test(phone)) return json({ success: false, error: 'phone required' }, 400);
        return json({ success: true, reports: state.rows.filter(r => r.user_phone === phone) });
      }
      if (isDelete) {
        const id = parseInt(u.searchParams.get('id') || body.id || 0, 10);
        const phone = u.searchParams.get('phone') || body.phone || '';
        state.deleteCalls.push({ id, phone });
        if (!(id > 0)) return json({ success: false, error: 'invalid id' }, 400);
        if (!/^09\d{9}$/.test(phone)) return json({ success: false, error: 'phone required' }, 400);
        const before = state.rows.length;
        state.rows = state.rows.filter(r => !(r.id === id && r.user_phone === phone));
        if (state.rows.length === before) return json({ success: false, error: 'not found' }, 404);
        return json({ success: true, deleted_id: id });
      }
      if (method === 'POST') {
        const id = state.nextId++;
        state.rows.unshift({ id, user_phone: body.phone || body.userPhone, title: body.title, description: body.description, status: 'pending', created_at: '2026-09-22 09:00:00' });
        return json({ success: true, id, tracking_code: 'EP-1403-' + String(id).padStart(4, '0') });
      }
    }
    if (u.pathname.endsWith('/tickets.php')) return json({ success: true, tickets: [] });
    if (u.pathname.endsWith('/departments.php')) return json({ success: true, departments: [] });
    if (u.pathname.endsWith('/users.php')) return json({ success: true, user: null });
    return json({ success: false }, 404);
  }
  return { state, fetchImpl, owner };
}

/* ── محیط مرورگر ساختگی ─────────────────────────────────────────── */
function makeApp(backend) {
  const html = `<!doctype html><html><body>
    <div id="reportsListWrap"></div><div id="reportsCountBadge"></div>
    <div id="reportsFilterTabs"><button class="filter-tab active" data-filter="all"></button></div>
    <div id="profileReportsList"></div><div id="trackRecentList"></div>
    <div id="userTicketsListWrap"></div>
  </body></html>`;
  const dom = new JSDOM(html, { url: 'http://localhost/eplak/index.html', runScripts: 'dangerously', pretendToBeVisual: true,
    beforeParse(w) {
      w.fetch = backend.fetchImpl;
      w.showToast = () => {};
      w.showScreen = () => {};
      w.goBack = () => {};
      w.EplakIcons = { get: (x) => x };
      w.i18n = { getLanguage: () => 'fa', t: (x) => x };
      w.PointerEvent = w.MouseEvent;
    } });
  const w = dom.window;
  // اسکریپت‌ها به‌صورت تگ <script> کلاسیک اجرا می‌شوند تا let/const سطح بالا (مثل reports) مثل مرورگر واقعی سراسری باشند
  for (const f of ['core/state.js', 'core/storage.js', 'modules/reports.js']) {
    const el = w.document.createElement('script');
    el.textContent = read(f);
    w.document.body.appendChild(el);
  }
  return w;
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(cond, msg) {
  if (cond) console.log('  ✔', msg);
  else { failures++; console.log('  ✘', msg); }
}
const titles = (w) => w.eval('reports').map(r => r.title);
const R = (w) => w.eval('reports');

(async () => {
  /* ─ سناریو ۱: حذف عادی؛ سپس چند بار همگام‌سازی پس‌زمینه ─ */
  {
    console.log('\n[1] حذف عادی + همگام‌سازی پس‌زمینه');
    const b = makeBackend(); const w = makeApp(b);
    w.loginWithPhone(b.owner);
    await w.loadReportsFromBackend(b.owner, { silent: true });
    check(R(w).length === 2, `دو گزارش کاربر بارگذاری شد (${titles(w).join(' | ')})`);
    check(!titles(w).includes('گزارش شخص دیگر'), 'گزارش کاربر دیگر دیده نمی‌شود');

    await w.deleteReport('1');
    check(R(w).length === 1, 'بلافاصله از لیست حذف شد');
    check(b.state.deleteCalls.length === 1 && b.state.deleteCalls[0].id === 1 && b.state.deleteCalls[0].phone === b.owner, 'درخواست حذف با شناسه‌ی عددی و شماره‌ی مالک به سرور رفت');
    check(!b.state.rows.some(r => r.id === 1), 'در سرور هم حذف شد');

    for (let i = 0; i < 3; i++) await w.loadReportsFromBackend(b.owner, { silent: true });
    check(R(w).length === 1 && !titles(w).includes('چراغ خیابان خراب'), 'بعد از ۳ بار همگام‌سازی برنگشت');
    const saved = JSON.parse(w.localStorage.getItem('eplak_reports_' + b.owner));
    check(saved.length === 1, 'localStorage هم به‌روز است');
  }

  /* ─ سناریو ۲: مسابقه — GET قبل از حذف شروع شده و بعد از حذف تمام می‌شود ─ */
  {
    console.log('\n[2] مسابقه با polling (پاسخ قدیمی سرور بعد از حذف می‌رسد)');
    const b = makeBackend(); const w = makeApp(b);
    w.loginWithPhone(b.owner);
    await w.loadReportsFromBackend(b.owner, { silent: true });

    b.state.delayMs = 120;                     // پاسخ سرور کند است
    const staleSync = w.loadReportsFromBackend(b.owner, { silent: true }); // شبیه‌ساز polling live.js
    await sleep(10);
    b.state.delayMs = 0;
    const del = w.deleteReport('2');
    await Promise.all([staleSync, del]);
    await w.loadReportsFromBackend(b.owner, { silent: true });
    check(!titles(w).includes('چاله در معبر'), 'گزارش حذف‌شده با پاسخ قدیمی سرور برنگشت');
    check(!b.state.rows.some(r => r.id === 2), 'و در سرور هم حذف شده');
  }

  /* ─ سناریو ۳: سرور در دسترس نیست؛ حذف باید بعداً اعمال شود ─ */
  {
    console.log('\n[3] حذف در حالت آفلاین → اعمال بعدی');
    const b = makeBackend(); const w = makeApp(b);
    w.loginWithPhone(b.owner);
    await w.loadReportsFromBackend(b.owner, { silent: true });

    b.state.offline = true;
    await w.deleteReport('1');
    check(R(w).length === 1, 'در حالت آفلاین از لیست کاربر حذف شد');
    await w.loadReportsFromBackend(b.owner, { silent: true }); // شکست می‌خورد
    check(R(w).length === 1, 'همگام‌سازی ناموفق چیزی را برنگرداند');

    b.state.offline = false;
    check(b.state.rows.some(r => r.id === 1), 'هنوز در سرور هست (چون آفلاین بودیم)');
    await w.loadReportsFromBackend(b.owner, { silent: true }); // باید اول حذف معوق را بفرستد
    check(!b.state.rows.some(r => r.id === 1), 'با برگشت اینترنت، حذف معوق در سرور اعمال شد');
    check(R(w).length === 1 && !titles(w).includes('چراغ خیابان خراب'), 'و همچنان در لیست نیست');
    check(JSON.parse(w.localStorage.getItem('eplak_pending_report_deletes')).length === 0, 'صف حذف معوق خالی شد');
  }

  /* ─ سناریو ۴: ثبت گزارش جدید و حذف فوری آن ─ */
  {
    console.log('\n[4] ثبت گزارش جدید → حذف فوری (شناسه‌ی سروری باید استفاده شود)');
    const b = makeBackend(); const w = makeApp(b);
    w.loginWithPhone(b.owner);
    await w.loadReportsFromBackend(b.owner, { silent: true });
    // شبیه‌سازی فرم
    w.eval(`reportDraft = { type: 'سایر', department: 'خدمات شهری', subDepartment: 'نظافت', desc: 'زباله جمع نشده', location: 'خیابان امام', photos: [] };`);
    w.submitNewReport();
    await sleep(30); // ارسال پس‌زمینه
    const created = R(w).find(r => r.title.startsWith('زباله'));
    check(!!created, 'گزارش جدید در لیست است');
    check(/^\d+$/.test(String(created.id)), `شناسه‌ی گزارش بعد از ثبت، شناسه‌ی سرور شد (${created.id})`);
    check(b.state.rows.some(r => r.title === created.title), 'در سرور ثبت شد');

    await w.deleteReport(String(created.id));
    check(!b.state.rows.some(r => r.title === created.title), 'حذف فوری بعد از ثبت، در سرور اعمال شد');
    for (let i = 0; i < 2; i++) await w.loadReportsFromBackend(b.owner, { silent: true });
    check(!R(w).some(r => r.title === created.title), 'و با همگام‌سازی برنگشت');
  }

  /* ─ سناریو ۵: حذف با شناسه‌ی کد پیگیری (از صفحه‌ی جزئیات) ─ */
  {
    console.log('\n[5] حذف از صفحه جزئیات (activeReportId)');
    const b = makeBackend(); const w = makeApp(b);
    w.loginWithPhone(b.owner);
    await w.loadReportsFromBackend(b.owner, { silent: true });
    w.eval(`activeReportId = '2';`);
    w.deleteCurrentOpenReport();
    await sleep(20);
    check(!R(w).some(r => r.id === '2'), 'از لیست حذف شد');
    check(!b.state.rows.some(r => r.id === 2), 'در سرور حذف شد');
  }

  /* ─ سناریو ۶: ثبت گزارش در حالت آفلاین → بعداً به سرور می‌رسد، بدون تکرار ─ */
  {
    console.log('\n[6] ثبت آفلاین → ارسال بعدی بدون تکرار');
    const b = makeBackend(); const w = makeApp(b);
    w.loginWithPhone(b.owner);
    await w.loadReportsFromBackend(b.owner, { silent: true });
    b.state.offline = true;
    w.eval(`reportDraft = { type: 'سایر', department: 'خدمات شهری', subDepartment: 'فضای سبز', desc: 'درخت شکسته', location: 'پارک شهر', photos: [] };`);
    w.submitNewReport();
    await sleep(30);
    check(R(w).some(r => r.title === 'درخت شکسته'), 'گزارش آفلاین در لیست کاربر است');
    await w.loadReportsFromBackend(b.owner, { silent: true });
    check(R(w).some(r => r.title === 'درخت شکسته'), 'همگام‌سازی ناموفق آن را پاک نکرد');
    b.state.offline = false;
    await w.loadReportsFromBackend(b.owner, { silent: true });
    const srv = b.state.rows.filter(r => r.title === 'درخت شکسته');
    check(srv.length === 1, 'با برگشت اینترنت، دقیقاً یک بار در سرور ثبت شد');
    const local = R(w).filter(r => r.title === 'درخت شکسته');
    check(local.length === 1 && String(local[0].id) === String(srv[0].id), 'در لیست کاربر یک نسخه با شناسه‌ی سرور وجود دارد (بدون تکرار)');
    await w.loadReportsFromBackend(b.owner, { silent: true });
    check(R(w).filter(r => r.title === 'درخت شکسته').length === 1, 'بعد از همگام‌سازی مجدد هم تکراری نشد');
    check(R(w).length === 3, `تعداد کل درست است (${R(w).length})`);
  }

  console.log(failures ? `\n❌ ${failures} مورد ناموفق` : '\n✅ همه‌ی سناریوها موفق');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('TEST CRASH', e); process.exit(2); });
