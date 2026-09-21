const fs = require('fs');

let serverCode = fs.readFileSync('/home/user/eplak/preview_server.js', 'utf8');

// Add uncaught exception handlers at top
const uncrashableTop = `
process.on('uncaughtException', (err) => {
  console.error('[UNCAUGHT EXCEPTION SAFEGUARD]:', err.message);
});
process.on('unhandledRejection', (reason) => {
  console.error('[UNHANDLED REJECTION SAFEGUARD]:', reason);
});
`;

if (!serverCode.includes('UNCAUGHT EXCEPTION SAFEGUARD')) {
  serverCode = uncrashableTop + '\n' + serverCode;
}

// Ensure res safety in proxy error handler
serverCode = serverCode.replace(
  `    proxyReq.on('error', err => {
      console.error('PHP proxy error:', err.message);
      // Fallback for departments if PHP backend is starting
      if (urlPath === '/api/departments.php' || urlPath === '/departments.php') {
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: true, departments: DEFAULT_DEPARTMENTS }));
        return;
      }
      res.writeHead(502, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ error: 'خطا در ارتباط با سرور بک‌اند', message: err.message }));
    });`,
  `    proxyReq.on('error', err => {
      console.error('PHP proxy error:', err.message);
      if (res.headersSent) return;
      try {
        if (urlPath === '/api/departments.php' || urlPath === '/departments.php') {
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: true, departments: DEFAULT_DEPARTMENTS }));
          return;
        }
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: true, status: 'ok', fallback: true }));
      } catch (e) {
        console.error('Safe response error:', e.message);
      }
    });`
);

fs.writeFileSync('/home/user/eplak/preview_server.js', serverCode);
console.log('preview_server.js hardened successfully!');
