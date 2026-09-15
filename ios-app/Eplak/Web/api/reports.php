<?php
require_once __DIR__ . '/../admin/includes/db.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $phone = trim($_GET['phone'] ?? '');
    if ($phone !== '') {
        $stmt = $pdo->prepare('SELECT * FROM reports WHERE user_phone = :phone ORDER BY created_at DESC');
        $stmt->execute([':phone' => $phone]);
        echo json_encode(['success' => true, 'reports' => $stmt->fetchAll()]);
        exit;
    }

    $stmt = $pdo->query('SELECT * FROM reports ORDER BY created_at DESC');
    echo json_encode(['success' => true, 'reports' => $stmt->fetchAll()]);
    exit;
}

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

$phone = trim($input['phone'] ?? $input['userPhone'] ?? '');
$subject = trim($input['subject'] ?? $input['title'] ?? '');
$details = trim($input['details'] ?? $input['description'] ?? '');
$reportType = trim($input['reportType'] ?? $input['category'] ?? 'سایر');
$department = trim((string)($input['department'] ?? $input['mainDepartment'] ?? ''));
$subDepartment = trim((string)($input['subDepartment'] ?? $input['sub_department'] ?? ''));
$location = trim((string)($input['location'] ?? ''));

if ($phone === '' || $subject === '' || $details === '') {
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

    $stmtReport = $pdo->prepare('INSERT INTO reports (user_phone, title, description, category, department, sub_department, location, status) VALUES (:phone, :title, :description, :category, :department, :sub_department, :location, :status)');
    $stmtReport->execute([
        ':phone' => $phone,
        ':title' => $subject,
        ':description' => $details,
        ':category' => $reportType,
        ':department' => $department,
        ':sub_department' => $subDepartment,
        ':location' => $location,
        ':status' => 'pending',
    ]);

    $pdo->commit();
    echo json_encode(['success' => true]);
} catch (PDOException $e) {
    $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}
