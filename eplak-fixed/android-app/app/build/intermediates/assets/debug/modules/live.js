/* ============================================================
   modules/live.js — محتوای زنده (اخبار، دانستنی‌ها، اعلان‌ها)
   داده‌ها را از پایگاه داده (پنل ادمین) می‌خواند و بلافاصله در اپ
   نمایش می‌دهد. اگر ارتباط برقرار نبود، محتوای پیش‌فرض دست‌نخورده
   باقی می‌ماند و هیچ خطایی نمایش داده نمی‌شود.
   ============================================================ */
(function () {
  'use strict';

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
     اخبار و دانستنی‌ها
  ─────────────────────────────────────────────────────────── */
  function applyNews(items) {
    if (typeof newsData === 'undefined' || !Array.isArray(items)) return;

    const news = items.filter(function (i) { return i.type === 'news'; });
    const tips = items.filter(function (i) { return i.type === 'tip'; });

    /* تب «اخبار و اطلاعات» — جایگزینی درجا (newsData یک const است) */
    if (news.length) {
      newsData.length = 0;
      news.forEach(function (n) {
        newsData.push({
          id: 'srv-' + n.id,
          title: n.title,
          date: faDate(n.updated_at),
          icon: n.icon || '📰',
          summary: n.summary || '',
          body: n.body
        });
      });
      if (typeof renderNewsList === 'function') renderNewsList();
    }

    /* تب «دانستنی‌های ورامین» */
    renderTips(tips);

    /* نوار «آخرین اخبار» در پیشخوان */
    renderDashStrip(news.length ? newsData.slice(0, 2) : []);
  }

  function renderTips(tips) {
    let wrap = document.getElementById('knowledgeListWrap');
    if (!wrap) return;

    if (!tips.length) {
      wrap.innerHTML = '';
      return;
    }

    wrap.innerHTML = tips.map(function (t) {
      return ''
        + '<div class="glass-card" style="padding:14px; display:flex; gap:12px; align-items:flex-start; cursor:pointer;"'
        + ' onclick="openTipDetail(\'srv-' + t.id + '\')">'
        + (t.image_url
            ? '<img src="' + escapeText(t.image_url) + '" alt="" style="width:60px;height:60px;border-radius:14px;object-fit:cover;flex-shrink:0;">'
            : '<div class="promo-img" style="width:60px; height:60px; flex-shrink:0;">'
              + '<div class="promo-img-bg" style="font-size:24px;">' + escapeText(t.icon || '🏛️') + '</div></div>')
        + '<div style="flex:1; text-align:right;">'
        +   '<h4 style="font-size:13px; font-weight:700; line-height:1.5;">' + escapeText(t.title) + '</h4>'
        +   '<p style="font-size:11px; color:var(--text-muted); margin-top:4px; line-height:1.6;">' + escapeText(t.summary || '') + '</p>'
        + '</div>'
        + '</div>';
    }).join('');

    /* برای نمایش جزئیات در حافظه نگه می‌داریم */
    window.__EPLAK_TIPS__ = tips;
  }

  function renderDashStrip(items) {
    const wrap = document.getElementById('dashNewsWrap');
    if (!wrap || !items.length) return;
    wrap.innerHTML = items.map(function (n) {
      return ''
        + '<div class="mini-news-card" onclick="openNewsDetail(\'' + n.id + '\')">'
        +   '<div class="mini-news-text">'
        +     '<h4>' + escapeText(n.title) + '</h4>'
        +     '<p>' + escapeText(n.date) + '</p>'
        +   '</div>'
        +   '<div class="mini-news-icon">' + escapeText(n.icon) + '</div>'
        + '</div>';
    }).join('');
  }

  /* نمایش جزئیات یک دانستنی (از پنل ادمین) */
  window.openTipDetail = function (id) {
    const list = window.__EPLAK_TIPS__ || [];
    const t = list.find(function (x) { return 'srv-' + x.id === id; });
    if (!t) return;

    const img = document.getElementById('newsDetailImg');
    const title = document.getElementById('newsDetailTitle');
    const date = document.getElementById('newsDetailDate');
    const body = document.getElementById('newsDetailBody');
    if (img) img.textContent = t.icon || '🏛️';
    if (title) title.textContent = t.title;
    if (date) date.textContent = faDate(t.updated_at);
    if (body) body.textContent = t.body;
    if (typeof showScreen === 'function') showScreen('screen-news-detail');
  };

  /* ───────────────────────────────────────────────────────────
     اعلان‌ها
  ─────────────────────────────────────────────────────────── */
  function applyNotifications(items) {
    if (typeof notifications === 'undefined' || !Array.isArray(items)) return;

    items.forEach(function (n) {
      const sid = 'srv-' + n.id;
      const exists = notifications.some(function (x) { return String(x.id) === sid; });
      if (exists) {
        const local = notifications.find(function (x) { return String(x.id) === sid; });
        if (local && n.read_flag === 1) local.read = true;
        return;
      }
      /* اعلان‌های جدید بالای فهرست قرار می‌گیرند */
      notifications.unshift({
        id: sid,
        title: n.title,
        body: n.body,
        read: n.read_flag === 1,
        time: faTime(n.created_at),
        date: faDate(n.created_at),
        icon: '🔔'
      });
    });

    if (typeof saveNotifications === 'function') {
      try { saveNotifications(); } catch (e) {}
    }
    if (typeof renderNotifications === 'function') renderNotifications();
  }

  /* ───────────────────────────────────────────────────────────
     همگام‌سازی
  ─────────────────────────────────────────────────────────── */
  async function syncNews() {
    try {
      const res = await fetch(apiBase() + '/news.php?limit=50', { cache: 'no-store' });
      if (!res.ok) return false;
      const data = await res.json();
      if (!data || data.success !== true) return false;
      applyNews(data.items || []);
      return true;
    } catch (e) {
      return false; /* آفلاین — محتوای پیش‌فرض باقی می‌ماند */
    }
  }

  async function syncNotifications() {
    try {
      const phone = (typeof userProfile !== 'undefined' && (userProfile.rawPhone || userProfile.phone))
        ? (userProfile.rawPhone || userProfile.phone)
        : '';
      if (!phone) return false;
      const res = await fetch(apiBase() + '/notifications.php?phone=' + encodeURIComponent(phone), { cache: 'no-store' });
      if (!res.ok) return false;
      const data = await res.json();
      if (!data || data.success !== true) return false;
      applyNotifications(data.notifications || []);
      return true;
    } catch (e) {
      return false;
    }
  }

  window.syncLiveContent = async function () {
    const a = await syncNews();
    const b = await syncNotifications();
    return { news: a, notifications: b };
  };

  /* اجرا در شروع و به‌صورت دوره‌ای (هر ۶۰ ثانیه) */
  function start() {
    window.syncLiveContent();
    setInterval(window.syncLiveContent, 60000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
