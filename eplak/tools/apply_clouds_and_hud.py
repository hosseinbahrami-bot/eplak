import re

print("--- [1] Updating modules/weather-3d.js with 4-5 organic clouds and robust HUD data binding ---")

with open('/home/user/eplak/eplak-fixed/modules/weather-3d.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace getOrganicCloudsHtml with 4-5 distinct, gorgeous, organic soft clouds
new_clouds_func = """  /* ────────── ساخت ۴ الی ۵ ابر ارگانیک، بسیار زیبا، محو و طبیعی ────────── */
  function getOrganicCloudsHtml(isDay, isRain) {
    var cloudGrad = isDay
      ? '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(255,255,255,0.92)"/><stop offset="55%" stop-color="rgba(240,248,255,0.76)"/><stop offset="85%" stop-color="rgba(215,230,250,0.32)"/><stop offset="100%" stop-color="rgba(200,220,245,0)"/></radialGradient>'
      : '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(175,198,230,0.70)"/><stop offset="55%" stop-color="rgba(120,148,188,0.48)"/><stop offset="85%" stop-color="rgba(75,100,140,0.22)"/><stop offset="100%" stop-color="rgba(50,75,115,0)"/></radialGradient>';

    if (isRain) {
      cloudGrad = isDay
        ? '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(130,145,170,0.88)"/><stop offset="60%" stop-color="rgba(95,110,135,0.68)"/><stop offset="100%" stop-color="rgba(70,85,110,0)"/></radialGradient>'
        : '<radialGradient id="acG1" cx="45%" cy="30%" r="65%"><stop offset="0%" stop-color="rgba(45,60,85,0.90)"/><stop offset="60%" stop-color="rgba(28,40,62,0.72)"/><stop offset="100%" stop-color="rgba(15,25,45,0)"/></radialGradient>';
    }

    var defs = '<defs>' + cloudGrad + '<filter id="cloudSoftBlur" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="3.8"/></filter></defs>';

    // ابر ۱: ابر اصلی پفکی در بالا-راست
    var svg1 = ''
      + '<svg class="apple-cloud-organic ac-org-1" viewBox="0 0 240 85" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="65" cy="52" rx="46" ry="22" fill="url(#acG1)"/>'
      +     '<ellipse cx="120" cy="42" rx="56" ry="28" fill="url(#acG1)"/>'
      +     '<ellipse cx="170" cy="50" rx="44" ry="20" fill="url(#acG1)"/>'
      +     '<ellipse cx="94" cy="32" rx="36" ry="22" fill="url(#acG1)"/>'
      +     '<ellipse cx="142" cy="34" rx="38" ry="22" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    // ابر ۲: ابر متوسط و کشیده در مرکز-چپ
    var svg2 = ''
      + '<svg class="apple-cloud-organic ac-org-2" viewBox="0 0 200 75" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="55" cy="46" rx="40" ry="20" fill="url(#acG1)"/>'
      +     '<ellipse cx="102" cy="38" rx="48" ry="25" fill="url(#acG1)"/>'
      +     '<ellipse cx="148" cy="44" rx="38" ry="18" fill="url(#acG1)"/>'
      +     '<ellipse cx="80" cy="28" rx="30" ry="19" fill="url(#acG1)"/>'
      +     '<ellipse cx="122" cy="30" rx="32" ry="19" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    // ابر ۳: ابر سبک و ملایم در بالای مرکز
    var svg3 = ''
      + '<svg class="apple-cloud-organic ac-org-3" viewBox="0 0 170 65" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="45" cy="40" rx="34" ry="17" fill="url(#acG1)"/>'
      +     '<ellipse cx="88" cy="32" rx="42" ry="22" fill="url(#acG1)"/>'
      +     '<ellipse cx="128" cy="38" rx="32" ry="16" fill="url(#acG1)"/>'
      +     '<ellipse cx="70" cy="24" rx="26" ry="16" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    // ابر ۴: ابر ظریف و کوچک در بخش پایین‌تر
    var svg4 = ''
      + '<svg class="apple-cloud-organic ac-org-4" viewBox="0 0 150 60" fill="none" xmlns="http://www.w3.org/2000/svg">'
      +   defs
      +   '<g filter="url(#cloudSoftBlur)">'
      +     '<ellipse cx="40" cy="36" rx="30" ry="16" fill="url(#acG1)"/>'
      +     '<ellipse cx="78" cy="28" rx="36" ry="20" fill="url(#acG1)"/>'
      +     '<ellipse cx="112" cy="34" rx="28" ry="15" fill="url(#acG1)"/>'
      +   '</g>'
      + '</svg>';

    return svg1 + svg2 + svg3 + svg4;
  }"""

js = re.sub(
    r'/\* ────────── ساخت ابرهای فوق‌العاده زیبا.*?return svg1 \+ svg2;\s*\}',
    new_clouds_func,
    js,
    flags=re.DOTALL
)

with open('/home/user/eplak/eplak-fixed/modules/weather-3d.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("   -> modules/weather-3d.js updated with 4 organic clouds!")


print("--- [2] Updating assets/css/style.css to ensure HUD and all 4 clouds are 100% styled & visible ---")

with open('/home/user/eplak/eplak-fixed/assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace from /* ============================================================ ابرهای ارگانیک to end of file with full HUD and clouds
clean_end_pattern = r'/\* ============================================================\s*ابرهای ارگانیک.*?$'

complete_clouds_and_hud_css = """/* ============================================================
   ابرهای ارگانیک، محو، بسیار شیک و طبیعی اپل (Organic Soft-Edge Clouds)
   ============================================================ */
.apple-clouds-container {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
  overflow: hidden;
}

.apple-cloud-organic {
  position: absolute;
  pointer-events: none;
  will-change: transform;
}

/* ابر ۱: پفکی و بزرگ در بالا-راست */
.apple-cloud-organic.ac-org-1 {
  width: 145px;
  height: 52px;
  top: 10px;
  right: -30px;
  animation: appleCloudFloat1 48s linear infinite;
  opacity: 0.92;
}

/* ابر ۲: متوسط و کشیده در مرکز-چپ */
.apple-cloud-organic.ac-org-2 {
  width: 125px;
  height: 46px;
  top: 40px;
  left: -25px;
  animation: appleCloudFloat2 62s linear infinite;
  opacity: 0.85;
}

/* ابر ۳: نرم و آرام در بالای مرکز */
.apple-cloud-organic.ac-org-3 {
  width: 110px;
  height: 40px;
  top: 18px;
  left: 32%;
  animation: appleCloudFloat3 56s linear infinite;
  opacity: 0.78;
}

/* ابر ۴: ظریف و شناور در لایه میانی */
.apple-cloud-organic.ac-org-4 {
  width: 95px;
  height: 36px;
  top: 60px;
  right: 15%;
  animation: appleCloudFloat4 70s linear infinite;
  opacity: 0.72;
}

@keyframes appleCloudFloat1 {
  0% { transform: translateX(180px); }
  100% { transform: translateX(-370px); }
}
@keyframes appleCloudFloat2 {
  0% { transform: translateX(200px); }
  100% { transform: translateX(-350px); }
}
@keyframes appleCloudFloat3 {
  0% { transform: translateX(150px); }
  100% { transform: translateX(-320px); }
}
@keyframes appleCloudFloat4 {
  0% { transform: translateX(170px); }
  100% { transform: translateX(-340px); }
}

/* ============================================================
   لایه اطلاعات آنلاین و شیشه‌ای اپل ودر (Apple Weather HUD)
   کاملاً پرنور، خوانا، زیبا و در بالاترین لایه (z-index: 10)
   ============================================================ */
.apple-hud {
  position: absolute;
  inset: 0;
  z-index: 10;
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
  pointer-events: auto;
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
  text-shadow: 0 1px 6px rgba(0,0,0,0.5);
}
.apple-time-pill {
  padding: 3px 11px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 10.5px;
  font-weight: 600;
  color: #F8FAFC;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  text-shadow: 0 1px 3px rgba(0,0,0,0.4);
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
  text-shadow: 0 4px 18px rgba(0,0,0,0.45);
}
.apple-temp-deg {
  font-size: 32px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.85);
  margin-right: 2px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.apple-condition-title {
  font-size: 14.5px;
  font-weight: 600;
  color: #ffffff;
  margin-top: 4px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.45);
}
.apple-hilo-text {
  font-size: 11.5px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

/* کپسول شیشه‌ای یکپارچه پایین کادر مشابه اپل ودر */
.apple-hud-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.38);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.16);
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
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
  color: rgba(255, 255, 255, 0.72);
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
  background: rgba(255, 255, 255, 0.16);
}
"""

match = re.search(clean_end_pattern, css, flags=re.DOTALL)
if match:
    css = css[:match.start()] + complete_clouds_and_hud_css
else:
    css += "\n" + complete_clouds_and_hud_css

with open('/home/user/eplak/eplak-fixed/assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("   -> style.css successfully updated with complete Apple HUD styles!")

