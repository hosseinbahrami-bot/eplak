const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const HOST = '0.0.0.0';
const ROOT_DIR = path.join(__dirname, 'eplak-fixed');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf'
};

const DEFAULT_DEPARTMENTS = [
  {
    id: 1,
    name: 'حوزه شهردار',
    children: [
      { id: 2, name: 'دفتر شهردار ورامین' },
      { id: 3, name: 'روابط عمومی و امور بین‌الملل' },
      { id: 4, name: 'بازرسی و ارزیابی عملکرد' },
      { id: 5, name: 'حراست شهرداری' },
      { id: 6, name: 'امور حقوقی' },
      { id: 7, name: 'شورای مشاوران' }
    ]
  },
  {
    id: 8,
    name: 'معاونت اداری و مالی',
    children: [
      { id: 9, name: 'منابع انسانی' },
      { id: 10, name: 'امور اداری' },
      { id: 11, name: 'امور مالی و حسابداری' },
      { id: 12, name: 'بودجه و برنامه‌ریزی' },
      { id: 13, name: 'تدارکات و پشتیبانی' },
      { id: 14, name: 'فناوری اطلاعات (IT)' }
    ]
  },
  {
    id: 15,
    name: 'معاونت فنی و عمرانی',
    children: [
      { id: 16, name: 'طراحی و اجرای پروژه‌های عمرانی' },
      { id: 17, name: 'ساخت و نگهداری معابر' },
      { id: 18, name: 'پل‌ها و تونل‌ها' },
      { id: 19, name: 'ساختمان‌های عمومی' },
      { id: 20, name: 'تأسیسات شهری' }
    ]
  },
  {
    id: 21,
    name: 'معاونت شهرسازی و معماری',
    children: [
      { id: 22, name: 'صدور پروانه ساختمانی' },
      { id: 23, name: 'پایان کار ساختمان' },
      { id: 24, name: 'کنترل و نظارت ساختمانی' },
      { id: 25, name: 'طرح‌های توسعه شهری' },
      { id: 26, name: 'کمیسیون‌های شهرسازی' }
    ]
  },
  {
    id: 27,
    name: 'معاونت خدمات شهری',
    children: [
      { id: 28, name: 'نظافت شهری' },
      { id: 29, name: 'مدیریت پسماند' },
      { id: 30, name: 'فضای سبز' },
      { id: 31, name: 'زیباسازی شهر' },
      { id: 32, name: 'آرامستان‌ها' },
      { id: 33, name: 'کنترل حیوانات شهری' }
    ]
  },
  {
    id: 34,
    name: 'معاونت حمل‌ونقل و ترافیک',
    children: [
      { id: 35, name: 'مدیریت ترافیک' },
      { id: 36, name: 'پارکینگ‌ها' },
      { id: 37, name: 'حمل‌ونقل عمومی' },
      { id: 38, name: 'پایانه‌ها' },
      { id: 39, name: 'ایمنی و علائم راهنمایی' }
    ]
  },
  {
    id: 40,
    name: 'معاونت فرهنگی و اجتماعی',
    children: [
      { id: 41, name: 'فرهنگسراها' },
      { id: 42, name: 'کتابخانه‌ها' },
      { id: 43, name: 'امور جوانان' },
      { id: 44, name: 'امور بانوان' },
      { id: 45, name: 'مشارکت‌های مردمی' },
      { id: 46, name: 'ورزش همگانی' }
    ]
  },
  {
    id: 47,
    name: 'معاونت برنامه‌ریزی و توسعه',
    children: [
      { id: 48, name: 'آمار و اطلاعات' },
      { id: 49, name: 'پژوهش و نوآوری' },
      { id: 50, name: 'مدیریت پروژه' },
      { id: 51, name: 'هوشمندسازی شهر' }
    ]
  },
  {
    id: 52,
    name: 'سازمان‌ها و شرکت‌های وابسته',
    children: [
      { id: 53, name: 'سازمان مدیریت پسماند' },
      { id: 54, name: 'سازمان آتش‌نشانی و خدمات ایمنی' },
      { id: 55, name: 'سازمان پارک‌ها و فضای سبز' },
      { id: 56, name: 'سازمان زیباسازی' },
      { id: 57, name: 'سازمان حمل‌ونقل بار و مسافر' },
      { id: 58, name: 'سازمان میادین و بازارها' },
      { id: 59, name: 'سازمان آرامستان‌ها' },
      { id: 60, name: 'سازمان فناوری اطلاعات و ارتباطات' },
      { id: 61, name: 'سازمان فرهنگی، اجتماعی و ورزشی' },
      { id: 62, name: 'سازمان سرمایه‌گذاری و مشارکت‌های مردمی' },
      { id: 63, name: 'شرکت بهره‌برداری مترو' },
      { id: 64, name: 'شرکت واحد اتوبوسرانی' },
      { id: 65, name: 'شرکت نوسازی و بهسازی شهری' }
    ]
  }
];

const server = http.createServer((req, res) => {
  // CORS & Iframe embedding headers (essential for Arena preview)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, HEAD, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.setHeader('X-Content-Type-Options', 'nosniff');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  let urlPath = decodeURIComponent(req.url.split('?')[0]);

  // Handle Mock API endpoints for local/preview execution without PHP server
  if (urlPath === '/api/departments.php' || urlPath === '/departments.php') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, departments: DEFAULT_DEPARTMENTS }));
    return;
  }

  if (urlPath === '/api/reports.php' || urlPath === '/reports.php') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, reports: [] }));
    return;
  }

  if (urlPath === '/api/notifications.php' || urlPath === '/notifications.php') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, notifications: [] }));
    return;
  }

  if (urlPath === '/api/news.php' || urlPath === '/news.php') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, news: [] }));
    return;
  }

  if (urlPath === '/' || urlPath === '') {
    urlPath = '/index.html';
  }

  let filePath = path.normalize(path.join(ROOT_DIR, urlPath));

  if (!filePath.startsWith(ROOT_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Access Denied');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('File Not Found');
      return;
    }

    if (stats.isDirectory()) {
      filePath = path.join(filePath, 'index.html');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    const stream = fs.createReadStream(filePath);
    stream.on('error', () => {
      if (!res.headersSent) res.writeHead(500);
      res.end();
    });
    stream.pipe(res);
  });
});

server.listen(PORT, HOST, () => {
  console.log(`Eplak preview server running at http://${HOST}:${PORT}`);
});
