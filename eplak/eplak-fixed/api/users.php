<?php
require_once __DIR__ . '/../admin/includes/db.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$method = $_SERVER['REQUEST_METHOD'];
if ($method === 'GET') {
    $phone = trim($_GET['phone'] ?? '');
    if ($phone === '') {
        http_response_code(400);
        echo json_encode(['error' => 'Phone is required'], JSON_UNESCAPED_UNICODE);
        exit;
    }

    $stmt = $pdo->prepare('SELECT id, phone, name, address, nid, created_at FROM users WHERE phone = :phone LIMIT 1');
    $stmt->execute([':phone' => $phone]);
    $user = $stmt->fetch();
    if (!$user) {
        echo json_encode(['success' => false, 'user' => null], JSON_UNESCAPED_UNICODE);
        exit;
    }

    echo json_encode(['success' => true, 'user' => $user], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($method !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON'], JSON_UNESCAPED_UNICODE);
    exit;
}

$phone = trim($input['phone'] ?? $input['userPhone'] ?? '');
$name = trim($input['name'] ?? '');
$address = trim($input['address'] ?? '');
$nid = trim($input['nid'] ?? '');

if ($phone === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Phone is required'], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($name === '') {
    $name = 'شهروند';
}

try {
    $stmt = $pdo->prepare('INSERT INTO users (phone, name, address, nid) VALUES (:phone, :name, :address, :nid)
        ON DUPLICATE KEY UPDATE
            name = IF(VALUES(name) != "" AND VALUES(name) != "شهروند", VALUES(name), IF(name != "", name, VALUES(name))),
            address = IF(VALUES(address) != "", VALUES(address), address),
            nid = IF(VALUES(nid) != "", VALUES(nid), nid)');
    $stmt->execute([
        ':phone' => $phone,
        ':name' => $name,
        ':address' => $address,
        ':nid' => $nid,
    ]);

    $stmtGet = $pdo->prepare('SELECT id, phone, name, address, nid, created_at FROM users WHERE phone = :phone LIMIT 1');
    $stmtGet->execute([':phone' => $phone]);
    $savedUser = $stmtGet->fetch();

    echo json_encode(['success' => true, 'user' => $savedUser], JSON_UNESCAPED_UNICODE);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()], JSON_UNESCAPED_UNICODE);
}
