# -*- coding: utf-8 -*-
# قائمة شاملة بمصادر الأخبار المحلية الجزائرية والعالمية
# تم تنظيم المصادر حسب الأولوية والفئة لضمان تنويع المحتوى

NEWS_SOURCES = [
    # ==================== المصادر الرسمية الجزائرية (أولوية عالية) ====================
    {
        'name': 'وكالة الأنباء الجزائرية (APS)',
        'url': 'https://www.aps.dz/ar/rss.xml',
        'type': 'rss',
        'category': 'urgent',
        'priority': 1,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['#txt_depeche'],
            'unwanted_phrases': ['وكالة الأنباء الجزائرية', 'APS', 'وأج']
        }
    },
    {
        'name': 'الإذاعة الجزائرية',
        'url': 'https://www.radioalgerie.dz/news/ar/rss.xml',
        'type': 'rss',
        'category': 'official',
        'priority': 1,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-body'],
            'unwanted_phrases': ['الإذاعة الجزائرية']
        }
    },
    {
        'name': 'التلفزيون الجزائري (ENTV)',
        'url': 'https://www.entv.dz/rss.xml',
        'type': 'rss',
        'category': 'official',
        'priority': 1,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['التلفزيون الجزائري']
        }
    },
    
    # ==================== الصحف الجزائرية الرئيسية ====================
    {
        'name': 'الشروق اليومي',
        'url': 'https://www.echoroukonline.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.post-content', '.entry-content'],
            'unwanted_phrases': ['الشروق أونلاين', 'جريدة الشروق اليومي']
        }
    },
    {
        'name': 'النهار الجديد',
        'url': 'https://www.ennaharonline.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['النهار أونلاين', 'جريدة النهار الجديد']
        }
    },
    {
        'name': 'الخبر',
        'url': 'https://www.elkhabar.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-body', '.entry-content'],
            'unwanted_phrases': ['جريدة الخبر']
        }
    },
    {
        'name': 'البلاد',
        'url': 'https://elbilad.net/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['البلاد.نت']
        }
    },
    {
        'name': 'TSA Algérie',
        'url': 'https://www.tsa-algerie.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['TSA Algérie']
        }
    },
    {
        'name': 'جريدة النصر',
        'url': 'https://www.annasronline.com/rss.xml',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['جريدة النصر']
        }
    },
    {
        'name': 'أخبار اليوم',
        'url': 'https://www.akhbarelyoum.dz/feed',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['أخبار اليوم']
        }
    },
    {
        'name': 'الموعد اليومي',
        'url': 'https://www.elmaouid.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['الموعد اليومي']
        }
    },
    {
        'name': 'الشعب',
        'url': 'https://www.ech-chaab.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['الشعب']
        }
    },
    {
        'name': 'المساء',
        'url': 'https://www.el-massa.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['المساء']
        }
    },
    {
        'name': 'صوت الأحرار',
        'url': 'https://www.sawt-alahrar.net/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['صوت الأحرار']
        }
    },
    {
        'name': 'الحوار',
        'url': 'https://www.elhiwaronline.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['الحوار']
        }
    },
    {
        'name': 'المحور',
        'url': 'https://www.elmihwar.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['المحور']
        }
    },
    {
        'name': 'جريدة الجمهورية',
        'url': 'https://www.djazairess.com/eldjoumhouria/rss',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.story_body'],
            'unwanted_phrases': ['جريدة الجمهورية']
        }
    },
    
    # ==================== المصادر الاقتصادية الجزائرية ====================
    {
        'name': 'Algérie Eco',
        'url': 'https://www.algerie-eco.com/feed/',
        'type': 'rss',
        'category': 'economic',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.td-post-content', '.entry-content'],
            'unwanted_phrases': ['Algérie Eco']
        }
    },
    {
        'name': 'الاقتصاد الجزائري',
        'url': 'https://www.djazairess.com/feed/',
        'type': 'rss',
        'category': 'economic',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.story_body', '.entry-content'],
            'unwanted_phrases': ['جزايرس']
        }
    },
    
    # ==================== المصادر الرياضية الجزائرية ====================
    {
        'name': 'الهداف',
        'url': 'https://www.elheddaf.com/feed/',
        'type': 'rss',
        'category': 'sports',
        'priority': 3,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['الهداف']
        }
    },
    {
        'name': 'البطل',
        'url': 'https://www.lebuteur.com/feed/',
        'type': 'rss',
        'category': 'sports',
        'priority': 3,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['البطولة']
        }
    },
    {
        'name': 'DZFoot',
        'url': 'https://www.dzfoot.com/feed/',
        'type': 'rss',
        'category': 'sports',
        'priority': 3,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['DZfoot']
        }
    },

    # ==================== قنوات تلفزيونية جزائرية ====================
    {
        'name': 'قناة البلاد',
        'url': 'https://www.elbilad.net/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['البلاد.نت']
        }
    },
    {
        'name': 'قناة دزاير نيوز',
        'url': 'https://www.dzairnews.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.post-content', '.entry-content'],
            'unwanted_phrases': ['دزاير نيوز']
        }
    },
    {
        'name': 'قناة نوميديا نيوز',
        'url': 'https://numidianews.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.post-content', '.entry-content'],
            'unwanted_phrases': ['نوميديا نيوز']
        }
    },
    {
        'name': 'قناة الحياة',
        'url': 'https://www.elhayatonline.com/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['قناة الحياة']
        }
    },
    {
        'name': 'قناة بور تي في',
        'url': 'https://www.beurtv.tv/feed/',
        'type': 'rss',
        'category': 'news',
        'priority': 2,
        'country': 'DZ',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['قناة بور تي في']
        }
    },
    
    # ==================== المصادر العربية العالمية ====================
    {
        'name': 'الجزيرة نت',
        'url': 'https://www.aljazeera.net/rss/all.xml',
        'type': 'rss',
        'category': 'news',
        'priority': 4,
        'country': 'QA',
        'scraping_config': {
            'content_selectors': ['.wysiwyg--all-content'],
            'unwanted_phrases': ['الجزيرة.نت']
        }
    },
    {
        'name': 'العربية',
        'url': 'https://www.alarabiya.net/rss.xml',
        'type': 'rss',
        'category': 'news',
        'priority': 4,
        'country': 'SA',
        'scraping_config': {
            'content_selectors': ['.article-body'],
            'unwanted_phrases': ['العربية.نت']
        }
    },
    {
        'name': 'BBC العربية',
        'url': 'https://feeds.bbci.co.uk/arabic/rss.xml',
        'type': 'rss',
        'category': 'news',
        'priority': 4,
        'country': 'GB',
        'scraping_config': {
            'content_selectors': ['main > div > p'],
            'unwanted_phrases': ['بي بي سي']
        }
    },
    {
        'name': 'سكاي نيوز عربية',
        'url': 'https://www.skynewsarabia.com/rss.xml',
        'type': 'rss',
        'category': 'news',
        'priority': 4,
        'country': 'AE',
        'scraping_config': {
            'content_selectors': ['.article-body'],
            'unwanted_phrases': ['سكاي نيوز عربية']
        }
    },
    {
        'name': 'فرانس 24 عربي',
        'url': 'https://www.france24.com/ar/rss',
        'type': 'rss',
        'category': 'news',
        'priority': 4,
        'country': 'FR',
        'scraping_config': {
            'content_selectors': ['.t-content__body'],
            'unwanted_phrases': ['فرانس 24']
        }
    },
    {
        'name': 'RT Arabic',
        'url': 'https://arabic.rt.com/rss/',
        'type': 'rss',
        'category': 'news',
        'priority': 4,
        'country': 'RU',
        'scraping_config': {
            'content_selectors': ['.article '],
            'unwanted_phrases': ['RT Arabic']
        }
    },
    
    # ==================== المصادر الاقتصادية العالمية ====================
    {
        'name': 'العربية بزنس',
        # ❌ هذا المصدر معطل حالياً (HTTP 403) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.alarabiya.net/ar/aswaq/rss.xml',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'economic',
        'priority': 5,
        'country': 'SA',
        'scraping_config': {
            'content_selectors': ['.article-body'],
            'unwanted_phrases': ['العربية بزنس']
        }
    },
    {
        'name': 'الاقتصادية',
        'url': 'https://www.aleqt.com/rss.xml',
        'type': 'rss',
        'category': 'economic',
        'priority': 5,
        'country': 'SA',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['الاقتصادية']
        }
    },
    {
        'name': 'معلومات مباشر',
        # ❌ هذا المصدر معطل حالياً (HTTP 404) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.mubasher.info/feed/',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'economic',
        'priority': 5,
        'country': 'AE',
        'scraping_config': {
            'content_selectors': ['.article-content', '.entry-content'],
            'unwanted_phrases': ['مباشر']
        }
    },
    
    # ==================== المصادر الرياضية العالمية ====================
    {
        'name': 'بي إن سبورت',
        # ❌ هذا المصدر معطل حالياً (HTTP 403) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.beinsports.com/ar/rss.xml',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'QA',
        'scraping_config': {
            'content_selectors': ['article > div > p'],
            'unwanted_phrases': ['beIN SPORTS']
        }
    },
    {
        'name': 'كووورة',
        # ❌ هذا المصدر معطل حالياً (HTTP 404) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.kooora.com/rss.xml',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'EG',
        'scraping_config': {
            'content_selectors': ['.articleBody'],
            'unwanted_phrases': ['كووورة']
        }
    },
    {
        'name': 'يلا كورة',
        'url': 'https://www.yallakora.com/rss.xml',
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'EG',
        'scraping_config': {
            'content_selectors': ['.article-body', '.entry-content'],
            'unwanted_phrases': ['يلا كورة']
        }
    },
    {
        'name': 'الرياضة العربية',
        # ❌ هذا المصدر معطل حالياً (HTTP 404) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.arriyadiyah.com/feed/',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'SA',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['الرياضية']
        }
    },
    {
        'name': 'Goal.com',
        # ❌ هذا المصدر معطل حالياً (HTTP 404) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.goal.com/ar/feeds/news.xml',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'GLOBAL',
        'scraping_config': {
            'content_selectors': ['.article-body'],
            'unwanted_phrases': ['Goal.com']
        }
    },
    {
        'name': 'Eurosport',
        'url': 'https://arabia.eurosport.com/rss.xml',
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'GLOBAL',
        'scraping_config': {
            'content_selectors': ['.story-body'],
            'unwanted_phrases': ['Eurosport']
        }
    },
    {
        'name': 'FilGoal',
        # ❌ هذا المصدر معطل حالياً (HTTP 404) ولا يوجد له RSS رسمي فعال
        # 'url': 'https://www.filgoal.com/rss-feed.xml',
        # يمكن حذفه أو تعطيله مؤقتاً
        'type': 'rss',
        'category': 'sports',
        'priority': 6,
        'country': 'EG',
        'scraping_config': {
            'content_selectors': ['#NewsStoryHolder'],
            'unwanted_phrases': ['FilGoal']
        }
    },
    
    # ==================== المصادر التقنية ====================
    {
        'name': 'عالم التقنية',
        'url': 'https://www.tech-wd.com/feed/',
        'type': 'rss',
        'category': 'technology',
        'priority': 7,
        'country': 'SA',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['عالم التقنية']
        }
    },
    {
        'name': 'أراجيك تك',
        'url': 'https://www.arageek.com/tech/feed',
        'type': 'rss',
        'category': 'technology',
        'priority': 7,
        'country': 'JO',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['أراجيك']
        }
    },
    {
        'name': 'البوابة العربية للأخبار التقنية',
        'url': 'https://aitnews.com/feed/',
        'type': 'rss',
        'category': 'technology',
        'priority': 7,
        'country': 'الإمارات',
        'scraping_config': {
            'content_selectors': ['.entry-content'],
            'unwanted_phrases': ['البوابة العربية للأخبار التقنية']
        }
    }
]

def get_source_by_name(name):
    """Fetches a source's configuration by its name."""
    for source in NEWS_SOURCES:
        if source['name'] == name:
            return source
    return {}



# ==================== إعدادات المصادر ====================
# تصنيف الأولويات:
# 1 = عاجل ورسمي (مصادر حكومية جزائرية)
# 2 = محلي مهم (صحف جزائرية رئيسية)
# 3 = رياضي محلي
# 4 = عالمي مهم
# 5 = اقتصادي عالمي
# 6 = رياضي عالمي
# 7 = تقني ومتخصص

# تصنيف الفئات:
# urgent = أخبار عاجلة
# official = مصادر رسمية
# news = أخبار عامة
# economic = اقتصادية
# sports = رياضية
# technology = تقنية