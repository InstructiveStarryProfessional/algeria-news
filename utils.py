# utils.py

import re
import html
from datetime import datetime
import pytz

def clean_html(text):
    """
    تنظيف النص من وسوم HTML
    """
    if not text:
        return ""
    
    # إزالة وسوم HTML
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # تحويل رموز HTML الخاصة
    text = html.unescape(text)
    
    # إزالة المسافات الزائدة
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def prepare_article_content(title, content, unwanted_phrases=None):
    """
    Prepares the article content for display by cleaning it and removing unwanted phrases.
    """
    if not content:
        return ""

    # Clean HTML tags
    content = clean_html(content)

    # Remove unwanted phrases if provided
    if unwanted_phrases:
        for phrase in unwanted_phrases:
            content = content.replace(phrase, "")
    
    # إزالة الأسطر التي تحتوي على رموز أو أرقام فقط
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # تجاهل الأسطر التي تحتوي على رموز أو أرقام فقط
        if line and not re.match(r'^[\d\s\-_.,;:!?()\[\]{}"\'\/\\]+$', line):
            # تجاهل الأسطر القصيرة جداً (أقل من 10 أحرف)
            if len(line) >= 10:
                cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # تحقق من جودة المحتوى
    if not is_content_useful(content, title):
        return ""
    
    # إذا كان المحتوى قصيراً، أرجعه كما هو
    if len(content) <= 100:
        return content.strip()
    
    # إنشاء ملخص ذكي للمحتوى الطويل
    return create_smart_summary(content)

def is_content_useful(content, title):
    """
    فحص إذا كان المحتوى مفيداً للعرض أم لا
    """
    # إذا كان المحتوى يحتوي على نسبة عالية من الروابط أو الرموز
    link_ratio = len(re.findall(r'http[s]?://|www\.', content)) / max(len(content.split()), 1)
    if link_ratio > 0.1:  # أكثر من 10% روابط
        return False
    
    # إذا كان المحتوى يحتوي على نسبة عالية من الرموز الخاصة
    special_chars = len(re.findall(r'[^\w\s\u0600-\u06FF\u0750-\u077F]', content))
    if special_chars / max(len(content), 1) > 0.3:  # أكثر من 30% رموز خاصة
        return False
    
    # إذا كان المحتوى مجرد تكرار للعنوان بكلمات مختلفة
    title_words = set(title.lower().split())
    content_words = set(content.lower().split())
    if len(title_words.intersection(content_words)) / max(len(title_words), 1) > 0.8:
        return False
    
    return True

def create_smart_summary(content):
    """
    إنشاء ملخص ذكي للمحتوى الطويل
    """
    # تقسيم المحتوى إلى جمل
    sentences = re.split(r'[.!?]\s+', content)
    
    # اختيار أول جملة أو جملتين مفيدتين
    summary_sentences = []
    for sentence in sentences[:3]:  # أول 3 جمل كحد أقصى
        sentence = sentence.strip()
        if len(sentence) > 20 and len(summary_sentences) < 2:
            summary_sentences.append(sentence)
    
    if summary_sentences:
        summary = '. '.join(summary_sentences)
        if not summary.endswith('.'):
            summary += '.'
        
        # إذا كان الملخص لا يزال طويلاً، نقطعه عند 200 حرف
        if len(summary) > 200:
            summary = summary[:200]
            last_space = summary.rfind(' ')
            if last_space > 100:
                summary = summary[:last_space] + '...'
        
        return summary
    else:
        # إذا لم نجد جمل مفيدة، نأخذ أول 150 حرف
        summary = content[:150]
        last_space = summary.rfind(' ')
        if last_space > 50:
            summary = summary[:last_space] + '...'
        return summary

def format_date(date_obj, timezone='Africa/Algiers'):
    """
    تنسيق التاريخ بالتوقيت المحلي للجزائر
    """
    if not date_obj:
        return ""
    
    # تحويل التاريخ إلى توقيت الجزائر
    local_tz = pytz.timezone(timezone)
    if date_obj.tzinfo is None:
        # إذا كان التاريخ بدون منطقة زمنية، نفترض أنه UTC
        date_obj = pytz.utc.localize(date_obj)
    
    local_date = date_obj.astimezone(local_tz)
    
    # تنسيق التاريخ بالعربية
    months_ar = {
        1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
        7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
    }
    
    day = local_date.day
    month = months_ar[local_date.month]
    year = local_date.year
    time = local_date.strftime("%H:%M")
    
    return f"{day} {month} {year} - {time}"

