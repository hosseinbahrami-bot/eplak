#!/usr/bin/env python3
import sys

# Paths for style.css
css_files = [
    '/home/user/eplak/eplak-fixed/assets/css/style.css',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/assets/css/style.css',
    '/home/user/eplak/ios-app/Eplak/Web/assets/css/style.css'
]

vip_card_css = '''
  /* =========================================================
     کادر بزرگ دیدار حضوری با شهردار و شورای شهر (ترکیب دو کادر در بالای عوارض و کسب و کار)
     ========================================================= */
  .svc-vip-meeting-card {
    grid-column: 1 / -1;
    min-height: auto;
    background: linear-gradient(135deg, rgba(0, 201, 167, 0.16) 0%, rgba(16, 185, 129, 0.08) 45%, rgba(6, 95, 70, 0.2) 100%);
    border: 1.5px solid rgba(0, 201, 167, 0.45);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 22px;
    padding: 16px 16px 14px;
    display: flex;
    flex-direction: column;
    gap: 9px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 8px 26px -4px rgba(0, 201, 167, 0.22), inset 0 1px 1px rgba(255, 255, 255, 0.2);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    -webkit-tap-highlight-color: transparent;
  }
  .svc-vip-meeting-card::before {
    content: '';
    position: absolute;
    top: -40px;
    right: -40px;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, rgba(0, 201, 167, 0.32) 0%, transparent 70%);
    pointer-events: none;
    border-radius: 50%;
  }
  body.lang-en .svc-vip-meeting-card::before,
  html[dir="ltr"] .svc-vip-meeting-card::before {
    right: auto;
    left: -40px;
  }
  .svc-vip-meeting-card:hover {
    transform: translateY(-3px);
    border-color: rgba(0, 201, 167, 0.75);
    box-shadow: 0 12px 32px -4px rgba(0, 201, 167, 0.35), inset 0 1px 2px rgba(255, 255, 255, 0.3);
  }
  .svc-vip-meeting-card:active {
    transform: scale(0.98);
  }
  .svc-vip-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 2;
  }
  .svc-vip-top-left {
    display: flex;
    align-items: center;
    gap: 9px;
  }
  .svc-vip-icon {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    background: linear-gradient(135deg, rgba(0, 201, 167, 0.32), rgba(16, 185, 129, 0.38));
    border: 1px solid rgba(0, 201, 167, 0.55);
    box-shadow: 0 4px 14px rgba(0, 201, 167, 0.28);
  }
  .svc-vip-badge {
    font-size: 11px;
    font-weight: 800;
    padding: 3.5px 9px;
    border-radius: 12px;
    background: rgba(0, 201, 167, 0.2);
    color: var(--teal);
    border: 1px solid rgba(0, 201, 167, 0.35);
    letter-spacing: 0.2px;
  }
  .svc-vip-tag {
    font-size: 11px;
    font-weight: 700;
    color: var(--teal);
    background: rgba(0, 201, 167, 0.12);
    padding: 3.5px 9px;
    border-radius: 12px;
    border: 1px solid rgba(0, 201, 167, 0.22);
  }
  .svc-vip-body {
    position: relative;
    z-index: 2;
    text-align: right;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  body.lang-en .svc-vip-body,
  html[dir="ltr"] .svc-vip-body {
    text-align: left;
  }
  .svc-vip-title {
    font-size: 15px;
    font-weight: 900;
    color: var(--text-primary);
    line-height: 1.45;
    margin: 0;
  }
  .svc-vip-desc {
    font-size: 11.5px;
    color: var(--text-muted);
    line-height: 1.65;
    margin: 0;
  }
  .svc-vip-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 2;
    margin-top: 4px;
    padding-top: 9px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }
  .svc-vip-action {
    font-size: 12px;
    font-weight: 800;
    color: var(--teal);
  }
  .svc-vip-arrow {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(0, 201, 167, 0.2);
    border: 1px solid rgba(0, 201, 167, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--teal);
    font-size: 13px;
    font-weight: 800;
    transition: transform 0.22s ease;
  }
  .svc-vip-meeting-card:hover .svc-vip-arrow {
    transform: translateX(-4px);
  }
  body.lang-en .svc-vip-meeting-card:hover .svc-vip-arrow,
  html[dir="ltr"] .svc-vip-meeting-card:hover .svc-vip-arrow {
    transform: translateX(4px);
  }
'''

