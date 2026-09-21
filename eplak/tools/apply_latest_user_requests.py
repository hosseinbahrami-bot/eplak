#!/usr/bin/env python3
import sys

# 1. Update index.html across root, Android, iOS
index_files = [
    '/home/user/eplak/eplak-fixed/index.html',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/index.html',
    '/home/user/eplak/ios-app/Eplak/Web/index.html'
]

# We need to remove the 4 target chips from screen-mayor-meeting
target_with_chips = '''      <!-- طرف ملاقات -->
      <div>
        <label for="meetingTargetSelect" style="display:block; font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">طرف ملاقات مدنظر شما *</label>
        
        <!-- کارت‌های انتخاب سریع و پرکنتراست در حالت شب و روز -->
        <div class="meeting-target-grid">
          <button type="button" class="meeting-target-chip active" onclick="selectMeetingTarget('شهردار محترم ورامین', this)">
            <span class="chip-icon">🏛️</span>
            <span>شهردار محترم ورامین</span>
          </button>
          <button type="button" class="meeting-target-chip" onclick="selectMeetingTarget('ریاست و اعضای محترم شورای اسلامی شهر', this)">
            <span class="chip-icon">👥</span>
            <span>اعضای محترم شورای شهر</span>
          </button>
          <button type="button" class="meeting-target-chip" onclick="selectMeetingTarget('دیدار مشترک (شهردار و اعضای شورا)', this)">
            <span class="chip-icon">🤝</span>
            <span>دیدار مشترک شهردار و شورا</span>
          </button>
          <button type="button" class="meeting-target-chip" onclick="selectMeetingTarget('معاونت‌های تخصصی شهرداری ورامین', this)">
            <span class="chip-icon">🏢</span>
            <span>معاونت‌های تخصصی شهرداری</span>
          </button>
        </div>

        <select id="meetingTargetSelect" class="input-field select-field" onchange="syncMeetingTargetChips(this.value)" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:#0d2238; color:#ffffff; border:1.5px solid rgba(255,255,255,0.2); border-radius:14px;">
          <option value="شهردار محترم ورامین" style="background-color:#0c1c2e; color:#ffffff;">شهردار محترم ورامین</option>
          <option value="ریاست و اعضای محترم شورای اسلامی شهر" style="background-color:#0c1c2e; color:#ffffff;">ریاست و اعضای محترم شورای اسلامی شهر</option>
          <option value="دیدار مشترک (شهردار و اعضای شورا)" style="background-color:#0c1c2e; color:#ffffff;">دیدار مشترک (شهردار و اعضای شورا)</option>
          <option value="معاونت‌های تخصصی شهرداری ورامین" style="background-color:#0c1c2e; color:#ffffff;">معاونت‌های تخصصی شهرداری ورامین</option>
        </select>
      </div>'''

clean_target = '''      <!-- طرف ملاقات -->
      <div>
        <label for="meetingTargetSelect" style="display:block; font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">طرف ملاقات مدنظر شما *</label>
        <select id="meetingTargetSelect" class="input-field select-field" style="width:100%; font-size:13.5px; text-align:right; direction:rtl; padding:13px 14px; background:#0d2238; color:#ffffff; border:1.5px solid rgba(255,255,255,0.2); border-radius:14px;">
          <option value="شهردار محترم ورامین" style="background-color:#0c1c2e; color:#ffffff;">شهردار محترم ورامین</option>
          <option value="ریاست و اعضای محترم شورای اسلامی شهر" style="background-color:#0c1c2e; color:#ffffff;">ریاست و اعضای محترم شورای اسلامی شهر</option>
          <option value="دیدار مشترک (شهردار و اعضای شورا)" style="background-color:#0c1c2e; color:#ffffff;">دیدار مشترک (شهردار و اعضای شورا)</option>
          <option value="معاونت‌های تخصصی شهرداری ورامین" style="background-color:#0c1c2e; color:#ffffff;">معاونت‌های تخصصی شهرداری ورامین</option>
        </select>
      </div>'''

