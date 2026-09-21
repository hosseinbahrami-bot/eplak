<?php
require_once __DIR__ . '/../admin/includes/db.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
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

$name = trim($input['name'] ?? '');
$phone = trim($input['phone'] ?? '');
$address = trim($input['address'] ?? '');

if ($name === '' || $phone === '' || $address === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Name, phone, and address are required']);
    exit;
}

try {
    $stmt = $pdo->prepare('INSERT INTO customers (name, phone, address) VALUES (:name, :phone, :address)');
    $stmt->execute([
        ':name' => $name,
        ':phone' => $phone,
        ':address' => $address,
    ]);
    echo json_encode(['success' => true, 'id' => $pdo->lastInsertId()]);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}
