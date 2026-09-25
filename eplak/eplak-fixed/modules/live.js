/* ============================================================
   modules/live.js — محتوای زنده (اخبار، دانستنی‌ها، اعلان‌ها و پوش بلادرنگ)
   ارتباط مستقیم و دوطرفه بین اپ شهروندی و پنل مدیریت MariaDB
   ============================================================ */
(function () {
  'use strict';

  var isInitialNotifs = true;
  var seenNotifIds = new Set();
  var systemPushKeys = new Set();
  var isSyncing = false;

  function apiBase() {
    return (typeof window.EPLAK_API_BASE_URL === 'string' && window.EPLAK_API_BASE_URL)
      ? window.EPLAK_API_BASE_URL.replace(/\/$/, '')
      : 'api';
  }

  function faDate(value) {
    try {
      const d = value ? new Date(String(value).replace(' ', 'T')) : new Date();
      if (isNaN(d.getTime())) return '';
      return d.toLocaleDateString('fa-IR', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (e) {
      return '';
    }
  }

  function faTime(value) {
    try {
      const d = value ? new Date(String(value).replace(' ', 'T')) : new Date();
      if (isNaN(d.getTime())) return '';
      return d.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return '';
    }
  }

  function escapeText(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ───────────────────────────────────────────────────────────
     پوش نوتیفیکیشن سیستمی مرورگر و گوشی
     اعلان برای همه حالت‌ها از NotificationManager سیستم‌عامل عبور می‌کند؛
     هیچ بنر یا صدای اختصاصی داخل برنامه جای اعلان سیستم را نمی‌گیرد.
  ─────────────────────────────────────────────────────────── */
  var pushConfigPromise = null;
  var pushSubscribedPhone = '';

  function bindServiceWorkerMessages() {
    if (!('serviceWorker' in navigator) || window.eplakSwMessageBound) return;
    window.eplakSwMessageBound = true;
    navigator.serviceWorker.addEventListener('message', function (event) {
      var message = event.data || {};
      if (message.action === 'open_notifications') {
        if (typeof showScreen === 'function') showScreen('screen-notifications');
      } else if (message.action === 'push_received' && message.data) {
        // خود Service Worker اعلان سیستمی را نشان داده است؛ شناسه ارسال را
        // نگه می‌داریم تا polling همان اعلان را دوباره نشان ندهد.
        if (message.data.id != null) systemPushKeys.add(String(message.data.id));
        if (typeof window.syncLiveContent === 'function') window.syncLiveContent();
      }
    });
  }

  function registerServiceWorker() {
    bindServiceWorkerMessages();
    if (!('serviceWorker' in navigator)) return Promise.resolve(null);
    if (window.eplakServiceWorkerRegistration) {
      return Promise.resolve(window.eplakServiceWorkerRegistration);
    }
    if (!window.eplakServiceWorkerPromise) {
      window.eplakServiceWorkerPromise = navigator.serviceWorker.register('./sw.js', { scope: './' })
        .then(function (registration) {
          window.eplakServiceWorkerRegistration = registration;
          return registration;
        })
        .catch(function (error) {
          console.warn('[push] service worker registration failed:', error);
          return null;
        });
    }
    return window.eplakServiceWorkerPromise;
  }

  function urlBase64ToUint8Array(value) {
    var padding = '='.repeat((4 - (value.length % 4)) % 4);
    var base64 = (value + padding).replace(/-/g, '+').replace(/_/g, '/');
    var raw = window.atob(base64);
    var output = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) output[i] = raw.charCodeAt(i);
    return output;
  }

  function getPushConfig() {
    if (pushConfigPromise) return pushConfigPromise;
    pushConfigPromise = fetch(apiBase() + '/push.php?action=config&t=' + Date.now(), { cache: 'no-store' })
      .then(function (response) { return response.ok ? response.json() : null; })
      .catch(function () { return null; });
    return pushConfigPromise;
  }

  async function subscribeToPush(phone) {
    phone = String(phone || '');
    if (!phone || pushSubscribedPhone === phone || !('PushManager' in window)) return false;
    if (!('Notification' in window) || Notification.permission !== 'granted') return false;

    var config = await getPushConfig();
    if (!config || !config.enabled || !config.public_key) return false;
    var registration = await registerServiceWorker();
    if (!registration || !registration.pushManager) return false;

    try {
      var subscription = await registration.pushManager.getSubscription();
      if (!subscription) {
        subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(config.public_key)
        });
      }
      var response = await fetch(apiBase() + '/push.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'subscribe', phone: phone, subscription: subscription.toJSON() })
      });
      if (!response.ok) return false;
      pushSubscribedPhone = phone;
      return true;
    } catch (error) {
      console.warn('[push] subscription failed:', error);
      return false;
    }
  }

  async function unsubscribeFromPush(phone) {
    phone = String(phone || '');
    if (!phone || !('PushManager' in window)) return false;
    try {
      var registration = await registerServiceWorker();
      var subscription = registration && registration.pushManager
        ? await registration.pushManager.getSubscription()
        : null;
      if (!subscription) {
        pushSubscribedPhone = '';
        return true;
      }
      var response = await fetch(apiBase() + '/push.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'unsubscribe',
          phone: phone,
          endpoint: subscription.endpoint
        })
      });
      if (response.ok) pushSubscribedPhone = '';
      return response.ok;
    } catch (e) {
      return false;
    }
  }

  async function requestPushPermission() {
    if (!('Notification' in window)) return false;
    try {
      var permission = Notification.permission;
      if (permission === 'default') permission = await Notification.requestPermission();
      if (permission !== 'granted') return false;
      await registerServiceWorker();
      var phone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : '';
      if (phone) await subscribeToPush(phone);
      return true;
    } catch (e) {
      return false;
    }
  }
  window.requestPushPermission = requestPushPermission;
  window.subscribeToPush = subscribeToPush;
  window.unsubscribeFromPush = unsubscribeFromPush;

  function triggerDeviceNotification(title, body, id) {
    // در APK، NotificationManager اندروید اعلان واقعی با کانال صدادار و ویبره را
    // نشان می‌دهد؛ WebView فایل محلی معمولاً PushManager/Service Worker ندارد.
    if (window.AndroidApp && typeof window.AndroidApp.showNotification === 'function') {
      try {
        window.AndroidApp.showNotification(String(title || 'اعلان جدید'), String(body || ''), String(id || Date.now()));
      } catch (e) {
        console.warn('[push] native notification error:', e);
      }
      return;
    }

    // در PWA نیز اعلان سیستم در foreground و background یکسان است؛
    // silent=false و vibrate در Service Worker صدای/ویبره سیستم را فعال می‌کند.
    if (!('Notification' in window) || Notification.permission !== 'granted') return;
    registerServiceWorker().then(function (registration) {
      if (!registration || typeof registration.showNotification !== 'function') return;
      return registration.showNotification(title, {
        body: body,
        icon: './assets/img/pwa-icon-192.png',
        badge: './assets/img/pwa-icon-192.png',
        tag: 'eplak-' + id,
        renotify: true,
        silent: false,
        vibrate: [250, 100, 250],
        data: { url: './index.html#screen-notifications' }
      });
    }).catch(function (e) {
      console.warn('[push] device notification error:', e);
    });
  }

  /* ───────────────────────────────────────────────────────────
     اخبار و دانستنی‌ها
  ─────────────────────────────────────────────────────────── */
  function applyNews(items) {
    if (typeof newsData === 'undefined' || !Array.isArray(items)) return;

    const news = items.filter(function (i) { return i.type === 'news'; });
    const tips = items.filter(function (i) { return i.type === 'tip'; });
    const legacy = document.getElementById('legacyHeritageFallback');
    // حتی پاسخ خالی هم معتبر است؛ حذف یک مطلب در پنل باید در اپ هم حذف شود.
    if (legacy) legacy.style.display = 'none';

    /* تب «اخبار و اطلاعات» — همیشه با داده‌های سرور جایگزین می‌شود. */
    newsData.length = 0;
    news.forEach(function (n) {
      newsData.push({
        id: 'srv-' + n.id,
        title: n.title,
        date: faDate(n.updated_at),
        icon: n.icon || '📰',
        summary: n.summary || '',
        body: n.body,
        image_url: n.image_url || ''
      });
    });
    // حالت انگلیسی هم باید همان مطالب منتشرشده و قابل‌مدیریت پنل را نشان دهد،
    // نه داده‌های قدیمیِ ثابت داخل کد.
    if (typeof window !== 'undefined') {
      window.newsData_EN = newsData.slice();
    }
    if (typeof renderNewsList === 'function') renderNewsList();

    /* تب «دانستنی‌های ورامین» */
    renderTips(tips);

    /* نوار «آخرین اخبار» در پیشخوان */
    renderDashStrip(newsData.slice(0, 2));
  }

  function renderTips(tips) {
    let wrap = document.getElementById('knowledgeListWrap');
    if (!wrap) return;

    if (!tips.length) {
      wrap.innerHTML = '';
      window.__EPLAK_TIPS__ = [];
      return;
    }

    wrap.innerHTML = tips.map(function (t) {
      return ''
        + '<div class="glass-card" style="padding:14px; display:flex; gap:12px; align-items:flex-start; cursor:pointer;"'
        + ' onclick="openTipDetail(\'srv-' + t.id + '\')">'
        + (t.image_url
            ? '<img src="' + escapeText(t.image_url) + '" alt="' + escapeText(t.title) + '" style="width:60px;height:60px;border-radius:14px;object-fit:cover;flex-shrink:0;">'
            : '<div class="promo-img" style="width:60px; height:60px; flex-shrink:0;">'
              + '<div class="promo-img-bg">' + (window.EplakIcons ? window.EplakIcons.get(t.icon || '🏛️') : escapeText(t.icon || '🏛️')) + '</div></div>')
        + '<div style="flex:1; text-align:right;">'
        +   '<h4 style="font-size:13px; font-weight:700; line-height:1.5;">' + escapeText(t.title) + '</h4>'
        +   '<p style="font-size:11px; color:var(--text-muted); margin-top:4px; line-height:1.6;">' + escapeText(t.summary || '') + '</p>'
        + '</div>'
        + '</div>';
    }).join('');

    window.__EPLAK_TIPS__ = tips;
  }

  function renderDashStrip(items) {
    const wrap = document.getElementById('dashNewsWrap');
    if (!wrap) return;
    if (!items.length) { wrap.innerHTML = ''; return; }
    const isEn = (window.i18n && typeof window.i18n.getLanguage === 'function')
      ? window.i18n.getLanguage() === 'en'
      : (window.i18n && window.i18n.currentLang === 'en');
    const source = (isEn && window.newsData_EN) ? window.newsData_EN : items;
    wrap.innerHTML = source.slice(0, 2).map(function (n) {
      return ''
        + '<div class="mini-news-card" onclick="openNewsDetail(\'' + n.id + '\')">'
        +   '<div class="mini-news-text" style="text-align:' + (isEn ? 'left' : 'right') + ';">'
        +     '<h4>' + escapeText(n.title) + '</h4>'
        +     '<p>' + escapeText(n.date) + '</p>'
        +   '</div>'
        +   '<div class="mini-news-icon">' + (window.EplakIcons ? window.EplakIcons.get(n.icon) : escapeText(n.icon)) + '</div>'
        + '</div>';
    }).join('');
  }
  window.renderDashStrip = renderDashStrip;

  window.openTipDetail = function (id) {
    const list = window.__EPLAK_TIPS__ || [];
    const t = list.find(function (x) { return 'srv-' + x.id === id; });
    if (!t) return;

    const img = document.getElementById('newsDetailImg');
    const title = document.getElementById('newsDetailTitle');
    const date = document.getElementById('newsDetailDate');
    const body = document.getElementById('newsDetailBody');
    if (img) {
      img.innerHTML = t.image_url
        ? '<img src="' + escapeText(t.image_url) + '" alt="' + escapeText(t.title) + '" style="width:100%;height:100%;object-fit:cover;border-radius:16px;">'
        : (window.EplakIcons ? window.EplakIcons.get(t.icon || '🏛️') : (t.icon || '🏛️'));
    }
    if (title) title.textContent = t.title;
    if (date) date.textContent = faDate(t.updated_at);
    if (body) body.textContent = t.body;
    if (typeof showScreen === 'function') showScreen('screen-news-detail');
  };

  /* ───────────────────────────────────────────────────────────
     اعلان‌ها و همگام‌سازی بلادرنگ
  ─────────────────────────────────────────────────────────── */
  function applyNotifications(items) {
    if (typeof notifications === 'undefined' || !Array.isArray(items)) return;

    var newItemsFound = [];

    items.forEach(function (n) {
      const sid = 'srv-' + n.id;
      const numericId = parseInt(n.id, 10);

      const exists = notifications.some(function (x) {
        return String(x.id) === sid || String(x.id) === String(numericId);
      });

      if (exists) {
        const local = notifications.find(function (x) {
          return String(x.id) === sid || String(x.id) === String(numericId);
        });
        if (local && n.read_flag === 1) local.read = true;
      } else {
        var notifObj = {
          id: sid,
          title: n.title,
          body: n.body,
          read: n.read_flag === 1,
          time: faTime(n.created_at),
          date: faDate(n.created_at),
          icon: '🔔'
        };
        notifications.unshift(notifObj);

        var systemKey = n.send_id != null ? String(n.send_id) : String(n.id);
        if (!isInitialNotifs && !seenNotifIds.has(numericId) && !systemPushKeys.has(systemKey)) {
          newItemsFound.push(n);
        }
        systemPushKeys.delete(systemKey);
      }

      seenNotifIds.add(numericId);
    });

    if (typeof saveNotifications === 'function') {
      try { saveNotifications(); } catch (e) {}
    }
    if (typeof renderNotifications === 'function') {
      try { renderNotifications(); } catch (e) {}
    }

    // Trigger alerts for newly arrived announcements
    if (!isInitialNotifs && newItemsFound.length > 0) {
      var latest = newItemsFound[0];
      triggerDeviceNotification(latest.title, latest.body, latest.id);
    }

    isInitialNotifs = false;
  }

  /* ───────────────────────────────────────────────────────────
     همگام‌سازی
  ─────────────────────────────────────────────────────────── */
  async function syncNews() {
    try {
      const res = await fetch(apiBase() + '/news.php?limit=50', { cache: 'no-store' });
      if (!res.ok) return false;
      const data = await res.json();
      // پاسخ fallback/خطای backend که items ندارد نباید محتوای فعلی را پاک کند.
      if (!data || data.success !== true || !Array.isArray(data.items)) return false;
      applyNews(data.items);
      return true;
    } catch (e) {
      return false;
    }
  }

  async function syncNotifications() {
    try {
      var phone = '';
      if (typeof getCurrentPhone === 'function') {
        phone = getCurrentPhone();
      }
      if (!phone && typeof userProfile !== 'undefined') {
        phone = userProfile.rawPhone || userProfile.phone || '';
      }

      // If user hasn't logged in, query broadcast notifications ('all')
      var queryPhone = phone || 'all';
      const res = await fetch(apiBase() + '/notifications.php?phone=' + encodeURIComponent(queryPhone) + '&t=' + Date.now(), { cache: 'no-store' });
      if (!res.ok) return false;
      const data = await res.json();
      // پاسخ fallback/خطای backend نباید اولین همگام‌سازی را مصرف کند.
      if (!data || data.success !== true || !Array.isArray(data.notifications)) return false;
      applyNotifications(data.notifications);
      if (phone && 'Notification' in window && Notification.permission === 'granted') {
        subscribeToPush(phone);
      }
      return true;
    } catch (e) {
      return false;
    }
  }

  async function syncReportsLive() {
    try {
      var phone = (typeof getCurrentPhone === 'function') ? getCurrentPhone() : '';
      if (phone && typeof loadReportsFromBackend === 'function') {
        await loadReportsFromBackend(phone, { silent: true });
      }
    } catch (e) {}
  }

  window.syncLiveContent = async function () {
    if (isSyncing) return;
    isSyncing = true;
    try {
      await syncNotifications();
      await syncReportsLive();
    } finally {
      isSyncing = false;
    }
  };

  /* راه‌اندازی و بررسی مداوم بلادرنگ (هر ۳.۵ ثانیه) */
  function start() {
    // Service worker از همان ابتدا ثبت می‌شود تا در زمان بسته بودن برنامه
    // بتواند رویداد push را دریافت کند؛ مجوز فقط بعد از تعامل کاربر درخواست می‌شود.
    registerServiceWorker();

    // Initial fetch of news and notifications
    syncNews();
    syncNotifications();

    // Fast real-time polling for instant broadcast notifications and report updates
    setInterval(window.syncLiveContent, 3500);

    // Refresh news every 30 seconds
    setInterval(syncNews, 30000);

    // Request notification permission gracefully on first user interaction
    var permissionTriggered = false;
    function promptPerm() {
      if (permissionTriggered) return;
      permissionTriggered = true;
      requestPushPermission();
      document.removeEventListener('click', promptPerm);
      document.removeEventListener('touchstart', promptPerm);
    }
    document.addEventListener('click', promptPerm);
    document.addEventListener('touchstart', promptPerm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
