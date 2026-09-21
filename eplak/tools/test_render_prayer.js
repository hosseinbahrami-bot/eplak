const timings = {
  Fajr: '04:26',
  Sunrise: '05:50',
  Dhuhr: '11:57',
  Asr: '15:26',
  Maghrib: '18:22',
  Isha: '19:09'
};

function nowMinutes() {
  const tf = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Tehran', hour: 'numeric', minute: 'numeric', hour12: false });
  const parts = tf.formatToParts(new Date());
  let h = 0, m = 0;
  parts.forEach(function (p) {
    if (p.type === 'hour') h = parseInt(p.value, 10);
    if (p.type === 'minute') m = parseInt(p.value, 10);
  });
  if (h === 24) h = 0;
  return h * 60 + m;
}

const PRAYERS = [
  { key: 'Fajr',    fa: 'اذان صبح', en: 'Fajr' },
  { key: 'Sunrise', fa: 'طلوع',     en: 'Sunrise' },
  { key: 'Dhuhr',   fa: 'اذان ظهر', en: 'Dhuhr' },
  { key: 'Asr',     fa: 'اذان عصر', en: 'Asr' },
  { key: 'Maghrib', fa: 'اذان مغرب', en: 'Maghrib' },
  { key: 'Isha',    fa: 'اذان عشاء', en: 'Isha' }
];

function toMinutes(hhmm) {
  const parts = String(hhmm || '').split(':');
  return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
}

function nextPrayer(timings) {
  const now = nowMinutes();
  let best = null;
  PRAYERS.forEach(function (p) {
    const mins = toMinutes(timings ? timings[p.key] : null);
    if (mins == null) return;
    if (mins > now && (best == null || mins < best.mins)) {
      best = { key: p.key, fa: p.fa, en: p.en, mins: mins };
    }
  });
  if (!best && timings) {
    const first = toMinutes(timings[PRAYERS[0].key]);
    if (first != null) best = { key: PRAYERS[0].key, fa: PRAYERS[0].fa, en: PRAYERS[0].en, mins: first + 1440 };
  }
  return best;
}

function fa(str) {
  const f = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  return String(str).replace(/[0-9]/g, function (w) { return f[Number(w)]; });
}

function countdownText(next) {
  if (!next) return '';
  const diff = next.mins - nowMinutes();
  const mins = diff > 0 ? diff : diff + 1440;
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  const isSunrise = (next.key === 'Sunrise');
  const targetName = isSunrise ? 'طلوع' : 'اذان';
  if (h <= 0) return fa(m) + ' دقیقه تا ' + targetName;
  return fa(h) + ' ساعت و ' + fa(m) + ' دقیقه تا ' + targetName;
}

const next = nextPrayer(timings);
console.log("Tehran current time in minutes:", nowMinutes());
console.log("Next prayer:", next.fa, "(key:", next.key, "mins:", next.mins, ")");
console.log("Countdown text:", countdownText(next));
