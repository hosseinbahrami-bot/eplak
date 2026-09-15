<?php
require_once __DIR__ . '/../admin/includes/db.php';

header('Content-Type: application/json; charset=utf-8');

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
    $phone = trim($_GET['phone'] ?? '');
    if ($phone === '') {
        http_response_code(400);
        echo json_encode(['error' => 'Phone is required']);
        exit;
    }

    $stmt = $pdo->prepare('SELECT * FROM tickets WHERE user_phone = :phone ORDER BY created_at DESC');
    $stmt->execute([':phone' => $phone]);
    echo json_encode(['success' => true, 'tickets' => $stmt->fetchAll()]);
    exit;
}

if ($method === 'PATCH' || $method === 'PUT') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!is_array($input)) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON']);
        exit;
    }

    $id = (int)($input['id'] ?? 0);
    $reply = trim((string)($input['reply'] ?? ''));
    $status = trim((string)($input['status'] ?? 'pending'));

    if ($id <= 0 || $reply === '') {
        http_response_code(400);
        echo json_encode(['error' => 'Ticket id and reply are required']);
        exit;
    }

    try {
        $stmt = $pdo->prepare('UPDATE tickets SET reply = :reply, status = :status WHERE id = :id');
        $stmt->execute([
            ':reply' => $reply,
            ':status' => $status ?: 'pending',
            ':id' => $id,
        ]);
        echo json_encode(['success' => true]);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
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

$phone = trim($input['userPhone'] ?? $input['phone'] ?? '');
$title = trim($input['title'] ?? '');
$description = trim($input['description'] ?? '');
$status = trim($input['status'] ?? 'pending');

if ($phone === '' || $title === '' || $description === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Phone, title, and description are required']);
    exit;
}

try {
    $pdo->beginTransaction();

    $stmtUser = $pdo->prepare('INSERT INTO users (phone, name, address, nid) VALUES (:phone, :name, :address, :nid) ON DUPLICATE KEY UPDATE phone = phone');
    $stmtUser->execute([
        ':phone' => $phone,
        ':name' => $input['name'] ?? '',
        ':address' => $input['address'] ?? '',
        ':nid' => $input['nid'] ?? '',
    ]);

    $stmt = $pdo->prepare('INSERT INTO tickets (user_phone, title, description, status, reply) VALUES (:phone, :title, :description, :status, :reply)');
    $stmt->execute([
        ':phone' => $phone,
        ':title' => $title,
        ':description' => $description,
        ':status' => $status ?: 'pending',
        ':reply' => '',
    ]);

    $pdo->commit();
    echo json_encode(['success' => true, 'id' => $pdo->lastInsertId()]);
} catch (PDOException $e) {
    $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}
