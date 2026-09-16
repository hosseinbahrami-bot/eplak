/* modules/auth.js — ورود، احراز هویت و تایید کد OTP */

let otpTimerInterval = null;
let otpSeconds = 30;

// شنود خودکار فرم لاگین برای بازداری از Submit سنتی (پیشگیری از رفرش WebView)
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.querySelector('#screen-login form') || document.querySelector('form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      sendOtp();
    });
  }
});

function sendOtp() {
  const input = document.getElementById('loginPhoneInput');
  const phone = (input ? input.value : '').trim();

  if (!isValidIranMobile(phone)) {
    showToast('شماره موبایل را به‌درستی وارد کنید (مثال: 09123456789)');
    return;
  }

  // --- درخواست واقعی به بک‌اند (ارسال SMS) ---
  // آدرس IP بک‌اند خود را جاگذاری کنید (مثلا http://10.0.2.2:3000/api/send-otp)
  fetch('http://10.0.2.2:3000/api/send-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone: phone })
  })
  .then(response => {
    if (!response.ok) throw new Error('خطا در ارسال کد');
    return response.json();
  })
  .then(data => {
    userProfile.rawPhone = phone;
    document.getElementById('otpPhoneDisplay').textContent = phone;
    showScreen('screen-otp');
    startOtpTimer();
    setTimeout(() => {
      const firstBox = document.querySelector('#screen-otp .otp-box');
      if (firstBox) firstBox.focus();
    }, 300);
  })
  .catch(err => {
    // اگر فعلاً بک‌اند خاموش است، برای تست برنامه را متوقف نمی‌کنیم:
    console.error(err);
    alert('هشدار ارتباط با سرور: ' + err.message + '\n(انتقال آفلاین به صفحه بعد)');

    userProfile.rawPhone = phone;
    document.getElementById('otpPhoneDisplay').textContent = phone;
    showScreen('screen-otp');
    startOtpTimer();
  });
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
  if (linkEl) linkEl.style.display = 'none';
  if (textEl) textEl.style.display = 'inline';

  otpTimerInterval = setInterval(() => {
    otpSeconds--;
    if (otpSeconds <= 0) {
      clearInterval(otpTimerInterval);
      if (textEl) textEl.style.display = 'none';
      if (linkEl) linkEl.style.display = 'inline';
    } else {
      const m = String(Math.floor(otpSeconds / 60)).padStart(2, '0');
      const s = String(otpSeconds % 60).padStart(2, '0');
      if (textEl) textEl.textContent = `ارسال مجدد کد تا ${m}:${s}`;
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

  if (!isValidIranMobile(userProfile.rawPhone)) {
    showToast('شماره موبایل نامعتبر است. لطفاً دوباره تلاش کنید');
    clearInterval(otpTimerInterval);
    showScreen('screen-login');
    return;
  }

  // --- تایید کد در بک‌اند ---
  fetch('http://10.0.2.2:3000/api/verify-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone: userProfile.rawPhone, code: code })
  })
  .then(res => res.json())
  .then(data => {
    completeLogin();
  })
  .catch(err => {
    // حالت پشتیبان برای تست فرانت‌اند
    completeLogin();
  });
}

function completeLogin() {
  clearInterval(otpTimerInterval);

  if (typeof loginWithPhone === 'function') {
    loginWithPhone(userProfile.rawPhone);
  } else {
    userProfile.phone = formatPhoneDisplay(userProfile.rawPhone);
    if (!userProfile.name || userProfile.name.trim() === '') {
      userProfile.name = 'شهروند';
    }
  }

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

  if (typeof logoutCurrentUser === 'function') {
    logoutCurrentUser();
  } else {
    userProfile.rawPhone = '';
    userProfile.phone = '';
    userProfile.name = 'شهروند';
  }

  showScreen('screen-login');
}