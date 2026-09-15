/* core/state.js — وضعیت سراسری و داده‌های اپلیکیشن ای‌پلاک */
/* استخراج‌شده عیناً از فایل اصلی app_01.html بدون تغییر منطق */

  /* =========================================================
     ای‌پلاک — Application State & Data
  ========================================================= */

  const STATUS_LABEL = {
    all: 'همه',
    pending: 'در انتظار',
    in_progress: 'در حال بررسی',
    review: 'در حال بررسی',
    done: 'انجام شده'
  };
  const STATUS_CLASS = {
    all: 'status-review',
    pending: 'status-pending',
    in_progress: 'status-review',
    review: 'status-review',
    done: 'status-done'
  };

  function normalizeStatusValue(value) {
    const raw = String(value ?? '').trim();
    if (!raw) return 'pending';
    const normalized = raw.toLowerCase();
    const normalizedSafe = normalized.replace(/\s+/g, '').replace(/[_-]+/g, '');
    const map = {
      all: 'all',
      همه: 'all',
      'در انتظار': 'pending',
      pending: 'pending',
      wait: 'pending',
      waiting: 'pending',
      'در حال بررسی': 'in_progress',
      'درحال‌بررسی': 'in_progress',
      in_progress: 'in_progress',
      review: 'in_progress',
      بررسی: 'in_progress',
      'پاسخ داده شده': 'done',
      'پاسخ‌داده‌شده': 'done',
      'انجام شده': 'done',
      'انجام‌شده': 'done',
      done: 'done',
      completed: 'done',
      answered: 'done',
      'answereddone': 'done'
    };

    if (map[raw] !== undefined) return map[raw];
    if (map[normalized] !== undefined) return map[normalized];
    if (map[normalizedSafe] !== undefined) return map[normalizedSafe];
    return 'pending';
  }

  function getStatusMeta(status) {
    const key = normalizeStatusValue(status);
    return {
      key,
      label: STATUS_LABEL[key] || 'در انتظار',
      className: STATUS_CLASS[key] || 'status-pending'
    };
  }

  // الگوی معتبر شماره موبایل ایران: 09 + پیش‌شماره اپراتور معتبر + ۷ رقم باقیمانده
  // پیش‌شماره‌های پذیرفته‌شده: 090, 091, 092, 093, 099 (طبق تخصیص رگولاتوری ایران)
  const IRAN_MOBILE_REGEX = /^09(0[0-9]|1[0-9]|2[0-9]|3[0-9]|9[0-9])\d{7}$/;

  function isValidIranMobile(phone) {
    return typeof phone === 'string' && IRAN_MOBILE_REGEX.test(phone);
  }

  // Current logged-in user (mutable demo data) — مقداردهی اولیه از پروفایل ذخیره‌شده (در صورت وجود)
  const userProfile = {
    name: 'شهروند',
    phone: '',
    rawPhone: ''
  };

  // Reports — آرایه خالی؛ داده‌های واقعی هر کاربر از localStorage بارگذاری می‌شود (core/storage.js)
  let reports = [];
  let reportIdCounter = 1;

  const newsData = [
    { id: 'n1', title: 'افتتاح پارک جدید در منطقه شمالی ورامین', date: '۱۴۰۳/۰۳/۱۲', icon: '🌳',
      summary: 'پارک جدید شهر با امکانات ورزشی و فضای سبز گسترده افتتاح شد.',
      body: 'پارک جدید شهرداری ورامین با مساحت بیش از ۵ هکتار و امکاناتی شامل زمین‌های ورزشی، مسیر پیاده‌روی، فضای بازی کودکان و فضای سبز گسترده، آماده بهره‌برداری شهروندان عزیز شده است. این پروژه با مشارکت شهروندان و در راستای ارتقای کیفیت زندگی شهری اجرا شده است.' },
    { id: 'n2', title: 'اطلاعیه نوبت‌دهی پرداخت عوارض نوسازی', date: '۱۴۰۳/۰۳/۰۸', icon: '📋',
      summary: 'مهلت پرداخت عوارض نوسازی سال جاری تا پایان خرداد ماه تمدید شد.',
      body: 'به اطلاع شهروندان محترم می‌رساند مهلت پرداخت عوارض نوسازی سال جاری تا پایان خرداد ماه تمدید گردیده است. شهروندان می‌توانند از طریق بخش «پرداخت عوارض» همین برنامه نسبت به پرداخت بدهی خود اقدام نمایند.' },
    { id: 'n3', title: 'برگزاری جشنواره فرهنگی شهر ورامین', date: '۱۴۰۳/۰۲/۲۵', icon: '🎉',
      summary: 'جشنواره فرهنگی و هنری شهر با حضور هنرمندان محلی برگزار می‌شود.',
      body: 'شهرداری ورامین با همکاری اداره فرهنگ و ارشاد اسلامی، جشنواره فرهنگی و هنری شهر را با حضور هنرمندان محلی و برنامه‌های متنوع برای خانواده‌ها برگزار می‌کند. زمان و مکان دقیق برگزاری متعاقباً اعلام خواهد شد.' },
    { id: 'n4', title: 'آغاز طرح بازآفرینی بافت فرسوده مرکز شهر', date: '۱۴۰۳/۰۲/۱۰', icon: '🏗️',
      summary: 'طرح نوسازی و بازآفرینی بافت فرسوده مرکز شهر آغاز شد.',
      body: 'با هدف ارتقای کیفیت بصری و کالبدی مرکز شهر، طرح بازآفرینی بافت فرسوده با همکاری شهرداری و سازمان نوسازی شهری آغاز شده و طی فازهای مختلف تا پایان سال ادامه خواهد داشت.' }
  ];

  // Payments — آرایه خالی؛ داده‌های هر کاربر از localStorage بارگذاری می‌شود
  let payments = [];

  const mapPlaces = [
    { name: 'ساختمان مرکزی شهرداری', dist: '۲۰۰ متر', icon: '🏢', bg: 'rgba(0,201,167,0.12)' },
    { name: 'پارک شهر', dist: '۴۵۰ متر', icon: '🌳', bg: 'rgba(0,180,80,0.12)' },
    { name: 'بیمارستان امام خمینی', dist: '۱.۲ کیلومتر', icon: '🏥', bg: 'rgba(255,80,80,0.12)' },
    { name: 'کتابخانه عمومی', dist: '۸۰۰ متر', icon: '📚', bg: 'rgba(100,150,255,0.12)' },
    { name: 'میدان شهرداری', dist: '۲۰۰ متر', icon: '📍', bg: 'rgba(255,180,0,0.12)' },
    { name: 'پایانه مسافربری', dist: '۲.۵ کیلومتر', icon: '🚌', bg: 'rgba(150,80,255,0.12)' }
  ];

  // Notifications — آرایه خالی؛ داده‌های هر کاربر از localStorage بارگذاری می‌شود
  let notifications = [];

  // Favorites: ids reference home service cards
  const allServices = [
    { id: 's1', icon: '📋', bg: 'rgba(0,201,167,0.12)', title: 'ثبت درخواست', sub: 'گزارش مشکل', screen: 'screen-report' },
    { id: 's2', icon: '🔍', bg: 'rgba(100,150,255,0.12)', title: 'پیگیری درخواست', sub: 'وضعیت گزارش‌ها', screen: 'screen-track' },
    { id: 's3', icon: '📢', bg: 'rgba(255,120,0,0.12)', title: 'اخبار و اطلاعیه‌ها', sub: 'آخرین اخبار شهرداری', screen: 'screen-news' },
    { id: 's4', icon: '✨', bg: 'rgba(150,80,255,0.12)', title: 'خدمات', sub: 'سرویس‌های شهری', screen: 'screen-services' }
  ];
  // Favorites — آرایه خالی؛ داده‌های هر کاربر از localStorage بارگذاری می‌شود
  let favoriteIds = [];

  // Multi-step report form draft
  let reportDraft = { type: 'سایر', department: '', subDepartment: '', desc: '', location: '', photos: [] };
  let activeReportId = null; // for detail screen
  let pendingPaymentId = null;


  /* =========================================================
     Helpers
  ========================================================= */
  function toPersianDigits(input) {
    const fa = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
    return String(input).replace(/[0-9]/g, d => fa[d]);
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

