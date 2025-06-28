# ==================== إعدادات قاعدة البيانات ====================
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import random

# ==================== إعدادات الاتصال ====================
DATABASE_URL = "sqlite:///news.db"
Base = declarative_base()

# ==================== نموذج المقال ====================
class Article(Base):
    """نموذج قاعدة البيانات للمقالات الإخبارية"""
    __tablename__ = 'articles'

    # الحقول الأساسية
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # عنوان المقال
    link = Column(String, unique=True, nullable=False)  # رابط المقال
    source = Column(String, nullable=False)  # مصدر الخبر
    published_date = Column(DateTime, nullable=False)  # تاريخ النشر
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # تاريخ الإضافة
    
    # الحقول الإضافية
    category = Column(String, nullable=True)  # تصنيف المقال
    image_url = Column(String, nullable=True)  # رابط الصورة
    summary = Column(String, nullable=True)  # ملخص المقال
    
    # حقول التتبع
    sent_to_telegram = Column(Boolean, default=False)  # تم الإرسال للتليجرام
    sentiment_score = Column(Float, nullable=True)  # درجة المشاعر

    def __repr__(self):
        return f"<Article(title='{self.title}', source='{self.source}')>"

# ==================== نموذج الإحصائيات ====================
class Stats(Base):
    """نموذج قاعدة البيانات لتخزين إحصائيات البوت"""
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    total_articles = Column(Integer, default=0)
    articles_by_source = Column(String, default='{}')  # تخزين كـ JSON
    articles_by_category = Column(String, default='{}') # تخزين كـ JSON

# ==================== نموذج المشتركين ====================
class Subscriber(Base):
    """نموذج قاعدة البيانات للمستخدمين المشتركين"""
    __tablename__ = 'subscribers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.datetime.utcnow)

# ==================== دوال قاعدة البيانات ====================

def get_db_session():
    """إنشاء جلسة اتصال جديدة مع قاعدة البيانات"""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def get_random_unsent_high_sentiment_article():
    """
    استرجاع مقال عشوائي غير مرسل بمشاعر إيجابية من آخر 24 ساعة
    مع إعطاء أولوية للمصادر الجزائرية
    """
    session = get_db_session()
    try:
        # حساب الوقت قبل 24 ساعة
        twenty_four_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        
        # البحث عن مقال جزائري أولاً
        algerian_article = session.query(Article).filter(
            Article.sent_to_telegram == False,
            Article.sentiment_score > 0.3,  # مشاعر إيجابية
            Article.published_date >= twenty_four_hours_ago,
            Article.source.like('%الجزائر%')  # مصادر جزائرية
        ).order_by(func.random()).first()
        
        if algerian_article:
            return algerian_article
        
        # إذا لم توجد مقالات جزائرية، البحث في المصادر العربية
        article = session.query(Article).filter(
            Article.sent_to_telegram == False,
            Article.sentiment_score > 0.3,  # مشاعر إيجابية
            Article.published_date >= twenty_four_hours_ago
        ).order_by(func.random()).first()
        
        return article
    except Exception as e:
        print(f"خطأ في استرجاع المقال: {e}")
        return None
    finally:
        session.close()