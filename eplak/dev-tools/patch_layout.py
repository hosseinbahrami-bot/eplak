#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بازطراحی صفحه خدمات به سبک پیشخوان (پنل‌های کادربندی‌شده)"""
import io, re

P = "/home/user/eplak-fixed/modules/services.js"
s = io.open(P, encoding="utf-8").read()

# ---------- 1) افزودن عنوان کوتاه به هر سرویس (برای گرید دسترسی سریع) ----------
shorts = {
    "id: 'payment',":      "short: 'پرداخت عوارض',",
    "id: 'business',":     "short: 'کسب‌وکارها',",
    "id: 'tourism',":      "short: 'بوم‌گردی',",
    "id: 'recycling',":    "short: 'بازیافت',",
    "id: 'superapp',":     "short: 'مکمل‌ها',",
    "id: 'ruralmap',":     "short: 'طرح هادی',",
    "id: 'metro',":        "short: 'مترو و قطار',",
    "id: 'traffic',":      "short: 'طرح ترافیک',",
    "id: 'transit',":      "short: 'ناوگان عمومی',",
}
for key, short in shorts.items():
    assert key in s, key
    s = s.replace(key, key + "\n      " + short, 1)

# ---------- 2) شناسه و توضیح برای هر دسته ----------
old_groups = """  const SERVICE_GROUPS = [
    { title: 'مالی و عوارض شهری', icon: '💳', ids: ['payment'] },
    { title: 'کسب‌وکار و بوم‌گردی', icon: '🏪', ids: ['business', 'tourism'] },
    { title: 'محیط‌زیست و بازیافت', icon: '♻️', ids: ['recycling'] },
    { title: 'زندگی شهری هوشمند', icon: '🧩', ids: ['superapp', 'ruralmap'] },
    { title: 'حمل‌ونقل و ترافیک', icon: '🚇', ids: ['metro', 'traffic', 'transit'] }
  ];"""

new_groups = """  const SERVICE_GROUPS = [
    {
      id: 'finance', title: 'مالی و عوارض شهری', icon: '💳',
      desc: 'استعلام و پرداخت عوارض، قبوض و بدهی‌های شهری',
      ids: ['payment']
    },
    {
      id: 'business-cat', title: 'کسب‌وکار و بوم‌گردی', icon: '🏪',
      desc: 'ویترین اصناف، تبلیغات محله‌محور و معرفی ظرفیت‌های گردشگری هر شهر',
      ids: ['business', 'tourism']
    },
    {
      id: 'environment', title: 'محیط‌زیست و بازیافت', icon: '♻️',
      desc: 'تفکیک از مبدأ، فروش به پایلوت و درخواست آنلاین جمع‌آوری',
      ids: ['recycling']
    },
    {
      id: 'smart', title: 'زندگی شهری هوشمند', icon: '🧩',
      desc: 'ماژول‌های روزمره و دسترسی برخط به نقشه‌های مصوب شهری و روستایی',
      ids: ['superapp', 'ruralmap']
    },
    {
      id: 'transport', title: 'حمل‌ونقل و ترافیک', icon: '🚇',
      desc: 'برنامه حرکت قطارها، پرداخت عوارض تردد و پایش لحظه‌ای ناوگان',
      ids: ['metro', 'traffic', 'transit']
    }
  ];

  /* سرویس‌های پرمصرف برای «دسترسی سریع» */
  const QUICK_SERVICE_IDS = ['payment', 'recycling', 'ruralmap', 'metro', 'transit', 'business'];"""
assert old_groups in s
s = s.replace(old_groups, new_groups, 1)

