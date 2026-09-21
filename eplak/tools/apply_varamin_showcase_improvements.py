import re

print("[1] Updating eplak-fixed/assets/css/style.css ...")
style_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

old_vsc_css_pattern = r'/\* ===== VARAMIN SHOWCASE \(شهر ما، خانه ما\) — Carousel ===== \*/.*?\.vsc-frame-ring \{'

new_vsc_css = """/* ===== VARAMIN SHOWCASE (شهر ما، خانه ما) — Carousel ===== */
  .varamin-showcase {
    margin: 4px 16px 0;
    position: relative;
    border-radius: 26px;
    overflow: hidden;
    height: 300px;
    cursor: grab;
    isolation: isolate;
    box-shadow:
      0 20px 50px -12px rgba(0,0,0,0.55),
      0 2px 0 rgba(255,255,255,0.04) inset;
    user-select: none;
    -webkit-user-select: none;
    -webkit-touch-callout: none;
    touch-action: pan-y;
  }
  .varamin-showcase:active {
    cursor: grabbing;
  }

  .vsc-track {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: row;
    direction: ltr;
    height: 100%;
    width: 100%;
    transition: transform 0.32s cubic-bezier(0.25, 1, 0.5, 1);
    will-change: transform;
    touch-action: pan-y;
    user-select: none;
    -webkit-user-select: none;
    transform: translate3d(0, 0, 0);
  }
  .vsc-track.vsc-dragging {
    transition: none !important;
  }

  .vsc-slide {
    position: relative;
    flex: 0 0 100%;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: flex-end;
    direction: rtl;
    user-select: none;
    -webkit-user-select: none;
  }

  .vsc-photo-layer {
    position: absolute;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
  }
  .vsc-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 32%;
    display: block;
    filter: saturate(1.08) contrast(1.04);
    -webkit-user-drag: none;
    user-select: none;
    pointer-events: none;
  }
  .vsc-photo-tower { object-position: center 50%; }

  .vsc-dots {
    position: absolute;
    left: 50%;
    bottom: 14px;
    transform: translateX(-50%);
    z-index: 4;
    display: flex;
    gap: 7px;
    padding: 6px 9px;
    border-radius: 999px;
    background: rgba(8,20,20,0.35);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
  .vsc-dot {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    border: none;
    padding: 0;
    background: rgba(255,255,255,0.45);
    cursor: pointer;
    transition: width 0.35s ease, background 0.35s ease;
  }
  .vsc-dot.active {
    width: 18px;
    background: var(--teal, #00E5C3);
    box-shadow: 0 0 8px 1px rgba(0,229,195,0.7);
  }

  /* مشکی بالای عکس به سمت وسط که محو و کمرنگ می‌شود و ارتفاعش کم است */
  .vsc-top-shade {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 35%;
    background:
      linear-gradient(180deg, rgba(0, 0, 0, 0.88) 0%, rgba(0, 0, 0, 0.52) 32%, rgba(0, 0, 0, 0.16) 68%, rgba(0, 0, 0, 0) 100%),
      radial-gradient(ellipse 90% 65% at 50% 0%, rgba(0, 0, 0, 0.72) 0%, rgba(0, 0, 0, 0) 100%);
    z-index: 1;
    pointer-events: none;
  }

  /* layered depth shading for legibility + richness */
  .vsc-shade {
    position: absolute;
    inset: 0;
    background:
      /* گرادینت مشکی بالای عکس فید شونده به سمت وسط با ارتفاع کم */
      linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.48) 15%, rgba(0,0,0,0.12) 26%, transparent 36%),
      /* گرادینت تیره پایین برای وضوح کامل متن و دکمه‌ها */
      linear-gradient(180deg, transparent 40%, rgba(6,16,18,0.65) 66%, rgba(4,10,12,0.96) 100%),
      linear-gradient(95deg, rgba(4,14,14,0.45) 0%, rgba(4,14,14,0.05) 45%, rgba(4,14,14,0) 70%);
    z-index: 1;
    pointer-events: none;
  }
  .vsc-grain {
    position: absolute;
    inset: 0;
    z-index: 1;
    background-image: radial-gradient(rgba(255,255,255,0.045) 1px, transparent 1px);
    background-size: 3px 3px;
    mix-blend-mode: overlay;
    opacity: 0.5;
    pointer-events: none;
  }

  /* subtle inner ring frame for a crafted, premium feel */
  .vsc-frame-ring {"""

