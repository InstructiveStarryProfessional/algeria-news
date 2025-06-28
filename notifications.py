# notifications.py

import logging
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN
from database import get_db_session, Subscriber

logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self):
        self.session = get_db_session()
        self.bot = Bot(TELEGRAM_BOT_TOKEN)

    def add_user(self, user_id):
        """إضافة مستخدم جديد إلى قائمة المشتركين."""
        existing_subscriber = self.session.query(Subscriber).filter_by(user_id=user_id).first()
        if existing_subscriber:
            return False  # المستخدم مسجل بالفعل

        new_subscriber = Subscriber(user_id=user_id)
        self.session.add(new_subscriber)
        self.session.commit()
        return True

    def remove_user(self, user_id):
        """إزالة مستخدم من قائمة المشتركين."""
        subscriber = self.session.query(Subscriber).filter_by(user_id=user_id).first()
        if subscriber:
            self.session.delete(subscriber)
            self.session.commit()
            return True
        return False

    def get_subscribers_count(self):
        """الحصول على عدد المشتركين."""
        return self.session.query(Subscriber).count()

    async def notify_users(self, article, category):
        """إرسال إشعارات للمستخدمين."""
        # هذا مجرد مثال، يمكن توسيعه لدعم التفضيلات
        subscribers = self.session.query(Subscriber).all()
        for subscriber in subscribers:
            try:
                # يجب تعديل هذه الرسالة لتكون أكثر ملاءمة
                message = f"خبر جديد في فئة {category}:\n{article.title}\n{article.link}"
                await self.bot.send_message(chat_id=subscriber.user_id, text=message)
            except Exception as e:
                logger.error(f"Failed to send notification to {subscriber.user_id}: {e}")
    
    def update_preferences(self, user_id, preferences):
        """
        تحديث تفضيلات المستخدم في قاعدة البيانات
        """
        subscriber = self.session.query(Subscriber).filter_by(user_id=user_id).first()
        if subscriber:
            if hasattr(subscriber, 'preferences'):
                subscriber.preferences.update(preferences)
            else:
                subscriber.preferences = preferences
            self.session.commit()
            return True
        return False

    def get_user_preferences(self, user_id):
        """
        الحصول على تفضيلات المستخدم من قاعدة البيانات
        """
        subscriber = self.session.query(Subscriber).filter_by(user_id=user_id).first()
        if subscriber and hasattr(subscriber, 'preferences'):
            return subscriber.preferences
        return None
    
    def get_subscribers_count(self):
        """
        الحصول على عدد المشتركين
        """
        return self.session.query(Subscriber).count()

    def get_news_summary(self, category=None, local_only=False, sports_only=False):
        """
        إرجاع ملخص لعناوين الأخبار الأخيرة خلال 24 ساعة حسب الفئة أو النوع.
        category: يمكن تحديد فئة (مثل 'news' أو 'economic' أو 'sports')
        local_only: إذا True، فقط الأخبار المحلية (country='DZ')
        sports_only: إذا True، فقط الأخبار الرياضية
        """
        from database import Article
        import datetime
        session = self.session
        now = datetime.datetime.utcnow()
        since = now - datetime.timedelta(hours=24)
        query = session.query(Article).filter(Article.published_date >= since)
        if local_only:
            query = query.filter(Article.country == 'DZ')
        if sports_only:
            query = query.filter(Article.category == 'sports')
        if category:
            query = query.filter(Article.category == category)
        articles = query.order_by(Article.published_date.desc()).all()
        return [(a.title, a.published_date, a.source) for a in articles]
# إنشاء كائن عام لإدارة الإشعارات
notification_manager = NotificationManager()