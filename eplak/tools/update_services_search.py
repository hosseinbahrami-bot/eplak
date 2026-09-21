#!/usr/bin/env python3
import sys

services_files = [
    '/home/user/eplak/eplak-fixed/modules/services.js',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/modules/services.js',
    '/home/user/eplak/ios-app/Eplak/Web/modules/services.js'
]

# We will replace renderServices() and add the new search & target selection functions.

new_render_services = '''  /* =========================================================
     Render — صفحه خدمات (کادر جستجوی مدرن + کادرهای مربعی ۶ گانه)
  ========================================================= */
  function renderServices() {
    const wrap = document.getElementById('servicesListWrap');
    if (!wrap) return;

    const isEn = isEnglishActive();
    const groups = getServiceGroups();
    const services = getServicesList();
    const totalServices = services.length;

    const statsText = isEn
      ? svcPersianDigits(groups.length) + ' Main Categories • ' + svcPersianDigits(totalServices) + ' Online Services'
      : svcPersianDigits(groups.length) + ' بخش اصلی • ' + svcPersianDigits(totalServices) + ' خدمت برخط شهری';
    
    const hintText = isEn
      ? 'Tap any category below to access its specialized municipal services:'
      : 'برای مشاهده خدمات تخصصی هر حوزه، کادر مربوطه را لمس کنید:';

    const searchPlaceholder = isEn
      ? 'Search municipal services, taxes, permits, mayor meeting...'
      : 'جستجوی هوشمند در خدمات، عوارض، مجوزها، دیدار حضوری...';

    let html = '';

    // کادر مدرن و شیک جستجوی خدمات شهری
    html += '<div class="svc-search-container">' +
      '<div class="svc-search-box">' +
        '<div class="svc-search-icon-box">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>' +
        '</div>' +
        '<input type="text" id="mainServicesSearchInput" class="svc-search-input" placeholder="' + searchPlaceholder + '" oninput="handleMainServicesSearch(this.value)" autocomplete="off">' +
        '<button type="button" id="mainServicesSearchClear" class="svc-search-clear" onclick="clearMainServicesSearch()" style="display:none;" aria-label="' + (isEn ? 'Clear' : 'پاک کردن') + '">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' +
        '</button>' +
      '</div>' +
      '<div class="svc-quick-tags" id="svcQuickTags">' +
        '<button type="button" class="svc-quick-tag" data-term="دیدار" onclick="quickFilterServices(\\'دیدار حضوری\\')">🏛️ ' + (isEn ? 'Mayor Meeting' : 'دیدار با شهردار') + '</button>' +
        '<button type="button" class="svc-quick-tag" data-term="عوارض" onclick="quickFilterServices(\\'عوارض\\')">💳 ' + (isEn ? 'Taxes' : 'عوارض و نوسازی') + '</button>' +
        '<button type="button" class="svc-quick-tag" data-term="کسب" onclick="quickFilterServices(\\'کسب و کار\\')">🏪 ' + (isEn ? 'Business' : 'کسب و کار') + '</button>' +
        '<button type="button" class="svc-quick-tag" data-term="پسماند" onclick="quickFilterServices(\\'پسماند\\')">♻️ ' + (isEn ? 'Recycling' : 'پسماند و تفکیک') + '</button>' +
        '<button type="button" class="svc-quick-tag" data-term="ترافیک" onclick="quickFilterServices(\\'ترافیک\\')">🚇 ' + (isEn ? 'Transport' : 'حمل‌ونقل و ترافیک') + '</button>' +
        '<button type="button" class="svc-quick-tag" data-term="مناقصه" onclick="quickFilterServices(\\'مناقصه\\')">📑 ' + (isEn ? 'Tenders' : 'مناقصات') + '</button>' +
        '<button type="button" class="svc-quick-tag" data-term="آرامستان" onclick="quickFilterServices(\\'آرامستان\\')">🕊️ ' + (isEn ? 'Cemeteries' : 'آرامستان‌ها') + '</button>' +
      '</div>' +
    '</div>';

    // مخزن اختصاصی نمایش نتایج جستجوی زنده
    html += '<div id="mainServicesSearchResults" style="display:none; padding:0 16px; margin-bottom:14px;"></div>';

    // نوار وضعیت مختصر بالای دسته‌بندی‌ها
    html += '<div id="servicesCountStrip" class="svc-count-strip" style="margin:0 16px 8px;">' +
      '<span class="svc-count-num">' + svcPersianDigits(groups.length) + '</span>' +
      '<span class="svc-count-label">' + (isEn ? 'Categories' : 'بخش خدمات') + '</span>' +
      '<span class="svc-count-sep"></span>' +
      '<span class="svc-count-hint">' + statsText + '</span>' +
    '</div>';

    html += '<p id="servicesHintText" style="font-size:12px; color:var(--text-muted); margin:0 18px 4px; text-align:' + (isEn ? 'left' : 'right') + ';">' + hintText + '</p>';

    // گرید کادرهای مربعی مدرن (۶ بخش اصلی + کادر بزرگ دیدار حضوری در بالا)
    html += '<div class="svc-square-grid" id="servicesMainGridWrap">';

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
    '</div>';

    groups.forEach(function (group) {
      html += '' +
        '<div class="svc-square-card" style="--accent-rgb:' + group.accent + '; --accent-color:' + group.accentColor + ';" onclick="openServiceCategory(\\'' + group.id + '\\')">' +
          '<div class="svc-square-top">' +
            '<div class="svc-square-icon">' + renderLuxIcon(group.id, group.icon) + '</div>' +
            '<span class="svc-square-badge">' + group.badge + '</span>' +
          '</div>' +
          '<div class="svc-square-body">' +
            '<h3 class="svc-square-title">' + group.title + '</h3>' +
            '<p class="svc-square-sub">' + group.desc + '</p>' +
            '<div class="svc-square-footer">' +
              '<span>' + (isEn ? 'View Services' : 'مشاهده خدمات') + '</span>' +
              '<span class="svc-square-arrow">' + (isEn ? '→' : '←') + '</span>' +
            '</div>' +
          '</div>' +
        '</div>';
    });
    html += '</div>';

    wrap.innerHTML = html;
  }'''

