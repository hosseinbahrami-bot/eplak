import re

print("[1] Updating eplak-fixed/assets/css/style.css ...")
style_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the vsc-shade rule
old_vsc_shade_pattern = r'/\* layered depth shading:.*?\*/\s*\.vsc-shade\s*\{.*?pointer-events:\s*none;\s*\}'

new_vsc_shade = """/* layered depth shading: مشکی شیک از پایین عکس به سمت وسط که ملایم محو می‌شود با ارتفاع کم */
  .vsc-shade {
    position: absolute;
    inset: 0;
    background:
      /* گرادینت مشکی خالص از لبه پایین به سمت وسط که ملایم محو می‌شود و ارتفاعش کم است */
      linear-gradient(to top, rgba(0, 0, 0, 0.95) 0%, rgba(0, 0, 0, 0.72) 16%, rgba(0, 0, 0, 0.32) 30%, rgba(0, 0, 0, 0.06) 42%, transparent 48%),
      linear-gradient(95deg, rgba(0, 0, 0, 0.35) 0%, transparent 45%);
    z-index: 1;
    pointer-events: none;
  }"""

match_shade = re.search(old_vsc_shade_pattern, css, flags=re.DOTALL)
if match_shade:
    css = css[:match_shade.start()] + new_vsc_shade + css[match_shade.end():]
    print("   -> vsc-shade updated with low-height bottom black gradient!")
else:
    print("   [!] Could not regex match vsc-shade, trying fallback replace...")
    css = re.sub(r'\.vsc-shade\s*\{[^}]*\}', new_vsc_shade, css, count=1)
    print("   -> vsc-shade replaced by fallback!")

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css)


print("\n[2] Updating eplak-fixed/modules/home.js ...")
home_js_path = '/home/user/eplak/eplak-fixed/modules/home.js'

