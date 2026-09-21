const cloudSvgDay = `
<svg class="apple-cloud-svg ac-svg-1" viewBox="0 0 240 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="cloudGradDay1" cx="45%" cy="30%" r="65%">
      <stop offset="0%" stop-color="rgba(255,255,255,0.94)"/>
      <stop offset="60%" stop-color="rgba(240,248,255,0.72)"/>
      <stop offset="90%" stop-color="rgba(210,225,245,0.3)"/>
      <stop offset="100%" stop-color="rgba(190,210,235,0)"/>
    </radialGradient>
    <filter id="cloudBlur1" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>
  <g filter="url(#cloudBlur1)">
    <ellipse cx="65" cy="55" rx="45" ry="24" fill="url(#cloudGradDay1)"/>
    <ellipse cx="118" cy="45" rx="55" ry="30" fill="url(#cloudGradDay1)"/>
    <ellipse cx="165" cy="54" rx="42" ry="22" fill="url(#cloudGradDay1)"/>
    <ellipse cx="92" cy="34" rx="34" ry="24" fill="rgba(255,255,255,0.9)"/>
    <ellipse cx="136" cy="36" rx="36" ry="24" fill="rgba(255,255,255,0.88)"/>
  </g>
</svg>`;
console.log("SVG cloud length:", cloudSvgDay.length);
