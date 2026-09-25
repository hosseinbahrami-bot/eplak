/* Service Worker for Eplak — دریافت پوش وقتی اپلیکیشن بسته یا در پس‌زمینه است */
self.addEventListener('install', function (event) {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

// API و فایل‌ها همیشه از شبکه خوانده می‌شوند تا اعلان/محتوای پنل تازه بماند.
self.addEventListener('fetch', function (event) {
  event.respondWith(fetch(event.request));
});

function notificationPayload(event) {
  var data = {
    title: 'اعلان شهرداری ورامین',
    body: 'پیام جدیدی از سوی شهرداری ارسال شد.',
    url: './index.html#screen-notifications',
    id: Date.now()
  };
  if (event.data) {
    try {
      data = Object.assign(data, event.data.json());
    } catch (error) {
      data.body = event.data.text();
    }
  }
  return data;
}

function showEplakNotification(data) {
  var icon = new URL('./assets/img/pwa-icon-192.png', self.registration.scope).href;
  var options = {
    body: data.body,
    icon: icon,
    badge: icon,
    tag: 'eplak-' + String(data.id || Date.now()),
    renotify: true,
    silent: false,
    vibrate: [250, 100, 250],
    requireInteraction: false,
    data: {
      url: data.url || './index.html#screen-notifications',
      id: data.id || 0
    },
    actions: [
      { action: 'open', title: 'مشاهده اعلان' }
    ]
  };
  return self.registration.showNotification(data.title, options);
}

self.addEventListener('push', function (event) {
  var data = notificationPayload(event);
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (clientList) {
      // اعلان همیشه توسط خود سیستم‌عامل نمایش داده می‌شود؛ حتی اگر کاربر
      // هم‌اکنون داخل برنامه باشد. پیام زیر فقط برای تازه‌سازی فهرست است.
      clientList.forEach(function (client) {
        client.postMessage({ action: 'push_received', data: data });
      });
      return showEplakNotification(data);
    })
  );
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  var data = event.notification.data || {};
  var targetUrl = data.url || './index.html#screen-notifications';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (clientList) {
      for (var i = 0; i < clientList.length; i++) {
        var client = clientList[i];
        if ('focus' in client) {
          client.postMessage({ action: 'open_notifications' });
          return client.focus();
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(new URL(targetUrl, self.registration.scope).href);
      }
      return undefined;
    })
  );
});
