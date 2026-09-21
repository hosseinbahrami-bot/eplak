import re
import os

print("[1] Updating eplak-fixed/assets/css/style.css ...")
style_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css_snippet = """
  /* ===== REPORTS & TICKETS SEGMENTED SWITCHER ===== */
  .reports-main-switcher {
    position: relative;
    display: flex;
    gap: 4px;
    padding: 4px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    isolation: isolate;
  }
  .reports-switcher-indicator {
    position: absolute;
    top: 4px;
    bottom: 4px;
    right: 4px;
    width: calc(50% - 6px);
    border-radius: 12px;
    background: linear-gradient(135deg, var(--teal), var(--teal-dark));
    box-shadow: 0 4px 14px rgba(0, 201, 167, 0.45);
    transition: transform 0.35s cubic-bezier(.22,.85,.32,1);
    z-index: 0;
  }
  .reports-switcher-btn {
    position: relative;
    z-index: 1;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 11px 10px;
    border: none;
    background: transparent;
    color: var(--text-muted);
    font-family: inherit;
    font-size: 13.5px;
    font-weight: 700;
    border-radius: 12px;
    cursor: pointer;
    transition: color 0.3s ease;
    white-space: nowrap;
  }
  .reports-switcher-btn.active {
    color: #052e28;
    font-weight: 800;
  }
  .reports-counter-pill {
    font-size: 11px;
    padding: 2px 7px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.18);
    color: inherit;
    font-weight: 800;
    line-height: 1.3;
  }
  .reports-switcher-btn.active .reports-counter-pill {
    background: rgba(5, 46, 40, 0.22);
    color: #052e28;
  }
  html.day .reports-main-switcher {
    background: rgba(0, 0, 0, 0.04);
    border-color: rgba(0, 160, 130, 0.18);
  }
  html.day .reports-switcher-btn.active {
    color: #ffffff;
  }
  html.day .reports-switcher-btn.active .reports-counter-pill {
    background: rgba(255, 255, 255, 0.28);
    color: #ffffff;
  }

  /* Ticket Delete & Action Buttons */
  .ticket-delete-btn {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.24);
    color: #ef4444;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    padding: 0;
  }
  .ticket-delete-btn:hover, .ticket-delete-btn:active {
    background: rgba(239, 68, 68, 0.22);
    border-color: rgba(239, 68, 68, 0.5);
    transform: scale(1.06);
  }
  .btn-danger-outline {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.38);
    color: #ef4444;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.25s ease;
  }
  .btn-danger-outline:hover, .btn-danger-outline:active {
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
    transform: translateY(-1px);
  }

  /* Track Item Card */
  .track-item-card {
    cursor: pointer;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }
  .track-item-card:active {
    transform: scale(0.985);
  }
"""

if 'reports-main-switcher' not in css:
    css += "\n" + new_css_snippet + "\n"
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("   -> CSS updated successfully!")
else:
    print("   -> CSS already contains reports-main-switcher.")

