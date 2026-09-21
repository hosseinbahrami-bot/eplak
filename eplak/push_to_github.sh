#!/usr/bin/env bash
# اسکریپت ارسال مستقیم تغییرات سامانه به گیت‌هاب (Push to GitHub)

if [ -z "$1" ]; then
  echo "لطفاً آدرس ریپازیتوری گیت‌هاب خود را وارد نمایید."
  echo "نحوه استفاده:"
  echo "  ./push_to_github.sh https://github.com/USERNAME/REPO.git"
  echo "یا در صورت استفاده از توکن دسترسی (Personal Access Token):"
  echo "  ./push_to_github.sh https://ghp_TOKEN@github.com/USERNAME/REPO.git"
  exit 1
fi

REMOTE_URL="$1"
git remote remove github 2>/dev/null
git remote add github "$REMOTE_URL"
git branch -M main

echo "در حال ارسال تغییرات به ریپازیتوری گیت‌هاب..."
git push -u github main --force

if [ $? -eq 0 ]; then
  echo "✓ تمامی تغییرات و کامیت‌ها با موفقیت در گیت‌هاب آپدیت شدند."
else
  echo "✗ خطا در ارسال به گیت‌هاب. لطفاً دسترسی توکن یا آدرس ریپازیتوری را بررسی کنید."
fi
