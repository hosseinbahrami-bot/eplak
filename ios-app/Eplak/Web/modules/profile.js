/* modules/profile.js — پروفایل کاربر، تنظیمات و علاقه‌مندی‌ها */
/* استخراج‌شده عیناً از فایل اصلی app_01.html بدون تغییر منطق */

  /* =========================================================
     Favorites
  ========================================================= */
  function renderFavorites() {
    const grid = document.getElementById('favoritesGridWrap');
    const empty = document.getElementById('favoritesEmptyState');
    const favs = allServices.filter(s => favoriteIds.includes(s.id));
    if (favs.length === 0) {
      grid.style.display = 'none';
      empty.style.display = 'block';
      return;
    }
    grid.style.display = 'grid';
    empty.style.display = 'none';
    grid.innerHTML = favs.map(s => `
      <div class="service-card" style="position:relative;">
        <span onclick="event.stopPropagation(); toggleFavorite('${s.id}')" style="position:absolute; top:6px; left:6px; font-size:14px; cursor:pointer;">❤️</span>
        <div onclick="showScreen('${s.screen}')" style="display:flex; flex-direction:column; align-items:center; gap:8px; cursor:pointer;">
          <div class="service-icon" style="background:${s.bg};">${s.icon}</div>
          <div>
            <h3>${s.title}</h3>
            <p>${s.sub}</p>
          </div>
        </div>
      </div>
    `).join('');
  }

  function toggleFavorite(id) {
    const idx = favoriteIds.indexOf(id);
    if (idx !== -1) favoriteIds.splice(idx, 1);
    if (typeof saveFavorites === 'function') saveFavorites();
    renderFavorites();
    showToast('از علاقه‌مندی‌ها حذف شد');
  }


/* =========================================================
   Profile
   توجه: تابع saveProfile() اکنون به‌صورت واحد در core/storage.js
   تعریف شده (مدیریت چندحسابی بر اساس شماره موبایل). برای جلوگیری
   از تداخل و override ناخواسته، نسخهٔ تکراری این تابع از این فایل
   حذف شده است.
========================================================= */
  function toggleProfileDarkMode(el) {
    el.classList.toggle('on');
    if (window.soundManager && typeof window.soundManager.playTick === 'function') {
      window.soundManager.playTick();
    }
    applyTheme(!el.classList.contains('on'));
  }

  function toggleProfileSound(el) {
    if (!window.soundManager) return;
    const newState = window.soundManager.toggleSound();
    el.classList.toggle('on', newState);
    const isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');
    showToast(newState
      ? (isEn ? 'Sound effects enabled' : 'افکت‌های صوتی فعال شد')
      : (isEn ? 'Sound effects disabled' : 'افکت‌های صوتی غیرفعال شد'));
  }

  function syncProfileSoundToggle() {
    const el = document.getElementById('profileSoundToggle');
    if (el && window.soundManager) {
      el.classList.toggle('on', window.soundManager.isEnabled());
    }
  }

  document.addEventListener('DOMContentLoaded', syncProfileSoundToggle);
  window.toggleProfileSound = toggleProfileSound;
  window.syncProfileSoundToggle = syncProfileSoundToggle;

  function toggleLanguage(el) {
    if (window.i18n && typeof window.i18n.toggleLanguage === 'function') {
      window.i18n.toggleLanguage();
      return;
    }
    const display = document.getElementById('langValueDisplay');
    const isFa = display ? display.textContent.trim() === 'فارسی' : true;
    if (display) display.textContent = isFa ? 'English' : 'فارسی';
    showToast(isFa ? 'Language changed to English' : 'زبان به فارسی تغییر یافت');
  }

