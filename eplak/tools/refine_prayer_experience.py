import re

city_live_path = '/home/user/eplak/eplak-fixed/modules/city-live.js'
with open(city_live_path, 'r', encoding='utf-8') as f:
    cjs = f.read()

# Update countdownText to be natural and poetic
new_countdown = """  function countdownText(next) {
    if (!next) return '';
    const diff = next.mins - nowMinutes();
    const mins = diff > 0 ? diff : diff + 1440;
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    if (isEnglish()) {
      if (h <= 0) return m + ' min to prayer';
      return h + 'h ' + m + 'm to prayer';
    }
    if (h <= 0) return fa(m) + ' دقیقه تا اذان';
    return fa(h) + ' ساعت و ' + fa(m) + ' دقیقه تا اذان';
  }"""

cjs = re.sub(
    r'function countdownText\(next\)\s*\{.*?return fa\(h\)[^\}]*\}',
    new_countdown,
    cjs,
    flags=re.DOTALL
)

# Replace renderPrayer with the full luxury implementation
new_render_prayer = """  /* ───────────── رندر فوق‌العاده شکیل، خاص و زیبای اوقات شرعی ───────────── */
  function renderPrayer(data) {
    const box = el('prayerCardBody');
    if (!box) return;
    const isEn = isEnglish();
    if (!data || !data.timings) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'Loading prayer times...' : 'در حال دریافت اوقات شرعی...') + '</div>';
      return;
    }

    const next = nextPrayer(data.timings);
    const cd = el('prayerCountdown');
    if (cd) {
      const nextLabel = next ? (isEn ? next.en : next.fa) : '';
      cd.textContent = next ? ((isEn ? 'Next: ' : 'نوبت در پیش‌رو: ') + nextLabel) : (isEn ? 'Varamin Horizon' : 'افق شرعی شهر ورامین');
    }

    // آیکون‌های وکتوری اختصاصی با پالت رنگی شکیل برای هر وقت شرعی
    const PRAYER_THEMES = {
      Fajr: {
        color: '#38BDF8',
        bg: 'rgba(56, 189, 248, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3m0 12v3M5 12H2m20 0h-3M6.3 6.3l2.1 2.1m7.2 7.2l2.1 2.1M6.3 17.7l2.1-2.1m7.2-7.2l2.1-2.1"/><circle cx="12" cy="12" r="3.2" fill="currentColor" fill-opacity="0.25"/></svg>'
      },
      Sunrise: {
        color: '#F59E0B',
        bg: 'rgba(245, 158, 11, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a5 5 0 0 0-10 0M12 2v5M4.22 10.22l2.83 2.83M1 18h22M19.78 10.22l-2.83 2.83M12 11a3 3 0 0 1 3 3"/></svg>'
      },
      Dhuhr: {
        color: '#FBBF24',
        bg: 'rgba(251, 191, 36, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.5" fill="currentColor" fill-opacity="0.25"/><path d="M12 1v3m0 16v3M4.22 4.22l2.12 2.12m11.32 11.32l2.12 2.12M1 12h3m16 0h3M4.22 19.78l2.12-2.12m11.32-11.32l2.12-2.12"/></svg>'
      },
      Asr: {
        color: '#FB923C',
        bg: 'rgba(251, 146, 60, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="4" fill="currentColor" fill-opacity="0.25"/><path d="M8 2v2m0 8v2M2 8h2m8 0h2m7 10H3m18-4H7"/></svg>'
      },
      Maghrib: {
        color: '#F43F5E',
        bg: 'rgba(244, 63, 94, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a5 5 0 0 0-10 0M12 9v5M4.22 10.22l2.83 2.83M1 18h22M19.78 10.22l-2.83 2.83M12 14l2-2"/></svg>'
      },
      Isha: {
        color: '#A78BFA',
        bg: 'rgba(167, 139, 250, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="currentColor" fill-opacity="0.25"/><path d="M19 4v2m-1-1h2"/></svg>'
      }
    };

    let html = '<div class="prayer-luxury-wrap">';

    // ۱. بنر ویژه نوبت در پیش‌رو (Hero Banner)
    if (next) {
      const nextTime = data.timings[next.key] || '—';
      const theme = PRAYER_THEMES[next.key] || { color: '#00E5C3', bg: 'rgba(0,229,195,0.15)', svg: '🕌' };
      const nextLabel = isEn ? next.en : next.fa;
      const countText = countdownText(next);

      html += ''
        + '<div class="prayer-next-hero">'
        +   '<div class="pnh-glow-orb"></div>'
        +   '<div class="pnh-content">'
        +     '<div class="pnh-header">'
        +       '<div class="pnh-tag">'
        +         '<span class="pnh-pulse-dot"></span>'
        +         '<span>' + (isEn ? 'Upcoming Prayer' : 'نوبت در پیش‌رو') + '</span>'
        +       '</div>'
        +       '<div class="pnh-countdown">'
        +         '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
        +         '<span>' + countText + '</span>'
        +       '</div>'
        +     '</div>'
        +     '<div class="pnh-main">'
        +       '<div class="pnh-title-group">'
        +         '<div class="pnh-icon-wrap" style="color:' + theme.color + '; background:' + theme.bg + '; border-color:' + theme.color + '44;">'
        +           theme.svg
        +         '</div>'
        +         '<div>'
        +           '<div class="pnh-title">' + nextLabel + '</div>'
        +           '<div class="pnh-sub">' + (isEn ? 'Varamin Horizon' : 'افق شرعی شهر ورامین') + '</div>'
        +         '</div>'
        +       '</div>'
        +       '<div class="pnh-time" dir="ltr">' + fa(String(nextTime).slice(0, 5)) + '</div>'
        +     '</div>'
        +   '</div>'
        + '</div>';
    }

    // ۲. شبکه کارت‌های شکیل اوقات شرعی (۳ ستون در ۲ سطر منظم)
    html += '<div class="prayer-cards-grid">';
    PRAYERS.forEach(function (p) {
      const time = data.timings[p.key] || '—';
      const isNext = next && next.key === p.key;
      const label = isEn ? p.en : p.fa;
      const theme = PRAYER_THEMES[p.key] || { color: '#00E5C3', bg: 'rgba(0,229,195,0.15)', svg: '🕌' };

      html += ''
        + '<div class="prayer-box-card' + (isNext ? ' is-active-prayer' : '') + '">'
        +   '<div class="pbc-top">'
        +     '<span class="pbc-icon-disc" style="color:' + theme.color + '; background:' + theme.bg + ';">' + theme.svg + '</span>'
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
    r'/\* ──+ رندر فوق‌العاده شکیل.*?box\.innerHTML = html;\s*\}',
    new_render_prayer,
    cjs,
    flags=re.DOTALL
)

# Add 1-minute ticker for prayer countdown in init
if 'setInterval(function () { if (current && current.prayer) renderPrayer(current.prayer); }, 60000);' not in cjs:
    cjs = cjs.replace(
        "/* به‌روزرسانی خودکار */",
        "/* به‌روزرسانی دقیقه به دقیقه شمارش معکوس اذان */\n    setInterval(function () { if (current && current.prayer) renderPrayer(current.prayer); }, 60000);\n\n    /* به‌روزرسانی خودکار */"
    )

with open(city_live_path, 'w', encoding='utf-8') as f:
    f.write(cjs)

print("city-live.js updated successfully!")
