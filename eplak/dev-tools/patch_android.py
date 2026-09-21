#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""همسان‌سازی بخش «خدمات» با نسخه وب‌ویوی اندروید"""
import io, re, shutil, os

AND = "/home/user/eplak-fixed/android-app/app/src/main/assets"
IDX = os.path.join(AND, "index.html")
CSS = os.path.join(AND, "assets/css/style.css")

# 1) کپی ماژول جدید
shutil.copy("/home/user/eplak-fixed/modules/services.js", os.path.join(AND, "modules/services.js"))
print("services.js copied to android assets")

html = io.open(IDX, encoding="utf-8").read()
n0 = len(html)

NAV_SERVICES = """      <button class="nav-item" onclick="showScreen('screen-services')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5l1.9 4.9 4.9 1.9-4.9 1.9L12 16.1l-1.9-4.9L5.2 9.3l4.9-1.9z"/><path d="M18.5 15l.8 2.1 2.1.8-2.1.8-.8 2.1-.8-2.1-2.1-.8 2.1-.8z"/><path d="M5.5 14l.6 1.5 1.5.6-1.5.6-.6 1.5-.6-1.5L3.4 16.1l1.5-.6z"/></svg>
        خدمات
      </button>
"""

# 2) آیتم منو بعد از «پیشخوان»
pattern = re.compile(
    r'(<button class="nav-item[^>]*>\s*\n\s*<svg[^>]*>.*?</svg>\s*\n\s*پیشخوان\s*\n\s*</button>\n)',
    re.DOTALL)
html, n_nav = pattern.subn(lambda m: m.group(1) + NAV_SERVICES, html)
print("nav items added:", n_nav)

# 3) کارت‌های خانه و داشبورد
home_old = """        <div class="service-card" onclick="showScreen('screen-payment')">
          <div class="service-icon" style="background:rgba(150,80,255,0.12);">💳</div>
          <div>
            <h3>پرداخت عوارض</h3>
            <p>عوارض و قبوض</p>
          </div>
        </div>
"""
home_new = """        <div class="service-card" onclick="showScreen('screen-services')">
          <div class="service-icon" style="background:linear-gradient(135deg,rgba(0,201,167,0.22),rgba(124,58,237,0.22));">✨</div>
          <div>
            <h3>خدمات</h3>
            <p>سرویس‌های شهری</p>
          </div>
        </div>
"""
dash_old = """        <div class="service-card" onclick="showScreen('screen-payment')">
          <div class="service-icon" style="background:rgba(150,80,255,0.12);">💳</div>
          <div><h3>پرداخت عوارض</h3><p>عوارض و قبوض</p></div>
        </div>
"""
dash_new = """        <div class="service-card" onclick="showScreen('screen-services')">
          <div class="service-icon" style="background:linear-gradient(135deg,rgba(0,201,167,0.22),rgba(124,58,237,0.22));">✨</div>
          <div><h3>خدمات</h3><p>سرویس‌های شهری</p></div>
        </div>
"""
c = 0
if home_old in html:
    html = html.replace(home_old, home_new, 1); c += 1
if dash_old in html:
    html = html.replace(dash_old, dash_new, 1); c += 1
print("grid cards replaced:", c)

# 4) صفحات جدید (همان محتوای نسخه وب)
web = io.open("/home/user/eplak-fixed/index.html", encoding="utf-8").read()
start = web.index('  <!-- ============ SCREEN: SERVICES (خدمات) ============ -->')
end = web.index('  <!-- ============ SCREEN: CITY MAP ============ -->')
SCREENS = web[start:end]

anchor = "  <!-- ============ SCREEN: CITY MAP ============ -->"
assert anchor in html
html = html.replace(anchor, SCREENS + anchor, 1)
print("screens inserted")

# 5) تگ اسکریپت
sa = '<script src="modules/profile.js"></script>'
assert sa in html
html = html.replace(sa, sa + '\n<script src="modules/services.js"></script>', 1)
print("script tag added")

io.open(IDX, "w", encoding="utf-8").write(html)
print("index.html: %d -> %d bytes" % (n0, len(html)))

# 6) الحاق بلوک CSS جدید (فقط بخش خدمات) به استایل اندروید
webcss = io.open("/home/user/eplak-fixed/assets/css/style.css", encoding="utf-8").read()
marker = "  /* =========================================================\n     ===== SECTION: SERVICES (خدمات) — premium cards ====="
block = webcss[webcss.index(marker):]

css = io.open(CSS, encoding="utf-8").read()
if "SECTION: SERVICES" in css:
    print("css block already present — skipped")
else:
    io.open(CSS, "w", encoding="utf-8").write(css.rstrip() + "\n\n" + block.rstrip() + "\n")
    print("css block appended (%d chars)" % len(block))
