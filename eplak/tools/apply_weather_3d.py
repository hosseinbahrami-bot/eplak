import re

print("[1] Updating modules/city-live.js ...")
city_live_path = '/home/user/eplak/eplak-fixed/modules/city-live.js'
with open(city_live_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace renderWeather function
old_render_weather = """  function renderWeather(data) {
    const box = el('weatherCardBody');
    if (!box) return;
    if (window.Weather3D && typeof window.Weather3D.init === 'function') {
      window.Weather3D.init(box, data);
      return;
    }
    const isEn = isEnglish();
    if (!data) {
      box.innerHTML = '<div class="city-live-empty">' + (isEn ? 'No data received' : 'داده‌ای دریافت نشد') + '</div>';
      return;
    }"""

js = re.sub(
    r'function renderWeather\(data\)\s*\{\s*const box = el\(\'weatherCardBody\'\);\s*if \(!box\) return;\s*const isEn = isEnglish\(\);\s*if \(!data\) \{',
    old_render_weather,
    js
)

# On initial boot in city-live.js, make sure Weather3D is initialized
init_boot_code = """  // نمایش فوری استیج ۳ بعدی حتی قبل از دریافت پاسخ شبکه
  try {
    const initialBox = el('weatherCardBody');
    if (initialBox && window.Weather3D) {
      window.Weather3D.init(initialBox, current ? current.weather : null);
    }
  } catch (e) {}"""

if 'نمایش فوری استیج ۳ بعدی' not in js:
    js = js.replace('let loading = false;', 'let loading = false;\n' + init_boot_code)

with open(city_live_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("   -> modules/city-live.js updated successfully!")


print("\n[2] Updating index.html ...")
index_path = '/home/user/eplak/eplak-fixed/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

if 'modules/weather-3d.js' not in html:
    html = html.replace(
        '<script src="modules/city-live.js?v=10"></script>',
        '<script src="modules/weather-3d.js?v=20"></script>\n<script src="modules/city-live.js?v=20"></script>'
    )
    html = html.replace(
        '<script src="modules/city-live.js"></script>',
        '<script src="modules/weather-3d.js?v=20"></script>\n<script src="modules/city-live.js?v=20"></script>'
    )
    print("   -> modules/weather-3d.js script tag added to index.html!")
else:
    print("   -> weather-3d.js already present in index.html.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("   -> index.html updated successfully!")

