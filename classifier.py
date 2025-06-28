# classifier.py

# Simple keyword-based classifier
# This can be expanded with more sophisticated NLP techniques

CATEGORIES = {
    'سياسة': ['سياسة', 'حكومة', 'انتخابات', 'برلمان', 'رئيس', 'وزير'],
    'اقتصاد': ['اقتصاد', 'بورصة', 'أسهم', 'استثمار', 'تجارة', 'نفط'],
    'رياضة': ['رياضة', 'كرة القدم', 'الدوري', 'كأس', 'منتخب', 'لاعب'],
    'تكنولوجيا': ['تكنولوجيا', 'هواتف', 'تطبيقات', 'إنترنت', 'ذكاء اصطناعي'],
    'ثقافة': ['ثقافة', 'فن', 'موسيقى', 'سينما', 'مسرح', 'تراث'],
}

EMOJIS = {
    'سياسة': '🏛️',
    'اقتصاد': '💰',
    'رياضة': '⚽',
    'تكنولوجيا': '📱',
    'ثقافة': '🎨',
    'عام': '📰' # Default emoji
}

def classify_article(title, summary):
    """Classifies an article based on keywords in title and summary."""
    text_to_check = (title + ' ' + summary).lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in text_to_check for keyword in keywords):
            return category
    return 'عام' # Default category

def get_emoji_for_category(category):
    """Returns an emoji for a given category."""
    return EMOJIS.get(category, EMOJIS['عام'])