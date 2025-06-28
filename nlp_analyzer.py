# nlp_analyzer.py

import re
import logging
from collections import Counter
import json
import os

logger = logging.getLogger(__name__)

# ملف لتخزين بيانات التحليل
ANALYSIS_FILE = "news_analysis.json"

# قائمة الكلمات غير المهمة (stop words) باللغة العربية
ARABIC_STOP_WORDS = [
    "من", "في", "على", "إلى", "عن", "مع", "هذا", "هذه", "ذلك", "تلك",
    "أن", "لا", "ما", "هل", "كيف", "متى", "أين", "لماذا", "كم", "أي",
    "و", "ف", "ثم", "أو", "أم", "لكن", "بل", "حتى", "إذا", "إن",
    "كان", "كانت", "كانوا", "يكون", "تكون", "سوف", "سـ", "قد", "منذ",
    "خلال", "بعد", "قبل", "عند", "عندما", "بينما", "كما", "بين", "فوق", "تحت",
    "له", "لها", "لهم", "لهن", "به", "بها", "بهم", "بهن", "منه", "منها",
    "منهم", "منهن", "عنه", "عنها", "عنهم", "عنهن", "إليه", "إليها", "إليهم", "إليهن",
    "هو", "هي", "هم", "هن", "نحن", "أنت", "أنتم", "أنتن", "أنا", "أنتما",
    "هما", "هما", "نحن", "أنتم", "هم", "هن", "التي", "الذي", "اللذان", "اللتان",
    "الذين", "اللاتي", "اللواتي", "الأول", "الأولى", "الثاني", "الثانية", "الثالث", "الثالثة",
    "الرابع", "الرابعة", "الخامس", "الخامسة", "السادس", "السادسة", "السابع", "السابعة",
    "الثامن", "الثامنة", "التاسع", "التاسعة", "العاشر", "العاشرة"
]

# قائمة الكلمات المفتاحية للمشاعر الإيجابية
POSITIVE_WORDS = [
    "نجاح", "تطور", "تقدم", "إنجاز", "تحسن", "ارتفاع", "زيادة", "ربح", "فوز", "انتصار",
    "تفاؤل", "أمل", "سلام", "استقرار", "ازدهار", "رخاء", "تعاون", "اتفاق", "تفاهم", "مكافأة",
    "جائزة", "تكريم", "تقدير", "احترام", "دعم", "مساعدة", "تضامن", "تعافي", "شفاء", "علاج",
    "حل", "إصلاح", "تطوير", "ابتكار", "إبداع", "اختراع", "اكتشاف", "تحسين", "تعزيز", "تمكين",
    "فرحة", "سعادة", "بهجة", "سرور", "مسرة", "بشرى", "خير", "بركة", "نعمة", "هدية",
    "منحة", "عطاء", "كرم", "سخاء", "جود", "إحسان", "فضل", "مروءة", "شهامة", "نبل",
    "توفيق", "نصر", "ظفر", "غلبة", "تفوق", "امتياز", "براعة", "مهارة", "حذق", "إتقان"
]

# قائمة الكلمات المفتاحية للمشاعر السلبية
NEGATIVE_WORDS = [
    "فشل", "تراجع", "انخفاض", "هبوط", "خسارة", "هزيمة", "تشاؤم", "يأس", "حرب", "صراع",
    "توتر", "أزمة", "مشكلة", "خلاف", "نزاع", "عقوبة", "غرامة", "عقاب", "إهانة", "احتقار",
    "رفض", "معارضة", "تهديد", "خطر", "ضرر", "إصابة", "مرض", "وفاة", "موت", "قتل",
    "اعتداء", "هجوم", "إرهاب", "تفجير", "تدمير", "تخريب", "سرقة", "احتيال", "فساد", "رشوة",
    "حزن", "ألم", "معاناة", "بؤس", "شقاء", "تعاسة", "كآبة", "اكتئاب", "قلق", "خوف",
    "رعب", "فزع", "هلع", "ذعر", "جزع", "ارتباك", "حيرة", "ارتياب", "شك", "ظن",
    "غضب", "سخط", "حنق", "غيظ", "حقد", "كره", "بغض", "عداوة", "خصومة", "عداء"
]

