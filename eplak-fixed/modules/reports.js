/* modules/reports.js — ثبت گزارش جدید، لیست گزارش‌ها و پیگیری درخواست */
/* استخراج‌شده عیناً از فایل اصلی app_01.html با پشتیبانی آفلاین و داده‌های توکار شهرداری */

  const DEFAULT_DEPARTMENTS = [
    {
      id: 1,
      name: 'حوزه شهردار',
      children: [
        { id: 2, name: 'دفتر شهردار ورامین' },
        { id: 3, name: 'روابط عمومی و امور بین‌الملل' },
        { id: 4, name: 'بازرسی و ارزیابی عملکرد' },
        { id: 5, name: 'حراست شهرداری' },
        { id: 6, name: 'امور حقوقی' },
        { id: 7, name: 'شورای مشاوران' }
      ]
    },
    {
      id: 8,
      name: 'معاونت اداری و مالی',
      children: [
        { id: 9, name: 'منابع انسانی' },
        { id: 10, name: 'امور اداری' },
        { id: 11, name: 'امور مالی و حسابداری' },
        { id: 12, name: 'بودجه و برنامه‌ریزی' },
        { id: 13, name: 'تدارکات و پشتیبانی' },
        { id: 14, name: 'فناوری اطلاعات (IT)' }
      ]
    },
    {
      id: 15,
      name: 'معاونت فنی و عمرانی',
      children: [
        { id: 16, name: 'طراحی و اجرای پروژه‌های عمرانی' },
        { id: 17, name: 'ساخت و نگهداری معابر' },
        { id: 18, name: 'پل‌ها و تونل‌ها' },
        { id: 19, name: 'ساختمان‌های عمومی' },
        { id: 20, name: 'تأسیسات شهری' }
      ]
    },
    {
      id: 21,
      name: 'معاونت شهرسازی و معماری',
      children: [
        { id: 22, name: 'صدور پروانه ساختمانی' },
        { id: 23, name: 'پایان کار ساختمان' },
        { id: 24, name: 'کنترل و نظارت ساختمانی' },
        { id: 25, name: 'طرح‌های توسعه شهری' },
        { id: 26, name: 'کمیسیون‌های شهرسازی' }
      ]
    },
    {
      id: 27,
      name: 'معاونت خدمات شهری',
      children: [
        { id: 28, name: 'نظافت شهری' },
        { id: 29, name: 'مدیریت پسماند' },
        { id: 30, name: 'فضای سبز' },
        { id: 31, name: 'زیباسازی شهر' },
        { id: 32, name: 'آرامستان‌ها' },
        { id: 33, name: 'کنترل حیوانات شهری' }
      ]
    },
    {
      id: 34,
      name: 'معاونت حمل‌ونقل و ترافیک',
      children: [
        { id: 35, name: 'مدیریت ترافیک' },
        { id: 36, name: 'پارکینگ‌ها' },
        { id: 37, name: 'حمل‌ونقل عمومی' },
        { id: 38, name: 'پایانه‌ها' },
        { id: 39, name: 'ایمنی و علائم راهنمایی' }
      ]
    },
    {
      id: 40,
      name: 'معاونت فرهنگی و اجتماعی',
      children: [
        { id: 41, name: 'فرهنگسراها' },
        { id: 42, name: 'کتابخانه‌ها' },
        { id: 43, name: 'امور جوانان' },
        { id: 44, name: 'امور بانوان' },
        { id: 45, name: 'مشارکت‌های مردمی' },
        { id: 46, name: 'ورزش همگانی' }
      ]
    },
    {
      id: 47,
      name: 'معاونت برنامه‌ریزی و توسعه',
      children: [
        { id: 48, name: 'آمار و اطلاعات' },
        { id: 49, name: 'پژوهش و نوآوری' },
        { id: 50, name: 'مدیریت پروژه' },
        { id: 51, name: 'هوشمندسازی شهر' }
      ]
    },
    {
      id: 52,
      name: 'سازمان‌ها و شرکت‌های وابسته',
      children: [
        { id: 53, name: 'سازمان مدیریت پسماند' },
        { id: 54, name: 'سازمان آتش‌نشانی و خدمات ایمنی' },
        { id: 55, name: 'سازمان پارک‌ها و فضای سبز' },
        { id: 56, name: 'سازمان زیباسازی' },
        { id: 57, name: 'سازمان حمل‌ونقل بار و مسافر' },
        { id: 58, name: 'سازمان میادین و بازارها' },
        { id: 59, name: 'سازمان آرامستان‌ها' },
        { id: 60, name: 'سازمان فناوری اطلاعات و ارتباطات' },
        { id: 61, name: 'سازمان فرهنگی، اجتماعی و ورزشی' },
        { id: 62, name: 'سازمان سرمایه‌گذاری و مشارکت‌های مردمی' },
        { id: 63, name: 'شرکت بهره‌برداری مترو' },
        { id: 64, name: 'شرکت واحد اتوبوسرانی' },
        { id: 65, name: 'شرکت نوسازی و بهسازی شهری' }
      ]
    }
  ];

  /* =========================================================
     New Report — multi-step form
  ========================================================= */
  function startNewReport() {
    resetReportDraft();
    loadDepartmentsFromBackend();
    showScreen('screen-report');
  }

  function renderDepartments(list) {
    const wrap = document.getElementById('deptListWrap');
    if (!wrap) return;
    const items = (Array.isArray(list) && list.length) ? list : DEFAULT_DEPARTMENTS;
    const safeEscape = (typeof escapeHtml === 'function')
      ? escapeHtml
      : (str => String(str || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])));

    wrap.innerHTML = items.map((parent, parentIndex) => `
      <div class="dept-item">
        <div class="dept-header" onclick="toggleDept(this)">
          <span class="dept-title">${parentIndex + 1}. ${safeEscape(parent.name)}</span>
          <span class="dept-arrow">⌄</span>
        </div>
        <div class="dept-sub-list">
          ${(parent.children || []).map(child => `
            <div class="dept-sub-item" onclick="selectDepartment(this, '${safeEscape(parent.name).replace(/'/g, "\\'")}')">${safeEscape(child.name)}</div>
          `).join('')}
        </div>
      </div>
    `).join('');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadDepartmentsFromBackend);
  } else {
    loadDepartmentsFromBackend();
  }

  async function loadDepartmentsFromBackend() {
    const wrap = document.getElementById('deptListWrap');
    if (!wrap) return;

    // If wrap is empty or currently contains an error/loading message, immediately render default departments
    if (!wrap.children.length || wrap.querySelector('.dept-item') === null) {
      renderDepartments(DEFAULT_DEPARTMENTS);
    }

    try {
      const apiBase = window.EPLAK_API_BASE_URL ||
        (window.location.protocol === 'file:' ? 'http://192.168.98.133/eplak-fixed/api' : 'api');
      const response = await fetch(`${apiBase}/departments.php`);
      if (!response.ok) throw new Error('bad response');
      const data = await response.json();
      const list = Array.isArray(data?.departments) ? data.departments : [];

      if (list.length) {
        renderDepartments(list);
      }
    } catch (error) {
      console.warn('[departments] Backend sync note (using built-in municipal directory):', error.message || error);
      if (!wrap.children.length || wrap.querySelector('.dept-item') === null) {
        renderDepartments(DEFAULT_DEPARTMENTS);
      }
    }
  }

  window.DEFAULT_DEPARTMENTS = DEFAULT_DEPARTMENTS;
  window.renderDepartments = renderDepartments;

  function formatReportDate(dateValue) {
    if (!dateValue) return '—';
    const date = new Date(dateValue);
    if (Number.isNaN(date.getTime())) return dateValue;
    return date.toLocaleDateString('fa-IR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  }

  async function loadReportsFromBackend(phone = getCurrentPhone(), options = {}) {
    const { silent = false } = options;
    if (!phone) {
      reports.length = 0;
      return [];
    }

    try {
      const apiBase = window.EPLAK_API_BASE_URL ||
        (window.location.protocol === 'file:' ? 'http://192.168.98.133/eplak-fixed/api' : 'api');
      const response = await fetch(`${apiBase}/reports.php?phone=${encodeURIComponent(phone)}`);
      if (!response.ok) throw new Error('reports fetch failed');
      const data = await response.json();
      const rows = Array.isArray(data?.reports) ? data.reports : [];
      const mapped = rows.map(item => ({
        id: String(item.id),
        code: item.code || `EP-1403-${String(Number(item.id) + 1000).padStart(4, '0')}`,
        title: item.title || 'گزارش جدید',
        location: item.location || 'نامشخص',
        date: formatReportDate(item.created_at),
        status: normalizeStatusValue(item.status || 'pending'),
        icon: '📋',
        iconBg: 'rgba(0,201,167,0.12)',
        desc: item.description || item.details || '',
        department: item.department || '',
        subDepartment: item.sub_department || '',
        reply: item.reply || '',
        timeline: Array.isArray(item.timeline) ? item.timeline : []
      }));

      reports.length = 0;
      mapped.forEach(item => reports.push(item));
      if (typeof saveReports === 'function') saveReports(phone);
      return reports;
    } catch (error) {
      if (!silent) {
        console.warn('[reports] backend sync failed', error);
      }
      return reports;
    }
  }

  window.loadReportsFromBackend = loadReportsFromBackend;

  function resetReportDraft() {
    reportDraft = { type: 'سایر', department: '', subDepartment: '', desc: '', location: '', photos: [] };
    const desc = document.getElementById('reportDescInput');
    if (desc) { desc.value = ''; updateCount(desc); }
    document.querySelectorAll('#deptListWrap .dept-sub-item').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('#deptListWrap .dept-item').forEach(it => it.classList.remove('open'));
    const deptBox = document.getElementById('deptSelectedBox');
    if (deptBox) deptBox.style.display = 'none';
    const loc = document.getElementById('reportLocationInput');
    if (loc) loc.value = '';
    const photoPrev = document.getElementById('reportPhotosPreview');
    if (photoPrev) photoPrev.innerHTML = '';
  }

  function toggleDept(headerEl) {
    const item = headerEl.closest('.dept-item');
    if (!item) return;
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('#deptListWrap .dept-item.open').forEach(el => el.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
  }

  function selectDepartment(el, mainLabel) {
    document.querySelectorAll('#deptListWrap .dept-sub-item').forEach(s => s.classList.remove('active'));
    el.classList.add('active');
    const subLabel = el.textContent.trim();
    reportDraft.department = mainLabel;
    reportDraft.subDepartment = subLabel;
    const box = document.getElementById('deptSelectedBox');
    const text = document.getElementById('deptSelectedText');
    if (box && text) {
      text.textContent = mainLabel + ' / ' + subLabel;
      box.style.display = 'flex';
    }
    document.querySelectorAll('#deptListWrap .dept-item.open').forEach(it => it.classList.remove('open'));
  }

  function updateCount(el) {
    const count = el.value.length;
    el.nextElementSibling.textContent = count + '/300';
  }

  function goReportStep2() {
    const descEl = document.getElementById('reportDescInput');
    reportDraft.desc = descEl.value.trim();
    if (!reportDraft.subDepartment) {
      showToast('لطفاً واحد مربوطه را انتخاب کنید');
      return;
    }
    if (!reportDraft.desc) {
      showToast('لطفاً توضیحات مشکل را وارد کنید');
      return;
    }
    showScreen('screen-report-step2');
  }

  function useCurrentLocation() {
    document.getElementById('reportLocationInput').value = 'موقعیت فعلی کاربر (دریافت‌شده از GPS)';
    showToast('موقعیت فعلی شما دریافت شد');
  }

  function goReportStep3() {
    const locEl = document.getElementById('reportLocationInput');
    reportDraft.location = locEl.value.trim();
    if (!reportDraft.location) {
      showToast('لطفاً موقعیت مکانی را مشخص کنید');
      return;
    }
    showScreen('screen-report-step3');
  }

  function addReportPhotos(input) {
    const files = Array.from(input.files || []);
    const remaining = 3 - reportDraft.photos.length;
    files.slice(0, remaining).forEach(file => {
      reportDraft.photos.push(file.name);
    });
    renderReportPhotosPreview();
    input.value = '';
  }

  function renderReportPhotosPreview() {
    const wrap = document.getElementById('reportPhotosPreview');
    wrap.innerHTML = reportDraft.photos.map((name, idx) => `
      <div style="position:relative; width:64px; height:64px; border-radius:12px; background:var(--card-bg); border:1px solid var(--card-border); display:flex; align-items:center; justify-content:center; font-size:22px;">
        🖼️
        <span onclick="removeReportPhoto(${idx})" style="position:absolute; top:-6px; left:-6px; width:20px; height:20px; background:rgba(255,60,60,0.9); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; color:white; cursor:pointer;">✕</span>
      </div>
    `).join('');
  }

  function removeReportPhoto(idx) {
    reportDraft.photos.splice(idx, 1);
    renderReportPhotosPreview();
  }

  function goReportStep4() {
    document.getElementById('confirmDeptText').textContent = reportDraft.subDepartment
      ? (reportDraft.department + ' / ' + reportDraft.subDepartment) : '—';
    document.getElementById('confirmDescText').textContent = reportDraft.desc || '—';
    document.getElementById('confirmLocationText').textContent = reportDraft.location || '—';
    document.getElementById('confirmPhotoCount').textContent = `${toPersianDigits(reportDraft.photos.length)} تصویر`;
    showScreen('screen-report-step4');
  }

  async function submitNewReport() {
    const iconMap = { 'سایر': '⋯', 'نظافت': '💡', 'زیرساخت': '🌿', 'زیرسبز': '🌳', 'روشنایی': '🔆' };
    const currentPhone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : '';
    const title = (reportDraft.desc || '').slice(0, 28) || (reportDraft.type + ' - گزارش جدید');
    const code = 'EP-1403-' + String(1000 + reports.length + 1).padStart(4, '0');
    const newReport = {
      id: `r${reportIdCounter++}`,
      code,
      title,
      location: reportDraft.location || 'نامشخص',
      date: formatReportDate(new Date().toISOString()),
      status: 'pending',
      icon: iconMap[reportDraft.type] || '📋',
      iconBg: 'rgba(0,201,167,0.12)',
      desc: reportDraft.desc || 'بدون توضیحات',
      department: reportDraft.department || '',
      subDepartment: reportDraft.subDepartment || '',
      reply: '',
      timeline: []
    };

    reports.unshift(newReport);
    if (typeof saveReports === 'function') saveReports();

    if (currentPhone && typeof window.syncDataToBackend === 'function') {
      try {
        await window.syncDataToBackend('reports', {
          userPhone: currentPhone,
          title: newReport.title,
          description: newReport.desc || newReport.title,
          category: newReport.subDepartment || newReport.department || 'سایر',
          department: newReport.department || '',
          subDepartment: newReport.subDepartment || '',
          location: newReport.location || ''
        });
        await loadReportsFromBackend(currentPhone, { silent: true });
      } catch (error) {
        console.warn('[reports] sync failed after submit', error);
      }
    }

    document.getElementById('successTrackCode').textContent = code;
    showScreen('screen-report-success');
  }


  /* =========================================================
     Reports List / Filter / Detail
  ========================================================= */
  async function renderReportsList(filter, options = {}) {
    const wrap = document.getElementById('reportsListWrap');
    if (!wrap) return;
    const phone = getCurrentPhone();
    if (phone && !options.skipBackend) {
      await loadReportsFromBackend(phone, { silent: true });
    }

    const normalizedFilter = normalizeStatusValue(filter ?? 'all');
    const list = normalizedFilter === 'all'
      ? reports
      : reports.filter(r => normalizeStatusValue(r.status) === normalizedFilter || (normalizeStatusValue(r.status) === 'in_progress' && normalizedFilter === 'in_progress'));

    const countBadge = document.getElementById('reportsCountBadge');
    if (countBadge) countBadge.textContent = toPersianDigits(reports.length);

    if (list.length === 0) {
      wrap.innerHTML = `<div style="text-align:center; padding:30px 10px; color:var(--text-muted); font-size:13px;">گزارشی در این دسته یافت نشد</div>`;
      return;
    }
    wrap.innerHTML = list.map(r => {
      const statusMeta = getStatusMeta(r.status);
      return `
        <div class="report-swipe">
          <div class="report-delete-bg" onpointerdown="event.stopPropagation()" onclick="deleteReport('${r.id}', event)">
            <div class="delete-action" style="color:#ef4444;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3,6 5,6 21,6"/><path d="M19,6 L19,20 a2,2 0 0 1 -2,2 H7 a2,2 0 0 1 -2,-2 L5,6"/><path d="M8,6 V4 a2,2 0 0 1 2,-2 h4 a2,2 0 0 1 2,2 v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
              <span style="color:#ef4444; font-weight:800;">حذف</span>
            </div>
          </div>
          <div class="report-swipe-item" onclick="openReportDetail('${r.id}')">
            <div class="report-item">
              <span class="report-status ${statusMeta.className}">${statusMeta.label}</span>
              <div class="report-info">
                <h4>${escapeHtml(r.title)}</h4>
                <p>${escapeHtml(r.location)} - ${r.date}</p>
              </div>
              <div class="report-icon-box" style="background:${r.iconBg};">${r.icon}</div>
            </div>
          </div>
        </div>
      `;
    }).join('');
    initReportSwipe();
  }

  async function deleteReport(id, e) {
    if (e) {
      if (typeof e.preventDefault === 'function') e.preventDefault();
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
    }
    const targetId = String(id || activeReportId || '').trim();
    if (!targetId) return;

    const idx = reports.findIndex(r => String(r.id).trim() === targetId || String(r.code).trim() === targetId);
    if (idx === -1) {
      console.warn('[reports] report to delete not found:', targetId);
      return;
    }

    const removedReport = reports[idx];
    reports.splice(idx, 1);

    const phone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : '';
    if (typeof saveReports === 'function') {
      saveReports(phone);
    }

    if (phone) {
      try {
        const apiBase = window.EPLAK_API_BASE_URL ||
          (window.location.protocol === 'file:' ? 'http://192.168.98.133/eplak-fixed/api' : 'api');
        fetch(`${apiBase}/reports.php?action=delete&id=${encodeURIComponent(removedReport.id)}&phone=${encodeURIComponent(phone)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'delete', id: removedReport.id, phone })
        }).catch(() => {});
      } catch (err) {
        console.warn('[reports] backend delete failed', err);
      }
    }

    const activeTab = document.querySelector('#reportsFilterTabs .filter-tab.active');
    const filter = activeTab ? activeTab.getAttribute('data-filter') : 'all';
    renderReportsList(filter, { skipBackend: true });

    if (typeof renderProfileReportsSummary === 'function') {
      renderProfileReportsSummary({ skipBackend: true });
    }
    if (typeof renderProfileTrackingQuick === 'function') {
      renderProfileTrackingQuick({ skipBackend: true });
    }
    if (typeof renderTrackRecent === 'function') {
      renderTrackRecent({ skipBackend: true });
    }

    showToast('گزارش با موفقیت حذف شد');
  }

  window.deleteReport = deleteReport;
  window.deleteCurrentOpenReport = function() {
    if (!activeReportId) return;
    deleteReport(activeReportId);
    if (typeof goBack === 'function') goBack();
  };

  /* =========================================================
     Swipe-to-delete gesture for report items
  ========================================================= */
  document.addEventListener('pointerdown', (e) => {
    if (e.target.closest && e.target.closest('.report-swipe')) return;
    document.querySelectorAll('#reportsListWrap .report-swipe-item.open').forEach(el => {
      el.style.transform = 'translateX(0)';
      el.classList.remove('open');
    });
  });

  function initReportSwipe() {
    const SWIPE_OPEN = -88; // px the item shifts to reveal the delete action
    const items = document.querySelectorAll('#reportsListWrap .report-swipe-item');

    function closeSwipeItem(el) {
      el.style.transform = 'translateX(0)';
      el.classList.remove('open');
    }

    function closeAllExcept(except) {
      document.querySelectorAll('#reportsListWrap .report-swipe-item.open').forEach(el => {
        if (el !== except) closeSwipeItem(el);
      });
    }

    items.forEach(item => {
      let startX = 0;
      let baseX = 0;
      let dragging = false;
      let moved = false;

      item.addEventListener('pointerdown', (e) => {
        if (e.pointerType === 'mouse' && e.button !== 0) return;
        dragging = true;
        moved = false;
        startX = e.clientX;
        baseX = item.classList.contains('open') ? SWIPE_OPEN : 0;
        item.classList.add('swiping');
        closeAllExcept(item);
        try { item.setPointerCapture(e.pointerId); } catch (err) {}
      });

      item.addEventListener('pointermove', (e) => {
        if (!dragging) return;
        const delta = e.clientX - startX;
        if (Math.abs(delta) > 6) moved = true;
        let next = baseX + delta;
        if (next > 0) next = next * 0.25; // rubber-band past the resting point
        if (next < SWIPE_OPEN) next = SWIPE_OPEN + (next - SWIPE_OPEN) * 0.2; // rubber-band past open
        item.style.transform = `translateX(${next}px)`;
      });

      function endDrag() {
        if (!dragging) return;
        dragging = false;
        item.classList.remove('swiping');
        const match = /translateX\((-?\d+\.?\d*)px\)/.exec(item.style.transform || '');
        const x = match ? parseFloat(match[1]) : 0;
        if (x < SWIPE_OPEN / 2) {
          item.style.transform = `translateX(${SWIPE_OPEN}px)`;
          item.classList.add('open');
        } else {
          closeSwipeItem(item);
        }
      }

      item.addEventListener('pointerup', endDrag);
      item.addEventListener('pointercancel', endDrag);

      // Prevent the tap-to-open-detail click from firing right after a swipe,
      // and let a tap on an already-open item close it instead of navigating.
      item.addEventListener('click', (e) => {
        if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; return; }
        if (item.classList.contains('open')) {
          e.preventDefault();
          e.stopPropagation();
          closeSwipeItem(item);
        }
      }, true);
    });
  }

  function filterReports(filter, btn) {
    const safeFilter = normalizeStatusValue(filter ?? 'all');
    document.querySelectorAll('#reportsFilterTabs .filter-tab').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderReportsList(safeFilter);
  }

  function openReportDetail(id) {
    const r = reports.find(x => x.id === id);
    if (!r) return;
    const safeStatus = normalizeStatusValue(r.status);
    const statusMeta = getStatusMeta(safeStatus);
    const replyText = (r.reply || r.admin_reply || r.response || '').trim();
    const timelineBase = Array.isArray(r.timeline) && r.timeline.length ? r.timeline : [
      { label: 'ثبت گزارش', date: r.date || '—', done: true },
      { label: 'بررسی اولیه', date: safeStatus === 'in_progress' || safeStatus === 'done' ? '—' : '—', done: safeStatus === 'in_progress' || safeStatus === 'done' },
      { label: 'ارجاع به واحد مربوطه', date: safeStatus === 'done' ? '—' : '—', done: safeStatus === 'done' },
      { label: 'پاسخ مدیریت', date: replyText ? '—' : '—', done: !!replyText }
    ];

    activeReportId = id;
    document.getElementById('detailIconBox').style.background = r.iconBg;
    document.getElementById('detailIconBox').textContent = r.icon;
    document.getElementById('detailTitle').textContent = r.title;
    document.getElementById('detailDate').textContent = r.date;
    const statusEl = document.getElementById('detailStatus');
    statusEl.className = 'report-status ' + statusMeta.className;
    statusEl.textContent = statusMeta.label;
    document.getElementById('detailCode').textContent = r.code;
    document.getElementById('detailLocation').textContent = r.location;
    document.getElementById('detailDept').textContent = (r.department && r.subDepartment)
      ? (r.department + ' / ' + r.subDepartment) : '—';
    document.getElementById('detailDesc').textContent = r.desc;

    const replyWrap = document.getElementById('detailReplyWrap');
    if (replyWrap) {
      if (replyText) {
        replyWrap.style.display = 'block';
        replyWrap.innerHTML = `
          <div style="text-align:right;">
            <p style="font-size:12px; color:var(--text-muted); margin-bottom:4px;">پاسخ مدیریت</p>
            <p style="font-size:13px; line-height:1.8; color:var(--text-primary);">${escapeHtml(replyText)}</p>
          </div>
        `;
      } else {
        replyWrap.style.display = 'none';
        replyWrap.innerHTML = '';
      }
    }

    document.getElementById('detailTimeline').innerHTML = timelineBase.map((step, idx) => {
      const isLast = idx === timelineBase.length - 1;
      const dotClass = step.done ? 'done' : (idx > 0 && timelineBase[idx - 1].done && !step.done ? 'current' : '');
      return `
        <div class="timeline-row">
          <div class="timeline-marker">
            <div class="timeline-dot ${dotClass}"></div>
            ${!isLast ? `<div class="timeline-line ${step.done ? 'done' : ''}"></div>` : ''}
          </div>
          <div class="timeline-content">
            <h5>${escapeHtml(step.label)}</h5>
            <p>${step.date || '—'}</p>
          </div>
        </div>`;
    }).join('');
    showScreen('screen-report-detail');
  }


  /* =========================================================
     Track Request
  ========================================================= */
  function getTrackingInputElement() {
    const primary = document.getElementById('trackCodeInput');
    if (primary) return primary;
    const profileInput = document.getElementById('profileTrackCodeInput');
    if (profileInput) return profileInput;
    return document.getElementById('homeTrackCodeInput');
  }

  function getTrackingResultBox() {
    const primary = document.getElementById('trackResultBox');
    if (primary) return primary;
    const profileBox = document.getElementById('profileTrackResultBox');
    if (profileBox) return profileBox;
    return document.getElementById('homeTrackResultBox');
  }

  async function renderProfileReportsSummary(options = {}) {
    const wrap = document.getElementById('profileReportsList');
    if (!wrap) return;
    const phone = getCurrentPhone();
    if (phone && !options.skipBackend) {
      await loadReportsFromBackend(phone, { silent: true });
    }

    if (!reports.length) {
      wrap.innerHTML = '<div style="padding:14px 0; color:var(--text-muted); font-size:13px; text-align:center;">هنوز گزارشی ثبت نشده است.</div>';
      return;
    }

    wrap.innerHTML = reports.slice(0, 3).map(r => {
      const statusMeta = getStatusMeta(r.status);
      return `
        <div class="report-item" onclick="openReportDetail('${r.id}')">
          <span class="report-status ${statusMeta.className}">${statusMeta.label}</span>
          <div class="report-info">
            <h4>${escapeHtml(r.title)}</h4>
            <p>${escapeHtml(r.code || '—')}</p>
          </div>
          <div class="report-icon-box" style="background:${r.iconBg};">${r.icon}</div>
        </div>
      `;
    }).join('');
  }

  async function renderHomeReportsSummary() {
    return renderProfileReportsSummary();
  }

  function renderReportListCards(items, box) {
    if (!box) return;
    if (!Array.isArray(items) || !items.length) {
      box.innerHTML = '<div style="padding:12px 0; color:var(--text-muted); font-size:12.5px; text-align:center;">در حال حاضر گزارشی برای نمایش وجود ندارد.</div>';
      return;
    }

    box.innerHTML = items.map(r => {
      const statusMeta = getStatusMeta(r.status);
      return `
        <div class="report-item" onclick="openReportDetail('${r.id}')">
          <span class="report-status ${statusMeta.className}">${statusMeta.label}</span>
          <div class="report-info">
            <h4>${escapeHtml(r.title)}</h4>
            <p>${escapeHtml(r.code || '—')}</p>
          </div>
          <div class="report-icon-box" style="background:${r.iconBg};">${r.icon}</div>
        </div>
      `;
    }).join('');
  }

  async function renderProfileTrackingQuick(options = {}) {
    const box = document.getElementById('profileTrackResultBox');
    if (!box) return;
    const phone = getCurrentPhone();
    if (phone && !options.skipBackend) {
      await loadReportsFromBackend(phone, { silent: true });
    }

    const input = document.getElementById('profileTrackCodeInput');
    if (!input || !input.value.trim()) {
      renderReportListCards(reports, box);
      return;
    }

    const code = input.value.trim();
    if (!code) return;
    const normalizedCode = code.toLowerCase().replace(/\s+/g, '');
    const found = reports.find(r => {
      const reportCode = String(r.code || '').toLowerCase().replace(/\s+/g, '');
      const reportTitle = String(r.title || '').toLowerCase().replace(/\s+/g, '');
      return reportCode === normalizedCode || reportTitle.includes(normalizedCode);
    });
    if (!found) {
      box.innerHTML = '<div class="glass-card" style="padding:16px; text-align:center; font-size:13px; color:var(--text-muted);">گزارشی با این کد پیگیری یافت نشد</div>';
      return;
    }
    renderReportListCards([found], box);
  }

  async function renderHomeTrackingQuick() {
    return renderProfileTrackingQuick();
  }

  async function renderTrackRecent(options = {}) {
    const wrap = document.getElementById('trackRecentList');
    const resultBox = getTrackingResultBox();
    if (!wrap) return;
    const phone = getCurrentPhone();
    if (phone && !options.skipBackend) {
      await loadReportsFromBackend(phone, { silent: true });
    }
    if (!reports.length) {
      wrap.innerHTML = '<div style="padding:14px 0; color:var(--text-muted); font-size:13px; text-align:center;">در حال حاضر گزارشی برای نمایش وجود ندارد.</div>';
      if (resultBox && !resultBox.innerHTML) {
        resultBox.innerHTML = '<div style="padding:12px 0; color:var(--text-muted); font-size:12.5px; text-align:center;">در حال حاضر گزارشی برای نمایش وجود ندارد.</div>';
      }
      return;
    }
    wrap.innerHTML = reports.slice(0, 4).map(r => {
      const statusMeta = getStatusMeta(r.status);
      return `
        <div class="report-item" onclick="openReportDetail('${r.id}')">
          <span class="report-status ${statusMeta.className}">${statusMeta.label}</span>
          <div class="report-info">
            <h4>${escapeHtml(r.title)}</h4>
            <p>${escapeHtml(r.code || '—')}</p>
          </div>
          <div class="report-icon-box" style="background:${r.iconBg};">${r.icon}</div>
        </div>
      `;
    }).join('');
    if (resultBox && !resultBox.innerHTML) {
      resultBox.innerHTML = '<div style="padding:12px 0; color:var(--text-muted); font-size:12.5px; text-align:center;">در حال حاضر گزارشی برای نمایش وجود ندارد.</div>';
    }
  }

  async function searchByTrackCode() {
    const input = getTrackingInputElement();
    const resultBox = getTrackingResultBox();
    const code = (input ? input.value.trim() : '');
    const phone = getCurrentPhone();
    if (phone) {
      await loadReportsFromBackend(phone, { silent: true });
    }

    if (!code) {
      renderReportListCards(reports, resultBox);
      return;
    }

    const normalizedCode = code.toLowerCase().replace(/\s+/g, '');
    const found = reports.find(r => {
      const reportCode = String(r.code || '').toLowerCase().replace(/\s+/g, '');
      const reportTitle = String(r.title || '').toLowerCase().replace(/\s+/g, '');
      return reportCode === normalizedCode || reportTitle.includes(normalizedCode);
    });
    if (!found) {
      if (resultBox) {
        resultBox.innerHTML = `<div class="glass-card" style="padding:16px; text-align:center; font-size:13px; color:var(--text-muted);">گزارشی با این کد پیگیری یافت نشد</div>`;
      }
      return;
    }
    renderReportListCards([found], resultBox);
  }

