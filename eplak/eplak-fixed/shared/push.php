<?php
/*
 * Web Push بدون وابستگی به کتابخانه خارجی.
 *
 * کلیدهای VAPID هرگز نباید داخل گیت قرار بگیرند. آن‌ها را در متغیرهای
 * محیطی VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY / VAPID_SUBJECT یا در
 * shared/config.php قرار دهید. کلید عمومی به صورت base64url خام ۶۵ بایتی
 * (با پیشوند 04) و کلید خصوصی به صورت base64url خام ۳۲ بایتی یا PEM پذیرفته
 * می‌شوند.
 */
if (!function_exists('eplakConfig')) {
    require_once __DIR__ . '/bootstrap.php';
}

function eplakPushBase64UrlEncode(string $value): string {
    return rtrim(strtr(base64_encode($value), '+/', '-_'), '=');
}

function eplakPushBase64UrlDecode(string $value): string {
    $value = strtr($value, '-_', '+/');
    $padding = strlen($value) % 4;
    if ($padding > 0) {
        $value .= str_repeat('=', 4 - $padding);
    }
    $decoded = base64_decode($value, true);
    if ($decoded === false) {
        throw new RuntimeException('کلید پوش نامعتبر است.');
    }
    return $decoded;
}

function eplakPushDerLength(int $length): string {
    if ($length < 128) {
        return chr($length);
    }
    $bytes = '';
    while ($length > 0) {
        $bytes = chr($length & 0xff) . $bytes;
        $length >>= 8;
    }
    return chr(0x80 | strlen($bytes)) . $bytes;
}

function eplakPushPem(string $label, string $der): string {
    return "-----BEGIN {$label}-----\n"
        . chunk_split(base64_encode($der), 64, "\n")
        . "-----END {$label}-----\n";
}

function eplakPushPublicPem(string $rawPublicKey): string {
    if (strlen($rawPublicKey) !== 65 || $rawPublicKey[0] !== "\x04") {
        throw new RuntimeException('کلید عمومی p256dh نامعتبر است.');
    }
    // SubjectPublicKeyInfo برای id-ecPublicKey و منحنی prime256v1.
    $der = "\x30\x59\x30\x13\x06\x07\x2a\x86\x48\xce\x3d\x02\x01\x06\x08\x2a\x86\x48\xce\x3d\x03\x01\x07\x03\x42\x00" . $rawPublicKey;
    return eplakPushPem('PUBLIC KEY', $der);
}

function eplakPushPrivatePem(string $rawPrivateKey, string $rawPublicKey): string {
    if (strlen($rawPrivateKey) !== 32 || strlen($rawPublicKey) !== 65) {
        throw new RuntimeException('کلید VAPID نامعتبر است.');
    }
    $body = "\x02\x01\x01"
        . "\x04\x20" . $rawPrivateKey
        . "\xa0\x0a\x06\x08\x2a\x86\x48\xce\x3d\x03\x01\x07"
        . "\xa1\x44\x03\x42\x00" . $rawPublicKey;
    $der = "\x30" . eplakPushDerLength(strlen($body)) . $body;
    return eplakPushPem('EC PRIVATE KEY', $der);
}

function eplakPushHkdfExtract(string $salt, string $ikm): string {
    if ($salt === '') {
        $salt = str_repeat("\x00", 32);
    }
    return hash_hmac('sha256', $ikm, $salt, true);
}

function eplakPushHkdfExpand(string $prk, string $info, int $length): string {
    $output = '';
    $previous = '';
    $counter = 1;
    while (strlen($output) < $length) {
        $previous = hash_hmac('sha256', $previous . $info . chr($counter), $prk, true);
        $output .= $previous;
        $counter++;
        if ($counter > 255) {
            throw new RuntimeException('HKDF output خیلی بزرگ است.');
        }
    }
    return substr($output, 0, $length);
}

function eplakPushEcKeyPair(): array {
    $key = openssl_pkey_new([
        'curve_name' => 'prime256v1',
        'private_key_type' => OPENSSL_KEYTYPE_EC,
    ]);
    if ($key === false) {
        throw new RuntimeException('ساخت کلید موقت پوش ممکن نشد.');
    }
    $details = openssl_pkey_get_details($key);
    $x = $details['ec']['x'] ?? '';
    $y = $details['ec']['y'] ?? '';
    if (strlen($x) !== 32 || strlen($y) !== 32) {
        throw new RuntimeException('کلید موقت منحنی بیضوی نامعتبر است.');
    }
    return [$key, "\x04" . $x . $y];
}

