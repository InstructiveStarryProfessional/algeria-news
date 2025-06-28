# app.py - ملف للتوافق مع Render كخدمة ويب

import os
import threading
import time
from flask import Flask, jsonify
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# متغير للتحكم في حالة البوت
bot_running = False
bot_thread = None

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return jsonify({
        "status": "running",
        "bot_status": "running" if bot_running else "stopped",
        "message": "بوت أخبار الجزائر يعمل بنجاح! 🚀"
    })

@app.route('/health')
def health():
    """فحص صحة الخدمة"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "bot_running": bot_running
    })

@app.route('/start-bot')
def start_bot():
    """تشغيل البوت"""
    global bot_running, bot_thread
    
    if not bot_running:
        bot_running = True
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        return jsonify({"status": "success", "message": "تم تشغيل البوت بنجاح"})
    else:
        return jsonify({"status": "already_running", "message": "البوت يعمل بالفعل"})

def run_bot():
    """تشغيل البوت في خيط منفصل"""
    global bot_running
    try:
        from bot import main as bot_main
        logger.info("بدء تشغيل البوت...")
        bot_main()
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}")
    finally:
        bot_running = False

if __name__ == '__main__':
    # تشغيل البوت تلقائياً عند بدء التطبيق
    if os.getenv('RENDER') == 'true':
        # على Render، نبدأ البوت في خيط منفصل
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        bot_running = True
        logger.info("تم بدء البوت في خيط منفصل")
    
    # تشغيل خادم Flask
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"بدء تشغيل خادم Flask على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 