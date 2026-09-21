#!/usr/bin/env python3
import sys
import re

css_files = [
    '/home/user/eplak/eplak-fixed/assets/css/style.css',
    '/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/assets/css/style.css',
    '/home/user/eplak/ios-app/Eplak/Web/assets/css/style.css'
]

btn_secondary_and_cat_search_css = '''
  /* =========================================================
     دکمه ثانویه / انصراف و بازگشت (هماهنگ با سبک کارتی و رنگ‌های اپلیکیشن)
     ========================================================= */
  .btn-secondary {
    background: var(--card-bg, rgba(255, 255, 255, 0.07));
    border: 1.5px solid var(--card-border, rgba(255, 255, 255, 0.16));
    border-radius: var(--radius-btn, 14px);
    color: var(--text-primary, #ffffff);
    font-family: 'Vazirmatn', sans-serif;
    font-size: 13.5px;
    font-weight: 700;
    padding: 13px 20px;
    cursor: pointer;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18), inset 0 1px 1px rgba(255, 255, 255, 0.12);
    transition: all 0.24s cubic-bezier(0.34, 1.56, 0.64, 1);
    -webkit-tap-highlight-color: transparent;
  }
  .btn-secondary svg {
    color: var(--teal, #00c9a7);
    transition: transform 0.2s ease;
  }
  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(0, 201, 167, 0.55);
    color: var(--teal, #00c9a7);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25), 0 0 14px rgba(0, 201, 167, 0.25);
  }
  .btn-secondary:active {
    transform: scale(0.97);
  }
  html.day .btn-secondary {
    background: rgba(255, 255, 255, 0.9);
    border: 1.5px solid rgba(0, 150, 130, 0.28);
    color: #0a2a22;
    box-shadow: 0 2px 10px rgba(0, 150, 130, 0.1);
  }
  html.day .btn-secondary:hover {
    background: #ffffff;
    border-color: var(--teal);
    color: #008f75;
  }

  /* =========================================================
     کادر لوکس و مدرن جستجو درون دسته‌بندی‌های ۶ گانه (Category Search Box)
     ========================================================= */
  .cat-search-container {
    margin: 0 16px 12px;
    position: relative;
    display: flex;
    align-items: center;
    background: var(--card-bg);
    border: 1.5px solid var(--card-border);
    border-radius: 18px;
    padding: 4px 12px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 6px 22px -4px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.14);
    transition: all 0.24s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .cat-search-container:focus-within {
    border-color: var(--cat-accent, var(--teal));
    box-shadow: 0 8px 28px -4px rgba(var(--cat-accent-rgb, 0, 201, 167), 0.35), 0 0 0 3px rgba(var(--cat-accent-rgb, 0, 201, 167), 0.18);
    transform: translateY(-1px);
  }
  .cat-search-icon-box {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: rgba(var(--cat-accent-rgb, 0, 201, 167), 0.14);
    border: 1px solid rgba(var(--cat-accent-rgb, 0, 201, 167), 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--cat-accent, var(--teal));
    flex-shrink: 0;
    margin-left: 10px;
    transition: all 0.22s ease;
  }
  body.lang-en .cat-search-icon-box, html[dir="ltr"] .cat-search-icon-box {
    margin-left: 0;
    margin-right: 10px;
  }
  .cat-search-container:focus-within .cat-search-icon-box {
    background: var(--cat-accent, var(--teal));
    color: #051824;
    box-shadow: 0 4px 12px rgba(var(--cat-accent-rgb, 0, 201, 167), 0.4);
  }
  .cat-search-input {
    flex: 1;
    background: transparent !important;
    border: none !important;
    outline: none !important;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary) !important;
    padding: 10px 0 !important;
    text-align: right;
    direction: rtl;
    box-shadow: none !important;
  }
  body.lang-en .cat-search-input, html[dir="ltr"] .cat-search-input {
    text-align: left;
    direction: ltr;
  }
  .cat-search-input::placeholder {
    color: var(--text-muted);
    font-size: 12.5px;
    font-weight: 500;
  }
  .cat-search-clear {
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
  .cat-search-clear:hover {
    background: rgba(255, 77, 77, 0.2);
    color: #ff4d4d;
  }
  html.day .cat-search-container {
    background: rgba(255, 255, 255, 0.85);
    border-color: rgba(0, 150, 130, 0.2);
    box-shadow: 0 2px 12px rgba(0, 150, 130, 0.08);
  }
  html.day .cat-search-input {
    color: #0a2a22 !important;
  }
'''

for cp in css_files:
    with open(cp, 'r', encoding='utf-8') as f:
        c = f.read()
    if '.cat-search-container' not in c:
        c += '\n' + btn_secondary_and_cat_search_css
        with open(cp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Added btn-secondary and cat-search-container to {cp}")
    else:
        print(f"Already in {cp}")

print("CSS updated.")