search_functions = '''
  /* =========================================================
     جستجوی هوشمند و همه‌جانبه خدمات شهری در صفحه خدمات
  ========================================================= */
  function handleMainServicesSearch(keyword) {
    const term = (keyword || '').trim().toLowerCase();
    const clearBtn = document.getElementById('mainServicesSearchClear');
    const resultsWrap = document.getElementById('mainServicesSearchResults');
    const gridWrap = document.getElementById('servicesMainGridWrap');
    const countStrip = document.getElementById('servicesCountStrip');
    const hintText = document.getElementById('servicesHintText');
    const quickTagsWrap = document.getElementById('svcQuickTags');

    if (clearBtn) {
      clearBtn.style.display = term ? 'flex' : 'none';
    }

    if (quickTagsWrap) {
      const tags = quickTagsWrap.querySelectorAll('.svc-quick-tag');
      tags.forEach(function (tag) {
        const tagText = tag.getAttribute('data-term') || tag.textContent;
        tag.classList.toggle('active', term && tagText.includes(term));
      });
    }

    if (!term) {
      if (resultsWrap) {
        resultsWrap.style.display = 'none';
        resultsWrap.innerHTML = '';
      }
      if (gridWrap) gridWrap.style.display = 'grid';
      if (countStrip) countStrip.style.display = 'flex';
      if (hintText) hintText.style.display = 'block';
      return;
    }

    if (gridWrap) gridWrap.style.display = 'none';
    if (countStrip) countStrip.style.display = 'none';
    if (hintText) hintText.style.display = 'none';
    if (!resultsWrap) return;

    resultsWrap.style.display = 'flex';
    resultsWrap.style.flexDirection = 'column';
    resultsWrap.style.gap = '10px';

    const isEn = isEnglishActive();
    const services = getServicesList();

    // بررسی تطابق با کارت دیدار حضوری
    const meetingMatch = (
      term.includes('دیدار') || term.includes('شهردار') || term.includes('شورا') ||
      term.includes('ملاقات') || term.includes('حضوری') || term.includes('جلسه') ||
      term.includes('نوبت') || term.includes('وقت') ||
      term.includes('mayor') || term.includes('council') || term.includes('meeting')
    );

    // جستجو در ۲۵+ خدمت شهری
    const matchedServices = services.filter(function (s) {
      const haystack = (
        (s.title || '') + ' ' +
        (s.short || '') + ' ' +
        (s.sub || '') + ' ' +
        (s.intro || '') + ' ' +
        (s.chips || []).join(' ')
      ).toLowerCase();
      return haystack.includes(term);
    });

    const totalMatches = matchedServices.length + (meetingMatch ? 1 : 0);

    let html = '';

    // نوار تعداد نتایج
    html += '<div style="display:flex; align-items:center; justify-content:space-between; padding:4px 4px 6px;">' +
      '<span style="font-size:12.5px; font-weight:800; color:var(--teal);">' +
        (isEn ? totalMatches + ' Services Found' : svcPersianDigits(totalMatches) + ' خدمت مرتبط یافت شد') +
      '</span>' +
      '<button type="button" onclick="clearMainServicesSearch()" style="background:transparent; border:none; font-size:11.5px; color:var(--text-muted); cursor:pointer; font-weight:600;">' +
        (isEn ? 'Clear Filter ✕' : 'پاک کردن فیلتر ✕') +
      '</button>' +
    '</div>';

    // اگر کارت دیدار حضوری تطابق داشت
    if (meetingMatch) {
      const meetingTitle = isEn
        ? 'Request in-person meeting with City Council & Mayor'
        : 'درخواست دیدار حضوری با اعضای شورای شهر و شهردار محترم';
      const meetingBadge = isEn ? 'Face-to-Face Meeting' : 'دیدار چهره‌به‌چهره';
      const meetingTag = isEn ? 'Direct Municipal Access' : 'ارتباط مستقیم با مدیریت شهری';
      const meetingDesc = isEn
        ? 'Book in-person appointment, direct public audience with Mayor and City Council members.'
        : 'ثبت نوبت ملاقات عمومی، پیگیری مستقیم مطالبات شهری و طرح چهره‌به‌چهره موضوعات با مدیریت ارشد شهرداری و اعضای شورا';

      html += '<div class="svc-vip-meeting-card" onclick="openMayorMeetingService()" style="margin:0;">' +
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
          '<span class="svc-vip-action">' + (isEn ? 'Book Appointment' : 'رزرو وقت و ثبت درخواست دیدار') + '</span>' +
          '<span class="svc-vip-arrow">' + (isEn ? '→' : '←') + '</span>' +
        '</div>' +
      '</div>';
    }

    if (matchedServices.length > 0) {
      matchedServices.forEach(function (s) {
        html += serviceCardHtml(s.id);
      });
    }

    if (totalMatches === 0) {
      html += '<div class="glass-card" style="padding:28px 20px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:8px;">' +
        '<div style="font-size:32px;">🔍</div>' +
        '<h4 style="font-size:14px; font-weight:800; color:var(--text-primary); margin:0;">' +
          (isEn ? 'No services found' : 'خدمتی با این مشخصات یافت نشد') +
        '</h4>' +
        '<p style="font-size:12px; color:var(--text-muted); line-height:1.7; margin:0;">' +
          (isEn
            ? 'Try searching with keywords like taxes, renovation, business, permits, or in-person meeting.'
            : 'می‌توانید کلماتی مانند عوارض، نوسازی، پسماند، کسب و کار، دیدار حضوری یا ترافیک را جستجو فرمایید.') +
        '</p>' +
      '</div>';
    }

    resultsWrap.innerHTML = html;
  }

  function clearMainServicesSearch() {
    const input = document.getElementById('mainServicesSearchInput');
    if (input) {
      input.value = '';
      input.focus();
    }
    handleMainServicesSearch('');
  }

  function quickFilterServices(tag) {
    const input = document.getElementById('mainServicesSearchInput');
    if (input) {
      input.value = tag;
    }
    handleMainServicesSearch(tag);
  }

  function selectMeetingTarget(targetVal, btnElem) {
    const sel = document.getElementById('meetingTargetSelect');
    if (sel) {
      sel.value = targetVal;
    }
    document.querySelectorAll('.meeting-target-chip').forEach(function (c) {
      c.classList.remove('active');
    });
    if (btnElem) {
      btnElem.classList.add('active');
    }
  }

  function syncMeetingTargetChips(selectedVal) {
    document.querySelectorAll('.meeting-target-chip').forEach(function (c) {
      const text = c.textContent || '';
      if (text.includes(selectedVal) || selectedVal.includes(text.replace(/[🏛️👥🤝🏢]/g, '').trim())) {
        c.classList.add('active');
      } else {
        c.classList.remove('active');
      }
    });
  }
'''

