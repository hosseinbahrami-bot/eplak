import re

css_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace weather 3D styles with authentic Apple Weather design
apple_css = """/* ============================================================
   سیستم استایل آب‌وهوای الهام‌گرفته از اپل (Apple Weather iOS Design)
   - کادر کاملاً ثابت و ایستا (بدون چرخش و لرزش)
   - ابرهای کوچک، ظریف و ارگانیک (Small, Elegant Volumetric Clouds)
   - باران کریستالی و باریک (Apple Needle Rain) با پاشش آب ملایم
   - تایپوگرافی شیک و کپسول شیشه‌ای یکپارچه پایین کادر مشابه iOS 18
   ============================================================ */

.apple-weather-wrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

/* نوار چیپ‌های کپسولی شیشه‌ای اپل */
.apple-chips-scroll {
  width: 100%;
  overflow-x: auto;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
  padding: 1px 2px 4px;
}
.apple-chips-scroll::-webkit-scrollbar {
  display: none;
}
.apple-chips {
  display: flex;
  gap: 6px;
  width: max-content;
}
.apple-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.apple-chip:hover {
  background: rgba(255, 255, 255, 0.16);
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
}
.apple-chip.active {
  background: #ffffff;
  border-color: #ffffff;
  color: #0f172a;
  font-weight: 700;
  box-shadow: 0 3px 12px rgba(255, 255, 255, 0.35);
}
.apple-chip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 6px #10B981;
}

/* کادر اصلی اپل ودر: کاملاً ثابت، بدون چرخش و لرزش (Rock-Solid Frame) */
.apple-weather-card {
  position: relative;
  width: 100%;
  height: 252px;
  border-radius: 26px;
  overflow: hidden;
  box-shadow:
    0 16px 40px -10px rgba(0,0,0,0.5),
    0 0 0 1px rgba(255,255,255,0.16) inset;
  isolation: isolate;
  user-select: none;
  -webkit-user-select: none;
  transform: none !important; /* تضمین ثبات صددرصدی کادر */
}

/* پس‌زمینه رنگ آسمان با گرادینت اتمسفریک پیوسته */
.apple-sky-bg {
  position: absolute;
  inset: 0;
  z-index: 1;
  transition: background 0.9s cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* روز آفتابی اپل */
.apple-sky-bg.sky-day {
  background: linear-gradient(180deg, #1C7ED6 0%, #339AF0 42%, #74C0FC 78%, #A5D8FF 100%);
}
/* شب صاف اپل */
.apple-sky-bg.sky-night {
  background: linear-gradient(180deg, #060B18 0%, #0D162B 40%, #152442 75%, #1C335C 100%);
}
/* باران در شب: آسمان تیره شبانه با نور ملایم سرمه‌ای (بدون خورشید!) */
.apple-sky-bg.sky-night.sky-rain,
.apple-sky-bg.sky-night.sky-storm {
  background: linear-gradient(180deg, #060A14 0%, #0E1624 45%, #162235 78%, #1F2F46 100%);
}
/* باران در روز: آسمان ابری ملایم و نقره‌ای */
.apple-sky-bg.sky-day.sky-rain {
  background: linear-gradient(180deg, #1E293B 0%, #334155 45%, #475569 75%, #64748B 100%);
}
/* غروب درخشان اپل */
.apple-sky-bg.sky-sunset {
  background: linear-gradient(180deg, #2D1452 0%, #681C7A 28%, #A8245D 56%, #E0542E 82%, #F69D3C 100%);
}
/* طلوع لطیف */
.apple-sky-bg.sky-sunrise {
  background: linear-gradient(180deg, #1E1B4B 0%, #4C1D95 32%, #9D174D 60%, #F97316 84%, #FDE047 100%);
}
/* برف */
.apple-sky-bg.sky-snow {
  background: linear-gradient(180deg, #091124 0%, #132240 45%, #1E365E 78%, #2A4C80 100%);
}
/* طوفان */
.apple-sky-bg.sky-storm {
  background: linear-gradient(180deg, #060812 0%, #111526 40%, #1C1942 75%, #2B285E 100%);
}
/* ابری */
.apple-sky-bg.sky-cloudy {
  background: linear-gradient(180deg, #1E293B 0%, #334155 45%, #475569 75%, #64748B 100%);
}
/* باد */
.apple-sky-bg.sky-wind {
  background: linear-gradient(180deg, #155E75 0%, #0284C7 45%, #38BDF8 75%, #BAE6FD 100%);
}

.apple-sky-haze {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 65px;
  background: linear-gradient(to top, rgba(255,255,255,0.06) 0%, transparent 100%);
  z-index: 2;
  pointer-events: none;
}

/* اجسام فلکی اپل (Sun & Moon) */
.apple-celestial {
  position: absolute;
  top: 18px;
  left: 22px;
  z-index: 2;
  pointer-events: none;
}

/* خورشید ملایم و شیک اپل */
.apple-sun {
  position: relative;
  width: 52px;
  height: 52px;
}
.apple-sun-core {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 40%, #FFFFFF 0%, #FEF08A 35%, #FBBF24 70%, #F59E0B 100%);
  box-shadow:
    0 0 20px rgba(254, 240, 138, 0.9),
    0 0 50px rgba(245, 158, 11, 0.45),
    0 0 80px rgba(245, 158, 11, 0.25);
  animation: appleSunPulse 5s ease-in-out infinite;
}
.apple-sun-halo {
  position: absolute;
  inset: -15px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(254, 240, 138, 0.28) 0%, rgba(245, 158, 11, 0.1) 50%, transparent 75%);
}

/* ماه شیک اپل */
.apple-moon {
  position: relative;
  width: 48px;
  height: 48px;
}
.apple-moon-body {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #FFFFFF 0%, #E2E8F0 35%, #CBD5E1 65%, #94A3B8 100%);
  box-shadow:
    0 0 20px rgba(255, 255, 255, 0.75),
    0 0 50px rgba(186, 230, 253, 0.3);
  animation: appleMoonFloat 6s ease-in-out infinite;
}
.apple-moon-body::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background:
    radial-gradient(circle at 28% 28%, rgba(100,116,139,0.3) 0%, transparent 20%),
    radial-gradient(circle at 55% 42%, rgba(100,116,139,0.25) 0%, transparent 16%),
    radial-gradient(circle at 40% 68%, rgba(71,85,105,0.35) 0%, transparent 24%);
}
.apple-moon-glow {
  position: absolute;
  inset: -14px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(226, 232, 240, 0.18) 0%, transparent 75%);
}

/* هاله ملایم باران در شب (بدون خورشید!) */
.apple-moon-haze-rain {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(148, 163, 184, 0.16) 0%, transparent 70%);
  margin-top: 5px;
}
.apple-sun-haze-rain {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.18) 0%, transparent 70%);
}
.apple-sunset-sun {
  width: 56px;
  height: 56px;
  margin-top: 20px;
  border-radius: 50%;
  background: radial-gradient(circle at 45% 45%, #FEF08A 0%, #F97316 50%, #DC2626 90%);
  box-shadow: 0 0 30px #F97316, 0 0 70px rgba(234, 88, 12, 0.5);
}

/* ============================================================
   ابرهای کوچک، بسیار شیک، ظریف و ارگانیک اپل (Small Apple Clouds)
   ============================================================ */
.apple-clouds-container {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
}

.apple-cloud {
  position: absolute;
  border-radius: 999px;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.16));
}
.apple-cloud::before,
.apple-cloud::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: inherit;
}

/* ابر ۱: کوچک و ظریف */
.apple-cloud.ac-1 {
  width: 84px;
  height: 26px;
  top: 20px;
  right: 25px;
  animation: appleCloudDrift1 45s linear infinite;
  opacity: 0.9;
}
.apple-cloud.ac-1::before {
  width: 36px; height: 36px; top: -16px; left: 14px;
}
.apple-cloud.ac-1::after {
  width: 28px; height: 28px; top: -12px; left: 42px;
}

/* ابر ۲: متوسط و پفکی */
.apple-cloud.ac-2 {
  width: 98px;
  height: 28px;
  top: 50px;
  left: 20px;
  animation: appleCloudDrift2 55s linear infinite;
  opacity: 0.82;
}
.apple-cloud.ac-2::before {
  width: 40px; height: 40px; top: -18px; left: 18px;
}
.apple-cloud.ac-2::after {
  width: 32px; height: 32px; top: -14px; left: 50px;
}

/* ابر ۳: کوچک و سبک */
.apple-cloud.ac-3 {
  width: 70px;
  height: 22px;
  top: 15px;
  left: 45%;
  animation: appleCloudDrift3 60s linear infinite;
  opacity: 0.72;
}
.apple-cloud.ac-3::before {
  width: 28px; height: 28px; top: -13px; left: 12px;
}
.apple-cloud.ac-3::after {
  width: 22px; height: 22px; top: -9px; left: 34px;
}

/* ابر سبک در دوردست روز آفتابی */
.apple-cloud.ac-distant {
  width: 65px;
  height: 20px;
  top: 36px;
  right: 30px;
  animation: appleCloudDrift1 50s linear infinite;
  opacity: 0.55;
}
.apple-cloud.ac-distant::before {
  width: 26px; height: 26px; top: -12px; left: 10px;
}

/* استایل‌های رنگی ابر بر اساس شب/روز/باران */
.apple-cloud.day-cloud {
  background: rgba(255, 255, 255, 0.88);
  box-shadow: inset 0 2px 4px rgba(255,255,255,0.95);
}
.apple-cloud.night-cloud {
  background: rgba(148, 163, 184, 0.45);
  box-shadow: inset 0 1px 3px rgba(255,255,255,0.35);
}
.apple-cloud.night-rain-cloud {
  background: rgba(26, 36, 52, 0.85);
  box-shadow: inset 0 1px 3px rgba(255,255,255,0.15);
}
.apple-cloud.day-rain-cloud {
  background: rgba(71, 85, 105, 0.82);
  box-shadow: inset 0 2px 4px rgba(255,255,255,0.25);
}

/* کانواس رندر باران سوزنی و پدیده‌ها */
.apple-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 4;
  pointer-events: none;
}

.apple-lightning-flash {
  position: absolute;
  inset: 0;
  background: rgba(224, 242, 254, 0.9);
  z-index: 5;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.04s ease;
}

/* ============================================================
   لایه اطلاعات شیشه‌ای اپل ودر (Apple Weather HUD)
   ============================================================ */
.apple-hud {
  position: absolute;
  inset: 0;
  z-index: 6;
  padding: 14px 18px 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  direction: rtl;
  pointer-events: none;
}

.apple-hud-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.apple-city-badge {
  display: flex;
  align-items: center;
  gap: 6px;
}
.apple-radar-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 8px #10B981;
  animation: heroDotPulse 2s infinite;
}
.apple-city-name {
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.2px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.4);
}
.apple-time-pill {
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.28);
  border: 1px solid rgba(255, 255, 255, 0.16);
  font-size: 10.5px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.apple-hud-center {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: -6px;
}
.apple-temp-row {
  display: flex;
  align-items: baseline;
  line-height: 0.95;
}
.apple-temp-val {
  font-size: 52px;
  font-weight: 300;
  color: #ffffff;
  letter-spacing: -2px;
  text-shadow: 0 4px 18px rgba(0,0,0,0.35);
}
.apple-temp-deg {
  font-size: 32px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.8);
  margin-right: 2px;
}
.apple-condition-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin-top: 4px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.35);
}
.apple-hilo-text {
  font-size: 11.5px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.72);
  margin-top: 2px;
}

/* کپسول شیشه‌ای یکپارچه پایین کادر مشابه اپل ودر */
.apple-hud-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.32);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.14);
  box-shadow: 0 4px 16px rgba(0,0,0,0.25);
  pointer-events: auto;
}
.apple-bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  flex: 1;
}
.apple-bar-label {
  font-size: 9.5px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.65);
}
.apple-bar-val {
  font-size: 11.5px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.2px;
}
.apple-bar-divider {
  width: 1px;
  height: 20px;
  background: rgba(255, 255, 255, 0.14);
}

/* انیمیشن‌های ملایم اپل */
@keyframes appleSunPulse {
  0%, 100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.03); filter: brightness(1.08); }
}
@keyframes appleMoonFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}
@keyframes appleCloudDrift1 {
  0% { transform: translateX(180px); }
  100% { transform: translateX(-360px); }
}
@keyframes appleCloudDrift2 {
  0% { transform: translateX(210px); }
  100% { transform: translateX(-390px); }
}
@keyframes appleCloudDrift3 {
  0% { transform: translateX(160px); }
  100% { transform: translateX(-340px); }
}
"""

pattern = r'/\* ============================================================\s*سیستم استایل آب‌وهوای اتمسفریک.*?$'
match = re.search(pattern, css, flags=re.DOTALL)
if match:
    css = css[:match.start()] + apple_css
    print("   -> Replaced with Apple Weather styles!")
else:
    css += "\n" + apple_css
    print("   -> Appended Apple Weather styles!")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("   -> style.css successfully updated with Apple Weather design!")
