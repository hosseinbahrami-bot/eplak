import { chromium } from 'playwright';
const browser = await chromium.launch();

async function audit(w, h, theme, label) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
  page.on('requestfailed', r => errors.push('FAILED: ' + r.url().slice(0, 90) + ' :: ' + (r.failure()?.errorText || '')));

  await page.goto('http://127.0.0.1:8081/login.php', { waitUntil: 'networkidle' });
  await page.evaluate(t => { document.documentElement.setAttribute('data-theme', t); localStorage.setItem('eplak_admin_theme', t); }, theme);
  await page.waitForTimeout(1500);

  const info = await page.evaluate(() => {
    const out = { elements: [], docOverflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth };
    const sel = ['.login-box', '.brand', '.brand-logo', '.brand-name', '.brand-sub', '.divider', '.theme-toggle', 'form', '.btn-login', '.form-options', '.footer-links', '.version'];
    sel.forEach(s => {
      const el = document.querySelector(s);
      if (!el) { out.elements.push({ sel: s, missing: true }); return; }
      const r = el.getBoundingClientRect();
      out.elements.push({
        sel: s,
        x: Math.round(r.x), y: Math.round(r.y),
        w: Math.round(r.width), h: Math.round(r.height),
        visible: r.width > 0 && r.height > 0 && getComputedStyle(el).display !== 'none',
        outsideLeft: r.left < 0,
        outsideRight: r.right > window.innerWidth,
        fontFamily: s === '.brand-name' ? getComputedStyle(el).fontFamily.split(',')[0] : undefined,
      });
    });
    // بررسی آیکون‌های FontAwesome
    const icons = [...document.querySelectorAll('i.fas, i.fa-solid, i.fa')].map(i => {
      const r = i.getBoundingClientRect();
      return { cls: i.className, w: Math.round(r.width), h: Math.round(r.height) };
    });
    out.icons = icons;
    out.faLoaded = typeof window.FontAwesome !== 'undefined';
    return out;
  });

  console.log(`\n===== ${label} (${w}x${h}, ${theme}) =====`);
  console.log('  سرریز افقی صفحه:', info.docOverflowX);
  console.log('  FontAwesome بارگذاری شده:', info.faLoaded);
  info.elements.forEach(e => {
    if (e.missing) { console.log(`  ❌ ${e.sel}: وجود ندارد`); return; }
    const flags = [];
    if (!e.visible) flags.push('نامرئی');
    if (e.outsideLeft) flags.push('بیرون از چپ');
    if (e.outsideRight) flags.push('بیرون از راست');
    console.log(`  ${e.sel.padEnd(16)} x=${String(e.x).padStart(4)} y=${String(e.y).padStart(4)} ${String(e.w).padStart(4)}×${String(e.h).padStart(3)} ${flags.length ? '⚠️ ' + flags.join('، ') : '✅'}`);
  });
  console.log('  آیکون‌ها:', JSON.stringify(info.icons.slice(0, 6)));
  if (errors.length) console.log('  خطاها:', errors.slice(0, 4).join(' | '));

  await page.screenshot({ path: `/home/user/shots/LOGIN-${label}.png` });
  await ctx.close();
}

await audit(1440, 900, 'light', 'desktop-light');
await audit(1440, 900, 'dark', 'desktop-dark');
await audit(390, 844, 'light', 'mobile-light');
await audit(390, 844, 'dark', 'mobile-dark');
await browser.close();
