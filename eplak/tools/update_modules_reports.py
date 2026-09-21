import re

reports_js_path = '/home/user/eplak/eplak-fixed/modules/reports.js'
with open(reports_js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Let's see the tracking section first:
# replace renderTrackRecent & searchByTrackCode
tracking_code_replacement = """  /* =========================================================
     Request & Ticket Tracking (پیگیری درخواست‌ها و تیکت‌ها)
  ========================================================= */
  let activeTrackFilter = 'all';

  function filterTrackList(filter, btnEl) {
    activeTrackFilter = filter;
    document.querySelectorAll('#trackFilterTabs .filter-tab').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    renderTrackRecent({ skipBackend: true });
  }

  function renderTrackRecent(options = {}) {
    const wrap = document.getElementById('trackRecentList');
    const resultBox = getTrackingResultBox();
    if (!wrap) return;

    const doRender = () => {
      const isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
        ? window.i18n.getLanguage() === 'en'
        : (window.i18n && window.i18n.currentLang === 'en');
      const noItemsMsg = isEn ? 'No requests or tickets to display.' : 'در حال حاضر گزارش یا تیکتی برای پیگیری وجود ندارد.';

      let items = [];

      if (activeTrackFilter === 'all' || activeTrackFilter === 'reports') {
        reports.forEach(r => {
          items.push({
            type: 'report',
            id: r.id,
            code: r.code || '—',
            title: r.title,
            sub: r.location ? `${r.location} • ${r.dateTime || r.date || '—'}` : (r.dateTime || r.date || '—'),
            status: r.status,
            created_at: r.rawDate || r.created_at || r.date || '',
            dateTime: r.dateTime || r.date || '—',
            icon: r.icon,
            iconBg: r.iconBg,
            raw: r
          });
        });
      }

      if (activeTrackFilter === 'all' || activeTrackFilter === 'tickets') {
        tickets.forEach(t => {
          items.push({
            type: 'ticket',
            id: t.id,
            code: t.code || '—',
            title: t.title,
            sub: `${t.department || 'پشتیبانی شهرداری'} • ${t.dateTime || formatReportDateTime(t.created_at)}`,
            status: t.status,
            reply: t.reply,
            created_at: t.created_at || '',
            dateTime: t.dateTime || formatReportDateTime(t.created_at),
            icon: 'ticket',
            iconBg: 'rgba(0,201,167,0.18)',
            raw: t
          });
        });
      }

      // مرتب‌سازی بر اساس تازه‌ترین تاریخ و ساعت
      items.sort((a, b) => {
        const timeA = new Date(a.created_at).getTime() || 0;
        const timeB = new Date(b.created_at).getTime() || 0;
        return timeB - timeA;
      });

      if (!items.length) {
        wrap.innerHTML = `<div style="padding:22px 0; color:var(--text-muted); font-size:13px; text-align:center;">${noItemsMsg}</div>`;
        return;
      }

      wrap.innerHTML = items.map(item => {
        const isTicket = item.type === 'ticket';
        const hasReply = !!(isTicket && item.reply && item.reply.trim());
        let statusMeta = getStatusMeta(item.status);
        let statusLabel = statusMeta.label;
        if (isTicket) {
          if (hasReply) {
            statusLabel = 'پاسخ داده شده';
          } else if (item.status === 'pending') {
            statusLabel = 'در انتظار پاسخ';
          }
        }

        const typeBadge = isTicket
          ? `<span style="font-size:10.5px; font-weight:800; background:rgba(0,201,167,0.15); color:var(--teal); padding:2px 7px; border-radius:8px;">🎫 تیکت</span>`
          : `<span style="font-size:10.5px; font-weight:800; background:rgba(59,130,246,0.15); color:#3b82f6; padding:2px 7px; border-radius:8px;">📋 گزارش</span>`;

        const onClickCall = isTicket ? `openTicketDetail('${item.id}')` : `openReportDetail('${item.id}')`;
        const hasReplyBadge = hasReply
          ? `<span style="font-size:10.5px; font-weight:700; color:#10b981; background:rgba(16,185,129,0.12); padding:2px 6px; border-radius:6px;">پاسخ شهرداری</span>`
          : '';

        return `
          <div class="report-item track-item-card" onclick="${onClickCall}" style="align-items:flex-start; padding:13px 14px;">
            <div style="display:flex; flex-direction:column; align-items:flex-start; gap:4px; flex-shrink:0;">
              <span class="report-status ${statusMeta.className}">${statusLabel}</span>
              ${hasReplyBadge}
            </div>
            <div class="report-info" style="flex:1; text-align:right;">
              <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px; justify-content:flex-end;">
                ${typeBadge}
                <span style="font-size:11px; font-weight:700; color:var(--teal); direction:ltr; font-family:monospace;">${escapeHtml(item.code)}</span>
              </div>
              <h4 style="font-size:13.5px; font-weight:800; margin:0 0 4px; color:var(--text-primary); line-height:1.5;">${escapeHtml(item.title)}</h4>
              <p style="font-size:11px; color:var(--text-muted); margin:0;">${escapeHtml(item.sub)}</p>
            </div>
            <div class="report-icon-box" style="background:${item.iconBg}; align-self:center; font-size:18px;">
              ${isTicket ? '🎫' : (window.EplakIcons ? window.EplakIcons.get(item.icon) : item.icon)}
            </div>
          </div>
        `;
      }).join('');
    };

    doRender();

    const phone = getCurrentPhone();
    if (phone && !options.skipBackend) {
      Promise.all([
        loadReportsFromBackend(phone, { silent: true }),
        loadTicketsFromBackend(phone, { silent: true })
      ]).then(() => {
        doRender();
      }).catch(() => {});
    }
  }

  function searchByTrackCode() {
    const input = getTrackingInputElement();
    const resultBox = getTrackingResultBox();
    const code = (input ? input.value.trim() : '');

    // واژه کلیدی مستقیم برای ورود به پنل ادمین
    const lowerCode = code.toLowerCase();
    if (lowerCode === 'admin' || lowerCode === 'panel' || lowerCode === 'modir' || code === 'مدیر') {
      window.location.href = '/admin';
      return;
    }

    const isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');

    if (!code) {
      renderTrackRecent({ skipBackend: true });
      if (resultBox) resultBox.innerHTML = '';
      return;
    }

    const normalizedCode = code.toLowerCase().replace(/\\s+/g, '');
    
    // ۱. جستجو در تیکت‌ها
    const foundTicket = tickets.find(t => {
      const tCode = String(t.code || '').toLowerCase().replace(/\\s+/g, '');
      const tTitle = String(t.title || '').toLowerCase().replace(/\\s+/g, '');
      return tCode === normalizedCode || tTitle.includes(normalizedCode);
    });
    if (foundTicket) {
      openTicketDetail(foundTicket.id);
      return;
    }

    // ۲. جستجو در گزارش‌ها
    const foundReport = reports.find(r => {
      const reportCode = String(r.code || '').toLowerCase().replace(/\\s+/g, '');
      const reportTitle = String(r.title || '').toLowerCase().replace(/\\s+/g, '');
      return reportCode === normalizedCode || reportTitle.includes(normalizedCode);
    });

    if (foundReport) {
      openReportDetail(foundReport.id);
      return;
    }

    const phone = getCurrentPhone();
    if (phone) {
      Promise.all([
        loadReportsFromBackend(phone, { silent: true }),
        loadTicketsFromBackend(phone, { silent: true })
      ]).then(() => {
        const foundTicketAfter = tickets.find(t => {
          const tCode = String(t.code || '').toLowerCase().replace(/\\s+/g, '');
          const tTitle = String(t.title || '').toLowerCase().replace(/\\s+/g, '');
          return tCode === normalizedCode || tTitle.includes(normalizedCode);
        });
        if (foundTicketAfter) {
          openTicketDetail(foundTicketAfter.id);
          return;
        }

        const foundReportAfter = reports.find(r => {
          const reportCode = String(r.code || '').toLowerCase().replace(/\\s+/g, '');
          const reportTitle = String(r.title || '').toLowerCase().replace(/\\s+/g, '');
          return reportCode === normalizedCode || reportTitle.includes(normalizedCode);
        });
        if (foundReportAfter) {
          openReportDetail(foundReportAfter.id);
          return;
        }

        if (resultBox) {
          const notFoundMsg = isEn ? 'No request or ticket found with this code' : `درخواستی با کد «${escapeHtml(code)}» یافت نشد`;
          resultBox.innerHTML = `<div class="glass-card" style="padding:16px; text-align:center; font-size:13px; color:var(--text-muted); border-radius:14px;">${notFoundMsg}</div>`;
        }
      }).catch(() => {
        if (resultBox) {
          const notFoundMsg = isEn ? 'No request or ticket found with this code' : `درخواستی با کد «${escapeHtml(code)}» یافت نشد`;
          resultBox.innerHTML = `<div class="glass-card" style="padding:16px; text-align:center; font-size:13px; color:var(--text-muted); border-radius:14px;">${notFoundMsg}</div>`;
        }
      });
    } else {
      if (resultBox) {
        const notFoundMsg = isEn ? 'No request or ticket found with this code' : `درخواستی با کد «${escapeHtml(code)}» یافت نشد`;
        resultBox.innerHTML = `<div class="glass-card" style="padding:16px; text-align:center; font-size:13px; color:var(--text-muted); border-radius:14px;">${notFoundMsg}</div>`;
      }
    }
  }
"""

# Replace old renderTrackRecent and searchByTrackCode
old_tracking_pattern = r'function renderTrackRecent\(options = \{\}\) \{.*?function searchByTrackCode\(\) \{.*?\n  \}\n'
match_track = re.search(old_tracking_pattern, js, flags=re.DOTALL)
if match_track:
    js = js[:match_track.start()] + tracking_code_replacement + js[match_track.end():]
    print("   -> renderTrackRecent & searchByTrackCode replaced successfully!")
else:
    print("   [!] Could not match old tracking pattern directly, trying alternative match...")
    start_idx = js.find('function renderTrackRecent(')
    end_idx = js.find('/* =========================================================\n     Ticket System')
    if start_idx != -1 and end_idx != -1:
        js = js[:start_idx] + tracking_code_replacement + "\n\n  " + js[end_idx:]
        print("   -> renderTrackRecent & searchByTrackCode replaced by section markers!")
    else:
        print("   [ERR] Failed to locate tracking functions.")

# Now update ticket section and add tab switcher + ticket deletion
ticket_code_new = """  /* =========================================================
     Ticket System (ثبت تیکت، مدیریت، تفکیک تب‌ها و حذف تیکت)
  ========================================================= */
  let tickets = [];
  window.tickets = tickets;
  let activeTicketId = null;
  window.activeTicketId = activeTicketId;
  let activeTicketFilter = 'all';
  let activeReportsMainTab = 'reports';

  function switchReportsMainTab(section, btnEl) {
    activeReportsMainTab = section;
    const isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');

    const indicator = document.getElementById('reportsSwitcherIndicator');
    const btns = document.querySelectorAll('#reportsMainSwitcher .reports-switcher-btn');
    btns.forEach(b => b.classList.remove('active'));
    if (btnEl) {
      btnEl.classList.add('active');
    } else {
      const activeBtn = document.getElementById(section === 'tickets' ? 'tabBtnTickets' : 'tabBtnReports');
      if (activeBtn) activeBtn.classList.add('active');
    }

    if (indicator) {
      if (section === 'tickets') {
        indicator.style.transform = isEn ? 'translateX(100%)' : 'translateX(-100%)';
      } else {
        indicator.style.transform = 'translateX(0)';
      }
    }

    const paneReports = document.getElementById('sectionReportsPane');
    const paneTickets = document.getElementById('sectionTicketsPane');

    if (section === 'tickets') {
      if (paneReports) paneReports.style.display = 'none';
      if (paneTickets) {
        paneTickets.style.display = 'flex';
        renderUserTicketsList(activeTicketFilter);
      }
    } else {
      if (paneTickets) paneTickets.style.display = 'none';
      if (paneReports) {
        paneReports.style.display = 'flex';
        renderReportsList('all');
      }
    }
  }

  function filterUserTickets(filter, btnEl) {
    activeTicketFilter = filter;
    document.querySelectorAll('#ticketsFilterTabs .filter-tab').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    renderUserTicketsList(filter);
  }

  function loadSavedTickets(phone = (typeof getCurrentPhone === 'function' ? getCurrentPhone() : '')) {
    try {
      const key = 'eplak_tickets_' + (phone || 'guest');
      const raw = localStorage.getItem(key);
      if (raw) {
        tickets = JSON.parse(raw);
      } else {
        tickets = [];
      }
    } catch (e) {
      tickets = [];
    }
    return tickets;
  }

  function saveTickets(phone = (typeof getCurrentPhone === 'function' ? getCurrentPhone() : '')) {
    try {
      const key = 'eplak_tickets_' + (phone || 'guest');
      localStorage.setItem(key, JSON.stringify(tickets));
    } catch (e) {}
  }

  function startNewTicket() {
    const titleInp = document.getElementById('ticketTitleInput');
    const descInp = document.getElementById('ticketDescInput');
    const deptSel = document.getElementById('ticketDeptSelect');
    const prioSel = document.getElementById('ticketPrioritySelect');
    const countEl = document.getElementById('ticketCharCount');

    if (titleInp) titleInp.value = '';
    if (descInp) descInp.value = '';
    if (deptSel) deptSel.selectedIndex = 0;
    if (prioSel) prioSel.value = 'medium';
    if (countEl) countEl.textContent = '0/800';

    showScreen('screen-ticket-new');
  }

  function updateTicketCount(el) {
    if (!el) return;
    const count = (el.value || '').length;
    const countEl = document.getElementById('ticketCharCount');
    if (countEl) countEl.textContent = count + '/800';
  }

  function submitNewTicket() {
    const titleInp = document.getElementById('ticketTitleInput');
    const descInp = document.getElementById('ticketDescInput');
    const deptSel = document.getElementById('ticketDeptSelect');
    const prioSel = document.getElementById('ticketPrioritySelect');

    const title = (titleInp ? titleInp.value : '').trim();
    const desc = (descInp ? descInp.value : '').trim();
    const dept = (deptSel ? deptSel.value : 'حوزه شهردار و روابط عمومی').trim();
    const priority = (prioSel ? prioSel.value : 'medium').trim();

    if (!title) {
      if (typeof showToast === 'function') showToast('لطفاً عنوان تیکت را وارد فرمایید');
      return;
    }
    if (!desc) {
      if (typeof showToast === 'function') showToast('لطفاً شرح و متن تیکت را بنویسید');
      return;
    }

    const currentPhone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : '';
    const nowIso = new Date().toISOString();
    const localCode = 'TK-1403-' + String(1000 + tickets.length + 1).padStart(4, '0');

    const newTicket = {
      id: 'tk_' + Date.now(),
      code: localCode,
      title: title,
      description: desc,
      category: dept,
      department: dept,
      priority: priority,
      status: 'pending',
      reply: '',
      user_phone: currentPhone,
      created_at: nowIso,
      dateTime: formatReportDateTime(nowIso)
    };

    // ۱. ثبت بلادرنگ و فوری در حافظه محلی و UI (بدون کوچکترین لگ - 0ms)
    tickets.unshift(newTicket);
    saveTickets(currentPhone);

    const codeElem = document.getElementById('successTicketCode');
    if (codeElem) codeElem.textContent = localCode;

    if (window.soundManager && typeof window.soundManager.playDing === 'function') {
      window.soundManager.playDing();
    }

    // ۲. نمایش فوری صفحه ثبت موفق تیکت
    showScreen('screen-ticket-success');

    // به‌روزرسانی کارت‌های تیکت در صفحه گزارش‌ها و بخش پیگیری
    renderUserTicketsList(activeTicketFilter);
    if (typeof renderTrackRecent === 'function') {
      renderTrackRecent({ skipBackend: true });
    }

    // ۳. ارسال مستقیم و بلادرنگ به پنل تیکت ادمین و ذخیره در دیتابیس MariaDB
    const payload = {
      userPhone: currentPhone,
      title: title,
      description: desc,
      category: dept,
      department: dept,
      priority: priority,
      status: 'pending'
    };

    const apiBase = window.EPLAK_API_BASE_URL ||
      (window.location && window.location.protocol === 'file:' ? 'http://192.168.98.133/eplak-fixed/api' : 'api');

    const syncPromise = (typeof window.syncDataToBackend === 'function')
      ? window.syncDataToBackend('tickets', payload)
      : fetch(`${apiBase}/tickets.php`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(r => r.json());

    syncPromise
    .then(data => {
      if (data && data.success) {
        if (data.tracking_code) {
          newTicket.code = data.tracking_code;
          if (codeElem) codeElem.textContent = data.tracking_code;
        }
        if (data.id) newTicket.id = String(data.id);
        saveTickets(currentPhone);
        renderUserTicketsList(activeTicketFilter);
        if (typeof renderTrackRecent === 'function') {
          renderTrackRecent({ skipBackend: true });
        }
      }
    })
    .catch(err => {
      console.warn('[tickets] background sync note:', err);
    });
  }

  function loadTicketsFromBackend(phone = (typeof getCurrentPhone === 'function' ? getCurrentPhone() : ''), options = {}) {
    if (!phone) return Promise.resolve(tickets);
    const apiBase = window.EPLAK_API_BASE_URL ||
      (window.location && window.location.protocol === 'file:' ? 'http://192.168.98.133/eplak-fixed/api' : 'api');

    return fetch(`${apiBase}/tickets.php?phone=${encodeURIComponent(phone)}`)
      .then(r => r.json())
      .then(data => {
        const rows = Array.isArray(data?.tickets) ? data.tickets : [];
        if (rows.length > 0) {
          tickets = rows.map(t => ({
            id: String(t.id),
            code: t.code || `TK-1403-${String(Number(t.id) + 1000).padStart(4, '0')}`,
            title: t.title || 'تیکت جدید',
            description: t.description || '',
            category: t.category || '',
            department: t.department || '',
            priority: t.priority || 'medium',
            status: normalizeStatusValue(t.status || 'pending'),
            reply: t.reply || '',
            user_phone: t.user_phone || phone,
            created_at: t.created_at,
            dateTime: formatReportDateTime(t.created_at)
          }));
          saveTickets(phone);
        }
        return tickets;
      })
      .catch(err => {
        console.warn('[tickets] backend load note:', err);
        return tickets;
      });
  }

  function renderUserTicketsList(filter = activeTicketFilter) {
    const wrap = document.getElementById('userTicketsListWrap');
    if (!wrap) return;

    const countBadge = document.getElementById('userTicketsCountBadge');
    if (countBadge) countBadge.textContent = toPersianDigits(tickets.length);

    let filtered = tickets;
    if (filter === 'pending') {
      filtered = tickets.filter(t => !t.reply || !t.reply.trim() || t.status === 'pending');
    } else if (filter === 'answered') {
      filtered = tickets.filter(t => (t.reply && t.reply.trim()) || t.status === 'done' || t.status === 'answered');
    }

    if (filtered.length === 0) {
      const emptyMsg = filter === 'all'
        ? 'هنوز تیکتی ثبت نکرده‌اید'
        : (filter === 'answered' ? 'هنوز تیکت پاسخ داده شده‌ای ندارید' : 'تیکتی در انتظار پاسخ نیست');
      wrap.innerHTML = `<div style="text-align:center; padding:18px; color:var(--text-muted); font-size:12.5px; background:rgba(255,255,255,0.03); border-radius:14px; border:1px dashed var(--card-border);">${emptyMsg}</div>`;
      return;
    }

    const priorityLabels = {
      low: 'پایین',
      medium: 'متوسط',
      high: 'بالا',
      critical: 'بحرانی'
    };

    wrap.innerHTML = filtered.map(t => {
      const hasReply = !!(t.reply && t.reply.trim());
      let statusMeta = getStatusMeta(t.status);
      let statusLabel = statusMeta.label;
      if (hasReply) {
        statusLabel = 'پاسخ داده شده';
      } else if (t.status === 'pending') {
        statusLabel = 'در انتظار بررسی';
      }
      const pLabel = priorityLabels[t.priority] || 'متوسط';

      return `
        <div class="glass-card ticket-card-item" style="padding:14px; cursor:pointer; border-radius:14px; display:flex; flex-direction:column; gap:8px;" onclick="openTicketDetail('${t.id}')">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="report-status ${statusMeta.className}">${statusLabel}</span>
              <span style="font-size:11.5px; font-weight:700; color:var(--teal); direction:ltr; font-family:monospace;">${escapeHtml(t.code || '')}</span>
            </div>
            <button type="button" class="ticket-delete-btn" title="حذف تیکت" onclick="event.stopPropagation(); confirmDeleteTicket('${t.id}', event)" aria-label="حذف تیکت">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
            </button>
          </div>
          <div style="text-align:right;">
            <h4 style="font-size:13.5px; font-weight:800; margin:0 0 4px; color:var(--text-primary); line-height:1.5;">${escapeHtml(t.title)}</h4>
            <p style="font-size:11.5px; color:var(--text-muted); margin:0;">${escapeHtml(t.department || 'پشتیبانی شهرداری')} • اولویت: ${pLabel} • ${t.dateTime || formatReportDateTime(t.created_at)}</p>
          </div>
          ${hasReply ? `
            <div style="margin-top:4px; padding:8px 12px; border-radius:10px; background:rgba(0,201,167,0.09); border:1px solid rgba(0,201,167,0.25); text-align:right;">
              <div style="display:flex; align-items:center; gap:6px; font-size:11.5px; font-weight:800; color:var(--teal);">
                <span>🏛️ پاسخ مدیریت شهرداری:</span>
              </div>
              <p style="font-size:12px; color:var(--text-primary); margin:4px 0 0; line-height:1.6;">${escapeHtml(t.reply.slice(0, 95))}${t.reply.length > 95 ? '...' : ''}</p>
            </div>
          ` : ''}
        </div>
      `;
    }).join('');
  }

  function openTicketDetail(id) {
    const t = tickets.find(x => String(x.id) === String(id) || String(x.code) === String(id));
    if (!t) return;
    activeTicketId = t.id;

    const statusMeta = getStatusMeta(t.status);
    const priorityLabels = {
      low: 'پایین',
      medium: 'متوسط',
      high: 'بالا',
      critical: 'بحرانی'
    };

    const titleEl = document.getElementById('ticketDetailTitle');
    const statusEl = document.getElementById('ticketDetailStatus');
    const codeEl = document.getElementById('ticketDetailCode');
    const dateEl = document.getElementById('ticketDetailDate');
    const deptEl = document.getElementById('ticketDetailDept');
    const prioEl = document.getElementById('ticketDetailPriority');
    const descEl = document.getElementById('ticketDetailDesc');
    const replyCard = document.getElementById('ticketDetailReplyCard');
    const replyEl = document.getElementById('ticketDetailReply');

    if (titleEl) titleEl.textContent = t.title || 'بدون عنوان';
    if (statusEl) {
      statusEl.className = 'report-status ' + statusMeta.className;
      statusEl.textContent = (t.reply && t.reply.trim()) ? 'پاسخ داده شده' : statusMeta.label;
    }
    if (codeEl) codeEl.textContent = t.code || '—';
    if (dateEl) dateEl.textContent = t.dateTime || formatReportDateTime(t.created_at);
    if (deptEl) deptEl.textContent = t.department || 'پشتیبانی شهرداری';
    if (prioEl) prioEl.textContent = priorityLabels[t.priority] || 'متوسط';
    if (descEl) descEl.textContent = t.description || '—';

    if (replyCard && replyEl) {
      if (t.reply && t.reply.trim()) {
        replyEl.textContent = t.reply;
        replyCard.style.display = 'flex';
      } else {
        replyCard.style.display = 'none';
        replyEl.textContent = '';
      }
    }

    showScreen('screen-ticket-detail');
  }

  /* =========================================================
     Ticket Deletion Logic (حذف تیکت همراه با تایید و هماهنگی سرور)
  ========================================================= */
  function deleteCurrentOpenTicket() {
    if (!activeTicketId) return;
    confirmDeleteTicket(activeTicketId, null, true);
  }

  function confirmDeleteTicket(id, e, isFromDetail = false) {
    if (e) {
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
      if (typeof e.preventDefault === 'function') e.preventDefault();
    }
    const targetId = String(id || activeTicketId || '').trim();
    if (!targetId) return;

    const t = tickets.find(x => String(x.id).trim() === targetId || String(x.code).trim() === targetId);
    const title = t ? t.title : 'این تیکت';

    if (window.confirm(`آیا از حذف تیکت «${title}» اطمینان دارید؟`)) {
      deleteTicketById(targetId);
      if (isFromDetail && typeof goBack === 'function') {
        goBack();
      }
    }
  }

  async function deleteTicketById(id) {
    const targetId = String(id || '').trim();
    if (!targetId) return;

    const idx = tickets.findIndex(t => String(t.id).trim() === targetId || String(t.code).trim() === targetId);
    if (idx === -1) return;

    const removedTicket = tickets[idx];
    tickets.splice(idx, 1);

    const phone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : '';
    saveTickets(phone);

    // ارسال به بک‌اند جهت حذف قطعی از دیتابیس
    try {
      const apiBase = window.EPLAK_API_BASE_URL ||
        (window.location && window.location.protocol === 'file:' ? 'http://192.168.98.133/eplak-fixed/api' : 'api');
      fetch(`${apiBase}/tickets.php?id=${encodeURIComponent(removedTicket.id)}`, {
        method: 'DELETE'
      }).catch(() => {
        fetch(`${apiBase}/tickets.php?action=delete&id=${encodeURIComponent(removedTicket.id)}`, {
          method: 'POST'
        }).catch(() => {});
      });
    } catch (err) {
      console.warn('[tickets] backend delete note:', err);
    }

    renderUserTicketsList(activeTicketFilter);
    if (typeof renderTrackRecent === 'function') {
      renderTrackRecent({ skipBackend: true });
    }
    if (typeof showToast === 'function') {
      showToast('تیکت با موفقیت حذف شد');
    }
  }

  // مقداردهی اولیه تیکت‌ها از حافظه محلی
  loadSavedTickets();

  // Window exports
  window.switchReportsMainTab = switchReportsMainTab;
  window.filterUserTickets = filterUserTickets;
  window.confirmDeleteTicket = confirmDeleteTicket;
  window.deleteCurrentOpenTicket = deleteCurrentOpenTicket;
  window.deleteTicketById = deleteTicketById;
  window.filterTrackList = filterTrackList;
  window.startNewTicket = startNewTicket;
  window.updateTicketCount = updateTicketCount;
  window.submitNewTicket = submitNewTicket;
  window.loadTicketsFromBackend = loadTicketsFromBackend;
  window.renderUserTicketsList = renderUserTicketsList;
  window.openTicketDetail = openTicketDetail;
  window.tickets = tickets;

  window.submitNewReport = submitNewReport;
  window.renderReportsList = renderReportsList;
  window.filterReports = filterReports;
  window.openReportDetail = openReportDetail;
  window.renderProfileReportsSummary = renderProfileReportsSummary;
  window.renderHomeReportsSummary = renderHomeReportsSummary;
  window.renderProfileTrackingQuick = renderProfileTrackingQuick;
  window.renderHomeTrackingQuick = renderHomeTrackingQuick;
  window.renderTrackRecent = renderTrackRecent;
  window.searchByTrackCode = searchByTrackCode;
"""

# Replace old ticket section to the end of the file
old_ticket_section_idx = js.find('/* =========================================================\n     Ticket System')
if old_ticket_section_idx != -1:
    js = js[:old_ticket_section_idx] + ticket_code_new + "\n\n})();\n"
    print("   -> Ticket system section replaced successfully!")
else:
    print("   [ERR] Could not locate start of Ticket System section.")

with open(reports_js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("[4] modules/reports.js updated successfully!")
