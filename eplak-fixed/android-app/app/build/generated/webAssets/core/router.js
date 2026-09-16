/* core/router.js — مدیریت نمایش صفحات (showScreen) و تم روز/شب */
/* استخراج‌شده عیناً از فایل اصلی app_01.html بدون تغییر منطق */

  /* =========================================================
     Screen Navigation
  ========================================================= */
  function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const target = document.getElementById(id);
    if (!target) return;
    target.classList.add('active');
    onScreenShow(id);
  }

  function onScreenShow(id) {
    /* اگر از پیشخوان خارج شدیم، تایمر ساعت را متوقف کن */
    if (id !== 'screen-dashboard' && typeof _dashClockTimer !== 'undefined' && _dashClockTimer) {
      clearInterval(_dashClockTimer);
      _dashClockTimer = null;
    }
    switch (id) {
      case 'screen-home':
        break;
      case 'screen-profile':
        if (typeof renderProfileReportsSummary === 'function') renderProfileReportsSummary();
        if (typeof renderProfileTrackingQuick === 'function') renderProfileTrackingQuick();
        break;
      case 'screen-reports': renderReportsList('all'); break;
      case 'screen-services': renderServices(); break;
      case 'screen-dashboard': renderDashboard(); break;
      case 'screen-track': renderTrackRecent(); break;
      case 'screen-news': renderNewsList(); break;
      case 'screen-payment': renderPaymentList(); break;
      case 'screen-map': renderMapPlaces(); break;
      case 'screen-notifications': renderNotifications(); break;
      case 'screen-favorites': renderFavorites(); break;
      case 'screen-profile-edit':
        if (typeof fillEditProfileForm === 'function') {
          fillEditProfileForm();
        } else {
          document.getElementById('editNameInput').value = userProfile.name;
        }
        break;
    }
  }

  function showToast(msg) {
    const toast = document.getElementById('globalToast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => toast.classList.remove('show'), 2200);
  }


  /* =========================================================
     THEME TOGGLE: day / night
  ========================================================= */
  let isDay = false;

  function applyTheme(day) {
    isDay = day;
    if (day) {
      document.documentElement.classList.add('day');
    } else {
      document.documentElement.classList.remove('day');
    }
    document.querySelectorAll('.theme-toggle button').forEach(btn => {
      const isSun = btn.textContent.trim() === '☀️';
      const isMoon = btn.textContent.trim() === '🌙';
      if (day && isSun) btn.classList.add('active');
      else if (day && isMoon) btn.classList.remove('active');
      else if (!day && isMoon) btn.classList.add('active');
      else if (!day && isSun) btn.classList.remove('active');
    });
    const profileToggle = document.getElementById('profileDarkToggle');
    if (profileToggle) profileToggle.classList.toggle('on', !day);
  }

  document.querySelectorAll('.theme-toggle button').forEach(btn => {
    btn.addEventListener('click', function() {
      const clickedSun = this.textContent.trim() === '☀️';
      applyTheme(clickedSun);
    });
  });

  /* هماهنگ‌سازی اولیه‌ی وضعیت تم با دکمه‌ی فعالِ از پیش‌رندرشده در HTML
     (برای جلوگیری از ناهماهنگی بین کلاس day/night و خورشید/ماه هیرو بنر خانه) */
  document.addEventListener('DOMContentLoaded', () => {
    const activeBtn = document.querySelector('.theme-toggle button.active');
    if (activeBtn) {
      applyTheme(activeBtn.textContent.trim() === '☀️');
    }
  });
