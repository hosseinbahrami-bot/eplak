import re

path = '/home/user/eplak/eplak-fixed/modules/weather-3d.js'
with open(path, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the rain drawing section with ultra-fast single-batch stroke
old_rain_pattern = r'// ۱\. رندر باران ظریف اپل با حلقه‌های ریز پاشش\s*if \(state\.type === \'rain\' \|\| state\.type === \'storm\'\) \{.*?// ۲\. رندر برف'

new_rain_code = """// ۱. رندر باران بسیار سریع و فوق‌العاده روان اپل (یکپارچه با ۱ استروک در فریم)
    if (state.type === 'rain' || state.type === 'storm') {
      ctx.strokeStyle = state.type === 'storm' ? 'rgba(215, 240, 255, 0.65)' : 'rgba(225, 245, 255, 0.55)';
      ctx.lineWidth = 0.9;
      ctx.lineCap = 'round';
      ctx.beginPath(); // شروع یکپارچه مسیر برای صفر کردن لگ

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x + p.windAngle, p.y + p.len);

        p.y += p.speed;
        p.x += (p.windAngle * (p.speed / 16));

        if (p.y > h - 14) {
          if (p.depth > 0.5 && splashes.length < 8 && Math.random() > 0.7) {
            splashes.push({
              x: p.x,
              y: h - 8 + Math.random() * 4,
              radius: 0.8,
              maxRadius: 2.2 + p.depth * 3,
              alpha: 0.5
            });
          }
          p.y = -18;
          p.x = Math.random() * (w + 40) - 10;
        }
      }
      ctx.stroke(); // یک کال استروک برای کل باران به جای ۶۰ بار کال کردن!

      // حلقه‌های پاشش ظریف
      if (splashes.length > 0) {
        ctx.lineWidth = 0.75;
        for (var sIdx = splashes.length - 1; sIdx >= 0; sIdx--) {
          var sp = splashes[sIdx];
          ctx.strokeStyle = 'rgba(225, 245, 255, ' + sp.alpha + ')';
          ctx.beginPath();
          ctx.ellipse(sp.x, sp.y, sp.radius, sp.radius * 0.3, 0, 0, Math.PI * 2);
          ctx.stroke();
          sp.radius += 0.45;
          sp.alpha -= 0.06;
          if (sp.alpha <= 0) splashes.splice(sIdx, 1);
        }
      }

      if (state.type === 'storm') {
        if (timeTick > nextLightningTime) {
          createNaturalLightning();
          nextLightningTime = timeTick + 160 + Math.floor(Math.random() * 200);
        }
        if (activeLightningBolt) drawLightningBolt(activeLightningBolt);
      }
    }

    // ۲. رندر برف"""

js = re.sub(old_rain_pattern, new_rain_code, js, flags=re.DOTALL)

# In drawLightningBolt, remove heavy ctx.shadowBlur which causes major frame drops
js = js.replace("ctx.shadowBlur = 12;", "/* shadowBlur removed for 60fps */")

with open(path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Canvas optimized for buttery 60fps!")
