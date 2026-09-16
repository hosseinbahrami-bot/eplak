/* ============================================================
   modules/city-live.js — اطلاعات زندهٔ شهر ورامین
   · شاخص آلودگی هوا (AQI) به‌همراه نمودار ۲۴ ساعته
   · وضعیت آب‌وهوا
   · اوقات شرعی
   · پشتیبانی کامل دوزبانه (فارسی و انگلیسی)

   داده‌ها از سرویس‌های رایگان Open-Meteo و Aladhan دریافت می‌شوند
   و در localStorage ذخیره می‌شوند تا در صورت نبود اینترنت، آخرین
   مقادیرِ دریافت‌شده بدون خطا نمایش داده شود.
   ============================================================ */
(function () {
  'use strict';

  /* ───────────── ثابت‌ها ───────────── */
  const VARAMIN = { lat: 35.3247, lon: 51.6453, name: 'ورامین', nameEn: 'Varamin' };
  const CACHE_KEY = 'eplak_city_live_v1';
  const CACHE_TTL = 15 * 60 * 1000;   // ۱۵ دقیقه
  const REQUEST_TIMEOUT = 9000;       // ۹ ثانیه

  /* ───────────── ابزارها ───────────── */
  function isEnglish() {
    return (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');
  }

  function fa(input) {
    if (isEnglish()) {
      return String(input == null ? '' : input);
    }
    const digits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return String(input == null ? '' : input).replace(/[0-9]/g, d => digits[Number(d)]);
  }

  function num(value, digits) {
    const n = Number(value);
    if (!isFinite(n)) return '—';
    const fixed = typeof digits === 'number' ? n.toFixed(digits) : String(Math.round(n));
    return fa(fixed);
  }

  function el(id) { return document.getElementById(id); }

  function readCache() {
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      return (parsed && typeof parsed === 'object') ? parsed : null;
    } catch (e) { return null; }
  }

  function writeCache(data) {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify(data)); } catch (e) { /* بی‌صدا */ }
  }

  function fetchJson(url) {
    return new Promise(function (resolve, reject) {
      let done = false;
      const timer = setTimeout(function () {
        if (!done) { done = true; reject(new Error('timeout')); }
      }, REQUEST_TIMEOUT);

      fetch(url, { cache: 'no-store' })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (json) {
          if (!done) { done = true; clearTimeout(timer); resolve(json); }
        })
        .catch(function (err) {
          if (!done) { done = true; clearTimeout(timer); reject(err); }
        });
    });
  }

  /* ───────────── طبقه‌بندی کیفیت هوا ───────────── */
  const AQI_LEVELS_FA = [
    { max: 50,  label: 'پاک',       desc: 'هوای سالم — مناسب برای همه',      color: '#00C9A7', icon: '😊' },
    { max: 100, label: 'قابل قبول', desc: 'کیفیت قابل قبول — گروه‌های حساس مراقب باشند', color: '#FFD166', icon: '🙂' },
    { max: 150, label: 'ناسالم برای حساس‌ها', desc: 'گروه‌های حساس فعالیت سنگین انجام ندهند', color: '#FF9F45', icon: '😐' },
    { max: 200, label: 'ناسالم',    desc: 'همه ممکن است تحت تأثیر قرار بگیرند', color: '#FF5A5F', icon: '😷' },
    { max: 300, label: 'بسیار ناسالم', desc: 'هشدار سلامت — از خروج غیرضروری بپرهیزید', color: '#B45BE0', icon: '🤢' },
    { max: 9999, label: 'خطرناک',   desc: 'وضعیت اضطراری — در خانه بمانید',  color: '#8B3A3A', icon: '☠️' }
  ];

  const AQI_LEVELS_EN = [
    { max: 50,  label: 'Good',       desc: 'Air quality is healthy — ideal for all', color: '#00C9A7', icon: '😊' },
    { max: 100, label: 'Moderate',   desc: 'Acceptable quality — sensitive groups take care', color: '#FFD166', icon: '🙂' },
    { max: 150, label: 'Unhealthy for Sensitive', desc: 'Sensitive groups should avoid heavy outdoor exertion', color: '#FF9F45', icon: '😐' },
    { max: 200, label: 'Unhealthy',  desc: 'Everyone may begin to experience adverse health effects', color: '#FF5A5F', icon: '😷' },
    { max: 300, label: 'Very Unhealthy', desc: 'Health warning — avoid non-essential outdoor activity', color: '#B45BE0', icon: '🤢' },
    { max: 9999, label: 'Hazardous', desc: 'Emergency conditions — stay indoors',  color: '#8B3A3A', icon: '☠️' }
  ];

  function aqiLevel(aqi) {
    const v = Number(aqi) || 0;
    const levels = isEnglish() ? AQI_LEVELS_EN : AQI_LEVELS_FA;
    for (let i = 0; i < levels.length; i++) {
      if (v <= levels[i].max) return levels[i];
    }
    return levels[levels.length - 1];
  }

  /* ───────────── کدهای وضعیت هوا (WMO) ───────────── */
  const WEATHER_CODES = {
    0:  { fa: 'آفتابی',           en: 'Sunny',            icon: '☀️' },
    1:  { fa: 'عمدتاً صاف',       en: 'Mostly Clear',     icon: '🌤️' },
    2:  { fa: 'کمی ابری',         en: 'Partly Cloudy',    icon: '⛅' },
    3:  { fa: 'ابری',             en: 'Overcast',         icon: '☁️' },
    45: { fa: 'مه‌آلود',          en: 'Foggy',            icon: '🌫️' },
    48: { fa: 'مه یخ‌زده',        en: 'Freezing Fog',     icon: '🌫️' },
    51: { fa: 'نم‌نم باران',      en: 'Light Drizzle',    icon: '🌦️' },
    53: { fa: 'نم‌نم باران',      en: 'Drizzle',          icon: '🌦️' },
    55: { fa: 'نم‌نم شدید',       en: 'Heavy Drizzle',    icon: '🌦️' },
    61: { fa: 'بارانی',           en: 'Rainy',            icon: '🌧️' },
    63: { fa: 'باران متوسط',      en: 'Moderate Rain',    icon: '🌧️' },
    65: { fa: 'باران شدید',       en: 'Heavy Rain',       icon: '🌧️' },
    71: { fa: 'برف سبک',          en: 'Light Snow',       icon: '🌨️' },
    73: { fa: 'برف',              en: 'Snow',             icon: '❄️' },
    75: { fa: 'برف سنگین',        en: 'Heavy Snow',       icon: '❄️' },
    80: { fa: 'رگبار',            en: 'Showers',          icon: '🌦️' },
    81: { fa: 'رگبار شدید',       en: 'Heavy Showers',    icon: '🌧️' },
    82: { fa: 'رگبار بسیار شدید', en: 'Violent Showers',  icon: '⛈️' },
    95: { fa: 'رعد و برق',        en: 'Thunderstorm',     icon: '⛈️' },
    96: { fa: 'رعد و برق و تگرگ', en: 'Thunderstorm & Hail', icon: '⛈️' },
    99: { fa: 'رعد و برق شدید',   en: 'Severe Thunderstorm', icon: '⛈️' }
  };

  function weatherInfo(code) {
    const item = WEATHER_CODES[Number(code)];
    if (!item) return { label: isEnglish() ? 'Unknown' : 'نامشخص', icon: '🌡️' };
    return {
      label: isEnglish() ? item.en : item.fa,
      icon: item.icon
    };
  }

  /* ───────────── اوقات شرعی ───────────── */
  const PRAYERS = [
    { key: 'Fajr',    fa: 'اذان صبح', en: 'Fajr',    icon: '🌅' },
    { key: 'Sunrise', fa: 'طلوع',     en: 'Sunrise', icon: '🌄' },
    { key: 'Dhuhr',   fa: 'اذان ظهر', en: 'Dhuhr',   icon: '☀️' },
    { key: 'Asr',     fa: 'اذان عصر', en: 'Asr',     icon: '🌇' },
    { key: 'Maghrib', fa: 'اذان مغرب', en: 'Maghrib', icon: '🌆' },
    { key: 'Isha',    fa: 'اذان عشاء', en: 'Isha',    icon: '🌙' }
  ];

  function toMinutes(hhmm) {
    const parts = String(hhmm || '').split(':');
    if (parts.length < 2) return null;
    const h = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10);
    if (isNaN(h) || isNaN(m)) return null;
    return h * 60 + m;
  }

  function nowMinutes() {
    const d = new Date();
    return d.getHours() * 60 + d.getMinutes();
  }

  function nextPrayer(timings) {
    const now = nowMinutes();
    let best = null;
    PRAYERS.forEach(function (p) {
      if (p.key === 'Sunrise') { return; }   /* طلوع، وقت نماز نیست */
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
  }

  function countdownText(next) {
    if (!next) return '';
    const diff = next.mins - nowMinutes();
    const mins = diff > 0 ? diff : diff + 1440;
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    if (isEnglish()) {
      if (h <= 0) return 'in ' + m + ' minutes';
      return 'in ' + h + ' hour' + (h > 1 ? 's' : '') + ' and ' + m + ' minute' + (m !== 1 ? 's' : '');
    }
    if (h <= 0) return fa(m) + ' دقیقه دیگر';
    return fa(h) + ' ساعت و ' + fa(m) + ' دقیقه دیگر';
  }

  /* ───────────── دریافت داده‌ها ───────────── */
  function fetchAqi() {
    const url = 'https://air-quality-api.open-meteo.com/v1/air-quality'
      + '?latitude=' + VARAMIN.lat + '&longitude=' + VARAMIN.lon
      + '&current=pm2_5,pm10,us_aqi'
      + '&hourly=us_aqi'
      + '&timezone=Asia/Tehran&past_days=1&forecast_days=1';
    return fetchJson(url).then(function (json) {
      const cur = (json && json.current) || {};
      const hourly = (json && json.hourly) || {};
      const times = hourly.time || [];
      const values = hourly.us_aqi || [];

      /* ۲۴ ساعت گذشته تا ساعت جاری */
      const nowIso = new Date().toISOString().slice(0, 13) + ':00';
      let endIdx = times.indexOf(nowIso);
      if (endIdx < 0) {
        endIdx = -1;
        for (let i = times.length - 1; i >= 0; i--) {
          if (values[i] != null) { endIdx = i; break; }
        }
      }
      const startIdx = Math.max(0, endIdx - 23);
      const series = [];
      for (let i = startIdx; i <= endIdx; i++) {
        if (values[i] != null) series.push({ t: times[i], v: Number(values[i]) });
      }

      return {
        aqi: Number(cur.us_aqi) || 0,
        pm25: Number(cur.pm2_5) || 0,
        pm10: Number(cur.pm10) || 0,
        series: series,
        updatedAt: cur.time || new Date().toISOString()
      };
    });
  }

  function fetchWeather() {
    const url = 'https://api.open-meteo.com/v1/forecast'
      + '?latitude=' + VARAMIN.lat + '&longitude=' + VARAMIN.lon
      + '&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,is_day'
      + '&daily=temperature_2m_max,temperature_2m_min'
      + '&timezone=Asia/Tehran&forecast_days=1';
    return fetchJson(url).then(function (json) {
      const c = (json && json.current) || {};
      const d = (json && json.daily) || {};
      return {
        temp: Number(c.temperature_2m),
        feels: Number(c.apparent_temperature),
        humidity: Number(c.relative_humidity_2m),
        wind: Number(c.wind_speed_10m),
        code: Number(c.weather_code),
        isDay: c.is_day === 1 || c.is_day === true,
        max: Array.isArray(d.temperature_2m_max) ? Number(d.temperature_2m_max[0]) : null,
        min: Array.isArray(d.temperature_2m_min) ? Number(d.temperature_2m_min[0]) : null,
        updatedAt: c.time || new Date().toISOString()
      };
    });
  }

  function fetchPrayer() {
    const url = 'https://api.aladhan.com/v1/timings'
      + '?latitude=' + VARAMIN.lat + '&longitude=' + VARAMIN.lon + '&method=7';
    return fetchJson(url).then(function (json) {
      const timings = (json && json.data && json.data.timings) || null;
      const hijri = (json && json.data && json.data.date && json.data.date.hijri) || null;
      if (!timings) throw new Error('no timings');
      return {
        timings: timings,
        hijriFa: hijri ? (hijri.day + ' ' + hijri.month.ar + ' ' + hijri.year) : '',
        hijriEn: hijri ? (hijri.day + ' ' + (hijri.month.en || hijri.month.ar) + ' ' + hijri.year) : '',
        updatedAt: new Date().toISOString()
      };
    });
  }

  /* ───────────── رسم نمودار ───────────── */
  function buildSparkline(series, color) {
    const W = 300, H = 76, PAD = 6;
    if (!series || series.length < 2) return '';

    const values = series.map(p => p.v);
    const maxV = Math.max.apply(null, values);
    const minV = Math.min.apply(null, values);
    const top = Math.max(50, Math.ceil((maxV * 1.15) / 10) * 10);
    const bottom = Math.min(minV, 0);
    const span = Math.max(1, top - bottom);

    const stepX = (W - PAD * 2) / (values.length - 1);
    const pts = values.map(function (v, i) {
      const x = PAD + i * stepX;
      const y = PAD + (H - PAD * 2) * (1 - (v - bottom) / span);
      return [x, y];
    });

    function smooth(pathPoints) {
      let d = 'M' + pathPoints[0][0].toFixed(1) + ',' + pathPoints[0][1].toFixed(1);
      for (let i = 0; i < pathPoints.length - 1; i++) {
        const p0 = pathPoints[i];
        const p1 = pathPoints[i + 1];
        const cx = (p0[0] + p1[0]) / 2;
        d += ' C' + cx.toFixed(1) + ',' + p0[1].toFixed(1)
           + ' ' + cx.toFixed(1) + ',' + p1[1].toFixed(1)
           + ' ' + p1[0].toFixed(1) + ',' + p1[1].toFixed(1);
      }
      return d;
    }

    const line = smooth(pts);
    const area = line + ' L' + pts[pts.length - 1][0].toFixed(1) + ',' + (H - PAD)
               + ' L' + pts[0][0].toFixed(1) + ',' + (H - PAD) + ' Z';
    const last = pts[pts.length - 1];
    const gid = 'aqiGrad';

    return ''
      + '<svg class="aqi-chart" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-label="نمودار ۲۴ ساعتهٔ شاخص آلودگی">'
      + '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1">'
      + '<stop offset="0%" stop-color="' + color + '" stop-opacity="0.38"/>'
      + '<stop offset="100%" stop-color="' + color + '" stop-opacity="0.02"/>'
      + '</linearGradient></defs>'
      + '<path d="' + area + '" fill="url(#' + gid + ')"/>'
      + '<path class="aqi-chart-line" d="' + line + '" fill="none" stroke="' + color + '" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
      + '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="4" fill="' + color + '"/>'
      + '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="8" fill="' + color + '" opacity="0.22"/>'
      + '</svg>';
  }

  function buildGauge(aqi, color) {
    const pct = Math.max(0, Math.min(100, (Number(aqi) / 300) * 100));
    const R = 52, C = Math.PI * R;              /* نیم‌دایره */
    const dash = (pct / 100) * C;
    return ''
      + '<svg class="aqi-gauge" viewBox="0 0 130 78" aria-label="نمایشگر شاخص آلودگی">'
      + '<path d="M13,68 A52,52 0 0 1 117,68" fill="none" stroke="rgba(128,128,128,0.22)" stroke-width="11" stroke-linecap="round"/>'
      + '<path d="M13,68 A52,52 0 0 1 117,68" fill="none" stroke="' + color + '" stroke-width="11" stroke-linecap="round"'
      + ' stroke-dasharray="' + dash.toFixed(1) + ' ' + (C - dash).toFixed(1) + '"/>'
      + '<text x="65" y="60" text-anchor="middle" class="aqi-gauge-value" fill="' + color + '">' + fa(aqi) + '</text>'
      + '</svg>';
  }

  /* ───────────── رندر کارت‌ها ───────────── */
  function renderAqi(data) {
    const box = el('aqiCardBody');
    if (!box) return;
    const isEn = isEnglish();
    if (!data) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'No data received — retry to update' : 'داده‌ای دریافت نشد — برای به‌روزرسانی دوباره تلاش کنید') + '</div>';
      return;
    }
    const lvl = aqiLevel(data.aqi);
    const chart = buildSparkline(data.series, lvl.color);
    const badge = el('aqiBadge');
    if (badge) {
      badge.textContent = lvl.label;
      badge.style.background = lvl.color + '22';
      badge.style.color = lvl.color;
      badge.style.borderColor = lvl.color + '55';
    }
    const gaugeWrap = el('aqiGaugeWrap');
    if (gaugeWrap) gaugeWrap.innerHTML = buildGauge(data.aqi, lvl.color);

    const windowLabel = isEn ? 'Chart Window' : 'بازهٔ نمودار';
    const hoursLabel = isEn ? 'Hours' : 'ساعت';

    box.innerHTML = ''
      + '<div class="aqi-main">'
      +   '<div class="aqi-desc">' + lvl.desc + '</div>'
      + '</div>'
      + '<div class="aqi-chart-wrap">' + (chart || '<div class="city-live-empty">' + (isEn ? 'Chart unavailable' : 'نمودار در دسترس نیست') + '</div>') + '</div>'
      + '<div class="aqi-meta">'
      +   '<div class="aqi-meta-item"><span class="aqi-meta-label">PM2.5</span><span class="aqi-meta-value">' + num(data.pm25, 1) + '</span><span class="aqi-meta-unit">µg/m³</span></div>'
      +   '<div class="aqi-meta-item"><span class="aqi-meta-label">PM10</span><span class="aqi-meta-value">' + num(data.pm10, 1) + '</span><span class="aqi-meta-unit">µg/m³</span></div>'
      +   '<div class="aqi-meta-item"><span class="aqi-meta-label">' + windowLabel + '</span><span class="aqi-meta-value">' + (isEn ? '24' : '۲۴') + '</span><span class="aqi-meta-unit">' + hoursLabel + '</span></div>'
      + '</div>';
  }

  function renderWeather(data) {
    const box = el('weatherCardBody');
    if (!box) return;
    const isEn = isEnglish();
    if (!data) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'No data received' : 'داده‌ای دریافت نشد') + '</div>';
      return;
    }
    const info = weatherInfo(data.code);
    const feelsLabel = isEn ? 'Feels like' : 'احساس';
    const humidityLabel = isEn ? 'Humidity' : 'رطوبت';
    const windLabel = isEn ? 'Wind' : 'باد';
    const minLabel = isEn ? 'Min' : 'کمینه';
    const maxLabel = isEn ? 'Max' : 'بیشینه';
    const humUnit = isEn ? '%' : '٪';

    box.innerHTML = ''
      + '<div class="w-now">'
      +   '<div class="w-icon">' + info.icon + '</div>'
      +   '<div class="w-temp-wrap">'
      +     '<div class="w-temp">' + num(data.temp) + '<span class="w-deg">°</span></div>'
      +     '<div class="w-cond">' + info.label + '</div>'
      +   '</div>'
      + '</div>'
      + '<div class="w-grid">'
      +   '<div class="w-item"><span class="w-item-icon">🌡️</span><span class="w-item-label">' + feelsLabel + '</span><span class="w-item-value">' + num(data.feels) + '°</span></div>'
      +   '<div class="w-item"><span class="w-item-icon">💧</span><span class="w-item-label">' + humidityLabel + '</span><span class="w-item-value">' + num(data.humidity) + humUnit + '</span></div>'
      +   '<div class="w-item"><span class="w-item-icon">💨</span><span class="w-item-label">' + windLabel + '</span><span class="w-item-value">' + num(data.wind) + ' km/h</span></div>'
      +   '<div class="w-item"><span class="w-item-icon">📉</span><span class="w-item-label">' + minLabel + '</span><span class="w-item-value">' + num(data.min) + '°</span></div>'
      +   '<div class="w-item"><span class="w-item-icon">📈</span><span class="w-item-label">' + maxLabel + '</span><span class="w-item-value">' + num(data.max) + '°</span></div>'
      + '</div>';
  }

  function renderPrayer(data) {
    const box = el('prayerCardBody');
    if (!box) return;
    const isEn = isEnglish();
    if (!data || !data.timings) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'No data received' : 'داده‌ای دریافت نشد') + '</div>';
      return;
    }
    const next = nextPrayer(data.timings);
    const cd = el('prayerCountdown');
    if (cd) {
      const nextLabel = next ? (isEn ? next.en : next.fa) : '';
      cd.textContent = next ? (nextLabel + ' — ' + countdownText(next)) : '';
    }

    let html = '<div class="prayer-grid">';
    PRAYERS.forEach(function (p) {
      const time = data.timings[p.key] || '—';
      const isNext = next && next.key === p.key;
      const label = isEn ? p.en : p.fa;
      html += '<div class="prayer-item' + (isNext ? ' prayer-next' : '') + '">'
            +   '<span class="prayer-icon">' + p.icon + '</span>'
            +   '<span class="prayer-label">' + label + '</span>'
            +   '<span class="prayer-time" dir="ltr">' + fa(String(time).slice(0, 5)) + '</span>'
            + '</div>';
    });
    html += '</div>';

    const hijriText = isEn ? (data.hijriEn ? (data.hijriEn + ' AH') : '') : (data.hijriFa ? (data.hijriFa + ' هجری قمری') : '');
    if (hijriText) {
      html += '<div class="prayer-hijri">' + hijriText + '</div>';
    }
    box.innerHTML = html;
  }

  function setUpdated(data) {
    const node = el('cityLiveUpdated');
    if (!node || !data || !data.fetchedAt) return;
    try {
      const d = new Date(data.fetchedAt);
      const isEn = isEnglish();
      if (isEn) {
        const t = d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
        node.textContent = 'Updated: ' + t;
      } else {
        const t = d.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
        node.textContent = 'به‌روزرسانی: ' + t;
      }
    } catch (e) { /* بی‌صدا */ }
  }

  /* ───────────── مدیریت وضعیت ───────────── */
  let current = readCache();
  let loading = false;

  function paint(data) {
    if (!data) return;
    renderAqi(data.aqi);
    renderWeather(data.weather);
    renderPrayer(data.prayer);
    setUpdated(data);
  }

  function load(force) {
    if (loading) return Promise.resolve(current);
    const cached = readCache();
    const fresh = cached && (Date.now() - (cached.fetchedAt || 0)) < CACHE_TTL;

    if (!force && fresh) {
      current = cached;
      paint(cached);
      return Promise.resolve(cached);
    }
    if (cached) paint(cached);

    loading = true;
    const results = {};
    return Promise.all([
      fetchAqi().then(r => { results.aqi = r; }).catch(() => {}),
      fetchWeather().then(r => { results.weather = r; }).catch(() => {}),
      fetchPrayer().then(r => { results.prayer = r; }).catch(() => {})
    ]).then(function () {
      loading = false;
      if (!results.aqi && !results.weather && !results.prayer) {
        /* هیچ دادهٔ تازه‌ای نرسید — همان کش قبلی می‌ماند */
        if (cached) paint(cached);
        return cached;
      }
      const merged = {
        aqi: results.aqi || (cached && cached.aqi),
        weather: results.weather || (cached && cached.weather),
        prayer: results.prayer || (cached && cached.prayer),
        fetchedAt: Date.now()
      };
      current = merged;
      writeCache(merged);
      paint(merged);
      return merged;
    }).catch(function () {
      loading = false;
      if (cached) paint(cached);
      return cached;
    });
  }

  /* ───────────── راه‌اندازی ───────────── */
  function init() {
    if (readCache()) paint(readCache());
    load(false);

    const btn = el('cityLiveRefresh');
    if (btn) {
      btn.addEventListener('click', function () {
        btn.classList.add('spinning');
        load(true).then(function () {
          setTimeout(function () { btn.classList.remove('spinning'); }, 600);
        });
      });
    }

    /* به‌روزرسانی خودکار */
    setInterval(function () { load(false); }, CACHE_TTL);

    /* هر بار که پیشخوان نمایش داده شد، داده‌ها را تازه کن */
    if (typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
      window.addEventListener('eplak:screen', function (e) {
        if (e && e.detail === 'screen-dashboard') load(false);
      });

      /* رندر فوری هنگام تغییر زبان برنامه */
      window.addEventListener('languagechange', function () {
        if (current) paint(current);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.renderCityLive = function () {
    if (current) paint(current);
  };
  window.eplakCityLive = {
    refresh: function () { return load(true); },
    render: function () { if (current) paint(current); }
  };
})();
