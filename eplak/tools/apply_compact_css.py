import re

css_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """  /* ============================================================
     طراحی مدرن، فوق‌العاده فشرده و ظریف بخش اوقات شرعی
     ============================================================ */
  #prayerCard {
    position: relative;
    overflow: hidden;
    padding: 11px 13px !important;
    background: linear-gradient(180deg, rgba(13, 28, 48, 0.72) 0%, rgba(7, 18, 32, 0.8) 100%);
    border: 1px solid rgba(0, 201, 167, 0.18);
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.28);
  }
  html.day #prayerCard {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.88) 0%, rgba(235, 248, 245, 0.92) 100%);
    border: 1px solid rgba(0, 150, 130, 0.2);
    box-shadow: 0 4px 18px rgba(0, 150, 130, 0.07);
  }

  .prayer-luxury-wrap {
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  /* ۱. بنر ویژه نوبت در پیش‌رو — کاملاً فشرده و کم‌حجم */
  .prayer-next-hero {
    position: relative;
    overflow: hidden;
    border-radius: 11px;
    padding: 6px 10px;
    background: linear-gradient(135deg, rgba(0, 201, 167, 0.16) 0%, rgba(13, 35, 58, 0.65) 100%);
    border: 1px solid rgba(0, 229, 195, 0.28);
    box-shadow: 0 4px 14px -2px rgba(0, 201, 167, 0.14), inset 0 1px 0 rgba(255, 255, 255, 0.12);
  }
  html.day .prayer-next-hero {
    background: linear-gradient(135deg, rgba(0, 201, 167, 0.14) 0%, rgba(255, 255, 255, 0.95) 100%);
    border: 1px solid rgba(0, 168, 142, 0.25);
    box-shadow: 0 3px 12px rgba(0, 168, 142, 0.1), inset 0 1px 0 #ffffff;
  }

  .pnh-content {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .pnh-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
  }

  .pnh-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 1.5px 7px;
    border-radius: 999px;
    background: rgba(0, 201, 167, 0.2);
    border: 1px solid rgba(0, 229, 195, 0.35);
    font-size: 8.5px;
    font-weight: 700;
    color: #00E5C3;
    letter-spacing: 0.1px;
  }
  html.day .pnh-tag {
    background: rgba(0, 168, 142, 0.12);
    border-color: rgba(0, 168, 142, 0.3);
    color: #008770;
  }

  .pnh-pulse-dot {
    width: 4.5px;
    height: 4.5px;
    border-radius: 50%;
    background: #00E5C3;
    box-shadow: 0 0 6px #00E5C3;
    animation: heroDotPulse 1.8s infinite;
  }

  .pnh-countdown {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 8.5px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    padding: 1.5px 7px;
    background: rgba(0, 0, 0, 0.25);
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  html.day .pnh-countdown {
    color: rgba(10, 42, 34, 0.8);
    background: rgba(255, 255, 255, 0.75);
    border-color: rgba(0, 150, 130, 0.18);
  }

  .pnh-main {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .pnh-title-group {
    display: flex;
    align-items: center;
    gap: 7px;
  }

  .pnh-icon-wrap {
    width: 24px;
    height: 24px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .pnh-icon-wrap svg {
    width: 13px;
    height: 13px;
  }

  .pnh-title {
    font-size: 12px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
  }
  html.day .pnh-title {
    color: #0a2a22;
  }

  .pnh-time {
    font-size: 16px;
    font-weight: 900;
    color: #00E5C3;
    letter-spacing: 0.3px;
    text-shadow: 0 1px 8px rgba(0, 229, 195, 0.3);
  }
  html.day .pnh-time {
    color: #008770;
    text-shadow: none;
  }

  /* ۲. شبکه ۶ کارت بسیار فشرده و شکیل اوقات شرعی */
  .prayer-cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
  }

  .prayer-box-card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5px 3px;
    border-radius: 9px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    transition: all 0.2s ease;
    cursor: default;
    overflow: hidden;
  }
  html.day .prayer-box-card {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(0, 150, 130, 0.13);
  }

  .prayer-box-card:hover {
    transform: translateY(-1px);
    border-color: rgba(255, 255, 255, 0.15);
  }

  .prayer-box-card.is-active-prayer {
    background: linear-gradient(145deg, rgba(0, 201, 167, 0.18) 0%, rgba(0, 201, 167, 0.05) 100%) !important;
    border: 1.2px solid #00E5C3 !important;
    box-shadow: 0 3px 12px rgba(0, 201, 167, 0.2);
  }
  html.day .prayer-box-card.is-active-prayer {
    background: linear-gradient(145deg, rgba(0, 168, 142, 0.14) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
    border: 1.2px solid #00A88E !important;
    box-shadow: 0 3px 10px rgba(0, 168, 142, 0.15);
  }

  .pbc-top {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    margin-bottom: 2px;
  }

  .pbc-icon-disc {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .pbc-icon-disc svg {
    width: 11px;
    height: 11px;
  }

  .pbc-label {
    font-size: 9px;
    font-weight: 600;
    color: var(--text-muted);
    white-space: nowrap;
  }
  .is-active-prayer .pbc-label {
    color: #00E5C3;
    font-weight: 700;
  }
  html.day .is-active-prayer .pbc-label {
    color: #008770;
  }

  .pbc-time {
    font-size: 11.5px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 0.3px;
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
    left: 22%;
    right: 22%;
    height: 1.5px;
    background: #00E5C3;
    box-shadow: 0 0 6px #00E5C3;
    border-radius: 999px;
  }
  html.day .pbc-active-glow {
    background: #00A88E;
    box-shadow: 0 0 5px #00A88E;
  }

  /* ۳. فوتر تاریخ هجری قمری و افق شرعی */
  .prayer-calendar-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    padding: 3px 9px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    width: fit-content;
    margin: 2px auto 0;
  }
  html.day .prayer-calendar-footer {
    background: rgba(0, 150, 130, 0.05);
    border-color: rgba(0, 150, 130, 0.12);
  }

  .pcf-icon {
    font-size: 9.5px;
    line-height: 1;
  }

  .pcf-text {
    font-size: 9px;
    font-weight: 600;
    color: var(--text-muted);
  }

  @media (max-width: 360px) {
    .prayer-cards-grid {
      gap: 3.5px;
    }
    .prayer-box-card {
      padding: 4px 2px;
    }
    .pbc-label {
      font-size: 8.5px;
    }
    .pbc-time {
      font-size: 10.5px;
    }
    .pnh-title {
      font-size: 11px;
    }
    .pnh-time {
      font-size: 14.5px;
    }
  }"""

# Replace the previous prayer block
pattern = r'/\* =+\s*طراحی فوق‌العاده شکیل.*?(?=\n\s*\.city-live-empty|\n\s*@media\s*\(prefers-reduced-motion|$)'
match = re.search(pattern, css, flags=re.DOTALL)
if match:
    css = css[:match.start()] + new_css + "\n\n" + css[match.end():]
    print("Replaced prayer CSS with ultra-compact modern styles!")
else:
    print("Could not find pattern, appending...")
    css += "\n" + new_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css successfully!")
