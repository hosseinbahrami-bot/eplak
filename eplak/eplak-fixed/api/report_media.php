<?php
/*
 * تحویل محافظت‌شده‌ی فایل‌های گزارش.
 * پوشه‌ی uploads/reports به‌صورت مستقیم قابل فهرست/اجرا نیست؛ اپ با شماره‌ی
 * مالک و پنل با نشست معتبر ادمین از این endpoint فایل را دریافت می‌کنند.
 */
require_once __DIR__ . '/_common.php';
require_once dirname(__DIR__) . '/shared/report_media.php';

header('X-Content-Type-Options: nosniff');
header('Access-Control-Allow-Origin: *');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'GET') {
    http_response_code(405);
    exit;
}

$id = (int)($_GET['id'] ?? 0);
if ($id <= 0) {
    http_response_code(404);
    exit;
}

try {
    $stmt = $pdo->prepare('SELECT id, user_phone, file_path, mime_type, file_size
                           FROM report_media WHERE id = :id LIMIT 1');
    $stmt->execute([':id' => $id]);
    $media = $stmt->fetch();
    if (!$media) {
        http_response_code(404);
        exit;
    }

    $isAdmin = false;
    if ((string)($_GET['admin'] ?? '') === '1') {
        eplakStartSession('eplak_admin');
        $isAdmin = !empty($_SESSION['admin_logged_in']) && !empty($_SESSION['admin_id']);
    }
    if (!$isAdmin) {
        $phone = eplakNormalizePhone($_GET['phone'] ?? '');
        if ($phone === '' || !hash_equals((string)$media['user_phone'], $phone)) {
            // وجود/عدم وجود فایل را به درخواست‌کننده‌ی غیرمجاز افشا نکن.
            http_response_code(404);
            exit;
        }
    }

    $filename = basename((string)$media['file_path']);
    if ($filename === '' || $filename === '.' || $filename === '..' || !preg_match('/^[a-f0-9]{32}\.(?:jpg|jpeg|png|webp|gif|mp4|webm|mov|m4v)$/i', $filename)) {
        http_response_code(404);
        exit;
    }
    $absolute = eplakReportMediaRoot() . DIRECTORY_SEPARATOR . $filename;
    if (!is_file($absolute) || !is_readable($absolute)) {
        http_response_code(404);
        exit;
    }

    $allowedMimes = [
        'image/jpeg', 'image/png', 'image/webp', 'image/gif',
        'video/mp4', 'video/webm', 'video/quicktime', 'video/x-m4v'
    ];
    $mime = strtolower((string)$media['mime_type']);
    if (!in_array($mime, $allowedMimes, true)) {
        $mime = eplakReportMediaMime($absolute);
    }
    if (!in_array($mime, $allowedMimes, true)) {
        http_response_code(415);
        exit;
    }

    header('Content-Type: ' . $mime);
    header('Content-Disposition: inline; filename="' . $filename . '"');
    header('X-Content-Type-Options: nosniff');
    header('Cache-Control: private, max-age=3600');
    header('Content-Length: ' . (string)filesize($absolute));
    readfile($absolute);
} catch (Throwable $e) {
    error_log('[eplak-api:report_media] ' . $e->getMessage());
    http_response_code(500);
}