for fp in index_files:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    if target_with_chips in c:
        c = c.replace(target_with_chips, clean_target)
        print(f"Removed 4 meeting chips from {fp}")
    else:
        print(f"Warning: target_with_chips not found in {fp}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

# 2. Update modules/services.js across root, Android, iOS
services_files = [
    '/home/user/eplak/eplak-fixed/modules/services.js',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/modules/services.js',
    '/home/user/eplak/ios-app/Eplak/Web/modules/services.js'
]

old_cat_search_block = '''    // فیلتر جستجوی درون بخشی
    html += '<div style="padding:0 16px 4px;">' +
      '<div class="search-box" style="margin:0;">' +
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>' +
        '<input type="text" id="catSearchInput" placeholder="' + (isEn ? 'Search inside this category...' : 'جستجو در خدمات این بخش...') + '" oninput="filterCategoryServices(this.value, \\'' + group.id + '\\')">' +
      '</div>' +
    '</div>';'''

new_cat_search_block = '''    // فیلتر مدرن، لوکس و شکیل جستجوی درون بخشی
    const catSearchPlaceholder = isEn
      ? 'Search in ' + group.title + '...'
      : 'جستجو در خدمات ' + group.title + '...';

    html += '<div class="cat-search-container" style="--cat-accent:' + group.accentColor + '; --cat-accent-rgb:' + group.accent + ';">' +
      '<div class="cat-search-icon-box">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>' +
      '</div>' +
      '<input type="text" id="catSearchInput" class="cat-search-input" placeholder="' + catSearchPlaceholder + '" oninput="filterCategoryServices(this.value, \\'' + group.id + '\\')" autocomplete="off">' +
      '<button type="button" id="catSearchClear" class="cat-search-clear" onclick="clearCatSearch(\\'' + group.id + '\\')" style="display:none;" aria-label="' + (isEn ? 'Clear' : 'پاک کردن') + '">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' +
      '</button>' +
    '</div>';'''

old_filter_func = '''  function filterCategoryServices(keyword, catId) {
    const listWrap = document.getElementById('catServicesList');
    if (!listWrap) return;
    const groups = getServiceGroups();
    const group = groups.find(function (g) { return g.id === catId; });
    if (!group) return;

    const term = (keyword || '').trim().toLowerCase();
    const filteredIds = group.ids.filter(function (id) {
      if (!term) return true;
      const s = svcById(id);
      if (!s) return false;
      return (s.title + ' ' + s.sub + ' ' + (s.chips || []).join(' ')).toLowerCase().includes(term);
    });

    if (filteredIds.length === 0) {
      listWrap.innerHTML = '<div style="text-align:center; padding:30px 10px; color:var(--text-muted); font-size:13px;">' +
        (isEnglishActive() ? 'No services found matching your search.' : 'سرویسی منطبق با جستجوی شما یافت نشد.') +
      '</div>';
    } else {
      listWrap.innerHTML = filteredIds.map(function (id) { return serviceCardHtml(id); }).join('');
    }
  }'''

new_filter_func = '''  function filterCategoryServices(keyword, catId) {
    const listWrap = document.getElementById('catServicesList');
    if (!listWrap) return;
    const clearBtn = document.getElementById('catSearchClear');
    const groups = getServiceGroups();
    const group = groups.find(function (g) { return g.id === catId; });
    if (!group) return;

    const term = (keyword || '').trim().toLowerCase();
    if (clearBtn) {
      clearBtn.style.display = term ? 'flex' : 'none';
    }

    const filteredIds = group.ids.filter(function (id) {
      if (!term) return true;
      const s = svcById(id);
      if (!s) return false;
      return (
        (s.title || '') + ' ' +
        (s.sub || '') + ' ' +
        (s.chips || []).join(' ') + ' ' +
        (s.intro || '')
      ).toLowerCase().includes(term);
    });

    if (filteredIds.length === 0) {
      listWrap.innerHTML = '<div class="glass-card" style="text-align:center; padding:28px 20px; margin:0 4px; display:flex; flex-direction:column; align-items:center; gap:8px;">' +
        '<div style="font-size:28px;">🔍</div>' +
        '<h4 style="font-size:14px; font-weight:800; color:var(--text-primary); margin:0;">' +
          (isEnglishActive() ? 'No services found in ' + group.title : 'خدمتی در بخش «' + group.title + '» یافت نشد') +
        '</h4>' +
        '<p style="font-size:12px; color:var(--text-muted); line-height:1.7; margin:0;">' +
          (isEnglishActive()
            ? 'Try different keywords or check the main services search.'
            : 'می‌توانید عنوان دیگری را امتحان فرمایید یا از کادر جستجوی صفحه اصلی خدمات استفاده کنید.') +
        '</p>' +
      '</div>';
    } else {
      listWrap.innerHTML = filteredIds.map(function (id) { return serviceCardHtml(id); }).join('');
    }
  }

  function clearCatSearch(catId) {
    const inp = document.getElementById('catSearchInput');
    if (inp) {
      inp.value = '';
      inp.focus();
    }
    filterCategoryServices('', catId);
  }'''

for sp in services_files:
    with open(sp, 'r', encoding='utf-8') as f:
        sc = f.read()

    if old_cat_search_block in sc:
        sc = sc.replace(old_cat_search_block, new_cat_search_block)
        print(f"Replaced category search block in {sp}")
    else:
        print(f"Warning: old_cat_search_block not found in {sp}")

    if old_filter_func in sc:
        sc = sc.replace(old_filter_func, new_filter_func)
        print(f"Replaced filterCategoryServices in {sp}")
    else:
        print(f"Warning: old_filter_func not found in {sp}")

    if 'window.clearCatSearch = clearCatSearch;' not in sc:
        export_marker = '  window.filterCategoryServices = filterCategoryServices;'
        if export_marker in sc:
            sc = sc.replace(export_marker, export_marker + '\n  window.clearCatSearch = clearCatSearch;')
            print(f"Added window.clearCatSearch to {sp}")

    with open(sp, 'w', encoding='utf-8') as f:
        f.write(sc)

print("Updates applied successfully.")
