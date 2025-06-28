# bot.py

import asyncio
import logging
import datetime
import time
from telegram import Bot, InputMediaPhoto, InputMediaVideo, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, filters, MessageHandler, CallbackQueryHandler
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from utils import clean_html, format_date, enhance_title, create_hashtags, prepare_article_content
from media_handler import extract_video_url, is_youtube_url, get_video_thumbnail
from stats import bot_stats
from notifications import notification_manager
from nlp_analyzer import news_analyzer
from cache_manager import cache_manager
from error_handler import handle_telegram_error, retry_on_failure, log_error, error_stats, setup_error_logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# تم حذف أوامر التشغيل - البوت يعمل تلقائياً الآن

async def stats_command(update, context):
    """عرض إحصائيات البوت."""
    stats = bot_stats.get_summary()
    
    # إنشاء لوحة مفاتيح للتنقل بين الإحصائيات
    keyboard = [
        [InlineKeyboardButton("📊 الإحصائيات العامة", callback_data="stats_general")],
        [InlineKeyboardButton("📈 المواضيع الرائجة", callback_data="stats_trending")],
        [InlineKeyboardButton("😊 تحليل المشاعر", callback_data="stats_sentiment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # تنسيق الإحصائيات
    text = "📊 *إحصائيات بوت أخبار الجزائر* 📊\n\n"
    text += f"📰 *إجمالي الأخبار المنشورة:* {stats['total_articles']}\n"
    text += f"📆 *عدد أيام التشغيل:* {stats['days_running']}\n"
    text += f"📈 *متوسط الأخبار اليومي:* {stats['avg_per_day']}\n"
    text += f"👥 *عدد المشتركين:* {notification_manager.get_subscribers_count()}\n\n"
    
    # أكثر المصادر نشاطاً
    text += "🔝 *أكثر المصادر نشاطاً:*\n"
    for source, count in stats['top_sources']:
        text += f"  • {source}: {count} خبر\n"
    
    text += "\n📋 *الأخبار حسب التصنيف:*\n"
    for category, count in stats['top_categories']:
        text += f"  • {category}: {count} خبر\n"
    
    text += f"\n🕒 *آخر تحديث:* {stats['last_update']}\n"
    text += "\n👇 اختر من القائمة أدناه لعرض المزيد من الإحصائيات"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

async def stats_callback(update, context):
    """معالجة الضغط على أزرار الإحصائيات"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "stats_general":
        # إعادة عرض الإحصائيات العامة
        await stats_command(update, context)
    
    elif query.data == "stats_trending":
        # عرض المواضيع الرائجة
        trending_topics = news_analyzer.get_trending_topics(15)
        
        text = "📈 *المواضيع الرائجة في الأخبار* 📈\n\n"
        
        for i, (topic, count) in enumerate(trending_topics, 1):
            text += f"{i}. *{topic}*: {count} مرة\n"
        
        if not trending_topics:
            text += "لا توجد مواضيع رائجة حتى الآن.\n"
        
        # إضافة زر للعودة
        keyboard = [[InlineKeyboardButton("🔙 العودة للإحصائيات العامة", callback_data="stats_general")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    elif query.data == "stats_sentiment":
        # عرض تحليل المشاعر
        sentiment = news_analyzer.get_sentiment_summary()
        source_sentiment = news_analyzer.get_source_sentiment()
        
        total = sentiment["positive"] + sentiment["negative"] + sentiment["neutral"]
        if total > 0:
            pos_percent = round((sentiment["positive"] / total) * 100)
            neg_percent = round((sentiment["negative"] / total) * 100)
            neu_percent = round((sentiment["neutral"] / total) * 100)
        else:
            pos_percent = neg_percent = neu_percent = 0
        
        text = "😊 *تحليل المشاعر في الأخبار* 😊\n\n"
        text += f"*التوزيع العام للمشاعر:*\n"
        text += f"😃 إيجابي: {sentiment['positive']} ({pos_percent}%)\n"
        text += f"😡 سلبي: {sentiment['negative']} ({neg_percent}%)\n"
        text += f"😐 محايد: {sentiment['neutral']} ({neu_percent}%)\n\n"
        
        text += "*تحليل المشاعر حسب المصدر:*\n"
        for source, data in list(source_sentiment.items())[:5]:  # أخذ أول 5 مصادر فقط
            total_source = data["positive"] + data["negative"] + data["neutral"]
            if total_source > 0:
                pos_percent = round((data["positive"] / total_source) * 100)
                neg_percent = round((data["negative"] / total_source) * 100)
                neu_percent = round((data["neutral"] / total_source) * 100)
                
                text += f"*{source}*: 😃 {pos_percent}% | 😡 {neg_percent}% | 😐 {neu_percent}%\n"
        
        # إضافة زر للعودة
        keyboard = [[InlineKeyboardButton("🔙 العودة للإحصائيات العامة", callback_data="stats_general")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

async def start_command(update, context):
    """بدء البوت والاشتراك في الإشعارات."""
    user = update.effective_user
    added = notification_manager.add_user(user.id)
    
    if added:
        await update.message.reply_text(
            f"👋 أهلاً بك يا {user.first_name}!\n\n"
            "أنا بوت أخبار الجزائر، سأبقيك على اطلاع بآخر الأخبار من مصادر موثوقة.\n\n"
            "تم اشتراكك بنجاح في نظام الإشعارات الفورية. ✅\n"
            "لإلغاء الاشتراك في أي وقت، استخدم الأمر /unsubscribe.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            f"أهلاً بعودتك يا {user.first_name}! أنت مشترك بالفعل. 👍\n\n"
            "لا داعي للاشتراك مرة أخرى. ستصلك آخر الأخبار فور ورودها."
        )

async def subscribe_command(update, context):
    """الاشتراك في نظام الإشعارات."""
    user = update.effective_user
    added = notification_manager.add_user(user.id)
    
    if added:
        await update.message.reply_text("تم اشتراكك في نظام الإشعارات بنجاح. ✅")
    else:
        await update.message.reply_text("أنت مشترك بالفعل. 👍")

async def unsubscribe_command(update, context):
    """إلغاء الاشتراك من نظام الإشعارات."""
    user = update.effective_user
    removed = notification_manager.remove_user(user.id)
    
    if removed:
        await update.message.reply_text("تم إلغاء اشتراكك من نظام الإشعارات بنجاح. ✅\n\nيمكنك الاشتراك مجدداً في أي وقت باستخدام الأمر /start")
    else:
        await update.message.reply_text("أنت غير مشترك في نظام الإشعارات. استخدم الأمر /start للاشتراك.")

async def trends_command(update, context):
    """عرض المواضيع الرائجة."""
    trending_topics = news_analyzer.get_trending_topics(10)
    
    text = "📈 *المواضيع الرائجة في الأخبار* 📈\n\n"
    
    for i, (topic, count) in enumerate(trending_topics, 1):
        text += f"{i}. *{topic}*: {count} مرة\n"
    
    if not trending_topics:
        text += "لا توجد مواضيع رائجة حتى الآن.\n"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def main() -> None:
    """Run the bot."""
    # إعداد نظام تسجيل الأخطاء
    setup_error_logging()
    
    # إنشاء التطبيق
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("subscribe", subscribe_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_handler(CommandHandler("trends", trends_command))
    
    # إضافة معالج للأزرار التفاعلية
    application.add_handler(CallbackQueryHandler(stats_callback, pattern='^stats_'))
    application.add_handler(CallbackQueryHandler(read_more_callback, pattern='^read_more:'))


    # جدولة مهمة جمع الأخبار كل 30 ثانية
    job_queue = application.job_queue
    job_queue.run_repeating(fetch_and_send_news, interval=30, first=10) # 30 seconds
    
    # جدولة تنظيف التخزين المؤقت كل ساعة
    job_queue.run_repeating(lambda context: cache_manager.clear_old_cache(), interval=3600, first=3600)

    logger.info("🚀 بوت أخبار الجزائر بدأ العمل تلقائياً...")
    logger.info("📰 سيتم جلب الأخبار فور صدورها ونشرها كل 30 ثانية")
    logger.info("🗂️ سيتم تنظيف التخزين المؤقت كل ساعة")
    
    # تشغيل البوت حتى يضغط المستخدم Ctrl-C
    application.run_polling()

def diversify_articles_by_source(articles):
    """تنويع المقالات لتجنب التكرار من نفس المصدر متتالياً."""
    if not articles:
        return []
    
    # تجميع المقالات حسب المصدر
    articles_by_source = {}
    for article in articles:
        source_name = article.source
        if source_name not in articles_by_source:
            articles_by_source[source_name] = []
        articles_by_source[source_name].append(article)
    
    # ترتيب المصادر حسب عدد المقالات (الأقل أولاً لضمان التنويع)
    sorted_sources = sorted(articles_by_source.keys(), 
                           key=lambda x: len(articles_by_source[x]))
    
    # توزيع المقالات بالتناوب بين المصادر
    diversified = []
    max_articles = max(len(articles_by_source[source]) for source in sorted_sources)
    
    for i in range(max_articles):
        for source in sorted_sources:
            if i < len(articles_by_source[source]):
                diversified.append(articles_by_source[source][i])
    
    return diversified

async def process_source(source, session):
    """معالجة مصدر أخبار واحد لجلب وحفظ المقالات الجديدة."""
    from rss_parser import parse_rss_feed
    from web_scraper import scrape_website, scrape_article_content
    from database import Article
    from nlp_analyzer import news_analyzer
    from classifier import classify_article
    from media_handler import extract_video_url

    new_articles = []
    try:
        logger.info(f"معالجة المصدر: {source['name']} - الأولوية: {source.get('priority', 'غير محددة')}")
        
        articles_data = []
        if source['type'] == 'rss':
            articles_data = parse_rss_feed(source['url'])
        elif source['type'] == 'scrape':
            articles_data = scrape_website(source)

        # فلترة المقالات حسب التاريخ (آخر 24 ساعة فقط)
        twenty_four_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        
        for article_data in articles_data:
            # التحقق من عدم وجود المقال مسبقاً
            exists = session.query(Article).filter_by(link=article_data['link']).first()
            if not exists:
                # فلترة الأخبار القديمة (أكثر من 24 ساعة)
                if article_data['published_date'] < twenty_four_hours_ago:
                    logger.debug(f"تجاهل مقال قديم: {article_data['title']}")
                    continue
                    
                logger.info(f"معالجة مقال جديد: {article_data['title']}")

                # استخراج المحتوى الكامل
                full_content = scrape_article_content(article_data['link'], source.get('scraping_config'))
                summary = full_content if full_content else article_data['summary']
                
                # تصنيف المقال
                category = classify_article(article_data['title'], summary)
                
                # إذا كان المصدر له فئة محددة، استخدمها
                if 'category' in source:
                    category = source['category']
                
                # تحليل المشاعر
                sentiment_score = news_analyzer.analyze_sentiment(article_data['title'] + " " + summary)

                # إنشاء مقال جديد
                new_article = Article(
                    title=article_data['title'],
                    sentiment_score=sentiment_score,
                    link=article_data['link'],
                    source=article_data['source_name'],
                    published_date=article_data['published_date'],
                    category=category,
                    image_url=article_data.get('image_url', ''),
                    summary=summary
                )
                session.add(new_article)
                new_articles.append(new_article)

        if new_articles:
            session.flush() # Flush to get IDs for new articles
            for article in new_articles:
                session.refresh(article) # Refresh to get the ID
            logger.info(f"تم العثور على {len(new_articles)} مقال جديد من {source['name']}")
        else:
            logger.debug(f"لا توجد مقالات جديدة من {source['name']}")
            
    except Exception as e:
        log_error(e, f"خطأ في معالجة المصدر: {source['name']}")
        error_stats.record_error(e, f"source_{source['name']}")
        logger.error(f"فشل في معالجة المصدر {source['name']}: {str(e)}")
    
    return new_articles

async def fetch_and_send_news(context):
    """جلب الأخبار من المصادر وإرسالها للتليجرام مع تطبيق الأولويات والتنويع."""
    from sources import NEWS_SOURCES, get_source_by_name
    from database import get_db_session, get_random_unsent_high_sentiment_article

    logger.info("🔄 بدء دورة جلب الأخبار الجديدة...")
    session = get_db_session()
    
    # معالجة المصادر بشكل متزامن
    tasks = [process_source(source, session) for source in NEWS_SOURCES]
    results = await asyncio.gather(*tasks)
    
    # تجميع جميع المقالات الجديدة
    all_new_articles = [article for sublist in results for article in sublist]
    
    # فلترة الأخبار للـ 24 ساعة الماضية فقط
    twenty_four_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    recent_articles = [article for article in all_new_articles 
                      if article.published_date >= twenty_four_hours_ago]
    
    if recent_articles:
        session.commit()
        logger.info(f"تم العثور على {len(recent_articles)} مقال جديد خلال آخر 24 ساعة")
    else:
        session.rollback()
        logger.info("لم يتم العثور على أخبار جديدة خلال آخر 24 ساعة")

    # ترتيب وتنويع الأخبار حسب الأولوية
    if recent_articles:
        # تصنيف الأخبار حسب الأولوية
        urgent_news = []
        local_news = []  # أخبار محلية جزائرية
        official_news = []
        economic_news = []
        sports_news = []
        other_news = []

        urgent_keywords = ['عاجل', 'طارئ', 'انفجار', 'حادث', 'وفاة', 'استقالة', 'إعلان هام', 'قرار عاجل']
        
        for article in recent_articles:
            title_lower = article.title.lower()
            source_country = get_source_by_name(article.source).get('country', 'Unknown')

            if any(keyword in title_lower for keyword in urgent_keywords):
                urgent_news.append(article)
            elif source_country == 'DZ':
                local_news.append(article)
            elif article.category == 'official':
                official_news.append(article)
            elif article.category in ['economic', 'اقتصاد']:
                economic_news.append(article)
            elif article.category in ['sports', 'رياضة']:
                sports_news.append(article)
            else:
                other_news.append(article)

        # ترتيب الأخبار حسب الأولوية مع التنويع
        prioritized_articles = []
        prioritized_articles.extend(urgent_news)
        prioritized_articles.extend(diversify_articles_by_source(local_news))
        
        remaining_articles = official_news + economic_news + other_news + sports_news
        diversified_articles = diversify_articles_by_source(remaining_articles)
        prioritized_articles.extend(diversified_articles)

        logger.info(f"إرسال {len(prioritized_articles)} مقال مع ترتيب الأولوية والتنويع")
        logger.info(f"الأخبار العاجلة: {len(urgent_news)}, المحلية: {len(local_news)}, الرسمية: {len(official_news)}, الاقتصادية: {len(economic_news)}, الرياضية: {len(sports_news)}, أخرى: {len(other_news)}")
        
        # إرسال المقالات مع فترات زمنية مناسبة
        # أولاً: إرسال الأخبار العاجلة المحلية فقط كل 30 ثانية
        urgent_local_news = [a for a in urgent_news if a in local_news]
        other_news = [a for a in prioritized_articles if a not in urgent_local_news]

        for i, article in enumerate(urgent_local_news):
            try:
                await send_article_to_telegram(context.bot, article)
                article.sent_to_telegram = True
                session.commit()
                bot_stats.add_article(article.source, article.category)
                await notification_manager.notify_users(article, article.category)
                logger.info("انتظار 30 ثانية (خبر عاجل محلي) قبل إرسال الخبر التالي")
                await asyncio.sleep(30)
            except Exception as e:
                log_error(e, f"فشل في معالجة المقال: {article.title}")
                error_stats.record_error(e, "send_article_loop")
                session.rollback()

        # ثم: إرسال بقية الأخبار (العالمية والمحلية غير العاجلة) بفاصل 30 ثانية بين كل خبر
        for i, article in enumerate(other_news):
            try:
                await send_article_to_telegram(context.bot, article)
                article.sent_to_telegram = True
                session.commit()
                bot_stats.add_article(article.source, article.category)
                await notification_manager.notify_users(article, article.category)
                logger.info("انتظار 30 ثانية قبل إرسال الخبر التالي")
                await asyncio.sleep(30)
            except Exception as e:
                log_error(e, f"فشل في معالجة المقال: {article.title}")
                error_stats.record_error(e, "send_article_loop")
                session.rollback()
    logger.info(f"انتهاء دورة جلب الأخبار. تم العثور على {len(recent_articles) if recent_articles else 0} مقال جديد")
    
    # تسجيل إحصائيات الأخطاء
    error_summary = error_stats.get_stats()
    if error_summary['total_errors'] > 0:
        logger.warning(f"إجمالي الأخطاء في هذه الدورة: {error_summary['total_errors']}")

    # إذا لم يتم العثور على أخبار جديدة، جرب إرسال مقال عشوائي بمشاعر إيجابية
    if not recent_articles:
        logger.info("لم يتم العثور على أخبار جديدة. البحث عن مقالات غير مرسلة بمشاعر إيجابية...")
        session = get_db_session()
        random_article = get_random_unsent_high_sentiment_article(session)
        if random_article:
            logger.info(f"إرسال مقال عشوائي بمشاعر إيجابية: {random_article.title}")
            await send_article_to_telegram(context.bot, random_article)
            random_article.sent_to_telegram = True # Mark as sent
            session.commit()
        else:
            logger.info("No high-sentiment unsent articles found in the last 24 hours.")
        session.close()

async def read_more_callback(update: Update, context: CallbackContext):
    """Callback function for the 'Read More' button."""
    query = update.callback_query
    article_id = query.data.split(':')[1]
    try:
        article_id_int = int(article_id)
    except Exception as e:
        logger.error(f"خطأ في تحويل article_id إلى int: {article_id} - {e}")
        await query.answer(text="خطأ داخلي في قراءة المزيد.", show_alert=True)
        return

    from database import get_db_session, Article
    session = get_db_session()
    article = session.query(Article).filter_by(id=article_id_int).first()
    logger.info(f"زر قراءة المزيد: article_id={article_id}, موجود في قاعدة البيانات: {bool(article)}")
    session.close()

    if article:
        await query.answer()
        # إرسال المحتوى الكامل للمستخدم الذي ضغط على الزر
        await query.message.reply_text(
            text=f"<b>{article.title}</b>\n\n{article.summary}",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        await query.answer(text="عذراً، لم يتم العثور على هذا الخبر.", show_alert=True)

async def send_article_to_telegram(bot, article):
    """تنسيق وإرسال مقال واحد إلى قناة التليجرام مع عرض محسن للمحتوى."""
    from classifier import classify_article, get_emoji_for_category

    category = classify_article(article.title, article.summary)
    category_emoji = get_emoji_for_category(category)

    # تنظيف وتحسين النصوص
    title = enhance_title(article.title)
    
    # تحسين عرض المحتوى - عرض ملخص مناسب بدلاً من المحتوى الكامل
    from sources import get_source_by_name
    source_config = get_source_by_name(article.source)
    unwanted_phrases = source_config.get('scraping_config', {}).get('unwanted_phrases', [])
    content = prepare_article_content(article.summary, article.title, unwanted_phrases)

    # إنشاء الهاشتاجات
    hashtags = create_hashtags(article.title, content, article.source, category)

    # تنسيق الرسالة المحسن
    message = f"{category_emoji} <b>{title}</b>\n\n"
    
    # إضافة المحتوى فقط إذا كان مفيداً ومختصراً
    if content and len(content.strip()) > 20:
        message += f"{content}\n\n"
    
    message += f"<a href='{article.link}'>🔗 المصدر: {article.source}</a>\n"
    message += f"📅 {format_date(article.published_date)}\n\n"
    message += f"{hashtags}"

    text = message

    try:
        # التحقق من وجود محتوى مرئي (فيديو أو صورة)
        video_url = extract_video_url(article.link)
        has_media = bool(article.image_url or video_url)
        
        # إذا كان هناك فيديو مباشر (ليس يوتيوب)، نرسله مع النص
        if video_url and not is_youtube_url(video_url):
            try:
                await bot.send_video(
                    chat_id=TELEGRAM_CHANNEL_ID,
                    video=video_url,
                    caption=text,
                    parse_mode=ParseMode.HTML
                )
                logger.info(f"تم إرسال مقال مع فيديو: {title}")
                return
            except Exception as e:
                logger.error(f"فشل في إرسال الفيديو للمقال {title}: {e}")
                # في حالة فشل إرسال الفيديو، نستمر لإرسال الخبر مع الصورة أو بدونها
        
        # إذا كان هناك فيديو يوتيوب، نضيف رابطه في النص
        if video_url and is_youtube_url(video_url):
            text += f"\n\n🎬 <a href='{video_url}'>شاهد الفيديو</a>"
        
        # إذا كان هناك صورة، نرسلها مع الخبر
        image_url = article.image_url
        
        # إذا لم تكن هناك صورة ولكن هناك فيديو يوتيوب، نستخدم صورة الفيديو المصغرة
        if not image_url and video_url and is_youtube_url(video_url):
            image_url = get_video_thumbnail(video_url)
        
        # استخدام التخزين المؤقت للصور
        if image_url:
            cached_image = cache_manager.get_cached_image(image_url)
            image_url = cached_image
        
        await _send_telegram_message(bot, image_url, text, title, category, article.id, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        log_error(e, f"send_article_to_telegram: {title}")
        error_stats.record_error(e, "send_article_to_telegram")
        # محاولة إرسال بدون صورة في حالة فشل إرسال الصورة
        try:
            await _send_telegram_message(bot, None, text, title, category, article.id)
        except Exception as e2:
            log_error(e2, f"send_article_to_telegram_fallback: {title}")
            error_stats.record_error(e2, "send_article_to_telegram_fallback")

@handle_telegram_error
@retry_on_failure(max_retries=2)
async def _send_telegram_message(bot, image_url, text, title, category, article_id, parse_mode=ParseMode.HTML):
    """إرسال رسالة إلى التليجرام مع معالجة الأخطاء"""
    keyboard = [[InlineKeyboardButton("📰 قراءة المزيد", callback_data=f'read_more:{article_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if image_url:
        # إرسال الصورة مع النص
        await bot.send_photo(
            chat_id=TELEGRAM_CHANNEL_ID,
            photo=image_url,
            caption=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        logger.info(f"تم إرسال مقال مع صورة: {title} (الفئة: {category})")
    else:
        # إرسال نص فقط مع معاينة الرابط
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=False,  # إظهار معاينة الرابط
            reply_markup=reply_markup
        )
        logger.info(f"تم إرسال مقال نصي: {title} (الفئة: {category})")


if __name__ == "__main__":
    asyncio.run(main())