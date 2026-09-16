/* app.js — نقطه ورود اصلی اپلیکیشن ای‌پلاک */
/*
   این فایل آخرین اسکریپتی است که در index.html لود می‌شود؛ یعنی در این
   مرحله همه‌ی فایل‌های core/*.js و modules/*.js (و توابع داخل آن‌ها)
   از قبل تعریف شده‌اند. به همین دلیل بخش «Init» که در فایل اصلی
   app_01.html در انتهای تگ <script> قرار داشت (و به applyTheme و
   updateNotifDot از بخش‌های مختلف نیاز دارد) عیناً به این‌جا منتقل شده
   است تا به همان ترتیب اجرای فایل اصلی (همه چیز تعریف شود، سپس اجرا شود)
   وفادار بمانیم؛ هیچ مقدار یا منطقی تغییر نکرده است.
*/

/* =========================================================
   Init
========================================================= */
applyTheme(false);
updateNotifDot();
/* =========================================================
   کد عیب‌یابی عمومی (Debug)
========================================================= */

// ۱. گرفتن تمام کدهای خطا در کل صفحه
window.onerror = function (msg, url, lineNo, columnNo, error) {
    alert("خطای جاوااسکریپت:\n" + msg + "\nدر خط: " + lineNo);
    return false;
};

// ۲. گرفتن خطاهای مربوط به درخواست‌های شبکه (Promise / Fetch)
window.addEventListener('unhandledrejection', function (event) {
    alert("خطای درخواست شبکه (API):\n" + event.reason);
});

// ۳. تست کلیک روی دکمه‌ها
document.addEventListener('click', function(e) {
    // اگر روی دکمه یا لینکی کلیک شد خبر بده
    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
        console.log("دکمه کلیک شد:", e.target.innerText);
    }
});
// --- کد عیب‌یابی مستقیم روی صفحه ---
window.onerror = function (msg, url, lineNo) {
    document.body.innerHTML += "<div style='color:red; background:white; position:fixed; bottom:0; width:100%; z-index:9999;'>خطا: " + msg + " (خط " + lineNo + ")</div>";
    return false;
};

// نمایش درخواست‌های API
const originalFetch = window.fetch;
window.fetch = function() {
    console.log("درخواست ارسال شد به:", arguments[0]);
    return originalFetch.apply(this, arguments).catch(err => {
        document.body.innerHTML += "<div style='color:blue; background:yellow; position:fixed; bottom:50px; width:100%; z-index:9999;'>ارور شبکه: " + err + "</div>";
        throw err;
    });
};