# ---------- 3) جایگزینی منطق رندر فهرست با چیدمان پنلی (سبک پیشخوان) ----------
start = s.index("  function renderServices() {")
end = s.index("  /* =========================================================\n     Render — جزئیات هر سرویس")
new_render = '''  function renderServices() {
    const wrap = document.getElementById('servicesListWrap');
    if (!wrap) return;

    const total = EPLAK_SERVICES.length;

    wrap.innerHTML =
      '<div class="svc-count-strip">' +
        '<span class="svc-count-num">' + svcPersianDigits(total) + '</span>' +
        '<span class="svc-count-label">سرویس در ۵ بخش</span>' +
        '<span class="svc-count-sep"></span>' +
        '<span class="svc-count-hint">برای ورود به هر بخش، روی کادر آن بزنید</span>' +
      '</div>' +

      /* ===== دسترسی سریع (هم‌سبک با پیشخوان) ===== */
      '<div class="section-title">دسترسی سریع</div>' +
      '<div class="services-grid">' +
        QUICK_SERVICE_IDS.map(function (id) {
          const s = svcById(id);
          if (!s) return '';
          return '' +
            '<div class="service-card" onclick="openServiceDetail(\\'' + s.id + '\\')">' +
              '<div class="service-icon" style="background:rgba(' + s.accent + ',0.15);">' + s.icon + '</div>' +
              '<div><h3>' + s.short + '</h3><p>ورود مستقیم</p></div>' +
            '</div>';
        }).join('') +
      '</div>' +

      /* ===== پنل‌های هر بخش ===== */
      SERVICE_GROUPS.map(categoryPanelHtml).join('');
  }

  /* کادر مستقل هر بخش — با زدن روی هدرِ کادر وارد همان بخش می‌شوید */
  function categoryPanelHtml(group) {
    return '' +
      '<div class="svc-panel">' +
        '<div class="svc-panel-head" onclick="openServiceCategory(\\'' + group.id + '\\')">' +
          '<span class="svc-panel-icon">' + group.icon + '</span>' +
          '<div class="svc-panel-head-text">' +
            '<h3>' + group.title + '</h3>' +
            '<p>' + group.desc + '</p>' +
          '</div>' +
          '<span class="svc-panel-count">' + svcPersianDigits(group.ids.length) + '</span>' +
          '<span class="svc-panel-go">' + svcChevron() + '</span>' +
        '</div>' +
        '<div class="svc-panel-rows">' +
          group.ids.map(serviceRowHtml).join('') +
        '</div>' +
      '</div>';
  }

  /* هر سطر داخل کادرِ بخش — ورود مستقیم به صفحه همان سرویس */
  function serviceRowHtml(id) {
    const s = svcById(id);
    if (!s) return '';

    return '' +
      '<div class="svc-row" style="--accent:' + s.accent + ';" ' +
           'onclick="event.stopPropagation(); openServiceDetail(\\'' + s.id + '\\')">' +
        '<div class="svc-row-icon">' + s.icon + '</div>' +
        '<div class="svc-row-body">' +
          '<h4>' + s.title + '</h4>' +
          '<p>' + s.sub + '</p>' +
        '</div>' +
        (s.badge ? '<span class="svc-badge svc-badge-' + s.badge.tone + '">' + s.badge.text + '</span>' : '') +
        '<span class="svc-row-go">' + svcChevron() + '</span>' +
      '</div>';
  }

  /* باز کردن صفحه اختصاصیِ یک بخش */
  function openServiceCategory(catId) {
    const group = SERVICE_GROUPS.find(function (g) { return g.id === catId; });
    if (!group) return;

    const wrap = document.getElementById('serviceCategoryWrap');
    if (!wrap) return;

    let html = '' +
      '<div class="svc-cat-hero">' +
        '<span class="svc-cat-glow"></span>' +
        '<div class="svc-cat-hero-top">' +
          '<div class="svc-cat-icon">' + group.icon + '</div>' +
          '<div class="svc-cat-hero-text">' +
            '<h2>' + group.title + '</h2>' +
            '<p>' + group.desc + '</p>' +
            '<span class="svc-cat-meta">' + svcPersianDigits(group.ids.length) + ' سرویس در این بخش</span>' +
          '</div>' +
        '</div>' +
      '</div>';

    html += '<div class="section-title">سرویس‌های این بخش</div>';
    html += '<div class="svc-list" style="padding:0 16px;">' +
      group.ids.map(serviceCardHtml).join('') +
    '</div>';

    wrap.innerHTML = html;
    showScreen('screen-service-category');
  }

'''
s = s[:start] + new_render + s[end:]

io.open(P, "w", encoding="utf-8").write(s)
print("services.js restructured")
