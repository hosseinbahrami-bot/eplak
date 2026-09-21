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

  /* شهرهای تحت پوشش کارت آلودگی هوا */
  const AQI_CITIES = [
    { key: 'varamin',   fa: 'ورامین',   en: 'Varamin',   lat: 35.3247, lon: 51.6453 },
    { key: 'qarchak',   fa: 'قرچک',     en: 'Qarchak',   lat: 35.3871, lon: 51.5787 },
    { key: 'pishva',    fa: 'پیشوا',    en: 'Pishva',    lat: 35.3172, lon: 51.6808 },
    { key: 'javadabad', fa: 'جوادآباد', en: 'Javadabad', lat: 35.2403, lon: 51.6197 }
  ];
  const AQI_CITY_PREF_KEY = 'eplak_aqi_city_v1';
  const AQI_CITY_CACHE_KEY = 'eplak_aqi_cities_v1';

  function getCity(key) {
    for (let i = 0; i < AQI_CITIES.length; i++) if (AQI_CITIES[i].key === key) return AQI_CITIES[i];
    return AQI_CITIES[0];
  }
  function loadCityPref() {
    try { return localStorage.getItem(AQI_CITY_PREF_KEY) || 'varamin'; } catch (e) { return 'varamin'; }
  }
  function saveCityPref(key) {
    try { localStorage.setItem(AQI_CITY_PREF_KEY, key); } catch (e) { /* بی‌صدا */ }
  }
  let selectedCityKey = loadCityPref();

  function readCityCache() {
    try {
      const raw = localStorage.getItem(AQI_CITY_CACHE_KEY);
      const parsed = raw ? JSON.parse(raw) : {};
      return (parsed && typeof parsed === 'object') ? parsed : {};
    } catch (e) { return {}; }
  }
  function writeCityCacheEntry(key, data) {
    try {
      const all = readCityCache();
      all[key] = { d: data, t: Date.now() };
      localStorage.setItem(AQI_CITY_CACHE_KEY, JSON.stringify(all));
    } catch (e) { /* بی‌صدا */ }
  }
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

  /* روشن/تیره‌سازی رنگ hex (p از -۱۰۰ تا +۱۰۰) — برای گرادیان به سبک iOS */
  function shade(hex, p) {
    try {
      let n = String(hex || '').replace('#', '');
      if (n.length === 3) n = n.split('').map(function (c) { return c + c; }).join('');
      const num = parseInt(n, 16);
      let r = (num >> 16) & 255, g = (num >> 8) & 255, b = num & 255;
      const t = p < 0 ? 0 : 255, q = Math.abs(p) / 100;
      r = Math.round((t - r) * q + r);
      g = Math.round((t - g) * q + g);
      b = Math.round((t - b) * q + b);
      return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    } catch (e) { return hex; }
  }

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
    { max: 50,  label: 'پاک',       desc: 'هوای سالم — مناسب برای همه',      color: '#00C9A7' },
    { max: 100, label: 'قابل قبول', desc: 'کیفیت قابل قبول — گروه‌های حساس مراقب باشند', color: '#FFD166' },
    { max: 150, label: 'ناسالم برای حساس‌ها', desc: 'گروه‌های حساس فعالیت سنگین انجام ندهند', color: '#FF9F45' },
    { max: 200, label: 'ناسالم',    desc: 'همه ممکن است تحت تأثیر قرار بگیرند', color: '#FF5A5F' },
    { max: 300, label: 'بسیار ناسالم', desc: 'هشدار سلامت — از خروج غیرضروری بپرهیزید', color: '#B45BE0' },
    { max: 9999, label: 'خطرناک',   desc: 'وضعیت اضطراری — در خانه بمانید',  color: '#8B3A3A' }
  ];

  const AQI_LEVELS_EN = [
    { max: 50,  label: 'Good',       desc: 'Air quality is healthy — ideal for all', color: '#00C9A7' },
    { max: 100, label: 'Moderate',   desc: 'Acceptable quality — sensitive groups take care', color: '#FFD166' },
    { max: 150, label: 'Unhealthy for Sensitive', desc: 'Sensitive groups should avoid heavy outdoor exertion', color: '#FF9F45' },
    { max: 200, label: 'Unhealthy',  desc: 'Everyone may begin to experience adverse health effects', color: '#FF5A5F' },
    { max: 300, label: 'Very Unhealthy', desc: 'Health warning — avoid non-essential outdoor activity', color: '#B45BE0' },
    { max: 9999, label: 'Hazardous', desc: 'Emergency conditions — stay indoors',  color: '#8B3A3A' }
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
    0:  { fa: 'آفتابی',           en: 'Sunny' },
    1:  { fa: 'عمدتاً صاف',       en: 'Mostly Clear' },
    2:  { fa: 'کمی ابری',         en: 'Partly Cloudy' },
    3:  { fa: 'ابری',             en: 'Overcast' },
    45: { fa: 'مه‌آلود',          en: 'Foggy' },
    48: { fa: 'مه یخ‌زده',        en: 'Freezing Fog' },
    51: { fa: 'نم‌نم باران',      en: 'Light Drizzle' },
    53: { fa: 'نم‌نم باران',      en: 'Drizzle' },
    55: { fa: 'نم‌نم شدید',       en: 'Heavy Drizzle' },
    61: { fa: 'بارانی',           en: 'Rainy' },
    63: { fa: 'باران متوسط',      en: 'Moderate Rain' },
    65: { fa: 'باران شدید',       en: 'Heavy Rain' },
    71: { fa: 'برف سبک',          en: 'Light Snow' },
    73: { fa: 'برف',              en: 'Snow' },
    75: { fa: 'برف سنگین',        en: 'Heavy Snow' },
    80: { fa: 'رگبار',            en: 'Showers' },
    81: { fa: 'رگبار شدید',       en: 'Heavy Showers' },
    82: { fa: 'رگبار بسیار شدید', en: 'Violent Showers' },
    95: { fa: 'رعد و برق',        en: 'Thunderstorm' },
    96: { fa: 'رعد و برق و تگرگ', en: 'Thunderstorm & Hail' },
    99: { fa: 'رعد و برق شدید',   en: 'Severe Thunderstorm' }
  };

  function weatherInfo(code) {
    const item = WEATHER_CODES[Number(code)];
    if (!item) return { label: isEnglish() ? 'Unknown' : 'نامشخص' };
    return {
      label: isEnglish() ? item.en : item.fa,
      icon: item.icon
    };
  }

  /* ───────────── اوقات شرعی ───────────── */
  const PRAYERS = [
    { key: 'Fajr',    fa: 'اذان صبح', en: 'Fajr' },
    { key: 'Sunrise', fa: 'طلوع',     en: 'Sunrise' },
    { key: 'Dhuhr',   fa: 'اذان ظهر', en: 'Dhuhr' },
    { key: 'Asr',     fa: 'اذان عصر', en: 'Asr' },
    { key: 'Maghrib', fa: 'اذان مغرب', en: 'Maghrib' },
    { key: 'Isha',    fa: 'اذان عشاء', en: 'Isha' }
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
  }

    function nextPrayer(timings) {
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
  }

      function countdownText(next) {
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
  }

  /* ───────────── دریافت داده‌ها ───────────── */
  function fetchAqi(city) {
    city = city || getCity(selectedCityKey);
    const url = 'https://air-quality-api.open-meteo.com/v1/air-quality'
      + '?latitude=' + city.lat + '&longitude=' + city.lon
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
        city: city.key,
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
      + '<path class="aqi-chart-line" d="' + line + '" pathLength="1" fill="none" stroke="' + color + '" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
      + '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="4" fill="' + color + '"/>'
      + '<circle class="aqi-tip-chart-pulse" cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="8" fill="' + color + '" opacity="0.25"/>'
      + '</svg>';
  }

  function buildSpectrumBar(aqi, color) {
    const pct = Math.max(0, Math.min(100, (Number(aqi) / 300) * 100));
    return ''
      + '<div class="aqi-spectrum-wrap">'
      +   '<span class="aqi-spectrum-edge">۰</span>'
      +   '<div class="aqi-spectrum">'
      +     '<div class="aqi-spectrum-marker" style="--pos:' + pct.toFixed(2) + '%; --mk:' + color + ';"></div>'
      +   '</div>'
      +   '<span class="aqi-spectrum-edge">۳۰۰+</span>'
      + '</div>';
  }

  /* ───────────── رندر کارت‌ها ───────────── */
  function buildCityBar(activeKey) {
    const isEn = isEnglish();
    let tabs = '';
    for (let i = 0; i < AQI_CITIES.length; i++) {
      const c = AQI_CITIES[i];
      const name = isEn ? c.en : c.fa;
      tabs += '<button type="button" class="aqi-city-tab' + (c.key === activeKey ? ' active' : '') + '" onclick="selectAqiCity(\'' + c.key + '\')">' + name + '</button>';
    }
    return '<div class="aqi-citybar">' + tabs + '</div>';
  }

  function renderAqi(data) {
    const box = el('aqiCardBody');
    const gaugeWrap = el('aqiGaugeWrap');
    if (!box) return;
    const isEn = isEnglish();

    const cityKey = (data && data.city) ? data.city : selectedCityKey;
    const city = getCity(cityKey);

    /* تب شهرها همیشه بالای کارت هست */
    if (gaugeWrap) {
      gaugeWrap.innerHTML = buildCityBar(cityKey)
        + (data ? '' : '');
    }

    if (!data) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'No data received — retry to update' : 'داده‌ای دریافت نشد — برای به‌روزرسانی دوباره تلاش کنید') + '</div>';
      return;
    }

    const lvl = aqiLevel(data.aqi);
    const chart = buildSparkline(data.series, lvl.color);


    const badge = el('aqiBadge');
    if (badge) badge.textContent = lvl.label;

    /* گرادیان تمام‌کادر به رنگ سطح هوا — سبک آب‌وهوای iOS */
    const card = el('aqiCard');
    if (card && card.style) {
      card.style.setProperty('--aqi', lvl.color);
      card.style.setProperty('--aqi-a', shade(lvl.color, 18));
      card.style.setProperty('--aqi-b', shade(lvl.color, -42));
    }

    if (gaugeWrap) {
      gaugeWrap.innerHTML = buildCityBar(cityKey)
        + '<div class="aqi-ios-hero">'
        +   '<div class="aqi-ios-num">' + fa(data.aqi) + '</div>'
        +   '<div class="aqi-ios-level">' + lvl.label + '</div>'
        +   '<div class="aqi-ios-desc">' + lvl.desc + '</div>'
        +   '<div class="aqi-ios-city">' + (isEn ? city.en : city.fa) + '</div>'
        + '</div>'
        + buildSpectrumBar(data.aqi, lvl.color);
    }

    const windowLabel = isEn ? 'Chart Window' : 'بازهٔ نمودار';
    const hoursLabel = isEn ? 'Hours' : 'ساعت';

    box.innerHTML = ''
      + '<div class="aqi-chart-panel">' + (chart || '<div class="city-live-empty">' + (isEn ? 'Chart unavailable' : 'نمودار در دسترس نیست') + '</div>') + '</div>'
      + '<div class="aqi-meta">'
      +   '<div class="aqi-meta-item"><span class="aqi-meta-label">PM2.5</span><span class="aqi-meta-value">' + num(data.pm25, 1) + '</span><span class="aqi-meta-unit">µg/m³</span></div>'
      +   '<div class="aqi-meta-item"><span class="aqi-meta-label">PM10</span><span class="aqi-meta-value">' + num(data.pm10, 1) + '</span><span class="aqi-meta-unit">µg/m³</span></div>'
      +   '<div class="aqi-meta-item"><span class="aqi-meta-label">' + windowLabel + '</span><span class="aqi-meta-value">' + (isEn ? '24' : '۲۴') + '</span><span class="aqi-meta-unit">' + hoursLabel + '</span></div>'
      + '</div>';
  }

  /* ───────────── انتخاب شهر ───────────── */
  function selectAqiCity(key) {
    if (!getCity(key) || key === selectedCityKey) return;
    selectedCityKey = key;
    saveCityPref(key);

    const cache = readCityCache();
    const hit = cache[key];
    if (hit && hit.d && (Date.now() - (hit.t || 0)) < CACHE_TTL) {
      renderAqi(hit.d);
      return;
    }

    /* حالت انتظار */
    const gaugeWrap = el('aqiGaugeWrap');
    const box = el('aqiCardBody');
    if (gaugeWrap) gaugeWrap.innerHTML = buildCityBar(key);
    if (box) box.innerHTML = '<div class="city-live-empty">' + (isEnglish() ? 'Loading city data…' : 'در حال دریافت داده‌های شهر…') + '</div>';

    fetchAqi(getCity(key)).then(function (d) {
      writeCityCacheEntry(key, d);
      if (selectedCityKey === key) renderAqi(d);
    }).catch(function () {
      if (selectedCityKey === key && hit && hit.d) renderAqi(hit.d);
      else if (selectedCityKey === key) {
        const b = el('aqiCardBody');
        if (b) b.innerHTML = '<div class="city-live-empty">' + (isEnglish() ? 'No data received — retry' : 'داده‌ای دریافت نشد — دوباره تلاش کنید') + '</div>';
      }
    });
  }

      function renderWeather(data) {
    const box = el('weatherCardBody');
    if (!box) return;
    if (window.Weather3D && typeof window.Weather3D.init === 'function') {
      window.Weather3D.init(box, data);
      return;
    }
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
      +   '<div class="w-icon">' + (window.EplakIcons ? window.EplakIcons.get(info.icon) : info.icon) + '</div>'
      +   '<div class="w-temp-wrap">'
      +     '<div class="w-temp">' + num(data.temp) + '<span class="w-deg">°</span></div>'
      +     '<div class="w-cond">' + info.label + '</div>'
      +   '</div>'
      + '</div>'
      + '<div class="w-grid">'
      +   '<div class="w-item"><span class="w-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px;vertical-align:middle;"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg></span><span class="w-item-label">' + feelsLabel + '</span><span class="w-item-value">' + num(data.feels) + '°</span></div>'
      +   '<div class="w-item"><span class="w-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px;vertical-align:middle;"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg></span><span class="w-item-label">' + humidityLabel + '</span><span class="w-item-value">' + num(data.humidity) + humUnit + '</span></div>'
      +   '<div class="w-item"><span class="w-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px;vertical-align:middle;"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg></span><span class="w-item-label">' + windLabel + '</span><span class="w-item-value">' + num(data.wind) + ' km/h</span></div>'
      +   '<div class="w-item"><span class="w-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px;vertical-align:middle;"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg></span><span class="w-item-label">' + minLabel + '</span><span class="w-item-value">' + num(data.min) + '°</span></div>'
      +   '<div class="w-item"><span class="w-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px;vertical-align:middle;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></span><span class="w-item-label">' + maxLabel + '</span><span class="w-item-value">' + num(data.max) + '°</span></div>'
      + '</div>';
  }

        /* ───────────── رندر فوق‌العاده مدرن، شکیل و فشرده اوقات شرعی ───────────── */
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
  // نمایش فوری استیج ۳ بعدی حتی قبل از دریافت پاسخ شبکه
  try {
    const initialBox = el('weatherCardBody');
    if (initialBox && window.Weather3D) {
      window.Weather3D.init(initialBox, current ? current.weather : null);
    }
  } catch (e) {}

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

    /* به‌روزرسانی دقیقه به دقیقه شمارش معکوس اذان */
    setInterval(function () { if (current && current.prayer) renderPrayer(current.prayer); }, 60000);

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
  window.selectAqiCity = selectAqiCity;
})();
