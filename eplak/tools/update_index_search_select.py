#!/usr/bin/env python3
import re

files_index = [
    '/home/user/eplak/eplak-fixed/index.html',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/index.html',
    '/home/user/eplak/ios-app/Eplak/Web/index.html'
]

# Replacement for target selection in screen-mayor-meeting
old_target_block = '''      <!-- طرف ملاقات -->
      <div>
        <label for="meetingTargetSelect" style="display:block; font-size:12.5px; font-weight:700; color:var(--text-primary); margin-bottom:6px; text-align:right;">طرف ملاقات مدنظر شما *</label>
        <select id="meetingTargetSelect" class="input-field" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:var(--card-bg); color:var(--text-primary); border:1px solid var(--card-border); border-radius:14px;">
          <option value="شهردار محترم ورامین">شهردار محترم ورامین</option>
          <option value="ریاست و اعضای محترم شورای اسلامی شهر">ریاست و اعضای محترم شورای اسلامی شهر</option>
          <option value="دیدار مشترک (شهردار و اعضای شورا)">دیدار مشترک (شهردار و اعضای شورا)</option>
          <option value="معاونت‌های تخصصی شهرداری ورامین">معاونت‌های تخصصی شهرداری ورامین</option>
        </select>
      </div>'''

new_target_block = '''      <!-- طرف ملاقات -->
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

# Replacement for cancel buttons
old_cancel_mayor = '<button type="button" class="btn-secondary" onclick="goBack()" style="padding:12px; font-size:13px;">انصراف و بازگشت به خدمات</button>'
new_cancel_home = '''<button type="button" class="btn-secondary" onclick="showScreen('screen-home')" style="padding:12px; font-size:13.5px; font-weight:700; display:flex; align-items:center; justify-content:center; gap:8px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><path d="M3 10.5L12 3l9 7.5V20a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>
          <span>انصراف و بازگشت به خانه</span>
        </button>'''

old_cancel_ticket = '<button type="button" class="btn-secondary" onclick="goBack()" style="padding:12px; font-size:13px;">انصراف و بازگشت</button>'

# Department select in ticket-new with high-contrast options
old_dept_select = '''        <select id="ticketDeptSelect" class="input-field" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:var(--card-bg); color:var(--text-primary); border:1px solid var(--card-border); border-radius:14px;">
          <option value="حوزه شهردار و روابط عمومی">حوزه شهردار و روابط عمومی</option>
          <option value="بازرسی و ارزیابی عملکرد">بازرسی و ارزیابی عملکرد و شکایات</option>
          <option value="معاونت خدمات شهری">معاونت خدمات شهری (نظافت، پسماند، فضای سبز)</option>
          <option value="معاونت فنی و عمرانی">معاونت فنی و عمرانی (معابر، آسفالت، زیرساخت)</option>
          <option value="معاونت شهرسازی و معماری">معاونت شهرسازی (پروانه، ساخت‌وساز، املاک)</option>
          <option value="معاونت اداری و مالی">معاونت اداری و مالی (عوارض، درآمد، حسابداری)</option>
          <option value="معاونت حمل‌ونقل و ترافیک">معاونت حمل‌ونقل و ترافیک</option>
          <option value="سازمان آتش‌نشانی و ایمنی">سازمان آتش‌نشانی و ایمنی</option>
          <option value="فناوری اطلاعات و شهر هوشمند">فناوری اطلاعات و شهر هوشمند</option>
          <option value="پشتیبانی عمومی">پشتیبانی عمومی و پیگیری اداری</option>
        </select>'''

new_dept_select = '''        <select id="ticketDeptSelect" class="input-field select-field" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:#0d2238; color:#ffffff; border:1.5px solid rgba(255,255,255,0.2); border-radius:14px;">
          <option value="حوزه شهردار و روابط عمومی" style="background-color:#0c1c2e; color:#ffffff;">حوزه شهردار و روابط عمومی</option>
          <option value="بازرسی و ارزیابی عملکرد" style="background-color:#0c1c2e; color:#ffffff;">بازرسی و ارزیابی عملکرد و شکایات</option>
          <option value="معاونت خدمات شهری" style="background-color:#0c1c2e; color:#ffffff;">معاونت خدمات شهری (نظافت، پسماند، فضای سبز)</option>
          <option value="معاونت فنی و عمرانی" style="background-color:#0c1c2e; color:#ffffff;">معاونت فنی و عمرانی (معابر، آسفالت، زیرساخت)</option>
          <option value="معاونت شهرسازی و معماری" style="background-color:#0c1c2e; color:#ffffff;">معاونت شهرسازی (پروانه، ساخت‌وساز، املاک)</option>
          <option value="معاونت اداری و مالی" style="background-color:#0c1c2e; color:#ffffff;">معاونت اداری و مالی (عوارض، درآمد، حسابداری)</option>
          <option value="معاونت حمل‌ونقل و ترافیک" style="background-color:#0c1c2e; color:#ffffff;">معاونت حمل‌ونقل و ترافیک</option>
          <option value="سازمان آتش‌نشانی و ایمنی" style="background-color:#0c1c2e; color:#ffffff;">سازمان آتش‌نشانی و ایمنی</option>
          <option value="فناوری اطلاعات و شهر هوشمند" style="background-color:#0c1c2e; color:#ffffff;">فناوری اطلاعات و شهر هوشمند</option>
          <option value="پشتیبانی عمومی" style="background-color:#0c1c2e; color:#ffffff;">پشتیبانی عمومی و پیگیری اداری</option>
        </select>'''

# Priority select in ticket-new with high-contrast options
old_priority_select = '''        <select id="ticketPrioritySelect" class="input-field" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:var(--card-bg); color:var(--text-primary); border:1px solid var(--card-border); border-radius:14px;">
          <option value="medium" selected>متوسط (عادی)</option>
          <option value="low">پایین (پیشنهاد / نظر)</option>
          <option value="high">بالا (نیازمند رسیدگی سریع)</option>
          <option value="critical">بحرانی و فوری (خطر یا حادثه شهری)</option>
        </select>'''

new_priority_select = '''        <select id="ticketPrioritySelect" class="input-field select-field" style="width:100%; font-size:13px; text-align:right; direction:rtl; padding:12px; background:#0d2238; color:#ffffff; border:1.5px solid rgba(255,255,255,0.2); border-radius:14px;">
          <option value="medium" selected style="background-color:#0c1c2e; color:#ffffff;">متوسط (عادی)</option>
          <option value="low" style="background-color:#0c1c2e; color:#ffffff;">پایین (پیشنهاد / نظر)</option>
          <option value="high" style="background-color:#0c1c2e; color:#ffffff;">بالا (نیازمند رسیدگی سریع)</option>
          <option value="critical" style="background-color:#0c1c2e; color:#ffffff;">بحرانی و فوری (خطر یا حادثه شهری)</option>
        </select>'''

for fp in files_index:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    if old_target_block in c:
        c = c.replace(old_target_block, new_target_block)
        print(f"Updated meeting target select in {fp}")
    else:
        print(f"old_target_block not matched in {fp}")

    if old_cancel_mayor in c:
        c = c.replace(old_cancel_mayor, new_cancel_home)
        print(f"Updated cancel button in screen-mayor-meeting in {fp}")
    else:
        print(f"old_cancel_mayor not matched in {fp}")

    if old_dept_select in c:
        c = c.replace(old_dept_select, new_dept_select)
        print(f"Updated dept select in {fp}")
    else:
        print(f"old_dept_select not matched in {fp}")

    if old_priority_select in c:
        c = c.replace(old_priority_select, new_priority_select)
        print(f"Updated priority select in {fp}")
    else:
        print(f"old_priority_select not matched in {fp}")

    if old_cancel_ticket in c:
        c = c.replace(old_cancel_ticket, new_cancel_home)
        print(f"Updated cancel button in ticket-new in {fp}")
    else:
        print(f"old_cancel_ticket not matched in {fp}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

print("Index files update completed.")
