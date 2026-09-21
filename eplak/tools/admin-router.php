<?php
/* admin-router.php — فقط برای پیش‌نمایش زنده:
   ریشه‌ی پورت ادمین را مستقیماً به صفحه ورود هدایت می‌کند.
   بقیه درخواست‌ها عیناً از پوشه admin سرو می‌شوند (بدون تغییر در پروژه). */
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($path === '/' || $path === '') {
    header('Location: /login.php', true, 302);
    exit;
}
return false; // سرو فایل از docroot (پوشه admin)
