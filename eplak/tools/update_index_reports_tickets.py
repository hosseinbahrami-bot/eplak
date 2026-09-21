import re

html_path = '/home/user/eplak/eplak-fixed/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Home screen service_track_report_sub
html = html.replace(
    '<p data-i18n="service_track_report_sub">وضعیت گزارش‌ها</p>',
    '<p data-i18n="service_track_report_sub">وضعیت گزارش‌ها و تیکت‌ها</p>'
)

# 2. Update screen-reports
reports_old_block = """      <div style="padding:0 20px; display:flex; align-items:center; gap:8px; justify-content:flex-start;">
        <h2 style="font-size:18px; font-weight:800;">گزارش‌های من</h2>
        <span class="badge-count" id="reportsCountBadge">4</span>
      </div>

      <!-- Filter Tabs -->
      <div style="display:flex; gap:8px; padding:0 16px; overflow-x:auto;" id="reportsFilterTabs">
        <button class="filter-tab active" data-filter="all" onclick="filterReports('all', this)">همه</button>
        <button class="filter-tab" data-filter="pending" onclick="filterReports('pending', this)">در انتظار</button>
        <button class="filter-tab" data-filter="done" onclick="filterReports('done', this)">انجام شده</button>
        <button class="filter-tab" data-filter="review" onclick="filterReports('review', this)">بررسی</button>
      </div>

      <!-- Reports List -->
      <div class="reports-list" id="reportsListWrap"></div>

      <!-- Add New Report Button -->
      <div style="padding:0 16px;">
        <button class="btn-teal" onclick="startNewReport()">
          <span>+ ثبت گزارش جدید</span>
        </button>
      </div>

      <!-- بخش ثبت تیکت (اتصال مستقیم به پنل تیکت ادمین) -->
      <div style="padding:0 16px; margin-top:8px;">
        <div class="glass-card" style="padding:16px; display:flex; flex-direction:column; gap:10px; border:1px solid rgba(0,201,167,0.28); background:linear-gradient(135deg, rgba(0,201,167,0.09), rgba(0,180,140,0.03)); border-radius:18px;">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:20px;">🎫</span>
              <span style="font-size:14px; font-weight:800; color:var(--text-primary);">ثبت تیکت</span>
            </div>
            <span style="font-size:11px; color:var(--teal); font-weight:700; background:rgba(0,201,167,0.12); padding:3px 8px; border-radius:10px;">ارتباط مستقیم با مدیریت شهرداری</span>
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

      <!-- لیست تیکت‌های ارسالی کاربر به مدیریت -->
      <div style="padding:0 16px; margin-top:6px;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
          <span style="font-size:13.5px; font-weight:800; color:var(--text-primary);">تیکت‌های ارسالی شما</span>
          <span id="userTicketsCountBadge" style="font-size:11.5px; background:rgba(0,201,167,0.15); color:var(--teal); padding:2px 8px; border-radius:10px; font-weight:800;">۰</span>
        </div>
        <div id="userTicketsListWrap" style="display:flex; flex-direction:column; gap:10px;"></div>
      </div>"""

