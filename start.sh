#!/bin/bash

# سكريبت بدء تشغيل بوت أخبار الجزائر على Render

echo "🚀 بدء تشغيل بوت أخبار الجزائر..."

# التحقق من وجود متغيرات البيئة المطلوبة
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ خطأ: متغير TELEGRAM_BOT_TOKEN غير محدد"
    exit 1
fi

if [ -z "$TELEGRAM_CHANNEL_ID" ]; then
    echo "❌ خطأ: متغير TELEGRAM_CHANNEL_ID غير محدد"
    exit 1
fi

echo "✅ تم التحقق من متغيرات البيئة"

# إنشاء مجلد التخزين المؤقت إذا لم يكن موجوداً
mkdir -p /tmp/cache

# تشغيل البوت
echo "🤖 تشغيل البوت..."
python main.py 