import re

print("[1] Updating eplak-fixed/index.html ...")
html_path = '/home/user/eplak/eplak-fixed/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove <div class="vsc-top-shade"></div> from index.html
if '<div class="vsc-top-shade"></div>' in html:
    html = html.replace('            <div class="vsc-top-shade"></div>\n', '')
    html = html.replace('<div class="vsc-top-shade"></div>', '')
    print("   -> Removed vsc-top-shade from index.html successfully!")
else:
    print("   -> vsc-top-shade not found in index.html.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)


print("\n[2] Updating eplak-fixed/assets/css/style.css ...")
style_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the top shade and update vsc-shade to pure bottom-up black gradient
old_shade_block = """  /* مشکی بالای عکس به سمت وسط که محو و کمرنگ می‌شود و ارتفاعش کم است */
  .vsc-top-shade {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 35%;
    background:
      linear-gradient(180deg, rgba(0, 0, 0, 0.88) 0%, rgba(0, 0, 0, 0.52) 32%, rgba(0, 0, 0, 0.16) 68%, rgba(0, 0, 0, 0) 100%),
      radial-gradient(ellipse 90% 65% at 50% 0%, rgba(0, 0, 0, 0.72) 0%, rgba(0, 0, 0, 0) 100%);
    z-index: 1;
    pointer-events: none;
  }

  /* layered depth shading for legibility + richness */
  .vsc-shade {
    position: absolute;
    inset: 0;
    background:
      /* گرادینت مشکی بالای عکس فید شونده به سمت وسط با ارتفاع کم */
      linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.48) 15%, rgba(0,0,0,0.12) 26%, transparent 36%),
      /* گرادینت تیره پایین برای وضوح کامل متن و دکمه‌ها */
      linear-gradient(180deg, transparent 40%, rgba(6,16,18,0.65) 66%, rgba(4,10,12,0.96) 100%),
      linear-gradient(95deg, rgba(4,14,14,0.45) 0%, rgba(4,14,14,0.05) 45%, rgba(4,14,14,0) 70%);
    z-index: 1;
    pointer-events: none;
  }"""

new_shade_block = """  /* layered depth shading: مشکی شیک از پایین عکس به سمت وسط که ملایم محو می‌شود */
  .vsc-shade {
    position: absolute;
    inset: 0;
    background:
      /* گرادینت مشکی از لبه پایین به سمت بالا/وسط که ملایم فید می‌شود (بالای عکس کاملاً تمیز و شفاف است) */
      linear-gradient(to top, rgba(0, 0, 0, 0.96) 0%, rgba(0, 0, 0, 0.82) 22%, rgba(0, 0, 0, 0.45) 44%, rgba(0, 0, 0, 0.10) 58%, transparent 68%),
      linear-gradient(95deg, rgba(0, 0, 0, 0.40) 0%, rgba(0, 0, 0, 0.08) 40%, transparent 65%);
    z-index: 1;
    pointer-events: none;
  }"""

if old_shade_block in css:
    css = css.replace(old_shade_block, new_shade_block)
    print("   -> CSS updated with exact replacement!")
else:
    print("   [!] Could not find exact old_shade_block, using regex replacement...")
    pattern = r'/\* مشکی بالای عکس.*?\*/\s*\.vsc-top-shade\s*\{.*?\}.*?\.vsc-shade\s*\{.*?\pointer-events:\s*none;\s*\}'
    match = re.search(pattern, css, flags=re.DOTALL)
    if match:
        css = css[:match.start()] + new_shade_block + css[match.end():]
        print("   -> CSS updated via regex replacement!")
    else:
        print("   [ERR] Failed to match shade block in style.css.")

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Done updating source files!")
