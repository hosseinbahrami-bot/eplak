#!/usr/bin/env python3
import re
import sys

files_index = [
    '/home/user/eplak/eplak-fixed/index.html',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/index.html',
    '/home/user/eplak/ios-app/Eplak/Web/index.html'
]

meeting_screen_html = '''
  <!-- ============ SCREEN: MAYOR & COUNCIL IN-PERSON MEETING (درخواست دیدار حضوری با اعضای شورای شهر و شهردار محترم) ============ -->
  <div class="screen" id="screen-mayor-meeting">
    <div class="bg-city" style="background:linear-gradient(180deg,var(--bg-grad1) 0%,var(--bg-grad2) 100%);">
      <div class="bg-orb orb-1" style="opacity:0.35;"></div>
    </div>
    <div style="background:var(--bg-screen); position:absolute; inset:0; z-index:2;"></div>

    <div class="top-header" style="position:relative;z-index:20;">
      <button class="app-back-btn" onclick="goBack()" aria-label="بازگشت">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
        <span data-i18n="back">بازگشت</span>
      </button>
      <div style="font-size:15px; font-weight:800;" data-i18n="mayor_meeting_header">درخواست دیدار حضوری</div>
      <div class="header-spacer"></div>
    </div>

    <div class="screen-content" style="position:relative;z-index:10; gap:14px; padding:0 16px 20px;">
      
      <!-- معرفی ملاقات مردمی -->
      <div class="glass-card" style="padding:16px; display:flex; align-items:center; gap:12px; background:linear-gradient(135deg, rgba(0,201,167,0.15), rgba(5,150,105,0.06)); border:1.5px solid rgba(0,201,167,0.35);">
        <div style="width:48px; height:48px; border-radius:14px; background:linear-gradient(135deg, #00c9a7, #059669); display:flex; align-items:center; justify-content:center; font-size:24px; flex-shrink:0; box-shadow:0 4px 14px rgba(0,201,167,0.35);">
          🏛️
        </div>
        <div style="text-align:right;">
          <h3 style="font-size:14px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">ملاقات عمومی و چهره‌به‌چهره</h3>
          <p style="font-size:11.5px; color:var(--text-muted); line-height:1.6; margin:0;">جلسات دیدار مستقیم شهردار محترم و اعضای شورای اسلامی شهر ورامین جهت استماع مطالبات و بررسی میدانی مشکلات شهروندان.</p>
        </div>
      </div>

      <!-- طرف ملاقات -->
      <div>
        <label for="meetingTargetSelect" style="display:block; font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">طرف ملاقات مدنظر شما *</label>
        <select id="meetingTargetSelect" class="input-field" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:var(--card-bg); color:var(--text-primary); border:1px solid var(--card-border); border-radius:14px;">
          <option value="شهردار محترم ورامین">شهردار محترم ورامین</option>
          <option value="ریاست و اعضای محترم شورای اسلامی شهر">ریاست و اعضای محترم شورای اسلامی شهر</option>
          <option value="دیدار مشترک (شهردار و اعضای شورا)">دیدار مشترک (شهردار و اعضای شورا)</option>
          <option value="معاونت‌های تخصصی شهرداری ورامین">معاونت‌های تخصصی شهرداری ورامین</option>
        </select>
      </div>

      <!-- مشخصات متقاضی -->
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
        <div>
          <label for="meetingNameInput" style="display:block; font-size:12px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">نام و نام خانوادگی *</label>
          <input type="text" id="meetingNameInput" class="input-field" placeholder="نام متقاضی" style="width:100%; font-size:12.5px; text-align:right; direction:rtl;">
        </div>
        <div>
          <label for="meetingPhoneInput" style="display:block; font-size:12px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">شماره تماس همراه *</label>
          <input type="tel" id="meetingPhoneInput" class="input-field" placeholder="0912..." style="width:100%; font-size:12.5px; text-align:left; direction:ltr;">
        </div>
      </div>

      <!-- موضوع دیدار -->
      <div>
        <label for="meetingSubjectInput" style="display:block; font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">موضوع و عنوان جلسه *</label>
        <input type="text" id="meetingSubjectInput" class="input-field" placeholder="مثلاً: طرح موضوع پرونده نوسازی، پیشنهاد پروژه عمرانی، مطالبات محله..." style="width:100%; font-size:13px; text-align:right; direction:rtl;">
      </div>

      <!-- شرح کامل موضوع -->
      <div>
        <label for="meetingDescInput" style="display:block; font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">شرح جزئیات، سوابق و مدارک مرتبط *</label>
        <textarea id="meetingDescInput" class="text-area" placeholder="لطفاً علت درخواست دیدار حضوری، سوابق پیگیری‌های قبلی و توضیحات تکمیلی را بنویسید..." style="width:100%; height:110px; font-size:13px; text-align:right; direction:rtl; resize:vertical;" maxlength="800"></textarea>
      </div>

      <div style="display:flex; flex-direction:column; gap:10px; margin-top:6px;">
        <button class="btn-teal" onclick="submitMayorMeetingRequest()" style="padding:14px; font-size:13.5px; font-weight:800; display:flex; align-items:center; justify-content:center; gap:8px;">
          <span>ارسال درخواست نوبت دیدار حضوری</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
        <button type="button" class="btn-secondary" onclick="goBack()" style="padding:12px; font-size:13px;">انصراف و بازگشت به خدمات</button>
      </div>

      <div class="bottom-pad"></div>
    </div>
  </div>
'''

def update_index_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Recent Activity block from dashboard
    pattern = re.compile(
        r'\s*<!-- Recent Activity -->\s*<div class="section-row">\s*<span class="section-title"[^>]*data-i18n="dash_recent_activity">.*?</span>\s*<button class="section-link"[^>]*>.*?</button>\s*</div>\s*<div class="reports-list" id="dashActivityWrap"[^>]*></div>',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        content = content[:m.start()] + content[m.end():]
        print(f"Removed Recent Activity from {filepath}")
    else:
        print(f"Pattern for Recent Activity not found in {filepath}")

    # 2. Add screen-mayor-meeting
    if 'id="screen-mayor-meeting"' not in content:
        insert_marker = '<!-- ============ SCREEN: TICKET SUCCESS'
        if insert_marker in content:
            content = content.replace(insert_marker, meeting_screen_html + '\n  ' + insert_marker)
            print(f"Added screen-mayor-meeting to {filepath}")
        else:
            print(f"Insert marker not found in {filepath}")
    else:
        print(f"screen-mayor-meeting already present in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for fp in files_index:
    update_index_file(fp)

print("Done updating index files.")
