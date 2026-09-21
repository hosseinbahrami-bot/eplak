import re

path = '/home/user/eplak/eplak-fixed/modules/weather-3d.js'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# Add visibility check in animation loop so it consumes 0% CPU when not viewing dashboard!
optimization_hook = """
  // توقف خودکار پردازش گرافیکی در صورت عدم نمایش صفحه پیشخوان جهت جلوگیری از لگ یا مصرف باتری
  function isDashboardVisible() {
    var dash = document.getElementById('screen-dashboard');
    return dash && dash.classList.contains('active');
  }

  function frame() {
    animFrameId = requestAnimationFrame(frame);
    if (!isDashboardVisible()) return; // اگر کاربر در پیشخوان نیست، پردازش نکن
    timeTick++;
    drawScene();
  }
"""

code = code.replace(
    """    function frame() {
      timeTick++;
      drawScene();
      animFrameId = requestAnimationFrame(frame);
    }""",
    optimization_hook
)

# In resizeCanvas, ensure it adapts whenever dashboard becomes active
resize_hook = """  function resizeCanvas() {
    if (!canvas) return;
    var rect = canvas.parentElement ? canvas.parentElement.getBoundingClientRect() : null;
    var w = (rect && rect.width > 50) ? rect.width : (canvas.parentElement ? canvas.parentElement.offsetWidth : 340);
    var h = (rect && rect.height > 50) ? rect.height : (canvas.parentElement ? canvas.parentElement.offsetHeight : 236);
    if (w > 0 && h > 0 && (canvas.width !== Math.floor(w) || canvas.height !== Math.floor(h))) {
      canvas.width = Math.floor(w);
      canvas.height = Math.floor(h);
      createParticles();
    }
  }"""

code = re.sub(
    r'function resizeCanvas\(\)\s*\{[^}]*\}',
    resize_hook,
    code
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Optimized weather-3d.js performance!")
