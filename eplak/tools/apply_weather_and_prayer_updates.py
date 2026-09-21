import re

print("--- [1] Removing 'زنده' and time pill from modules/weather-3d.js ---")
weather_path = '/home/user/eplak/eplak-fixed/modules/weather-3d.js'
with open(weather_path, 'r', encoding='utf-8') as f:
    wjs = f.read()

# Remove <div class="apple-time-pill" id="appleTimePill">...</div> from HTML template
wjs = re.sub(
    r'<div class="apple-time-pill"[^>]*>.*?</div>',
    '',
    wjs
)

# Remove timePill element reference and textContent assignment
wjs = re.sub(
    r'var timePill = document\.getElementById\(\'appleTimePill\'\);\s*',
    '',
    wjs
)
wjs = re.sub(
    r'if \(timePill\)\s*\{[^}]*\}\s*',
    '',
    wjs
)

with open(weather_path, 'w', encoding='utf-8') as f:
    f.write(wjs)
print("   -> 'زنده' and time pill removed successfully from weather-3d.js!")


print("\n--- [2] Overhauling Prayer Times (اوقات شرعی) in modules/city-live.js ---")
city_live_path = '/home/user/eplak/eplak-fixed/modules/city-live.js'
with open(city_live_path, 'r', encoding='utf-8') as f:
    cjs = f.read()

# Replace renderPrayer with a truly luxurious, distinctive Islamic-modern UI
new_render_prayer = """  /* ───────────── رندر فوق‌العاده شکیل، خاص و زیبای اوقات شرعی ───────────── */
  function renderPrayer(data) {
    const box = el('prayerCardBody');
    if (!box) return;
    const isEn = isEnglish();
    if (!data || !data.timings) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'No data received' : 'در حال بارگذاری اوقات شرعی...') + '</div>';
      return;
    }

    const next = nextPrayer(data.timings);
    const cd = el('prayerCountdown');
    if (cd) {
      const nextLabel = next ? (isEn ? next.en : next.fa) : '';
      cd.textContent = next ? ((isEn ? 'Next: ' : 'نوبت بعدی: ') + nextLabel + ' (' + countdownText(next) + ')') : (isEn ? 'Varamin' : 'افق شرعی ورامین');
    }

    // آیکون‌های وکتوری لوکس و متمایز برای هر وقت شرعی
    const PRAYER_SVGS = {
      Fajr: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v6m0 8v6M4.93 4.93l4.24 4.24m5.66 5.66l4.24 4.24M2 12h6m8 0h6M4.93 19.07l4.24-4.24m5.66-5.66l4.24-4.24"/><circle cx="12" cy="12" r="3" fill="currentColor" fill-opacity="0.2"/></svg>',
      Sunrise: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a5 5 0 0 0-10 0M12 2v4M4.22 10.22l2.83 2.83M1 18h22M19.78 10.22l-2.83 2.83M12 9a4 4 0 0 1 4 4"/></svg>',
      Dhuhr: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4" fill="currentColor" fill-opacity="0.25"/><path d="M12 2v3m0 14v3M4.93 4.93l2.12 2.12m9.9 9.9l2.12 2.12M2 12h3m14 0h3M4.93 19.07l2.12-2.12m9.9-9.9l2.12-2.12"/></svg>',
      Asr: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5C14.5 8 13.5 6 13.5 3c-1.5 1-2.5 3-2.5 5 0 1.5.5 2.5 1 3.5-2 1.5-3 3.5-3 5.5a7 7 0 0 0 3 5z"/></svg>',
      Maghrib: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a5 5 0 0 0-10 0M12 9v4M4.22 10.22l2.83 2.83M1 18h22M19.78 10.22l-2.83 2.83M12 13l2-2"/></svg>',
      Isha: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="currentColor" fill-opacity="0.2"/></svg>'
    };

    let html = '<div class="prayer-luxury-wrap">';

    // ۱. بنر ویژه نوبت بعدی (Hero Banner)
    if (next) {
      const nextTime = data.timings[next.key] || '—';
      const nextIcon = PRAYER_SVGS[next.key] || '🕌';
      const nextLabel = isEn ? next.en : next.fa;
      const countText = countdownText(next);

      html += ''
        + '<div class="prayer-next-hero">'
        +   '<div class="pnh-glow-orb"></div>'
        +   '<div class="pnh-content">'
        +     '<div class="pnh-header">'
        +       '<div class="pnh-tag">'
        +         '<span class="pnh-pulse-dot"></span>'
        +         '<span>' + (isEn ? 'Next Prayer' : 'نوبت در پیش‌رو') + '</span>'
        +       '</div>'
        +       '<div class="pnh-countdown">'
        +         '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
        +         '<span>' + (isEn ? 'in ' + countText : countText + ' باقی‌مانده') + '</span>'
        +       '</div>'
        +     '</div>'
        +     '<div class="pnh-main">'
        +       '<div class="pnh-title-group">'
        +         '<div class="pnh-icon-wrap">' + nextIcon + '</div>'
        +         '<div class="pnh-title">' + nextLabel + '</div>'
        +       '</div>'
        +       '<div class="pnh-time" dir="ltr">' + fa(String(nextTime).slice(0, 5)) + '</div>'
        +     '</div>'
        +   '</div>'
        + '</div>';
    }

    // ۲. شبکه کارت‌های شکیل اوقات شرعی (۳ ستون در ۲ سطر منظم و دلباز)
    html += '<div class="prayer-cards-grid">';
    PRAYERS.forEach(function (p) {
      const time = data.timings[p.key] || '—';
      const isNext = next && next.key === p.key;
      const label = isEn ? p.en : p.fa;
      const svgIcon = PRAYER_SVGS[p.key] || '🕌';

      html += ''
        + '<div class="prayer-box-card' + (isNext ? ' is-active-prayer' : '') + '">'
        +   '<div class="pbc-top">'
        +     '<span class="pbc-icon">' + svgIcon + '</span>'
        +     '<span class="pbc-label">' + label + '</span>'
        +   '</div>'
        +   '<div class="pbc-time" dir="ltr">' + fa(String(time).slice(0, 5)) + '</div>'
        +   (isNext ? '<div class="pbc-active-glow"></div>' : '')
        + '</div>';
    });
    html += '</div>';

    // ۳. فوتر تاریخ هجری قمری و افق شهر با نماد تقویم
    const hijriText = isEn
      ? (data.hijriEn ? (data.hijriEn + ' AH • Varamin Horizon') : 'Varamin Horizon')
      : (data.hijriFa ? (data.hijriFa + ' هجری قمری • افق شرعی ورامین') : 'افق شرعی شهر ورامین');

    html += ''
      + '<div class="prayer-calendar-footer">'
      +   '<span class="pcf-icon">🌙</span>'
      +   '<span class="pcf-text">' + fa(hijriText) + '</span>'
      + '</div>';

    html += '</div>';
    box.innerHTML = html;
  }"""

cjs = re.sub(
    r'function renderPrayer\(data\)\s*\{.*?box\.innerHTML = html;\s*\}',
    new_render_prayer,
    cjs,
    flags=re.DOTALL
)

with open(city_live_path, 'w', encoding='utf-8') as f:
    f.write(cjs)
print("   -> renderPrayer overhauled successfully!")

