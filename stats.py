# stats.py

import json
import logging
from datetime import datetime
from database import get_db_session, Stats

logger = logging.getLogger(__name__)

class BotStats:
    def __init__(self):
        self.session = get_db_session()
        self.stats = self._load_or_create_stats()

    def _load_or_create_stats(self):
        stats_record = self.session.query(Stats).first()
        if not stats_record:
            stats_record = Stats()
            self.session.add(stats_record)
            self.session.commit()
        return stats_record

    def add_article(self, source, category):
        """إضافة مقال جديد إلى الإحصائيات."""
        self.stats.total_articles += 1

        source_stats = json.loads(self.stats.articles_by_source)
        source_stats[source] = source_stats.get(source, 0) + 1
        self.stats.articles_by_source = json.dumps(source_stats)

        category_stats = json.loads(self.stats.articles_by_category)
        category_stats[category] = category_stats.get(category, 0) + 1
        self.stats.articles_by_category = json.dumps(category_stats)

        self.session.commit()

    def get_summary(self):
        """الحصول على ملخص الإحصائيات."""
        days_running = (datetime.utcnow() - self.stats.start_time).days + 1
        avg_per_day = self.stats.total_articles / days_running if days_running > 0 else 0

        top_sources = sorted(json.loads(self.stats.articles_by_source).items(), key=lambda item: item[1], reverse=True)[:5]
        top_categories = sorted(json.loads(self.stats.articles_by_category).items(), key=lambda item: item[1], reverse=True)[:5]

        return {
            'total_articles': self.stats.total_articles,
            'days_running': days_running,
            'avg_per_day': round(avg_per_day, 2),
            'top_sources': top_sources,
            'top_categories': top_categories,
            'last_update': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        top_sources = sorted(self.stats["articles_by_source"].items(), key=lambda x: x[1], reverse=True)[:5]
        
        # الحصول على أكثر التصنيفات شيوعاً
        top_categories = sorted(self.stats["articles_by_category"].items(), key=lambda x: x[1], reverse=True)
        
        # الحصول على إحصائيات آخر 7 أيام
        last_week_stats = {}
        today = datetime.now().date()
        for i in range(7):
            day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            if day in self.stats["daily_stats"]:
                last_week_stats[day] = self.stats["daily_stats"][day]["total"]
            else:
                last_week_stats[day] = 0
        
        return {
            "total_articles": self.stats["total_articles"],
            "days_running": days_running,
            "avg_per_day": round(avg_per_day, 1),
            "top_sources": top_sources,
            "top_categories": top_categories,
            "last_week": last_week_stats,
            "last_update": self.stats["last_update"]
        }

# إنشاء كائن عام للإحصائيات
bot_stats = BotStats()