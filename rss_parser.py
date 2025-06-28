# rss_parser.py

import feedparser
import logging
from datetime import datetime
from time import mktime
from urllib.parse import urljoin
import re

logger = logging.getLogger(__name__)

def extract_image_from_entry(entry, feed_url):
    """استخراج رابط الصورة من مدخل RSS."""
    # محاولة استخراج الصورة من حقول مختلفة
    # 1. البحث في حقل media_content
    if hasattr(entry, 'media_content') and entry.media_content:
        for media in entry.media_content:
            if 'url' in media:
                return media['url']
    
    # 2. البحث في حقل enclosures
    if hasattr(entry, 'enclosures') and entry.enclosures:
        for enclosure in entry.enclosures:
            if 'url' in enclosure and enclosure.get('type', '').startswith('image/'):
                return enclosure['url']
    
    # 3. البحث في حقل links
    if hasattr(entry, 'links'):
        for link in entry.links:
            if link.get('type', '').startswith('image/'):
                return link.get('href', '')
    
    # 4. البحث في محتوى المقال (summary أو content)
    content = getattr(entry, 'content', [{}])[0].get('value', '') if hasattr(entry, 'content') else ''
    if not content:
        content = getattr(entry, 'summary', '')
    
    # البحث عن وسوم الصور في المحتوى
    if content:
        img_match = re.search(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content)
        if img_match:
            img_url = img_match.group(1)
            # التأكد من أن الرابط كامل
            if not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(feed_url, img_url)
            return img_url
    
    # لم يتم العثور على صورة
    return ''

def parse_rss_feed(url):
    """Parses an RSS feed and returns a list of articles."""
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            # Get publication date
            published_time = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
            if published_time:
                published_date = datetime.fromtimestamp(mktime(published_time))
            else:
                published_date = datetime.now() # Fallback to current time

            # استخراج الصورة من المقال
            image_url = extract_image_from_entry(entry, url)

            articles.append({
                'title': getattr(entry, 'title', 'No Title'),
                'link': getattr(entry, 'link', ''),
                'summary': getattr(entry, 'summary', ''),
                'published_date': published_date,
                'source_name': feed.feed.get('title', 'Unknown Source'),
                'image_url': image_url
            })
        return articles
    except Exception as e:
        logger.error(f"Error parsing RSS feed {url}: {e}")
        return []