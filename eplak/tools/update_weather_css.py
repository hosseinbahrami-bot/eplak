import re

css_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the previous weather 3D styles with the hyper-realistic, fixed-frame styles
weather_section_pattern = r'/\* ============================================================\s*سیستم استایل آب‌وهوای سه‌بعدی.*?$'

new_weather_css = """/* ============================================================
   سیستم استایل آب‌وهوای اتمسفریک و واقع‌گرایانه پیشخوان (Realistic Weather)
   - کادر کاملاً ثابت و بدون چرخش (کادرش ثابت باشه)
   - افکت‌های بصری طبیعی، مدرن و خیره‌کننده (Apple Weather Grade)
   ============================================================ */

.w3d-wrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

/* نوار چیپ‌های کپسولی شیشه‌ای */
.w3d-chips-scroll {
  width: 100%;
  overflow-x: auto;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
  padding: 1px 2px 5px;
}
.w3d-chips-scroll::-webkit-scrollbar {
  display: none;
}
.w3d-chips {
  display: flex;
  gap: 6px;
  width: max-content;
}
.w3d-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 999px;
  border: 1px solid var(--card-border, rgba(255,255,255,0.12));
  background: var(--input-bg, rgba(255,255,255,0.06));
  color: var(--text-secondary, #94A3B8);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
.w3d-chip:hover {
  background: rgba(0, 229, 195, 0.16);
  border-color: rgba(0, 229, 195, 0.45);
  color: #fff;
}
.w3d-chip.active {
  background: var(--teal, #00E5C3);
  border-color: var(--teal, #00E5C3);
  color: #031B19;
  box-shadow: 0 4px 14px rgba(0, 229, 195, 0.35);
}
.w3d-chip-icon {
  font-size: 13px;
  line-height: 1;
}

/* کادر استیج: کاملاً ثابت، بدون چرخش و لرزش (Fixed & Stable Frame) */
.w3d-stage-fixed {
  position: relative;
  width: 100%;
  height: 242px;
  border-radius: 24px;
  overflow: hidden;
  box-shadow:
    0 16px 45px -10px rgba(0,0,0,0.5),
    0 0 0 1px rgba(255,255,255,0.14) inset;
  isolation: isolate;
  user-select: none;
  -webkit-user-select: none;
  transform: none !important; /* تضمین ثبات صددرصدی کادر */
}

/* پس‌زمینه رنگ آسمان اتمسفریک */
.w3d-sky-canvas {
  position: absolute;
  inset: 0;
  z-index: 1;
  transition: background 0.85s ease;
}

/* روز آفتابی طبیعی */
.w3d-sky-canvas.sky-day {
  background: linear-gradient(180deg, #1565C0 0%, #1E88E5 35%, #42A5F5 65%, #90CAF9 100%);
}
/* غروب درخشان */
.w3d-sky-canvas.sky-sunset {
  background: linear-gradient(180deg, #2E1065 0%, #6B21A8 30%, #BE185D 58%, #EA580C 82%, #FBBF24 100%);
}
/* طلوع لطیف */
.w3d-sky-canvas.sky-sunrise {
  background: linear-gradient(180deg, #1E1B4B 0%, #4C1D95 32%, #9D174D 60%, #F97316 84%, #FDE047 100%);
}
/* شب عمیق کهکشانی */
.w3d-sky-canvas.sky-night {
  background: linear-gradient(180deg, #020617 0%, #0B132B 42%, #1C2541 78%, #2B3A67 100%);
}
/* باران جوی */
.w3d-sky-canvas.sky-rain {
  background: linear-gradient(180deg, #0F172A 0%, #1E293B 45%, #334155 75%, #475569 100%);
}
/* برف زمستانی */
.w3d-sky-canvas.sky-snow {
  background: linear-gradient(180deg, #030712 0%, #0F172A 40%, #1E293B 75%, #2B3A55 100%);
}
/* طوفان و آذرخش */
.w3d-sky-canvas.sky-storm {
  background: linear-gradient(180deg, #050811 0%, #0F172A 40%, #1E1B4B 75%, #312E81 100%);
}
/* ابری */
.w3d-sky-canvas.sky-cloudy {
  background: linear-gradient(180deg, #1E293B 0%, #334155 45%, #475569 75%, #64748B 100%);
}
/* وزش باد */
.w3d-sky-canvas.sky-wind {
  background: linear-gradient(180deg, #1A365D 0%, #2B6CB0 45%, #4299E1 75%, #90CDF4 100%);
}

.w3d-horizon-glow {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(to top, rgba(255,255,255,0.08) 0%, transparent 100%);
  z-index: 2;
  pointer-events: none;
}

/* خورشید اتمسفریک و واقعی */
.w3d-celestial-stage {
  position: absolute;
  top: 18px;
  left: 22px;
  z-index: 2;
  pointer-events: none;
}

.w3d-natural-sun {
  position: relative;
  width: 62px;
  height: 62px;
}
.w3d-sun-plasma {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 40%, #FFFFFF 0%, #FFFBEB 25%, #FDE047 55%, #F59E0B 85%, #D97706 100%);
  box-shadow:
    0 0 25px rgba(255, 235, 59, 0.95),
    0 0 65px rgba(245, 158, 11, 0.55),
    0 0 110px rgba(217, 119, 6, 0.35);
  animation: sunGlowPulse 4s ease-in-out infinite;
}
.w3d-sun-corona {
  position: absolute;
  inset: -20px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(254, 240, 138, 0.35) 0%, rgba(245, 158, 11, 0.15) 50%, transparent 75%);
  animation: sunCoronaSpin 32s linear infinite;
}
.w3d-sunbeams {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 140px;
  height: 140px;
  transform: translate(-50%, -50%);
  background: conic-gradient(from 15deg, rgba(255,255,255,0.14) 0deg, transparent 25deg, rgba(255,255,255,0.12) 60deg, transparent 90deg, rgba(255,255,255,0.15) 130deg, transparent 160deg, rgba(255,255,255,0.12) 200deg, transparent 230deg, rgba(255,255,255,0.14) 270deg, transparent 310deg);
  border-radius: 50%;
  animation: sunRaySpin 45s linear infinite;
  filter: blur(2px);
}

/* خورشید غروب */
.w3d-sunset-orb {
  position: relative;
  width: 66px;
  height: 66px;
  margin-top: 25px;
}
.w3d-sunset-core {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 45% 45%, #FEF08A 0%, #F97316 45%, #DC2626 85%, #991B1B 100%);
  box-shadow:
    0 0 35px #F97316,
    0 0 85px rgba(234, 88, 12, 0.65);
}
.w3d-sunset-haze {
  position: absolute;
  inset: -35px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(251, 146, 60, 0.35) 0%, transparent 75%);
}

/* ماه واقعی با بافت دهانه‌ها و هاله نقره‌ای */
.w3d-natural-moon {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 50%;
}
.w3d-moon-texture {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background:
    radial-gradient(circle at 35% 35%, #FFFFFF 0%, #E2E8F0 35%, #CBD5E1 65%, #94A3B8 100%);
  box-shadow:
    0 0 25px rgba(255, 255, 255, 0.75),
    0 0 60px rgba(186, 230, 253, 0.35);
  animation: moonSoftFloat 5s ease-in-out infinite;
}
.w3d-moon-texture::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background:
    radial-gradient(circle at 28% 28%, rgba(100,116,139,0.3) 0%, transparent 22%),
    radial-gradient(circle at 55% 40%, rgba(100,116,139,0.25) 0%, transparent 18%),
    radial-gradient(circle at 38% 68%, rgba(71,85,105,0.35) 0%, transparent 26%),
    radial-gradient(circle at 72% 60%, rgba(71,85,105,0.28) 0%, transparent 20%);
}
.w3d-moon-halo {
  position: absolute;
  inset: -14px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(226, 232, 240, 0.22) 0%, transparent 75%);
}
.w3d-moon-glow-outer {
  position: absolute;
  inset: -30px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(148, 163, 184, 0.15) 0%, transparent 70%);
}

/* ابرهای حجمی طبیعی */
.w3d-cloud-stage {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
}
.w3d-vol-cloud {
  position: absolute;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.82);
  box-shadow:
    0 14px 30px rgba(0,0,0,0.18),
    inset 0 3px 6px rgba(255,255,255,0.95);
  filter: blur(0.5px);
}
.w3d-vol-cloud::before,
.w3d-vol-cloud::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: inherit;
}

.w3d-vol-cloud.cloud-bank-1 {
  width: 155px;
  height: 44px;
  top: 24px;
  right: -30px;
  animation: cloudRealDrift1 32s linear infinite;
  opacity: 0.85;
}
.w3d-vol-cloud.cloud-bank-1::before {
  width: 62px; height: 62px; top: -30px; left: 26px;
}
.w3d-vol-cloud.cloud-bank-1::after {
  width: 48px; height: 48px; top: -20px; left: 74px;
}

.w3d-vol-cloud.cloud-bank-2 {
  width: 185px;
  height: 52px;
  top: 56px;
  left: -40px;
  animation: cloudRealDrift2 42s linear infinite;
  opacity: 0.72;
}
.w3d-vol-cloud.cloud-bank-2::before {
  width: 74px; height: 74px; top: -35px; left: 34px;
}
.w3d-vol-cloud.cloud-bank-2::after {
  width: 58px; height: 58px; top: -24px; left: 92px;
}

.w3d-vol-cloud.cloud-bank-3 {
  width: 125px;
  height: 38px;
  top: 14px;
  left: 36%;
  animation: cloudRealDrift3 48s linear infinite;
  opacity: 0.6;
}
.w3d-vol-cloud.cloud-bank-3::before {
  width: 48px; height: 48px; top: -22px; left: 22px;
}
.w3d-vol-cloud.cloud-bank-3::after {
  width: 38px; height: 38px; top: -16px; left: 60px;
}

.w3d-vol-cloud.cloud-bank-distant {
  width: 110px;
  height: 32px;
  top: 44px;
  right: 25px;
  animation: cloudRealDrift1 38s linear infinite;
  opacity: 0.45;
}
.w3d-vol-cloud.cloud-bank-distant::before {
  width: 42px; height: 42px; top: -20px; left: 18px;
}

/* ابرهای طوفانی باردار */
.w3d-vol-cloud.stormy {
  background: rgba(30, 41, 59, 0.92);
  box-shadow:
    0 16px 40px rgba(0,0,0,0.6),
    inset 0 2px 5px rgba(255,255,255,0.18);
}
/* ابرهای غروب */
.w3d-vol-cloud.sunset-clouds {
  background: rgba(251, 146, 60, 0.75);
  box-shadow:
    0 12px 28px rgba(0,0,0,0.25),
    inset 0 3px 6px rgba(254, 240, 138, 0.8);
}

/* کانواس رندر ذرات جوی */
.w3d-fx-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 4;
  pointer-events: none;
}

/* فلاش صاعقه */
.w3d-ambient-flash {
  position: absolute;
  inset: 0;
  background: rgba(224, 242, 254, 0.92);
  z-index: 5;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.04s ease;
}

/* لایه شیشه‌ای مدرن نمایش وضعیت آب‌وهوا (Apple Weather HUD) */
.w3d-glass-hud {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 6;
  padding: 14px 18px 14px;
  background: linear-gradient(to top, rgba(4, 13, 20, 0.92) 0%, rgba(4, 13, 20, 0.65) 55%, transparent 100%);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  gap: 8px;
  direction: rtl;
}

.w3d-hud-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.w3d-location-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 700;
  color: #6EE7B7;
}
.w3d-radar-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00E5C3;
  box-shadow: 0 0 8px #00E5C3;
  animation: heroDotPulse 2s infinite;
}

.w3d-condition-badge {
  padding: 4px 12px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.18);
  font-size: 11px;
  font-weight: 700;
  color: #F0FDF4;
  letter-spacing: 0.2px;
}

.w3d-hud-center {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.w3d-temp-main {
  display: flex;
  align-items: baseline;
  line-height: 1;
}
.w3d-temp-val {
  font-size: 44px;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -1px;
  text-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.w3d-temp-unit {
  font-size: 24px;
  font-weight: 600;
  color: var(--teal, #00E5C3);
  margin-right: 2px;
}
.w3d-temp-sub {
  font-size: 11.5px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
}

.w3d-hud-pills {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}
.w3d-metric-capsule {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 6px 4px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.w3d-m-icon {
  font-size: 12px;
}
.w3d-m-label {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.65);
}
.w3d-m-val {
  font-size: 11.5px;
  font-weight: 800;
  color: #ffffff;
}

/* انیمیشن‌های روان و چشم‌نواز */
@keyframes sunGlowPulse {
  0%, 100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.04); filter: brightness(1.1); }
}
@keyframes sunCoronaSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
@keyframes sunRaySpin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}
@keyframes moonSoftFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}
@keyframes cloudRealDrift1 {
  0% { transform: translateX(220px); }
  100% { transform: translateX(-400px); }
}
@keyframes cloudRealDrift2 {
  0% { transform: translateX(250px); }
  100% { transform: translateX(-430px); }
}
@keyframes cloudRealDrift3 {
  0% { transform: translateX(190px); }
  100% { transform: translateX(-370px); }
}
"""

match = re.search(weather_section_pattern, css, flags=re.DOTALL)
if match:
    css = css[:match.start()] + new_weather_css
    print("   -> Replaced old weather 3D styles with new hyper-realistic styles!")
else:
    css += "\n" + new_weather_css
    print("   -> Appended new hyper-realistic styles!")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("   -> style.css successfully updated!")
