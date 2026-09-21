import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);

const info = await page.evaluate(() => {
  const out = [];
  document.querySelectorAll('.input-wrapper').forEach((w, idx) => {
    const input = w.querySelector('input');
    const icon = w.querySelector('.input-icon');
    const eye = w.querySelector('.toggle-password');
    const ir = input.getBoundingClientRect();
    const cs = getComputedStyle(input);
    const iconR = icon ? icon.getBoundingClientRect() : null;
    const eyeR = eye ? eye.getBoundingClientRect() : null;
    // در RTL متن از سمت راست شروع می‌شود
    const textStartX = ir.right - parseFloat(cs.paddingRight);
    out.push({
      field: input.name,
      input: { l: Math.round(ir.left), r: Math.round(ir.right) },
      padding: { right: cs.paddingRight, left: cs.paddingLeft },
      textStartX: Math.round(textStartX),
      icon: iconR ? { l: Math.round(iconR.left), r: Math.round(iconR.right), cls: icon.className } : null,
      iconOverlapsText: iconR ? (iconR.left < textStartX) : null,
      eye: eyeR ? { l: Math.round(eyeR.left), r: Math.round(eyeR.right) } : null,
      placeholder: input.placeholder,
    });
  });
  return out;
});
info.forEach(f => {
  console.log(`\n--- ${f.field} ---`);
  console.log('  جعبه ورودی:', JSON.stringify(f.input), '| فضا: راست', f.padding.right, '/ چپ', f.padding.left);
  console.log('  شروع متن (از راست):', f.textStartX);
  console.log('  آیکون:', JSON.stringify(f.icon));
  console.log('  ❗ آیکون روی متن می‌افتد:', f.iconOverlapsText);
  console.log('  آیکون چشم:', JSON.stringify(f.eye));
});
await browser.close();
