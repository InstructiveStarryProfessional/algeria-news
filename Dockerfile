# استخدام Python 3.11
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات أولاً لتحسين التخزين المؤقت
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# إنشاء مجلد التخزين المؤقت
RUN mkdir -p /tmp/cache

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV RENDER=true

# فتح المنفذ (مطلوب لـ Render)
EXPOSE 8000

# تشغيل البوت
CMD ["python", "main.py"] 