#!/usr/bin/env python3

services_files = [
    '/home/user/eplak/eplak-fixed/modules/services.js',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/modules/services.js',
    '/home/user/eplak/ios-app/Eplak/Web/modules/services.js'
]

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

for sp in services_files:
    with open(sp, 'r', encoding='utf-8') as f:
        sc = f.read()

    if 'function openMayorMeetingService' not in sc:
        marker = '  window.renderServices = renderServices;'
        if marker in sc:
            sc = sc.replace(marker, meeting_funcs_js + '\n' + marker)
            with open(sp, 'w', encoding='utf-8') as f:
                f.write(sc)
            print(f"Added meeting functions to {sp}")
        else:
            print(f"Marker not found in {sp}")
    else:
        print(f"Functions already in {sp}")

print("Done.")
