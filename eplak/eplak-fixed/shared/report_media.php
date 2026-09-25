<?php
/*
 * فایل‌های پیوست گزارش‌های شهروندی.
 *
 * فایل‌ها خارج از Git و در uploads/reports نگهداری می‌شوند؛ نام ذخیره‌شده
 * تصادفی است و نام/پسوند ارسالی کاربر هیچ‌گاه مستقیماً در مسیر فایل استفاده
 * نمی‌شود. محدودیت ویدیو در سمت سرور هم بررسی می‌شود و فقط به اعتبارسنجی
 * جاوااسکریپت وابسته نیست.
 */
if (!function_exists('eplakConfig')) {
    require_once __DIR__ . '/bootstrap.php';
}

if (!defined('EPLAK_REPORT_MAX_MEDIA')) {
    define('EPLAK_REPORT_MAX_MEDIA', 3);
}
if (!defined('EPLAK_REPORT_MAX_IMAGE_BYTES')) {
    define('EPLAK_REPORT_MAX_IMAGE_BYTES', 8 * 1024 * 1024);
}
if (!defined('EPLAK_REPORT_MAX_VIDEO_BYTES')) {
    define('EPLAK_REPORT_MAX_VIDEO_BYTES', 30 * 1024 * 1024);
}
if (!defined('EPLAK_REPORT_MAX_VIDEO_SECONDS')) {
    define('EPLAK_REPORT_MAX_VIDEO_SECONDS', 10.0);
}

