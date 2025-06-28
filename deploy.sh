#!/bin/bash

# سكريبت نشر بوت أخبار الجزائر على Render

echo "🚀 بدء عملية نشر بوت أخبار الجزائر..."

# التحقق من وجود Git
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت. يرجى تثبيت Git أولاً."
    exit 1
fi

# التحقق من وجود ملفات مطلوبة
required_files=("bot.py" "app.py" "requirements.txt" "config.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ملف $file غير موجود"
        exit 1
    fi
done

echo "✅ تم التحقق من الملفات المطلوبة"

# إضافة جميع الملفات إلى Git
echo "📁 إضافة الملفات إلى Git..."
git add .

# إنشاء commit
echo "💾 إنشاء commit..."
git commit -m "إعداد البوت للنشر على Render - $(date)"

# دفع التغييرات
echo "🚀 دفع التغييرات إلى GitHub..."
git push origin main

echo "✅ تم إرسال التحديثات بنجاح!"
echo ""
echo "📋 الخطوات التالية:"
echo "1. اذهب إلى dashboard.render.com"
echo "2. أنشئ خدمة ويب جديدة"
echo "3. اربط مستودع GitHub"
echo "4. أضف متغيرات البيئة:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - TELEGRAM_CHANNEL_ID"
echo "5. اضغط على 'Create Web Service'"
echo ""
echo "📖 راجع ملف README_RENDER.md للحصول على تعليمات مفصلة" 