match_css = re.search(old_vsc_css_pattern, css, flags=re.DOTALL)
if match_css:
    css = css[:match_css.start()] + new_vsc_css + css[match_css.end():]
    print("   -> CSS for Varamin Showcase updated successfully!")
else:
    print("   [ERR] Could not match old_vsc_css_pattern in style.css.")

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css)


print("\n[2] Updating eplak-fixed/index.html ...")
html_path = '/home/user/eplak/eplak-fixed/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add <div class="vsc-top-shade"></div> to Slide 1 and Slide 2 if not present
if '<div class="vsc-top-shade"></div>' not in html:
    html = html.replace(
        '<div class="vsc-photo-layer">\n              <img src="assets/img/varamin-mosque.jpg" alt="مسجد جامع ورامین" class="vsc-photo">\n            </div>\n            <div class="vsc-shade"></div>',
        '<div class="vsc-photo-layer">\n              <img src="assets/img/varamin-mosque.jpg" alt="مسجد جامع ورامین" class="vsc-photo">\n            </div>\n            <div class="vsc-top-shade"></div>\n            <div class="vsc-shade"></div>'
    )
    html = html.replace(
        '<div class="vsc-photo-layer">\n              <img src="assets/img/varamin-tower.jpg" alt="برج علاءالدوله ورامین" class="vsc-photo vsc-photo-tower">\n            </div>\n            <div class="vsc-shade"></div>',
        '<div class="vsc-photo-layer">\n              <img src="assets/img/varamin-tower.jpg" alt="برج علاءالدوله ورامین" class="vsc-photo vsc-photo-tower">\n            </div>\n            <div class="vsc-top-shade"></div>\n            <div class="vsc-shade"></div>'
    )
    print("   -> Added vsc-top-shade element to both showcase slides in index.html!")
