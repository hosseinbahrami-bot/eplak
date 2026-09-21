import re

print("[1] Updating eplak-fixed/index.html ...")
html_path = '/home/user/eplak/eplak-fixed/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the sectionTicketsPane content
old_tickets_pane_pattern = r'<div id="sectionTicketsPane"[^>]*>.*?<\/div>\s*<\/div>\s*(?=\s*<div class="bottom-pad">)'

new_tickets_pane = """<div id="sectionTicketsPane" class="reports-section-pane" style="display:none; flex-direction:column; gap:12px;">
        <!-- Filter Tabs -->
        <div style="display:flex; gap:8px; padding:0 16px; overflow-x:auto;" id="ticketsFilterTabs">
          <button class="filter-tab active" data-tfilter="all" onclick="filterUserTickets('all', this)">همه</button>
          <button class="filter-tab" data-tfilter="pending" onclick="filterUserTickets('pending', this)">در انتظار</button>
          <button class="filter-tab" data-tfilter="done" onclick="filterUserTickets('done', this)">انجام شده</button>
          <button class="filter-tab" data-tfilter="review" onclick="filterUserTickets('review', this)">بررسی</button>
        </div>

        <!-- Tickets List -->
        <div class="reports-list" id="userTicketsListWrap"></div>

        <!-- Add New Ticket Button -->
        <div style="padding:0 16px;">
          <button class="btn-teal" onclick="startNewTicket()">
            <span>+ ثبت تیکت جدید</span>
          </button>
        </div>
      </div>"""

match = re.search(old_tickets_pane_pattern, html, flags=re.DOTALL)
if match:
    html = html[:match.start()] + new_tickets_pane + html[match.end():]
    print("   -> sectionTicketsPane replaced successfully!")
