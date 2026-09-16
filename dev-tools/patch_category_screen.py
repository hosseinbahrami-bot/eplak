#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""افزودن صفحه اختصاصی هر بخش خدمات (وب + اندروید)"""
import io

SCREEN = """
  <!-- ============ SCREEN: SERVICE CATEGORY (صفحه هر بخش خدمات) ============ -->
  <div class="screen" id="screen-service-category">
    <div class="bg-city" style="background:linear-gradient(180deg,var(--bg-grad1) 0%,var(--bg-grad2) 100%);">
      <div class="bg-orb orb-1" style="opacity:0.3;"></div>
      <div class="bg-orb orb-3" style="opacity:0.4;"></div>
    </div>
    <div style="background:var(--bg-screen); position:absolute; inset:0; z-index:2;"></div>

    <div class="top-header" style="position:relative;z-index:20;">
      <button class="notif-btn" onclick="showScreen('screen-services')">→</button>
      <div style="font-size:16px; font-weight:800;">بخش خدمات</div>
      <div style="width:40px;"></div>
    </div>

    <div class="screen-content" style="position:relative;z-index:10; gap:14px; padding:0 0 20px;">
      <div id="serviceCategoryWrap" style="display:flex; flex-direction:column; gap:14px;"></div>
      <div class="bottom-pad"></div>
    </div>
  </div>

"""

ANCHOR = "  <!-- ============ SCREEN: CITY MAP ============ -->"

for path in ["/home/user/eplak-fixed/index.html",
             "/home/user/eplak-fixed/android-app/app/src/main/assets/index.html"]:
    html = io.open(path, encoding="utf-8").read()
    if 'id="screen-service-category"' in html:
        print("already present:", path)
        continue
    assert ANCHOR in html, path
    html = html.replace(ANCHOR, SCREEN + ANCHOR, 1)
    io.open(path, "w", encoding="utf-8").write(html)
    print("inserted into:", path)
