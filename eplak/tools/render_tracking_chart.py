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
icon_step1 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#00c9a7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="30" height="30"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'''
icon_step2 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="30" height="30"><rect x="3" y="4" width="18" height="16" rx="3"/><line x1="7" y1="8" x2="17" y2="8"/><line x1="7" y1="12" x2="13" y2="12"/><line x1="7" y1="16" x2="11" y2="16"/></svg>'''
icon_step3 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="30" height="30"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'''
icon_step4 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="30" height="30"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'''
icon_step5 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="30" height="30"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'''

icon_lvl1 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="36" height="36"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'''
icon_lvl2 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="36" height="36"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>'''
icon_lvl3 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#c084fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="36" height="36"><path d="M2 20h20M5 20V8l7-5 7 5v12M9 20v-6h6v6"/></svg>'''
icon_lvl4 = '''<svg viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="36" height="36"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'''

icon_qr = '''<svg viewBox="0 0 24 24" fill="none" stroke="#00c9a7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>'''
icon_shield = '''<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'''
icon_percent = '''<svg viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>'''

html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>چارت چرخه درخواست، پیگیری و ماتریس زمان‌بندی و بودجه ای‌پلاک</title>
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
  background-color: #070c17;
  background-image:
    radial-gradient(circle at 50% 0%, rgba(0, 201, 167, 0.17) 0%, transparent 46%),
    radial-gradient(circle at 12% 30%, rgba(56, 189, 248, 0.14) 0%, transparent 40%),
    radial-gradient(circle at 88% 30%, rgba(168, 85, 247, 0.14) 0%, transparent 40%),
    radial-gradient(circle at 50% 100%, rgba(245, 158, 11, 0.12) 0%, transparent 50%),
    radial-gradient(rgba(255, 255, 255, 0.05) 1.2px, transparent 1.2px);
  background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 28px 28px;
  font-family: 'YekanBakh', system-ui, -apple-system, sans-serif;
  color: #ffffff;
  padding: 38px 48px 30px;
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
  padding-bottom: 22px;
  border-bottom: 1.5px solid rgba(255, 255, 255, 0.12);
  position: relative;
}}
.header-wrapper::after {{
  content: '';
  position: absolute;
  bottom: -2px;
  right: 15%;
  left: 15%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00c9a7, #38bdf8, #a855f7, transparent);
  box-shadow: 0 0 16px rgba(0, 201, 167, 0.6);
}}

.brand-section {{
  display: flex;
  align-items: center;
  gap: 22px;
}}
.logo-container {{
  width: 98px;
  height: 98px;
  background: rgba(255, 255, 255, 0.05);
  border: 1.5px solid rgba(0, 201, 167, 0.4);
  border-radius: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 35px rgba(0, 201, 167, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
}}
.logo-container img {{
  width: 78px;
  height: auto;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.6));
}}
.title-block h1 {{
  font-size: 36px;
  font-weight: 900;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #ffffff 30%, #00c9a7 85%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: flex;
  align-items: center;
  gap: 14px;
}}
.title-block h1 .badge-ver {{
  font-size: 14.5px;
  font-weight: 800;
  padding: 5px 15px;
  border-radius: 20px;
  background: rgba(0, 201, 167, 0.16);
  color: #00c9a7;
  border: 1px solid rgba(0, 201, 167, 0.35);
  -webkit-text-fill-color: #00c9a7;
}}
.title-block p {{
  font-size: 18.5px;
  color: #94a3b8;
  margin-top: 5px;
  font-weight: 400;
}}