function eplakPushVapid(): ?array {
    $publicValue = trim((string)eplakConfig('VAPID_PUBLIC_KEY', ''));
    $privateValue = trim((string)eplakConfig('VAPID_PRIVATE_KEY', ''));
    if ($publicValue === '' || $privateValue === '') {
        return null;
    }

    $publicRaw = eplakPushBase64UrlDecode($publicValue);
    if (strlen($publicRaw) !== 65 || $publicRaw[0] !== "\x04") {
        throw new RuntimeException('VAPID_PUBLIC_KEY باید کلید عمومی خام P-256 باشد.');
    }

    if (strpos($privateValue, 'BEGIN ') !== false) {
        $privatePem = $privateValue;
    } else {
        $privateRaw = eplakPushBase64UrlDecode($privateValue);
        $privatePem = eplakPushPrivatePem($privateRaw, $publicRaw);
    }

    $privateKey = openssl_pkey_get_private($privatePem);
    if ($privateKey === false) {
        throw new RuntimeException('VAPID_PRIVATE_KEY قابل خواندن نیست.');
    }

    return [
        'public_raw' => $publicRaw,
        'public' => eplakPushBase64UrlEncode($publicRaw),
        'private' => $privateKey,
        'subject' => trim((string)eplakConfig('VAPID_SUBJECT', 'mailto:admin@example.com')),
    ];
}

function eplakPushDerInteger(string $der, int &$offset): string {
    if (($der[$offset] ?? '') !== "\x02") {
        throw new RuntimeException('امضای VAPID نامعتبر است.');
    }
    $offset++;
    $lengthByte = ord($der[$offset++]);
    if (($lengthByte & 0x80) !== 0) {
        $count = $lengthByte & 0x7f;
        $length = 0;
        for ($i = 0; $i < $count; $i++) {
            $length = ($length << 8) | ord($der[$offset++]);
        }
    } else {
        $length = $lengthByte;
    }
    $integer = substr($der, $offset, $length);
    $offset += $length;
    return ltrim($integer, "\x00");
}

function eplakPushEcdsaDerToRaw(string $der): string {
    $offset = 0;
    if (($der[$offset++] ?? '') !== "\x30") {
        throw new RuntimeException('امضای ECDSA نامعتبر است.');
    }
    $lengthByte = ord($der[$offset++]);
    if (($lengthByte & 0x80) !== 0) {
        $count = $lengthByte & 0x7f;
        $offset += $count;
    }
    $r = eplakPushDerInteger($der, $offset);
    $s = eplakPushDerInteger($der, $offset);
    if (strlen($r) > 32 || strlen($s) > 32) {
        throw new RuntimeException('طول امضای ECDSA نامعتبر است.');
    }
    return str_pad($r, 32, "\x00", STR_PAD_LEFT) . str_pad($s, 32, "\x00", STR_PAD_LEFT);
}

function eplakPushVapidJwt(string $endpoint, array $vapid): string {
    $parts = parse_url($endpoint);
    if (!$parts || empty($parts['scheme']) || empty($parts['host'])) {
        throw new RuntimeException('نشانی endpoint اعلان نامعتبر است.');
    }
    $audience = strtolower($parts['scheme']) . '://' . $parts['host'];
    if (!empty($parts['port'])) {
        $isDefaultPort = ($parts['scheme'] === 'https' && (int)$parts['port'] === 443)
            || ($parts['scheme'] === 'http' && (int)$parts['port'] === 80);
        if (!$isDefaultPort) {
            $audience .= ':' . (int)$parts['port'];
        }
    }

    $header = eplakPushBase64UrlEncode(json_encode(['typ' => 'JWT', 'alg' => 'ES256'], JSON_UNESCAPED_SLASHES));
    $claims = eplakPushBase64UrlEncode(json_encode([
        'aud' => $audience,
        'exp' => time() + 43200,
        'sub' => $vapid['subject'],
    ], JSON_UNESCAPED_SLASHES));
    $signingInput = $header . '.' . $claims;
    $signatureDer = '';
    if (!openssl_sign($signingInput, $signatureDer, $vapid['private'], OPENSSL_ALGO_SHA256)) {
        throw new RuntimeException('امضای VAPID ساخته نشد.');
    }
    $signature = eplakPushEcdsaDerToRaw($signatureDer);
    return $signingInput . '.' . eplakPushBase64UrlEncode($signature);
}

