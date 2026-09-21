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
        echo json_encode(['error' => 'Phone is required']);
        exit;
    }

    $stmt = $pdo->prepare('SELECT phone, name, address, nid FROM users WHERE phone = :phone LIMIT 1');
    $stmt->execute([':phone' => $phone]);
    $user = $stmt->fetch();
    if (!$user) {
        echo json_encode(['success' => false, 'user' => null]);
        exit;
    }

    echo json_encode(['success' => true, 'user' => $user]);
    exit;
}

if ($method !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

$phone = trim($input['phone'] ?? '');
$name = trim($input['name'] ?? '');
$address = trim($input['address'] ?? '');
$nid = trim($input['nid'] ?? '');

if ($phone === '' || $name === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Phone and name are required']);
    exit;
}

try {
    $stmt = $pdo->prepare('INSERT INTO users (phone, name, address, nid) VALUES (:phone, :name, :address, :nid) ON DUPLICATE KEY UPDATE name = VALUES(name), address = VALUES(address), nid = VALUES(nid)');
    $stmt->execute([
        ':phone' => $phone,
        ':name' => $name,
        ':address' => $address,
        ':nid' => $nid,
    ]);
    echo json_encode(['success' => true]);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}
