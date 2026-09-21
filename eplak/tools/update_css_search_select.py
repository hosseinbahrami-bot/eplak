#!/usr/bin/env python3
import sys

css_files = [
    '/home/user/eplak/eplak-fixed/assets/css/style.css',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/assets/css/style.css',
    '/home/user/eplak/ios-app/Eplak/Web/assets/css/style.css'
]

new_css = '''
  /* =========================================================
     استایل‌های منوی کشویی (Select & Option) در حالت شب و روز
     ========================================================= */
  select, select.input-field, select.select-field {
    width: 100%;
    background-color: #0d2238 !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 14px;
    padding: 12px 14px;
    font-family: inherit;
    font-size: 13px;
    cursor: pointer;
    outline: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2300c9a7' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: left 14px center !important;
    background-size: 16px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  body.lang-en select, html[dir="ltr"] select {
    background-position: right 14px center !important;
  }
  select:focus, select.input-field:focus, select.select-field:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(0, 201, 167, 0.25) !important;
  }
  select option, option {
    background-color: #0c1c2e !important;
    color: #ffffff !important;
    padding: 12px 14px !important;
    font-size: 13.5px !important;
    font-family: inherit !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
  select option:hover, select option:focus, select option:checked {
    background-color: #00c9a7 !important;
    color: #04141f !important;
    font-weight: 700;
  }
  html.day select, html.day select.input-field, html.day select.select-field {
    background-color: #ffffff !important;
    color: #0a2a22 !important;
    border-color: rgba(0, 150, 130, 0.25) !important;
    box-shadow: 0 2px 8px rgba(0, 150, 130, 0.08);
  }
  html.day select option, html.day option {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  }
  html.day select option:hover, html.day select option:focus, html.day select option:checked {
    background-color: #00c9a7 !important;
    color: #ffffff !important;
    font-weight: 700;
  }

  /* کارت‌های انتخابی طرف ملاقات (Target Chips) */
  .meeting-target-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 8px;
  }
  .meeting-target-chip {
    background: rgba(255, 255, 255, 0.06);
    border: 1.5px solid rgba(255, 255, 255, 0.14);
    border-radius: 13px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 12px;
    font-weight: 700;
    color: #ffffff;
    text-align: right;
  }
  body.lang-en .meeting-target-chip, html[dir="ltr"] .meeting-target-chip {
    text-align: left;
  }
  .meeting-target-chip:hover {
    border-color: rgba(0, 201, 167, 0.5);
    background: rgba(0, 201, 167, 0.1);
  }
  .meeting-target-chip.active {
    border-color: var(--teal) !important;
    background: rgba(0, 201, 167, 0.2) !important;
    color: var(--teal) !important;
    box-shadow: 0 4px 14px rgba(0, 201, 167, 0.28);
  }
  .meeting-target-chip .chip-icon {
    font-size: 16px;
    flex-shrink: 0;
  }
  html.day .meeting-target-chip {
    background: rgba(0, 150, 130, 0.07);
    border-color: rgba(0, 150, 130, 0.2);
    color: #0a2a22;
  }
  html.day .meeting-target-chip.active {
    border-color: var(--teal) !important;
    background: rgba(0, 201, 167, 0.22) !important;
    color: #008f75 !important;
  }

  /* =========================================================
     کادر مدرن و شیک جستجوی خدمات شهری (Services Smart Search)
     ========================================================= */
  .svc-search-container {
    margin: 0 16px 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .svc-search-box {
    position: relative;
    display: flex;
    align-items: center;
    background: var(--card-bg);
    border: 1.5px solid var(--card-border);
    border-radius: 18px;
    padding: 4px 12px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 6px 22px -4px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.15);
    transition: all 0.24s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .svc-search-box:focus-within {
    border-color: var(--teal);
    box-shadow: 0 8px 28px -4px rgba(0, 201, 167, 0.35), 0 0 0 3px rgba(0, 201, 167, 0.18);
    transform: translateY(-1px);
  }
  .svc-search-icon-box {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: rgba(0, 201, 167, 0.14);
    border: 1px solid rgba(0, 201, 167, 0.28);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--teal);
    flex-shrink: 0;
    margin-left: 10px;
    transition: all 0.2s ease;
  }
  body.lang-en .svc-search-icon-box, html[dir="ltr"] .svc-search-icon-box {
    margin-left: 0;
    margin-right: 10px;
  }
  .svc-search-box:focus-within .svc-search-icon-box {
    background: var(--teal);
    color: #051824;
    box-shadow: 0 4px 12px rgba(0, 201, 167, 0.4);
  }
  .svc-search-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    padding: 10px 0;
    text-align: right;
    direction: rtl;
  }
  body.lang-en .svc-search-input, html[dir="ltr"] .svc-search-input {
    text-align: left;
    direction: ltr;
  }
  .svc-search-input::placeholder {
    color: var(--text-muted);
    font-size: 12.5px;
    font-weight: 500;
  }
  .svc-search-clear {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    outline: none;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.2s ease;
  }
  .svc-search-clear:hover {
    background: rgba(255, 77, 77, 0.2);
    color: #ff4d4d;
  }
  .svc-quick-tags {
    display: flex;
    align-items: center;
    gap: 6px;
    overflow-x: auto;
    padding: 2px 2px 4px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }
  .svc-quick-tags::-webkit-scrollbar {
    display: none;
  }
  .svc-quick-tag {
    white-space: nowrap;
    padding: 5px 11px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.09);
    color: var(--text-light);
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }
  .svc-quick-tag:hover {
    background: rgba(0, 201, 167, 0.12);
    border-color: rgba(0, 201, 167, 0.35);
    color: var(--teal);
    transform: translateY(-1px);
  }
  .svc-quick-tag.active {
    background: var(--teal);
    border-color: var(--teal);
    color: #051824;
    font-weight: 800;
    box-shadow: 0 4px 12px rgba(0, 201, 167, 0.35);
  }
  html.day .svc-quick-tag {
    background: rgba(0, 150, 130, 0.08);
    border-color: rgba(0, 150, 130, 0.15);
    color: #0a2a22;
  }
  html.day .svc-quick-tag.active {
    background: var(--teal);
    color: #ffffff;
  }
'''

for cp in css_files:
    with open(cp, 'r', encoding='utf-8') as f:
        c = f.read()
    if '.svc-search-container' not in c:
        c += '\n' + new_css
        with open(cp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated CSS with search & select styles: {cp}")
    else:
        print(f"Already updated: {cp}")

print("CSS updates completed.")
