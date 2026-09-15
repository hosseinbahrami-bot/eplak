/* modules/auth.js — ورود، احراز هویت و تایید کد OTP */
/* استخراج‌شده عیناً از فایل اصلی app_01.html بدون تغییر منطق */

  /* =========================================================
     Login / OTP
  ========================================================= */
  let otpTimerInterval = null;
  let otpSeconds = 30;

  function sendOtp() {
    const input = document.getElementById('loginPhoneInput');
    const phone = (input.value || '').trim();

    if (!isValidIranMobile(phone)) {
      showToast('شماره موبایل را به‌درستی وارد کنید (مثال: 09123456789)');
      return;
    }

    userProfile.rawPhone = phone;
    document.getElementById('otpPhoneDisplay').textContent = phone;
    showScreen('screen-otp');
    startOtpTimer();
    setTimeout(() => {
      const firstBox = document.querySelector('#screen-otp .otp-box');
      if (firstBox) firstBox.focus();
    }, 300);
  }

  function otpAutoNext(el) {
    if (el.value.length === 1) {
      const next = el.nextElementSibling;
      if (next && next.classList.contains('otp-box')) next.focus();
    }
  }

  function startOtpTimer() {
    clearInterval(otpTimerInterval);
    otpSeconds = 30;
    const textEl = document.getElementById('otpTimerText');
    const linkEl = document.getElementById('otpResendLink');
    linkEl.style.display = 'none';
    textEl.style.display = 'inline';
    otpTimerInterval = setInterval(() => {
      otpSeconds--;
      if (otpSeconds <= 0) {
        clearInterval(otpTimerInterval);
        textEl.style.display = 'none';
        linkEl.style.display = 'inline';
      } else {
        const m = String(Math.floor(otpSeconds / 60)).padStart(2, '0');
        const s = String(otpSeconds % 60).padStart(2, '0');
        textEl.textContent = `ارسال مجدد کد تا ${m}:${s}`;
      }
    }, 1000);
  }

  function resendOtp() {
    showToast('کد تایید مجدداً ارسال شد');
    startOtpTimer();
    document.querySelectorAll('#screen-otp .otp-box').forEach(b => b.value = '');
  }

function verifyOtp() {
    const boxes = document.querySelectorAll('#screen-otp .otp-box');
    let code = '';

    boxes.forEach(b => code += b.value);

    if (code.length !== 4) {
        showToast('کد ۴ رقمی را کامل وارد کنید');
        return;
    }

    // اطمینان مضاعف از معتبر بودن شماره (دفاع در عمق؛ علاوه بر بررسی sendOtp)
    if (!isValidIranMobile(userProfile.rawPhone)) {
        showToast('شماره موبایل نامعتبر است. لطفاً دوباره تلاش کنید');
        clearInterval(otpTimerInterval);
        showScreen('screen-login');
        return;
    }

    clearInterval(otpTimerInterval);

    // ذخیرهٔ شماره موبایل به‌عنوان کاربر فعلی + بارگذاری/ساخت پروفایل مخصوص این شماره
    // (نام و عکس هر شماره جدا و مستقل نگه‌داری می‌شود — core/storage.js)
    if (typeof loginWithPhone === 'function') {
        loginWithPhone(userProfile.rawPhone);
    } else {
        // fallback در صورت نبود storage.js (نباید رخ دهد)
        userProfile.phone = formatPhoneDisplay(userProfile.rawPhone);
        if (!userProfile.name || userProfile.name.trim() === '') {
            userProfile.name = 'شهروند';
        }
    }

    // نمایش در پروفایل
    document.getElementById('profilePhoneDisplay').textContent = userProfile.phone;
    document.getElementById('profileNameDisplay').textContent = userProfile.name;

    showScreen('screen-home');
    showToast('ورود با موفقیت انجام شد');
}
  function formatPhoneDisplay(raw) {
    if (!raw || raw.length !== 11) return raw;
    return raw.slice(0, 4) + ' ' + raw.slice(4, 7) + ' ' + raw.slice(7);
  }

  function logoutUser() {
    clearInterval(otpTimerInterval);
    document.querySelectorAll('#screen-otp .otp-box').forEach(b => b.value = '');
    document.getElementById('loginPhoneInput').value = '';

    // پاک‌کردن session فعلی — پروفایل (نام/عکس) همین شماره برای ورود بعدی حفظ می‌شود
    if (typeof logoutCurrentUser === 'function') {
        logoutCurrentUser();
    } else {
        userProfile.rawPhone = '';
        userProfile.phone = '';
        userProfile.name = 'شهروند';
    }

    showScreen('screen-login');
  }

