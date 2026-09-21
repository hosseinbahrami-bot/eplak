<?php
require_once __DIR__ . '/../admin/includes/db.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
    $phone = trim($_GET['phone'] ?? '');
    if ($phone === '') {
        $stmt = $pdo->query('SELECT *, CONCAT("TK-1403-", LPAD(id + 1000, 4, "0")) AS code FROM tickets ORDER BY created_at DESC');
        echo json_encode(['success' => true, 'tickets' => $stmt->fetchAll()]);
        exit;
    }

    $stmt = $pdo->prepare('SELECT *, CONCAT("TK-1403-", LPAD(id + 1000, 4, "0")) AS code FROM tickets WHERE user_phone = :phone ORDER BY created_at DESC');
    $stmt->execute([':phone' => $phone]);
    echo json_encode(['success' => true, 'tickets' => $stmt->fetchAll()]);
    exit;
}

if ($method === 'DELETE' || (isset($_GET['action']) && $_GET['action'] === 'delete')) {
    $id = (int)($_GET['id'] ?? 0);
    $input = json_decode(file_get_contents('php://input'), true);
    if ($id <= 0 && is_array($input)) {
        $id = (int)($input['id'] ?? 0);
    }
    if ($id > 0) {
        $stmt = $pdo->prepare('DELETE FROM tickets WHERE id = :id');
        $stmt->execute([':id' => $id]);
        echo json_encode(['success' => true, 'deleted_id' => $id]);
        exit;
    }
    http_response_code(400);
    echo json_encode(['error' => 'Invalid ticket id']);
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
$title = trim($input['title'] ?? $input['subject'] ?? '');
$description = trim($input['description'] ?? $input['details'] ?? '');
$category = trim($input['category'] ?? 'پشتیبانی عمومی');
$department = trim($input['department'] ?? 'حوزه شهردار و روابط عمومی');
$priority = trim($input['priority'] ?? 'medium');
$status = trim($input['status'] ?? 'pending');

if ($phone === '' || $title === '' || $description === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Phone, title, and description are required']);
    exit;
}

try {
    $pdo->beginTransaction();

    $stmtUser = $pdo->prepare('INSERT INTO users (phone, name, address, nid) VALUES (:phone, :name, :address, :nid)
        ON DUPLICATE KEY UPDATE
            name = IF(VALUES(name) = "", name, VALUES(name)),
            address = IF(VALUES(address) = "", address, VALUES(address)),
            nid = IF(VALUES(nid) = "", nid, VALUES(nid))');
    $stmtUser->execute([
        ':phone' => $phone,
        ':name' => $input['name'] ?? '',
        ':address' => $input['address'] ?? '',
        ':nid' => $input['nid'] ?? '',
    ]);

    $stmt = $pdo->prepare('INSERT INTO tickets (user_phone, title, description, category, department, priority, status, reply) VALUES (:phone, :title, :description, :category, :department, :priority, :status, :reply)');
    $stmt->execute([
        ':phone' => $phone,
        ':title' => $title,
        ':description' => $description,
        ':category' => $category,
        ':department' => $department,
        ':priority' => $priority,
        ':status' => $status ?: 'pending',
        ':reply' => '',
    ]);
    $ticketId = (int)$pdo->lastInsertId();

    $pdo->commit();
    $code = 'TK-1403-' . str_pad((string)($ticketId + 1000), 4, '0', STR_PAD_LEFT);
    echo json_encode([
        'success' => true,
        'id' => $ticketId,
        'tracking_code' => $code,
        'ticket' => [
            'id' => $ticketId,
            'code' => $code,
            'user_phone' => $phone,
            'title' => $title,
            'description' => $description,
            'category' => $category,
            'department' => $department,
            'priority' => $priority,
            'status' => $status ?: 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]
    ], JSON_UNESCAPED_UNICODE);
} catch (PDOException $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}