def enhance_title(title):
    """
    تحسين العنوان وإزالة الكلمات الزائدة
    """
    if not title:
        return ""
    
    # إزالة كلمات مثل "عاجل" أو "حصري" من بداية العنوان
    title = re.sub(r'^(عاجل|حصري|خاص|مباشر|الآن)\s*[:|\-]\s*', '', title, flags=re.IGNORECASE)
    
    # إزالة الأقواس الزائدة
    title = re.sub(r'\(\s*\)', '', title)
    
    # تنظيف المسافات الزائدة
    title = re.sub(r'\s+', ' ', title)
    
    return title.strip()

def extract_hashtags(text, max_tags=3):
    """
    استخراج الكلمات المفتاحية من النص لاستخدامها كهاشتاقات
    """
    if not text:
        return []
    
    # قائمة الكلمات التي يجب تجاهلها
    stop_words = set([
        "من", "إلى", "عن", "على", "في", "مع", "هذا", "هذه", "تلك", "ذلك",
        "الذي", "التي", "وقد", "وقال", "وكان", "كانت", "لكن", "وأن", "وإن",
        "ثم", "أو", "أم", "إن", "إذا", "حتى", "لو", "منذ", "عند", "عندما",
        "لدى", "كل", "بعض", "غير", "بين", "بينما", "ضد", "خلال", "بعد",
        "قبل", "حول", "حين", "الى", "الي", "فى", "في", "انه", "أنه", "ان", "أن"
    ])
    
    # تنظيف النص وتقسيمه إلى كلمات
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    
    # إزالة الكلمات القصيرة والكلمات المتكررة والكلمات التي يجب تجاهلها
    unique_words = []
    for word in words:
        word = word.strip()
        if len(word) > 3 and word not in stop_words and word not in unique_words:
            unique_words.append(word)
    
    # اختيار أهم الكلمات (الأطول)
    unique_words.sort(key=len, reverse=True)
    return unique_words[:max_tags]

def create_hashtags(title, summary, source_name, category, keywords=None, sentiment=None):
    """
    إنشاء هاشتاقات للخبر
    
    Args:
        title: عنوان الخبر
        summary: ملخص الخبر
        source_name: اسم المصدر
        category: تصنيف الخبر
        keywords: الكلمات المفتاحية من التحليل (اختياري)
        sentiment: تحليل المشاعر (اختياري)
    """
    hashtags = ["#أخبار_الجزائر"]
    
    # إضافة تصنيف الخبر
    if category:
        category_tag = category.replace(' ', '_').replace('-', '_')
        hashtags.append(f"#{category_tag}")
    
    # إضافة اسم المصدر
    if source_name:
        source_tag = source_name.replace(' ', '_').replace('-', '_')
        hashtags.append(f"#{source_tag}")
    
    # إضافة هاشتاق للمشاعر
    if sentiment:
        if sentiment == "positive":
            hashtags.append("#أخبار_إيجابية")
        elif sentiment == "negative":
            hashtags.append("#أخبار_سلبية")
    
    # استخدام الكلمات المفتاحية من التحليل إذا كانت متوفرة
    if keywords and isinstance(keywords, list):
        for keyword in keywords:
            if len(hashtags) >= 7:  # زيادة الحد الأقصى للهاشتاقات
                break
            keyword_tag = keyword.replace(' ', '_').replace('-', '_')
            hashtags.append(f"#{keyword_tag}")
    else:
        # استخراج هاشتاقات إضافية من العنوان والملخص
        text = f"{title} {summary}"
        extra_tags = extract_hashtags(text)
        
        for tag in extra_tags:
            if len(hashtags) >= 7:  # زيادة الحد الأقصى للهاشتاقات
                break
            hashtags.append(f"#{tag}")
    
    return " ".join(hashtags)