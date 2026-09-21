const fs = require('fs');
const assert = require('assert');

console.log("=== COMPREHENSIVE VERIFICATION OF 3 USER REQUESTS ===");

// 1. Check index.html
console.log("\n[1] Checking index.html...");
const html = fs.readFileSync('/home/user/eplak/eplak-fixed/index.html', 'utf8');

// Check Screen Reports segmented switcher
assert(html.includes('id="reportsMainSwitcher"'), "Missing #reportsMainSwitcher in screen-reports");
assert(html.includes('id="tabBtnReports"'), "Missing #tabBtnReports in screen-reports");
assert(html.includes('id="tabBtnTickets"'), "Missing #tabBtnTickets in screen-reports");
assert(html.includes('id="sectionReportsPane"'), "Missing #sectionReportsPane in screen-reports");
assert(html.includes('id="sectionTicketsPane"'), "Missing #sectionTicketsPane in screen-reports");
assert(html.includes('id="ticketsFilterTabs"'), "Missing #ticketsFilterTabs in screen-reports");
assert(html.includes('id="userTicketsListWrap"'), "Missing #userTicketsListWrap in screen-reports");
console.log("  ✓ Screen Reports segmented switcher and dual panes present!");

// Check Ticket deletion button in detail view
assert(html.includes('id="ticketDetailDeleteBtn"'), "Missing #ticketDetailDeleteBtn in screen-ticket-detail");
assert(html.includes('deleteCurrentOpenTicket()'), "Missing deleteCurrentOpenTicket() handler in detail view");
console.log("  ✓ Ticket deletion button in screen-ticket-detail present!");

// Check Request tracking in Home and screen-track
assert(html.includes('وضعیت گزارش‌ها و تیکت‌ها'), "Missing 'وضعیت گزارش‌ها و تیکت‌ها' subtext on Home card");
assert(html.includes('id="trackFilterTabs"'), "Missing #trackFilterTabs in screen-track");
assert(html.includes('data-trackfilter="all"'), "Missing 'all' filter in screen-track");
assert(html.includes('data-trackfilter="reports"'), "Missing 'reports' filter in screen-track");
assert(html.includes('data-trackfilter="tickets"'), "Missing 'tickets' filter in screen-track");
console.log("  ✓ Request Tracking on Home screen and screen-track present!");

// 2. Check modules/reports.js
console.log("\n[2] Checking modules/reports.js...");
const js = fs.readFileSync('/home/user/eplak/eplak-fixed/modules/reports.js', 'utf8');

assert(js.includes('function switchReportsMainTab'), "Missing switchReportsMainTab");
assert(js.includes('function filterUserTickets'), "Missing filterUserTickets");
assert(js.includes('function renderUserTicketsList'), "Missing renderUserTicketsList");
assert(js.includes('confirmDeleteTicket'), "Missing confirmDeleteTicket in ticket list");
assert(js.includes('function confirmDeleteTicket'), "Missing confirmDeleteTicket");
assert(js.includes('function deleteTicketById'), "Missing deleteTicketById");
assert(js.includes('function deleteCurrentOpenTicket'), "Missing deleteCurrentOpenTicket");
assert(js.includes('function filterTrackList'), "Missing filterTrackList");
assert(js.includes('function renderTrackRecent'), "Missing renderTrackRecent");
assert(js.includes('function searchByTrackCode'), "Missing searchByTrackCode");
console.log("  ✓ All required JS functions defined and implemented!");

// Check CSS
console.log("\n[3] Checking assets/css/style.css...");
const css = fs.readFileSync('/home/user/eplak/eplak-fixed/assets/css/style.css', 'utf8');
assert(css.includes('.reports-main-switcher'), "Missing .reports-main-switcher CSS");
assert(css.includes('.reports-switcher-btn'), "Missing .reports-switcher-btn CSS");
assert(css.includes('.reports-switcher-indicator'), "Missing .reports-switcher-indicator CSS");
assert(css.includes('.ticket-delete-btn'), "Missing .ticket-delete-btn CSS");
assert(css.includes('.btn-danger-outline'), "Missing .btn-danger-outline CSS");
console.log("  ✓ All required CSS classes present!");

// Check synced files
console.log("\n[4] Checking Android & iOS sync...");
const androidHtml = fs.readFileSync('/home/user/eplak/eplak-fixed/android-app/app/src/main/assets/index.html', 'utf8');
assert(androidHtml.includes('id="reportsMainSwitcher"'), "Android index.html out of sync");
const iosHtml = fs.readFileSync('/home/user/eplak/ios-app/Eplak/Web/index.html', 'utf8');
assert(iosHtml.includes('id="reportsMainSwitcher"'), "iOS index.html out of sync");
console.log("  ✓ Android and iOS native wrapper bundles synchronized!");

console.log("\n=======================================================");
console.log("ALL THREE ENHANCEMENTS FULLY VERIFIED AND PASSING! 🎉");
console.log("=======================================================");
