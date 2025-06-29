# main.py

# ==================== بوت أخبار الجزائر - نقطة البداية ====================
# الملف الرئيسي لتشغيل بوت أخبار الجزائر

import asyncio
import logging
import sys
import os
from bot import main as bot_main

# ==================== إعدادات التسجيل ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==================== نقطة البداية الرئيسية ====================

if __name__ == "__main__":
    print("🤖 بدء تشغيل بوت أخبار الجزائر...")
    print("⚠️  اضغط Ctrl+C لإيقاف البوت")
    
    # التحقق من متغيرات البيئة المطلوبة
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ خطأ: متغير TELEGRAM_BOT_TOKEN غير محدد")
        sys.exit(1)
    
    if not os.getenv('TELEGRAM_CHANNEL_ID'):
        print("❌ خطأ: متغير TELEGRAM_CHANNEL_ID غير محدد")
        sys.exit(1)
    
    print("✅ تم التحقق من متغيرات البيئة")
    
    try:
        # تشغيل البوت الرئيسي
        bot_main()
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف البوت بواسطة المستخدم.")
    except Exception as e:
        logging.critical(f"❌ فشل تشغيل البوت بسبب خطأ فادح: {e}", exc_info=True)
        print(f"❌ خطأ فادح: {e}")
    finally:
        print("🔒 تم إغلاق البوت.")
        sys.exit(0)

# --- Self-ping keep_alive thread ---
import threading
import time
import requests
import os

def keep_alive():
    url = os.getenv('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
    interval = 30
    while True:
        try:
            res = requests.get(url)
            print(f"Pinged at {time.strftime('%Y-%m-%d %H:%M:%S')}, status: {res.status_code}")
        except Exception as e:
            print(f"Error pinging: {e}")
        time.sleep(interval)

threading.Thread(target=keep_alive, daemon=True).start()
