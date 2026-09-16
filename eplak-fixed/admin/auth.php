<?php
require_once __DIR__ . '/includes/db.php';
eplakStartSession('eplak_admin');

function isAdminLoggedIn(): bool {
    return !empty($_SESSION['admin_logged_in']) && !empty($_SESSION['admin_id']);
}

function requireAdmin(): void {
    if (!isAdminLoggedIn()) {
        eplakRedirect('login.php');
        exit;
    }
}

if (basename($_SERVER['PHP_SELF']) !== 'login.php' && basename($_SERVER['PHP_SELF']) !== 'logout.php') {
    requireAdmin();
}