function eplakReportMediaRoot(): string {
    // در محیط production می‌توان مسیر را خارج از webroot تنظیم کرد.
    $configured = trim((string)eplakConfig('REPORT_MEDIA_STORAGE_PATH', ''));
    $isAbsoluteWindows = strlen($configured) >= 3
        && $configured[1] === ':'
        && ($configured[2] === '/' || $configured[2] === '\\');
    if ($configured !== '' && (strpos($configured, DIRECTORY_SEPARATOR) === 0 || $isAbsoluteWindows)) {
        return rtrim($configured, DIRECTORY_SEPARATOR . '/\\');
    }
    return rtrim(EPLAK_ROOT, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'uploads' . DIRECTORY_SEPARATOR . 'reports';
}

function eplakReportMediaRelativePath(string $filename): string {
    return 'uploads/reports/' . ltrim($filename, '/\\');
}

function eplakReportMediaEndpointUrl(): string {
    $configuredBase = trim((string)eplakConfig('APP_BASE_URL', ''));
    if ($configuredBase !== '') {
        return rtrim($configuredBase, '/') . '/api/report_media.php';
    }
    $script = (string)($_SERVER['SCRIPT_NAME'] ?? '');
    $base = '';
    if (preg_match('~^(.*)/(?:api|admin)/[^/]+$~', $script, $matches)) {
        $base = rtrim((string)$matches[1], '/');
    }
    return ($base !== '' ? $base : '') . '/api/report_media.php';
}

function eplakReportMediaUrlForRecord(array $media): string {
    $id = (int)($media['id'] ?? 0);
    if ($id <= 0) {
        return '';
    }
    $script = (string)($_SERVER['SCRIPT_NAME'] ?? '');
    if (strpos($script, '/admin/') !== false) {
        return eplakReportMediaEndpointUrl() . '?id=' . $id . '&admin=1';
    }
    $phone = rawurlencode((string)($media['user_phone'] ?? ''));
    return eplakReportMediaEndpointUrl() . '?id=' . $id . '&phone=' . $phone;
}

function eplakReportMediaMime(string $path): string {
    $mime = '';
    if (class_exists('finfo')) {
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $mime = (string)$finfo->file($path);
    } elseif (function_exists('mime_content_type')) {
        $mime = (string)@mime_content_type($path);
    }
    return strtolower(trim($mime));
}

function eplakReportMediaExtension(string $mime): ?array {
    $map = [
        'image/jpeg'      => ['type' => 'image', 'ext' => 'jpg'],
        'image/png'       => ['type' => 'image', 'ext' => 'png'],
        'image/webp'      => ['type' => 'image', 'ext' => 'webp'],
        'image/gif'       => ['type' => 'image', 'ext' => 'gif'],
        'video/mp4'       => ['type' => 'video', 'ext' => 'mp4'],
        'video/webm'      => ['type' => 'video', 'ext' => 'webm'],
        'video/quicktime' => ['type' => 'video', 'ext' => 'mov'],
        'video/x-m4v'     => ['type' => 'video', 'ext' => 'm4v'],
    ];
    return $map[$mime] ?? null;
}

function eplakReportReadUInt32(string $data, int $offset): ?int {
    if ($offset < 0 || strlen($data) < $offset + 4) {
        return null;
    }
    $parts = unpack('Nvalue', substr($data, $offset, 4));
    return isset($parts['value']) ? (int)$parts['value'] : null;
}

function eplakReportReadUInt64(string $data, int $offset): ?int {
    if ($offset < 0 || strlen($data) < $offset + 8) {
        return null;
    }
    $parts = unpack('Nhigh/Nlow', substr($data, $offset, 8));
    if (!isset($parts['high'], $parts['low'])) {
        return null;
    }
    return (int)$parts['high'] * 4294967296 + (int)$parts['low'];
}

/**
 * استخراج مدت فایل‌های MP4/MOV بدون وابستگی اجباری به ffmpeg.
 * برای WebM/فرمت‌های دیگر ابتدا ffprobe استفاده می‌شود.
 */
function eplakReportMp4Duration(string $path): ?float {
    $data = @file_get_contents($path);
    if ($data === false || $data === '') {
        return null;
    }

    $length = strlen($data);
    $containers = [
        'moov' => true, 'trak' => true, 'mdia' => true, 'minf' => true,
        'stbl' => true, 'edts' => true, 'dinf' => true, 'meta' => true,
        'ilst' => true,
    ];

    $scan = static function (int $start, int $end) use (&$scan, $data, $length, $containers): ?float {
        $offset = $start;
        while ($offset + 8 <= $end && $offset + 8 <= $length) {
            $size32 = eplakReportReadUInt32($data, $offset);
            if ($size32 === null) {
                return null;
            }
            $type = substr($data, $offset + 4, 4);
            $header = 8;
            $size = $size32;
            if ($size32 === 1) {
                $size = eplakReportReadUInt64($data, $offset + 8);
                $header = 16;
            } elseif ($size32 === 0) {
                $size = $end - $offset;
            }
            if ($size === null || $size < $header || $offset + $size > $end) {
                return null;
            }

            $payload = $offset + $header;
            if ($type === 'mvhd' && $payload + 20 <= $length) {
                $version = ord($data[$payload]);
                if ($version === 1 && $payload + 32 <= $length) {
                    $timescale = eplakReportReadUInt32($data, $payload + 20);
                    $duration = eplakReportReadUInt64($data, $payload + 24);
                } else {
                    $timescale = eplakReportReadUInt32($data, $payload + 12);
                    $duration = eplakReportReadUInt32($data, $payload + 16);
                }
                if ($timescale !== null && $timescale > 0 && $duration !== null) {
                    return (float)$duration / (float)$timescale;
                }
            }

            if (isset($containers[$type])) {
                // meta در بعضی فایل‌ها چهار بایت version/flags قبل از child atom دارد.
                $childStart = $payload + ($type === 'meta' ? 4 : 0);
                if ($childStart < $offset + $size) {
                    $result = $scan($childStart, $offset + $size);
                    if ($result !== null) {
                        return $result;
                    }
                }
            }
            $offset += $size;
        }
        return null;
    };

    return $scan(0, $length);
}

function eplakReportEbmlVint(string $data, int $offset): ?array {
    if ($offset < 0 || $offset >= strlen($data)) {
        return null;
    }
    $first = ord($data[$offset]);
    $mask = 0x80;
    $width = 1;
    while ($width <= 8 && ($first & $mask) === 0) {
        $mask >>= 1;
        $width++;
    }
    if ($width > 8 || strlen($data) < $offset + $width) {
        return null;
    }
    $value = $first & ($mask - 1);
    for ($i = 1; $i < $width; $i++) {
        $value = ($value * 256) + ord($data[$offset + $i]);
    }
    // اندازه نامحدود EBML برای قطعه‌های زنده، مدت قابل اتکایی ندارد.
    if ($width === 8 && $value === 72057594037927935) {
        return null;
    }
    return ['value' => $value, 'width' => $width];
}

function eplakReportWebmDuration(string $path): ?float {
    $data = @file_get_contents($path);
    if ($data === false || $data === '') {
        return null;
    }
    $length = strlen($data);
    $timecodeScale = 1000000.0; // مقدار پیش‌فرض Matroska: یک میلی‌ثانیه
    $durationValue = null;
    for ($offset = 0; $offset + 4 < $length; $offset++) {
        $id = substr($data, $offset, 3);
        if ($id === "\x2A\xD7\xB1") {
            $size = eplakReportEbmlVint($data, $offset + 3);
            if ($size && $size['value'] > 0 && $size['value'] <= 8 && $offset + 3 + $size['width'] + $size['value'] <= $length) {
                $valueOffset = $offset + 3 + $size['width'];
                $scale = 0;
                for ($i = 0; $i < $size['value']; $i++) {
                    $scale = ($scale * 256) + ord($data[$valueOffset + $i]);
                }
                if ($scale > 0) {
                    $timecodeScale = (float)$scale;
                }
            }
        } elseif (substr($data, $offset, 2) === "\x44\x89") {
            $size = eplakReportEbmlVint($data, $offset + 2);
            if (!$size || !in_array($size['value'], [4, 8], true)) {
                continue;
            }
            $valueOffset = $offset + 2 + $size['width'];
            if ($valueOffset + $size['value'] > $length) {
                continue;
            }
            $unpacked = $size['value'] === 4
                ? @unpack('Gvalue', substr($data, $valueOffset, 4))
                : @unpack('Evalue', substr($data, $valueOffset, 8));
            if (is_array($unpacked) && isset($unpacked['value']) && is_finite((float)$unpacked['value'])) {
                $durationValue = (float)$unpacked['value'];
            }
        }
    }
    if ($durationValue === null || $durationValue < 0 || $timecodeScale <= 0) {
        return null;
    }
    return $durationValue * $timecodeScale / 1000000000.0;
}

function eplakReportVideoDuration(string $path): ?float {
    // اگر روی سرور ffprobe نصب باشد، WebM و همه فرمت‌های متداول را دقیق می‌خواند.
    if (function_exists('exec')) {
        $binary = trim((string)@shell_exec('command -v ffprobe 2>/dev/null'));
        if ($binary !== '') {
            $output = [];
            $exitCode = 1;
            $command = escapeshellarg($binary)
                . ' -v error -show_entries format=duration'
                . ' -of default=noprint_wrappers=1:nokey=1 '
                . escapeshellarg($path) . ' 2>/dev/null';
            @exec($command, $output, $exitCode);
            if ($exitCode === 0 && isset($output[0]) && is_numeric(trim((string)$output[0]))) {
                $duration = (float)trim((string)$output[0]);
                if ($duration >= 0) {
                    return $duration;
                }
            }
        }
    }

    $mp4Duration = eplakReportMp4Duration($path);
    return $mp4Duration !== null ? $mp4Duration : eplakReportWebmDuration($path);
}

/** فایل‌های multipart را به آرایه یکدست تبدیل می‌کند. */
function eplakNormalizeReportUploadFiles(array $fileBag): array {
    if (!isset($fileBag['name'])) {
        return [];
    }
    $names = is_array($fileBag['name']) ? $fileBag['name'] : [$fileBag['name']];
    $out = [];
    foreach ($names as $index => $name) {
        $out[] = [
            'name' => (string)$name,
            'type' => is_array($fileBag['type'] ?? null) ? (string)($fileBag['type'][$index] ?? '') : (string)($fileBag['type'] ?? ''),
            'tmp_name' => is_array($fileBag['tmp_name'] ?? null) ? (string)($fileBag['tmp_name'][$index] ?? '') : (string)($fileBag['tmp_name'] ?? ''),
            'error' => is_array($fileBag['error'] ?? null) ? (int)($fileBag['error'][$index] ?? UPLOAD_ERR_NO_FILE) : (int)($fileBag['error'] ?? UPLOAD_ERR_NO_FILE),
            'size' => is_array($fileBag['size'] ?? null) ? (int)($fileBag['size'][$index] ?? 0) : (int)($fileBag['size'] ?? 0),
        ];
    }
    return $out;
}

/**
 * اعتبارسنجی کامل قبل از درج گزارش. خروجی برای درج در جدول media استفاده می‌شود.
 * خطای این تابع ورودی کاربر است و API آن را با status 422 برمی‌گرداند.
 */
function eplakValidateReportMediaFiles(array $files): array {
    if (count($files) > EPLAK_REPORT_MAX_MEDIA) {
        throw new InvalidArgumentException('حداکثر ۳ فایل (تصویر یا فیلم) برای هر گزارش مجاز است.');
    }

    $prepared = [];
    foreach ($files as $file) {
        $error = (int)($file['error'] ?? UPLOAD_ERR_NO_FILE);
        if ($error === UPLOAD_ERR_NO_FILE) {
            continue;
        }
        if ($error !== UPLOAD_ERR_OK) {
            $message = $error === UPLOAD_ERR_INI_SIZE || $error === UPLOAD_ERR_FORM_SIZE
                ? 'حجم یکی از فایل‌ها از محدودیت سرور بیشتر است.'
                : 'یکی از فایل‌های ارسالی قابل دریافت نیست.';
            throw new InvalidArgumentException($message);
        }

        $tmp = (string)($file['tmp_name'] ?? '');
        if ($tmp === '' || !is_uploaded_file($tmp)) {
            throw new InvalidArgumentException('فایل ارسالی معتبر نیست.');
        }
        $size = (int)($file['size'] ?? 0);
        $mime = eplakReportMediaMime($tmp);
        $format = eplakReportMediaExtension($mime);
        if ($format === null) {
            throw new InvalidArgumentException('فرمت فایل پشتیبانی نمی‌شود. فقط JPG، PNG، WEBP، GIF، MP4 و WEBM مجاز هستند.');
        }

        $duration = null;
        if ($format['type'] === 'image') {
            if ($size <= 0 || $size > EPLAK_REPORT_MAX_IMAGE_BYTES || @getimagesize($tmp) === false) {
                throw new InvalidArgumentException('حجم یا ساختار یکی از تصاویر معتبر نیست. حداکثر حجم تصویر ۸ مگابایت است.');
            }
        } else {
            if ($size <= 0 || $size > EPLAK_REPORT_MAX_VIDEO_BYTES) {
                throw new InvalidArgumentException('حجم فیلم باید حداکثر ۳۰ مگابایت باشد.');
            }
            $duration = eplakReportVideoDuration($tmp);
            if ($duration === null || $duration <= 0) {
                throw new InvalidArgumentException('مدت فیلم قابل تشخیص نیست؛ لطفاً فیلم را با فرمت MP4 یا WEBM استاندارد دوباره انتخاب کنید.');
            }
            if ($duration > EPLAK_REPORT_MAX_VIDEO_SECONDS) {
                throw new InvalidArgumentException('مدت فیلم باید حداکثر ۱۰ ثانیه باشد.');
            }
        }

        $original = trim((string)($file['name'] ?? ''));
        $original = function_exists('mb_substr') ? mb_substr($original, 0, 255, 'UTF-8') : substr($original, 0, 255);
        $prepared[] = [
            'file' => $file,
            'media_type' => $format['type'],
            'extension' => $format['ext'],
            'mime_type' => $mime,
            'file_size' => $size,
            'duration_seconds' => $duration,
            'original_name' => $original,
        ];
    }
    return $prepared;
}

/** فایل‌ها را با نام تصادفی ذخیره و رکوردهای جدول report_media را درج می‌کند. */
function eplakPersistReportMedia(PDO $pdo, int $reportId, string $phone, array $prepared): array {
    if (!$prepared) {
        return [];
    }
    $root = eplakReportMediaRoot();
    if (!is_dir($root) && !@mkdir($root, 0750, true) && !is_dir($root)) {
        throw new RuntimeException('پوشه ذخیره فایل‌های گزارش ساخته نشد.');
    }

    $moved = [];
    $rows = [];
    try {
        $insert = $pdo->prepare(
            'INSERT INTO report_media
             (report_id, user_phone, media_type, file_path, original_name, mime_type, file_size, duration_seconds)
             VALUES (:report_id, :phone, :media_type, :file_path, :original_name, :mime_type, :file_size, :duration)'
        );
        foreach ($prepared as $item) {
            $filename = bin2hex(random_bytes(16)) . '.' . $item['extension'];
            $absolute = $root . DIRECTORY_SEPARATOR . $filename;
            if (!move_uploaded_file($item['file']['tmp_name'], $absolute)) {
                throw new RuntimeException('ذخیره یکی از فایل‌های گزارش انجام نشد.');
            }
            @chmod($absolute, 0640);
            $relative = eplakReportMediaRelativePath($filename);
            $insert->execute([
                ':report_id' => $reportId,
                ':phone' => $phone,
                ':media_type' => $item['media_type'],
                ':file_path' => $relative,
                ':original_name' => $item['original_name'],
                ':mime_type' => $item['mime_type'],
                ':file_size' => $item['file_size'],
                ':duration' => $item['duration_seconds'],
            ]);
            $mediaId = (int)$pdo->lastInsertId();
            $rows[] = [
                'id' => $mediaId,
                'media_type' => $item['media_type'],
                'path' => $relative,
                'url' => eplakReportMediaUrlForRecord([
                    'id' => $mediaId,
                    'user_phone' => $phone,
                ]),
                'original_name' => $item['original_name'],
                'mime_type' => $item['mime_type'],
                'file_size' => $item['file_size'],
                'duration_seconds' => $item['duration_seconds'],
            ];
            $moved[] = $absolute;
        }
        return $rows;
    } catch (Throwable $e) {
        foreach ($moved as $path) {
            @unlink($path);
        }
        throw $e;
    }
}

function eplakFetchReportMedia(PDO $pdo, array $reportIds, ?string $phone = null): array {
    $ids = [];
    foreach ($reportIds as $id) {
        $id = (int)$id;
        if ($id > 0) {
            $ids[$id] = $id;
        }
    }
    if (!$ids) {
        return [];
    }
    $placeholders = implode(',', array_fill(0, count($ids), '?'));
    $sql = 'SELECT id, report_id, user_phone, media_type, file_path, original_name, mime_type, file_size, duration_seconds, created_at
            FROM report_media WHERE report_id IN (' . $placeholders . ')';
    $params = array_values($ids);
    if ($phone !== null && $phone !== '') {
        $sql .= ' AND user_phone = ?';
        $params[] = $phone;
    }
    $sql .= ' ORDER BY id ASC';
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $out = [];
    foreach ($stmt->fetchAll() as $row) {
        $row['id'] = (int)$row['id'];
        $row['report_id'] = (int)$row['report_id'];
        $row['file_size'] = (int)$row['file_size'];
        $row['duration_seconds'] = $row['duration_seconds'] !== null ? (float)$row['duration_seconds'] : null;
        $row['path'] = $row['file_path'];
        $row['url'] = eplakReportMediaUrlForRecord($row);
        unset($row['file_path']);
        $out[(int)$row['report_id']][] = $row;
    }
    return $out;
}

function eplakAttachReportMedia(PDO $pdo, array $reports, ?string $phone = null): array {
    if (!$reports) {
        return $reports;
    }
    $ids = array_map(static fn($row) => (int)($row['id'] ?? 0), $reports);
    $byReport = eplakFetchReportMedia($pdo, $ids, $phone);
    foreach ($reports as &$report) {
        $id = (int)($report['id'] ?? 0);
        $report['media'] = $byReport[$id] ?? [];
        $report['media_count'] = count($report['media']);
    }
    unset($report);
    return $reports;
}

function eplakGetReportMedia(PDO $pdo, int $reportId, ?string $phone = null): array {
    $attached = eplakAttachReportMedia($pdo, [['id' => $reportId]], $phone);
    return $attached[0]['media'] ?? [];
}
