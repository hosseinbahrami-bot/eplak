import re

print("[1] Writing hyper-realistic, 100% stable modules/weather-3d.js ...")

weather_js = """/* ============================================================
   modules/weather-3d.js — سیستم آب‌وهوای اتمسفریک و واقع‌گرایانه پیشخوان
   - کادر کاملاً ثابت و مستحکم (بدون چرخش یا پرش کادر)
   - شبیه‌سازی فوق‌العاده طبیعی آسمان و پدیده‌های جوی:
     * روز آفتابی: خورشید درخشان، پرتوهای نور خورشید (God Rays) و ذرات طلایی معلق
     * شب مهتابی: ماه طبیعی با جزئیات، هاله نورانی، ستارگان چندعمقی چشمک‌زن و شهاب‌های گاه‌به‌گاه
     * غروب: طیف ارغوانی و نارنجی با افق ملتهب
     * ابر و باد: ابرهای چندلایه با سایه‌روشن طبیعی، جریان‌های باد و برگ‌های پاییزی معلق در هوا
     * باران: قطرات مورب، اثر برخورد و پاشش قطرات (Splash Rings) و مه ملایم کف
     * برف: دانه‌های بلورین چندعمقی (Bokeh Foreground & Sharp Midground) با نوسان ملایم باد
     * طوفان: ابرهای متراکم باردار و شاخه‌های آذرخش واقعی (Branching Lightning Bolts)
   - نوار چیپ‌های کپسولی شیشه‌ای برای تست سریع کلیه حالت‌ها
   - بهینه‌سازی دقیق ۶۰ فریم با خاموشی خودکار در صفحات دیگر
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

  function getTimePeriod() {
    var h = new Date().getHours();
    if (h >= 5 && h < 7) return 'sunrise'; // طلوع
    if (h >= 7 && h < 18) return 'day';     // روز
    if (h >= 18 && h < 20) return 'sunset'; // غروب
    return 'night';                         // شب
  }

  function resolveWeatherState() {
    var period = getTimePeriod();
    var isEn = isEnglish();

    if (currentMode === 'auto') {
      var code = (weatherData && typeof weatherData.code === 'number') ? weatherData.code : 0;
      var wind = (weatherData && typeof weatherData.wind === 'number') ? weatherData.wind : 14;
      var isWindy = wind >= 16;

      if (code >= 95) {
        return { type: 'storm', period: period, label: isEn ? 'Thunderstorm' : 'رعد و برق و طوفان' };
      } else if (code >= 71 && code <= 86) {
        return { type: 'snow', period: period, label: isEn ? 'Snowfall' : 'بارش آرام برف' };
      } else if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) {
        return { type: 'rain', period: period, label: isEn ? 'Rainy' : 'بارش باران بهاری' };
      } else if (code === 3 || code === 45 || code === 48) {
        return { type: 'cloudy', period: period, label: isEn ? 'Overcast Sky' : 'هوای ابری و مه‌آلود' };
      } else if (isWindy || code === 2) {
        return { type: 'wind', period: period, label: isEn ? 'Breezy & Cloudy' : 'نیمه‌ابری همراه با وزش باد' };
      } else {
        if (period === 'night') {
          return { type: 'clear', period: 'night', label: isEn ? 'Clear & Starry Night' : 'صاف و مهتابی' };
        } else if (period === 'sunset') {
          return { type: 'clear', period: 'sunset', label: isEn ? 'Sunset Glow' : 'غروب زرین و دل‌انگیز' };
        } else if (period === 'sunrise') {
          return { type: 'clear', period: 'sunrise', label: isEn ? 'Morning Dawn' : 'طلوع باطراوت آفتاب' };
        } else {
          return { type: 'clear', period: 'day', label: isEn ? 'Sunny & Clear' : 'آفتابی و درخشان' };
        }
      }
    }

    switch (currentMode) {
      case 'sunny':
        return { type: 'clear', period: 'day', label: isEn ? 'Sunny & Clear' : 'آفتابی و درخشان' };
      case 'night':
        return { type: 'clear', period: 'night', label: isEn ? 'Clear & Starry Night' : 'شب مهتابی و پرستاره' };
      case 'cloudy':
        return { type: 'cloudy', period: 'day', label: isEn ? 'Overcast & Soft Clouds' : 'ابرهای ملایم پاییزی' };
      case 'wind':
        return { type: 'wind', period: 'day', label: isEn ? 'Autumn Breeze & Leaves' : 'وزش باد و برگ‌های پاییزی' };
      case 'rain':
        return { type: 'rain', period: 'day', label: isEn ? 'Atmospheric Rain' : 'بارش دل‌نشین باران' };
      case 'snow':
        return { type: 'snow', period: 'night', label: isEn ? 'Gentle Snowfall' : 'بارش بلورهای برف زمستانی' };
      case 'storm':
        return { type: 'storm', period: 'night', label: isEn ? 'Thunderstorm & Lightning' : 'طوفان سهمگین و آذرخش' };
      default:
        return { type: 'clear', period: period, label: isEn ? 'Pleasant Weather' : 'هوای صاف و دلپذیر' };
    }
  }

  /* ────────── ساخت ساختار HTML استیج طبیعی ────────── */
  function renderStageHtml(container) {
    var isEn = isEnglish();
    var html = ''
      + '<div class="w3d-wrap">'
      +   '<!-- نوار چیپ‌های کپسولی برای تست آسان تمامی شرایط آب‌وهوا -->'
      +   '<div class="w3d-chips-scroll">'
      +     '<div class="w3d-chips">'
      +       '<button class="w3d-chip' + (currentMode === 'auto' ? ' active' : '') + '" data-mode="auto" type="button"><span class="w3d-chip-icon">🌐</span> ' + (isEn ? 'Live' : 'خودکار') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'sunny' ? ' active' : '') + '" data-mode="sunny" type="button"><span class="w3d-chip-icon">☀️</span> ' + (isEn ? 'Sunny' : 'آفتابی') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'night' ? ' active' : '') + '" data-mode="night" type="button"><span class="w3d-chip-icon">🌙</span> ' + (isEn ? 'Moon' : 'شب مهتابی') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'cloudy' ? ' active' : '') + '" data-mode="cloudy" type="button"><span class="w3d-chip-icon">☁️</span> ' + (isEn ? 'Cloudy' : 'ابری') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'wind' ? ' active' : '') + '" data-mode="wind" type="button"><span class="w3d-chip-icon">💨</span> ' + (isEn ? 'Wind' : 'وزش باد') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'rain' ? ' active' : '') + '" data-mode="rain" type="button"><span class="w3d-chip-icon">🌧️</span> ' + (isEn ? 'Rain' : 'باران') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'snow' ? ' active' : '') + '" data-mode="snow" type="button"><span class="w3d-chip-icon">❄️</span> ' + (isEn ? 'Snow' : 'برف') + '</button>'
      +       '<button class="w3d-chip' + (currentMode === 'storm' ? ' active' : '') + '" data-mode="storm" type="button"><span class="w3d-chip-icon">⚡</span> ' + (isEn ? 'Storm' : 'طوفان') + '</button>'
      +     '</div>'
      +   '</div>'
      +   '<!-- کادر استیج طبیعی و ثابت (کاملاً فیکس و بدون لرزش) -->'
      +   '<div class="w3d-stage-fixed" id="w3dStage">'
      +     '<!-- پس‌زمینه رنگ آسمان و اتمسفر -->'
      +     '<div class="w3d-sky-canvas" id="w3dSkyBg"></div>'
      +     '<div class="w3d-horizon-glow"></div>'
      +     '<!-- جسم فلکی واقع‌گرایانه (خورشید اتمسفریک یا ماه واقعی) -->'
      +     '<div class="w3d-celestial-stage" id="w3dCelestial"></div>'
      +     '<!-- ابرهای حجمی طبیعی با پرتوهای نور -->'
      +     '<div class="w3d-cloud-stage" id="w3dCloudsStage"></div>'
      +     '<!-- کانواس رندر پدیده‌ها: قطرات باران، پاشش، دانه‌های برف، ستارگان و رعدوبرق -->'
      +     '<canvas class="w3d-fx-canvas" id="w3dCanvas"></canvas>'
      +     '<!-- فلاش صاعقه اتمسفریک -->'
      +     '<div class="w3d-ambient-flash" id="w3dLightningFlash"></div>'
      +     '<!-- لایه شیشه‌ای و خوانای اطلاعات آب‌وهوا (طراحی مدرن اپل ودر) -->'
      +     '<div class="w3d-glass-hud">'
      +       '<div class="w3d-hud-header">'
      +         '<div class="w3d-location-pill">'
      +           '<span class="w3d-radar-dot"></span>'
      +           '<span id="w3dHudTimeTag">ورامین • ایستگاه زنده</span>'
      +         '</div>'
      +         '<div class="w3d-condition-badge" id="w3dHudCondition">صاف و آفتابی</div>'
      +       '</div>'
      +       '<div class="w3d-hud-center">'
      +         '<div class="w3d-temp-main">'
      +           '<span class="w3d-temp-val" id="w3dHudTemp">۲۴</span>'
      +           '<span class="w3d-temp-unit">°</span>'
      +         '</div>'
      +         '<div class="w3d-temp-sub" id="w3dHudHiLo">بیشینه ۲۸° / کمینه ۱۶°</div>'
      +       '</div>'
      +       '<div class="w3d-hud-pills">'
      +         '<div class="w3d-metric-capsule">'
      +           '<span class="w3d-m-icon">🌡️</span>'
      +           '<span class="w3d-m-label">' + (isEn ? 'Feels' : 'احساس') + '</span>'
      +           '<span class="w3d-m-val" id="w3dHudFeels">۲۳°</span>'
      +         '</div>'
      +         '<div class="w3d-metric-capsule">'
      +           '<span class="w3d-m-icon">💧</span>'
      +           '<span class="w3d-m-label">' + (isEn ? 'Humidity' : 'رطوبت') + '</span>'
      +           '<span class="w3d-m-val" id="w3dHudHumidity">۴۲٪</span>'
      +         '</div>'
      +         '<div class="w3d-metric-capsule">'
      +           '<span class="w3d-m-icon">💨</span>'
      +           '<span class="w3d-m-label">' + (isEn ? 'Wind' : 'سرعت باد') + '</span>'
      +           '<span class="w3d-m-val" id="w3dHudWind">۱۸ km/h</span>'
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
    var chips = container.querySelectorAll('.w3d-chip');
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

  /* ────────── راه‌اندازی کانواس گرافیکی ────────── */
  function initCanvas() {
    canvas = document.getElementById('w3dCanvas');
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
    var h = (rect && rect.height > 50) ? rect.height : (canvas.parentElement ? canvas.parentElement.offsetHeight : 240);
    if (w > 0 && h > 0 && (canvas.width !== Math.floor(w) || canvas.height !== Math.floor(h))) {
      canvas.width = Math.floor(w);
      canvas.height = Math.floor(h);
      createParticles();
    }
  }

  /* ────────── ایجاد ذرات طبیعی متناسب با شرایط جوی ────────── */
  function createParticles() {
    particles = [];
    splashes = [];
    meteors = [];
    leaves = [];
    var state = resolveWeatherState();
    var w = canvas ? canvas.width : 350;
    var h = canvas ? canvas.height : 240;

    // باران
    if (state.type === 'rain' || state.type === 'storm') {
      var rainCount = state.type === 'storm' ? 85 : 55;
      for (var i = 0; i < rainCount; i++) {
        var depth = Math.random(); // 0: دور و محو، 1: نزدیک و سریع
        particles.push({
          x: Math.random() * (w + 60) - 30,
          y: Math.random() * h,
          depth: depth,
          speed: 12 + depth * 14,
          len: 14 + depth * 18,
          width: 0.8 + depth * 1.2,
          opacity: 0.35 + depth * 0.45,
          windAngle: -3.5 - Math.random() * 2
        });
      }
    }
    // برف زمستانی چندلایه با افکت عمق بوکه
    else if (state.type === 'snow') {
      var snowCount = 55;
      for (var j = 0; j < snowCount; j++) {
        var sDepth = Math.random();
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          depth: sDepth,
          radius: sDepth > 0.85 ? (4 + Math.random() * 3) : (1.2 + sDepth * 2.8),
          speed: 0.7 + sDepth * 1.5,
          swayAmp: 10 + sDepth * 20,
          swayFreq: 0.015 + Math.random() * 0.02,
          phase: Math.random() * Math.PI * 2,
          opacity: sDepth > 0.85 ? 0.35 : (0.5 + sDepth * 0.4),
          blur: sDepth > 0.85
        });
      }
    }
    // وزش باد و برگ‌های معلق
    else if (state.type === 'wind') {
      var leafCount = 7;
      for (var l = 0; l < leafCount; l++) {
        leaves.push({
          x: Math.random() * w,
          y: 20 + Math.random() * (h - 70),
          size: 14 + Math.random() * 10,
          speedX: -2.5 - Math.random() * 3.5,
          speedY: 0.4 + Math.random() * 0.8,
          rotation: Math.random() * Math.PI * 2,
          rotSpeed: 0.03 + Math.random() * 0.05,
          flip: Math.random() * Math.PI,
          flipSpeed: 0.04 + Math.random() * 0.06,
          color: Math.random() > 0.5 ? '#E65100' : (Math.random() > 0.5 ? '#F57C00' : '#FFB300')
        });
      }
    }
    // شب مهتابی و پرستاره
    else if (state.period === 'night' || currentMode === 'night') {
      var starCount = 50;
      for (var k = 0; k < starCount; k++) {
        var stDepth = Math.random();
        particles.push({
          x: Math.random() * w,
          y: Math.random() * (h * 0.75),
          radius: 0.6 + stDepth * 1.4,
          twinkleSpeed: 0.02 + Math.random() * 0.04,
          phase: Math.random() * Math.PI * 2,
          baseAlpha: 0.3 + stDepth * 0.6,
          hasHalo: stDepth > 0.85
        });
      }
    }
    // روز آفتابی: ذرات گرد طلایی معلق در نور (Dust Motes / Sunbeams)
    else if (state.period === 'day' && state.type === 'clear') {
      var moteCount = 25;
      for (var m = 0; m < moteCount; m++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          radius: 0.8 + Math.random() * 1.5,
          speedY: -0.2 - Math.random() * 0.4,
          sway: 0.02 + Math.random() * 0.03,
          phase: Math.random() * Math.PI * 2,
          opacity: 0.2 + Math.random() * 0.5
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

  /* ────────── موتور رندر فیزیک طبیعی کانواس ────────── */
  function drawScene() {
    if (!ctx || !canvas) return;
    var w = canvas.width;
    var h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    var state = resolveWeatherState();

    // ۱. رندر باران واقعی همراه با حلقه پاشش قطرات (Splash Rings)
    if (state.type === 'rain' || state.type === 'storm') {
      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        ctx.strokeStyle = state.type === 'storm' ? 'rgba(215, 235, 255, ' + p.opacity + ')' : 'rgba(225, 245, 255, ' + p.opacity + ')';
        ctx.lineWidth = p.width;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x + p.windAngle, p.y + p.len);
        ctx.stroke();

        p.y += p.speed;
        p.x += (p.windAngle * (p.speed / 16));

        // برخورد به پایین و ایجاد اثر پاشش
        if (p.y > h - 15) {
          if (p.depth > 0.4 && Math.random() > 0.6) {
            splashes.push({
              x: p.x,
              y: h - 10 + Math.random() * 6,
              radius: 1,
              maxRadius: 3 + p.depth * 5,
              alpha: 0.6
            });
          }
          p.y = -20;
          p.x = Math.random() * (w + 60) - 20;
        }
      }

      // رسم و محو شدن حلقه‌های پاشش قطرات
      for (var sIdx = splashes.length - 1; sIdx >= 0; sIdx--) {
        var sp = splashes[sIdx];
        ctx.strokeStyle = 'rgba(225, 245, 255, ' + sp.alpha + ')';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.ellipse(sp.x, sp.y, sp.radius, sp.radius * 0.35, 0, 0, Math.PI * 2);
        ctx.stroke();
        sp.radius += 0.5;
        sp.alpha -= 0.05;
        if (sp.alpha <= 0) {
          splashes.splice(sIdx, 1);
        }
      }

      // مدیریت آذرخش و رعدوبرق در طوفان
      if (state.type === 'storm') {
        if (timeTick > nextLightningTime) {
          createNaturalLightning();
          nextLightningTime = timeTick + 150 + Math.floor(Math.random() * 220);
        }
        if (activeLightningBolt) {
          drawLightningBolt(activeLightningBolt);
        }
      }
    }

    // ۲. رندر برف سه‌بعدی با عمق میدان
    else if (state.type === 'snow') {
      for (var j = 0; j < particles.length; j++) {
        var sn = particles[j];
        var swayX = Math.sin(timeTick * sn.swayFreq + sn.phase) * (sn.swayAmp * 0.08);
        sn.y += sn.speed;
        sn.x += swayX;

        if (sn.y > h + 15) {
          sn.y = -15;
          sn.x = Math.random() * w;
        }

        ctx.beginPath();
        var snowGrad = ctx.createRadialGradient(sn.x, sn.y, 0, sn.x, sn.y, sn.radius);
        snowGrad.addColorStop(0, 'rgba(255, 255, 255, ' + sn.opacity + ')');
        snowGrad.addColorStop(0.7, 'rgba(255, 255, 255, ' + (sn.opacity * 0.6) + ')');
        snowGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = snowGrad;
        ctx.arc(sn.x, sn.y, sn.radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // ۳. رندر وزش باد و برگ‌های معلق پاییزی
    else if (state.type === 'wind') {
      // خطوط روان باد
      var windPhase = (timeTick * 0.03) % (Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      var yStream1 = 55 + Math.sin(windPhase) * 6;
      ctx.moveTo(w + 30 - ((timeTick * 4) % (w + 100)), yStream1);
      ctx.bezierCurveTo(w * 0.7, yStream1 - 10, w * 0.4, yStream1 + 10, 0, yStream1);
      ctx.stroke();

      // رسم برگ‌های پاییزی معلق در هوا با چرخش سه‌بعدی
      for (var lIdx = 0; lIdx < leaves.length; lIdx++) {
        var lf = leaves[lIdx];
        lf.x += lf.speedX;
        lf.y += Math.sin(timeTick * 0.04 + lIdx) * 0.8 + lf.speedY;
        lf.rotation += lf.rotSpeed;
        lf.flip += lf.flipSpeed;

        if (lf.x < -40) {
          lf.x = w + 40;
          lf.y = 20 + Math.random() * (h - 70);
        }

        ctx.save();
        ctx.translate(lf.x, lf.y);
        ctx.rotate(lf.rotation);
        ctx.scale(Math.cos(lf.flip), 1); // شبیه‌سازی غلتش سه‌بعدی برگ در باد

        ctx.fillStyle = lf.color;
        ctx.beginPath();
        ctx.moveTo(0, -lf.size * 0.5);
        ctx.quadraticCurveTo(lf.size * 0.5, 0, 0, lf.size * 0.5);
        ctx.quadraticCurveTo(-lf.size * 0.5, 0, 0, -lf.size * 0.5);
        ctx.fill();

        // ساقه برگ
        ctx.strokeStyle = 'rgba(70, 30, 0, 0.7)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, lf.size * 0.5);
        ctx.lineTo(0, lf.size * 0.7);
        ctx.stroke();

        ctx.restore();
      }
    }

    // ۴. رندر ستارگان درخشان شب و شهاب‌سنگ
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
          ctx.fillStyle = 'rgba(180, 220, 255, ' + (sAlpha * 0.25) + ')';
          ctx.arc(star.x, star.y, star.radius * 3.5, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // شبیه‌سازی گاه‌به‌گاه شهاب‌سنگ
      if (Math.random() < 0.003 && meteors.length === 0) {
        meteors.push({
          x: w * 0.6 + Math.random() * (w * 0.3),
          y: 10 + Math.random() * 30,
          dx: -7 - Math.random() * 4,
          dy: 4 + Math.random() * 3,
          length: 50 + Math.random() * 40,
          life: 1.0
        });
      }

      for (var mIdx = meteors.length - 1; mIdx >= 0; mIdx--) {
        var met = meteors[mIdx];
        var metGrad = ctx.createLinearGradient(met.x, met.y, met.x - met.dx * (met.length / 10), met.y - met.dy * (met.length / 10));
        metGrad.addColorStop(0, 'rgba(255, 255, 255, ' + met.life + ')');
        metGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.strokeStyle = metGrad;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(met.x, met.y);
        ctx.lineTo(met.x - met.dx * (met.length / 8), met.y - met.dy * (met.length / 8));
        ctx.stroke();

        met.x += met.dx;
        met.y += met.dy;
        met.life -= 0.04;
        if (met.life <= 0) meteors.splice(mIdx, 1);
      }
    }

    // ۵. روز آفتابی: رندر ذرات طلایی شناور در پرتوهای خورشید
    else if (state.period === 'day' && state.type === 'clear') {
      for (var dIdx = 0; dIdx < particles.length; dIdx++) {
        var mote = particles[dIdx];
        mote.y += mote.speedY;
        mote.x += Math.sin(timeTick * mote.sway + mote.phase) * 0.3;
        if (mote.y < -10) {
          mote.y = h + 10;
          mote.x = Math.random() * w;
        }
        ctx.beginPath();
        ctx.fillStyle = 'rgba(255, 235, 160, ' + mote.opacity + ')';
        ctx.arc(mote.x, mote.y, mote.radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  /* ────────── شاخه‌های صاعقه طبیعی ────────── */
  function createNaturalLightning() {
    if (!canvas) return;
    var startX = canvas.width * 0.35 + Math.random() * (canvas.width * 0.4);
    var startY = 15;
    var segments = [];
    var curX = startX;
    var curY = startY;

    while (curY < canvas.height - 40) {
      var nextX = curX + (Math.random() - 0.5) * 32;
      var nextY = curY + 12 + Math.random() * 20;
      segments.push({ x1: curX, y1: curY, x2: nextX, y2: nextY });

      // شاخه فرعی
      if (Math.random() > 0.65) {
        segments.push({
          x1: nextX,
          y1: nextY,
          x2: nextX + (Math.random() - 0.5) * 38,
          y2: nextY + 16 + Math.random() * 18,
          isBranch: true
        });
      }
      curX = nextX;
      curY = nextY;
    }

    activeLightningBolt = { segments: segments, alpha: 1.0 };

    var flash = document.getElementById('w3dLightningFlash');
    if (flash) {
      flash.style.opacity = '0.85';
      setTimeout(function () {
        flash.style.opacity = '0.15';
        setTimeout(function () {
          flash.style.opacity = '0.6';
          setTimeout(function () { flash.style.opacity = '0'; }, 70);
        }, 50);
      }, 60);
    }
  }

  function drawLightningBolt(bolt) {
    if (!ctx || !bolt) return;
    ctx.save();
    ctx.shadowColor = '#00F5FF';
    ctx.shadowBlur = 14;

    for (var b = 0; b < bolt.segments.length; b++) {
      var seg = bolt.segments[b];
      ctx.strokeStyle = seg.isBranch ? ('rgba(200, 240, 255, ' + (bolt.alpha * 0.65) + ')') : ('rgba(255, 255, 255, ' + bolt.alpha + ')');
      ctx.lineWidth = seg.isBranch ? 1.2 : 2.4;
      ctx.beginPath();
      ctx.moveTo(seg.x1, seg.y1);
      ctx.lineTo(seg.x2, seg.y2);
      ctx.stroke();
    }
    ctx.restore();

    bolt.alpha -= 0.12;
    if (bolt.alpha <= 0) {
      activeLightningBolt = null;
    }
  }

  /* ────────── اعمال استایل و عناصر بصری اتمسفریک ────────── */
  function applyWeatherState() {
    var state = resolveWeatherState();
    var isEn = isEnglish();

    var skyBg = document.getElementById('w3dSkyBg');
    var celestial = document.getElementById('w3dCelestial');
    var cloudsStage = document.getElementById('w3dCloudsStage');
    var condText = document.getElementById('w3dHudCondition');
    var timeTag = document.getElementById('w3dHudTimeTag');
    var tempNum = document.getElementById('w3dHudTemp');
    var hilo = document.getElementById('w3dHudHiLo');
    var feels = document.getElementById('w3dHudFeels');
    var humidity = document.getElementById('w3dHudHumidity');
    var windSpd = document.getElementById('w3dHudWind');

    if (!skyBg) return;

    // ۱. گرادینت آسمان با رنگ‌های غنی و عمیق
    skyBg.className = 'w3d-sky-canvas sky-' + state.period + ' sky-' + state.type;

    // ۲. جسم فلکی طبیعی (خورشید واقع‌گرایانه با پرتوهای نور، یا ماه طبیعی با دهانه‌ها)
    if (state.period === 'night' || currentMode === 'night' || state.type === 'snow') {
      celestial.innerHTML = ''
        + '<div class="w3d-natural-moon">'
        +   '<div class="w3d-moon-texture"></div>'
        +   '<div class="w3d-moon-halo"></div>'
        +   '<div class="w3d-moon-glow-outer"></div>'
        + '</div>';
    } else if (state.period === 'sunset') {
      celestial.innerHTML = ''
        + '<div class="w3d-sunset-orb">'
        +   '<div class="w3d-sunset-core"></div>'
        +   '<div class="w3d-sunset-haze"></div>'
        + '</div>';
    } else {
      celestial.innerHTML = ''
        + '<div class="w3d-natural-sun">'
        +   '<div class="w3d-sun-plasma"></div>'
        +   '<div class="w3d-sun-corona"></div>'
        +   '<div class="w3d-sunbeams"></div>'
        + '</div>';
    }

    // ۳. ابرهای حجمی طبیعی با نورپردازی متناسب
    if (state.type === 'cloudy' || state.type === 'wind' || state.type === 'rain' || state.type === 'storm') {
      var isDark = (state.type === 'storm' || state.type === 'rain');
      var cloudTheme = isDark ? ' stormy' : (state.period === 'sunset' ? ' sunset-clouds' : ' fair-clouds');
      cloudsStage.innerHTML = ''
        + '<div class="w3d-vol-cloud cloud-bank-1' + cloudTheme + '"></div>'
        + '<div class="w3d-vol-cloud cloud-bank-2' + cloudTheme + '"></div>'
        + '<div class="w3d-vol-cloud cloud-bank-3' + cloudTheme + '"></div>';
    } else if (state.period === 'day' && state.type === 'clear') {
      cloudsStage.innerHTML = '<div class="w3d-vol-cloud cloud-bank-distant"></div>';
    } else {
      cloudsStage.innerHTML = '';
    }

    // ۴. متن و برچسب‌های وضعیت
    if (condText) condText.textContent = state.label;

    if (timeTag) {
      var periodFa = {
        sunrise: 'طلوع آفتاب',
        day: 'روز',
        sunset: 'غروب',
        night: 'شب'
      }[state.period] || 'زنده';
      var periodEn = {
        sunrise: 'Sunrise',
        day: 'Daytime',
        sunset: 'Sunset',
        night: 'Night'
      }[state.period] || 'Live';
      timeTag.textContent = (isEn ? 'Varamin • ' + periodEn : 'ورامین • ' + periodFa);
    }

    // ۵. ارقام دما و متریک‌ها
    var t = 24, fl = 23, hm = 42, wd = 18, hi = 28, lo = 16;
    if (weatherData) {
      if (typeof weatherData.temp === 'number') t = Math.round(weatherData.temp);
      if (typeof weatherData.feels === 'number') fl = Math.round(weatherData.feels);
      if (typeof weatherData.humidity === 'number') hm = Math.round(weatherData.humidity);
      if (typeof weatherData.wind === 'number') wd = Math.round(weatherData.wind);
      if (typeof weatherData.max === 'number') hi = Math.round(weatherData.max);
      if (typeof weatherData.min === 'number') lo = Math.round(weatherData.min);
    }

    if (currentMode === 'snow') { t = -2; fl = -5; hm = 84; wd = 12; hi = 1; lo = -6; }
    if (currentMode === 'storm') { t = 16; fl = 14; hm = 89; wd = 45; hi = 20; lo = 14; }
    if (currentMode === 'rain') { t = 17; fl = 15; hm = 82; wd = 22; hi = 19; lo = 13; }
    if (currentMode === 'night' && !weatherData) { t = 18; fl = 17; hm = 54; wd = 10; hi = 27; lo = 15; }
    if (currentMode === 'wind') { t = 20; fl = 19; hm = 45; wd = 32; hi = 24; lo = 14; }

    if (tempNum) tempNum.textContent = fa(t);
    if (feels) feels.textContent = fa(fl) + '°';
    var humUnit = isEn ? '%' : '٪';
    if (humidity) humidity.textContent = fa(hm) + humUnit;
    if (windSpd) windSpd.textContent = fa(wd) + ' km/h';
    if (hilo) {
      hilo.textContent = isEn
        ? ('H: ' + fa(hi) + '°  L: ' + fa(lo) + '°')
        : ('بیشینه ' + fa(hi) + '° / کمینه ' + fa(lo) + '°');
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
    f.write(weather_js)
print("   -> modules/weather-3d.js successfully rewritten with realistic atmospheric engine!")