.kpi-pills {{
  display: flex;
  gap: 14px;
}}
.kpi-pill {{
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(15px);
  border-radius: 18px;
  padding: 11px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.kpi-num {{
  font-size: 28px;
  font-weight: 900;
  color: #00c9a7;
  line-height: 1;
}}
.kpi-text {{
  font-size: 13px;
  line-height: 1.35;
  color: #cbd5e1;
}}
.kpi-text strong {{
  display: block;
  font-size: 14.5px;
  color: #fff;
}}

/* ================= SECTION 1: 5-STEP LIFECYCLE ================= */
.section-heading {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0 12px;
}}
.section-title {{
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 10px;
}}
.section-sub {{
  font-size: 14px;
  color: #94a3b8;
}}

.pipeline-grid {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
  position: relative;
}}
.pipeline-step {{
  background: rgba(15, 23, 42, 0.75);
  border: 1.5px solid var(--step-border);
  border-radius: 22px;
  padding: 18px 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.pipeline-step::before {{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle at top right, var(--step-glow), transparent 70%);
  pointer-events: none;
}}

.step-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}}
.step-badge {{
  font-size: 12px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 12px;
  background: var(--badge-bg);
  color: var(--step-color);
  border: 1px solid var(--badge-border);
}}
.step-icon {{
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: var(--icon-bg);
  border: 1px solid var(--icon-border);
  display: flex;
  align-items: center;
  justify-content: center;
}}

.step-main h3 {{
  font-size: 19px;
  font-weight: 900;
  color: #fff;
  margin-bottom: 4px;
}}
.step-main p {{
  font-size: 13px;
  color: #cbd5e1;
  line-height: 1.5;
}}
.step-meta {{
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 12px;
  color: var(--step-color);
  font-weight: 700;
}}

/* ================= SECTION 2: 4-TIER SLA & BUDGET MATRIX ================= */
.matrix-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 10px;
}}

