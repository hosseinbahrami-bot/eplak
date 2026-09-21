// Verify time-of-day logic
function getTimePeriod(hour) {
  if (hour >= 5 && hour < 7) return 'sunrise';
  if (hour >= 7 && hour < 18) return 'day';
  if (hour >= 18 && hour < 20) return 'sunset';
  return 'night';
}

const hours = [3, 6, 12, 19, 23];
hours.forEach(h => {
  console.log(`Hour ${h}:00 -> ${getTimePeriod(h)}`);
});
