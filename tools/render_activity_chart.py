import base64
import subprocess
import os

def b64(p):
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

font_bold = b64("/home/user/eplak/eplak-fixed/admin/assets/fonts/YekanBakh-Bold.woff2")
font_heavy = b64("/home/user/eplak/eplak-fixed/admin/assets/fonts/YekanBakh-Heavy.woff2")
font_regular = b64("/home/user/eplak/eplak-fixed/admin/assets/fonts/YekanBakh-Regular.woff2")
logo = b64("/home/user/eplak/eplak-fixed/assets/img/logo.png")

# SVG Icons
icon_finance = '''<svg viewBox="0 0 24 24" fill="none" stroke="#c084fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="34" height="34"><rect x="2" y="5" width="20" height="14" rx="3"/><line x1="2" y1="10" x2="22" y2="10"/><circle cx="6" cy="15" r="1.5" fill="#c084fc"/><circle cx="10" cy="15" r="1.5" fill="#c084fc"/></svg>'''
icon_biz = '''<svg viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="34" height="34"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/><path d="M2 9h20"/></svg>'''
icon_env = '''<svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="34" height="34"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.2a1.8 1.8 0 0 0 1.57-.88 1.8 1.8 0 0 0 .004-1.78L17 10"/><path d="M12 2l4.8 8.4a1.8 1.8 0 0 1 0 1.76 1.8 1.8 0 0 1-1.56.88H8.76a1.8 1.8 0 0 1-1.56-.88 1.8 1.8 0 0 1 0-1.76L12 2z"/></svg>'''
icon_transport = '''<svg viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="34" height="34"><rect x="4" y="3" width="16" height="15" rx="3"/><line x1="4" y1="11" x2="20" y2="11"/><circle cx="8" cy="15" r="1.5" fill="#60a5fa"/><circle cx="16" cy="15" r="1.5" fill="#60a5fa"/><path d="M7 18l-3 3M17 18l3 3M9 3v-1M15 3v-1"/></svg>'''
icon_tenders = '''<svg viewBox="0 0 24 24" fill="none" stroke="#fb7185" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="34" height="34"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>'''
icon_cem = '''<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="34" height="34"><path d="M12 2C8 2 4 6 4 10c0 5 8 12 8 12s8-7 8-12c0-4-4-8-8-8z"/><circle cx="12" cy="9" r="3" fill="#38bdf8"/><path d="M12 7v4M10 9h4"/></svg>'''

icon_137 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#00c9a7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="32" height="32"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>'''
icon_radar = '''<svg viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="32" height="32"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2" fill="#60a5fa"/><line x1="12" y1="2" x2="12" y2="12"/></svg>'''

icon_wind = '''<svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="26" height="26"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>'''
icon_sun = '''<svg viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="26" height="26"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'''
icon_mosque = '''<svg viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="26" height="26"><path d="M3 21h18M5 21V9l7-6 7 6v12M9 21v-6a3 3 0 0 1 6 0v6"/></svg>'''
icon_news = '''<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="26" height="26"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8V6Z"/></svg>'''

html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>چارت ساختار فعالیت‌های ای‌پلاک</title>
<style>
@font-face {{
  font-family: 'YekanBakh';
  src: url('data:font/woff2;base64,{font_regular}') format('woff2');
  font-weight: 400;
  font-style: normal;
}}
@font-face {{
  font-family: 'YekanBakh';
  src: url('data:font/woff2;base64,{font_bold}') format('woff2');
  font-weight: 700;
  font-style: normal;
}}
@font-face {{
  font-family: 'YekanBakh';
  src: url('data:font/woff2;base64,{font_heavy}') format('woff2');
  font-weight: 900;
  font-style: normal;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  width: 2400px;
  height: 1560px;
  background-color: #070c16;
  background-image:
    radial-gradient(circle at 50% 0%, rgba(0, 201, 167, 0.18) 0%, transparent 48%),
    radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.16) 0%, transparent 42%),
    radial-gradient(circle at 90% 20%, rgba(245, 158, 11, 0.16) 0%, transparent 42%),
    radial-gradient(circle at 50% 100%, rgba(59, 130, 246, 0.18) 0%, transparent 52%),
    radial-gradient(rgba(255, 255, 255, 0.055) 1.2px, transparent 1.2px);
  background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 30px 30px;
  font-family: 'YekanBakh', system-ui, -apple-system, sans-serif;
  color: #ffffff;
  padding: 42px 50px 32px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}}

