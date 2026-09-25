<?php
require_once __DIR__ . '/auth.php';
require_once __DIR__ . '/includes/functions.php';

$currentAdminId = (int)($_SESSION['admin_id'] ?? 0);
$currentAdminStmt = $pdo->prepare('SELECT id, username, role FROM admin_users WHERE id = :id LIMIT 1');
$currentAdminStmt->execute([':id' => $currentAdminId]);
$currentAdmin = $currentAdminStmt->fetch();

if (!$currentAdmin) {
    eplakRedirect('logout.php');
}

$message = '';
$messageType = 'danger';
$formUsername = (string)$currentAdmin['username'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    eplakRequireCsrf();

    $formUsername = trim((string)($_POST['username'] ?? ''));
    $currentPassword = (string)($_POST['current_password'] ?? '');
    $newPassword = (string)($_POST['new_password'] ?? '');
    $confirmPassword = (string)($_POST['confirm_password'] ?? '');

    if ($formUsername === '' || !preg_match('/^[\p{L}\p{N}_.@-]{3,100}$/u', $formUsername)) {
        $message = '⚠️ نام کاربری باید بین ۳ تا ۱۰۰ کاراکتر باشد و فقط شامل حروف، عدد، نقطه، خط تیره، زیرخط یا @ باشد.';
    } elseif ($currentPassword === '') {
        $message = '⚠️ برای ثبت تغییرات، رمز عبور فعلی را وارد کنید.';
    } else {
        $check = $pdo->prepare('SELECT password_hash FROM admin_users WHERE id = :id LIMIT 1');
        $check->execute([':id' => $currentAdminId]);
        $passwordHash = (string)$check->fetchColumn();

        if ($passwordHash === '' || !password_verify($currentPassword, $passwordHash)) {
            $message = '❌ رمز عبور فعلی صحیح نیست.';
        } elseif ($newPassword !== '' && strlen($newPassword) < 8) {
            $message = '⚠️ رمز عبور جدید باید حداقل ۸ کاراکتر باشد.';
        } elseif ($newPassword !== '' && $newPassword !== $confirmPassword) {
            $message = '⚠️ تکرار رمز عبور جدید با آن یکسان نیست.';
        } else {
            $duplicate = $pdo->prepare('SELECT id FROM admin_users WHERE username = :username AND id <> :id LIMIT 1');
            $duplicate->execute([':username' => $formUsername, ':id' => $currentAdminId]);
            if ($duplicate->fetch()) {
                $message = '⚠️ این نام کاربری قبلاً برای مدیر دیگری ثبت شده است.';
            } else {
                if ($newPassword !== '') {
                    $update = $pdo->prepare('UPDATE admin_users SET username = :username, password_hash = :password_hash WHERE id = :id');
                    $update->execute([
                        ':username' => $formUsername,
                        ':password_hash' => password_hash($newPassword, PASSWORD_DEFAULT),
                        ':id' => $currentAdminId,
                    ]);
                } else {
                    $update = $pdo->prepare('UPDATE admin_users SET username = :username WHERE id = :id');
                    $update->execute([':username' => $formUsername, ':id' => $currentAdminId]);
                }

                session_regenerate_id(true);
                $_SESSION['admin_username'] = $formUsername;
                $currentAdmin['username'] = $formUsername;
                $message = $newPassword !== ''
                    ? '✅ نام کاربری و رمز عبور با موفقیت تغییر کرد.'
                    : '✅ نام کاربری با موفقیت تغییر کرد.';
                $messageType = 'success';
                $_POST = [];
            }
        }
    }
}
?>
<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>تنظیمات حساب مدیر</title>
  <link rel="stylesheet" href="assets/style.css?v=8">
  <link rel="stylesheet" href="assets/fontawesome/css/all.min.css">
  <script src="assets/theme.js?v=8"></script>
  <script src="assets/persian-digits.js?v=8"></script>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <img class="logo-light" src="assets/img/logo.png" alt="ای‌پلاک">
        <img class="logo-dark" src="assets/img/logo-light.png" alt="ای‌پلاک">
      </div>
      <nav>
        <a href="index.php"><i class="fas fa-chart-pie"></i> <span>داشبورد</span></a>
        <a href="reports.php"><i class="fas fa-flag"></i> <span>گزارش‌ها</span></a>
        <a href="tickets.php"><i class="fas fa-ticket-alt"></i> <span>تیکت‌ها</span></a>
        <a href="users.php"><i class="fas fa-users"></i> <span>کاربران</span></a>
        <a href="departments.php"><i class="fas fa-sitemap"></i> <span>واحدها</span></a>
        <a href="news.php"><i class="fas fa-newspaper"></i> <span>اخبار و دانستنی‌ها</span></a>
        <a href="notifications.php"><i class="fas fa-bell"></i> <span>ارسال اعلان</span></a>
        <a href="export.php"><i class="fas fa-file-excel"></i> <span>خروجی اکسل</span></a>
        <a class="active" href="settings.php"><i class="fas fa-cog"></i> <span>تنظیمات</span></a>
        <a href="logout.php"><i class="fas fa-sign-out-alt"></i> <span>خروج</span></a>
      </nav>
    </aside>

    <main class="main">
      <header class="topbar">
        <div class="topbar-left">
          <h1><i class="fas fa-user-shield" style="color:var(--primary-500); margin-left:12px;"></i> تنظیمات حساب مدیر</h1>
          <p>تغییر امن نام کاربری و رمز عبور پنل مدیریت</p>
        </div>
      </header>

      <?php if ($message): ?>
        <div class="alert alert-<?= htmlspecialchars($messageType, ENT_QUOTES, 'UTF-8') ?>" style="margin:0 24px 16px;">
          <?= htmlspecialchars($message, ENT_QUOTES, 'UTF-8') ?>
        </div>
      <?php endif; ?>

      <section class="panel" style="margin:0 24px 24px; max-width:760px;">
        <h2><i class="fas fa-key"></i> اطلاعات ورود</h2>
        <p style="color:var(--dark-500); line-height:1.9; margin-top:8px;">
          برای جلوگیری از تغییر ناخواسته، وارد کردن رمز عبور فعلی الزامی است. اگر فقط نام کاربری را می‌خواهید تغییر دهید، دو فیلد رمز جدید را خالی بگذارید.
        </p>

        <form method="post" autocomplete="off" style="display:grid; gap:18px; margin-top:20px;">
          <?= eplakCsrfField() ?>
          <div class="form-group">
            <label for="username">نام کاربری جدید <span style="color:var(--danger);">*</span></label>
            <input class="search-input" style="width:100%;" type="text" id="username" name="username" required minlength="3" maxlength="100"
                   value="<?= htmlspecialchars($formUsername, ENT_QUOTES, 'UTF-8') ?>" autocomplete="username" dir="ltr">
          </div>

          <div class="form-group">
            <label for="current_password">رمز عبور فعلی <span style="color:var(--danger);">*</span></label>
            <input class="search-input" style="width:100%;" type="password" id="current_password" name="current_password" required autocomplete="current-password" dir="ltr">
          </div>

          <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:18px;">
            <div class="form-group">
              <label for="new_password">رمز عبور جدید</label>
              <input class="search-input" style="width:100%;" type="password" id="new_password" name="new_password" minlength="8" maxlength="255" autocomplete="new-password" dir="ltr">
              <small style="display:block; color:var(--dark-500); margin-top:6px;">حداقل ۸ کاراکتر</small>
            </div>
            <div class="form-group">
              <label for="confirm_password">تکرار رمز عبور جدید</label>
              <input class="search-input" style="width:100%;" type="password" id="confirm_password" name="confirm_password" minlength="8" maxlength="255" autocomplete="new-password" dir="ltr">
            </div>
          </div>

          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> ذخیره تغییرات</button>
            <a href="index.php" class="btn btn-secondary">انصراف</a>
          </div>
        </form>
      </section>

      <section class="panel" style="margin:0 24px 24px; max-width:760px;">
        <h2><i class="fas fa-info-circle"></i> حساب فعال</h2>
        <div class="stats-mini" style="margin-top:14px;">
          <div class="stat-item">نام کاربری <strong dir="ltr"><?= htmlspecialchars($currentAdmin['username'], ENT_QUOTES, 'UTF-8') ?></strong></div>
          <div class="stat-item">سطح دسترسی <strong><?= htmlspecialchars($currentAdmin['role'] === 'super_admin' ? 'مدیر کل' : 'مدیر', ENT_QUOTES, 'UTF-8') ?></strong></div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
