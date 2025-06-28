# config.py

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# ==================== إعدادات التليجرام ====================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# معالجة معرف القناة
if TELEGRAM_CHANNEL_ID and TELEGRAM_CHANNEL_ID.startswith('@'):
    # إذا كان المعرف يبدأ بـ @، نحتاج لتحويله إلى معرف رقمي
    # سنستخدم المعرف كما هو وسيتم التحويل في البوت
    pass

# التحقق من وجود المتغيرات الأساسية
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN غير موجود في متغيرات البيئة")
if not TELEGRAM_CHANNEL_ID:
    raise ValueError("❌ TELEGRAM_CHANNEL_ID غير موجود في متغيرات البيئة")

# ==================== إعدادات قاعدة البيانات ====================
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///news.db')

# ==================== إعدادات التخزين المؤقت ====================
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
CACHE_DURATION = int(os.getenv('CACHE_DURATION', '3600'))  # ساعة واحدة
CACHE_DIR = os.getenv('CACHE_DIR', 'cache')

# ==================== إعدادات الشبكة ====================
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))  # 30 ثانية
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))  # 3 محاولات
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '5'))  # 5 ثوان