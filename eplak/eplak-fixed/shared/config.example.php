<?php
/* shared/config.php — تنظیمات خصوصی سرور (این فایل را کپی کرده و config.php بنامید؛ در گیت قرار نمی‌گیرد)
   یا به‌جای آن متغیرهای محیطی DB_HOST / DB_USER / DB_PASS / DB_NAME را تنظیم کنید. */
return [
    'host' => '127.0.0.1',
    'user' => 'wigitali_root',
    'pass' => 'CHANGE_ME',
    'name' => 'wigitali_eplak-db',

    /* برای پوش واقعی مرورگر؛ کلیدها را با web-push generate-vapid-keys
       بسازید و هرگز کلید خصوصی را در گیت قرار ندهید. */
    'vapid_public_key' => '',
    'vapid_private_key' => '',
    'vapid_subject' => 'mailto:admin@example.com',
];
