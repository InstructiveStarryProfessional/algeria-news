#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تشخيص لمشاكل إرسال الرسائل إلى قناة التليجرام
"""

import asyncio
import logging
import os
from telegram import Bot
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

# إعداد التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def get_channel_id(bot, channel_username):
    """تحويل معرف القناة من @username إلى معرف رقمي"""
    try:
        if channel_username.startswith('@'):
            try:
                chat = await bot.get_chat(channel_username)
                logger.info(f"✅ تم تحويل معرف القناة {channel_username} إلى {chat.id}")
                return str(chat.id)
            except Exception as chat_error:
                logger.warning(f"⚠️ فشل في تحويل معرف القناة {channel_username}: {chat_error}")
                return channel_username
        return channel_username
    except Exception as e:
        logger.error(f"❌ خطأ في تحويل معرف القناة {channel_username}: {e}")
        return channel_username

async def test_telegram_connection():
    """اختبار الاتصال بقناة التليجرام"""
    logger.info("🔍 بدء اختبار الاتصال بقناة التليجرام...")
    
    # التحقق من وجود المتغيرات
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN غير محدد")
        return False
    
    if not TELEGRAM_CHANNEL_ID:
        logger.error("❌ TELEGRAM_CHANNEL_ID غير محدد")
        return False
    
    logger.info(f"✅ TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN[:10]}...")
    logger.info(f"✅ TELEGRAM_CHANNEL_ID: {TELEGRAM_CHANNEL_ID}")
    
    try:
        # إنشاء كائن البوت
        bot = Bot(TELEGRAM_BOT_TOKEN)
        
        # اختبار معلومات البوت
        bot_info = await bot.get_me()
        logger.info(f"✅ معلومات البوت: {bot_info.first_name} (@{bot_info.username})")
        
        # تحويل معرف القناة
        channel_id = await get_channel_id(bot, TELEGRAM_CHANNEL_ID)
        logger.info(f"📢 معرف القناة النهائي: {channel_id}")
        
        # اختبار إرسال رسالة بسيطة
        test_message = "🧪 *اختبار الاتصال*\n\nهذه رسالة اختبار من بوت أخبار الجزائر\n\n✅ إذا وصلتك هذه الرسالة، فالاتصال يعمل بشكل صحيح"
        
        logger.info("📤 محاولة إرسال رسالة اختبار...")
        await bot.send_message(
            chat_id=channel_id,
            text=test_message,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("✅ تم إرسال رسالة الاختبار بنجاح!")
        
        # اختبار إرسال رسالة مع صورة
        logger.info("📤 محاولة إرسال رسالة مع صورة...")
        await bot.send_photo(
            chat_id=channel_id,
            photo="https://via.placeholder.com/400x200/0066cc/ffffff?text=Test+Image",
            caption="🖼️ *اختبار الصورة*\n\nهذه صورة اختبار من بوت أخبار الجزائر",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("✅ تم إرسال رسالة مع صورة بنجاح!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ فشل في اختبار الاتصال: {e}")
        
        # تحليل نوع الخطأ
        error_msg = str(e).lower()
        if 'chat not found' in error_msg:
            logger.error("🔍 المشكلة: القناة غير موجودة أو معرف القناة خاطئ")
            logger.error("💡 الحلول:")
            logger.error("   1. تأكد من أن البوت مشرف في القناة")
            logger.error("   2. تأكد من صحة معرف القناة")
            logger.error("   3. جرب استخدام معرف رقمي بدلاً من @username")
        elif 'bot was blocked' in error_msg:
            logger.error("🔍 المشكلة: البوت محظور من القناة")
        elif 'forbidden' in error_msg:
            logger.error("🔍 المشكلة: البوت ليس لديه صلاحية الكتابة في القناة")
            logger.error("💡 الحل: أضف البوت كمشرف في القناة مع صلاحية إرسال الرسائل")
        elif 'unauthorized' in error_msg:
            logger.error("🔍 المشكلة: رمز البوت غير صحيح")
        else:
            logger.error(f"🔍 خطأ غير معروف: {e}")
        
        return False

async def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء تشخيص مشاكل التليجرام...")
    
    success = await test_telegram_connection()
    
    if success:
        logger.info("🎉 جميع الاختبارات نجحت! البوت جاهز للعمل.")
    else:
        logger.error("❌ فشل في اختبار الاتصال. راجع الأخطاء أعلاه.")
    
    logger.info("🔚 انتهاء التشخيص.")

if __name__ == "__main__":
    asyncio.run(main()) 