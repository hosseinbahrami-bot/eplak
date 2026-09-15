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
    applyTheme(!el.classList.contains('on'));
  }

  function toggleLanguage(el) {
    const display = document.getElementById('langValueDisplay');
    const isFa = display.textContent.trim() === 'فارسی';
    display.textContent = isFa ? 'English' : 'فارسی';
    showToast(isFa ? 'Language set to English (نمایشی)' : 'زبان به فارسی تغییر یافت');
  }

