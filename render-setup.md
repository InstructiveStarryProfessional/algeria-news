# 🚀 دليل سريع لرفع البوت على Render

## ⚡ خطوات سريعة

### 1. رفع الكود إلى GitHub
```bash
git init
git add .
git commit -m "إعداد البوت للرفع على Render"
git branch -M main
git remote add origin https://github.com/username/repo-name.git
git push -u origin main
```

### 2. إنشاء خدمة على Render
1. اذهب إلى [dashboard.render.com](https://dashboard.render.com)
2. اضغط "New +" → "Web Service"
3. اربط مستودع GitHub
4. اختر المستودع

### 3. إعداد الخدمة
- **Name**: `algeria-news-bot`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### 4. إضافة متغيرات البيئة
| المتغير | القيمة |
|---------|--------|
| `TELEGRAM_BOT_TOKEN` | `your_bot_token_here` |
| `TELEGRAM_CHANNEL_ID` | `@your_channel` |
| `RENDER` | `true` |

### 5. تشغيل الخدمة
اضغط "Create Web Service" وانتظر حتى يصبح "Live"

## 🔧 الحصول على التوكن والقناة

### توكن البوت:
1. اذهب إلى @BotFather على تليجرام
2. أرسل `/newbot`
3. اتبع التعليمات
4. احفظ التوكن

### معرف القناة:
1. أنشئ قناة جديدة
2. أضف البوت كمدير
3. احصل على المعرف:
   - عامة: `@channel_name`
   - خاصة: `-1001234567890`

## ✅ التحقق من العمل
- اذهب إلى `https://your-app.onrender.com`
- يجب أن ترى رسالة "بوت أخبار الجزائر يعمل بنجاح!"

## 🆘 استكشاف الأخطاء
- راجع سجلات Render في قسم "Logs"
- تحقق من متغيرات البيئة
- تأكد من صحة التوكن ومعرف القناة

---
📖 للحصول على دليل مفصل، راجع `README_RENDER.md` 