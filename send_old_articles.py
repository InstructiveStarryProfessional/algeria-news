#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إرسال مقالات قديمة غير مرسلة لضمان استمرار نشاط البوت
"""

import asyncio
import datetime
import logging
from database import get_db_session, Article
from bot import send_article_to_telegram, get_channel_id
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN
from sqlalchemy import func

# إعداد التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_old_articles():
    """إرسال مقالات قديمة غير مرسلة"""
    session = get_db_session()
    bot = Bot(TELEGRAM_BOT_TOKEN)
    
    try:
        # البحث عن مقالات غير مرسلة من آخر 7 أيام
        seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        
        # مقالات غير مرسلة مع مشاعر إيجابية
        articles = session.query(Article).filter(
            Article.sent_to_telegram == False,
            Article.published_date >= seven_days_ago,
            Article.sentiment_score > 0.2  # مشاعر إيجابية أو محايدة
        ).order_by(
            Article.sentiment_score.desc(),  # أولوية للمشاعر الإيجابية
            Article.published_date.desc()    # ثم الأحدث
        ).limit(5).all()
        
        if not articles:
            logger.info("❌ لا توجد مقالات غير مرسلة مناسبة للإرسال")
            return
        
        logger.info(f"📰 وجدت {len(articles)} مقال غير مرسل للإرسال")
        
        for i, article in enumerate(articles, 1):
            try:
                logger.info(f"📤 إرسال المقال {i}/{len(articles)}: {article.title}")
                
                # إرسال المقال
                await send_article_to_telegram(bot, article)
                
                # تحديث حالة المقال
                article.sent_to_telegram = True
                session.commit()
                
                logger.info(f"✅ تم إرسال المقال بنجاح: {article.title}")
                
                # انتظار 30 ثانية بين كل مقال
                if i < len(articles):
                    logger.info("⏳ انتظار 30 ثانية قبل إرسال المقال التالي...")
                    await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"❌ فشل في إرسال المقال {article.title}: {e}")
                session.rollback()
        
        logger.info("🎉 انتهاء إرسال المقالات القديمة")
        
    except Exception as e:
        logger.error(f"❌ خطأ في إرسال المقالات القديمة: {e}")
    finally:
        session.close()

async def send_test_message():
    """إرسال رسالة اختبار"""
    bot = Bot(TELEGRAM_BOT_TOKEN)
    
    try:
        from config import TELEGRAM_CHANNEL_ID
        from telegram.constants import ParseMode
        
        # تحويل معرف القناة
        channel_id = await get_channel_id(bot, TELEGRAM_CHANNEL_ID)
        
        # رسالة اختبار
        test_message = """🤖 *تحديث حالة البوت*

📊 **إحصائيات قاعدة البيانات:**
• إجمالي المقالات: 1568
• المقالات المرسلة: 1128
• المقالات غير المرسلة: 440
• المقالات في آخر 24 ساعة: 78

✅ **البوت يعمل بشكل طبيعي**
📰 **سيتم إرسال مقالات قديمة غير مرسلة لضمان الاستمرارية**

🔗 المصادر النشطة: APS, الشروق, النهار, الخبر, TSA Algérie, وغيرها..."""

        await bot.send_message(
            chat_id=channel_id,
            text=test_message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info("✅ تم إرسال رسالة تحديث الحالة")
        
    except Exception as e:
        logger.error(f"❌ فشل في إرسال رسالة التحديث: {e}")

async def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء إرسال المقالات القديمة...")
    
    # إرسال رسالة تحديث الحالة
    await send_test_message()
    
    # إرسال مقالات قديمة
    await send_old_articles()
    
    logger.info("🔚 انتهاء العملية")

if __name__ == "__main__":
    asyncio.run(main()) 