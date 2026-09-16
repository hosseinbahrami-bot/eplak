/* modules/dashboard.js — پیشخوان: اخبار، پرداخت عوارض، نقشه شهر و اعلان‌ها */
/* استخراج‌شده عیناً از فایل اصلی app_01.html بدون تغییر منطق */

  /* =========================================================
     تبدیل تاریخ میلادی به شمسی (الگوریتم جلالی)
  ========================================================= */
  function toJalali(gy, gm, gd) {
    const g_d_m = [0,31,59,90,120,151,181,212,243,273,304,334];
    let jy = (gy <= 1600) ? 0 : 979;
    gy -= (gy <= 1600) ? 621 : 1600;
    let gy2 = (gm > 2) ? (gy + 1) : gy;
    let days = (365 * gy) + (Math.floor((gy2 + 3) / 4)) - (Math.floor((gy2 + 99) / 100))
             + (Math.floor((gy2 + 399) / 400)) - 80 + gd + g_d_m[gm - 1];
    jy += 33 * Math.floor(days / 12053);
    days %= 12053;
    jy += 4 * Math.floor(days / 1461);
    days %= 1461;
    if (days > 365) { jy += Math.floor((days - 1) / 365); days = (days - 1) % 365; }
    let jm = (days < 186) ? 1 + Math.floor(days / 31) : 7 + Math.floor((days - 186) / 30);
    let jd = 1 + ((days < 186) ? (days % 31) : ((days - 186) % 30));
    return [jy, jm, jd];
  }

  const JALALI_MONTHS = [
    'فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور',
    'مهر','آبان','آذر','دی','بهمن','اسفند'
  ];
  const JALALI_WEEKDAYS = ['یک‌شنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنج‌شنبه','جمعه','شنبه'];

  function getJalaliDateStr(date) {
    const [jy, jm, jd] = toJalali(date.getFullYear(), date.getMonth() + 1, date.getDate());
    const weekday = JALALI_WEEKDAYS[date.getDay()];
    const short = toPersianDigits(jy) + '/' + toPersianDigits(String(jm).padStart(2,'0')) + '/' + toPersianDigits(String(jd).padStart(2,'0'));
    const full  = toPersianDigits(jd) + ' ' + JALALI_MONTHS[jm - 1] + ' ' + toPersianDigits(jy);
    return { short, full, weekday };
  }

  /* ساعت زنده — هر ثانیه به‌روز می‌شود */
  let _dashClockTimer = null;
  function startDashClock() {
    if (_dashClockTimer) clearInterval(_dashClockTimer);
    function tick() {
      const now  = new Date();
      const hh   = String(now.getHours()).padStart(2, '0');
      const mm   = String(now.getMinutes()).padStart(2, '0');
      const ss   = String(now.getSeconds()).padStart(2, '0');

      const clkEl = document.getElementById('dashLiveClock');
      if (clkEl) clkEl.innerHTML = toPersianDigits(hh) + ':' + toPersianDigits(mm) +
        '<span class="dash-clock-secs" id="dashClockSecs">:' + toPersianDigits(ss) + '</span>';

      const jalali = getJalaliDateStr(now);
      const fullEl = document.getElementById('dashFullDate');
      if (fullEl) fullEl.textContent = jalali.full;
      const wdEl = document.getElementById('dashWeekDay');
      if (wdEl) wdEl.textContent = jalali.weekday;
    }
    tick();
    _dashClockTimer = setInterval(tick, 1000);
  }

  /* =========================================================
     Personal Dashboard (تب پیشخوان در نوار پایین)
  ========================================================= */
  function renderDashboard() {
    /* راه‌اندازی ساعت زنده */
    startDashClock();

    const pendingCount = reports.filter(r => r.status === 'pending').length;
    const doneCount = reports.filter(r => r.status === 'done').length;
    const debt = payments.filter(p => p.status === 'pending').reduce((s, p) => s + p.amount, 0);
    const unreadCount = notifications.filter(n => !n.read).length;

    const setText = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setText('dashPendingCount', toPersianDigits(pendingCount));
    setText('dashDoneCount', toPersianDigits(doneCount));
    setText('dashDebtAmount', debt > 0 ? formatToman(debt) : 'بدون بدهی');
    setText('dashNotifCount', toPersianDigits(unreadCount));

    const dot = document.getElementById('dashNotifDot');
    if (dot) dot.style.display = unreadCount > 0 ? 'block' : 'none';

    const activityWrap = document.getElementById('dashActivityWrap');
    if (activityWrap) {
      const recent = reports.slice(0, 3);
      activityWrap.innerHTML = recent.length === 0
        ? `<div style="text-align:center; padding:24px 10px; color:var(--text-muted); font-size:13px;">هنوز فعالیتی ثبت نشده است</div>`
        : recent.map(r => `
          <div class="report-item" onclick="openReportDetail('${r.id}')">
            <span class="report-status ${STATUS_CLASS[r.status]}">${STATUS_LABEL[r.status]}</span>
            <div class="report-info">
              <h4>${escapeHtml(r.title)}</h4>
              <p>${escapeHtml(r.location)} - ${r.date}</p>
            </div>
            <div class="report-icon-box" style="background:${r.iconBg};">${r.icon}</div>
          </div>
        `).join('');
    }

    const newsWrap = document.getElementById('dashNewsWrap');
    if (newsWrap) {
      newsWrap.innerHTML = newsData.slice(0, 2).map(n => `
        <div class="mini-news-card" onclick="openNewsDetail('${n.id}')">
          <div class="mini-news-text">
            <h4>${escapeHtml(n.title)}</h4>
            <p>${n.date}</p>
          </div>
          <div class="mini-news-icon">${n.icon}</div>
        </div>
      `).join('');
    }
  }

  function filterReportsAndGo(filter) {
    showScreen('screen-reports');
    const tab = document.querySelector(`#reportsFilterTabs .filter-tab[data-filter="${filter}"]`);
    if (tab) filterReports(filter, tab);
    else renderReportsList(filter);
  }

  /* =========================================================
     News
  ========================================================= */
  function renderNewsList() {
    const wrap = document.getElementById('newsListWrap');
    if (!wrap) return;
    wrap.innerHTML = newsData.map(n => `
      <div class="glass-card" style="padding:14px; display:flex; gap:12px; align-items:center; cursor:pointer;" onclick="openNewsDetail('${n.id}')">
        <div class="promo-img" style="width:60px; height:60px; flex-shrink:0;">
          <div class="promo-img-bg" style="font-size:24px;">${n.icon}</div>
        </div>
        <div style="flex:1; text-align:right;">
          <h4 style="font-size:13px; font-weight:700; line-height:1.5;">${escapeHtml(n.title)}</h4>
          <p style="font-size:11px; color:var(--text-muted); margin-top:4px; line-height:1.5;">${escapeHtml(n.summary)}</p>
          <p style="font-size:10px; color:var(--text-muted); margin-top:6px;">${n.date}</p>
        </div>
      </div>
    `).join('');
  }

  function openNewsDetail(id) {
    const n = newsData.find(x => x.id === id);
    if (!n) return;
    document.getElementById('newsDetailImg').textContent = n.icon;
    document.getElementById('newsDetailTitle').textContent = n.title;
    document.getElementById('newsDetailDate').textContent = n.date;
    document.getElementById('newsDetailBody').textContent = n.body;
    showScreen('screen-news-detail');
  }

  /* =========================================================
     News screen — tab switcher (دانستنی‌های ورامین / اخبار و اطلاعات)
  ========================================================= */
  function switchNewsTab(tab, btnEl) {
    const indicator = document.getElementById('newsTabsIndicator');
    const tabs = document.querySelectorAll('#newsTabs .news-tab');
    tabs.forEach(t => t.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');

    if (indicator) {
      indicator.style.transform = (tab === 'news') ? 'translateX(-100%)' : 'translateX(0)';
    }

    document.getElementById('newsPanelKnowledge').classList.toggle('active', tab === 'knowledge');
    document.getElementById('newsPanelNews').classList.toggle('active', tab === 'news');
  }

  /* =========================================================
     Heritage knowledge cards (مسجد جامع / برج علاءالدوله)
  ========================================================= */
  const heritageData = {
    mosque: {
      img: 'assets/img/varamin-mosque.jpg',
      photoClass: '',
      pin: '۷۲۲ ه.ق · دوره ایلخانی',
      title: 'مسجد جامع ورامین',
      body: 'مسجد جامع ورامین، معروف به مسجد جمعه ورامین، یکی از کهن‌ترین و باشکوه‌ترین بناهای برجامانده از دوره ایلخانی در ایران است. ساخت آن در روزگار سلطان محمد خدابنده (الجایتو) آغاز شد و در دوران فرزند و جانشین او، ابوسعید بهادرخان، در سال ۷۲۲ هجری قمری به پایان رسید.\n\nاین مسجد با نقشه‌ای مستطیلی به ابعاد تقریبی ۶۶ در ۴۳ متر، تنها نمونه کامل و یکپارچه مساجد چهارایوانی در ایران است؛ سبکی که از سلجوقیان آغاز شده و در این بنا به اوج پختگی خود رسیده است. گنبدخانه مسجد با گذر از فیل‌پوش‌ها از مربع به هشت‌ضلعی و سپس شانزده‌ضلعی، به گنبدی باشکوه ختم می‌شود.\n\nسردر بلند و کشیده ورودی، کاشی‌کاری‌های معرق فیروزه‌ای و لاجوردی، گچ‌بری‌های ظریف گرداگرد محراب و کتیبه‌های تاریخی به خط ثلث و کوفی، این بنا را به یکی از مهم‌ترین آثار هنری و معماری دوران اسلامی ایران بدل کرده‌اند. در دوران معاصر، استاد محمدکریم پیرنیا، پدر معماری سنتی ایران، مرمت این اثر گران‌بها را بر عهده داشت.',
      tags: ['مسجد جامع', 'معماری ایلخانی', 'میراث ملی']
    },
    tower: {
      img: 'assets/img/varamin-tower.jpg',
      photoClass: ' heritage-photo-tower',
      pin: '۶۸۸ ه.ق · آرامگاهی',
      title: 'برج علاءالدوله ورامین',
      body: 'برج علاءالدوله، که با نام برج علاءالدین نیز شناخته می‌شود، یکی از قدیمی‌ترین برج‌های آرامگاهی به‌جامانده از ایران است. این بنا در سال ۶۸۸ هجری قمری، در اواخر سده هفتم هجری، به دستور فخرالدین بر فراز آرامگاه پدرش، حسن علاءالدوله، حاکم وقت شهر ری، ساخته شد.\n\nبرج از بدنه‌ای استوانه‌ای آجری با چین‌خوردگی‌های عمودی شکل گرفته که در ارتفاعی نزدیک به ۱۷ متر به گنبدی مخروطی و بلند ختم می‌شود؛ ترکیبی که سیمای منحصربه‌فرد و شناخته‌شده این بنا را در میدان مرکزی ورامین رقم زده است. در محل اتصال بخش استوانه‌ای به مخروطی، کتیبه‌ای آجری با خطوط کوفی برگ‌دار حک شده که نام بانی، تاریخ بنا و دعایی برای آرامش روح علاءالدوله را در خود دارد.\n\nنمای بیرونی برج با شمسه‌های آجری و کاشی‌های فیروزه‌ای و لاجوردی تزئین شده است. این اثر در ۱۵ دی ماه ۱۳۱۰ با شماره ثبت ۱۷۷ در فهرست آثار ملی ایران به ثبت رسید و امروزه یکی از نمادهای شناخته‌شده شهر ورامین و مقصد علاقه‌مندان به تاریخ و معماری ایرانی است.',
      tags: ['برج آرامگاهی', 'دوره ایلخانی', 'میراث ملی']
    }
  };

  function openHeritageDetail(key) {
    const h = heritageData[key];
    if (!h) return;
    const imgEl = document.getElementById('heritageDetailImg');
    imgEl.src = h.img;
    imgEl.alt = h.title;
    imgEl.className = 'heritage-photo' + h.photoClass;
    document.getElementById('heritageDetailPin').textContent = h.pin;
    document.getElementById('heritageDetailTitle').textContent = h.title;
    document.getElementById('heritageDetailBody').textContent = h.body;
    document.getElementById('heritageDetailTags').innerHTML = h.tags.map(t => `<span class="vsc-tag">${escapeHtml(t)}</span>`).join('');
    showScreen('screen-heritage-detail');
  }



  /* =========================================================
     Payments
  ========================================================= */
  function formatToman(n) {
    return toPersianDigits(n.toLocaleString('en-US')) + ' تومان';
  }

  function renderPaymentList() {
    const wrap = document.getElementById('paymentListWrap');
    if (!wrap) return;
    const total = payments.filter(p => p.status === 'pending').reduce((s, p) => s + p.amount, 0);
    document.getElementById('paymentTotalDebt').textContent = formatToman(total);
    wrap.innerHTML = payments.map(p => `
      <div class="report-item" onclick="openPaymentDetail('${p.id}')">
        <span class="report-status ${p.status === 'done' ? 'status-done' : 'status-pending'}">${p.status === 'done' ? 'پرداخت‌شده' : 'پرداخت‌نشده'}</span>
        <div class="report-info">
          <h4>${escapeHtml(p.title)}</h4>
          <p>مهلت: ${p.due}</p>
        </div>
        <div class="report-icon-box" style="background:rgba(150,80,255,0.12);">💳</div>
      </div>
    `).join('');
  }

  function openPaymentDetail(id) {
    const p = payments.find(x => x.id === id);
    if (!p) return;
    pendingPaymentId = id;
    document.getElementById('payDetailTitle').textContent = p.title;
    document.getElementById('payDetailCode').textContent = p.code;
    document.getElementById('payDetailDue').textContent = p.due;
    const statusEl = document.getElementById('payDetailStatus');
    statusEl.className = 'report-status ' + (p.status === 'done' ? 'status-done' : 'status-pending');
    statusEl.textContent = p.status === 'done' ? 'پرداخت‌شده' : 'پرداخت‌نشده';
    document.getElementById('payDetailAmount').textContent = formatToman(p.amount);
    const payBtn = document.getElementById('payNowBtn');
    if (p.status === 'done') {
      payBtn.textContent = 'این قبض قبلاً پرداخت شده است';
      payBtn.style.opacity = '0.6';
      payBtn.style.pointerEvents = 'none';
    } else {
      payBtn.textContent = 'پرداخت آنلاین';
      payBtn.style.opacity = '1';
      payBtn.style.pointerEvents = 'auto';
    }
    showScreen('screen-payment-detail');
  }

  function payInvoice() {
    const p = payments.find(x => x.id === pendingPaymentId);
    if (!p) return;
    p.status = 'done';
    if (typeof savePayments === 'function') savePayments();
    showToast('پرداخت با موفقیت انجام شد');
    openPaymentDetail(p.id);
  }


  /* =========================================================
     Map
  ========================================================= */
  function renderMapPlaces() {
    const wrap = document.getElementById('mapPlacesWrap');
    if (!wrap) return;
    wrap.innerHTML = mapPlaces.map(pl => `
      <div class="menu-item" onclick="showToast('مسیر به ${escapeHtml(pl.name)} نمایش داده شد')">
        <span class="menu-item-value">${pl.dist}</span>
        <div class="menu-item-right">
          <div class="menu-item-icon" style="background:${pl.bg};">${pl.icon}</div>
          <span class="menu-item-label">${escapeHtml(pl.name)}</span>
        </div>
      </div>
    `).join('');
  }


  /* =========================================================
     Notifications
  ========================================================= */
  function renderNotifications() {
    const wrap = document.getElementById('notifListWrap');
    if (!wrap) return;
    if (notifications.length === 0) {
      wrap.innerHTML = `<div style="text-align:center; padding:30px 10px; color:var(--text-muted); font-size:13px;">اعلانی وجود ندارد</div>`;
    } else {
      wrap.innerHTML = notifications.map(n => `
        <div class="report-item" onclick="markNotifRead('${n.id}')" style="${n.read ? 'opacity:0.6;' : ''}">
          ${!n.read ? '<span style="width:8px;height:8px;border-radius:50%;background:var(--orange);flex-shrink:0;"></span>' : '<span style="width:8px;height:8px;flex-shrink:0;"></span>'}
          <div class="report-info">
            <h4>${escapeHtml(n.title)}</h4>
            <p>${escapeHtml(n.body)} · ${n.time}</p>
          </div>
          <div class="report-icon-box" style="background:rgba(0,201,167,0.12);">${n.icon}</div>
        </div>
      `).join('');
    }
    updateNotifDot();
  }

  function markNotifRead(id) {
    const n = notifications.find(x => x.id === id);
    if (n) n.read = true;
    if (typeof saveNotifications === 'function') saveNotifications();
    renderNotifications();
  }

  function markAllNotifsRead() {
    notifications.forEach(n => n.read = true);
    if (typeof saveNotifications === 'function') saveNotifications();
    renderNotifications();
    showToast('همه اعلان‌ها خوانده شد');
  }

  function updateNotifDot() {
    const hasUnread = notifications.some(n => !n.read);
    const dot = document.getElementById('homeNotifDot');
    if (dot) dot.style.display = hasUnread ? 'block' : 'none';
    const dashDot = document.getElementById('dashNotifDot');
    if (dashDot) dashDot.style.display = hasUnread ? 'block' : 'none';
  }

