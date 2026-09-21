import re

print("--- 1. Updating index.html ---")
index_path = '/home/user/eplak/eplak-fixed/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update version query string for style.css and modules/home.js to bust browser cache
html = re.sub(r'href="assets/css/style\.css\?v=\d+"', 'href="assets/css/style.css?v=20"', html)
html = re.sub(r'src="modules/home\.js\?v=\d+"', 'src="modules/home.js?v=20"', html)

# 2. In index.html, remove the inline onclick="showScreen('screen-news')" from .vsc-slide containers
# so swiping doesn't trigger unexpected screen transitions!
html = html.replace(
    '<div class="vsc-slide" onclick="showScreen(\'screen-news\')">',
    '<div class="vsc-slide">'
)

# 3. Add draggable="false" and ondragstart="return false;" to varamin images
html = html.replace(
    '<img src="assets/img/varamin-mosque.jpg" alt="مسجد جامع ورامین" class="vsc-photo">',
    '<img src="assets/img/varamin-mosque.jpg" alt="مسجد جامع ورامین" class="vsc-photo" draggable="false" ondragstart="return false;">'
)
html = html.replace(
    '<img src="assets/img/varamin-tower.jpg" alt="برج علاءالدوله ورامین" class="vsc-photo vsc-photo-tower">',
    '<img src="assets/img/varamin-tower.jpg" alt="برج علاءالدوله ورامین" class="vsc-photo vsc-photo-tower" draggable="false" ondragstart="return false;">'
)

# 4. Add elegant left/right navigation arrow buttons inside varaminShowcase
arrows_markup = """        <!-- دکمه‌های ناوبری لمسی و کلیکی چپ و راست -->
        <button class="vsc-nav vsc-prev" onclick="event.stopPropagation(); vscPrev();" aria-label="عکس قبلی" type="button">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
        <button class="vsc-nav vsc-next" onclick="event.stopPropagation(); vscNext();" aria-label="عکس بعدی" type="button">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>"""

if 'class="vsc-nav vsc-prev"' not in html:
    # Insert right before <div class="vsc-dots"
    html = html.replace(
        '<div class="vsc-dots" id="vscDots">',
        arrows_markup + '\n\n        <div class="vsc-dots" id="vscDots">'
    )
    print("   -> Added navigation arrows into varaminShowcase!")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("   -> index.html updated successfully!")


print("\n--- 2. Updating assets/css/style.css ---")
style_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .vsc-shade block with strict bottom-positioned low-height fade
new_vsc_shade_css = """  /* سایه مشکی اختصاصی از پایین عکس به سمت وسط با ارتفاع کم و فید شونده */
  .vsc-shade {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 48%; /* ارتفاع کم: دقیقاً کمتر از نیمی از عکس و فقط در بخش پایینی */
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.94) 0%,
      rgba(0, 0, 0, 0.72) 28%,
      rgba(0, 0, 0, 0.35) 60%,
      rgba(0, 0, 0, 0.08) 84%,
      transparent 100%
    );
    z-index: 1;
    pointer-events: none;
  }"""

css = re.sub(
    r'/\*.*?\*/\s*\.vsc-shade\s*\{[^}]*\}',
    new_vsc_shade_css,
    css,
    count=1
)

# Ensure .vsc-nav buttons are styled
nav_css = """
  /* دکمه‌های ناوبری شیشه‌ای و مدرن چپ و راست اسلایدر */
  .vsc-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(8, 20, 24, 0.65);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.22);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 5;
    transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
    padding: 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    touch-action: manipulation;
  }
  .vsc-nav:hover {
    background: rgba(0, 229, 195, 0.3);
    border-color: rgba(0, 229, 195, 0.8);
    color: #00E5C3;
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 0 14px rgba(0, 229, 195, 0.5);
  }
  .vsc-nav:active {
    transform: translateY(-50%) scale(0.92);
  }
  .vsc-prev {
    right: 14px;
  }
  .vsc-next {
    left: 14px;
  }
"""

if '.vsc-nav' not in css:
    css = css.replace('.vsc-dots {', nav_css + '\n  .vsc-dots {')
    print("   -> Added .vsc-nav styles to style.css!")
else:
    print("   -> .vsc-nav styles already present.")

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("   -> style.css updated successfully!")


print("\n--- 3. Updating modules/home.js with flawless gesture engine ---")
home_js_path = '/home/user/eplak/eplak-fixed/modules/home.js'

