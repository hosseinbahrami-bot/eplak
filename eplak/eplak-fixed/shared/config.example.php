<?php
/* shared/config.php — تنظیمات خصوصی سرور (این فایل را کپی کرده و config.php بنامید؛ در گیت قرار نمی‌گیرد)
   یا به‌جای آن متغیرهای محیطی DB_HOST / DB_USER / DB_PASS / DB_NAME را تنظیم کنید. */
return [
    'host' => '127.0.0.1',
    'user' => 'wigitali_root',
    'pass' => 'CHANGE_ME',
    'name' => 'wigitali_eplak-db',

    /* اختیاری: آدرس پایه‌ی نصب، مانند https://eplak.ir/eplak-fixed.
       برای ساخت URL رسانه‌ها در نصب‌هایی که مسیر خودکار قابل تشخیص نیست. */
    'app_base_url' => '',
    /* بهتر است این مسیر در production خارج از webroot باشد؛ در غیر این صورت
       uploads/reports با .htaccess فقط از طریق endpoint محافظت‌شده خوانده می‌شود. */
    'report_media_storage_path' => '',

    /* برای پوش واقعی مرورگر؛ کلیدها را با web-push generate-vapid-keys
       بسازید و هرگز کلید خصوصی را در گیت قرار ندهید. */
    'vapid_public_key' => '',
    'vapid_private_key' => '',
    'vapid_subject' => 'mailto:admin@example.com',
];
