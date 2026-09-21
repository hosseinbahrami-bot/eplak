#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""اعمال بخش «خدمات» روی index.html پروژه ای‌پلاک"""
import re, io, sys

PATH = "/home/user/eplak-fixed/index.html"
html = io.open(PATH, encoding="utf-8").read()
orig_len = len(html)

NAV_SERVICES = """      <button class="nav-item" onclick="showScreen('screen-services')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5l1.9 4.9 4.9 1.9-4.9 1.9L12 16.1l-1.9-4.9L5.2 9.3l4.9-1.9z"/><path d="M18.5 15l.8 2.1 2.1.8-2.1.8-.8 2.1-.8-2.1-2.1-.8 2.1-.8z"/><path d="M5.5 14l.6 1.5 1.5.6-1.5.6-.6 1.5-.6-1.5L3.4 16.1l1.5-.6z"/></svg>
        خدمات
      </button>
"""

# ---------------------------------------------------------------- 1. nav item
pattern = re.compile(
    r'(<button class="nav-item[^>]*>\s*\n\s*<svg[^>]*>.*?</svg>\s*\n\s*پیشخوان\s*\n\s*</button>\n)',
    re.DOTALL)

def add_nav(m):
    # در بلوک‌هایی که خودِ پیشخوان فعال است، آیتم خدمات غیرفعال می‌ماند (درست)
    return m.group(1) + NAV_SERVICES

html, n_nav = pattern.subn(add_nav, html)
print("nav items added:", n_nav)

# ------------------------------------------------- 2. home grid: payment -> services
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
assert home_old in html, "home payment card not found"
html = html.replace(home_old, home_new, 1)
print("home grid card replaced")

# --------------------------------------------- 3. dashboard grid: payment -> services
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
assert dash_old in html, "dashboard payment card not found"
html = html.replace(dash_old, dash_new, 1)
print("dashboard grid card replaced")

# ------------------------------------------------------------- 4. new screens
SCREENS = """
  <!-- ============ SCREEN: SERVICES (خدمات) ============ -->
  <div class="screen" id="screen-services">
    <div class="bg-city" style="background:linear-gradient(180deg,var(--bg-grad1) 0%,var(--bg-grad2) 100%);">
      <div class="bg-orb orb-1" style="opacity:0.35;"></div>
      <div class="bg-orb orb-3" style="opacity:0.45;"></div>
    </div>
    <div style="background:var(--bg-screen); position:absolute; inset:0; z-index:2;"></div>

    <div class="top-header" style="position:relative;z-index:20;">
      <button class="notif-btn" onclick="showScreen('screen-notifications')">🔔</button>
      <img src="assets/img/logo.png" alt="ای‌پلاک" class="header-logo-img">
      <div class="theme-toggle">
        <button class="active">☀️</button>
        <button>🌙</button>
      </div>
    </div>

    <div class="screen-content" style="position:relative;z-index:10; gap:14px; padding:0 0 20px;">

      <div class="svc-hero">
        <div class="svc-hero-row">
          <span class="svc-hero-badge"><span class="svc-live-dot"></span>سوپر‌اپلیکیشن خدمات شهری</span>
          <h2>خدمات ای‌پلاک</h2>
          <p>از پرداخت عوارض و بازیافت تا حمل‌ونقل، گردشگری و زندگی شهری هوشمند؛ همه در یک جا.</p>
        </div>
        <div class="svc-hero-emblem">✨</div>
      </div>

      <div id="servicesListWrap" style="display:flex; flex-direction:column; gap:18px;"></div>

      <div class="bottom-pad"></div>
    </div>

    <!-- Nav Bar -->
    <div class="nav-bar">
      <button class="nav-item" onclick="showScreen('screen-home')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>
        خانه
      </button>
      <button class="nav-item" onclick="showScreen('screen-dashboard')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
        پیشخوان
      </button>
      <button class="nav-item active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5l1.9 4.9 4.9 1.9-4.9 1.9L12 16.1l-1.9-4.9L5.2 9.3l4.9-1.9z"/><path d="M18.5 15l.8 2.1 2.1.8-2.1.8-.8 2.1-.8-2.1-2.1-.8 2.1-.8z"/><path d="M5.5 14l.6 1.5 1.5.6-1.5.6-.6 1.5-.6-1.5L3.4 16.1l1.5-.6z"/></svg>
        خدمات
      </button>
      <button class="nav-item" onclick="showScreen('screen-reports')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
        گزارش‌ها
      </button>
      <button class="nav-item" onclick="showScreen('screen-profile')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        پروفایل
      </button>
    </div>
  </div>

  <!-- ============ SCREEN: SERVICE DETAIL (جزئیات هر سرویس) ============ -->
  <div class="screen" id="screen-service-detail">
    <div class="bg-city" style="background:linear-gradient(180deg,var(--bg-grad1) 0%,var(--bg-grad2) 100%);">
      <div class="bg-orb orb-1" style="opacity:0.3;"></div>
    </div>
    <div style="background:var(--bg-screen); position:absolute; inset:0; z-index:2;"></div>

    <div class="top-header" style="position:relative;z-index:20;">
      <button class="notif-btn" onclick="showScreen('screen-services')">→</button>
      <div style="font-size:16px; font-weight:800;">جزئیات سرویس</div>
      <div style="width:40px;"></div>
    </div>

    <div class="screen-content" style="position:relative;z-index:10; gap:14px; padding:0 0 20px;">
      <div id="serviceDetailWrap" style="display:flex; flex-direction:column; gap:14px;"></div>
      <div class="bottom-pad"></div>
    </div>
  </div>

"""

anchor = "  <!-- ============ SCREEN: CITY MAP ============ -->"
assert anchor in html, "city map anchor not found"
html = html.replace(anchor, SCREENS + anchor, 1)
print("new screens inserted")

# --------------------------------------------------------- 5. script tag
script_anchor = '<script src="modules/profile.js"></script>'
assert script_anchor in html
html = html.replace(script_anchor, script_anchor + '\n<script src="modules/services.js"></script>', 1)
print("script tag added")

io.open(PATH, "w", encoding="utf-8").write(html)
print("done: %d -> %d bytes" % (orig_len, len(html)))
