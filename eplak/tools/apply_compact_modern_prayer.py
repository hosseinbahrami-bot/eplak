import re

# 1. Update city-live.js
city_live_path = '/home/user/eplak/eplak-fixed/modules/city-live.js'
with open(city_live_path, 'r', encoding='utf-8') as f:
    cjs = f.read()

# Fix nowMinutes to use Asia/Tehran timezone with local fallback
new_now_minutes = """  function nowMinutes() {
    try {
      const tf = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Tehran', hour: 'numeric', minute: 'numeric', hour12: false });
      const parts = tf.formatToParts(new Date());
      let h = 0, m = 0;
      parts.forEach(function (p) {
        if (p.type === 'hour') h = parseInt(p.value, 10);
        if (p.type === 'minute') m = parseInt(p.value, 10);
      });
      if (h === 24) h = 0;
      return h * 60 + m;
    } catch (e) {
      const d = new Date();
      return d.getHours() * 60 + d.getMinutes();
    }
  }"""

cjs = re.sub(
    r'function nowMinutes\(\)\s*\{.*?return d\.getHours\(\)[^\}]*\}',
    new_now_minutes,
    cjs,
    flags=re.DOTALL
)

# Fix nextPrayer to include Sunrise (طلوع) and NOT skip it!
new_next_prayer = """  function nextPrayer(timings) {
    const now = nowMinutes();
    let best = null;
    PRAYERS.forEach(function (p) {
      const mins = toMinutes(timings ? timings[p.key] : null);
      if (mins == null) return;
      if (mins > now && (best == null || mins < best.mins)) {
        best = { key: p.key, fa: p.fa, en: p.en, mins: mins };
      }
    });
    if (!best && timings) {
      const first = toMinutes(timings[PRAYERS[0].key]);
      if (first != null) best = { key: PRAYERS[0].key, fa: PRAYERS[0].fa, en: PRAYERS[0].en, mins: first + 1440 };
    }
    return best;
  }"""

cjs = re.sub(
    r'function nextPrayer\(timings\)\s*\{.*?return best;\s*\}',
    new_next_prayer,
    cjs,
    flags=re.DOTALL
)

# Fix countdownText for Sunrise vs Prayer
new_countdown = """  function countdownText(next) {
    if (!next) return '';
    const diff = next.mins - nowMinutes();
    const mins = diff > 0 ? diff : diff + 1440;
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    const isSunrise = (next.key === 'Sunrise');
    if (isEnglish()) {
      const tgt = isSunrise ? 'sunrise' : 'prayer';
      if (h <= 0) return m + ' min to ' + tgt;
      return h + 'h ' + m + 'm to ' + tgt;
    }
    const targetName = isSunrise ? 'طلوع' : 'اذان';
    if (h <= 0) return fa(m) + ' دقیقه تا ' + targetName;
    return fa(h) + ' ساعت و ' + fa(m) + ' دقیقه تا ' + targetName;
  }"""

cjs = re.sub(
    r'function countdownText\(next\)\s*\{.*?return fa\(h\)[^\}]*\}',
    new_countdown,
    cjs,
    flags=re.DOTALL
)