.matrix-card {{
  background: rgba(13, 20, 36, 0.85);
  border-radius: 26px;
  border: 1.5px solid var(--tier-border);
  padding: 24px 22px 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 16px 35px -8px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(25px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.matrix-card::before {{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 140px;
  height: 140px;
  background: radial-gradient(circle at top right, var(--tier-glow), transparent 70%);
  pointer-events: none;
}}

.tier-head {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}}
.tier-icon-wrap {{
  width: 62px;
  height: 62px;
  border-radius: 18px;
  background: var(--tier-icon-bg);
  border: 1.5px solid var(--tier-icon-border);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px -4px var(--tier-glow);
}}
.tier-tag {{
  font-size: 13px;
  font-weight: 800;
  padding: 5px 12px;
  border-radius: 14px;
  background: var(--tier-tag-bg);
  color: var(--tier-color);
  border: 1px solid var(--tier-tag-border);
}}

.tier-title {{
  font-size: 21px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 2px;
}}
.tier-en {{
  font-size: 12px;
  font-weight: 700;
  color: var(--tier-color);
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}}

/* Key Parameters Strip */
.tier-stat-strip {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 14px;
}}
.tier-stat-box {{
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 14px;
  padding: 8px 10px;
}}
.stat-box-lbl {{
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
}}
.stat-box-val {{
  font-size: 15px;
  font-weight: 900;
  color: var(--tier-color);
  margin-top: 2px;
}}

.tier-examples {{
  display: flex;
  flex-direction: column;
  gap: 7px;
  margin-bottom: 14px;
}}
.example-item {{
  background: rgba(255, 255, 255, 0.035);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 12px;
  padding: 7px 12px;
  font-size: 13px;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.example-bullet {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--tier-color);
  flex-shrink: 0;
}}

.tier-footer {{
  background: rgba(var(--rgb), 0.1);
  border: 1px dashed rgba(var(--rgb), 0.35);
  border-radius: 14px;
  padding: 9px 14px;
  font-size: 12.5px;
  color: #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.tier-footer strong {{
  color: var(--tier-color);
  font-weight: 800;
}}

/* Level Palette */
.tier-1 {{
  --rgb: 16, 185, 129;
  --tier-color: #34d399;
  --tier-border: rgba(16, 185, 129, 0.4);
  --tier-glow: rgba(16, 185, 129, 0.35);
  --tier-icon-bg: rgba(16, 185, 129, 0.16);
  --tier-icon-border: rgba(16, 185, 129, 0.4);
  --tier-tag-bg: rgba(16, 185, 129, 0.14);
  --tier-tag-border: rgba(16, 185, 129, 0.3);
}}
.tier-2 {{
  --rgb: 59, 130, 246;
  --tier-color: #60a5fa;
  --tier-border: rgba(59, 130, 246, 0.4);
  --tier-glow: rgba(59, 130, 246, 0.35);
  --tier-icon-bg: rgba(59, 130, 246, 0.16);
  --tier-icon-border: rgba(59, 130, 246, 0.4);
  --tier-tag-bg: rgba(59, 130, 246, 0.14);
  --tier-tag-border: rgba(59, 130, 246, 0.3);
}}
.tier-3 {{
  --rgb: 168, 85, 247;
  --tier-color: #c084fc;
  --tier-border: rgba(168, 85, 247, 0.4);
  --tier-glow: rgba(168, 85, 247, 0.35);
  --tier-icon-bg: rgba(168, 85, 247, 0.16);
  --tier-icon-border: rgba(168, 85, 247, 0.4);
  --tier-tag-bg: rgba(168, 85, 247, 0.14);
  --tier-tag-border: rgba(168, 85, 247, 0.3);
}}
.tier-4 {{
  --rgb: 245, 158, 11;
  --tier-color: #fbbf24;
  --tier-border: rgba(245, 158, 11, 0.4);
  --tier-glow: rgba(245, 158, 11, 0.35);
  --tier-icon-bg: rgba(245, 158, 11, 0.16);
  --tier-icon-border: rgba(245, 158, 11, 0.4);
  --tier-tag-bg: rgba(245, 158, 11, 0.14);
  --tier-tag-border: rgba(245, 158, 11, 0.3);
}}

/* ================= SECTION 3: TRACKING & GOVERNANCE PILLARS ================= */
.pillars-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 14px;
}}
.pillar-card {{
  background: rgba(15, 23, 42, 0.7);
  border: 1.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  padding: 16px 20px;
  backdrop-filter: blur(15px);
  display: flex;
  align-items: center;
  gap: 16px;
}}
.pillar-icon-box {{
  width: 54px;
  height: 54px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.pillar-info h4 {{
  font-size: 16.5px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 2px;
}}
.pillar-info p {{
  font-size: 12.5px;
  color: #94a3b8;
  line-height: 1.4;
}}

/* Footer */
.footer-strip {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 13.5px;
  color: #94a3b8;
}}
.footer-strip .specs {{
  display: flex;
  gap: 20px;
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

  <!-- Top Header -->
  <header class="header-wrapper">
    <div class="brand-section">
      <div class="logo-container">
        <img src="data:image/png;base64,{logo}" alt="ای‌پلاک">
      </div>
      <div class="title-block">
        <h1>
          <span>چارت جامع چرخه درخواست، پیگیری هوشمند و ماتریس زمان‌بندی و بودجه</span>
          <span class="badge-ver">SLA استاندارد شهرداری ورامین</span>
        </h1>
        <p>رهگیری مکانیزه، شفافیت مالی و تناسب دقیق مدت زمان اجرای عملیات بر مبنای بودجه و مقیاس کار • E-Pelak Workflow</p>
      </div>
    </div>
    <div class="kpi-pills">
      <div class="kpi-pill">
        <span class="kpi-num">۵</span>
        <div class="kpi-text"><strong>گام پیگیری هوشمند</strong>از ثبت تا رضایت‌سنجی</div>
      </div>
      <div class="kpi-pill">
        <span class="kpi-num">۴</span>
        <div class="kpi-text"><strong>سطح بودجه و زمان</strong>SLA استاندارد شهری</div>
      </div>
      <div class="kpi-pill">
        <span class="kpi-num">EP</span>
        <div class="kpi-text"><strong>کد رهگیری یکتا</strong>پیامک آنی و QR اعتبارسنجی</div>
      </div>
    </div>
  </header>

  <!-- Section 1: The 5-Step Lifecycle -->
  <section>
    <div class="section-heading">
      <div class="section-title">
        <span>🔄</span> چرخه ۵ مرحله‌ای رسیدگی به درخواست‌های مردمی (از ثبت تا مختومه‌سازی)
      </div>
      <div class="section-sub">ارتباط برخط شهروند با کارتابل منطقه، ناظر فنی و شهردار ناحیه</div>
    </div>

    <div class="pipeline-grid">

      <!-- Step 1 -->
      <div class="pipeline-step" style="--step-border:rgba(0,201,167,0.4); --step-glow:rgba(0,201,167,0.3); --step-color:#00c9a7; --badge-bg:rgba(0,201,167,0.12); --badge-border:rgba(0,201,167,0.3); --icon-bg:rgba(0,201,167,0.15); --icon-border:rgba(0,201,167,0.4);">
        <div class="step-top">
          <span class="step-badge">مرحله اول</span>
          <div class="step-icon">{icon_step1}</div>
        </div>
        <div class="step-main">
          <h3>۱. ثبت درخواست شهروندی</h3>
          <p>انتخاب موضوع مشکل (آسفالت، پسماند، روشنایی...)، درج توضیحات و پیوست عکس با موقعیت ماهواره‌ای GPS دقیق معبر.</p>
        </div>
        <div class="step-meta">مدت اقدام: کمتر از ۲ دقیقه توسط شهروند</div>
      </div>

      <!-- Step 2 -->
      <div class="pipeline-step" style="--step-border:rgba(56,189,248,0.4); --step-glow:rgba(56,189,248,0.3); --step-color:#38bdf8; --badge-bg:rgba(56,189,248,0.12); --badge-border:rgba(56,189,248,0.3); --icon-bg:rgba(56,189,248,0.15); --icon-border:rgba(56,189,248,0.4);">
        <div class="step-top">
          <span class="step-badge">مرحله دوم</span>
          <div class="step-icon">{icon_step2}</div>
        </div>
        <div class="step-main">
          <h3>۲. صدور کد رهگیری و تریاژ</h3>
          <p>تخصیص شناسه یکتا (مانند EP-1403-9821)، ارسال آنی پیامک تایید به همراه لینک رهگیری و اعتبارسنجی اولیه اپراتور ۱۳۷.</p>
        </div>
        <div class="step-meta">مدت زمان: آنی سیستمی (حداکثر ۱۵ دقیقه)</div>
      </div>

      <!-- Step 3 -->
      <div class="pipeline-step" style="--step-border:rgba(168,85,247,0.4); --step-glow:rgba(168,85,247,0.3); --step-color:#c084fc; --badge-bg:rgba(168,85,247,0.12); --badge-border:rgba(168,85,247,0.3); --icon-bg:rgba(168,85,247,0.15); --icon-border:rgba(168,85,247,0.4);">
        <div class="step-top">
          <span class="step-badge">مرحله سوم</span>
          <div class="step-icon">{icon_step3}</div>
        </div>
        <div class="step-main">
          <h3>۳. ارجاع و برآورد بودجه</h3>
          <p>ارجاع خودکار به واحد مربوطه (عمران، خدمات شهری، زیباسازی...)، کارشناسی میدانی و تطبیق با ماتریس سقف بودجه و SLA.</p>
        </div>
        <div class="step-meta">سطح‌بندی: فوری، خرد، متوسط یا کلان</div>
      </div>

      <!-- Step 4 -->
      <div class="pipeline-step" style="--step-border:rgba(251,191,36,0.4); --step-glow:rgba(251,191,36,0.3); --step-color:#fbbf24; --badge-bg:rgba(251,191,36,0.12); --badge-border:rgba(251,191,36,0.3); --icon-bg:rgba(251,191,36,0.15); --icon-border:rgba(251,191,36,0.4);">
        <div class="step-top">
          <span class="step-badge">مرحله چهارم</span>
          <div class="step-icon">{icon_step4}</div>
        </div>
        <div class="step-main">
          <h3>۴. اجرای میدانی و رفع نقص</h3>
          <p>اعزام ماشین‌آلات و اکیپ‌های عملیاتی شهرداری، بارگذاری تصویر بعد از انجام کار توسط پیمانکار و تایید ناظر مقیم ناحیه.</p>
        </div>
        <div class="step-meta">پایش لحظه‌ای: نمایش درصد پیشرفت در اپ</div>
      </div>

      <!-- Step 5 -->
      <div class="pipeline-step" style="--step-border:rgba(16,185,129,0.4); --step-glow:rgba(16,185,129,0.3); --step-color:#34d399; --badge-bg:rgba(16,185,129,0.12); --badge-border:rgba(16,185,129,0.3); --icon-bg:rgba(16,185,129,0.15); --icon-border:rgba(16,185,129,0.4);">
        <div class="step-top">
          <span class="step-badge">مرحله پنجم</span>
          <div class="step-icon">{icon_step5}</div>
        </div>
        <div class="step-main">
          <h3>۵. تایید شهروند و رضایت‌سنجی</h3>
          <p>ارسال اعلان خاتمه به شهروند، ثبت امتیاز کیفیت کار (۱ تا ۵ ستاره) و امکان درخواست بررسی مجدد در صورت عدم رضایت.</p>
        </div>
        <div class="step-meta">فرجام کار: مختومه فقط با تایید شهروند</div>
      </div>

    </div>
  </section>

  <!-- Section 2: 4-Tier Budget-to-Duration SLA Matrix -->
  <section>
    <div class="section-heading">
      <div class="section-title">
        <span>⏱️</span> ماتریس تطبیق مدت زمان انجام کار متناسب با بودجه و مقیاس پروژه (SLA Matrix)
      </div>
      <div class="section-sub">استاندارد مصوب زمان‌بندی شهرداری ورامین جهت جلوگیری از بلاتکلیفی گزارش‌ها</div>
    </div>

    <div class="matrix-grid">

      <!-- Tier 1: Immediate -->
      <div class="matrix-card tier-1">
        <div>
          <div class="tier-head">
            <div class="tier-icon-wrap">{icon_lvl1}</div>
            <span class="tier-tag">سطح ۱: فوری و روزمره</span>
          </div>
          <div class="tier-title">خدمات ضربتی و اضطراری</div>
          <div class="tier-en">TIER 1: EMERGENCY & RAPID FIX</div>

          <div class="tier-stat-strip">
            <div class="tier-stat-box">
              <div class="stat-box-lbl">مدت زمان استاندارد</div>
              <div class="stat-box-val">۲ الی ۱۲ ساعت</div>
            </div>
            <div class="tier-stat-box">
              <div class="stat-box-lbl">منبع و سقف بودجه</div>
              <div class="stat-box-val">تنخواه جاری ناحیه</div>
            </div>
          </div>

          <div class="tier-examples">
            <div class="example-item"><span class="example-bullet"></span>رفع خطر درخت شکسته یا شاخه‌های آویزان</div>
            <div class="example-item"><span class="example-bullet"></span>خاموشی یا نقص روشنایی معابر و پارک‌ها</div>
            <div class="example-item"><span class="example-bullet"></span>لایروبی انسداد جوی و مهار آب‌گرفتگی باران</div>
            <div class="example-item"><span class="example-bullet"></span>تعویض یا شستشوی فوری مخازن زباله مکانیزه</div>
            <div class="example-item"><span class="example-bullet"></span>جمع‌آوری فوری لاشه حیوانات و ضایعات معبر</div>
          </div>
        </div>

        <div class="tier-footer">
          <span>واحد مجری: <strong>خدمات شهری و اکیپ امانی</strong></span>
          <span>پایش: <strong>هشدار پس از ۱۲ ساعت</strong></span>
        </div>
      </div>

      <!-- Tier 2: Small Scale -->
      <div class="matrix-card tier-2">
        <div>
          <div class="tier-head">
            <div class="tier-icon-wrap">{icon_lvl2}</div>
            <span class="tier-tag">سطح ۲: پروژه‌های خرد محله‌ای</span>
          </div>
          <div class="tier-title">تعمیرات و بهسازی خرد</div>
          <div class="tier-en">TIER 2: LOCAL MINOR REPAIR</div>

          <div class="tier-stat-strip">
            <div class="tier-stat-box">
              <div class="stat-box-lbl">مدت زمان استاندارد</div>
              <div class="stat-box-val">۲ الی ۳ روز کاری</div>
            </div>
            <div class="tier-stat-box">
              <div class="stat-box-lbl">منبع و سقف بودجه</div>
              <div class="stat-box-val">تا ۵۰ میلیون تومان</div>
            </div>
          </div>

          <div class="tier-examples">
            <div class="example-item"><span class="example-bullet"></span>لکه‌گیری چاله‌های کوچه و پیاده‌روها</div>
            <div class="example-item"><span class="example-bullet"></span>نصب، اصلاح یا رنگ‌آمیزی سرعت‌گیر آسفالتی</div>
            <div class="example-item"><span class="example-bullet"></span>تعمیر نیمکت‌ها و ست‌های بازی ورزشی بوستان</div>
            <div class="example-item"><span class="example-bullet"></span>نصب یا مرمت تابلو نام کوچه و معابر محله</div>
            <div class="example-item"><span class="example-bullet"></span>ساماندهی باغچه‌ها و علف‌تراشی حاشیه معابر</div>
          </div>
        </div>

        <div class="tier-footer">
          <span>واحد مجری: <strong>شهرداری ناحیه و فضای سبز</strong></span>
          <span>پایش: <strong>گزارش به شهردار منطقه</strong></span>
        </div>
      </div>

      <!-- Tier 3: Medium Scale -->
      <div class="matrix-card tier-3">
        <div>
          <div class="tier-head">
            <div class="tier-icon-wrap">{icon_lvl3}</div>
            <span class="tier-tag">سطح ۳: پروژه‌های متوسط شهری</span>
          </div>
          <div class="tier-title">عمران و بهسازی معابر</div>
          <div class="tier-en">TIER 3: MEDIUM INFRASTRUCTURE</div>

          <div class="tier-stat-strip">
            <div class="tier-stat-box">
              <div class="stat-box-lbl">مدت زمان استاندارد</div>
              <div class="stat-box-val">۷ الی ۱۴ روز کاری</div>
            </div>
            <div class="tier-stat-box">
              <div class="stat-box-lbl">منبع و سقف بودجه</div>
              <div class="stat-box-val">۵۰ تا ۳۰۰ میلیون تومان</div>
            </div>
          </div>

          <div class="tier-examples">
            <div class="example-item"><span class="example-bullet"></span>روکش کامل آسفالت یک یا چند کوچه بن‌بست</div>
            <div class="example-item"><span class="example-bullet"></span>جدول‌گذاری، کانیوا و دفع آب‌های سطحی کوچه</div>
            <div class="example-item"><span class="example-bullet"></span>کف‌پوش و مناسب‌سازی پیاده‌رو معلولین و سالمندان</div>
            <div class="example-item"><span class="example-bullet"></span>احداث برج نوری یا بهسازی تاسیسات بوستان</div>
            <div class="example-item"><span class="example-bullet"></span>نصب چراغ راهنمایی هوشمند و اصلاح هندسی</div>
          </div>
        </div>

        <div class="tier-footer">
          <span>واحد مجری: <strong>معاونت فنی و سازمان عمران</strong></span>
          <span>تخصیص: <strong>اعتبار تملک دارایی سرمایه‌ای</strong></span>
        </div>
      </div>

      <!-- Tier 4: Major Infrastructure -->
      <div class="matrix-card tier-4">
        <div>
          <div class="tier-head">
            <div class="tier-icon-wrap">{icon_lvl4}</div>
            <span class="tier-tag">سطح ۴: پروژه‌های کلان و زیربنایی</span>
          </div>
          <div class="tier-title">طرح‌های کلان و سرمایه‌ای</div>
          <div class="tier-en">TIER 4: STRATEGIC MEGA PROJECTS</div>

          <div class="tier-stat-strip">
            <div class="tier-stat-box">
              <div class="stat-box-lbl">مدت زمان استاندارد</div>
              <div class="stat-box-val">۳۰ الی ۹۰ روز کاری</div>
            </div>
            <div class="tier-stat-box">
              <div class="stat-box-lbl">منبع و سقف بودجه</div>
              <div class="stat-box-val">بیش از ۳۰۰ میلیون تومان</div>
            </div>
          </div>

          <div class="tier-examples">
            <div class="example-item"><span class="example-bullet"></span>احداث پارک و فضای سبز چند هکتاری محله‌ای</div>
            <div class="example-item"><span class="example-bullet"></span>احداث پل مکانیزه عابر پیاده یا تقاطع غیرهمسطح</div>
            <div class="example-item"><span class="example-bullet"></span>تعریض خیابان اصلی و تملک املاک مسیری</div>
            <div class="example-item"><span class="example-bullet"></span>احداث کانال سرپوشیده جمع‌آوری سیلاب شهری</div>
            <div class="example-item"><span class="example-bullet"></span>نوسازی جامع ناوگان یا احداث سالن مدیریت بحران</div>
          </div>
        </div>

        <div class="tier-footer">
          <span>فرآیند: <strong>مصوبه شورای شهر + مناقصه ستاد</strong></span>
          <span>نظارت: <strong>شورای اسلامی شهر ورامین</strong></span>
        </div>
      </div>

    </div>
  </section>

  <!-- Section 3: 3 Governance & Transparency Pillars -->
  <section class="pillars-grid">
    <div class="pillar-card">
      <div class="pillar-icon-box">{icon_qr}</div>
      <div class="pillar-info">
        <h4>شناسه رهگیری و استعلام برخط</h4>
        <p>هر درخواست دارای بارکد دوبعدی QR و کد یکتای کشوری است؛ پیامک مراحل تغییر وضعیت و نام تکنسین مجری به شماره موبایل شهروند مخابره می‌شود.</p>
      </div>
    </div>
    <div class="pillar-card">
      <div class="pillar-icon-box">{icon_percent}</div>
      <div class="pillar-info">
        <h4>شفافیت مالی و زمان‌سنج پیشرفت</h4>
        <p>در پروژه‌های عمرانی، درصد پیشرفت فیزیکی، تاریخ برآورد اتمام، مبلغ مصوب و مشخصات پیمانکار در کارتابل «پیگیری درخواست» برای عموم قابل رویت است.</p>
      </div>
    </div>
    <div class="pillar-card">
      <div class="pillar-icon-box">{icon_shield}</div>
      <div class="pillar-info">
        <h4>سامانه هشدار تاخیر و ضمانت حقوق شهروند</h4>
        <p>در صورت گذشت زمان از سقف SLA، تیکت قرمز شده و مستقیماً به کارتابل بازرسی و شهردار ورامین هدایت می‌شود تا دلیل تاخیر بررسی و اقدام فوری گردد.</p>
      </div>
    </div>
  </section>

  <!-- Footer Technical Bar -->
  <footer class="footer-strip">
    <div class="specs">
      <div class="spec-item"><span class="spec-dot"></span>ارتباط مستقیم با مرکز پیام ۱۳۷ شهرداری ورامین</div>
      <div class="spec-item"><span class="spec-dot"></span>پشتیبانی دو زبانه (فارسی / انگلیسی) در کارتابل پیگیری</div>
      <div class="spec-item"><span class="spec-dot"></span>آرشیو دائمی سوابق و تاریخچه رسیدگی در پروفایل شهروندی</div>
      <div class="spec-item"><span class="spec-dot"></span>الزام به تایید نهایی شهروند قبل از بایگانی و بسته شدن گزارش</div>
    </div>
    <div>طراحی و استقرار: سیستم هوشمند مدیریت شهری ای‌پلاک • شهرداری ورامین</div>
  </footer>

</body>
</html>
"""

html_path = "/home/user/eplak/tools/eplak_tracking_chart.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved HTML template to", html_path)

output_png = "/home/user/eplak/eplak_tracking_budget_chart.png"
cmd = [
    "/usr/bin/chromium",
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--window-size=2400,1560",
    f"--screenshot={output_png}",
    html_path
]

print("Rendering high-res tracking & budget chart...")
subprocess.run(cmd, check=True)
size = os.path.getsize(output_png)
print(f"Chart rendered successfully to {output_png} ({size:,} bytes)")