/* Header */
.header-wrapper {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  position: relative;
}}
.header-wrapper::after {{
  content: '';
  position: absolute;
  bottom: -1px;
  right: 10%;
  left: 10%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00c9a7, #3b82f6, #a855f7, transparent);
  box-shadow: 0 0 15px rgba(0, 201, 167, 0.5);
}}

.brand-section {{
  display: flex;
  align-items: center;
  gap: 24px;
}}
.logo-container {{
  width: 105px;
  height: 105px;
  background: rgba(255, 255, 255, 0.05);
  border: 1.5px solid rgba(0, 201, 167, 0.4);
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 40px rgba(0, 201, 167, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(15px);
}}
.logo-container img {{
  width: 82px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.6));
}}
.title-block h1 {{
  font-size: 38px;
  font-weight: 900;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #ffffff 40%, #00c9a7 90%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: flex;
  align-items: center;
  gap: 16px;
}}
.title-block h1 .badge-ver {{
  font-size: 15px;
  font-weight: 700;
  padding: 5px 16px;
  border-radius: 22px;
  background: rgba(0, 201, 167, 0.16);
  color: #00c9a7;
  border: 1px solid rgba(0, 201, 167, 0.35);
  -webkit-text-fill-color: #00c9a7;
}}
.title-block p {{
  font-size: 19px;
  color: #94a3b8;
  margin-top: 6px;
  font-weight: 400;
}}

.kpi-pills {{
  display: flex;
  gap: 16px;
}}
.kpi-pill {{
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 12px 22px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}}
.kpi-num {{
  font-size: 32px;
  font-weight: 900;
  color: #00c9a7;
  line-height: 1;
}}
.kpi-text {{
  font-size: 13.5px;
  line-height: 1.4;
  color: #cbd5e1;
}}
.kpi-text strong {{
  display: block;
  font-size: 15px;
  color: #fff;
}}

/* Main Grid - 6 Key Spheres */
.grid-container {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin: 22px 0 20px;
}}

.sector-card {{
  background: rgba(13, 20, 36, 0.85);
  backdrop-filter: blur(30px);
  border-radius: 26px;
  padding: 22px 24px 18px;
  border: 1.5px solid var(--border-color);
  position: relative;
  overflow: hidden;
  box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.sector-card::before {{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 170px;
  height: 170px;
  background: radial-gradient(circle at top right, var(--accent-glow), transparent 70%);
  pointer-events: none;
}}

.sector-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  position: relative;
  z-index: 2;
}}
.sector-title-wrap {{
  display: flex;
  align-items: center;
  gap: 16px;
}}
.sector-icon-box {{
  width: 66px;
  height: 66px;
  border-radius: 20px;
  background: var(--icon-bg);
  border: 1.5px solid var(--icon-border);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px -4px var(--accent-glow);
  flex-shrink: 0;
}}
.sector-title-wrap h2 {{
  font-size: 25px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.25;
}}
.sector-title-wrap .sector-en {{
  font-size: 13px;
  color: var(--accent-color);
  font-weight: 700;
  letter-spacing: 0.6px;
}}

.sector-badge {{
  font-size: 13.5px;
  font-weight: 800;
  padding: 6px 15px;
  border-radius: 16px;
  background: var(--badge-bg);
  color: var(--accent-color);
  border: 1px solid var(--badge-border);
  white-space: nowrap;
}}