reports_new_block = """      <!-- Segmented main switcher: گزارش‌های من vs تیکت‌های من -->
      <div style="padding:0 16px;">
        <div class="reports-main-switcher" id="reportsMainSwitcher">
          <div class="reports-switcher-indicator" id="reportsSwitcherIndicator"></div>
          <button type="button" class="reports-switcher-btn active" id="tabBtnReports" onclick="switchReportsMainTab('reports', this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            <span>گزارش‌های من</span>
            <span class="reports-counter-pill" id="reportsCountBadge">0</span>
          </button>
          <button type="button" class="reports-switcher-btn" id="tabBtnTickets" onclick="switchReportsMainTab('tickets', this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M7 15h0M2 9.5h20M2 14.5h20"/></svg>
            <span>تیکت‌های من</span>
            <span class="reports-counter-pill" id="userTicketsCountBadge">0</span>
          </button>
        </div>
      </div>

      <!-- ============ بخش اول: گزارش‌های من ============ -->
      <div id="sectionReportsPane" class="reports-section-pane active" style="display:flex; flex-direction:column; gap:12px;">
        <!-- Filter Tabs -->
        <div style="display:flex; gap:8px; padding:0 16px; overflow-x:auto;" id="reportsFilterTabs">
          <button class="filter-tab active" data-filter="all" onclick="filterReports('all', this)">همه</button>
          <button class="filter-tab" data-filter="pending" onclick="filterReports('pending', this)">در انتظار</button>
          <button class="filter-tab" data-filter="done" onclick="filterReports('done', this)">انجام شده</button>
          <button class="filter-tab" data-filter="review" onclick="filterReports('review', this)">بررسی</button>
        </div>

        <!-- Reports List -->
        <div class="reports-list" id="reportsListWrap"></div>

        <!-- Add New Report Button -->
        <div style="padding:0 16px;">
          <button class="btn-teal" onclick="startNewReport()">
            <span>+ ثبت گزارش جدید</span>
          </button>
        </div>
      </div>

      <!-- ============ بخش دوم: تیکت‌های من ============ -->
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

if reports_old_block in html:
    html = html.replace(reports_old_block, reports_new_block)
    print("   -> screen-reports updated successfully!")
else:
    print("   [!] Could not find exact reports_old_block, checking with regex...")
    # fallback regex
    pattern = r'<div style="padding:0 20px; display:flex; align-items:center; gap:8px; justify-content:flex-start;">\s*<h2 style="font-size:18px; font-weight:800;">گزارش‌های من</h2>.*?<div id="userTicketsListWrap"[^>]*></div>\s*</div>'
    match = re.search(pattern, html, flags=re.DOTALL)
    if match:
        html = html[:match.start()] + reports_new_block + html[match.end():]
        print("   -> screen-reports updated via regex!")
    else:
        print("   [ERR] Regex failed to match reports block.")

# 3. Update screen-ticket-detail with delete button
detail_old = """      <!-- پاسخ مدیریت شهرداری -->
      <div id="ticketDetailReplyCard" class="glass-card" style="display:none; padding:16px; border:1px solid rgba(0,201,167,0.35); background:rgba(0,201,167,0.06); flex-direction:column; gap:8px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">🏛️</span>
          <span style="font-size:13px; font-weight:800; color:var(--teal);">پاسخ کارشناس / مدیریت شهرداری:</span>
        </div>
        <p id="ticketDetailReply" style="font-size:13px; line-height:1.9; color:var(--text-primary); margin:0; white-space:pre-line; text-align:right;">—</p>
      </div>

      <button class="btn-teal" onclick="goBack()" style="margin-top:8px;">بازگشت</button>"""

detail_new = """      <!-- پاسخ مدیریت شهرداری -->
      <div id="ticketDetailReplyCard" class="glass-card" style="display:none; padding:16px; border:1px solid rgba(0,201,167,0.35); background:rgba(0,201,167,0.06); flex-direction:column; gap:8px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:18px;">🏛️</span>
          <span style="font-size:13px; font-weight:800; color:var(--teal);">پاسخ کارشناس / مدیریت شهرداری:</span>
        </div>
        <p id="ticketDetailReply" style="font-size:13px; line-height:1.9; color:var(--text-primary); margin:0; white-space:pre-line; text-align:right;">—</p>
      </div>

      <div style="display:flex; gap:10px; margin-top:10px;">
        <button class="btn-secondary" onclick="goBack()" style="flex:1; padding:12px 16px;">بازگشت</button>
        <button type="button" class="btn-danger-outline" id="ticketDetailDeleteBtn" onclick="deleteCurrentOpenTicket()" style="flex:1; padding:12px 16px; display:flex; align-items:center; justify-content:center; gap:6px; font-weight:700;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
          <span>حذف تیکت</span>
        </button>
      </div>"""

if detail_old in html:
    html = html.replace(detail_old, detail_new)
    print("   -> screen-ticket-detail updated successfully!")
else:
    print("   [!] Could not find exact detail_old, trying regex...")
    pattern_detail = r'(<div id="ticketDetailReplyCard"[^>]*>.*?</div>\s*)<button class="btn-teal" onclick="goBack\(\)"[^>]*>بازگشت</button>'
    match_d = re.search(pattern_detail, html, flags=re.DOTALL)
    if match_d:
        html = html[:match_d.start(1)] + match_d.group(1) + """      <div style="display:flex; gap:10px; margin-top:10px;">
        <button class="btn-secondary" onclick="goBack()" style="flex:1; padding:12px 16px;">بازگشت</button>
        <button type="button" class="btn-danger-outline" id="ticketDetailDeleteBtn" onclick="deleteCurrentOpenTicket()" style="flex:1; padding:12px 16px; display:flex; align-items:center; justify-content:center; gap:6px; font-weight:700;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
          <span>حذف تیکت</span>
        </button>
      </div>""" + html[match_d.end():]
        print("   -> screen-ticket-detail updated via regex!")

# 4. Update screen-track
track_old = """    <div class="screen-content" style="position:relative;z-index:10; gap:14px; padding:0 16px 20px;">
      <p style="font-size:13px; color:var(--text-muted); text-align:right;">کد پیگیری دریافتی هنگام ثبت گزارش را وارد کنید یا از بین گزارش‌های اخیر انتخاب کنید</p>

      <div style="display:flex; flex-direction:column; gap:10px;">
        <input type="text" id="trackCodeInput" class="input-field" placeholder="مثلاً EP-1403-0021" style="direction:ltr; text-align:left; width:100%;">
        <button class="btn-teal" style="width:100%; padding:12px 18px; font-weight:700;" onclick="searchByTrackCode()">جستجو</button>
      </div>

      <div id="trackResultBox"></div>

      <div class="section-title" style="padding:0 4px; margin-top:6px;">گزارش‌های اخیر</div>
      <div class="reports-list" id="trackRecentList"></div>

      <div class="bottom-pad"></div>
    </div>"""

track_new = """    <div class="screen-content" style="position:relative;z-index:10; gap:14px; padding:0 16px 20px;">
      <p style="font-size:13px; color:var(--text-muted); text-align:right; margin:0; line-height:1.7;">
        کد پیگیری گزارش (مثل EP-...) یا تیکت (مثل TK-...) را وارد نمایید یا از درخواست‌های اخیر پیگیری فرمایید
      </p>

      <div style="display:flex; flex-direction:column; gap:10px;">
        <input type="text" id="trackCodeInput" class="input-field" placeholder="مثلاً EP-1403-0021 یا TK-1403-0012" style="direction:ltr; text-align:left; width:100%;">
        <button class="btn-teal" style="width:100%; padding:12px 18px; font-weight:700;" onclick="searchByTrackCode()">جستجو و پیگیری</button>
      </div>

      <div id="trackResultBox"></div>

      <!-- تب‌های فیلتر پیگیری: همه / گزارش‌ها / تیکت‌ها -->
      <div style="display:flex; gap:8px; overflow-x:auto; margin-top:2px;" id="trackFilterTabs">
        <button class="filter-tab active" data-trackfilter="all" onclick="filterTrackList('all', this)">همه موارد</button>
        <button class="filter-tab" data-trackfilter="reports" onclick="filterTrackList('reports', this)">📋 گزارش‌ها</button>
        <button class="filter-tab" data-trackfilter="tickets" onclick="filterTrackList('tickets', this)">🎫 تیکت‌ها</button>
      </div>

      <div class="reports-list" id="trackRecentList"></div>

      <div class="bottom-pad"></div>
    </div>"""

if track_old in html:
    html = html.replace(track_old, track_new)
    print("   -> screen-track updated successfully!")
else:
    print("   [!] Could not find exact track_old, trying regex...")
    pattern_track = r'(<div class="screen" id="screen-track">.*?<div class="screen-content"[^>]*>)\s*<p[^>]*>.*?<\/p>\s*<div style="display:flex; flex-direction:column; gap:10px;">.*?<div class="reports-list" id="trackRecentList"><\/div>\s*<div class="bottom-pad"><\/div>\s*<\/div>'
    match_t = re.search(pattern_track, html, flags=re.DOTALL)
    if match_t:
        html = html[:match_t.start(1)] + match_t.group(1) + """
      <p style="font-size:13px; color:var(--text-muted); text-align:right; margin:0; line-height:1.7;">
        کد پیگیری گزارش (مثل EP-...) یا تیکت (مثل TK-...) را وارد نمایید یا از درخواست‌های اخیر پیگیری فرمایید
      </p>

      <div style="display:flex; flex-direction:column; gap:10px;">
        <input type="text" id="trackCodeInput" class="input-field" placeholder="مثلاً EP-1403-0021 یا TK-1403-0012" style="direction:ltr; text-align:left; width:100%;">
        <button class="btn-teal" style="width:100%; padding:12px 18px; font-weight:700;" onclick="searchByTrackCode()">جستجو و پیگیری</button>
      </div>

      <div id="trackResultBox"></div>

      <!-- تب‌های فیلتر پیگیری: همه / گزارش‌ها / تیکت‌ها -->
      <div style="display:flex; gap:8px; overflow-x:auto; margin-top:2px;" id="trackFilterTabs">
        <button class="filter-tab active" data-trackfilter="all" onclick="filterTrackList('all', this)">همه موارد</button>
        <button class="filter-tab" data-trackfilter="reports" onclick="filterTrackList('reports', this)">📋 گزارش‌ها</button>
        <button class="filter-tab" data-trackfilter="tickets" onclick="filterTrackList('tickets', this)">🎫 تیکت‌ها</button>
      </div>

      <div class="reports-list" id="trackRecentList"></div>

      <div class="bottom-pad"></div>
    </div>""" + html[match_t.end():]
        print("   -> screen-track updated via regex!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("[3] index.html updated successfully!")