function eplakPushEncrypt(string $payload, string $clientPublicRaw, string $authSecret): array {
    [$ephemeralKey, $ephemeralPublicRaw] = eplakPushEcKeyPair();
    $clientPublicPem = eplakPushPublicPem($clientPublicRaw);
    $sharedSecret = openssl_pkey_derive($clientPublicPem, $ephemeralKey, 32);
    if ($sharedSecret === false || strlen($sharedSecret) !== 32) {
        throw new RuntimeException('توافق کلید Web Push برقرار نشد.');
    }

    $keyInfo = "WebPush: info\x00" . $clientPublicRaw . $ephemeralPublicRaw;
    $ikm = eplakPushHkdfExpand(eplakPushHkdfExtract($authSecret, $sharedSecret), $keyInfo, 32);
    $salt = random_bytes(16);
    $prk = eplakPushHkdfExtract($salt, $ikm);
    $cek = eplakPushHkdfExpand($prk, "Content-Encoding: aes128gcm\x00", 16);
    $nonce = eplakPushHkdfExpand($prk, "Content-Encoding: nonce\x00", 12);

    // رکورد با delimiter مقدار ۲ به پایان می‌رسد؛ padding صفر در payload لازم نیست.
    $plaintext = $payload . "\x02";
    $tag = '';
    $ciphertext = openssl_encrypt($plaintext, 'aes-128-gcm', $cek, OPENSSL_RAW_DATA, $nonce, $tag);
    if ($ciphertext === false) {
        throw new RuntimeException('رمزگذاری اعلان پوش انجام نشد.');
    }

    // aes128gcm: salt (16) + record size (4) + key id length (1) + ephemeral key + ciphertext.
    $body = $salt . pack('N', 4096) . chr(strlen($ephemeralPublicRaw)) . $ephemeralPublicRaw . $ciphertext . $tag;
    return [$body, $ephemeralPublicRaw];
}

function eplakPushHttpPost(string $endpoint, string $body, array $headers): int {
    $headerLines = [];
    foreach ($headers as $name => $value) {
        $headerLines[] = $name . ': ' . $value;
    }

    if (function_exists('curl_init')) {
        $ch = curl_init($endpoint);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $body,
            CURLOPT_HTTPHEADER => $headerLines,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => false,
            CURLOPT_TIMEOUT => 20,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_SSL_VERIFYHOST => 2,
        ]);
        curl_exec($ch);
        $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        if ($status === 0 && $error !== '') {
            throw new RuntimeException($error);
        }
        return $status;
    }

    $context = stream_context_create([
        'http' => [
            'method' => 'POST',
            'header' => implode("\r\n", $headerLines),
            'content' => $body,
            'timeout' => 20,
            'ignore_errors' => true,
        ],
    ]);
    @file_get_contents($endpoint, false, $context);
    foreach (($http_response_header ?? []) as $line) {
        if (preg_match('#^HTTP/\S+\s+(\d+)#', $line, $matches)) {
            return (int)$matches[1];
        }
    }
    return 0;
}

function eplakSendWebPushToPhones(PDO $pdo, array $phones, array $data): int {
    $vapid = eplakPushVapid();
    if ($vapid === null || !$phones) {
        return 0;
    }

    $phones = array_values(array_unique(array_filter(array_map('trim', $phones), static fn($phone) => $phone !== '')));
    if (!$phones) {
        return 0;
    }
    $placeholders = implode(',', array_fill(0, count($phones), '?'));
    $stmt = $pdo->prepare("SELECT id, endpoint, endpoint_hash, p256dh, auth FROM push_subscriptions WHERE user_phone IN ($placeholders)");
    $stmt->execute($phones);
    $subscriptions = $stmt->fetchAll();
    $payload = json_encode([
        'title' => (string)($data['title'] ?? 'اعلان شهرداری ورامین'),
        'body' => (string)($data['body'] ?? ''),
        'url' => (string)($data['url'] ?? './index.html#screen-notifications'),
        'id' => (int)($data['id'] ?? 0),
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $delivered = 0;

    foreach ($subscriptions as $subscription) {
        try {
            $clientPublic = eplakPushBase64UrlDecode((string)$subscription['p256dh']);
            $auth = eplakPushBase64UrlDecode((string)$subscription['auth']);
            if (strlen($clientPublic) !== 65 || strlen($auth) !== 16) {
                throw new RuntimeException('اطلاعات رمزگذاری subscription ناقص است.');
            }
            [$encryptedBody] = eplakPushEncrypt($payload, $clientPublic, $auth);
            $jwt = eplakPushVapidJwt((string)$subscription['endpoint'], $vapid);
            $status = eplakPushHttpPost((string)$subscription['endpoint'], $encryptedBody, [
                'TTL' => '86400',
                'Content-Type' => 'application/octet-stream',
                'Content-Encoding' => 'aes128gcm',
                'Authorization' => 'vapid t=' . $jwt . ', k=' . $vapid['public'],
            ]);

            if ($status === 404 || $status === 410) {
                $delete = $pdo->prepare('DELETE FROM push_subscriptions WHERE endpoint_hash = :hash');
                $delete->execute([':hash' => $subscription['endpoint_hash']]);
            } elseif ($status >= 200 && $status < 300) {
                $delivered++;
            }
        } catch (Throwable $error) {
            error_log('[eplak] push subscription failed: ' . $error->getMessage());
        }
    }

    return $delivered;
}
