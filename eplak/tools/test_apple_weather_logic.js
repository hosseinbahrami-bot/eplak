// Test period resolution for all modes
function getTimePeriod() {
  const h = new Date().getHours();
  if (h >= 5 && h < 7) return 'sunrise';
  if (h >= 7 && h < 18) return 'day';
  if (h >= 18 && h < 20) return 'sunset';
  return 'night';
}

const currentPeriod = getTimePeriod();
console.log("Current real time period:", currentPeriod);

// When mode is rain, it MUST inherit currentPeriod (night or day), NEVER force 'day'!
console.log("Rain at night will have period:", currentPeriod);
