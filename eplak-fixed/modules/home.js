/* modules/home.js — صفحه خانه (Home) */
/*
   توجه: در فایل اصلی app_01.html منطق اختصاصی جداگانه‌ای برای صفحه خانه
   تعریف نشده بود؛ صفحه خانه فقط از showScreen() و showToast() که در
   core/router.js قرار دارند استفاده می‌کند (مثلاً دکمه‌های Services Grid
   و Promo Banner مستقیماً onclick="showScreen(...)" صدا می‌زنند).
   این فایل برای پایبندی کامل به ساختار چارت درخواستی نگه داشته شده و
   عمداً خالی از منطق اضافه است تا چیزی به رفتار اصلی اپ اضافه/تغییر نکند.

   ===== افزوده‌ی جدید: کاروسل «میراث ورامین» =====
   اسلایدر دو-اسلایدی (مسجد جامع ورامین / برج علاءالدوله ورامین) با:
   - چرخش خودکار (auto-play) و توقف موقت هنگام تعامل کاربر
   - پشتیبانی از سوایپ لمسی و درگ با ماوس
   - نقاط (dots) قابل کلیک برای پرش مستقیم به هر اسلاید
*/

(function initVaraminShowcase() {
  var track = document.getElementById('vscTrack');
  var showcase = document.getElementById('varaminShowcase');
  var dotsWrap = document.getElementById('vscDots');
  if (!track || !showcase || !dotsWrap) return;

  var slides = track.querySelectorAll('.vsc-slide');
  var dots = dotsWrap.querySelectorAll('.vsc-dot');
  var total = slides.length;
  var current = 0;
  var autoplayDelay = 4500;
  var autoplayTimer = null;

  function render() {
    track.style.transform = 'translateX(' + (current * 100) + '%)';
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i === current);
    });
  }

  window.vscGoTo = function (index) {
    current = ((index % total) + total) % total;
    render();
    restartAutoplay();
  };

  function next() {
    current = (current + 1) % total;
    render();
  }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(next, autoplayDelay);
  }
  function stopAutoplay() {
    if (autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; }
  }
  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  /* ---- Swipe / drag support ---- */
  var startX = 0, deltaX = 0, dragging = false, didDrag = false;
  var widthPx = 1;

  function pointerDown(x) {
    dragging = true;
    didDrag = false;
    startX = x;
    deltaX = 0;
    widthPx = showcase.getBoundingClientRect().width || 1;
    track.classList.add('vsc-dragging');
    stopAutoplay();
  }
  function pointerMove(x) {
    if (!dragging) return;
    deltaX = x - startX;
    if (Math.abs(deltaX) > 6) didDrag = true;
    var basePercent = -current * 100;
    var dragPercent = (deltaX / widthPx) * 100;
    track.style.transform = 'translateX(' + (basePercent + dragPercent) + '%)';
  }
  function pointerUp() {
    if (!dragging) return;
    dragging = false;
    track.classList.remove('vsc-dragging');
    var threshold = widthPx * 0.18;
    // RTL layout: dragging right (positive deltaX) reveals previous slide,
    // dragging left (negative deltaX) advances to next slide.
    if (deltaX <= -threshold) {
      current = (current + 1) % total;
    } else if (deltaX >= threshold) {
      current = ((current - 1) + total) % total;
    }
    render();
    restartAutoplay();
  }

  // Touch events
  track.addEventListener('touchstart', function (e) {
    pointerDown(e.touches[0].clientX);
  }, { passive: true });
  track.addEventListener('touchmove', function (e) {
    pointerMove(e.touches[0].clientX);
  }, { passive: true });
  track.addEventListener('touchend', pointerUp);

  // Mouse drag events (desktop preview)
  track.addEventListener('mousedown', function (e) {
    pointerDown(e.clientX);
    e.preventDefault();
  });
  window.addEventListener('mousemove', function (e) {
    if (dragging) pointerMove(e.clientX);
  });
  window.addEventListener('mouseup', function () {
    if (dragging) pointerUp();
  });

  // Prevent navigation click right after a drag
  slides.forEach(function (slide) {
    slide.addEventListener('click', function (e) {
      if (didDrag) {
        e.preventDefault();
        e.stopPropagation();
        didDrag = false;
      }
    }, true);
  });

  // Pause autoplay while finger/mouse hovers, resume on leave
  showcase.addEventListener('mouseenter', stopAutoplay);
  showcase.addEventListener('mouseleave', startAutoplay);

  render();
  startAutoplay();
})();