else:
    print("   [!] Regex search failed, trying exact replace...")
    exact_old = """      <!-- ============ بخش دوم: تیکت‌های من ============ -->
      <div id="sectionTicketsPane" class="reports-section-pane" style="display:none; flex-direction:column; gap:12px;">
        <!-- کادر ثبت تیکت جدید -->
        <div style="padding:0 16px;">
          <div class="glass-card" style="padding:16px; display:flex; flex-direction:column; gap:10px; border:1px solid rgba(0,201,167,0.28); background:linear-gradient(135deg, rgba(0,201,167,0.09), rgba(0,180,140,0.03)); border-radius:18px;">
            <div style="display:flex; align-items:center; justify-content:space-between;">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:20px;">🎫</span>
                <span style="font-size:14px; font-weight:800; color:var(--text-primary);">ثبت تیکت اداری</span>
              </div>
              <span style="font-size:11px; color:var(--teal); font-weight:700; background:rgba(0,201,167,0.12); padding:3px 8px; border-radius:10px;">ارتباط با مدیریت شهرداری</span>
            </div>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.7; margin:0;">
              ارسال مستقیم پیام، مکاتبه اداری، انتقادات، پیشنهادات و پیگیری‌ها به کارشناسان و مدیریت شهرداری
            </p>
            <button type="button" class="btn-teal" onclick="startNewTicket()" style="margin-top:2px; padding:12px 16px; font-size:13px; font-weight:700; display:flex; align-items:center; justify-content:center; gap:8px; border-radius:14px;">
              <span>➕ ثبت تیکت جدید</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="M5 12h14"/><path d="M12 5l7 7-7 7"/></svg>
            </button>
          </div>
        </div>

        <!-- فیلترهای وضعیت تیکت -->
        <div style="display:flex; gap:8px; padding:0 16px; overflow-x:auto;" id="ticketsFilterTabs">
          <button class="filter-tab active" data-tfilter="all" onclick="filterUserTickets('all', this)">همه تیکت‌ها</button>
          <button class="filter-tab" data-tfilter="pending" onclick="filterUserTickets('pending', this)">در انتظار پاسخ</button>
          <button class="filter-tab" data-tfilter="answered" onclick="filterUserTickets('answered', this)">پاسخ داده شده</button>
        </div>

        <!-- لیست تیکت‌های ارسالی کاربر -->
        <div style="padding:0 16px;">
          <div id="userTicketsListWrap" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>
      </div>"""
    if exact_old in html:
        html = html.replace(exact_old, "      <!-- ============ بخش دوم: تیکت‌های من ============\n      " + new_tickets_pane)
        print("   -> Exact replace succeeded!")
    else:
        print("   [ERR] Could not replace sectionTicketsPane.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)


print("\n[2] Updating eplak-fixed/modules/reports.js ...")
js_path = '/home/user/eplak/eplak-fixed/modules/reports.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Update swipe gesture to handle both reports and tickets
js = js.replace(
    "document.querySelectorAll('#reportsListWrap .report-swipe-item.open').forEach(el => {",
    "document.querySelectorAll('#reportsListWrap .report-swipe-item.open, #userTicketsListWrap .report-swipe-item.open').forEach(el => {"
)
js = js.replace(
    "const items = document.querySelectorAll('#reportsListWrap .report-swipe-item');",
    "const items = document.querySelectorAll('#reportsListWrap .report-swipe-item, #userTicketsListWrap .report-swipe-item');"
)
js = js.replace(
    "document.querySelectorAll('#reportsListWrap .report-swipe-item.open').forEach(el => {",
    "document.querySelectorAll('#reportsListWrap .report-swipe-item.open, #userTicketsListWrap .report-swipe-item.open').forEach(el => {"
)

# Update renderUserTicketsList to mirror renderReportsList style
new_render_tickets = """  function filterUserTickets(filter, btnEl) {
    activeTicketFilter = filter;
    document.querySelectorAll('#ticketsFilterTabs .filter-tab').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    renderUserTicketsList(filter);
  }

  function renderUserTicketsList(filter = activeTicketFilter) {
    const wrap = document.getElementById('userTicketsListWrap');
    if (!wrap) return;

    const countBadge = document.getElementById('userTicketsCountBadge');
    if (countBadge) countBadge.textContent = toPersianDigits(tickets.length);
    const repBadge = document.getElementById('reportsCountBadge');
    if (repBadge) repBadge.textContent = toPersianDigits(reports.length);

    const isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');
    const deleteWord = isEn ? 'Delete' : 'حذف';
    const emptyMsg = isEn ? 'No tickets found in this category' : 'تیکتی در این دسته یافت نشد';

    let filtered = tickets;
    if (filter === 'pending') {
      filtered = tickets.filter(t => (!t.reply || !t.reply.trim()) && (t.status === 'pending' || !t.status));
    } else if (filter === 'done' || filter === 'answered') {
      filtered = tickets.filter(t => (t.reply && t.reply.trim()) || t.status === 'done' || t.status === 'answered');
    } else if (filter === 'review' || filter === 'in_progress') {
      filtered = tickets.filter(t => t.status === 'in_progress' || t.status === 'review');
    }

    if (filtered.length === 0) {
      wrap.innerHTML = `<div style="text-align:center; padding:30px 10px; color:var(--text-muted); font-size:13px;">${emptyMsg}</div>`;
      return;
    }

    wrap.innerHTML = filtered.map(t => {
      const hasReply = !!(t.reply && t.reply.trim());
      let statusMeta = getStatusMeta(t.status);
      let statusLabel = statusMeta.label;
      if (hasReply) {
        statusLabel = isEn ? 'Answered' : 'پاسخ داده شده';
      } else if (t.status === 'pending') {
        statusLabel = isEn ? 'Pending' : 'در انتظار';
      } else if (t.status === 'in_progress' || t.status === 'review') {
        statusLabel = isEn ? 'In Review' : 'بررسی';
      }
      const displayDate = t.dateTime || formatReportDateTime(t.created_at);

      return `
        <div class="report-swipe">
          <div class="report-delete-bg" onpointerdown="event.stopPropagation()" onclick="confirmDeleteTicket('${t.id}', event)">
            <div class="delete-action" style="color:#ef4444;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3,6 5,6 21,6"/><path d="M19,6 L19,20 a2,2 0 0 1 -2,2 H7 a2,2 0 0 1 -2,-2 L5,6"/><path d="M8,6 V4 a2,2 0 0 1 2,-2 h4 a2,2 0 0 1 2,2 v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
              <span style="color:#ef4444; font-weight:800;">${deleteWord}</span>
            </div>
          </div>
          <div class="report-swipe-item" onclick="openTicketDetail('${t.id}')">
            <div class="report-item">
              <span class="report-status ${statusMeta.className}">${statusLabel}</span>
              <div class="report-info">
                <h4>${escapeHtml(t.title)}</h4>
                <p>${escapeHtml(t.department || 'پشتیبانی شهرداری')} - ${displayDate}${hasReply ? ' <span style="color:#10b981; font-weight:700;">(پاسخ شهرداری)</span>' : ''}</p>
              </div>
              <div class="report-icon-box" style="background:rgba(0,201,167,0.16); color:var(--teal);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:20px;height:20px;"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M7 15h0M2 9.5h20M2 14.5h20"/></svg>
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');
    initReportSwipe();
  }"""

old_render_tickets_pattern = r'function filterUserTickets\(filter, btnEl\) \{.*?function openTicketDetail\(id\) \{'
match_fn = re.search(old_render_tickets_pattern, js, flags=re.DOTALL)
if match_fn:
    js = js[:match_fn.start()] + new_render_tickets + "\n\n  function openTicketDetail(id) {" + js[match_fn.end():]
    print("   -> renderUserTicketsList replaced with reports-style cards & swipe delete!")
else:
    print("   [ERR] Could not locate old filterUserTickets/renderUserTicketsList.")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Saved files successfully!")