for sp in services_files:
    with open(sp, 'r', encoding='utf-8') as f:
        c = f.read()

    # Replace renderServices()
    # Find start and end of renderServices
    start_tag = '  function renderServices() {'
    end_tag = '    wrap.innerHTML = html;\n  }'
    s_idx = c.find(start_tag)
    e_idx = c.find(end_tag, s_idx)
    if s_idx != -1 and e_idx != -1:
        e_idx += len(end_tag)
        c = c[:s_idx] + new_render_services + c[e_idx:]
        print(f"Replaced renderServices in {sp}")
    else:
        print(f"Could not locate renderServices in {sp}")

    # Add search functions if not present
    if 'function handleMainServicesSearch' not in c:
        export_marker = '  window.openMayorMeetingService = openMayorMeetingService;'
        if export_marker in c:
            c = c.replace(export_marker, search_functions + '\n' + export_marker)
            print(f"Added search functions to {sp}")
        else:
            print(f"export_marker not found in {sp}")

    # Ensure windows exports
    window_exports = '''  window.handleMainServicesSearch = handleMainServicesSearch;
  window.clearMainServicesSearch = clearMainServicesSearch;
  window.quickFilterServices = quickFilterServices;
  window.selectMeetingTarget = selectMeetingTarget;
  window.syncMeetingTargetChips = syncMeetingTargetChips;'''

    if 'window.handleMainServicesSearch = handleMainServicesSearch;' not in c:
        last_export = '  window.submitMayorMeetingRequest = submitMayorMeetingRequest;'
        if last_export in c:
            c = c.replace(last_export, last_export + '\n' + window_exports)
            print(f"Added window exports to {sp}")

    with open(sp, 'w', encoding='utf-8') as f:
        f.write(c)

print("Services files updated successfully.")
