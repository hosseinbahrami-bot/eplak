import re

print("--- [1] Writing authentic Apple Weather modules/weather-3d.js ---")

apple_weather_js = """/* ============================================================
   modules/weather-3d.js — سیستم آب‌وهوای الهام‌گرفته از طراحی اپل (Apple Weather)
   - کادر کاملاً ثابت و ایستا (بدون چرخش یا لرزش)
   - هماهنگی دقیق شب و روز (در حالت باران در شب، ماه و آسمان شب حاکم است نه خورشید!)
   - ابرهای کوچک، بسیار شیک، ظریف و ارگانیک (Small, Elegant Volumetric Clouds)
   - بارش باران کریستالی و باریک (Apple Needle Rain) با پاشش آب ملایم
   - تایپوگرافی و طراحی کارت شیشه‌ای مینیمال و لوکس مشابه iOS 18
   - نوار چیپ‌های کپسولی برای تست و انتخاب وضعیت
   ============================================================ */

(function () {
  'use strict';

  var currentMode = 'auto'; // 'auto' | 'sunny' | 'night' | 'cloudy' | 'wind' | 'rain' | 'snow' | 'storm'
  var weatherData = null;
  var animFrameId = null;
  var canvas = null;
  var ctx = null;
  var particles = [];
  var splashes = [];
  var meteors = [];
  var leaves = [];
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

  // تشخیص دقیق زمان واقعی شب یا روز
  function getTimePeriod() {
    var h = new Date().getHours();
    if (h >= 5 && h < 7) return 'sunrise'; // طلوع
    if (h >= 7 && h < 18) return 'day';     // روز
    if (h >= 18 && h < 20) return 'sunset'; // غروب
    return 'night';                         // شب
  }

  // تعیین وضعیت بر اساس زمان واقعی و انتخاب کاربر
  function resolveWeatherState() {
    var currentPeriod = getTimePeriod();
    var isEn = isEnglish();

    if (currentMode === 'auto') {
      var code = (weatherData && typeof weatherData.code === 'number') ? weatherData.code : 0;
      var wind = (weatherData && typeof weatherData.wind === 'number') ? weatherData.wind : 12;
      var isWindy = wind >= 16;

      if (code >= 95) {
        return { type: 'storm', period: currentPeriod, label: isEn ? 'Thunderstorm' : 'رعد و برق' };
      } else if (code >= 71 && code <= 86) {
        return { type: 'snow', period: currentPeriod, label: isEn ? 'Snowfall' : 'بارش برف' };
      } else if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) {
        return { type: 'rain', period: currentPeriod, label: isEn ? 'Rain Showers' : 'بارش باران' };
      } else if (code === 3 || code === 45 || code === 48) {
        return { type: 'cloudy', period: currentPeriod, label: isEn ? 'Overcast' : 'ابری' };
      } else if (isWindy || code === 2) {
        return { type: 'wind', period: currentPeriod, label: isEn ? 'Breezy & Cloudy' : 'نیمه‌ابری و باد' };
      } else {
        if (currentPeriod === 'night') {
          return { type: 'clear', period: 'night', label: isEn ? 'Clear' : 'صاف و مهتابی' };
        } else if (currentPeriod === 'sunset') {
          return { type: 'clear', period: 'sunset', label: isEn ? 'Sunset' : 'غروب آفتاب' };
        } else if (currentPeriod === 'sunrise') {
          return { type: 'clear', period: 'sunrise', label: isEn ? 'Sunrise' : 'طلوع آفتاب' };
        } else {
          return { type: 'clear', period: 'day', label: isEn ? 'Sunny' : 'صاف و آفتابی' };
        }
      }
    }

    // در حالت‌های دستی: باران، برف، باد و ابر زمان واقعی کاربر را رعایت می‌کنند!
    // یعنی اگر الان شب است، باران در شب اتفاق می‌افتد نه با خورشید روز!
    switch (currentMode) {
      case 'sunny':
        return { type: 'clear', period: 'day', label: isEn ? 'Sunny' : 'صاف و آفتابی' };
      case 'night':
        return { type: 'clear', period: 'night', label: isEn ? 'Clear Sky' : 'صاف و مهتابی' };
      case 'cloudy':
        return { type: 'cloudy', period: currentPeriod, label: isEn ? 'Mostly Cloudy' : 'ابری' };
      case 'wind':
        return { type: 'wind', period: currentPeriod, label: isEn ? 'Windy' : 'وزش باد' };
      case 'rain':
        // کاملاً متناسب با زمان واقعی: شب با آسمان شب، روز با آسمان روز
        return { type: 'rain', period: currentPeriod, label: isEn ? 'Rain' : 'بارش باران' };
      case 'snow':
        return { type: 'snow', period: currentPeriod, label: isEn ? 'Snow' : 'بارش برف' };
      case 'storm':
        return { type: 'storm', period: currentPeriod, label: isEn ? 'Thunderstorm' : 'طوفان و آذرخش' };
      default:
        return { type: 'clear', period: currentPeriod, label: isEn ? 'Clear' : 'صاف' };
    }
  }

  /* ────────── ساخت قالب کارت آب‌وهوای اپل (Apple Weather) ────────── */
  function renderStageHtml(container) {
    var isEn = isEnglish();
    var html = ''
      + '<div class="apple-weather-wrap">'
      +   '<!-- نوار چیپ‌های کپسولی اپل برای انتخاب سریع وضعیت -->'
      +   '<div class="apple-chips-scroll">'
      +     '<div class="apple-chips">'
      +       '<button class="apple-chip' + (currentMode === 'auto' ? ' active' : '') + '" data-mode="auto" type="button"><span class="apple-chip-dot"></span>' + (isEn ? 'Live' : 'خودکار') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'sunny' ? ' active' : '') + '" data-mode="sunny" type="button">☀️ ' + (isEn ? 'Sunny' : 'آفتابی') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'night' ? ' active' : '') + '" data-mode="night" type="button">🌙 ' + (isEn ? 'Moon' : 'شب') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'cloudy' ? ' active' : '') + '" data-mode="cloudy" type="button">☁️ ' + (isEn ? 'Cloudy' : 'ابری') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'wind' ? ' active' : '') + '" data-mode="wind" type="button">💨 ' + (isEn ? 'Wind' : 'باد') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'rain' ? ' active' : '') + '" data-mode="rain" type="button">🌧️ ' + (isEn ? 'Rain' : 'باران') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'snow' ? ' active' : '') + '" data-mode="snow" type="button">❄️ ' + (isEn ? 'Snow' : 'برف') + '</button>'
      +       '<button class="apple-chip' + (currentMode === 'storm' ? ' active' : '') + '" data-mode="storm" type="button">⚡ ' + (isEn ? 'Storm' : 'طوفان') + '</button>'
      +     '</div>'
      +   '</div>'
      +   '<!-- کادر اصلی اپل ودر: کاملاً ثابت و بدون چرخش (Rock-Solid Frame) -->'
      +   '<div class="apple-weather-card" id="appleWeatherCard">'
      +     '<!-- پس‌زمینه رنگ آسمان با گرادینت اتمسفریک پیوسته -->'
      +     '<div class="apple-sky-bg" id="appleSkyBg"></div>'
      +     '<div class="apple-sky-haze"></div>'
      +     '<!-- جسم فلکی (خورشید ملایم اپل، ماه شب با هاله نرم) -->'
      +     '<div class="apple-celestial" id="appleCelestial"></div>'
      +     '<!-- ابرهای کوچک، ظریف و ارگانیک اپل -->'
      +     '<div class="apple-clouds-container" id="appleCloudsContainer"></div>'
      +     '<!-- کانواس پدیده‌ها: باران سوزنی باریک، برف پفکی، ستارگان و صاعقه -->'
      +     '<canvas class="apple-canvas" id="appleCanvas"></canvas>'
      +     '<div class="apple-lightning-flash" id="appleLightningFlash"></div>'
      +     '<!-- لایه شیشه‌ای و اطلاعات اپل ودر (Apple Weather HUD) -->'
      +     '<div class="apple-hud">'
      +       '<div class="apple-hud-top">'
      +         '<div class="apple-city-badge">'
      +           '<span class="apple-radar-dot"></span>'
      +           '<span class="apple-city-name" id="appleCityName">ورامین</span>'
      +         '</div>'
      +         '<div class="apple-time-pill" id="appleTimePill">ایستگاه زنده</div>'
      +       '</div>'
      +       '<div class="apple-hud-center">'
      +         '<div class="apple-temp-row">'
      +           '<span class="apple-temp-val" id="appleTempVal">۲۴</span>'
      +           '<span class="apple-temp-deg">°</span>'
      +         '</div>'
      +         '<div class="apple-condition-title" id="appleConditionTitle">صاف و مهتابی</div>'
      +         '<div class="apple-hilo-text" id="appleHiLoText">بیشینه ۲۸° / کمینه ۱۶°</div>'
      +       '</div>'
      +       '<!-- کپسول شیشه‌ای یکپارچه پایین کادر مشابه اپل ودر -->'
      +       '<div class="apple-hud-bar">'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">احساس</span>'
      +           '<span class="apple-bar-val" id="appleValFeels">۲۳°</span>'
      +         '</div>'
      +         '<div class="apple-bar-divider"></div>'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">رطوبت</span>'
      +           '<span class="apple-bar-val" id="appleValHumidity">۴۲٪</span>'
      +         '</div>'
      +         '<div class="apple-bar-divider"></div>'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">باد</span>'
      +           '<span class="apple-bar-val" id="appleValWind">۱۸ km/h</span>'
      +         '</div>'
      +         '<div class="apple-bar-divider"></div>'
      +         '<div class="apple-bar-item">'
      +           '<span class="apple-bar-label">دید افقی</span>'
      +           '<span class="apple-bar-val" id="appleValVisibility">۱۰ km</span>'
      +         '</div>'
      +       '</div>'
      +     '</div>'
      +   '</div>'
      + '</div>';

    container.innerHTML = html;
    bindChipEvents(container);
    initCanvas();
  }

  function bindChipEvents(container) {
    var chips = container.querySelectorAll('.apple-chip');
    chips.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var mode = btn.getAttribute('data-mode');
        chips.forEach(function (c) { c.classList.remove('active'); });
        btn.classList.add('active');
        currentMode = mode;
        applyWeatherState();
      });
    });
  }

  /* ────────── راه‌اندازی کانواس گرافیکی ۶۰ فریم ────────── */
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
    var h = (rect && rect.height > 50) ? rect.height : (canvas.parentElement ? canvas.parentElement.offsetHeight : 246);
    if (w > 0 && h > 0 && (canvas.width !== Math.floor(w) || canvas.height !== Math.floor(h))) {
      canvas.width = Math.floor(w);
      canvas.height = Math.floor(h);
      createParticles();
    }
  }

  /* ────────── ایجاد ذرات بسیار ظریف و طبیعی (Apple-Grade) ────────── */
  function createParticles() {
    particles = [];
    splashes = [];
    meteors = [];
    leaves = [];
    var state = resolveWeatherState();
    var w = canvas ? canvas.width : 350;
    var h = canvas ? canvas.height : 246;

    // ۱. باران فوق‌العاده ظریف و شیک (Apple Needle Rain)
    if (state.type === 'rain' || state.type === 'storm') {
      var rainCount = state.type === 'storm' ? 75 : 48;
      for (var i = 0; i < rainCount; i++) {
        var d = Math.random();
        particles.push({
          x: Math.random() * (w + 40) - 20,
          y: Math.random() * h,
          depth: d,
          speed: 13 + d * 11, // سرعت سقوط طبیعی
          len: 10 + d * 12,   // طول ظریف و باریک (کوچک و سوزنی)
          width: 0.75 + d * 0.4, // عرض فوق‌العاده نازک و سوزنی
          opacity: 0.35 + d * 0.45,
          windAngle: -2.2 - Math.random() * 1.5
        });
      }
    }
    // ۲. برف لطیف و بلورین
    else if (state.type === 'snow') {
      var snowCount = 45;
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
    // ۳. برگ‌های معلق پاییزی در باد
    else if (state.type === 'wind') {
      var leafCount = 5;
      for (var l = 0; l < leafCount; l++) {
        leaves.push({
          x: Math.random() * w,
          y: 20 + Math.random() * (h - 70),
          size: 11 + Math.random() * 7,
          speedX: -2.4 - Math.random() * 2.8,
          speedY: 0.3 + Math.random() * 0.6,
          rotation: Math.random() * Math.PI * 2,
          rotSpeed: 0.03 + Math.random() * 0.04,
          flip: Math.random() * Math.PI,
          flipSpeed: 0.04 + Math.random() * 0.05,
          color: Math.random() > 0.5 ? '#EA580C' : '#F59E0B'
        });
      }
    }
    // ۴. ستارگان درخشان شب
    else if (state.period === 'night' || currentMode === 'night') {
      var starCount = 45;
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
    // ۵. روز آفتابی: ذرات گرد طلایی معلق در نور خورشید
    else if (state.period === 'day' && state.type === 'clear') {
      var moteCount = 20;
      for (var m = 0; m < moteCount; m++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          radius: 0.7 + Math.random() * 1.2,
          speedY: -0.2 - Math.random() * 0.35,
          sway: 0.02 + Math.random() * 0.03,
          phase: Math.random() * Math.PI * 2,
          opacity: 0.2 + Math.random() * 0.4
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

  /* ────────── رندر فیزیک کانواس با بالاترین کیفیت ────────── */
  function drawScene() {
    if (!ctx || !canvas) return;
    var w = canvas.width;
    var h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    var state = resolveWeatherState();

    // ۱. رندر باران ظریف اپل با حلقه‌های ریز پاشش
    if (state.type === 'rain' || state.type === 'storm') {
      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        ctx.strokeStyle = state.type === 'storm'
          ? 'rgba(210, 235, 255, ' + p.opacity + ')'
          : 'rgba(225, 245, 255, ' + p.opacity + ')';
        ctx.lineWidth = p.width;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x + p.windAngle, p.y + p.len);
        ctx.stroke();

        p.y += p.speed;
        p.x += (p.windAngle * (p.speed / 16));

        // پاشش ریز در برخورد با پایین کارت
        if (p.y > h - 14) {
          if (p.depth > 0.45 && Math.random() > 0.65) {
            splashes.push({
              x: p.x,
              y: h - 8 + Math.random() * 5,
              radius: 0.8,
              maxRadius: 2.2 + p.depth * 3.5,
              alpha: 0.55
            });
          }
          p.y = -18;
          p.x = Math.random() * (w + 40) - 10;
        }
      }

      // حلقه‌های پاشش ظریف آب
      for (var sIdx = splashes.length - 1; sIdx >= 0; sIdx--) {
        var sp = splashes[sIdx];
        ctx.strokeStyle = 'rgba(225, 245, 255, ' + sp.alpha + ')';
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.ellipse(sp.x, sp.y, sp.radius, sp.radius * 0.32, 0, 0, Math.PI * 2);
        ctx.stroke();
        sp.radius += 0.4;
        sp.alpha -= 0.055;
        if (sp.alpha <= 0) splashes.splice(sIdx, 1);
      }

      // آذرخش طبیعی
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

    // ۳. رندر برگ‌های باد
    else if (state.type === 'wind') {
      for (var lIdx = 0; lIdx < leaves.length; lIdx++) {
        var lf = leaves[lIdx];
        lf.x += lf.speedX;
        lf.y += Math.sin(timeTick * 0.04 + lIdx) * 0.7 + lf.speedY;
        lf.rotation += lf.rotSpeed;
        lf.flip += lf.flipSpeed;

        if (lf.x < -30) {
          lf.x = w + 30;
          lf.y = 20 + Math.random() * (h - 70);
        }

        ctx.save();
        ctx.translate(lf.x, lf.y);
        ctx.rotate(lf.rotation);
        ctx.scale(Math.cos(lf.flip), 1);
        ctx.fillStyle = lf.color;
        ctx.beginPath();
        ctx.moveTo(0, -lf.size * 0.5);
        ctx.quadraticCurveTo(lf.size * 0.5, 0, 0, lf.size * 0.5);
        ctx.quadraticCurveTo(-lf.size * 0.5, 0, 0, -lf.size * 0.5);
        ctx.fill();
        ctx.restore();
      }
    }

    // ۴. رندر ستارگان شب و شهاب‌سنگ
    else if (state.period === 'night' || currentMode === 'night') {
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

    // ۵. روز آفتابی
    else if (state.period === 'day' && state.type === 'clear') {
      for (var dIdx = 0; dIdx < particles.length; dIdx++) {
        var mote = particles[dIdx];
        mote.y += mote.speedY;
        mote.x += Math.sin(timeTick * mote.sway + mote.phase) * 0.25;
        if (mote.y < -8) {
          mote.y = h + 8;
          mote.x = Math.random() * w;
        }
        ctx.beginPath();
        ctx.fillStyle = 'rgba(255, 240, 180, ' + mote.opacity + ')';
        ctx.arc(mote.x, mote.y, mote.radius, 0, Math.PI * 2);
        ctx.fill();
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
    ctx.shadowBlur = 12;

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

  /* ────────── اعمال المان‌های ظریف و شیک اپل ────────── */
  function applyWeatherState() {
    var state = resolveWeatherState();
    var isEn = isEnglish();

    var skyBg = document.getElementById('appleSkyBg');
    var celestial = document.getElementById('appleCelestial');
    var cloudsCont = document.getElementById('appleCloudsContainer');
    var condTitle = document.getElementById('appleConditionTitle');
    var timePill = document.getElementById('appleTimePill');
    var tempVal = document.getElementById('appleTempVal');
    var hilo = document.getElementById('appleHiLoText');
    var feels = document.getElementById('appleValFeels');
    var humidity = document.getElementById('appleValHumidity');
    var windSpd = document.getElementById('appleValWind');
    var visibility = document.getElementById('appleValVisibility');

    if (!skyBg) return;

    // ۱. رنگ آسمان اپل (طبیعی، غنی و هماهنگ با شب یا روز)
    skyBg.className = 'apple-sky-bg sky-' + state.period + ' sky-' + state.type;

    // ۲. جسم فلکی: فقط در شرایط بدون باران یا بدون طوفان سنگین نمایش داده می‌شود
    // مهم: در شب بارانی، مطلقاً خورشید وجود ندارد!
    if (state.type === 'rain' || state.type === 'storm') {
      // در باران، ابرهای بارانی متراکم جلوی خورشید و ماه را می‌پوشانند
      if (state.period === 'night') {
        // در شب بارانی، تنها یک هاله بسیار ملایم ماه در میان ابرها حس می‌شود
        celestial.innerHTML = '<div class="apple-moon-haze-rain"></div>';
      } else {
        // در روز بارانی، تنها روشنایی ملایم افق بدون خورشید مستقیم
        celestial.innerHTML = '<div class="apple-sun-haze-rain"></div>';
      }
    } else if (state.period === 'night' || currentMode === 'night' || state.type === 'snow') {
      // شب صاف یا برف در شب: ماه زیبای اپل با دهانه‌ها و هاله نقره‌ای
      celestial.innerHTML = ''
        + '<div class="apple-moon">'
        +   '<div class="apple-moon-body"></div>'
        +   '<div class="apple-moon-glow"></div>'
        + '</div>';
    } else if (state.period === 'sunset') {
      // غروب
      celestial.innerHTML = '<div class="apple-sunset-sun"></div>';
    } else {
      // روز آفتابی: خورشید درخشان و ملایم اپل
      celestial.innerHTML = ''
        + '<div class="apple-sun">'
        +   '<div class="apple-sun-core"></div>'
        +   '<div class="apple-sun-halo"></div>'
        + '</div>';
    }

    // ۳. ابرهای کوچک، بسیار شیک، ظریف و ارگانیک اپل (Small, Elegant Clouds)
    // برخلاف ابرهای بزرگ و مستطیلی قبلی، این ابرها کوچک، منحنی و پفکی هستند
    if (state.type === 'cloudy' || state.type === 'wind' || state.type === 'rain' || state.type === 'storm') {
      var isDark = (state.type === 'storm' || state.type === 'rain');
      var isNight = (state.period === 'night');
      var cloudClass = isDark ? (isNight ? ' night-rain-cloud' : ' day-rain-cloud') : (isNight ? ' night-cloud' : ' day-cloud');

      cloudsCont.innerHTML = ''
        + '<div class="apple-cloud ac-1 ' + cloudClass + '"></div>'
        + '<div class="apple-cloud ac-2 ' + cloudClass + '"></div>'
        + '<div class="apple-cloud ac-3 ' + cloudClass + '"></div>';
    } else if (state.period === 'day' && state.type === 'clear') {
      // در روز آفتابی، فقط یک ابر کوچک و سبک در دوردست
      cloudsCont.innerHTML = '<div class="apple-cloud ac-distant day-cloud"></div>';
    } else {
      cloudsCont.innerHTML = '';
    }

    // ۴. متن و عنوان وضعیت
    if (condTitle) condTitle.textContent = state.label;

    if (timePill) {
      var periodLabels = {
        sunrise: isEn ? 'Sunrise' : 'طلوع آفتاب',
        day: isEn ? 'Day' : 'روز',
        sunset: isEn ? 'Sunset' : 'غروب',
        night: isEn ? 'Night' : 'شب'
      };
      timePill.textContent = periodLabels[state.period] || (isEn ? 'Live' : 'ایستگاه زنده');
    }

    // ۵. مقادیر دما و متریک‌ها
    var t = 24, fl = 23, hm = 42, wd = 18, hi = 28, lo = 16, vis = 10;
    if (weatherData) {
      if (typeof weatherData.temp === 'number') t = Math.round(weatherData.temp);
      if (typeof weatherData.feels === 'number') fl = Math.round(weatherData.feels);
      if (typeof weatherData.humidity === 'number') hm = Math.round(weatherData.humidity);
      if (typeof weatherData.wind === 'number') wd = Math.round(weatherData.wind);
      if (typeof weatherData.max === 'number') hi = Math.round(weatherData.max);
      if (typeof weatherData.min === 'number') lo = Math.round(weatherData.min);
    }

    if (currentMode === 'snow') { t = -2; fl = -5; hm = 84; wd = 12; hi = 1; lo = -6; vis = 4; }
    if (currentMode === 'storm') { t = 16; fl = 14; hm = 89; wd = 45; hi = 20; lo = 14; vis = 6; }
    if (currentMode === 'rain') { t = 17; fl = 15; hm = 84; wd = 20; hi = 19; lo = 13; vis = 8; }
    if (currentMode === 'night' && !weatherData) { t = 18; fl = 17; hm = 54; wd = 10; hi = 27; lo = 15; vis = 10; }
    if (currentMode === 'wind') { t = 20; fl = 19; hm = 45; wd = 32; hi = 24; lo = 14; vis = 10; }

    if (tempVal) tempVal.textContent = fa(t);
    if (feels) feels.textContent = fa(fl) + '°';
    var humUnit = isEn ? '%' : '٪';
    if (humidity) humidity.textContent = fa(hm) + humUnit;
    if (windSpd) windSpd.textContent = fa(wd) + ' km/h';
    if (visibility) visibility.textContent = fa(vis) + ' km';
    if (hilo) {
      hilo.textContent = isEn
        ? ('H: ' + fa(hi) + '°   L: ' + fa(lo) + '°')
        : ('ب: ' + fa(hi) + '°   ک: ' + fa(lo) + '°');
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
    setMode: function (mode) {
      currentMode = mode;
      applyWeatherState();
    },
    onScreenShow: function () {
      resizeCanvas();
      applyWeatherState();
    }
  };

})();
"""

with open('/home/user/eplak/eplak-fixed/modules/weather-3d.js', 'w', encoding='utf-8') as f:
    f.write(apple_weather_js)

print("   -> modules/weather-3d.js successfully rewritten!")
