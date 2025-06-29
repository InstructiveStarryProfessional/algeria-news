#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت فحص قاعدة البيانات ومعرفة حالة المقالات
"""

import datetime
from database import get_db_session, Article
from sqlalchemy import func

def check_database():
    """فحص قاعدة البيانات"""
    session = get_db_session()
    
    print("🔍 فحص قاعدة البيانات...")
    print("=" * 50)
    
    # إجمالي المقالات
    total_articles = session.query(Article).count()
    print(f"📊 إجمالي المقالات: {total_articles}")
    
    # المقالات المرسلة وغير المرسلة
    sent_articles = session.query(Article).filter_by(sent_to_telegram=True).count()
    unsent_articles = session.query(Article).filter_by(sent_to_telegram=False).count()
    print(f"✅ المقالات المرسلة: {sent_articles}")
    print(f"❌ المقالات غير المرسلة: {unsent_articles}")
    
    # المقالات في آخر 24 ساعة
    twenty_four_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    recent_articles = session.query(Article).filter(
        Article.published_date >= twenty_four_hours_ago
    ).count()
    print(f"⏰ المقالات في آخر 24 ساعة: {recent_articles}")
    
    # المقالات غير المرسلة في آخر 24 ساعة
    recent_unsent = session.query(Article).filter(
        Article.sent_to_telegram == False,
        Article.published_date >= twenty_four_hours_ago
    ).count()
    print(f"📰 المقالات غير المرسلة في آخر 24 ساعة: {recent_unsent}")
    
    # المصادر الأكثر نشاطاً
    print("\n📈 المصادر الأكثر نشاطاً:")
    source_stats = session.query(
        Article.source, 
        func.count(Article.id).label('count')
    ).group_by(Article.source).order_by(func.count(Article.id).desc()).limit(10).all()
    
    for source, count in source_stats:
        print(f"   {source}: {count} مقال")
    
    # آخر 5 مقالات
    print("\n📰 آخر 5 مقالات:")
    recent_articles_list = session.query(Article).order_by(
        Article.published_date.desc()
    ).limit(5).all()
    
    for article in recent_articles_list:
        status = "✅ مرسل" if article.sent_to_telegram else "❌ غير مرسل"
        print(f"   {article.title[:50]}... ({status})")
        print(f"      المصدر: {article.source}")
        print(f"      التاريخ: {article.published_date}")
        print(f"      الرابط: {article.link}")
        print()
    
    # المقالات غير المرسلة مع مشاعر إيجابية
    print("😊 المقالات غير المرسلة مع مشاعر إيجابية:")
    positive_unsent = session.query(Article).filter(
        Article.sent_to_telegram == False,
        Article.sentiment_score > 0.3
    ).order_by(Article.published_date.desc()).limit(5).all()
    
    for article in positive_unsent:
        print(f"   {article.title[:50]}... (مشاعر: {article.sentiment_score:.2f})")
    
    session.close()
    
    print("\n" + "=" * 50)
    print("🔚 انتهاء فحص قاعدة البيانات")

if __name__ == "__main__":
    check_database() 