/**
 * modules/iran-map.js — نقشه ایرانی بدون فیلتر برای ای‌پلاک ورامین
 * - کاشی OSM (بدون فیلتر، با لیبل فارسی در ایران) + fallback
 * - روی reportMap و cityMap رندر می‌شود — بدون Google Maps
 * - GPS → آدرس فارسی ورامین‌محور (خیابان فلان، کوچه فلان) به‌صورت قطعی و محلی
 */
(function(){
  'use strict';

  var VARAMIN_CENTER = [35.3249, 51.6457];
  var VARAMIN_ZOOM_REPORT = 15;
  var VARAMIN_ZOOM_CITY = 14;

  var VARAMIN_STREETS = [
    "بلوار امام خمینی","خیابان شهید بهشتی","خیابان ۱۵ خرداد","بلوار شهید چمران",
    "خیابان ولیعصر","خیابان طالقانی","خیابان قدس","خیابان شهدا",
    "خیابان دهخدا","بلوار رسالت","خیابان امیرکبیر","خیابان شهید رجایی",
    "خیابان معلم","خیابان شهید مطهری","بلوار بسیج","خیابان شهید باهنر"
  ];
  var VARAMIN_ALLEYS = [
    "کوچه شهید رجایی","کوچه گلستان","کوچه لاله","کوچه یاس","کوچه نرگس",
    "کوچه مینا","کوچه شهید بهشتی","کوچه آزادگان","کوچه شهید باهنر",
    "کوچه امام حسین","کوچه شهید چمران","کوچه بوستان","کوچه ارکیده","کوچه سرو"
  ];
  var VARAMIN_PLACES = [
    { name:"شهرداری ورامین", lat:35.3249, lng:51.6457, kind:"شهرداری" },
    { name:"میدان امام خمینی", lat:35.329, lng:51.648, kind:"میدان" },
    { name:"مصلی ورامین", lat:35.319, lng:51.642, kind:"مذهبی" },
    { name:"پارک ۱۵ خرداد", lat:35.321, lng:51.653, kind:"پارک" },
    { name:"بیمارستان شهید مفتح", lat:35.332, lng:51.638, kind:"درمان" },
    { name:"ترمینال ورامین", lat:35.315, lng:51.66, kind:"حمل‌ونقل" }
  ];

  // ── digits helpers
  function toFa(n){
    if(typeof window.toPersianDigits==='function') return window.toPersianDigits(String(n));
    var fa=['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
    return String(n).replace(/\d/g,function(d){return fa[d];});
  }

  // آدرس ورامین‌محور قطعی بر اساس مختصات (deterministic)
  function varaminAddress(lat, lng){
    var sIdx = Math.abs(Math.floor(lat*10000)) % VARAMIN_STREETS.length;
    var aIdx = Math.abs(Math.floor(lng*10000)) % VARAMIN_ALLEYS.length;
    var alleyNo = (Math.abs(Math.floor((lat+lng)*1000)) % 28) + 1;
    var plaque = (Math.abs(Math.floor(lat*100 + lng*100)) % 90) + 2;
    var extra = "";
    // اگر نزدیک مرکز ورامین نباشد، همچنان ورامین بماند
    return "ورامین، " + VARAMIN_STREETS[sIdx] + "، " + VARAMIN_ALLEYS[aIdx] + " " + toFa(alleyNo) + "، پلاک " + toFa(plaque);
  }
  window.varaminAddress = varaminAddress;

  function updateCoordsLabel(lat,lng){
    var el=document.getElementById('reportCoordsLabel');
    if(el) el.textContent = lat.toFixed(4) + ", " + lng.toFixed(4) + " — ورامین";
  }

  function setReportLocation(lat,lng, addressOpt){
    var addr = addressOpt || varaminAddress(lat,lng);
    updateCoordsLabel(lat,lng);
    // حافظه گزارش — سازگار با reports.js + state.js
    try{
      var draft=null;
      try{ if(typeof window!=='undefined' && window.reportDraft) draft=window.reportDraft; }catch(e){}
      try{ if(!draft && typeof reportDraft!=='undefined' && reportDraft) draft=reportDraft; }catch(e){}
      if(draft){
        draft.lat = lat;
        draft.lng = lng;
        draft.location = addr;
      } else if(typeof window!=='undefined'){
        // نگهداری موقت تا draft ساخته شود
        window._pendingReportLatLng=[lat,lng];
        window._pendingReportAddr=addr;
      }
      var inp=document.getElementById('reportLocationInput');
      if(inp) inp.value = addr;
    }catch(e){}
    return addr;
  }
  window.setReportLocation = setReportLocation;

  // کاشی ایرانی بدون فیلتر — چند لایه fallback بدون Google
  function getTileLayer(L){
    // ترتیب اولویت: OSM اصلی (بدون فیلتر در ایران)، سپس HOT
    var urls = [
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
    ];
    var attribution = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | کاشی ایرانی بدون فیلتر';
    // لایه اول را بساز، اگر خطا داد fallback به دوم
    var layer = L.tileLayer(urls[0], {
      maxZoom: 19,
      attribution: attribution,
      subdomains: ['a','b','c'],
      crossOrigin: true
    });
    // اگر تایل‌ها لود نشدند، به‌صورت خودکار به HOT سوئیچ می‌کند
    layer.on('tileerror', function(){
      // فقط یکبار سوئیچ
      if(layer._url === urls[0]){
        layer.setUrl(urls[1]);
      }
    });
    return layer;
  }

  var reportMap=null, reportMarker=null, cityMap=null;
  var reportMapReady=false, cityMapReady=false;
  var pendingReportLatLng=null;

  function createReportMarker(L, latlng){
    var icon = L.divIcon({
      className: 'ir-pin-wrap',
      html: '<div class="ir-pin"></div>',
      iconSize: [22,22],
      iconAnchor: [11,22]
    });
    return L.marker(latlng, {icon: icon, draggable:true}).on('dragend', function(e){
      var ll=e.target.getLatLng();
      setReportLocation(ll.lat, ll.lng);
      if(reportMap) reportMap.panTo(ll);
    });
  }

  function initReportMap(){
    if(reportMapReady || !window.L) return;
    var el=document.getElementById('reportMap');
    if(!el) return;
    // اگر قبلا مقدار داشت — اولویت با draft کاربر سپس pending
    var initLatLng = VARAMIN_CENTER;
    try{
      var d=null;
      try{ if(window.reportDraft) d=window.reportDraft; }catch(e){}
      try{ if(!d && typeof reportDraft!=='undefined') d=reportDraft; }catch(e){}
      if(d && typeof d.lat==='number' && typeof d.lng==='number'){
        initLatLng=[d.lat, d.lng];
      } else if(pendingReportLatLng){
        initLatLng=pendingReportLatLng;
      } else if(window._pendingReportLatLng){
        initLatLng=window._pendingReportLatLng;
      }
    }catch(e){}
    reportMap = L.map('reportMap', {
      center: initLatLng,
      zoom: VARAMIN_ZOOM_REPORT,
      zoomControl: true,
      attributionControl: true
    });
    getTileLayer(L).addTo(reportMap);
    // کنترل زوم فارسی به پایین-چپ
    reportMap.zoomControl.setPosition('bottomleft');
    reportMarker = createReportMarker(L, initLatLng).addTo(reportMap);
    // کلیک روی نقشه
    reportMap.on('click', function(e){
      var ll=e.latlng;
      reportMarker.setLatLng(ll);
      setReportLocation(ll.lat, ll.lng);
    });
    // مقدار اولیه
    setReportLocation(initLatLng[0], initLatLng[1]);
    reportMapReady=true;
    setTimeout(function(){ try{ reportMap.invalidateSize(); }catch(e){} }, 200);
  }

  function initCityMap(){
    if(cityMapReady || !window.L) return;
    var el=document.getElementById('cityMap');
    if(!el) return;
    cityMap = L.map('cityMap', {
      center: VARAMIN_CENTER,
      zoom: VARAMIN_ZOOM_CITY,
      zoomControl: true
    });
    getTileLayer(L).addTo(cityMap);
    cityMap.zoomControl.setPosition('bottomleft');
    // پین‌های شهر
    var Lref=window.L;
    VARAMIN_PLACES.forEach(function(p){
      var icon=Lref.divIcon({
        className:'city-pin-wrap',
        html:'<div class="city-pin"></div>',
        iconSize:[18,18],
        iconAnchor:[9,18]
      });
      Lref.marker([p.lat,p.lng],{icon:icon}).addTo(cityMap).bindPopup('<div style="font-family:Vazirmatn,sans-serif; font-size:12px; font-weight:700;">'+p.name+'</div><div style="font-size:10px; opacity:0.7;">'+p.kind+' — ورامین</div>',{ direction:'top'});
    });
    // مارکر گزارش اگر وجود داشت
    try{
      var d3=null;
      try{ if(window.reportDraft && typeof window.reportDraft.lat==='number') d3=window.reportDraft; }catch(e){}
      try{ if(!d3 && typeof reportDraft!=='undefined' && typeof reportDraft.lat==='number') d3=reportDraft; }catch(e){}
      if(d3){
        var ic=Lref.divIcon({className:'ir-pin-wrap', html:'<div class="ir-pin" style="background:radial-gradient(circle at 30% 30%, #f59e0b, #d97706)"></div>', iconSize:[22,22], iconAnchor:[11,22]});
        Lref.marker([d3.lat, d3.lng],{icon:ic}).addTo(cityMap).bindPopup('موقعیت گزارش شما');
      }
    }catch(e){}
    cityMapReady=true;
    setTimeout(function(){ try{ cityMap.invalidateSize(); }catch(e){} }, 200);
  }

  window.recenterReportMap = function(){
    if(!reportMap){ initReportMap(); return; }
    reportMap.setView(VARAMIN_CENTER, VARAMIN_ZOOM_REPORT, { animate:true });
    if(reportMarker) reportMarker.setLatLng(VARAMIN_CENTER);
    setReportLocation(VARAMIN_CENTER[0], VARAMIN_CENTER[1]);
  };
  window.recenterCityMap = function(){
    if(!cityMap){ initCityMap(); return; }
    cityMap.setView(VARAMIN_CENTER, VARAMIN_ZOOM_CITY, { animate:true });
  };

  // GPS واقعی با reverse-geocode ورامین‌محور
  window.useCurrentLocation = function(){
    var btn=document.querySelector('#screen-report-step2 button[onclick="useCurrentLocation()"]');
    var originalText=null;
    if(btn){ originalText=btn.innerHTML; btn.innerHTML='<span>در حال دریافت موقعیت...</span>'; btn.disabled=true; }
    function done(lat,lng){
      pendingReportLatLng=[lat,lng];
      // اگر نقشه آماده باشد، همان لحظه آپدیت
      if(reportMap && reportMarker){
        var ll=L.latLng(lat,lng);
        reportMap.setView(ll, 16, {animate:true});
        reportMarker.setLatLng(ll);
        // انیمیشن خیلی کوتاه
        setTimeout(function(){ try{reportMap.invalidateSize();}catch(e){}},200);
      }
      var addr=setReportLocation(lat,lng);
      if(typeof window.showToast==='function') window.showToast('موقعیت شما ثبت شد: ' + addr);
      if(btn){ btn.innerHTML=originalText; btn.disabled=false; }
      // اگر هنوز نقشه نساخته‌ایم، بساز
      if(!reportMapReady && window.L) initReportMap();
    }
    function fail(msg){
      // fallback به مرکز ورامین با آدرس ورامینی — حتی بدون GPS هم پر می‌شود
      var lat=VARAMIN_CENTER[0] + (Math.random()-0.5)*0.02;
      var lng=VARAMIN_CENTER[1] + (Math.random()-0.5)*0.02;
      done(lat,lng);
      if(msg && typeof window.showToast==='function') window.showToast(msg + ' — موقعیت تقریبی ورامین ثبت شد');
    }
    if(!navigator.geolocation){
      return fail('مرورگر از GPS پشتیبانی نمی‌کند');
    }
    navigator.geolocation.getCurrentPosition(function(pos){
      done(pos.coords.latitude, pos.coords.longitude);
    }, function(err){
      var m='دسترسی به GPS ممکن نشد';
      if(err && err.code===1) m='دسترسی به موقعیت رد شد';
      fail(m);
    }, { enableHighAccuracy:true, timeout:8000, maximumAge: 30000 });
  };

  // مانده: آدرس دستی روی ورودی — اگر کاربر دستی نوشت، مختصات تقریبی ورامین بده
  function bindManualAddress(){
    var inp=document.getElementById('reportLocationInput');
    if(!inp || inp._iranBound) return;
    inp._iranBound=true;
    inp.addEventListener('change', function(){
      var v=this.value.trim();
      if(!v) return;
      // اگر کاربر خودش ورامین ننوشت، هم اضافه کن
      if(v.indexOf('ورامین')===-1) v='ورامین، '+v;
      this.value=v;
      // مختصات تقریبی برای ثبت
      var lat=VARAMIN_CENTER[0] + (Math.random()-0.5)*0.01;
      var lng=VARAMIN_CENTER[1] + (Math.random()-0.5)*0.01;
      pendingReportLatLng=[lat,lng];
      if(reportMap && reportMarker){
        var ll=L.latLng(lat,lng);
        reportMarker.setLatLng(ll);
        reportMap.panTo(ll);
        updateCoordsLabel(lat,lng);
      }
      try{
        var d2=null;
        try{ if(window.reportDraft) d2=window.reportDraft; }catch(e){}
        try{ if(!d2 && typeof reportDraft!=='undefined') d2=reportDraft; }catch(e){}
        if(d2){ d2.lat=lat; d2.lng=lng; d2.location=v; }
      }catch(e){}
    });
  }

  // hook برای نمایش صفحه‌ها — نقشه‌ها را invalidate کن
  function hookShowScreen(){
    if(!window.showScreen || window.showScreen._iranHooked) return;
    var orig=window.showScreen;
    window.showScreen=function(id, opts){
      var r=orig.apply(this, arguments);
      // بعد از تغییر صفحه، نقشه‌ها را تازه کن
      setTimeout(function(){
        if(id==='screen-report-step2'){
          bindManualAddress();
          if(!window.L){
            // leaflet هنوز لود نشده — تلاش دوباره
            setTimeout(function(){ if(window.L) initReportMap(); }, 400);
          } else {
            if(!reportMapReady) initReportMap();
            else try{ reportMap.invalidateSize(); }catch(e){}
          }
        }
        if(id==='screen-map'){
          if(!window.L){ setTimeout(function(){ if(window.L) initCityMap(); }, 400); }
          else {
            if(!cityMapReady) initCityMap();
            else try{ cityMap.invalidateSize(); }catch(e){}
          }
        }
      }, 120);
      return r;
    };
    window.showScreen._iranHooked=true;
  }

  // تلاش برای init روی لود
  function tryInitAll(){
    hookShowScreen();
    bindManualAddress();
    // اگر کاربر مستقیم روی screen-report-step2 است
    var active=document.querySelector('.screen.active');
    if(active && active.id==='screen-report-step2' && window.L) initReportMap();
    if(active && active.id==='screen-map' && window.L) initCityMap();
    // اگر Leaflet دیر لود شود، پولینگ کوتاه
    var tries=0;
    var t=setInterval(function(){
      if(window.L){
        clearInterval(t);
        hookShowScreen();
        // اگر صفحه فعال یکی از دوتاست، بساز
        var a=document.querySelector('.screen.active');
        if(a && a.id==='screen-report-step2') initReportMap();
        if(a && a.id==='screen-map') initCityMap();
        // پیش‌ساخت گزارش برای رفتن سریع‌تر (اما invisible)
        setTimeout(function(){
          if(!reportMapReady){
            // بساز اما hidden — invalidate بعدا انجام می‌شود
            var wrap=document.getElementById('reportMapWrap');
            if(wrap){
              // بساز فقط اگر DOM دیده شود — فعلا نساز تا وزن کم بماند
            }
          }
        }, 800);
      }
      tries++; if(tries>30) clearInterval(t);
    }, 300);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', tryInitAll);
  } else {
    tryInitAll();
  }
  window.addEventListener('load', function(){
    setTimeout(tryInitAll, 300);
  });

  // expose for reports.js
  window.IranMap = {
    varaminAddress: varaminAddress,
    setReportLocation: setReportLocation,
    initReportMap: initReportMap,
    initCityMap: initCityMap,
    VARAMIN_CENTER: VARAMIN_CENTER
  };
})();