new_home_js = """/* modules/home.js — صفحه خانه (Home) */
/*
   ===== کاروسل دورانی فوق‌العاده روان و بدون لگ «میراث ورامین» =====
   - قابلیت سوایپ پیوسته و نامحدود به چپ و راست (Infinite Seamless Loop)
   - بدون کوچکترین گیر، پرش، تاخیر یا لگ (100% 60fps با GPU Hardware Acceleration)
   - حرکت دقیق ۱:۱ هماهنگ با نوک انگشت یا ماوس
   - دکمه‌های ناوبری اختصاصی چپ و راست (vscNext و vscPrev)
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
  var autoplayDelay = 5500;
  var autoplayTimer = null;
  var isAnimating = false;

  function updateDots(activeDotIndex) {
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i === activeDotIndex);
    });
  }

  function getRealIndex(idx) {
    if (idx === 0) return realCount - 1; // 1
    if (idx === totalSlides - 1) return 0; // 0
    return idx - 1;
  }

  function setTrackPosition(percent, animate) {
    if (animate) {
      track.classList.remove('vsc-dragging');
    } else {
      track.classList.add('vsc-dragging');
    }
    track.style.transform = 'translate3d(' + percent + '%, 0, 0)';
  }

  // نرمال‌سازی فوری اندیس قبل از هر حرکت یا کشیدن
  function normalizeIndex() {
    if (current <= 0) {
      current = realCount; // 2
      setTrackPosition(-current * 100, false);
      void track.offsetWidth;
    } else if (current >= totalSlides - 1) {
      current = 1;
      setTrackPosition(-current * 100, false);
      void track.offsetWidth;
    }
  }

  function goToIndex(idx, animate) {
    if (typeof animate === 'undefined') animate = true;
    current = idx;
    var targetPercent = -current * 100;
    setTrackPosition(targetPercent, animate);
    updateDots(getRealIndex(current));
  }

  window.vscGoTo = function (realIdx) {
    stopAutoplay();
    normalizeIndex();
    goToIndex(realIdx + 1, true);
    restartAutoplay();
  };

  window.vscNext = function () {
    stopAutoplay();
    normalizeIndex();
    goToIndex(current + 1, true);
    restartAutoplay();
  };

  window.vscPrev = function () {
    stopAutoplay();
    normalizeIndex();
    goToIndex(current - 1, true);
    restartAutoplay();
  };

  function nextSlideAuto() {
    if (isDragging) return;
    normalizeIndex();
    goToIndex(current + 1, true);
  }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(nextSlideAuto, autoplayDelay);
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
    isAnimating = false;

    if (current === 0) {
      // به کلون اسلاید آخر رسیدیم، پرش نامحسوس به اسلاید اصلی آخر
      current = totalSlides - 2; // 2
      setTrackPosition(-current * 100, false);
      void track.offsetWidth;
    } else if (current === totalSlides - 1) {
      // به کلون اسلاید اول رسیدیم، پرش نامحسوس به اسلاید اصلی اول
      current = 1;
      setTrackPosition(-current * 100, false);
      void track.offsetWidth;
    }
  });

  /* ---- موتور لمس و درگ فوق‌العاده روان بدون لگ با شتاب سخت‌افزاری ---- */
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
    normalizeIndex();
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
      if (absX > 6 || absY > 6) {
        directionLocked = true;
        if (absX >= absY) {
          isHorizontalSwipe = true;
          track.classList.add('vsc-dragging');
        } else {
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

    if (Math.abs(deltaX) > 8) {
      didDrag = true;
    }

    // حرکت یکپارچه ۱:۱ با دست کاربر
    var basePercent = -current * 100;
    var dragPercent = (deltaX / widthPx) * 100;
    track.style.transform = 'translate3d(' + (basePercent + dragPercent) + '%, 0, 0)';
  }

  function handleEnd() {
    if (!isDragging) return;
    isDragging = false;
    track.classList.remove('vsc-dragging');

    if (isHorizontalSwipe) {
      var threshold = Math.min(widthPx * 0.12, 45); // آستانه سریع ۴۵ پیکسل
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

  // رویدادهای لمسی موبایل (Touch Events)
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

  // رویدادهای ماوس دسکتاپ (Mouse Drag)
  showcase.addEventListener('mousedown', function (e) {
    if (e.button !== 0) return;
    // اگر روی دکمه‌ها کلیک شده، درگ فعال نشود
    if (e.target.closest('button')) return;
    handleStart(e.clientX, e.clientY);
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

  // جلوگیری کامل از رفتارهای پیش‌فرض کشیدن عکس در مرورگر
  showcase.addEventListener('dragstart', function (e) {
    e.preventDefault();
    return false;
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

  // توقف خودکار هنگام هاور ماوس
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
print("   -> modules/home.js updated successfully!")
