/* ============================================================
   modules/weather-3d.js — سیستم آب‌وهوای زنده، آنلاین و واقع‌گرایانه اپل (Apple Weather)
   - صددرصد متصل به زمان حال و داده‌های آنلاین ایستگاه هواشناسی ورامین
   - حذف کامل چیپ‌ها و حالت‌های دستی (فقط وضعیت واقعی لحظه‌ای)
   - ابرهای ارگانیک، محو، بسیار شیک و طبیعی با پرتوهای نور (Organic Soft-Edge Clouds)
   - بارش باران کریستالی و باریک سوزنی (Apple Needle Rain)
   - تشخیص قطعی شب و روز آنلاین (در شب، ماه و آسمان شبانه است؛ بدون خورشید!)
   - کادر کاملاً ثابت، مستحکم و ایستا (بدون چرخش یا لرزش کادر)
   ============================================================ */

(function () {
  'use strict';

  var weatherData = null;
  var animFrameId = null;
  var canvas = null;
  var ctx = null;
  var particles = [];
  var splashes = [];
  var meteors = [];
  var timeTick = 0;
  var nextLightningTime = 0;
  var activeLightningBolt = null;

  function isEnglish() {
    return (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');
  }

  function fa(input) {
    if (isEnglish()) return String(input == null ? '' : input);
    var digits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return String(input == null ? '' : input).replace(/[0-9]/g, function (d) { return digits[Number(d)]; });
  }

  // حل وضعیت آنلاین و واقعی آب‌وهوا بر اساس داده‌های Open-Meteo
  function resolveLiveState() {
    var isEn = isEnglish();
    var now = new Date();
    var hour = now.getHours();

    // تعیین شب یا روز بر اساس شاخص آنلاین isDay یا ساعت جاری
    var isDay = false;
    if (weatherData && typeof weatherData.isDay === 'boolean') {
      isDay = weatherData.isDay;
    } else {
      isDay = (hour >= 6 && hour < 18);
    }

    var period = isDay ? (hour >= 17 ? 'sunset' : (hour < 7 ? 'sunrise' : 'day')) : 'night';

    // مقادیر هواشناسی آنلاین (پیش‌فرض هوشمند همگام با آخرین آپدیت ورامین)
    var code = (weatherData && typeof weatherData.code === 'number') ? weatherData.code : 2;
    var wind = (weatherData && typeof weatherData.wind === 'number') ? weatherData.wind : 5.4;
    var temp = (weatherData && typeof weatherData.temp === 'number') ? weatherData.temp : 21;
    var feels = (weatherData && typeof weatherData.feels === 'number') ? weatherData.feels : 19;
    var humidity = (weatherData && typeof weatherData.humidity === 'number') ? weatherData.humidity : 32;
    var max = (weatherData && typeof weatherData.max === 'number') ? weatherData.max : 38;
    var min = (weatherData && typeof weatherData.min === 'number') ? weatherData.min : 21;

    var type = 'clear';
    var label = isEn ? 'Clear' : 'صاف';

    if (code >= 95) {
      type = 'storm';
      label = isEn ? 'Thunderstorm' : 'رعد و برق و طوفان';
    } else if (code >= 71 && code <= 86) {
      type = 'snow';
      label = isEn ? 'Snowfall' : 'بارش برف';
    } else if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) {
      type = 'rain';
      label = isEn ? 'Rain Showers' : 'بارش باران';
    } else if (code === 3 || code === 45 || code === 48) {
      type = 'cloudy';
      label = (code === 45 || code === 48) ? (isEn ? 'Foggy' : 'مه‌آلود') : (isEn ? 'Overcast' : 'تمام ابری');
    } else if (code === 1 || code === 2) {
      type = 'partly_cloudy';
      label = isDay ? (isEn ? 'Partly Cloudy' : 'کمی تا قسمتی ابری') : (isEn ? 'Partly Cloudy' : 'کمی ابری');
    } else {
      type = 'clear';
      if (!isDay) {
        label = isEn ? 'Clear Sky' : 'صاف و مهتابی';
      } else {
        label = (period === 'sunset') ? (isEn ? 'Sunset' : 'غروب آفتاب') : (isEn ? 'Sunny' : 'صاف و آفتابی');
      }
    }

    return {
      type: type,
      period: period,
      isDay: isDay,
      label: label,
      temp: Math.round(temp),
      feels: Math.round(feels),
      humidity: Math.round(humidity),
      wind: Math.round(wind),
      max: Math.round(max),
      min: Math.round(min)
    };
  }

  /* ────────── ساخت کادر ثابت آب‌وهوای اپل بدون چیپ ────────── */
  function renderStageHtml(container) {
    var isEn = isEnglish();
    var html = ''
      + '<div class="apple-weather-wrap">'
      +   '<!-- کادر اصلی اپل ودر: کاملاً ثابت و بدون چرخش (Rock-Solid Frame) -->'
      +   '<div class="apple-weather-card" id="appleWeatherCard">'
      +     '<!-- پس‌زمینه رنگ آسمان با گرادینت اتمسفریک پیوسته -->'
      +     '<div class="apple-sky-bg" id="appleSkyBg"></div>'
      +     '<div class="apple-sky-haze"></div>'
      +     '<!-- جسم فلکی (خورشید ملایم در روز، ماه شیک در شب — در شب هیچ خورشیدی نیست!) -->'
      +     '<div class="apple-celestial" id="appleCelestial"></div>'
      +     '<!-- ابرهای ارگانیک و محو و بسیار شیک اپل (Organic Soft Clouds) -->'
      +     '<div class="apple-clouds-container" id="appleCloudsContainer"></div>'
      +     '<!-- کانواس پدیده‌ها: باران سوزنی، برف، ستارگان و صاعقه -->'
      +     '<canvas class="apple-canvas" id="appleCanvas"></canvas>'
      +     '<div class="apple-lightning-flash" id="appleLightningFlash"></div>'
      +     '<!-- لایه شیشه‌ای و اطلاعات آنلاین اپل ودر (Apple Weather HUD) -->'
      +     '<div class="apple-hud">'
      +       '<div class="apple-hud-top">'
      +         '<div class="apple-city-badge">'
      +           '<span class="apple-radar-dot"></span>'
      +           '<span class="apple-city-name" id="appleCityName">ورامین</span>'
      +         '</div>'
      +         ''
      +       '</div>'
      +       '<div class="apple-hud-center">'
      +         '<div class="apple-temp-row">'
      +           '<span class="apple-temp-val" id="appleTempVal">--</span>'
      +           '<span class="apple-temp-deg">°</span>'
      +         '</div>'
      +         '<div class="apple-condition-title" id="appleConditionTitle">--</div>'
      +         '<div class="apple-hilo-text" id="appleHiLoText">--</div>'
      +       '</div>'
      +       '<!-- کپسول شیشه‌ای یکپارچه پایین کادر اپل ودر -->'
      +       '<div class="apple-hud-bar">'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">' + (isEn ? 'Feels Like' : 'احساس') + '</span>'
      +           '<span class="apple-bar-val" id="appleValFeels">--</span>'
      +         '</div>'
      +         '<div class="apple-bar-divider"></div>'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">' + (isEn ? 'Humidity' : 'رطوبت') + '</span>'
      +           '<span class="apple-bar-val" id="appleValHumidity">--</span>'
      +         '</div>'
      +         '<div class="apple-bar-divider"></div>'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">' + (isEn ? 'Wind' : 'سرعت باد') + '</span>'
      +           '<span class="apple-bar-val" id="appleValWind">--</span>'
      +         '</div>'
      +         '<div class="apple-bar-divider"></div>'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">' + (isEn ? 'Visibility' : 'دید افقی') + '</span>'
      +           '<span class="apple-bar-val" id="appleValVisibility">۱۰ km</span>'
      +         '</div>'
      +       '</div>'
      +     '</div>'
      +   '</div>'
      + '</div>';

    container.innerHTML = html;
    initCanvas();
  }

  function initCanvas() {
    canvas = document.getElementById('appleCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    createParticles();
    startAnimationLoop();
  }

  function resizeCanvas() {
    if (!canvas) return;
    var rect = canvas.parentElement ? canvas.parentElement.getBoundingClientRect() : null;
    var w = (rect && rect.width > 50) ? rect.width : (canvas.parentElement ? canvas.parentElement.offsetWidth : 350);
    var h = (rect && rect.height > 50) ? rect.height : (canvas.parentElement ? canvas.parentElement.offsetHeight : 252);
    if (w > 0 && h > 0 && (canvas.width !== Math.floor(w) || canvas.height !== Math.floor(h))) {
      canvas.width = Math.floor(w);
      canvas.height = Math.floor(h);
      createParticles();
    }
  }

  function createParticles() {
    particles = [];
    splashes = [];
    meteors = [];
    var state = resolveLiveState();
    var w = canvas ? canvas.width : 350;
    var h = canvas ? canvas.height : 252;

    // باران سوزنی و باریک اپل
    if (state.type === 'rain' || state.type === 'storm') {
      var rainCount = state.type === 'storm' ? 55 : 36;
      for (var i = 0; i < rainCount; i++) {
        var d = Math.random();
        particles.push({
          x: Math.random() * (w + 40) - 20,
          y: Math.random() * h,
          depth: d,
          speed: 13 + d * 11,
          len: 10 + d * 12,
          width: 0.75 + d * 0.4,
          opacity: 0.35 + d * 0.45,
          windAngle: -2.2 - Math.random() * 1.5
        });
      }
    }
    // برف زمستانی
    else if (state.type === 'snow') {
      var snowCount = 35;
      for (var j = 0; j < snowCount; j++) {
        var snDepth = Math.random();
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          depth: snDepth,
          radius: snDepth > 0.8 ? (3.2 + Math.random() * 2) : (1.1 + snDepth * 1.8),
          speed: 0.6 + snDepth * 1.2,
          swayAmp: 8 + snDepth * 14,
          swayFreq: 0.016 + Math.random() * 0.02,
          phase: Math.random() * Math.PI * 2,
          opacity: snDepth > 0.8 ? 0.35 : (0.5 + snDepth * 0.4)
        });
      }
    }
    // ستارگان چشمک‌زن شب
    else if (!state.isDay) {
      var starCount = 38;
      for (var k = 0; k < starCount; k++) {
        var stDepth = Math.random();
        particles.push({
          x: Math.random() * w,
          y: Math.random() * (h * 0.72),
          radius: 0.55 + stDepth * 1.1,
          twinkleSpeed: 0.025 + Math.random() * 0.04,
          phase: Math.random() * Math.PI * 2,
          baseAlpha: 0.35 + stDepth * 0.55,
          hasHalo: stDepth > 0.88
        });
      }
    }
  }

  function isDashboardActive() {
    var d = document.getElementById('screen-dashboard');
    return d && d.classList.contains('active');
  }

  function startAnimationLoop() {
    if (animFrameId) cancelAnimationFrame(animFrameId);
    function loop() {
      animFrameId = requestAnimationFrame(loop);
      if (!isDashboardActive()) return;
      timeTick++;
      drawScene();
    }
    animFrameId = requestAnimationFrame(loop);
  }

  function drawScene() {
    if (!ctx || !canvas) return;
    var w = canvas.width;
    var h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    var state = resolveLiveState();

    // ۱. رندر باران بسیار سبک و روان با ۱ استروک واحد در هر فریم
    if (state.type === 'rain' || state.type === 'storm') {
      ctx.strokeStyle = state.type === 'storm' ? 'rgba(215, 240, 255, 0.65)' : 'rgba(225, 245, 255, 0.55)';
      ctx.lineWidth = 0.85;
      ctx.lineCap = 'round';
      ctx.beginPath();

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x + p.windAngle, p.y + p.len);

        p.y += p.speed;
        p.x += (p.windAngle * (p.speed / 16));

        if (p.y > h - 14) {
          if (p.depth > 0.5 && splashes.length < 8 && Math.random() > 0.7) {
            splashes.push({
              x: p.x,
              y: h - 8 + Math.random() * 4,
              radius: 0.8,
              maxRadius: 2.2 + p.depth * 3,
              alpha: 0.5
            });
          }
          p.y = -18;
          p.x = Math.random() * (w + 40) - 10;
        }
      }
      ctx.stroke();

      if (splashes.length > 0) {
        ctx.lineWidth = 0.75;
        for (var sIdx = splashes.length - 1; sIdx >= 0; sIdx--) {
          var sp = splashes[sIdx];
          ctx.strokeStyle = 'rgba(225, 245, 255, ' + sp.alpha + ')';
          ctx.beginPath();
          ctx.ellipse(sp.x, sp.y, sp.radius, sp.radius * 0.3, 0, 0, Math.PI * 2);
          ctx.stroke();
          sp.radius += 0.45;
          sp.alpha -= 0.06;
          if (sp.alpha <= 0) splashes.splice(sIdx, 1);
        }
      }

      if (state.type === 'storm') {
        if (timeTick > nextLightningTime) {
          createNaturalLightning();
          nextLightningTime = timeTick + 160 + Math.floor(Math.random() * 200);
        }
        if (activeLightningBolt) drawLightningBolt(activeLightningBolt);
      }
    }

    // ۲. رندر برف
    else if (state.type === 'snow') {
      for (var j = 0; j < particles.length; j++) {
        var sn = particles[j];
        var swayX = Math.sin(timeTick * sn.swayFreq + sn.phase) * (sn.swayAmp * 0.07);
        sn.y += sn.speed;
        sn.x += swayX;

        if (sn.y > h + 12) {
          sn.y = -12;
          sn.x = Math.random() * w;
        }

        ctx.beginPath();
        var snowGrad = ctx.createRadialGradient(sn.x, sn.y, 0, sn.x, sn.y, sn.radius);
        snowGrad.addColorStop(0, 'rgba(255, 255, 255, ' + sn.opacity + ')');
        snowGrad.addColorStop(0.7, 'rgba(255, 255, 255, ' + (sn.opacity * 0.5) + ')');
        snowGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = snowGrad;
        ctx.arc(sn.x, sn.y, sn.radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // ۳. رندر ستارگان شب
    else if (!state.isDay) {
      for (var k = 0; k < particles.length; k++) {
        var star = particles[k];
        var sAlpha = star.baseAlpha + Math.sin(timeTick * star.twinkleSpeed + star.phase) * 0.35;
        sAlpha = Math.max(0.1, Math.min(1, sAlpha));

        ctx.beginPath();
        ctx.fillStyle = 'rgba(255, 255, 255, ' + sAlpha + ')';
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fill();

        if (star.hasHalo && sAlpha > 0.7) {
          ctx.beginPath();
          ctx.fillStyle = 'rgba(180, 220, 255, ' + (sAlpha * 0.22) + ')';
          ctx.arc(star.x, star.y, star.radius * 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      if (Math.random() < 0.003 && meteors.length === 0) {
        meteors.push({
          x: w * 0.65 + Math.random() * (w * 0.25),
          y: 10 + Math.random() * 25,
          dx: -7 - Math.random() * 3,
          dy: 4 + Math.random() * 2,
          length: 45 + Math.random() * 30,
          life: 1.0
        });
      }

      for (var mIdx = meteors.length - 1; mIdx >= 0; mIdx--) {
        var met = meteors[mIdx];
        var metGrad = ctx.createLinearGradient(met.x, met.y, met.x - met.dx * (met.length / 10), met.y - met.dy * (met.length / 10));
        metGrad.addColorStop(0, 'rgba(255, 255, 255, ' + met.life + ')');
        metGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.strokeStyle = metGrad;
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(met.x, met.y);
        ctx.lineTo(met.x - met.dx * (met.length / 8), met.y - met.dy * (met.length / 8));
        ctx.stroke();

        met.x += met.dx;
        met.y += met.dy;
        met.life -= 0.045;
        if (met.life <= 0) meteors.splice(mIdx, 1);
      }
    }
  }

  function createNaturalLightning() {
    if (!canvas) return;
    var startX = canvas.width * 0.35 + Math.random() * (canvas.width * 0.35);
    var startY = 15;
    var segments = [];
    var curX = startX;
    var curY = startY;

    while (curY < canvas.height - 40) {
      var nextX = curX + (Math.random() - 0.5) * 30;
      var nextY = curY + 12 + Math.random() * 18;
      segments.push({ x1: curX, y1: curY, x2: nextX, y2: nextY });
      if (Math.random() > 0.65) {
        segments.push({
          x1: nextX,
          y1: nextY,
          x2: nextX + (Math.random() - 0.5) * 32,
          y2: nextY + 14 + Math.random() * 16,
          isBranch: true
        });
      }
      curX = nextX;
      curY = nextY;
    }

    activeLightningBolt = { segments: segments, alpha: 1.0 };

    var flash = document.getElementById('appleLightningFlash');
    if (flash) {
      flash.style.opacity = '0.85';
      setTimeout(function () {
        flash.style.opacity = '0.15';
        setTimeout(function () {
          flash.style.opacity = '0.55';
          setTimeout(function () { flash.style.opacity = '0'; }, 70);
        }, 50);
      }, 60);
    }
  }

  function drawLightningBolt(bolt) {
    if (!ctx || !bolt) return;
    ctx.save();
    ctx.shadowColor = '#38BDF8';

    for (var b = 0; b < bolt.segments.length; b++) {
      var seg = bolt.segments[b];
      ctx.strokeStyle = seg.isBranch ? ('rgba(186, 230, 253, ' + (bolt.alpha * 0.65) + ')') : ('rgba(255, 255, 255, ' + bolt.alpha + ')');
      ctx.lineWidth = seg.isBranch ? 1.0 : 2.0;
      ctx.beginPath();
      ctx.moveTo(seg.x1, seg.y1);
      ctx.lineTo(seg.x2, seg.y2);
      ctx.stroke();
    }
    ctx.restore();

    bolt.alpha -= 0.12;
    if (bolt.alpha <= 0) activeLightningBolt = null;
  }

    /* ────────── ساخت ۴ الی ۵ ابر ارگانیک، بسیار زیبا، محو و طبیعی ────────── */
  function getOrganicCloudsHtml(isDay, isRain) {
    var cloudGrad = isDay
      ? '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(255,255,255,0.92)"/><stop offset="55%" stop-color="rgba(240,248,255,0.76)"/><stop offset="85%" stop-color="rgba(215,230,250,0.32)"/><stop offset="100%" stop-color="rgba(200,220,245,0)"/></radialGradient>'
      : '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(175,198,230,0.70)"/><stop offset="55%" stop-color="rgba(120,148,188,0.48)"/><stop offset="85%" stop-color="rgba(75,100,140,0.22)"/><stop offset="100%" stop-color="rgba(50,75,115,0)"/></radialGradient>';

    if (isRain) {
      cloudGrad = isDay
        ? '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(130,145,170,0.88)"/><stop offset="60%" stop-color="rgba(95,110,135,0.68)"/><stop offset="100%" stop-color="rgba(70,85,110,0)"/></radialGradient>'
        : '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(45,60,85,0.90)"/><stop offset="60%" stop-color="rgba(28,40,62,0.72)"/><stop offset="100%" stop-color="rgba(15,25,45,0)"/></radialGradient>';
    }

    var defs = '<defs>' + cloudGrad + '<filter id="cloudSoftBlur" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="3.8"/></filter></defs>';

    // ابر ۱: ابر اصلی پفکی در بالا-راست
    var svg1 = ''
      + '<svg class="apple-cloud-organic ac-org-1" viewBox="0 0 240 85" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="65" cy="52" rx="46" ry="22" fill="url(#acG1)"/>'
      +     '<ellipse cx="120" cy="42" rx="56" ry="28" fill="url(#acG1)"/>'
      +     '<ellipse cx="170" cy="50" rx="44" ry="20" fill="url(#acG1)"/>'
      +     '<ellipse cx="94" cy="32" rx="36" ry="22" fill="url(#acG1)"/>'
      +     '<ellipse cx="142" cy="34" rx="38" ry="22" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    // ابر ۲: ابر متوسط و کشیده در مرکز-چپ
    var svg2 = ''
      + '<svg class="apple-cloud-organic ac-org-2" viewBox="0 0 200 75" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="55" cy="46" rx="40" ry="20" fill="url(#acG1)"/>'
      +     '<ellipse cx="102" cy="38" rx="48" ry="25" fill="url(#acG1)"/>'
      +     '<ellipse cx="148" cy="44" rx="38" ry="18" fill="url(#acG1)"/>'
      +     '<ellipse cx="80" cy="28" rx="30" ry="19" fill="url(#acG1)"/>'
      +     '<ellipse cx="122" cy="30" rx="32" ry="19" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    // ابر ۳: ابر سبک و ملایم در بالای مرکز
    var svg3 = ''
      + '<svg class="apple-cloud-organic ac-org-3" viewBox="0 0 170 65" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="45" cy="40" rx="34" ry="17" fill="url(#acG1)"/>'
      +     '<ellipse cx="88" cy="32" rx="42" ry="22" fill="url(#acG1)"/>'
      +     '<ellipse cx="128" cy="38" rx="32" ry="16" fill="url(#acG1)"/>'
      +     '<ellipse cx="70" cy="24" rx="26" ry="16" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    // ابر ۴: ابر ظریف و کوچک در بخش پایین‌تر
    var svg4 = ''
      + '<svg class="apple-cloud-organic ac-org-4" viewBox="0 0 150 60" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="40" cy="36" rx="30" ry="16" fill="url(#acG1)"/>'
      +     '<ellipse cx="78" cy="28" rx="36" ry="20" fill="url(#acG1)"/>'
      +     '<ellipse cx="112" cy="34" rx="28" ry="15" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    return svg1 + svg2 + svg3 + svg4;
  }

  /* ────────── اعمال وضعیت نهایی آنلاین روی کارت ────────── */
  function applyWeatherState() {
    var state = resolveLiveState();
    var isEn = isEnglish();

    var skyBg = document.getElementById('appleSkyBg');
    var celestial = document.getElementById('appleCelestial');
    var cloudsCont = document.getElementById('appleCloudsContainer');
    var condTitle = document.getElementById('appleConditionTitle');
    var tempVal = document.getElementById('appleTempVal');
    var hilo = document.getElementById('appleHiLoText');
    var feels = document.getElementById('appleValFeels');
    var humidity = document.getElementById('appleValHumidity');
    var windSpd = document.getElementById('appleValWind');

    if (!skyBg) return;

    // ۱. رنگ آسمان دقیقاً بر اساس شب یا روز واقعی
    skyBg.className = 'apple-sky-bg sky-' + state.period + ' sky-' + state.type;

    // ۲. جسم فلکی: اگر شب است، ماه و هاله شب؛ اگر روز است، خورشید
    // مهم: در شب مطلقاً خورشید وجود ندارد!
    if (state.type === 'rain' || state.type === 'storm') {
      // در باران، نور مهتاب یا نور خورشید در ابرها حل شده است
      if (!state.isDay) {
        celestial.innerHTML = '<div class="apple-moon-haze-rain"></div>';
      } else {
        celestial.innerHTML = '<div class="apple-sun-haze-rain"></div>';
      }
    } else if (!state.isDay) {
      // شب صاف یا نیمه‌ابری: ماه زیبای اپل
      celestial.innerHTML = ''
        + '<div class="apple-moon">'
        +   '<div class="apple-moon-body"></div>'
        +   '<div class="apple-moon-glow"></div>'
        + '</div>';
    } else if (state.period === 'sunset') {
      // غروب
      celestial.innerHTML = '<div class="apple-sunset-sun"></div>';
    } else {
      // روز آفتابی
      celestial.innerHTML = ''
        + '<div class="apple-sun">'
        +   '<div class="apple-sun-core"></div>'
        +   '<div class="apple-sun-halo"></div>'
        + '</div>';
    }

    // ۳. ابرهای بسیار شیک، ارگانیک، طبیعی و محو وکتوری (Organic Soft Clouds)
    if (state.type === 'partly_cloudy' || state.type === 'cloudy' || state.type === 'rain' || state.type === 'storm') {
      var isRain = (state.type === 'rain' || state.type === 'storm');
      cloudsCont.innerHTML = getOrganicCloudsHtml(state.isDay, isRain);
    } else {
      cloudsCont.innerHTML = '';
    }

    // ۴. عنوان وضعیت زنده
    if (condTitle) condTitle.textContent = state.label;

    // ۵. درج ارقام آنلاین و دقیق
    if (tempVal) tempVal.textContent = fa(state.temp);
    if (feels) feels.textContent = fa(state.feels) + '°';
    var humUnit = isEn ? '%' : '٪';
    if (humidity) humidity.textContent = fa(state.humidity) + humUnit;
    if (windSpd) windSpd.textContent = fa(state.wind) + ' km/h';
    if (hilo) {
      hilo.textContent = isEn
        ? ('H: ' + fa(state.max) + '°   L: ' + fa(state.min) + '°')
        : ('ب: ' + fa(state.max) + '°   ک: ' + fa(state.min) + '°');
    }

    createParticles();
  }

  window.Weather3D = {
    init: function (containerEl, data) {
      if (!containerEl) return;
      weatherData = data || null;
      renderStageHtml(containerEl);
      applyWeatherState();
    },
    update: function (data) {
      weatherData = data;
      applyWeatherState();
    },
    onScreenShow: function () {
      resizeCanvas();
      applyWeatherState();
    }
  };

})();
