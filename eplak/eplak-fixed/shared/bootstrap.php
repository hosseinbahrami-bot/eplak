<?php
if (!defined('EPLAK_ROOT')) {
    define('EPLAK_ROOT', dirname(__DIR__));
}

function eplakIsHttpsRequest(): bool {
    if (!empty($_SERVER['HTTPS']) && strtolower((string) $_SERVER['HTTPS']) !== 'off') {
        return true;
    }
    $fwdProto = strtolower((string) ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ''));
    if ($fwdProto === 'https') {
        return true;
    }
    $fwdPort = (string) ($_SERVER['HTTP_X_FORWARDED_PORT'] ?? '');
    return $fwdPort === '443';
}

function eplakStartSession(string $name): void {
    if (session_status() === PHP_SESSION_NONE) {
        /* سازگاری با اجرا پشت پروکسی/پیش‌نمایشِ جاسازی‌شده (iframe):
           - SameSite=None; Secure اجازه می‌دهد کوکی در حالت جاسازی‌شده پذیرفته شود
           - اگر مرورگر کوکی شخص‌ثالث را مسدود کند، شناسه نشست از طریق URL
             (trans_sid) منتقل می‌شود تا ورود همچنان کار کند */
        /* اگر مرورگر کوکی را نپذیرد (مثلاً کوکی‌های شخص‌ثالث در حالت
           جاسازی‌شده مسدود باشند)، شناسه نشست به‌طور خودکار در URL منتقل
           می‌شود؛ در غیر این صورت نشانی‌ها تمیز می‌مانند. */
        /* هشدار امنیتی: انتقال شناسه‌ی نشست در URL (trans_sid) امکان
           Session Fixation و نشت شناسه در لاگ/Referer را فراهم می‌کرد؛
           غیرفعال شد. نشست فقط از طریق کوکی HttpOnly منتقل می‌شود. */
        @ini_set('session.use_cookies', '1');
        @ini_set('session.use_only_cookies', '1');
        @ini_set('session.use_trans_sid', '0');
        @ini_set('session.use_strict_mode', '1');
        @ini_set('session.cookie_httponly', '1');

        if (eplakIsHttpsRequest()) {
            session_set_cookie_params([
                'path'     => '/',
                'secure'   => true,
                'httponly' => true,
                'samesite' => 'None',
            ]);
        } else {
            session_set_cookie_params([
                'path'     => '/',
                'httponly' => true,
                'samesite' => 'Lax',
            ]);
        }
        session_name($name);
        session_start();
    }
}

function eplakSessionInUrlNeeded(): bool {
    $name = session_name();
    return session_status() !== PHP_SESSION_NONE
        && $name !== ''
        && session_id() !== ''
        && empty($_COOKIE[$name]);
}

/* هدایت سازگار با محیط‌هایی که کوکی را نمی‌پذیرند:
   اگر مرورگر کوکی نشست را نفرستاده باشد، شناسه نشست به نشانی مقصد افزوده
   می‌شود تا نشست بعد از هدایت هم حفظ گردد. در حالت عادی (کوکی فعال)
   نشانی‌ها دقیقاً همان قبل می‌مانند. */
function eplakRedirect(string $target): void {
    // فقط مسیرهای نسبی/داخلی — جلوگیری از Open Redirect
    if (preg_match('#^(https?:)?//#i', $target)) {
        $target = 'index.php';
    }
    header('Location: ' . $target);
    exit;
}

function eplakLoadConfig(): array {
    static $config = null;
    if (is_array($config)) {
        return $config;
    }

    $config = [];
    $cfgPath = __DIR__ . '/config.php';
    if (is_file($cfgPath)) {
        $loaded = include $cfgPath;
        if (is_array($loaded)) {
            $config = $loaded;
        }
    }

    return $config;
}

function eplakConfig(string $key, $default = null) {
    $envKey = strtoupper($key);
    $value = getenv($envKey);
    if ($value !== false && $value !== '') {
        return $value;
    }
    $config = eplakLoadConfig();
    $configKey = preg_match('/^DB_(.+)$/i', $key, $matches)
        ? strtolower($matches[1])
        : strtolower($key);
    if (array_key_exists($configKey, $config)) {
        return $config[$configKey];
    }
    return array_key_exists($key, $config) ? $config[$key] : $default;
}

