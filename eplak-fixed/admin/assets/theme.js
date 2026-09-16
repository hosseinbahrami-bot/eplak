/* ============================================
   کلید حالت شب / روز — پنل مدیریت ای‌پلاک
   - انتخاب کاربر در localStorage ذخیره می‌شود
   - اگر کاربر انتخاب نکرده باشد، تنظیم سیستم ملاک است
   ============================================ */
(function () {
    var KEY = 'eplak_admin_theme';
    var root = document.documentElement;

    /* اعمال تم ذخیره‌شده در اولین فرصت (جلوگیری از پرش رنگ) */
    try {
        var saved = localStorage.getItem(KEY);
        if (saved === 'dark' || saved === 'light') {
            root.setAttribute('data-theme', saved);
        }
    } catch (e) { /* localStorage در دسترس نیست */ }

    function activeTheme() {
        var t = root.getAttribute('data-theme');
        if (t === 'dark' || t === 'light') return t;
        return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
    }

    function hasFontAwesome() {
        var spans = document.createElement('span');
        spans.className = 'fas';
        spans.style.cssText = 'position:absolute;visibility:hidden;font-family:"Font Awesome 6 Free"';
        document.body.appendChild(spans);
        var ok = getComputedStyle(spans, null).fontFamily.indexOf('Font Awesome') > -1;
        document.body.removeChild(spans);
        return ok;
    }

    function paint(btn) {
        var dark = activeTheme() === 'dark';
        var icon = hasFontAwesome()
            ? (dark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>')
            : (dark ? '☀️' : '🌙');
        btn.innerHTML = icon + '<span>' + (dark ? 'حالت روز' : 'حالت شب') + '</span>';
        btn.setAttribute('title', dark ? 'تغییر به حالت روز' : 'تغییر به حالت شب');
        btn.setAttribute('aria-label', dark ? 'تغییر به حالت روز' : 'تغییر به حالت شب');
    }

    function createToggle() {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'theme-toggle';

        btn.addEventListener('click', function () {
            var next = activeTheme() === 'dark' ? 'light' : 'dark';
            root.setAttribute('data-theme', next);
            try { localStorage.setItem(KEY, next); } catch (e) {}
            paint(btn);
        });

        var topbar = document.querySelector('.topbar');
        var loginBox = document.querySelector('.login-box');
        if (topbar) {
            topbar.appendChild(btn);
        } else if (loginBox) {
            /* صفحه ورود: کلید درون کارت و در گوشه آن جای می‌گیرد (بدون تداخل) */
            btn.className = 'theme-toggle theme-toggle-inbox';
            loginBox.insertBefore(btn, loginBox.firstChild);
        } else {
            btn.className = 'theme-toggle theme-toggle-fixed';
            document.body.appendChild(btn);
        }
        paint(btn);

        /* اگر تنظیم سیستم تغییر کرد و کاربر انتخاب دستی ندارد */
        if (window.matchMedia) {
            var mq = window.matchMedia('(prefers-color-scheme: dark)');
            var onChange = function () {
                if (!localStorage.getItem(KEY)) paint(btn);
            };
            if (mq.addEventListener) mq.addEventListener('change', onChange);
            else if (mq.addListener) mq.addListener(onChange);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createToggle);
    } else {
        createToggle();
    }
})();
