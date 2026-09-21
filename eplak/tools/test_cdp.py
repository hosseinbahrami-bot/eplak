import subprocess
import time
import json
import urllib.request
import websocket
import base64
import os

def run_tests():
    # 1. Start chromium
    chrome_proc = subprocess.Popen([
        '/usr/bin/chromium',
        '--headless',
        '--no-sandbox',
        '--disable-gpu',
        '--remote-debugging-port=9222',
        '--remote-allow-origins=*',
        '--window-size=390,844',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(1.5)

    try:
        # Get websocket debugger url
        req = urllib.request.urlopen('http://127.0.0.1:9222/json')
        tabs = json.loads(req.read().decode('utf-8'))
        ws_url = tabs[0]['webSocketDebuggerUrl']
        print("Connected to Chromium:", ws_url)

        ws = websocket.create_connection(ws_url)

        msg_id = 0
        def cdp_send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {'id': msg_id, 'method': method}
            if params:
                payload['params'] = params
            ws.send(json.dumps(payload))
            while True:
                resp = json.loads(ws.recv())
                if resp.get('id') == msg_id:
                    return resp.get('result', {})

        # Enable Page and Runtime
        cdp_send('Page.enable')
        cdp_send('Runtime.enable')

        # Navigate to app
        cdp_send('Page.navigate', {'url': 'http://127.0.0.1:8080/'})
        time.sleep(2)

        def eval_js(expr):
            res = cdp_send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            return res.get('result', {}).get('value')

        def take_screenshot(path):
            res = cdp_send('Page.captureScreenshot', {'format': 'png'})
            data = base64.b64decode(res['data'])
            with open(path, 'wb') as f:
                f.write(data)
            print(f"Captured {path}")

        # Simulate login if on login screen
        curr = eval_js("window.getCurrentActiveScreenId ? window.getCurrentActiveScreenId() : ''")
        print("Current screen:", curr)
        if curr == 'screen-login':
            eval_js("document.getElementById('loginPhoneInput').value = '09123456789'; sendOtp();")
            time.sleep(0.8)
            eval_js("document.querySelectorAll('.otp-box').forEach(b => b.value = '1'); verifyOtp();")
            time.sleep(1.5)

        # 1. Capture Home screen with ad banner
        eval_js("window.showScreen('screen-home');")
        time.sleep(1)
        take_screenshot('/home/user/eplak/home_ad_screen.png')

        # 2. Services screen (Persian)
        eval_js("window.showScreen('screen-services');")
        time.sleep(0.8)
        has_quick = eval_js("document.getElementById('screen-services').innerText.includes('دسترسی سریع')")
        print("Contains 'دسترسی سریع':", has_quick)
        take_screenshot('/home/user/eplak/services_square_fa.png')

        # 3. Open Tenders & Auctions
        eval_js("window.openServiceCategory('tenders');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_tenders_fa.png')

        # 4. Test goBack()
        eval_js("window.goBack();")
        time.sleep(0.6)
        screen_after_back = eval_js("window.getCurrentActiveScreenId()")
        print("Screen after goBack():", screen_after_back)

        # 5. Open Cemeteries
        eval_js("window.openServiceCategory('cemeteries');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_cemeteries_fa.png')

        # 6. Open Cemetery Tariff Modal
        eval_js("window.openServiceDetail('cem_tariffs');")
        time.sleep(0.6)
        eval_js("window.serviceAction('cem_tariffs');")
        time.sleep(0.6)
        take_screenshot('/home/user/eplak/services_cem_tariff_modal.png')

        # Close modal and go back to services
        eval_js("const m = document.getElementById('cemTariffModal'); if(m) m.remove(); window.goBack();")
        time.sleep(0.5)

        # 7. Switch language to English
        eval_js("window.i18n.setLanguage('en'); window.showScreen('screen-services');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_square_en.png')

        # 8. Open Cemeteries in English
        eval_js("window.openServiceCategory('cemeteries');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_cemeteries_en.png')

        # 9. Open Tenders in English
        eval_js("window.openServiceCategory('tenders');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_tenders_en.png')

        # 10. Open Tenders Detail in Persian
        eval_js("window.i18n.setLanguage('fa'); window.openServiceDetail('tnd_civil');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_detail_civil_fa.png')

        # 11. Open Cemetery Detail in English
        eval_js("window.i18n.setLanguage('en'); window.openServiceDetail('cem_buy');")
        time.sleep(0.8)
        take_screenshot('/home/user/eplak/services_detail_cem_buy_en.png')

        ws.close()
    finally:
        chrome_proc.terminate()
        chrome_proc.wait()

if __name__ == '__main__':
    run_tests()