.services-list {{
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  z-index: 2;
}}
.service-item {{
  background: rgba(255, 255, 255, 0.045);
  border: 1px solid rgba(255, 255, 255, 0.085);
  border-radius: 15px;
  padding: 9px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
}}
.service-bullet {{
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent-color);
  box-shadow: 0 0 10px var(--accent-color);
  flex-shrink: 0;
}}
.service-info {{
  flex: 1;
}}
.service-title {{
  font-size: 17.5px;
  font-weight: 800;
  color: #ffffff;
}}
.service-sub {{
  font-size: 13.5px;
  color: #94a3b8;
  margin-top: 2px;
  line-height: 1.4;
}}

.sector-metric {{
  margin-top: 13px;
  padding: 10px 16px;
  border-radius: 14px;
  background: rgba(var(--rgb), 0.1);
  border: 1px dashed rgba(var(--rgb), 0.35);
  font-size: 14px;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}
.sector-metric strong {{
  color: var(--accent-color);
  font-weight: 800;
}}

/* Thematic Colors */
.card-finance {{
  --rgb: 168, 85, 247;
  --accent-color: #c084fc;
  --border-color: rgba(168, 85, 247, 0.4);
  --accent-glow: rgba(168, 85, 247, 0.35);
  --icon-bg: rgba(168, 85, 247, 0.16);
  --icon-border: rgba(168, 85, 247, 0.45);
  --badge-bg: rgba(168, 85, 247, 0.14);
  --badge-border: rgba(168, 85, 247, 0.3);
}}
.card-business {{
  --rgb: 245, 158, 11;
  --accent-color: #fbbf24;
  --border-color: rgba(245, 158, 11, 0.4);
  --accent-glow: rgba(245, 158, 11, 0.35);
  --icon-bg: rgba(245, 158, 11, 0.16);
  --icon-border: rgba(245, 158, 11, 0.45);
  --badge-bg: rgba(245, 158, 11, 0.14);
  --badge-border: rgba(245, 158, 11, 0.3);
}}
.card-environment {{
  --rgb: 16, 185, 129;
  --accent-color: #34d399;
  --border-color: rgba(16, 185, 129, 0.4);
  --accent-glow: rgba(16, 185, 129, 0.35);
  --icon-bg: rgba(16, 185, 129, 0.16);
  --icon-border: rgba(16, 185, 129, 0.45);
  --badge-bg: rgba(16, 185, 129, 0.14);
  --badge-border: rgba(16, 185, 129, 0.3);
}}
.card-transport {{
  --rgb: 59, 130, 246;
  --accent-color: #60a5fa;
  --border-color: rgba(59, 130, 246, 0.4);
  --accent-glow: rgba(59, 130, 246, 0.35);
  --icon-bg: rgba(59, 130, 246, 0.16);
  --icon-border: rgba(59, 130, 246, 0.45);
  --badge-bg: rgba(59, 130, 246, 0.14);
  --badge-border: rgba(59, 130, 246, 0.3);
}}
.card-tenders {{
  --rgb: 239, 68, 68;
  --accent-color: #fb7185;
  --border-color: rgba(239, 68, 68, 0.4);
  --accent-glow: rgba(239, 68, 68, 0.35);
  --icon-bg: rgba(239, 68, 68, 0.16);
  --icon-border: rgba(239, 68, 68, 0.45);
  --badge-bg: rgba(239, 68, 68, 0.14);
  --badge-border: rgba(239, 68, 68, 0.3);
}}
.card-cemeteries {{
  --rgb: 14, 165, 233;
  --accent-color: #38bdf8;
  --border-color: rgba(14, 165, 233, 0.4);
  --accent-glow: rgba(14, 165, 233, 0.35);
  --icon-bg: rgba(14, 165, 233, 0.16);
  --icon-border: rgba(14, 165, 233, 0.45);
  --badge-bg: rgba(14, 165, 233, 0.14);
  --badge-border: rgba(14, 165, 233, 0.3);
}}

/* Bottom Infrastructure Modules */
.infra-container {{
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 24px;
}}
.infra-card {{
  background: rgba(15, 23, 42, 0.75);
  border: 1.5px solid rgba(255, 255, 255, 0.14);
  border-radius: 24px;
  padding: 20px 26px;
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.infra-head {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}}
.infra-head-left {{
  display: flex;
  align-items: center;
  gap: 14px;
}}
.infra-head-left h3 {{
  font-size: 20px;
  font-weight: 800;
  color: #fff;
}}
.infra-head-left span {{
  font-size: 13px;
  color: #00c9a7;
}}

.flow-steps {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}}
.flow-step {{
  background: rgba(255, 255, 255, 0.045);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 12px 10px;
  text-align: center;
  position: relative;
}}
.flow-step-num {{
  font-size: 12px;
  font-weight: 800;
  color: #00c9a7;
  margin-bottom: 4px;
}}
.flow-step-title {{
  font-size: 14.5px;
  font-weight: 800;
  color: #f8fafc;
}}
.flow-step-desc {{
  font-size: 11.5px;
  color: #94a3b8;
  margin-top: 3px;
}}

.city-live-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.live-tile {{
  background: rgba(255, 255, 255, 0.045);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 12px 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}}
.live-tile-name {{
  font-size: 13px;
  font-weight: 700;
  color: #e2e8f0;
  margin-top: 4px;
}}
.live-tile-val {{
  font-size: 11.5px;
  color: #00c9a7;
  font-weight: 700;
  margin-top: 2px;
}}

/* Bottom Strip */
.footer-strip {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  color: #94a3b8;
}}
.footer-strip .specs {{
  display: flex;
  gap: 22px;
}}
.footer-strip .spec-item {{
  display: flex;
  align-items: center;
  gap: 8px;
  color: #cbd5e1;
}}
.footer-strip .spec-dot {{
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00c9a7;
  box-shadow: 0 0 8px #00c9a7;
}}
</style>
</head>
<body>

  <!-- 1. Header -->
  <header class="header-wrapper">
    <div class="brand-section">
      <div class="logo-container">
        <img src="data:image/png;base64,{logo}" alt="ای‌پلاک">
      </div>
      <div class="title-block">
        <h1>
          <span>چارت ساختار و قلمرو فعالیت‌های سوپر‌اپلیکیشن ای‌پلاک</span>
          <span class="badge-ver">جامع، برخط و دوزبانه</span>
        </h1>
        <p>سامانه یکپارچه مدیریت شهری، خدمات هوشمند و مشارکت مردمی شهرداری ورامین • E-Pelak Smart City Platform</p>
      </div>
    </div>
    <div class="kpi-pills">
      <div class="kpi-pill">
        <span class="kpi-num">۶</span>
        <div class="kpi-text"><strong>حوزه کلان خدمات</strong>طبقه‌بندی تخصصی شهری</div>
      </div>
      <div class="kpi-pill">
        <span class="kpi-num">۲۸</span>
        <div class="kpi-text"><strong>خدمت برخط فعال</strong>بدون نیاز به مراجعه حضوری</div>
      </div>
      <div class="kpi-pill">
        <span class="kpi-num">۱۳۷</span>
        <div class="kpi-text"><strong>سامانه ارتباط مردمی</strong>نظارت مستقیم شهروندان</div>
      </div>
    </div>
  </header>

  <!-- 2. Grid of 6 Core Functional Areas -->
  <main class="grid-container">

    <!-- 1. عوارض شهرداری -->
    <div class="sector-card card-finance">
      <div class="sector-header">
        <div class="sector-title-wrap">
          <div class="sector-icon-box">{icon_finance}</div>
          <div>
            <h2>عوارض و درآمدهای پایدار</h2>
            <div class="sector-en">MUNICIPAL TAXES & CLEARANCES</div>
          </div>
        </div>
        <span class="sector-badge">۵ خدمت تخصصی</span>
      </div>
      <div class="services-list">
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">عوارض نوسازی و عمران شهری</div>
            <div class="service-sub">استعلام با کد ۱۲ رقمی نوسازی ملک مسکونی و تجاری و تسویه شتابی</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">بهای خدمات مدیریت پسماند</div>
            <div class="service-sub">محاسبه سالیانه بهای پاکیزگی معابر بر مبنای کاربری و مصوبه شورا</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">عوارض کسب، پیشه و تابلوها</div>
            <div class="service-sub">تسویه سالانه واحدهای صنفی و تابلوهای تبلیغاتی سردر مغازه‌ها</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">عوارض سالیانه خودرو و موتورسیکلت</div>
            <div class="service-sub">اتصال کشوری به سامانه سمیع با کد VIN جهت تعویض پلاک و معاینه</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">مفاصاحساب و عدم بدهی دیجیتال</div>
            <div class="service-sub">صدور آنی گواهی رسمی ممهور به QR کد امنیتی جهت دفاتر اسناد رسمی</div>
          </div>
        </div>
      </div>
      <div class="sector-metric">
        <span>شاخص کلیدی: <strong>تسویه آنی شاپرک</strong></span>
        <span>تخفیف: <strong>۱۰٪ جایزه خوش‌حسابی</strong></span>
      </div>
    </div>

    <!-- 2. کسب و کار و تبلیغات -->
    <div class="sector-card card-business">
      <div class="sector-header">
        <div class="sector-title-wrap">
          <div class="sector-icon-box">{icon_biz}</div>
          <div>
            <h2>کسب‌وکار، اصناف و تبلیغات</h2>
            <div class="sector-en">COMMERCE, ADS & LOCAL MARKET</div>
          </div>
        </div>
        <span class="sector-badge">۴ خدمت تخصصی</span>
      </div>
      <div class="services-list">
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">ویترین دیجیتال اصناف ورامین</div>
            <div class="service-sub">صفحه اختصاصی فروشگاه، منوی محصولات، تخفیف‌ها و مسیریابی دقیق</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">ای‌پلاک ادز (تبلیغات هوشمند محله‌محور)</div>
            <div class="service-sub">نمایش بنرهای تبلیغاتی هدفمند به اهالی مناطق و محلات خاص ورامین</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">پروانه کسب و استعلامات سه‌گانه</div>
            <div class="service-sub">اتصال به درگاه ملی مجوزها جهت تایید ایمنی، آتش‌نشانی و شهرسازی</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">بازارچه محلی و صنایع دستی</div>
            <div class="service-sub">عرضه مستقیم فرش میناخانی ورامین، سفالگری و محصولات ارگانیک دشت</div>
          </div>
        </div>
      </div>
      <div class="sector-metric">
        <span>جامعه هدف: <strong>بیش از ۱۲ هزار کسبه</strong></span>
        <span>مزیت: <strong>رونق اقتصاد محلی و حذف واسطه‌ها</strong></span>
      </div>
    </div>

    <!-- 3. محیط زیست و بازیافت -->
    <div class="sector-card card-environment">
      <div class="sector-header">
        <div class="sector-title-wrap">
          <div class="sector-icon-box">{icon_env}</div>
          <div>
            <h2>محیط‌زیست، بازیافت و پسماند</h2>
            <div class="sector-en">ECO-SYSTEM, RECYCLING & WASTE</div>
          </div>
        </div>
        <span class="sector-badge">۴ خدمت تخصصی</span>
      </div>
      <div class="services-list">
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">جمع‌آوری پسماند خشک درب منزل</div>
            <div class="service-sub">اعزام خودرو به محل، توزین با ترازوی دیجیتال و خرید ضایعات بازیافتی</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">کیف پول سبز شهروندی</div>
            <div class="service-sub">واریز پاداش نقدی و تبدیل امتیاز تفکیک زباله به اعتبار تخفیف عوارض</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">نقشه غرفه‌ها و کانکس‌های بازیافت</div>
            <div class="service-sub">مسیریابی به نزدیک‌ترین ایستگاه و تبادل ضایعات با اقلام بهداشتی و گل</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">گزارش تخلیه نخاله و آلودگی معابر</div>
            <div class="service-sub">ثبت تخلفات زیست‌محیطی با عکس و GPS و اعزام اکیپ پاکسازی مکانیزه</div>
          </div>
        </div>
      </div>
      <div class="sector-metric">
        <span>استاندارد رسیدگی: <strong>حداکثر ۱۲ ساعت</strong></span>
        <span>اثر زیست‌محیطی: <strong>کاهش ۷۰٪ دفن غیربهداشتی</strong></span>
      </div>
    </div>

    <!-- 4. حمل و نقل و ترافیک -->
    <div class="sector-card card-transport">
      <div class="sector-header">
        <div class="sector-title-wrap">
          <div class="sector-icon-box">{icon_transport}</div>
          <div>
            <h2>حمل‌ونقل، ترافیک و تردد هوشمند</h2>
            <div class="sector-en">MOBILITY, TRANSIT & SMART TRAFFIC</div>
          </div>
        </div>
        <span class="sector-badge">۴ خدمت تخصصی</span>
      </div>
      <div class="services-list">
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">پایش لحظه‌ای ناوگان اتوبوس و تاکسی</div>
            <div class="service-sub">ردیابی زنده GPS خودروها روی نقشه شهر و تخمین دقیق زمان رسیدن</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">برنامه قطار حومه‌ای و مترو ورامین - تهران</div>
            <div class="service-sub">جدول حرکت روزانه رفت و برگشت ایستگاه راه‌آهن با هشدار تاخیرها</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">کارت بلیت شهری و شارژ الکترونیک</div>
            <div class="service-sub">افزایش اعتبار کارت اتوبوس با گوشی یا خرید بلیت‌های تک‌سفره بارکدی</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">طرح ترافیک و دوربین‌های پلاک‌خوان</div>
            <div class="service-sub">استعلام تردد در هسته مرکزی ورامین و ثبت سهمیه معافیت اهالی محل</div>
          </div>
        </div>
      </div>
      <div class="sector-metric">
        <span>پوشش ناوگان: <strong>۱۰۰٪ خطوط اتوبوس و تاکسی</strong></span>
        <span>پرداخت: <strong>حذف کامل پول نقد</strong></span>
      </div>
    </div>

    <!-- 5. مناقصات و مزایده‌ها -->
    <div class="sector-card card-tenders">
      <div class="sector-header">
        <div class="sector-title-wrap">
          <div class="sector-icon-box">{icon_tenders}</div>
          <div>
            <h2>مناقصات، مزایده‌ها و شفافیت</h2>
            <div class="sector-en">TENDERS, AUCTIONS & INTEGRITY</div>
          </div>
        </div>
        <span class="sector-badge">۵ خدمت تخصصی</span>
      </div>
      <div class="services-list">
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">مناقصات پروژه‌های عمرانی و آسفالت</div>
            <div class="service-sub">فراخوان بهسازی معابر، جدول‌گذاری، احداث بوستان‌ها و پل‌های تقاطع</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">مزایده‌های املاک، اراضی و غرفه‌ها</div>
            <div class="service-sub">فروش قطعات تفکیکی و اجاره غرفه‌های بازار روز با قیمت پایه کارشناسی</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">استعلام بهای خریدهای تدارکاتی</div>
            <div class="service-sub">ثبت آنلاین پیش‌فاکتور فروشندگان برای تامین قطعات و تجهیزات شهرداری</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">دانلود رایگان اسناد و دفترچه فنی</div>
            <div class="service-sub">دریافت بسته‌های شرایط عمومی پیمان، آنالیز بها و ضوابط HSE در قالب PDF</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">سامانه شفافیت و کارنامه معاملات</div>
            <div class="service-sub">انتشار عمومی مشخصات پیمانکار برنده، مبالغ قرارداد و مهندسین ناظر</div>
          </div>
        </div>
      </div>
      <div class="sector-metric">
        <span>شفافیت: <strong>اتصال به سامانه ستاد ایران</strong></span>
        <span>رویکرد: <strong>اتاق شیشه‌ای و مبارزه با فساد</strong></span>
      </div>
    </div>

    <!-- 6. آرامستان‌ها -->
    <div class="sector-card card-cemeteries">
      <div class="sector-header">
        <div class="sector-title-wrap">
          <div class="sector-icon-box">{icon_cem}</div>
          <div>
            <h2>آرامستان‌ها و خدمات متوفیات</h2>
            <div class="sector-en">HOSSEIN REZA CEMETERY SERVICES</div>
          </div>
        </div>
        <span class="sector-badge">۶ خدمت تخصصی</span>
      </div>
      <div class="services-list">
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">خرید و رزرو آنلاین قبور (حسین‌رضا)</div>
            <div class="service-sub">مشاهده ظرفیت قطعات ۱ تا ۵۰، فاز جدید توسعه و صدور پیش‌سند با کد ملی</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">استعلام تعرفه رسمی مصوب شورای شهر</div>
            <div class="service-sub">اطلاع از هزینه قبور جاری عمومی (رایگان/یارانه‌ای)، طبقات بتنی و غسالخانه</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">جستجوی متوفی و مکان‌یابی مزار</div>
            <div class="service-sub">یافتن قطعه، ردیف و شماره مزار با نام متوفی و مسیریابی قدم‌به‌قدم GPS</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">رزرو مداح، سیستم صوت و مراسم تشییع</div>
            <div class="service-sub">هماهنگی قاریان تاییدشده، اکوپرتابل، سایبان، صندلی و سالن اجتماعات</div>
          </div>
        </div>
        <div class="service-item">
          <span class="service-bullet"></span>
          <div class="service-info">
            <div class="service-title">ثبت گواهی فوت و مجوز دفن الکترونیک</div>
            <div class="service-sub">اتصال به پزشکی قانونی و ثبت‌احوال و اعزام ناوگان حمل متوفیات</div>
          </div>
        </div>
      </div>
      <div class="sector-metric">
        <span>موقعیت آرامستان: <strong>بهشت حسین‌رضا (ع) ورامین</strong></span>
        <span>مزیت: <strong>قطع دست دلالان و شفافیت کامل</strong></span>
      </div>
    </div>

  </main>

  <!-- 3. Bottom Foundation Infrastructure (137 Citizen Reporting & City Live) -->
  <section class="infra-container">
    
    <!-- سامانه ۱۳۷ -->
    <div class="infra-card" style="border-color:rgba(0, 201, 167, 0.4);">
      <div class="infra-head">
        <div class="infra-head-left">
          <span class="icon">{icon_137}</span>
          <div>
            <h3>سامانه مدیریت و ارتباطات مردمی ۱۳۷ ورامین</h3>
            <span>چرخه هوشمند ۵ مرحله‌ای رسیدگی به مطالبات و معضلات شهری</span>
          </div>
        </div>
        <span class="sector-badge" style="background:rgba(0,201,167,0.15); color:#00c9a7; border-color:rgba(0,201,167,0.35);">پاسخگویی ۲۴ ساعته</span>
      </div>
      <div class="flow-steps">
        <div class="flow-step">
          <div class="flow-step-num">گام ۱</div>
          <div class="flow-step-title">ثبت شهروند</div>
          <div class="flow-step-desc">ارسال عکس و موقعیت GPS</div>
        </div>
        <div class="flow-step">
          <div class="flow-step-num">گام ۲</div>
          <div class="flow-step-title">ارزیابی هوشمند</div>
          <div class="flow-step-desc">تفکیک موضوع و فوریت</div>
        </div>
        <div class="flow-step">
          <div class="flow-step-num">گام ۳</div>
          <div class="flow-step-title">ارجاع به واحد</div>
          <div class="flow-step-desc">عمران، خدمات، بازیافت...</div>
        </div>
        <div class="flow-step">
          <div class="flow-step-num">گام ۴</div>
          <div class="flow-step-title">اقدام میدانی</div>
          <div class="flow-step-desc">عملیات اجرایی و رفع نقص</div>
        </div>
        <div class="flow-step">
          <div class="flow-step-num">گام ۵</div>
          <div class="flow-step-title">تایید و سنجش</div>
          <div class="flow-step-desc">نظرسنجی کیفیت از شهروند</div>
        </div>
      </div>
    </div>

    <!-- داشبورد شهر زنده -->
    <div class="infra-card" style="border-color:rgba(59, 130, 246, 0.4);">
      <div class="infra-head">
        <div class="infra-head-left">
          <span class="icon">{icon_radar}</span>
          <div>
            <h3>داشبورد پایش بلادرنگ شهر ورامین (City Live)</h3>
            <span>رصد دائمی داده‌های زیست‌محیطی، اوقات شرعی و اعلانات رسمی</span>
          </div>
        </div>
        <span class="sector-badge" style="background:rgba(59,130,246,0.15); color:#60a5fa; border-color:rgba(59,130,246,0.35);">سنسورهای آنلاین</span>
      </div>
      <div class="city-live-grid">
        <div class="live-tile">
          <div class="live-tile-icon">{icon_wind}</div>
          <div class="live-tile-name">شاخص هوا (AQI)</div>
          <div class="live-tile-val">سنسورهای فعال شهر</div>
        </div>
        <div class="live-tile">
          <div class="live-tile-icon">{icon_sun}</div>
          <div class="live-tile-name">وضعیت جوی</div>
          <div class="live-tile-val">دمای لحظه‌ای دشت</div>
        </div>
        <div class="live-tile">
          <div class="live-tile-icon">{icon_mosque}</div>
          <div class="live-tile-name">اوقات شرعی</div>
          <div class="live-tile-val">افق شرعی ورامین</div>
        </div>
        <div class="live-tile">
          <div class="live-tile-icon">{icon_news}</div>
          <div class="live-tile-name">اخبار و اطلاعیه‌ها</div>
          <div class="live-tile-val">مصوبات رسمی شورا</div>
        </div>
      </div>
    </div>

  </section>

  <!-- 4. Footer Technical Bar -->
  <footer class="footer-strip">
    <div class="specs">
      <div class="spec-item"><span class="spec-dot"></span>امنیت داده‌ها با توکن امنیتی و ورود OTP پیامکی</div>
      <div class="spec-item"><span class="spec-dot"></span>اتصال سراسری به شبکه بانکی شاپرک، سمیع و درگاه ملی مجوزها</div>
      <div class="spec-item"><span class="spec-dot"></span>پشتیبانی دو زبانه کامل (فارسی / English) با تنظیم جهت خودکار LTR/RTL</div>
      <div class="spec-item"><span class="spec-dot"></span>معماری سه‌گانه: Android Native (APK) • iOS Native (Swift/IPA) • Progressive Web App (PWA)</div>
    </div>
    <div>طراحی و توسعه: سامانه یکپارچه مدیریت شهری ای‌پلاک • شهرداری ورامین</div>
  </footer>

</body>
</html>
"""

html_path = "/home/user/eplak/tools/eplak_chart.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

output_png = "/home/user/eplak/eplak_activity_chart.png"
cmd = [
    "/usr/bin/chromium",
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=2400,1560",
    f"--screenshot={output_png}",
    html_path
]

print("Rendering high-res SVG chart...")
subprocess.run(cmd, check=True)
size = os.path.getsize(output_png)
print(f"Chart rendered successfully to {output_png} ({size:,} bytes)")
