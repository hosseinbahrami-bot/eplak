package com.example.eplakfixed

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private var openNotificationsAfterLoad = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        openNotificationsAfterLoad = intent.getBooleanExtra(EXTRA_OPEN_NOTIFICATIONS, false)
        setContentView(R.layout.activity_main)
        NotificationWorker.schedule(this)

        webView = findViewById<WebView>(R.id.myWebView)
        val webSettings = webView.settings

        // فعال‌سازی جاوااسکریپت و ذخیره‌سازی
        webSettings.javaScriptEnabled = true
        webSettings.domStorageEnabled = true
        webSettings.databaseEnabled = true
        webSettings.javaScriptCanOpenWindowsAutomatically = true

        // دسترسی به فایل‌ها
        webSettings.allowFileAccess = true
        webSettings.allowContentAccess = true
        @Suppress("DEPRECATION")
        webSettings.allowFileAccessFromFileURLs = true
        // دسترسی «universal» از file:// غیرفعال: در صورت هر XSS داخل وب‌ویو، امکان خواندن
        // فایل‌های محلی/داده‌های اپ از بین می‌رود. اپ برای کارکرد به آن نیاز ندارد.
        @Suppress("DEPRECATION")
        webSettings.allowUniversalAccessFromFileURLs = false

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            webSettings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }

        // دیباگ وب‌ویو فقط در بیلد Debug (در نسخه‌ی انتشار، امکان اتصال DevTools به اپ بسته می‌شود)
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)

        // پل ارتباطی جاوااسکریپت و اندروید برای خروج هماهنگ و کنترل سخت‌افزاری
        webView.addJavascriptInterface(WebAppInterface(this), "AndroidApp")

        // اتصال کلاینت‌ها
        webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView, url: String) {
                super.onPageFinished(view, url)
                if (openNotificationsAfterLoad) {
                    openNotificationsAfterLoad = false
                    view.evaluateJavascript("if (typeof showScreen === 'function') showScreen('screen-notifications');", null)
                }
            }
        }
        webView.webChromeClient = WebChromeClient()

        // مدیریت هوشمند دکمه بازگشت (Hardware Back Button / Gesture Back)
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                // ارسال رویداد بازگشت به لایه مدیریت تاریخچه در جاوااسکریپت
                webView.evaluateJavascript(
                    """
                    (function() {
                        if (typeof window.handleAppBack === 'function') {
                            return window.handleAppBack(false);
                        } else if (typeof window.goBack === 'function') {
                            return window.goBack();
                        }
                        return false;
                    })();
                    """.trimIndent()
                ) { result ->
                    val handled = result == "true"
                    // اگر در جاوااسکریپت هندل نشد (یا وب‌ویو هنوز لود نشده بود)
                    if (!handled) {
                        if (webView.canGoBack()) {
                            webView.goBack()
                        } else {
                            isEnabled = false
                            onBackPressedDispatcher.onBackPressed()
                            isEnabled = true
                        }
                    }
                }
            }
        })

        // بارگذاری فایل HTML
        webView.loadUrl("file:///android_asset/index.html")
    }

    override fun onNewIntent(intent: android.content.Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        if (intent.getBooleanExtra(EXTRA_OPEN_NOTIFICATIONS, false) && ::webView.isInitialized) {
            openNotificationsAfterLoad = true
            webView.post {
                if (openNotificationsAfterLoad) {
                    openNotificationsAfterLoad = false
                    webView.evaluateJavascript("if (typeof showScreen === 'function') showScreen('screen-notifications');", null)
                }
            }
        }
    }

    companion object {
        const val EXTRA_OPEN_NOTIFICATIONS = "open_notifications"
    }

    class WebAppInterface(private val activity: AppCompatActivity) {
        @JavascriptInterface
        fun exitApp() {
            activity.runOnUiThread {
                activity.finish()
            }
        }

        @JavascriptInterface
        fun setCurrentPhone(phone: String) {
            if (phone.isBlank()) {
                NotificationWorker.clearPhone(activity)
                return
            }
            NotificationWorker.setPhone(activity, phone)
            requestNotificationPermission()
        }

        @JavascriptInterface
        fun showNotification(title: String, body: String, id: String) {
            val notificationId = id.toLongOrNull() ?: System.currentTimeMillis()
            NotificationWorker.notifyNow(activity, title, body, notificationId)
        }

        private fun requestNotificationPermission() {
            activity.runOnUiThread {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU
                    && activity.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
                ) {
                    activity.requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), 4107)
                }
            }
        }
    }
}