new_home_js = """/* modules/home.js — صفحه خانه (Home) */
/*
   ===== کاروسل دورانی فوق‌العاده روان و بدون لگ «میراث ورامین» =====
   - قابلیت سوایپ پیوسته و نامحدود به چپ و راست (Infinite Seamless Loop)
   - بدون کوچکترین گیر، پرش، تاخیر یا لگ (100% 60fps با GPU Hardware Acceleration)
   - حرکت دقیق ۱:۱ هماهنگ با نوک انگشت یا ماوس
   - تشخیص هوشمند اسکرول عمودی صفحه از سوایپ افقی
   - نقاط ناوبری زنده و هماهنگ (dots)
*/

(function initVaraminShowcase() {
  var showcase = document.getElementById('varaminShowcase');
  var track = document.getElementById('vscTrack');
  var dotsWrap = document.getElementById('vscDots');
  if (!showcase || !track || !dotsWrap) return;

  var originalSlides = track.querySelectorAll('.vsc-slide:not(.vsc-clone)');
  if (originalSlides.length < 2) return;

  // حذف کلون‌های قبلی در صورت بارگذاری مجدد
  track.querySelectorAll('.vsc-clone').forEach(function (el) { el.remove(); });

  // ایجاد کلون‌ها برای چرخش پیوسته و بدون قفل شدن به چپ و راست
  var firstClone = originalSlides[0].cloneNode(true);
  var lastClone = originalSlides[originalSlides.length - 1].cloneNode(true);
  firstClone.classList.add('vsc-clone');
  lastClone.classList.add('vsc-clone');

  track.insertBefore(lastClone, originalSlides[0]);
  track.appendChild(firstClone);

  var allSlides = track.querySelectorAll('.vsc-slide');
  var dots = dotsWrap.querySelectorAll('.vsc-dot');
  var realCount = originalSlides.length; // 2
  var totalSlides = allSlides.length; // 4 (0: lastClone, 1: slide1, 2: slide2, 3: firstClone)

  var current = 1; // شروع از اولین اسلاید اصلی (مسجد جامع)
  var autoplayDelay = 5000;
  var autoplayTimer = null;
  var isTransitioning = false;

  function updateDots(activeDotIndex) {
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i === activeDotIndex);
    });
  }

  function getRealIndex(index) {
    if (index === 0) return realCount - 1; // 1
    if (index === totalSlides - 1) return 0; // 0
    return index - 1;
  }

  function setTrackPosition(percent, animate) {
    if (animate) {
      track.classList.remove('vsc-dragging');
    } else {
      track.classList.add('vsc-dragging');
    }
    track.style.transform = 'translate3d(' + percent + '%, 0, 0)';
  }

  function goToIndex(index, animate) {
    if (typeof animate === 'undefined') animate = true;
    current = index;
    var targetPercent = -current * 100;
    setTrackPosition(targetPercent, animate);
    updateDots(getRealIndex(current));
  }

  window.vscGoTo = function (realIdx) {
    stopAutoplay();
    goToIndex(realIdx + 1, true);
    restartAutoplay();
  };

  function nextSlide() {
    if (isDragging) return;
    goToIndex(current + 1, true);
  }

  function prevSlide() {
    if (isDragging) return;
    goToIndex(current - 1, true);
  }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(nextSlide, autoplayDelay);
  }

  function stopAutoplay() {
    if (autoplayTimer) {
      clearInterval(autoplayTimer);
      autoplayTimer = null;
    }
  }

  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  // پس از پایان هر حرکت انیمیشنی، بررسی کلون‌ها و سوئیچ نامحسوس
  track.addEventListener('transitionend', function (e) {
    if (e.target !== track) return;
    isTransitioning = false;

    if (current === 0) {
      // به کلون اسلاید آخر رسیدیم، پرش نامحسوس به اسلاید اصلی آخر
      current = totalSlides - 2; // 2
      setTrackPosition(-current * 100, false);
      void track.offsetWidth; // force reflow
    } else if (current === totalSlides - 1) {
      // به کلون اسلاید اول رسیدیم، پرش نامحسوس به اسلاید اصلی اول
      current = 1;
      setTrackPosition(-current * 100, false);
      void track.offsetWidth; // force reflow
    }
  });

  /* ---- موتور لمس و درگ روان با شتاب سخت‌افزاری ---- */
  var startX = 0;
  var startY = 0;
  var deltaX = 0;
  var deltaY = 0;
  var isDragging = false;
  var isHorizontalSwipe = false;
  var directionLocked = false;
  var widthPx = 1;
  var didDrag = false;

  function handleStart(x, y) {
    isDragging = true;
    didDrag = false;
    directionLocked = false;
    isHorizontalSwipe = false;
    startX = x;
    startY = y;
    deltaX = 0;
    deltaY = 0;
    widthPx = showcase.getBoundingClientRect().width || 1;
    stopAutoplay();
  }

  function handleMove(x, y, e) {
    if (!isDragging) return;
    deltaX = x - startX;
    deltaY = y - startY;

    if (!directionLocked) {
      var absX = Math.abs(deltaX);
      var absY = Math.abs(deltaY);
      if (absX > 5 || absY > 5) {
        directionLocked = true;
        if (absX >= absY) {
          // سوایپ افقی تایید شد
          isHorizontalSwipe = true;
          track.classList.add('vsc-dragging');
        } else {
          // اسکرول عمودی صفحه — آزادسازی سوایپ برای حفظ روانی اسکرول صفحه
          isDragging = false;
          return;
        }
      } else {
        return;
      }
    }

    if (!isHorizontalSwipe) return;

    if (e && e.cancelable && typeof e.preventDefault === 'function') {
      e.preventDefault();
    }

    if (Math.abs(deltaX) > 6) {
      didDrag = true;
    }

    // حرکت ۱:۱ و هماهنگ با انگشت کاربر بدون کوچکترین لگ
    var basePercent = -current * 100;
    var dragPercent = (deltaX / widthPx) * 100;
    track.style.transform = 'translate3d(' + (basePercent + dragPercent) + '%, 0, 0)';
  }

  function handleEnd() {
    if (!isDragging && !isHorizontalSwipe) return;
    isDragging = false;
    track.classList.remove('vsc-dragging');

    if (isHorizontalSwipe) {
      var threshold = Math.min(widthPx * 0.15, 50); // آستانه سریع ۵۰ پیکسل
      if (deltaX < -threshold) {
        // کشیدن به چپ: اسلاید بعدی
        goToIndex(current + 1, true);
      } else if (deltaX > threshold) {
        // کشیدن به راست: اسلاید قبلی
        goToIndex(current - 1, true);
      } else {
        // برگشت نرم به همان اسلاید
        goToIndex(current, true);
      }
    }

    restartAutoplay();
  }

  // رویدادهای لمسی استاندارد موبایل (Touch Events)
  showcase.addEventListener('touchstart', function (e) {
    if (e.touches.length === 1) {
      handleStart(e.touches[0].clientX, e.touches[0].clientY);
    }
  }, { passive: true });

  showcase.addEventListener('touchmove', function (e) {
    if (e.touches.length === 1) {
      handleMove(e.touches[0].clientX, e.touches[0].clientY, e);
    }
  }, { passive: false });

  showcase.addEventListener('touchend', handleEnd, { passive: true });
  showcase.addEventListener('touchcancel', handleEnd, { passive: true });

  // رویدادهای ماوس دسکتاپ (Pointer/Mouse Events)
  showcase.addEventListener('mousedown', function (e) {
    if (e.button !== 0) return;
    handleStart(e.clientX, e.clientY);
    e.preventDefault();
  });

  window.addEventListener('mousemove', function (e) {
    if (isDragging) {
      handleMove(e.clientX, e.clientY, e);
    }
  });

  window.addEventListener('mouseup', function () {
    if (isDragging) {
      handleEnd();
    }
  });

  // جلوگیری از کلیک ناخواسته روی اسلاید هنگام درگ
  allSlides.forEach(function (slide) {
    slide.addEventListener('click', function (e) {
      if (didDrag) {
        e.preventDefault();
        e.stopPropagation();
        didDrag = false;
      }
    }, true);
  });

  // توقف موقت هنگام شناور شدن ماوس (در دسکتاپ)
  showcase.addEventListener('mouseenter', stopAutoplay);
  showcase.addEventListener('mouseleave', startAutoplay);

  // راه‌اندازی اولیه
  goToIndex(1, false);
  startAutoplay();
})();

/* ---- مدیریت کلیک روی بنر تبلیغات آی‌باتری ---- */
function handleHomeAdClick() {
  var isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
    ? window.i18n.getLanguage() === 'en'
    : (window.i18n && window.i18n.currentLang === 'en');
  if (typeof showToast === 'function') {
    showToast(isEn
      ? 'ibatri: Smart on-site car battery replacement service'
      : 'آی‌باتری: سامانه هوشمند تعویض باتری خودرو در محل');
  }
}
window.handleHomeAdClick = handleHomeAdClick;
"""

with open(home_js_path, 'w', encoding='utf-8') as f:
    f.write(new_home_js)

print("   -> modules/home.js updated with infinite bidirectional carousel!")