class NewsAnalyzer:
    def __init__(self):
        self.analysis_data = self._load_analysis_data()
    
    def _load_analysis_data(self):
        """تحميل بيانات التحليل من الملف"""
        if os.path.exists(ANALYSIS_FILE):
            try:
                with open(ANALYSIS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading analysis file: {e}")
        
        # إنشاء بيانات افتراضية إذا لم يكن الملف موجوداً
        return {
            "trending_topics": {},
            "sentiment_analysis": {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            },
            "word_frequency": {},
            "source_sentiment": {}
        }
    
    def _save_analysis_data(self):
        """حفظ بيانات التحليل في الملف"""
        try:
            with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving analysis file: {e}")
    
    def analyze_sentiment(self, text):
        """تحليل المشاعر في النص (إيجابي، سلبي، محايد)"""
        positive_count = sum(1 for word in text.split() if word in POSITIVE_WORDS)
        negative_count = sum(1 for word in text.split() if word in NEGATIVE_WORDS)

        if positive_count > negative_count:
            return 1.0  # إيجابي
        elif negative_count > positive_count:
            return -1.0 # سلبي
        else:
            return 0.0  # محايد

    def _extract_keywords(self, text):
        """استخراج الكلمات المفتاحية من النص"""
        # تنظيف النص
        text = re.sub(r'[^\w\s]', ' ', text)  # إزالة علامات الترقيم
        text = re.sub(r'\d+', ' ', text)       # إزالة الأرقام
        text = re.sub(r'\s+', ' ', text)       # إزالة المسافات المتعددة
        
        # تقسيم النص إلى كلمات
        words = text.split()
        
        # إزالة الكلمات غير المهمة
        filtered_words = [word for word in words if word.strip() and len(word) > 2 and word not in ARABIC_STOP_WORDS]
        
        # حساب تكرار الكلمات
        word_counts = Counter(filtered_words)
        
        # استخراج الكلمات المركبة (عبارات من كلمتين)
        bigrams = []
        for i in range(len(words) - 1):
            if (words[i] not in ARABIC_STOP_WORDS and words[i+1] not in ARABIC_STOP_WORDS 
                and len(words[i]) > 2 and len(words[i+1]) > 2):
                bigram = f"{words[i]} {words[i+1]}"
                bigrams.append(bigram)
        
        # حساب تكرار العبارات المركبة
        bigram_counts = Counter(bigrams)
        
        # دمج الكلمات المفردة والعبارات المركبة
        all_keywords = []
        
        # إضافة العبارات المركبة الأكثر تكراراً
        for bigram, count in bigram_counts.most_common(5):
            if count > 1:  # إضافة العبارات التي تتكرر أكثر من مرة
                all_keywords.append(bigram)
        
        # إضافة الكلمات المفردة الأكثر تكراراً
        for word, count in word_counts.most_common(10):
            if word not in ' '.join(all_keywords):  # تجنب تكرار الكلمات الموجودة في العبارات
                all_keywords.append(word)
        
        return all_keywords
    
    def _analyze_sentiment(self, text):
        """تحليل المشاعر في النص"""
        # تنظيف النص
        text = re.sub(r'[^\w\s]', ' ', text)  # إزالة علامات الترقيم
        text = re.sub(r'\s+', ' ', text)       # إزالة المسافات المتعددة
        text = text.lower()
        
        # تقسيم النص إلى كلمات
        words = text.split()
        
        # حساب نقاط المشاعر
        positive_score = 0
        negative_score = 0
        
        # فحص الكلمات الإيجابية
        for pos_word in POSITIVE_WORDS:
            if pos_word in text:
                # زيادة النقاط بناءً على عدد مرات ظهور الكلمة
                occurrences = text.count(pos_word)
                positive_score += occurrences
                
                # زيادة النقاط إذا كانت الكلمة في العنوان (مضاعفة الأهمية)
                if pos_word in text.split()[:10]:  # افتراض أن الكلمات الأولى هي العنوان
                    positive_score += 1
        
        # فحص الكلمات السلبية
        for neg_word in NEGATIVE_WORDS:
            if neg_word in text:
                # زيادة النقاط بناءً على عدد مرات ظهور الكلمة
                occurrences = text.count(neg_word)
                negative_score += occurrences
                
                # زيادة النقاط إذا كانت الكلمة في العنوان (مضاعفة الأهمية)
                if neg_word in text.split()[:10]:  # افتراض أن الكلمات الأولى هي العنوان
                    negative_score += 1
        
        # تحديد المشاعر بناءً على النقاط
        if positive_score > negative_score * 1.2:  # إعطاء أفضلية طفيفة للمشاعر الإيجابية
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"
    
    def analyze_article(self, article):
        """تحليل مقال إخباري"""
        # تحليل العنوان والملخص بشكل منفصل ثم دمجهما
        title = article['title']
        summary = article['summary']
        full_text = f"{title} {summary}"
        
        # استخراج الكلمات المفتاحية من العنوان (أهمية مضاعفة)
        title_keywords = self._extract_keywords(title)
        
        # استخراج الكلمات المفتاحية من النص الكامل
        full_keywords = self._extract_keywords(full_text)
        
        # دمج الكلمات المفتاحية مع إعطاء الأولوية للكلمات من العنوان
        combined_keywords = []
        
        # إضافة كلمات العنوان أولاً
        for keyword in title_keywords:
            if keyword not in combined_keywords:
                combined_keywords.append(keyword)
        
        # إضافة كلمات النص الكامل
        for keyword in full_keywords:
            if keyword not in combined_keywords and len(combined_keywords) < 10:
                combined_keywords.append(keyword)
        
        # تحليل المشاعر
        title_sentiment = self._analyze_sentiment(title)  # تحليل مشاعر العنوان
        full_sentiment = self._analyze_sentiment(full_text)  # تحليل مشاعر النص الكامل
        
        # تحديد المشاعر النهائية (إعطاء وزن أكبر لمشاعر العنوان)
        if title_sentiment == full_sentiment:
            sentiment = title_sentiment
        elif title_sentiment != "neutral":
            sentiment = title_sentiment  # تفضيل مشاعر العنوان إذا كانت غير محايدة
        else:
            sentiment = full_sentiment
        
        # تحديث بيانات التحليل
        self._update_trending_topics(combined_keywords)
        self._update_sentiment_analysis(sentiment)
        self._update_word_frequency(combined_keywords)
        self._update_source_sentiment(article['source_name'], sentiment)
        
        # حفظ البيانات
        self._save_analysis_data()
        
        # تحديد الكلمات المفتاحية النهائية للهاشتاقات (الأكثر أهمية)
        final_keywords = []
        
        # إضافة الكلمات المفتاحية من العنوان أولاً
        for keyword in title_keywords[:3]:
            if keyword not in final_keywords:
                final_keywords.append(keyword)
        
        # إضافة الكلمات المفتاحية من النص الكامل
        for keyword in combined_keywords:
            if keyword not in final_keywords and len(final_keywords) < 5:
                final_keywords.append(keyword)
        
        return {
            "keywords": final_keywords,  # أهم الكلمات المفتاحية
            "sentiment": sentiment
        }
    
    def _update_trending_topics(self, keywords):
        """تحديث المواضيع الرائجة"""
        for keyword in keywords:
            if keyword in self.analysis_data["trending_topics"]:
                self.analysis_data["trending_topics"][keyword] += 1
            else:
                self.analysis_data["trending_topics"][keyword] = 1
        
        # الاحتفاظ فقط بأهم 100 موضوع
        sorted_topics = sorted(self.analysis_data["trending_topics"].items(), key=lambda x: x[1], reverse=True)
        self.analysis_data["trending_topics"] = dict(sorted_topics[:100])
    
    def _update_sentiment_analysis(self, sentiment):
        """تحديث تحليل المشاعر"""
        self.analysis_data["sentiment_analysis"][sentiment] += 1
    
    def _update_word_frequency(self, keywords):
        """تحديث تكرار الكلمات"""
        for keyword in keywords:
            if keyword in self.analysis_data["word_frequency"]:
                self.analysis_data["word_frequency"][keyword] += 1
            else:
                self.analysis_data["word_frequency"][keyword] = 1
        
        # الاحتفاظ فقط بأهم 200 كلمة
        sorted_words = sorted(self.analysis_data["word_frequency"].items(), key=lambda x: x[1], reverse=True)
        self.analysis_data["word_frequency"] = dict(sorted_words[:200])
    
    def _update_source_sentiment(self, source, sentiment):
        """تحديث تحليل المشاعر حسب المصدر"""
        if source not in self.analysis_data["source_sentiment"]:
            self.analysis_data["source_sentiment"][source] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }
        
        self.analysis_data["source_sentiment"][source][sentiment] += 1
    
    def get_trending_topics(self, limit=10):
        """الحصول على المواضيع الرائجة"""
        sorted_topics = sorted(self.analysis_data["trending_topics"].items(), key=lambda x: x[1], reverse=True)
        return sorted_topics[:limit]
    
    def get_sentiment_summary(self):
        """الحصول على ملخص تحليل المشاعر"""
        return self.analysis_data["sentiment_analysis"]
    
    def get_source_sentiment(self):
        """الحصول على تحليل المشاعر حسب المصدر"""
        return self.analysis_data["source_sentiment"]

# إنشاء كائن عام للتحليل
news_analyzer = NewsAnalyzer()