# New ultra-modern, crisp line-art vector icons and ultra-compact renderPrayer
new_render_prayer = """  /* ───────────── رندر فوق‌العاده مدرن، شکیل و فشرده اوقات شرعی ───────────── */
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

    // آیکون‌های وکتوری کاملاً مدرن، مینیمال و خطی (Ultra-Modern Minimal SVG Icons)
    const MODERN_PRAYER_THEMES = {
      Fajr: {
        color: '#38BDF8',
        bg: 'rgba(56, 189, 248, 0.12)',
        svg: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="18" x2="21" y2="18"/><path d="M7 18a5 5 0 0 1 10 0"/><line x1="12" y1="5" x2="12" y2="8"/><line x1="6.8" y1="9.8" x2="8.8" y2="11.8"/><line x1="17.2" y1="9.8" x2="15.2" y2="11.8"/></svg>'
      },
      Sunrise: {
        color: '#F59E0B',
        bg: 'rgba(245, 158, 11, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="19" x2="21" y2="19"/><path d="M6 19a6 6 0 0 1 12 0"/><polyline points="9 8 12 5 15 8"/><line x1="12" y1="5" x2="12" y2="13"/></svg>'
      },
      Dhuhr: {
        color: '#FBBF24',
        bg: 'rgba(251, 191, 36, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3.8"/><line x1="12" y1="2" x2="12" y2="4.5"/><line x1="12" y1="19.5" x2="12" y2="22"/><line x1="2" y1="12" x2="4.5" y2="12"/><line x1="19.5" y1="12" x2="22" y2="12"/><line x1="4.9" y1="4.9" x2="6.6" y2="6.6"/><line x1="17.4" y1="17.4" x2="19.1" y2="19.1"/><line x1="4.9" y1="19.1" x2="6.6" y2="17.4"/><line x1="17.4" y1="6.6" x2="19.1" y2="4.9"/></svg>'
      },
      Asr: {
        color: '#FB923C',
        bg: 'rgba(251, 146, 60, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="15" cy="9" r="3.2"/><line x1="3" y1="20" x2="21" y2="20"/><line x1="15" y1="2" x2="15" y2="3.8"/><line x1="22" y1="9" x2="20.2" y2="9"/><line x1="5" y1="20" x2="11.5" y2="13.5"/></svg>'
      },
      Maghrib: {
        color: '#F43F5E',
        bg: 'rgba(244, 63, 94, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="19" x2="21" y2="19"/><path d="M6 19a6 6 0 0 1 12 0"/><polyline points="9 11 12 14 15 11"/><line x1="12" y1="7" x2="12" y2="14"/></svg>'
      },
      Isha: {
        color: '#A78BFA',
        bg: 'rgba(167, 139, 250, 0.14)',
        svg: '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/><circle cx="18" cy="5" r="1" fill="currentColor"/></svg>'
      }
    };

    let html = '<div class="prayer-luxury-wrap">';

    // ۱. بنر ویژه و بسیار فشرده نوبت در پیش‌رو (Compact Hero Banner)
    if (next) {
      const nextTime = data.timings[next.key] || '—';
      const theme = MODERN_PRAYER_THEMES[next.key] || { color: '#00E5C3', bg: 'rgba(0,229,195,0.15)', svg: '' };
      const nextLabel = isEn ? next.en : next.fa;
      const countText = countdownText(next);

      html += ''
        + '<div class="prayer-next-hero">'
        +   '<div class="pnh-content">'
        +     '<div class="pnh-header">'
        +       '<div class="pnh-tag">'
        +         '<span class="pnh-pulse-dot"></span>'
        +         '<span>' + (isEn ? 'Next' : 'در پیش‌رو') + '</span>'
        +       '</div>'
        +       '<div class="pnh-countdown">'
        +         '<svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
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
        +         '</div>'
        +       '</div>'
        +       '<div class="pnh-time" dir="ltr">' + fa(String(nextTime).slice(0, 5)) + '</div>'
        +     '</div>'
        +   '</div>'
        + '</div>';
    }

    // ۲. شبکه ۶ کادر فشرده و شکیل اوقات شرعی (۳ ستون در ۲ سطر کم‌ارتفاع و ظریف)
    html += '<div class="prayer-cards-grid">';
    PRAYERS.forEach(function (p) {
      const time = data.timings[p.key] || '—';
      const isNext = next && next.key === p.key;
      const label = isEn ? p.en : p.fa;
      const theme = MODERN_PRAYER_THEMES[p.key] || { color: '#00E5C3', bg: 'rgba(0,229,195,0.15)', svg: '' };

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

    // ۳. فوتر تاریخ هجری قمری و افق شهر در قالب کپسول بسیار ظریف و کوچک
    const hijriText = isEn
      ? (data.hijriEn ? (data.hijriEn + ' AH • Varamin') : 'Varamin')
      : (data.hijriFa ? (data.hijriFa + ' هجری قمری • افق ورامین') : 'افق شرعی شهر ورامین');

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

with open(city_live_path, 'w', encoding='utf-8') as f:
    f.write(cjs)

print("Updated city-live.js with modern icons, Sunrise support, and compact structure!")