function eplakEnsureColumn(PDO $pdo, string $table, string $column, string $definition): void {
    // نام جدول و ستون‌ها فقط از کد داخلی فراخوانی می‌شوند؛ backtick از SQL injection جلوگیری می‌کند.
    $table = preg_replace('/[^a-zA-Z0-9_]/', '', $table);
    $column = preg_replace('/[^a-zA-Z0-9_]/', '', $column);
    $stmt = $pdo->query("SHOW COLUMNS FROM `$table` LIKE '$column'");
    if (!$stmt->fetch()) {
        $pdo->exec("ALTER TABLE `$table` ADD COLUMN `$column` $definition");
    }
}

function eplakGetPdo(): PDO {
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    /* اطلاعات اتصال: اول متغیرهای محیطی، سپس فایل خصوصی shared/config.php
       (خارج از گیت — نمونه: shared/config.example.php). رمز عبور دیگر در کد نیست. */
    $host   = (string)eplakConfig('DB_HOST', '127.0.0.1');
    $user   = (string)eplakConfig('DB_USER', 'wigitali_root');
    $pass   = (string)eplakConfig('DB_PASS', '');
    $dbname = (string)eplakConfig('DB_NAME', 'wigitali_eplak-db');

    try {
        $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    } catch (\Throwable $e) {
        $pdo = new PDO("mysql:host=127.0.0.1;dbname=$dbname;charset=utf8mb4", $user, $pass, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS admin_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS tickets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_phone VARCHAR(20) NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        reply TEXT,
        category VARCHAR(100) DEFAULT '',
        department VARCHAR(255) DEFAULT '',
        priority VARCHAR(20) DEFAULT 'medium',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        phone VARCHAR(20) NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL DEFAULT '',
        address VARCHAR(500) DEFAULT '',
        nid VARCHAR(20) DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS notifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_phone VARCHAR(20) NOT NULL,
        title VARCHAR(255) NOT NULL,
        body TEXT NOT NULL,
        send_id INT NULL,
        read_flag TINYINT(1) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS notification_sends (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        body TEXT NOT NULL,
        target_type VARCHAR(50) NOT NULL DEFAULT 'all',
        recipients_count INT NOT NULL DEFAULT 0,
        created_by VARCHAR(100) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");

    /* نسخه‌های قبلی دیتابیس بعضی ستون‌های اعلان را نداشتند؛ migration باید روی
       دیتابیس موجود هم اجرا شود، نه فقط هنگام ساخت دیتابیس جدید. */
    foreach ([
        'user_phone' => "VARCHAR(20) NOT NULL DEFAULT ''",
        'title' => "VARCHAR(255) NOT NULL DEFAULT ''",
        'body' => "TEXT NULL",
        'send_id' => 'INT NULL',
        'read_flag' => 'TINYINT(1) NOT NULL DEFAULT 0',
        'created_at' => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    ] as $column => $definition) {
        eplakEnsureColumn($pdo, 'notifications', $column, $definition);
    }
    foreach ([
        'title' => "VARCHAR(255) NOT NULL DEFAULT ''",
        'body' => "TEXT NULL",
        'target_type' => "VARCHAR(50) NOT NULL DEFAULT 'all'",
        'recipients_count' => 'INT NOT NULL DEFAULT 0',
        'created_by' => 'VARCHAR(100) NULL',
        'created_at' => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    ] as $column => $definition) {
        eplakEnsureColumn($pdo, 'notification_sends', $column, $definition);
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS push_subscriptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_phone VARCHAR(20) NOT NULL,
        endpoint TEXT NOT NULL,
        endpoint_hash CHAR(64) NOT NULL,
        p256dh VARCHAR(255) NOT NULL,
        auth VARCHAR(255) NOT NULL,
        user_agent VARCHAR(255) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uq_push_endpoint_hash (endpoint_hash),
        KEY idx_push_user_phone (user_phone)
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(20) NOT NULL DEFAULT 'news',
        title VARCHAR(255) NOT NULL,
        summary VARCHAR(500) NULL,
        body TEXT NOT NULL,
        icon VARCHAR(32) NULL,
        image_url VARCHAR(1000) NULL,
        published TINYINT(1) NOT NULL DEFAULT 1,
        sort_order INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        KEY idx_news_type_published (type, published),
        KEY idx_news_sort (sort_order, id)
    )");

    foreach ([
        'type' => "VARCHAR(20) NOT NULL DEFAULT 'news'",
        'title' => "VARCHAR(255) NOT NULL DEFAULT ''",
        'summary' => 'VARCHAR(500) NULL',
        'body' => "TEXT NOT NULL",
        'icon' => 'VARCHAR(32) NULL',
        'image_url' => 'VARCHAR(1000) NULL',
        'published' => 'TINYINT(1) NOT NULL DEFAULT 1',
        'sort_order' => 'INT NOT NULL DEFAULT 0',
        'created_at' => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'updated_at' => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
    ] as $column => $definition) {
        eplakEnsureColumn($pdo, 'news', $column, $definition);
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS eplak_settings (
        setting_key VARCHAR(100) PRIMARY KEY,
        setting_value TEXT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )");

    $newsSeeded = $pdo->prepare('SELECT setting_value FROM eplak_settings WHERE setting_key = :key LIMIT 1');
    $newsSeeded->execute([':key' => 'news_defaults_seeded_v1']);
    if (!$newsSeeded->fetchColumn()) {
        $newsCount = (int)$pdo->query('SELECT COUNT(*) FROM news')->fetchColumn();
        if ($newsCount === 0) {
            $defaults = [
                [
                    'news',
                    'افتتاح پارک جدید در منطقه شمالی ورامین',
                    'پارک جدید شهر با امکانات ورزشی و فضای سبز گسترده افتتاح شد.',
                    'پارک جدید شهرداری ورامین با مساحت بیش از ۵ هکتار و امکاناتی شامل زمین‌های ورزشی، مسیر پیاده‌روی، فضای بازی کودکان و فضای سبز گسترده، آماده بهره‌برداری شهروندان عزیز شده است. این پروژه با مشارکت شهروندان و در راستای ارتقای کیفیت زندگی شهری اجرا شده است.',
                    '🌳', null, 1, 10
                ],
                [
                    'news',
                    'اطلاعیه نوبت‌دهی پرداخت عوارض نوسازی',
                    'مهلت پرداخت عوارض نوسازی سال جاری تا پایان خرداد ماه تمدید شد.',
                    'به اطلاع شهروندان محترم می‌رساند مهلت پرداخت عوارض نوسازی سال جاری تا پایان خرداد ماه تمدید گردیده است. شهروندان می‌توانند از طریق بخش «پرداخت عوارض» همین برنامه نسبت به پرداخت بدهی خود اقدام نمایند.',
                    '📋', null, 1, 20
                ],
                [
                    'news',
                    'برگزاری جشنواره فرهنگی شهر ورامین',
                    'جشنواره فرهنگی و هنری شهر با حضور هنرمندان محلی برگزار می‌شود.',
                    'شهرداری ورامین با همکاری اداره فرهنگ و ارشاد اسلامی، جشنواره فرهنگی و هنری شهر را با حضور هنرمندان محلی و برنامه‌های متنوع برای خانواده‌ها برگزار می‌کند. زمان و مکان دقیق برگزاری متعاقباً اعلام خواهد شد.',
                    '🎉', null, 1, 30
                ],
                [
                    'news',
                    'آغاز طرح بازآفرینی بافت فرسوده مرکز شهر',
                    'طرح نوسازی و بازآفرینی بافت فرسوده مرکز شهر آغاز شد.',
                    'با هدف ارتقای کیفیت بصری و کالبدی مرکز شهر، طرح بازآفرینی بافت فرسوده با همکاری شهرداری و سازمان نوسازی شهری آغاز شده و طی فازهای مختلف تا پایان سال ادامه خواهد داشت.',
                    '🏗️', null, 1, 40
                ],
                [
                    'tip',
                    'مسجد جامع ورامین',
                    'تنها نمونه کامل مساجد چهارایوانی ایران؛ شاهکاری از معماری دوران ایلخانی.',
                    'مسجد جامع ورامین، معروف به مسجد جمعه ورامین، یکی از کهن‌ترین و باشکوه‌ترین بناهای برجامانده از دوره ایلخانی در ایران است. ساخت آن در روزگار سلطان محمد خدابنده (الجایتو) آغاز شد و در دوران فرزند و جانشین او، ابوسعید بهادرخان، در سال ۷۲۲ هجری قمری به پایان رسید.

این مسجد با نقشه‌ای مستطیلی به ابعاد تقریبی ۶۶ در ۴۳ متر، تنها نمونه کامل و یکپارچه مساجد چهارایوانی در ایران است؛ سبکی که از سلجوقیان آغاز شده و در این بنا به اوج پختگی خود رسیده است. گنبدخانه مسجد با گذر از فیل‌پوش‌ها از مربع به هشت‌ضلعی و سپس شانزده‌ضلعی، به گنبدی باشکوه ختم می‌شود.

سردر بلند و کشیده ورودی، کاشی‌کاری‌های معرق فیروزه‌ای و لاجوردی، گچ‌بری‌های ظریف گرداگرد محراب و کتیبه‌های تاریخی به خط ثلث و کوفی، این بنا را به یکی از مهم‌ترین آثار هنری و معماری دوران اسلامی ایران بدل کرده‌اند. در دوران معاصر، استاد محمدکریم پیرنیا، پدر معماری سنتی ایران، مرمت این اثر گران‌بها را بر عهده داشت.',
                    '🏛️', 'assets/img/varamin-mosque.jpg', 1, 10
                ],
                [
                    'tip',
                    'برج علاءالدوله ورامین',
                    'برج آرامگاهی استوانه‌ای با گنبدی مخروطی بلند، یادگار دوره ایلخانی.',
                    'برج علاءالدوله، که با نام برج علاءالدین نیز شناخته می‌شود، یکی از قدیمی‌ترین برج‌های آرامگاهی به‌جامانده از ایران است. این بنا در سال ۶۸۸ هجری قمری، در اواخر سده هفتم هجری، به دستور فخرالدین بر فراز آرامگاه پدرش، حسن علاءالدوله، حاکم وقت شهر ری، ساخته شد.

برج از بدنه‌ای استوانه‌ای آجری با چین‌خوردگی‌های عمودی شکل گرفته که در ارتفاعی نزدیک به ۱۷ متر به گنبدی مخروطی و بلند ختم می‌شود؛ ترکیبی که سیمای منحصربه‌فرد و شناخته‌شده این بنا را در میدان مرکزی ورامین رقم زده است. در محل اتصال بخش استوانه‌ای به مخروطی، کتیبه‌ای آجری با خطوط کوفی برگ‌دار حک شده که نام بانی، تاریخ بنا و دعایی برای آرامش روح علاءالدوله را در خود دارد.

نمای بیرونی برج با شمسه‌های آجری و کاشی‌های فیروزه‌ای و لاجوردی تزئین شده است. این اثر در ۱۵ دی ماه ۱۳۱۰ با شماره ثبت ۱۷۷ در فهرست آثار ملی ایران به ثبت رسید و امروزه یکی از نمادهای شناخته‌شده شهر ورامین و مقصد علاقه‌مندان به تاریخ و معماری ایرانی است.',
                    '🕌', 'assets/img/varamin-tower.jpg', 1, 20
                ],
            ];
            $insertNews = $pdo->prepare('INSERT INTO news (type, title, summary, body, icon, image_url, published, sort_order) VALUES (:type, :title, :summary, :body, :icon, :image_url, :published, :sort_order)');
            foreach ($defaults as $item) {
                $insertNews->execute([
                    ':type' => $item[0], ':title' => $item[1], ':summary' => $item[2], ':body' => $item[3],
                    ':icon' => $item[4], ':image_url' => $item[5], ':published' => $item[6], ':sort_order' => $item[7],
                ]);
            }
        }
        $markSeeded = $pdo->prepare('INSERT INTO eplak_settings (setting_key, setting_value) VALUES (:key, :value) ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)');
        $markSeeded->execute([':key' => 'news_defaults_seeded_v1', ':value' => '1']);
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_phone VARCHAR(20) NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        category VARCHAR(100) NOT NULL,
        department VARCHAR(255) DEFAULT '',
        sub_department VARCHAR(255) DEFAULT '',
        location VARCHAR(500) DEFAULT '',
        status VARCHAR(50) DEFAULT 'pending',
        reply TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS report_media (
        id INT AUTO_INCREMENT PRIMARY KEY,
        report_id INT NOT NULL,
        user_phone VARCHAR(20) NOT NULL,
        media_type VARCHAR(10) NOT NULL,
        file_path VARCHAR(500) NOT NULL,
        original_name VARCHAR(255) DEFAULT '',
        mime_type VARCHAR(100) DEFAULT '',
        file_size INT UNSIGNED NOT NULL DEFAULT 0,
        duration_seconds DECIMAL(6,3) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        KEY idx_report_media_report (report_id),
        KEY idx_report_media_phone (user_phone)
    )");

    // مهاجرت غیرمخرب برای نصب‌هایی که جدول رسانه را قبلاً با ستون‌های ناقص ساخته‌اند.
    $mediaColumns = [
        'user_phone' => 'VARCHAR(20) NOT NULL',
        'media_type' => 'VARCHAR(10) NOT NULL',
        'file_path' => 'VARCHAR(500) NOT NULL',
        'original_name' => 'VARCHAR(255) DEFAULT ""',
        'mime_type' => 'VARCHAR(100) DEFAULT ""',
        'file_size' => 'INT UNSIGNED NOT NULL DEFAULT 0',
        'duration_seconds' => 'DECIMAL(6,3) NULL',
        'created_at' => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    ];
    foreach ($mediaColumns as $column => $definition) {
        $safeColumn = preg_replace('/[^a-zA-Z0-9_]/', '', $column);
        $col = $pdo->query("SHOW COLUMNS FROM report_media LIKE '$safeColumn'")->fetch();
        if (!$col) {
            $pdo->exec("ALTER TABLE report_media ADD COLUMN `$safeColumn` $definition");
        }
    }

    $pdo->exec("CREATE TABLE IF NOT EXISTS departments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        parent_id INT NULL,
        sort_order INT NOT NULL DEFAULT 0,
        is_active TINYINT(1) NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uq_department_name_parent (name, parent_id),
        KEY idx_department_parent (parent_id),
        CONSTRAINT fk_department_parent FOREIGN KEY (parent_id) REFERENCES departments(id) ON DELETE CASCADE
    )");

    $defaultDepartments = [
        'حوزه شهردار' => ['دفتر شهردار', 'روابط عمومی و امور بین‌الملل', 'بازرسی و ارزیابی عملکرد', 'حراست', 'امور حقوقی', 'شورای مشاوران'],
        'معاونت اداری و مالی' => ['منابع انسانی', 'امور اداری', 'امور مالی و حسابداری', 'بودجه و برنامه‌ریزی', 'تدارکات و پشتیبانی', 'فناوری اطلاعات (IT)'],
        'معاونت فنی و عمرانی' => ['طراحی و اجرای پروژه‌های عمرانی', 'ساخت و نگهداری معابر', 'پل‌ها و تونل‌ها', 'ساختمان‌های عمومی', 'تأسیسات شهری'],
        'معاونت شهرسازی و معماری' => ['صدور پروانه ساختمانی', 'پایان کار ساختمان', 'کنترل و نظارت ساختمانی', 'طرح‌های توسعه شهری', 'کمیسیون‌های شهرسازی'],
        'معاونت خدمات شهری' => ['نظافت شهری', 'مدیریت پسماند', 'فضای سبز', 'زیباسازی شهر', 'آرامستان‌ها', 'کنترل حیوانات شهری'],
        'معاونت حمل‌ونقل و ترافیک' => ['مدیریت ترافیک', 'پارکینگ‌ها', 'حمل‌ونقل عمومی', 'پایانه‌ها', 'ایمنی و علائم راهنمایی'],
        'معاونت فرهنگی و اجتماعی' => ['فرهنگسراها', 'کتابخانه‌ها', 'امور جوانان', 'امور بانوان', 'مشارکت‌های مردمی', 'ورزش همگانی'],
        'معاونت برنامه‌ریزی و توسعه' => ['آمار و اطلاعات', 'پژوهش و نوآوری', 'مدیریت پروژه', 'هوشمندسازی شهر'],
        'سازمان‌ها و شرکت‌های وابسته' => ['سازمان مدیریت پسماند', 'سازمان آتش‌نشانی و خدمات ایمنی', 'سازمان پارک‌ها و فضای سبز', 'سازمان زیباسازی', 'سازمان حمل‌ونقل بار و مسافر', 'سازمان میادین و بازارها', 'سازمان آرامستان‌ها', 'سازمان فناوری اطلاعات و ارتباطات', 'سازمان فرهنگی، اجتماعی و ورزشی', 'سازمان سرمایه‌گذاری و مشارکت‌های مردمی', 'شرکت بهره‌برداری مترو (در شهرهای دارای مترو)', 'شرکت واحد اتوبوسرانی', 'شرکت نوسازی و بهسازی شهری'],
    ];

    $count = (int)$pdo->query('SELECT COUNT(*) as count FROM departments')->fetch()['count'];
    if ($count === 0) {
        foreach ($defaultDepartments as $parentName => $children) {
            $parentStmt = $pdo->prepare('INSERT INTO departments (name, parent_id, sort_order, is_active) VALUES (:name, NULL, :sort_order, 1)');
            $parentStmt->execute([':name' => $parentName, ':sort_order' => 0]);
            $parentId = (int)$pdo->lastInsertId();

            foreach ($children as $index => $childName) {
                $childStmt = $pdo->prepare('INSERT INTO departments (name, parent_id, sort_order, is_active) VALUES (:name, :parent_id, :sort_order, 1)');
                $childStmt->execute([
                    ':name' => $childName,
                    ':parent_id' => $parentId,
                    ':sort_order' => $index + 1,
                ]);
            }
        }
    }

    foreach (['reply', 'department', 'sub_department', 'location'] as $column) {
        $col = $pdo->query("SHOW COLUMNS FROM reports LIKE '$column'")->fetch();
        if (!$col) {
            if ($column === 'reply') {
                $pdo->exec('ALTER TABLE reports ADD COLUMN reply TEXT NULL');
            } elseif ($column === 'department') {
                $pdo->exec('ALTER TABLE reports ADD COLUMN department VARCHAR(255) DEFAULT ""');
            } elseif ($column === 'sub_department') {
                $pdo->exec('ALTER TABLE reports ADD COLUMN sub_department VARCHAR(255) DEFAULT ""');
            } else {
                $pdo->exec('ALTER TABLE reports ADD COLUMN location VARCHAR(500) DEFAULT ""');
            }
        }
    }

    foreach (['category', 'department', 'priority'] as $column) {
        $col = $pdo->query("SHOW COLUMNS FROM tickets LIKE '$column'")->fetch();
        if (!$col) {
            if ($column === 'category') {
                $pdo->exec('ALTER TABLE tickets ADD COLUMN category VARCHAR(100) DEFAULT ""');
            } elseif ($column === 'department') {
                $pdo->exec('ALTER TABLE tickets ADD COLUMN department VARCHAR(255) DEFAULT ""');
            } else {
                $pdo->exec('ALTER TABLE tickets ADD COLUMN priority VARCHAR(20) DEFAULT "medium"');
            }
        }
    }

    $departmentColumns = [
        'slug' => 'VARCHAR(255) NULL',
        'code' => 'VARCHAR(50) NULL',
        'description' => 'TEXT NULL',
        'icon' => 'VARCHAR(50) NULL',
        'color' => 'VARCHAR(7) DEFAULT "#0f766e"',
        'updated_at' => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
    ];
    foreach ($departmentColumns as $column => $definition) {
        $col = $pdo->query("SHOW COLUMNS FROM departments LIKE '$column'")->fetch();
        if (!$col) {
            $pdo->exec("ALTER TABLE departments ADD COLUMN `$column` $definition");
        }
    }

    $adminCount = $pdo->query('SELECT COUNT(*) as count FROM admin_users')->fetch();
    if ((int)$adminCount['count'] === 0) {
        $defaultHash = password_hash('admin123', PASSWORD_DEFAULT);
        $stmt = $pdo->prepare('INSERT INTO admin_users (username, password_hash, role) VALUES (:username, :password_hash, :role)');
        $stmt->execute([
            ':username' => 'admin',
            ':password_hash' => $defaultHash,
            ':role' => 'super_admin',
        ]);
    }

    return $pdo;
}
