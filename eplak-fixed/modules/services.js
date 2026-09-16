/* modules/services.js — بخش «خدمات» (Services) */
/*
   این ماژول بخش جدید «خدمات» را در اپلیکیشن ای‌پلاک می‌سازد:
   - یک صفحه فهرست دسته‌بندی‌شده از سرویس‌ها (screen-services)
   - یک صفحه جزئیات پویا برای هر سرویس (screen-service-detail)

   همه محتواها در آرایه‌ی EPLAK_SERVICES تعریف شده‌اند؛ بنابراین هر سرویس
   متن، ویژگی‌ها و دکمه‌ی اقدامِ واقعیِ خودش را دارد (بدون متن خالی).
   طراحی با متغیر --accent (RGB) روی هر کارت انجام می‌شود تا با تم
   روز/شب و رنگ‌بندی کلی اپ هماهنگ بماند.
*/

  /* =========================================================
     Data — تعریف سرویس‌ها
  ========================================================= */

  const EPLAK_SERVICES = [

    /* ---------- ۱. پرداخت عوارض (منتقل‌شده به خدمات) ---------- */
    {
      id: 'payment',
      short: 'پرداخت عوارض',
      icon: '💳',
      accent: '150,80,255',
      title: 'پرداخت عوارض',
      sub: 'عوارض نوسازی، پسماند و قبوض شهری',
      badge: { text: 'فعال', tone: 'ok' },
      chips: ['استعلام با پلاک ملکی', 'پرداخت امن', 'رسید دیجیتال'],
      intro:
        'با وارد کردن پلاک ملکی یا شناسه قبض، بدهی عوارض نوسازی، پسماند و سایر قبوض شهری خود را در چند ثانیه استعلام کنید و بدون مراجعه حضوری، از طریق درگاه پرداخت امنِ مورد تأیید شهرداری تسویه نمایید. تمامی رسیدها در سوابق پرداخت پروفایل شما نگهداری می‌شود.',
      caps: [
        { icon: '💳', title: 'پرداخت آنلاین امن', desc: 'تسویه عوارض و قبوض از طریق درگاه بانکی با تأییدیه شهرداری.' },
        { icon: '🔢', title: 'استعلام با پلاک', desc: 'مشاهده بدهی تنها با وارد کردن پلاک ملکی یا شناسه قبض.' },
        { icon: '🧾', title: 'سوابق و رسیدها', desc: 'نگهداری رسیدهای دیجیتال در پروفایل برای مراجعات بعدی.' },
        { icon: '🔔', title: 'یادآوری سررسید', desc: 'اعلان خودکار پیش از پایان مهلت پرداخت هر قبض.' }
      ],
      action: { label: 'ورود به بخش پرداخت', kind: 'screen', target: 'screen-payment' }
    },

    /* ---------- ۲. دیسپلی کسب‌وکارهای محلی + ای‌پلاک ادز ---------- */
    {
      id: 'business',
      short: 'کسب‌وکارها',
      icon: '🏪',
      accent: '0,201,167',
      title: 'دیسپلی کسب‌وکارهای محلی',
      sub: 'ویترین دیجیتال اصناف همراه با ای‌پلاک ادز',
      badge: { text: 'جدید', tone: 'new' },
      chips: ['ویترین محله', 'تبلیغات هدفمند', 'نمایش روی نقشه'],
      intro:
        'هر واحد صنفی یک ویترین دیجیتال اختصاصی دارد: معرفی خدمات، ساعت کاری، تصاویر، راه‌های ارتباطی و موقعیت دقیق روی نقشه. کسب‌وکارها می‌توانند با «ای‌پلاک ادز» پیشنهادها و تخفیف‌های خود را دقیقاً به ساکنان همان محله نمایش دهند و شهروندان بر اساس نزدیکی و امتیاز مردمی انتخاب کنند.',
      caps: [
        { icon: '🏪', title: 'ویترین اختصاصی', desc: 'صفحه معرفی هر کسب‌وکار با تصاویر، ساعت کاری و راه‌های ارتباطی.' },
        { icon: '📣', title: 'ای‌پلاک ادز', desc: 'تبلیغات هدفمند بر اساس محله، دسته‌بندی و علاقه‌مندی شهروندان.' },
        { icon: '🗺️', title: 'نمایش روی نقشه', desc: 'نمایش کسب‌وکارها بر اساس نزدیکی و امتیاز مردمی روی نقشه شهر.' },
        { icon: '⭐', title: 'امتیاز و نظرات', desc: 'امتیازدهی شهروندان برای انتخاب آگاهانه و رقابت سالم.' }
      ],
      note: 'ثبت کسب‌وکار پس از بررسی کد صنفی و تأیید اتحادیه مربوطه فعال می‌شود.',
      action: { label: 'ثبت یا معرفی کسب‌وکار', kind: 'toast', toast: 'فرم ثبت کسب‌وکار در نسخه بعدی همین بخش فعال می‌شود' }
    },

    /* ---------- ۳. بوم‌گردی و گردشگری ---------- */
    {
      id: 'tourism',
      short: 'بوم‌گردی',
      icon: '🏕️',
      accent: '255,140,60',
      title: 'بوم‌گردی و گردشگری شهری',
      sub: 'معرفی و گسترش بوم‌گردی هر شهر',
      badge: { text: 'در حال توسعه', tone: 'soon' },
      chips: ['صنایع دستی', 'اقامتگاه بوم‌گردی', 'رویدادهای فصلی'],
      intro:
        'برای هر شهر یک پرونده اختصاصی ساخته می‌شود که بر اساس داده‌های ثبت‌شده همان شهر، جاذبه‌ها، اقامتگاه‌های بوم‌گردی، صنایع دستی و غذاهای محلی را معرفی می‌کند؛ از معرفی هنرمندان بومی و کارگاه‌های خانگی تا فروش مستقیم محصولات و رزرو اقامتگاه.',
      caps: [
        { icon: '🧭', title: 'اطلس جاذبه‌ها', desc: 'معرفی نقاط دیدنی، مسیرهای پیشنهادی و بهترین زمان بازدید.' },
        { icon: '🛖', title: 'اقامتگاه و هتلینگ بومی', desc: 'معرفی اقامتگاه‌های بوم‌گردی و خانه‌های محلی با ظرفیت و امکانات.' },
        { icon: '🧶', title: 'بازارچه صنایع دستی', desc: 'نمایش آثار هنرمندان محلی و امکان سفارش مستقیم.' },
        { icon: '🎉', title: 'رویدادها و جشنواره‌ها', desc: 'تقویم جشنواره‌های فصلی و آیین‌های محلی هر شهر.' }
      ],
      note: 'داده‌های هر شهر توسط دبیرخانه گردشگری همان شهر ثبت و تأیید می‌شود.',
      action: { label: 'مشاهده اطلس بوم‌گردی', kind: 'toast', toast: 'اطلس بوم‌گردی با داده‌های ثبت‌شده شهر به‌زودی در دسترس است' }
    },

    /* ---------- ۴. بازیافت و تفکیک پسماند ---------- */
    {
      id: 'recycling',
      short: 'بازیافت',
      icon: '♻️',
      accent: '0,180,110',
      title: 'بازیافت و تفکیک پسماند',
      sub: 'خرید توسط پایلوت و ثبت آنلاین درخواست جمع‌آوری',
      badge: { text: 'فعال', tone: 'ok' },
      chips: ['جمع‌آوری در محل', 'فروش به پایلوت', 'کیف پول سبز'],
      intro:
        'شهروندان مواد تفکیک‌شده را در محل تحویل می‌دهند و بهای آن‌ها بر اساس نرخ مصوب به «کیف پول سبز»شان واریز می‌شود. درخواست جمع‌آوری انواع ضایعات تفکیکی به‌صورت آنلاین ثبت و به نزدیک‌ترین پایلوت تأییدشده ارجاع می‌گردد؛ از کاغذ و پلاستیک تا فلز، شیشه و پسماند الکترونیک.',
      caps: [
        { icon: '♻️', title: 'درخواست جمع‌آوری آنلاین', desc: 'ثبت درخواست برای کاغذ، پلاستیک، فلز، شیشه و پسماند الکترونیک.' },
        { icon: '🚚', title: 'تحویل در محل', desc: 'تعیین زمان و آدرس برای دریافت مواد تفکیکی بدون مراجعه حضوری.' },
        { icon: '💰', title: 'فروش به پایلوت', desc: 'نرخ‌گذاری شفاف و تسویه از طریق کیف پول سبز شهروندی.' },
        { icon: '🌱', title: 'امتیاز و آموزش', desc: 'امتیاز سبز برای خانوارهای مشارکت‌کننده و آموزش تفکیک از مبدأ.' }
      ],
      action: {
        label: 'ثبت درخواست جمع‌آوری',
        kind: 'screen',
        target: 'screen-report',
        toast: 'نوع درخواست را «پسماند و بازیافت» انتخاب کنید'
      }
    },

    /* ---------- ۵. مکمل‌های سوپراپلیکیشن ---------- */
    {
      id: 'superapp',
      short: 'مکمل‌ها',
      icon: '🧩',
      accent: '100,150,255',
      title: 'مکمل‌های سوپراپلیکیشن ای‌پلاک',
      sub: 'آب‌وهوا، آلودگی هوا، اوقات شرعی و مدیریت ساختمان',
      badge: { text: 'جدید', tone: 'new' },
      chips: ['۴ ماژول کاربردی', 'به‌روزرسانی لحظه‌ای', 'شخصی‌سازی'],
      intro:
        'چهار ماژول پرکاربردِ روزمره در یک جا: پیش‌بینی آب‌وهوا و هشدارهای جوی، شاخص لحظه‌ای آلودگی هوا، اوقات شرعی بر اساس موقعیت شما و مدیریت هوشمند ساختمان. هر ماژول به‌صورت مستقل فعال می‌شود و در پیشخوان شما قابل چیدمان است.',
      modules: [
        { icon: '🌦️', title: 'آب‌وهوا', desc: 'پیش‌بینی ساعتی و روزانه، دما، بارش و هشدارهای جوی برای شهر شما.' },
        { icon: '🌫️', title: 'آلودگی هوا', desc: 'نمایش شاخص AQI، وضعیت روزهای ناسالم و توصیه‌های بهداشتی.' },
        { icon: '🕌', title: 'اوقات شرعی', desc: 'اذان صبح، ظهر و مغرب همراه با طلوع و غروب بر اساس موقعیت مکانی.' },
        { icon: '🏢', title: 'مدیریت ساختمان', desc: 'شارژ ماهانه، قبوض مشترک، اعلان‌های ساختمان و ارتباط با مدیر.' }
      ],
      caps: [
        { icon: '📍', title: 'بر اساس موقعیت شما', desc: 'نمایش داده‌ها برای محله یا شهر انتخابیِ کاربر.' },
        { icon: '🔔', title: 'اعلان‌های هوشمند', desc: 'هشدار برای روزهای ناسالم، بارش‌های شدید و سررسید شارژ.' },
        { icon: '🎛️', title: 'چیدمان دلخواه', desc: 'انتخاب ماژول‌های مورد نیاز برای نمایش در پیشخوان.' }
      ],
      action: { label: 'فعال‌سازی ماژول‌ها', kind: 'toast', toast: 'ماژول‌های انتخابی در پیشخوان شما قرار گرفت' }
    },

    /* ---------- ۶. نقشه طرح هادی روستایی ---------- */
    {
      id: 'ruralmap',
      short: 'طرح هادی',
      icon: '🗺️',
      accent: '255,200,0',
      title: 'نقشه طرح هادی روستایی',
      sub: 'نقشه آنلاین و یکپارچه به تفکیک هر آبادی',
      badge: { text: 'آنلاین', tone: 'live' },
      chips: ['استعلام قطعه', 'جلوگیری از کلاهبرداری', 'محدوده مصوب'],
      intro:
        'دسترسی برخط و در لحظه به نقشه مصوب طرح هادی هر روستا و آبادی؛ مشاهده محدوده، کاربری قطعات و حریم‌ها پیش از هرگونه معامله. این سرویس با شفاف‌سازی وضعیت هر قطعه، از معاملات غیرمجاز و کلاهبرداری در زمین‌های خارج از محدوده یا در حریم رودخانه‌ها جلوگیری می‌کند.',
      caps: [
        { icon: '🗺️', title: 'نقشه یکپارچه', desc: 'نمایش تمام آبادی‌ها در یک سامانه یکپارچه و به‌روز.' },
        { icon: '🔍', title: 'استعلام وضعیت قطعه', desc: 'بررسی کاربری (مسکونی، کشاورزی، تجاری) و وضعیت قطعه پیش از معامله.' },
        { icon: '⚠️', title: 'هشدار زمین‌های پرخطر', desc: 'علامت‌گذاری قطعات خارج از محدوده، در حریم یا دارای معارض.' },
        { icon: '🚧', title: 'گزارش تخلف', desc: 'ثبت گزارش تغییر کاربری یا ساخت‌وساز غیرمجاز با موقعیت دقیق.' }
      ],
      note: 'استعلام برخط صرفاً جنبه آگاهی‌بخشی دارد؛ برای انجام معامله رسمی به دفاتر اسناد رسمی مراجعه کنید.',
      action: { label: 'استعلام وضعیت قطعه', kind: 'toast', toast: 'سامانه استعلام قطعات پس از اتصال به پایگاه طرح هادی فعال می‌شود' }
    },

    /* ---------- ۷. مترو و قطارهای شهری و بین‌شهری ---------- */
    {
      id: 'metro',
      short: 'مترو و قطار',
      icon: '🚇',
      accent: '80,120,255',
      title: 'مترو و قطارهای شهری و بین‌شهری',
      sub: 'برنامه حرکت، وضعیت خطوط و برنامه‌ریزی سفر',
      badge: { text: 'به‌زودی', tone: 'soon' },
      chips: ['زمان‌بندی حرکت', 'مسیریاب سفر', 'اطلاع‌رسانی تأخیر'],
      intro:
        'مشاهده ساعت حرکت قطارهای شهری و بین‌شهری به تفکیک خط و ایستگاه، آگاهی از وضعیت لحظه‌ای خطوط و تأخیرها، و برنامه‌ریزی سفر با انتخاب کوتاه‌ترین مسیر. داده‌ها مستقیماً از مرکز کنترل بهره‌برداری دریافت و به‌صورت برخط به‌روزرسانی می‌شود.',
      caps: [
        { icon: '🚇', title: 'برنامه حرکت', desc: 'ساعت حرکت قطارها به تفکیک هر خط، ایستگاه و روز هفته.' },
        { icon: '📡', title: 'وضعیت لحظه‌ای خطوط', desc: 'نمایش تأخیرها، اختلال‌ها و تغییر مسیر به‌صورت برخط.' },
        { icon: '🧭', title: 'مسیریاب سفر', desc: 'انتخاب بهترین مسیر با کمترین تعویض و زمان تقریبی رسیدن.' },
        { icon: '🔔', title: 'اعلان تغییر برنامه', desc: 'دریافت هشدار برای تغییر زمان‌بندی خطوط مورد علاقه.' }
      ],
      action: { label: 'مشاهده برنامه حرکت', kind: 'toast', toast: 'برنامه حرکت پس از اتصال به مرکز کنترل بهره‌برداری نمایش داده می‌شود' }
    },

    /* ---------- ۸. پرداخت اینترنتی طرح ترافیک و آلودگی هوا ---------- */
    {
      id: 'traffic',
      short: 'طرح ترافیک',
      icon: '🚗',
      accent: '255,90,90',
      title: 'پرداخت طرح ترافیک و آلودگی هوا',
      sub: 'عوارض تردد در کلان‌شهرها، کاملاً آنلاین',
      badge: { text: 'آنلاین', tone: 'live' },
      chips: ['استعلام با پلاک', 'پرداخت اینترنتی', 'مدیریت سهمیه'],
      intro:
        'استعلام و پرداخت اینترنتی عوارض تردد در محدوده‌های طرح ترافیک و کنترل آلودگی هوا در کلان‌شهرها، تنها با وارد کردن شماره پلاک؛ بدون نیاز به مراجعه حضوری، با دریافت رسید معتبر و امکان مدیریت سهمیه روزانه و سالانه.',
      caps: [
        { icon: '🚗', title: 'استعلام با پلاک', desc: 'مشاهده بدهی تردد و تعداد روزهای مجاز باقی‌مانده.' },
        { icon: '💳', title: 'پرداخت آنلاین', desc: 'تسویه عوارض از درگاه بانکی و دریافت رسید دیجیتال.' },
        { icon: '🎟️', title: 'مدیریت سهمیه', desc: 'پیگیری سهمیه روزانه و سالانه و تمدید پیش از پایان اعتبار.' },
        { icon: '🔔', title: 'یادآوری اتمام مجوز', desc: 'اعلان پیش از پایان اعتبار مجوز تردد.' }
      ],
      action: { label: 'ورود به سامانه پرداخت', kind: 'toast', toast: 'درگاه پرداخت عوارض تردد به‌زودی در این بخش فعال می‌شود' }
    },

    /* ---------- ۹. پایش لحظه‌ای ناوگان عمومی و خرید بلیت ---------- */
    {
      id: 'transit',
      short: 'ناوگان عمومی',
      icon: '🚌',
      accent: '0,229,195',
      title: 'پایش ناوگان عمومی و خرید بلیت',
      sub: 'موقعیت لحظه‌ای تاکسیرانی، اتوبوسرانی و مترو برای عموم',
      badge: { text: 'لحظه‌ای', tone: 'live' },
      chips: ['پایش زنده', 'خرید آنلاین بلیت', 'زمان رسیدن'],
      intro:
        'موقعیت لحظه‌ای اتوبوس‌ها، تاکسی‌ها و قطارهای مترو روی نقشه برای همه شهروندان، همراه با زمان تقریبی رسیدن به هر ایستگاه و امکان خرید آنلاین بلیت یا شارژ کارت سفر. شفافیت عملکرد ناوگان، کیفیت خدمات و اعتماد عمومی را بالا می‌برد.',
      caps: [
        { icon: '📍', title: 'پایش لحظه‌ای ناوگان', desc: 'مشاهده زنده موقعیت اتوبوس، تاکسی و مترو روی نقشه برای عموم.' },
        { icon: '⏱️', title: 'زمان رسیدن به ایستگاه', desc: 'تخمین زمان رسیدن وسیله نقلیه بر اساس ترافیک لحظه‌ای.' },
        { icon: '🎫', title: 'خرید آنلاین بلیت', desc: 'خرید بلیت تک‌سفره و اعتباری و شارژ کارت سفر.' },
        { icon: '📮', title: 'شکایات و گم‌شده‌ها', desc: 'گزارش تأخیر، رفتار نامناسب راننده یا اشیای گم‌شده در ناوگان.' }
      ],
      action: { label: 'مشاهده ناوگان به‌صورت زنده', kind: 'toast', toast: 'پایش زنده ناوگان پس از اتصال به سامانه AVL فعال می‌شود' }
    }
  ];

  /* گروه‌بندی نمایش در صفحه خدمات */
  const SERVICE_GROUPS = [
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
  const QUICK_SERVICE_IDS = ['payment', 'recycling', 'ruralmap', 'metro', 'transit', 'business'];

  let activeServiceId = null;

  /* =========================================================
     Helpers
  ========================================================= */
  function svcById(id) {
    return EPLAK_SERVICES.find(function (s) { return s.id === id; }) || null;
  }

  /* تبدیل اعداد به فارسی؛ اگر تابع سراسری در دسترس نبود، از نسخه محلی استفاده می‌شود
     (برای سازگاری با هر دو نسخه وب و اندروید) */
  function svcPersianDigits(input) {
    if (typeof toPersianDigits === 'function') return toPersianDigits(input);
    const fa = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return String(input).replace(/[0-9]/g, function (d) { return fa[d]; });
  }

  function svcChevron() {
    /* width/height صریح: حتی اگر فایل استایل قدیمی از کش لود شود،
       آیکون هرگز بزرگ‌تر از اندازه تعیین‌شده نمایش داده نمی‌شود. */
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>';
  }

  /* =========================================================
     Render — فهرست خدمات
  ========================================================= */
  function renderServices() {
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
            '<div class="service-card" onclick="openServiceDetail(\'' + s.id + '\')">' +
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
        '<div class="svc-panel-head" onclick="openServiceCategory(\'' + group.id + '\')">' +
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

  /* کارت بزرگ سرویس — برای صفحه اختصاصی هر بخش */
  function serviceCardHtml(id) {
    const s = svcById(id);
    if (!s) return '';

    return '' +
      '<div class="svc-card" style="--accent:' + s.accent + ';" onclick="openServiceDetail(\'' + s.id + '\')">' +
        '<span class="svc-card-glow"></span>' +
        '<div class="svc-icon-tile">' + s.icon + '</div>' +
        '<div class="svc-card-body">' +
          '<div class="svc-card-head">' +
            '<h3>' + s.title + '</h3>' +
            (s.badge ? '<span class="svc-badge svc-badge-' + s.badge.tone + '">' + s.badge.text + '</span>' : '') +
          '</div>' +
          '<p>' + s.sub + '</p>' +
          '<div class="svc-chips">' +
            s.chips.map(function (c) { return '<span class="svc-chip">' + c + '</span>'; }).join('') +
          '</div>' +
        '</div>' +
        '<span class="svc-go">' + svcChevron() + '</span>' +
      '</div>';
  }

  /* هر سطر داخل کادرِ بخش — ورود مستقیم به صفحه همان سرویس */
  function serviceRowHtml(id) {
    const s = svcById(id);
    if (!s) return '';

    return '' +
      '<div class="svc-row" style="--accent:' + s.accent + ';" ' +
           'onclick="event.stopPropagation(); openServiceDetail(\'' + s.id + '\')">' +
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

  /* =========================================================
     Render — جزئیات هر سرویس
  ========================================================= */
  function openServiceDetail(id) {
    const s = svcById(id);
    if (!s) return;
    activeServiceId = id;

    const wrap = document.getElementById('serviceDetailWrap');
    if (!wrap) return;

    let html = '';

    /* Hero */
    html += '' +
      '<div class="svc-detail-hero" style="--accent:' + s.accent + ';">' +
        '<span class="svc-detail-glow"></span>' +
        '<div class="svc-detail-hero-top">' +
          '<div class="svc-icon-tile lg">' + s.icon + '</div>' +
          '<div class="svc-detail-hero-text">' +
            '<h2>' + s.title + '</h2>' +
            '<p>' + s.sub + '</p>' +
            (s.badge ? '<span class="svc-badge svc-badge-' + s.badge.tone + '">' + s.badge.text + '</span>' : '') +
          '</div>' +
        '</div>' +
      '</div>';

    /* معرفی */
    html += '' +
      '<div class="glass-card svc-intro-card">' +
        '<div class="svc-intro-label">این سرویس چیست؟</div>' +
        '<p>' + s.intro + '</p>' +
      '</div>';

    /* ماژول‌ها (برای سرویس‌های چندبخشی) */
    if (s.modules && s.modules.length) {
      html += '<div class="section-title">ماژول‌های این سرویس</div>';
      html += '<div class="svc-modules">' +
        s.modules.map(function (m) {
          return '' +
            '<div class="svc-module" style="--accent:' + s.accent + ';">' +
              '<div class="svc-module-icon">' + m.icon + '</div>' +
              '<div class="svc-module-body">' +
                '<h4>' + m.title + '</h4>' +
                '<p>' + m.desc + '</p>' +
              '</div>' +
            '</div>';
        }).join('') +
      '</div>';
    }

    /* قابلیت‌ها */
    if (s.caps && s.caps.length) {
      html += '<div class="section-title">چه چیزهایی ارائه می‌دهد؟</div>';
      html += '<div class="svc-caps">' +
        s.caps.map(function (c) {
          return '' +
            '<div class="svc-cap" style="--accent:' + s.accent + ';">' +
              '<div class="svc-cap-icon">' + c.icon + '</div>' +
              '<div class="svc-cap-body">' +
                '<h4>' + c.title + '</h4>' +
                '<p>' + c.desc + '</p>' +
              '</div>' +
            '</div>';
        }).join('') +
      '</div>';
    }

    /* نکته */
    if (s.note) {
      html += '<div class="svc-note"><span class="svc-note-icon">💡</span><p>' + s.note + '</p></div>';
    }

    /* دکمه اقدام */
    if (s.action) {
      html += '<button class="btn-teal svc-action-btn" onclick="serviceAction(\'' + s.id + '\')">' +
        '<span>' + s.action.label + '</span>' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><path d="M5 12h14M12 5l7 7-7 7"/></svg>' +
      '</button>';
    }

    wrap.innerHTML = html;
    showScreen('screen-service-detail');
  }

  /* اجرای دکمه اقدام هر سرویس */
  function serviceAction(id) {
    const s = activeServiceId === id ? svcById(id) : svcById(id);
    if (!s || !s.action) return;
    const a = s.action;

    if (a.kind === 'screen' && a.target) {
      showScreen(a.target);
      if (a.toast) showToast(a.toast);
      return;
    }
    showToast(a.toast || 'این سرویس به‌زودی فعال می‌شود');
  }

  /* =========================================================
     Auto-hook — اتصال خودکار به showScreen
     با این هوک، رفتن به صفحه خدمات در هر نسخه‌ای (وب یا وب‌ویو اندروید)
     باعث رندر خودکار فهرست می‌شود؛ حتی اگر core/router.js دست‌نخورده باشد.
  ========================================================= */
  (function svcAutoHook() {
    if (typeof window === 'undefined' || window.__eplakServicesHooked) return;
    window.__eplakServicesHooked = true;

    var originalShowScreen = window.showScreen;
    if (typeof originalShowScreen === 'function') {
      window.showScreen = function (id) {
        originalShowScreen(id);
        if (id === 'screen-services' && typeof renderServices === 'function') {
          renderServices();
        }
      };
    }
  })();
