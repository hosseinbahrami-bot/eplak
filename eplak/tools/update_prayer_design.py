import re

css_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Luxury Prayer Section Styles
prayer_css = """
  /* ============================================================
     طراحی فوق‌العاده شکیل، اختصاصی و زیبای بخش اوقات شرعی (Islamic Luxury)
     ============================================================ */
  #prayerCard {
    position: relative;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(13, 28, 48, 0.75) 0%, rgba(7, 18, 32, 0.82) 100%);
    border: 1px solid rgba(0, 201, 167, 0.18);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
  }
  html.day #prayerCard {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.85) 0%, rgba(235, 248, 245, 0.9) 100%);
    border: 1px solid rgba(0, 150, 130, 0.22);
    box-shadow: 0 8px 24px rgba(0, 150, 130, 0.08);
  }

  .prayer-luxury-wrap {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  /* ۱. بنر ویژه و لوکس نوبت در پیش‌رو (Next Prayer Hero) */
  .prayer-next-hero {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    padding: 13px 15px;
    background: linear-gradient(135deg, rgba(0, 201, 167, 0.18) 0%, rgba(13, 35, 58, 0.7) 100%);
    border: 1px solid rgba(0, 229, 195, 0.32);
    box-shadow: 0 6px 20px -2px rgba(0, 201, 167, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.15);
  }
  html.day .prayer-next-hero {
    background: linear-gradient(135deg, rgba(0, 201, 167, 0.16) 0%, rgba(255, 255, 255, 0.95) 100%);
    border: 1px solid rgba(0, 168, 142, 0.28);
    box-shadow: 0 6px 18px rgba(0, 168, 142, 0.12), inset 0 1px 0 #ffffff;
  }

  .pnh-glow-orb {
    position: absolute;
    top: -30px;
    left: -30px;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0, 229, 195, 0.25) 0%, transparent 70%);
    pointer-events: none;
    filter: blur(10px);
  }

  .pnh-content {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .pnh-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .pnh-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 999px;
    background: rgba(0, 201, 167, 0.22);
    border: 1px solid rgba(0, 229, 195, 0.4);
    font-size: 11px;
    font-weight: 700;
    color: #00E5C3;
  }
  html.day .pnh-tag {
    background: rgba(0, 168, 142, 0.15);
    border-color: rgba(0, 168, 142, 0.35);
    color: #008770;
  }

  .pnh-pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00E5C3;
    box-shadow: 0 0 8px #00E5C3;
    animation: heroDotPulse 1.8s infinite;
  }

  .pnh-countdown {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.75);
    padding: 3px 9px;
    background: rgba(0, 0, 0, 0.22);
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  html.day .pnh-countdown {
    color: rgba(10, 42, 34, 0.75);
    background: rgba(255, 255, 255, 0.7);
    border-color: rgba(0, 150, 130, 0.15);
  }

  .pnh-main {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 2px;
  }

  .pnh-title-group {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .pnh-icon-wrap {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: rgba(0, 201, 167, 0.22);
    border: 1px solid rgba(0, 229, 195, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #00E5C3;
    box-shadow: 0 4px 14px rgba(0, 201, 167, 0.25);
  }
  html.day .pnh-icon-wrap {
    background: rgba(0, 168, 142, 0.18);
    border-color: rgba(0, 168, 142, 0.3);
    color: #008770;
  }

  .pnh-icon-wrap svg {
    width: 22px;
    height: 22px;
  }

  .pnh-title {
    font-size: 17px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.3;
  }
  html.day .pnh-title {
    color: #0a2a22;
  }

  .pnh-sub {
    font-size: 10.5px;
    color: rgba(255, 255, 255, 0.6);
  }
  html.day .pnh-sub {
    color: rgba(10, 42, 34, 0.6);
  }

  .pnh-time {
    font-size: 25px;
    font-weight: 900;
    color: #00E5C3;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 10px rgba(0, 229, 195, 0.35);
  }
  html.day .pnh-time {
    color: #008770;
    text-shadow: none;
  }

  /* ۲. شبکه کارت‌های شکیل اوقات شرعی (۳ ستون در ۲ سطر) */
  .prayer-cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }

  .prayer-box-card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 11px 6px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: default;
    overflow: hidden;
  }
  html.day .prayer-box-card {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 150, 130, 0.15);
  }

  .prayer-box-card:hover {
    transform: translateY(-2px);
    border-color: rgba(255, 255, 255, 0.18);
  }

  .prayer-box-card.is-active-prayer {
    background: linear-gradient(145deg, rgba(0, 201, 167, 0.20) 0%, rgba(0, 201, 167, 0.06) 100%) !important;
    border: 1.5px solid #00E5C3 !important;
    box-shadow: 0 4px 18px rgba(0, 201, 167, 0.22);
  }
  html.day .prayer-box-card.is-active-prayer {
    background: linear-gradient(145deg, rgba(0, 168, 142, 0.16) 0%, rgba(255, 255, 255, 0.9) 100%) !important;
    border: 1.5px solid #00A88E !important;
    box-shadow: 0 4px 14px rgba(0, 168, 142, 0.18);
  }

  .pbc-top {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    margin-bottom: 5px;
  }

  .pbc-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.7);
  }
  html.day .pbc-icon {
    color: rgba(10, 42, 34, 0.7);
  }
  .is-active-prayer .pbc-icon {
    color: #00E5C3;
  }
  html.day .is-active-prayer .pbc-icon {
    color: #008770;
  }

  .pbc-icon svg {
    width: 17px;
    height: 17px;
  }

  .pbc-label {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    white-space: nowrap;
  }
  .is-active-prayer .pbc-label {
    color: #00E5C3;
    font-weight: 800;
  }
  html.day .is-active-prayer .pbc-label {
    color: #008770;
  }

  .pbc-time {
    font-size: 15px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 0.5px;
  }
  .is-active-prayer .pbc-time {
    color: #ffffff;
    font-weight: 900;
  }
  html.day .is-active-prayer .pbc-time {
    color: #0a2a22;
  }

  .pbc-active-glow {
    position: absolute;
    bottom: 0;
    left: 20%;
    right: 20%;
    height: 2px;
    background: #00E5C3;
    box-shadow: 0 0 8px #00E5C3;
    border-radius: 999px;
  }
  html.day .pbc-active-glow {
    background: #00A88E;
    box-shadow: 0 0 6px #00A88E;
  }

  /* ۳. فوتر تاریخ هجری قمری و افق شرعی */
  .prayer-calendar-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    width: fit-content;
    margin: 4px auto 0;
  }
  html.day .prayer-calendar-footer {
    background: rgba(0, 150, 130, 0.06);
    border-color: rgba(0, 150, 130, 0.15);
  }

  .pcf-icon {
    font-size: 13px;
    line-height: 1;
  }

  .pcf-text {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
  }

  @media (max-width: 360px) {
    .prayer-cards-grid {
      gap: 5px;
    }
    .prayer-box-card {
      padding: 9px 4px;
    }
    .pbc-label {
      font-size: 10px;
    }
    .pbc-time {
      font-size: 13.5px;
    }
    .pnh-title {
      font-size: 15px;
    }
    .pnh-time {
      font-size: 22px;
    }
  }
"""

# Replace the old .prayer-grid styles around lines 4135-4170
old_pattern = r'/\* ── اوقات شرعی ── \*/\s*\.prayer-grid\s*\{.*?\.prayer-hijri\s*\{[^\}]*\}'
if re.search(old_pattern, css, flags=re.DOTALL):
    css = re.sub(old_pattern, prayer_css, css, count=1, flags=re.DOTALL)
    print("Replaced old prayer-grid successfully!")
else:
    # Just append or replace
    css += "\n" + prayer_css
    print("Appended prayer CSS!")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css successfully!")