else:
    print("   -> vsc-top-shade already present in index.html.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)


print("\n[3] Updating eplak-fixed/modules/home.js ...")
home_js_path = '/home/user/eplak/eplak-fixed/modules/home.js'

new_home_js = """/* modules/home.js — صفحه خانه (Home) */
/*
   ===== کاروسل روان و بدون لگ «میراث ورامین» =====
   اسلایدر روان دوطرفه (چپ و راست) با:
   - حرکت 1:1 دقیق با لمس و درگ ماوس با شتاب سخت‌افزاری GPU (translate3d)
   - بدون کوچکترین گیر، پرش، تاخیر یا لگ
   - قفل زاویه حرکت (تشخیص هوشمند سوایپ افقی از اسکرول عمودی صفحه)
   - چرخش خودکار دورانی در هر دو جهت (چپ و راست)
   - نقاط ناوبری زنده (dots)
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
  var autoplayDelay = 5000;
  var autoplayTimer = null;

  function updateDots() {
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i === current);
    });
  }

  function goToSlide(index, animate) {
    if (typeof animate === 'undefined') animate = true;
    current = ((index % total) + total) % total;

    if (!animate) {
      track.classList.add('vsc-dragging');
    } else {
      track.classList.remove('vsc-dragging');
    }

    var targetPercent = -current * 100;
    track.style.transform = 'translate3d(' + targetPercent + '%, 0, 0)';
    updateDots();

    if (!animate) {
      // Force repaint then re-enable transition
      void track.offsetWidth;
      track.classList.remove('vsc-dragging');
    }
  }

  window.vscGoTo = function (index) {
    goToSlide(index, true);
    restartAutoplay();
  };

  function nextSlide() {
    goToSlide(current + 1, true);
  }

  function prevSlide() {
    goToSlide(current - 1, true);
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

  /* ---- حرکت روان، بلادرنگ و بدون لگ با لمس و ماوس ---- */
  var startX = 0;
  var startY = 0;
  var currentX = 0;
  var deltaX = 0;
  var deltaY = 0;
  var isDragging = false;
  var isHorizontalSwipe = false;
  var hasDeterminedDirection = false;
  var widthPx = 1;
  var didDrag = false;

  function onPointerDown(e) {
    if (e.pointerType === 'mouse' && e.button !== 0) return;

    isDragging = true;
    didDrag = false;
    hasDeterminedDirection = false;
    isHorizontalSwipe = false;

    startX = e.clientX;
    startY = e.clientY;
    currentX = e.clientX;
    deltaX = 0;
    deltaY = 0;

    widthPx = showcase.getBoundingClientRect().width || 1;
    stopAutoplay();

    try {
      track.setPointerCapture(e.pointerId);
    } catch (err) {}
  }

  function onPointerMove(e) {
    if (!isDragging) return;

    currentX = e.clientX;
    deltaX = currentX - startX;
    deltaY = e.clientY - startY;

    // تشخیص دقیق جهت در ۴ پیکسل اول حرکت
    if (!hasDeterminedDirection) {
      var absX = Math.abs(deltaX);
      var absY = Math.abs(deltaY);
      if (absX > 4 || absY > 4) {
        hasDeterminedDirection = true;
        if (absX >= absY) {
          // حرکت افقی — فعال‌سازی بی‌درنگ بدون لگ
          isHorizontalSwipe = true;
          track.classList.add('vsc-dragging');
        } else {
          // اسکرول عمودی صفحه — رهاسازی فوری تا اسکرول صفحه نرم و بدون گیر بماند
          isDragging = false;
          try {
            track.releasePointerCapture(e.pointerId);
          } catch (err) {}
          return;
        }
      } else {
        return;
      }
    }

    if (!isHorizontalSwipe) return;

    if (Math.abs(deltaX) > 6) {
      didDrag = true;
    }

    // حرکت یکپارچه ۱:۱ با انگشت با فیزیک روان
    var effectiveDelta = deltaX;
    var basePercent = -current * 100;
    var dragPercent = (effectiveDelta / widthPx) * 100;
    track.style.transform = 'translate3d(' + (basePercent + dragPercent) + '%, 0, 0)';
  }

  function onPointerEnd(e) {
    if (!isDragging && !isHorizontalSwipe) return;

    isDragging = false;
    track.classList.remove('vsc-dragging');

    if (isHorizontalSwipe) {
      var threshold = Math.min(widthPx * 0.15, 55); // آستانه سریع ۵۵ پیکسل
      if (deltaX < -threshold) {
        // کشیدن به چپ: اسلاید بعدی (با چرخش دورانی)
        goToSlide(current + 1, true);
      } else if (deltaX > threshold) {
        // کشیدن به راست: اسلاید قبلی (با چرخش دورانی)
        goToSlide(current - 1, true);
      } else {
        // بازگشت نرم به همان اسلاید
        goToSlide(current, true);
      }
    }

    try {
      track.releasePointerCapture(e.pointerId);
    } catch (err) {}

    restartAutoplay();
  }

  // ثبت رویدادهای Pointer جهت عملکرد بی‌نقص در لمسی، موس و قلم
  track.addEventListener('pointerdown', onPointerDown, { passive: true });
  track.addEventListener('pointermove', onPointerMove, { passive: true });
  track.addEventListener('pointerup', onPointerEnd);
  track.addEventListener('pointercancel', onPointerEnd);

  // جلوگیری از کلیک ناخواسته روی اسلاید هنگام درگ
  track.querySelectorAll('.vsc-slide').forEach(function (slide) {
    slide.addEventListener('click', function (e) {
      if (didDrag) {
        e.preventDefault();
        e.stopPropagation();
        didDrag = false;
      }
    }, true);
  });

  // توقف موقت هنگام توقف ماوس (در دسکتاپ)
  showcase.addEventListener('mouseenter', stopAutoplay);
  showcase.addEventListener('mouseleave', startAutoplay);

  // مقداردهی اولیه
  goToSlide(0, false);
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
