package com.example.eplakfixed

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.media.AudioAttributes
import android.media.RingtoneManager
import android.net.Uri
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.work.Constraints
import androidx.work.CoroutineWorker
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URLEncoder
import java.util.concurrent.TimeUnit

/**
 * پشتیبان اعلان برای نسخه APK.
 * WebView فایل محلی نمی‌تواند Service Worker وب را اجرا کند؛ بنابراین APK
 * در پس‌زمینه اعلان‌های جدید را از همان API بررسی و با NotificationManager
 * سیستم‌عامل نمایش می‌دهد. نسخه PWA از Web Push واقعی استفاده می‌کند.
 */
class NotificationWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val preferences = applicationContext.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
        val phone = preferences.getString(KEY_PHONE, "")?.trim().orEmpty()
        if (phone.isEmpty()) return@withContext Result.success()
        if (!NotificationManagerCompat.from(applicationContext).areNotificationsEnabled()) {
            return@withContext Result.success()
        }

        try {
            val lastId = preferences.getLong(KEY_LAST_ID, 0L)
            val initialized = preferences.getBoolean(KEY_INITIALIZED, false)
            val url = API_BASE_URL + "/notifications.php?phone=" +
                URLEncoder.encode(phone, "UTF-8") + "&since_id=" + lastId
            val response = getJson(url)
            val items = response.optJSONArray("notifications") ?: return@withContext Result.success()
            var newestId = lastId

            for (index in 0 until items.length()) {
                val item = items.optJSONObject(index) ?: continue
                val id = item.optLong("id", 0L)
                if (id > newestId) newestId = id
                if (initialized && id > lastId) {
                    showNotification(
                        item.optString("title", "اعلان جدید"),
                        item.optString("body", "پیام جدیدی از شهرداری ورامین دریافت شد."),
                        id
                    )
                }
            }

            preferences.edit()
                .putLong(KEY_LAST_ID, newestId)
                .putBoolean(KEY_INITIALIZED, true)
                .apply()
            Result.success()
        } catch (_: Exception) {
            Result.retry()
        }
    }

    private fun getJson(url: String): JSONObject {
        val connection = (Uri.parse(url).toString().let { java.net.URL(it).openConnection() } as HttpURLConnection)
        connection.requestMethod = "GET"
        connection.connectTimeout = 12_000
        connection.readTimeout = 20_000
        connection.setRequestProperty("Accept", "application/json")
        return try {
            if (connection.responseCode !in 200..299) throw IllegalStateException("HTTP ${connection.responseCode}")
            JSONObject(connection.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() })
        } finally {
            connection.disconnect()
        }
    }

    private fun showNotification(title: String, body: String, id: Long) {
        showSystemNotification(applicationContext, title, body, id)
    }

    companion object {
        /** نمایش فوری از bridge جاوااسکریپت؛ در foreground هم اعلان سیستم است. */
        fun notifyNow(context: Context, title: String, body: String, id: Long) {
            val appContext = context.applicationContext
            if (!NotificationManagerCompat.from(appContext).areNotificationsEnabled()) return
            val preferences = appContext.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
            val previousId = preferences.getLong(KEY_LAST_ID, 0L)
            if (id <= previousId) return
            preferences.edit()
                .putLong(KEY_LAST_ID, id)
                .putBoolean(KEY_INITIALIZED, true)
                .apply()
            showSystemNotification(appContext, title, body, id)
        }

        private fun showSystemNotification(context: Context, title: String, body: String, id: Long) {
            val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            createChannel(manager)

            val intent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                putExtra(MainActivity.EXTRA_OPEN_NOTIFICATIONS, true)
            }
            val pendingIntent = PendingIntent.getActivity(
                context,
                id.toInt(),
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or pendingIntentFlags()
            )

            val notification = NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle(title)
                .setContentText(body)
                .setStyle(NotificationCompat.BigTextStyle().bigText(body))
                .setContentIntent(pendingIntent)
                .setAutoCancel(true)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setCategory(NotificationCompat.CATEGORY_MESSAGE)
                .setVibrate(longArrayOf(0, 250, 100, 250))
                .setDefaults(NotificationCompat.DEFAULT_SOUND)
                .build()

            manager.notify(id.toInt(), notification)
        }

        private fun createChannel(manager: NotificationManager) {
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
            if (manager.getNotificationChannel(CHANNEL_ID) != null) return

            val sound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            val attributes = AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                .build()
            val channel = NotificationChannel(CHANNEL_ID, "اعلان‌های ای‌پلاک", NotificationManager.IMPORTANCE_HIGH)
            channel.description = "اعلان‌های مهم شهرداری ورامین"
            channel.enableVibration(true)
            channel.vibrationPattern = longArrayOf(0, 250, 100, 250)
            channel.setSound(sound, attributes)
            manager.createNotificationChannel(channel)
        }

        private fun pendingIntentFlags(): Int =
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0

        // همان نشانی پیش‌فرضی که core/storage.js برای APK استفاده می‌کند.
        private const val API_BASE_URL = "https://eplak.ir/eplak-fixed/api"
        private const val PREFERENCES = "eplak_native_notifications"
        private const val KEY_PHONE = "phone"
        private const val KEY_LAST_ID = "last_id"
        private const val KEY_INITIALIZED = "initialized"
        private const val CHANNEL_ID = "eplak_announcements"
        private const val WORK_NAME = "eplak_notification_poll"

        fun setPhone(context: Context, phone: String) {
            val preferences = context.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
            // بازیابی session در شروع دوباره نباید cursor اعلان را از صفر کند؛
            // فقط ورود به حساب جدید/پس از logout باید baseline تازه بسازد.
            if (preferences.getString(KEY_PHONE, "") == phone) {
                schedule(context)
                return
            }
            preferences.edit()
                .putString(KEY_PHONE, phone)
                .putBoolean(KEY_INITIALIZED, false)
                .putLong(KEY_LAST_ID, 0L)
                .apply()
            schedule(context)
            WorkManager.getInstance(context).enqueueUniqueWork(
                "${WORK_NAME}_now",
                ExistingWorkPolicy.REPLACE,
                OneTimeWorkRequestBuilder<NotificationWorker>().build()
            )
        }

        fun clearPhone(context: Context) {
            context.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE).edit().clear().apply()
            WorkManager.getInstance(context).cancelUniqueWork(WORK_NAME)
            WorkManager.getInstance(context).cancelUniqueWork("${WORK_NAME}_now")
        }

        fun schedule(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()
            val request = PeriodicWorkRequestBuilder<NotificationWorker>(15, TimeUnit.MINUTES)
                .setConstraints(constraints)
                .build()
            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                WORK_NAME,
                ExistingPeriodicWorkPolicy.UPDATE,
                request
            )
        }
    }
}