for cp in css_files:
    with open(cp, 'r', encoding='utf-8') as f:
        c = f.read()
    if '.svc-vip-meeting-card' not in c:
        marker = '  /* =========================================================\n     ===== پنل‌های بخش خدمات (سبک پیشخوان) ====='
        if marker in c:
            c = c.replace(marker, vip_card_css + '\n' + marker)
        else:
            c += '\n' + vip_card_css
        with open(cp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated CSS: {cp}")
    else:
        print(f"CSS already has .svc-vip-meeting-card: {cp}")

# Update services.js
services_files = [
    '/home/user/eplak/eplak-fixed/modules/services.js',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/modules/services.js',
    '/home/user/eplak/ios-app/Eplak/Web/modules/services.js'
]

meeting_card_js_snippet = '''    // گرید کادرهای مربعی مدرن (۶ بخش اصلی)
    html += '<div class="svc-square-grid">';

    // کادر بزرگ دیدار حضوری با اعضای شورای شهر و شهردار محترم (ترکیب دو کادر در یک کادر تمام‌عرض بالای عوارض شهرداری و کسب و کار)
    const meetingTitle = isEn
      ? 'Request in-person meeting with City Council & Mayor'
      : 'درخواست دیدار حضوری با اعضای شورای شهر و شهردار محترم';
    const meetingBadge = isEn ? 'Face-to-Face Meeting' : 'دیدار چهره‌به‌چهره';
    const meetingTag = isEn ? 'Direct Municipal Access' : 'ارتباط مستقیم با مدیریت شهری';
    const meetingDesc = isEn
      ? 'Book in-person appointment, direct public audience with Mayor and City Council members for citizen issues and proposals.'
      : 'ثبت نوبت ملاقات عمومی، پیگیری مستقیم مطالبات شهری و طرح چهره‌به‌چهره موضوعات با مدیریت ارشد شهرداری و اعضای شورا';
    const meetingAction = isEn ? 'Book Appointment & Submit Request' : 'رزرو وقت و ثبت درخواست دیدار';

    html += '<div class="svc-vip-meeting-card" onclick="openMayorMeetingService()">' +
      '<div class="svc-vip-top">' +
        '<div class="svc-vip-top-left">' +
          '<div class="svc-vip-icon">🏛️</div>' +
          '<span class="svc-vip-badge">' + meetingBadge + '</span>' +
        '</div>' +
        '<span class="svc-vip-tag">' + meetingTag + '</span>' +
      '</div>' +
      '<div class="svc-vip-body">' +
        '<h3 class="svc-vip-title">' + meetingTitle + '</h3>' +
        '<p class="svc-vip-desc">' + meetingDesc + '</p>' +
      '</div>' +
      '<div class="svc-vip-footer">' +
        '<span class="svc-vip-action">' + meetingAction + '</span>' +
        '<span class="svc-vip-arrow">' + (isEn ? '→' : '←') + '</span>' +
      '</div>' +
    '</div>';'''

meeting_funcs_js = '''
  /* =========================================================
     درخواست دیدار حضوری با شهردار و اعضای شورای اسلامی شهر
  ========================================================= */
  function openMayorMeetingService() {
    const userPhone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : (localStorage.getItem('eplak_phone') || '');
    const phoneInput = document.getElementById('meetingPhoneInput');
    if (phoneInput && userPhone) {
      phoneInput.value = userPhone;
    }
    const nameDisplay = document.getElementById('profileNameDisplay');
    const nameInput = document.getElementById('meetingNameInput');
    if (nameInput && nameDisplay && nameDisplay.textContent && nameDisplay.textContent.trim() !== 'شهروند') {
      nameInput.value = nameDisplay.textContent.trim();
    }
    showScreen('screen-mayor-meeting');
  }

  function submitMayorMeetingRequest() {
    const targetSel = document.getElementById('meetingTargetSelect');
    const nameInp = document.getElementById('meetingNameInput');
    const phoneInp = document.getElementById('meetingPhoneInput');
    const subjInp = document.getElementById('meetingSubjectInput');
    const descInp = document.getElementById('meetingDescInput');

    const target = (targetSel ? targetSel.value : 'شهردار محترم ورامین').trim();
    const name = (nameInp ? nameInp.value : '').trim();
    const phone = (phoneInp ? phoneInp.value : '').trim() || (typeof getCurrentPhone === 'function' ? getCurrentPhone() : (localStorage.getItem('eplak_phone') || '09120000000'));
    const subject = (subjInp ? subjInp.value : '').trim();
    const desc = (descInp ? descInp.value : '').trim();

    if (!subject) {
      if (typeof showToast === 'function') showToast('لطفاً موضوع ملاقات حضوری را وارد کنید');
      return;
    }
    if (!desc) {
      if (typeof showToast === 'function') showToast('لطفاً توضیحات درخواست را وارد فرمایید');
      return;
    }

    const title = 'دیدار حضوری: ' + subject;
    const fullDesc = 'طرف ملاقات: ' + target + '\\nمتقاضی: ' + (name || 'شهروند') + ' (' + phone + ')\\n\\nشرح موضوع:\\n' + desc;

    const localCode = 'TK-1403-' + String(1000 + (window.tickets ? window.tickets.length + 1 : 1)).padStart(4, '0');
    const nowIso = new Date().toISOString();

    const newTicket = {
      id: 'tk_' + Date.now(),
      code: localCode,
      title: title,
      description: fullDesc,
      category: 'دیدار حضوری و ملاقات مردمی',
      department: 'دفتر شهردار و شورای شهر',
      priority: 'high',
      status: 'pending',
      reply: '',
      user_phone: phone,
      created_at: nowIso,
      dateTime: typeof formatReportDateTime === 'function' ? formatReportDateTime(nowIso) : ''
    };

    if (window.tickets) {
      window.tickets.unshift(newTicket);
      if (typeof saveTickets === 'function') saveTickets(phone);
    }

    const codeElem = document.getElementById('successTicketCode');
    if (codeElem) codeElem.textContent = localCode;

    if (window.soundManager && typeof window.soundManager.playDing === 'function') {
      window.soundManager.playDing();
    }

    // پاکسازی فیلدها
    if (subjInp) subjInp.value = '';
    if (descInp) descInp.value = '';

    // انتقال آنی بدون لگ
    showScreen('screen-ticket-success');

    // همگام‌سازی در سرور
    const payload = {
      userPhone: phone,
      name: name,
      title: title,
      description: fullDesc,
      category: 'دیدار حضوری و ملاقات مردمی',
      department: 'دفتر شهردار و شورای شهر',
      priority: 'high',
      status: 'pending'
    };

    const syncPromise = (typeof window.syncDataToBackend === 'function')
      ? window.syncDataToBackend('tickets', payload)
      : fetch('api/tickets.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(function (r) { return r.json(); });

    syncPromise.then(function (data) {
      if (data && data.success) {
        if (data.tracking_code) {
          newTicket.code = data.tracking_code;
          if (codeElem) codeElem.textContent = data.tracking_code;
        }
        if (data.id) newTicket.id = String(data.id);
        if (typeof saveTickets === 'function') saveTickets(phone);
        if (typeof renderUserTicketsList === 'function') renderUserTicketsList();
      }
    }).catch(function (err) {
      console.warn('[meeting] background sync note:', err);
    });
  }

  window.openMayorMeetingService = openMayorMeetingService;
  window.submitMayorMeetingRequest = submitMayorMeetingRequest;
'''

old_grid_start = "    // گرید کادرهای مربعی مدرن (۶ بخش اصلی)\n    html += '<div class=\"svc-square-grid\">';"

for sp in services_files:
    with open(sp, 'r', encoding='utf-8') as f:
        sc = f.read()

    if 'svc-vip-meeting-card' not in sc:
        if old_grid_start in sc:
            sc = sc.replace(old_grid_start, meeting_card_js_snippet)
            print(f"Added meeting card to renderServices in {sp}")
        else:
            print(f"Warning: old_grid_start not found in {sp}")

    if 'openMayorMeetingService' not in sc:
        export_marker = '  window.renderServices = renderServices;'
        if export_marker in sc:
            sc = sc.replace(export_marker, meeting_funcs_js + '\n' + export_marker)
            print(f"Added meeting functions to {sp}")
        else:
            print(f"Warning: export_marker not found in {sp}")

    with open(sp, 'w', encoding='utf-8') as f:
        f.write(sc)

print("Services files updated successfully.")
