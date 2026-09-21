import re

path = '/home/user/eplak/eplak-fixed/core/i18n.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update service_track_report_sub
content = content.replace(
    "'service_track_report_sub': 'وضعیت گزارش‌ها',",
    "'service_track_report_sub': 'وضعیت گزارش‌ها و تیکت‌ها',"
)
content = content.replace(
    "'service_track_report_sub': 'Status of reports',",
    "'service_track_report_sub': 'Status of reports & tickets',"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[2] i18n.js updated successfully!")
