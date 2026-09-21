#!/usr/bin/env python3
"""
E2E Integration Test: Real-time Citizen App <-> Admin Panel & MariaDB Backend
"""
import urllib.request
import urllib.parse
import json
import http.cookiejar
import sys

BASE_URL = "http://127.0.0.1:8080"

def log(msg):
    print(f"[TEST] {msg}")

def test_flow():
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    # Step 1: Citizen logs in / registers
    phone = "09359876543"
    name = "سهراب سپهری"
    address = "ورامین، خیابان ۱۵ خرداد، کوچه بهار"
    log(f"1. Testing Citizen login & profile sync for {phone} ({name})...")

    user_payload = json.dumps({"phone": phone, "name": name, "address": address, "nid": "0412345678"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/api/users.php", data=user_payload, headers={"Content-Type": "application/json"})
    with opener.open(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert data.get("success") is True, f"User registration failed: {data}"
        log(f"   -> Success! User registered in DB: id={data['user']['id']}, name={data['user']['name']}")

    # Step 2: Verify user appears in Admin API
    log("2. Admin login & verifying real-time user detection in api_live.php...")
    session_id = ''
    with opener.open(f"{BASE_URL}/admin/login.php?autologin=1") as resp:
        url = resp.geturl()
        if 'eplak_admin=' in url:
            session_id = url.split('eplak_admin=')[1].split('&')[0]
        for h in resp.headers.get_all('Set-Cookie', []):
            if 'eplak_admin=' in h:
                session_id = h.split('eplak_admin=')[1].split(';')[0]

    with opener.open(f"{BASE_URL}/admin/api_live.php?eplak_admin=" + session_id) as resp:
        live_data = json.loads(resp.read().decode("utf-8"))
        assert live_data.get("success") is True, f"Admin live pulse failed: {live_data}"
        log(f"   -> Success! Total users in DB: {live_data['users_count']}, Latest user: {live_data['latest_user']['name']}")

    # Step 3: Citizen submits a report
    log("3. Testing Citizen report submission...")
    report_payload = json.dumps({
        "userPhone": phone,
        "title": "تعمیر روشنایی پارک ۱۵ خرداد",
        "description": "پایه‌های روشنایی ضلع جنوبی خاموش هستند و نیاز به تعویض لامپ دارند.",
        "category": "روشنایی",
        "department": "معاونت خدمات شهری",
        "subDepartment": "زیباسازی و روشنایی",
        "location": "ضلع جنوبی پارک ۱۵ خرداد"
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/api/reports.php", data=report_payload, headers={"Content-Type": "application/json"})
    report_id = None
    tracking_code = None
    with opener.open(req) as resp:
        rep_data = json.loads(resp.read().decode("utf-8"))
        assert rep_data.get("success") is True, f"Report submit failed: {rep_data}"
        report_id = rep_data["id"]
        tracking_code = rep_data["tracking_code"]
        log(f"   -> Success! Report submitted with ID={report_id}, Tracking Code={tracking_code}")

    # Step 4: Verify report shows up in admin live pulse
    log("4. Verifying new report in Admin live pulse...")
    with opener.open(f"{BASE_URL}/admin/api_live.php?eplak_admin=" + session_id) as resp:
        live_data = json.loads(resp.read().decode("utf-8"))
        assert live_data["latest_report"]["id"] == report_id, f"Latest report mismatch: {live_data}"
        log(f"   -> Success! Admin live pulse reports: {live_data['latest_report']['title']} (Pending: {live_data['pending_count']})")

    # Step 5: Admin broadcasts an announcement / push notification
    log("5. Testing Admin broadcast announcement to citizens...")
    notif_post_data = urllib.parse.urlencode({
        "title": "هشدار وقوع تندباد و بارندگی",
        "body": "طبق اطلاعیه هواشناسی، از پارک خودرو زیر درختان کهنسال خودداری نمایید.",
        "target": "all"
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/admin/notifications.php?eplak_admin=" + session_id, data=notif_post_data)
    with opener.open(req) as resp:
        log("   -> Broadcast notification posted by admin.")

    # Step 6: Citizen app retrieves broadcast announcement in real-time
    log("6. Verifying citizen app receives the broadcast push notification...")
    with opener.open(f"{BASE_URL}/api/notifications.php?phone={phone}") as resp:
        notif_data = json.loads(resp.read().decode("utf-8"))
        assert notif_data.get("success") is True, f"Notification fetch failed: {notif_data}"
        titles = [n["title"] for n in notif_data["notifications"]]
        assert "هشدار وقوع تندباد و بارندگی" in titles, f"Broadcast not received by citizen: {titles}"
        log(f"   -> Success! Citizen received notification: '{titles[0]}'")

    # Step 7: Admin replies to the report and marks as done
    log("7. Admin replies to report and marks as done...")
    reply_post_data = urllib.parse.urlencode({
        "status": "done",
        "reply": "اکیپ روشنایی اعزام شد و تمامی لامپ‌های پایه‌های جنوبی تعویض و رفع نقص گردید."
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/admin/report_detail.php?id={report_id}", data=reply_post_data)
    with opener.open(req) as resp:
        log("   -> Admin reply and status update saved.")

    # Step 8: Verifying citizen receives automated report status update notification
    log("8. Verifying citizen receives report status notification...")
    with opener.open(f"{BASE_URL}/api/notifications.php?phone={phone}") as resp:
        notif_data = json.loads(resp.read().decode("utf-8"))
        latest_title = notif_data["notifications"][0]["title"]
        assert "به‌روزرسانی گزارش" in latest_title, f"Status update notif not found: {latest_title}"
        log(f"   -> Success! Citizen received update: '{latest_title}'")
        log(f"      Body: {notif_data['notifications'][0]['body']}")

    # Step 9: Citizen submits a ticket and verifies it appears in Admin Tickets
    log("9. Testing Citizen ticket submission directly to Admin panel...")
    ticket_payload = json.dumps({
        "userPhone": phone,
        "title": "درخواست نصب سرعت‌گیر در بلوار باهنر",
        "description": "به دلیل سرعت بالای وسایل نقلیه و خطر تصادف عابرین، لطفاً سرعت‌گیر استاندارد نصب شود.",
        "category": "معاونت حمل‌ونقل و ترافیک",
        "department": "معاونت حمل‌ونقل و ترافیک",
        "priority": "high"
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/api/tickets.php", data=ticket_payload, headers={"Content-Type": "application/json"})
    ticket_id = None
    ticket_code = None
    with opener.open(req) as resp:
        t_data = json.loads(resp.read().decode("utf-8"))
        assert t_data.get("success") is True, f"Ticket submit failed: {t_data}"
        ticket_id = t_data["id"]
        ticket_code = t_data["tracking_code"]
        log(f"   -> Success! Ticket created: ID={ticket_id}, Code={ticket_code}")

    # Verify ticket in Admin Tickets list
    log("10. Verifying ticket in Admin Panel (/admin/tickets.php)...")
    with opener.open(f"{BASE_URL}/admin/tickets.php?eplak_admin=" + session_id) as resp:
        admin_tickets_html = resp.read().decode("utf-8")
        assert "درخواست نصب سرعت‌گیر در بلوار باهنر" in admin_tickets_html, "Ticket title not found in admin tickets list"
        assert phone in admin_tickets_html, "User phone not found in admin tickets list"
        log("   -> Success! Ticket is directly visible in Admin tickets table.")

    # Admin replies to ticket
    log("11. Admin replies to ticket in ticket_detail.php...")
    ticket_reply_data = urllib.parse.urlencode({
        "title": "درخواست نصب سرعت‌گیر در بلوار باهنر",
        "description": "به دلیل سرعت بالای وسایل نقلیه و خطر تصادف عابرین، لطفاً سرعت‌گیر استاندارد نصب شود.",
        "user_phone": phone,
        "category": "معاونت حمل‌ونقل و ترافیک",
        "department": "معاونت حمل‌ونقل و ترافیک",
        "priority": "high",
        "status": "in_progress",
        "reply": "درخواست شما به کارگروه ایمنی ترافیک ارجاع شد و بازدید میدانی در دستور کار قرار گرفت."
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/admin/ticket_detail.php?id={ticket_id}&eplak_admin=" + session_id, data=ticket_reply_data)
    with opener.open(req) as resp:
        log("   -> Admin reply to ticket saved.")

    # Citizen fetches tickets and sees admin reply
    log("12. Verifying citizen sees admin reply for their ticket...")
    with opener.open(f"{BASE_URL}/api/tickets.php?phone={phone}") as resp:
        user_tickets = json.loads(resp.read().decode("utf-8"))
        assert user_tickets.get("success") is True, f"Tickets fetch failed: {user_tickets}"
        matched = [t for t in user_tickets["tickets"] if t["id"] == ticket_id or t.get("code") == ticket_code]
        assert len(matched) > 0, "Submitted ticket not found in citizen tickets"
        assert "کارگروه ایمنی ترافیک" in matched[0]["reply"], f"Admin reply missing: {matched[0]}"
        log(f"   -> Success! Citizen received admin reply: '{matched[0]['reply']}'")
        log(f"      Status: {matched[0]['status']}")

    log("\n=======================================================")
    log("ALL REAL-TIME INTEGRATION TESTS PASSED SUCCESSFULLY! 🚀")
    log("=======================================================")


if __name__ == "__main__":
    test_flow()
