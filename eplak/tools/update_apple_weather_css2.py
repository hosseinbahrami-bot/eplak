import re

css_path = '/home/user/eplak/eplak-fixed/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace previous apple clouds styling with the organic SVG cloud styles
cloud_replace_pattern = r'/\* ============================================================\s*ابرهای کوچک، بسیار شیک.*?@keyframes appleCloudDrift3 \{[^}]*\}'

organic_cloud_css = """/* ============================================================
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

.apple-cloud-organic.ac-org-1 {
  width: 145px;
  height: 52px;
  top: 14px;
  right: -30px;
  animation: appleCloudFloat1 52s linear infinite;
  opacity: 0.92;
}

.apple-cloud-organic.ac-org-2 {
  width: 115px;
  height: 44px;
  top: 46px;
  left: -25px;
  animation: appleCloudFloat2 68s linear infinite;
  opacity: 0.82;
}

@keyframes appleCloudFloat1 {
  0% { transform: translateX(180px); }
  100% { transform: translateX(-360px); }
}

@keyframes appleCloudFloat2 {
  0% { transform: translateX(200px); }
  100% { transform: translateX(-350px); }
}"""

match = re.search(cloud_replace_pattern, css, flags=re.DOTALL)
if match:
    css = css[:match.start()] + organic_cloud_css + css[match.end():]
    print("   -> Replaced old cloud styles with organic SVG cloud styles!")
else:
    css += "\n" + organic_cloud_css
    print("   -> Appended organic SVG cloud styles!")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("   -> style.css updated successfully!")
