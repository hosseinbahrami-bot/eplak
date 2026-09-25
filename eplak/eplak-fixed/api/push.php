<?php
/*
 * ثبت subscription مرورگر برای Web Push.
 *
 * GET  ?action=config       کلید عمومی VAPID را برمی‌گرداند.
 * POST action=subscribe    فیلدهای phone و subscription (JSON)
 * POST action=unsubscribe  فیلدهای phone و endpoint
 */
require_once __DIR__ . '/../admin/includes/db.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');
header('Cache-Control: no-store, no-cache, must-revalidate');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

function eplakPushJson(array $payload, int $status = 200): void {
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

try {
    $action = strtolower(trim((string)($_GET['action'] ?? $_POST['action'] ?? '')));
    if ($action === 'config') {
        $publicKey = trim((string)eplakConfig('VAPID_PUBLIC_KEY', ''));
        eplakPushJson([
            'success' => true,
            'enabled' => $publicKey !== '',
            'public_key' => $publicKey,
        ]);
    }

    $raw = file_get_contents('php://input');
    $json = json_decode($raw ?: '', true);
    if (!is_array($json)) {
        $json = [];
    }
    $input = array_merge($_POST, $json);
    $phone = trim((string)($input['phone'] ?? ''));
    if ($phone !== '' && !preg_match('/^09\d{9}$/', $phone)) {
        eplakPushJson(['success' => false, 'error' => 'شماره موبایل نامعتبر است.'], 422);
    }

    if ($action === 'subscribe') {
        $subscription = $input['subscription'] ?? null;
        if (is_string($subscription)) {
            $subscription = json_decode($subscription, true);
        }
        $endpoint = is_array($subscription) ? trim((string)($subscription['endpoint'] ?? '')) : '';
        $keys = is_array($subscription) && is_array($subscription['keys'] ?? null) ? $subscription['keys'] : [];
        $p256dh = trim((string)($keys['p256dh'] ?? ''));
        $auth = trim((string)($keys['auth'] ?? ''));

        if ($phone === '' || $endpoint === '' || $p256dh === '' || $auth === '') {
            eplakPushJson(['success' => false, 'error' => 'اطلاعات subscription ناقص است.'], 422);
        }
        if (strlen($endpoint) > 2000 || strlen($p256dh) > 255 || strlen($auth) > 255) {
            eplakPushJson(['success' => false, 'error' => 'اطلاعات subscription بیش از حد مجاز است.'], 422);
        }

        $stmt = $pdo->prepare(
            'INSERT INTO push_subscriptions (user_phone, endpoint, endpoint_hash, p256dh, auth, user_agent)
             VALUES (:phone, :endpoint, :hash, :p256dh, :auth, :agent)
             ON DUPLICATE KEY UPDATE
                user_phone = VALUES(user_phone), endpoint = VALUES(endpoint),
                p256dh = VALUES(p256dh), auth = VALUES(auth), user_agent = VALUES(user_agent)'
        );
        $stmt->execute([
            ':phone' => $phone,
            ':endpoint' => $endpoint,
            ':hash' => hash('sha256', $endpoint),
            ':p256dh' => $p256dh,
            ':auth' => $auth,
            ':agent' => substr((string)($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 255),
        ]);
        eplakPushJson(['success' => true, 'subscribed' => true]);
    }

    if ($action === 'unsubscribe') {
        $endpoint = trim((string)($input['endpoint'] ?? ''));
        if ($endpoint === '') {
            eplakPushJson(['success' => false, 'error' => 'endpoint ارسال نشده است.'], 422);
        }
        $stmt = $pdo->prepare('DELETE FROM push_subscriptions WHERE endpoint_hash = :hash' . ($phone !== '' ? ' AND user_phone = :phone' : ''));
        $params = [':hash' => hash('sha256', $endpoint)];
        if ($phone !== '') {
            $params[':phone'] = $phone;
        }
        $stmt->execute($params);
        eplakPushJson(['success' => true, 'unsubscribed' => true]);
    }

    eplakPushJson(['success' => false, 'error' => 'عملیات نامعتبر است.'], 400);
} catch (Throwable $e) {
    eplakPushJson(['success' => false, 'error' => 'خطا در ثبت اعلان پوش: ' . $e->getMessage()], 500);
}
