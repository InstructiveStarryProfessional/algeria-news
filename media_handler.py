# media_handler.py

import logging
import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def is_valid_url(url):
    """
    التحقق من صحة الرابط
    """
    if not url:
        return False
        
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def extract_video_url(article_url):
    """
    استخراج رابط الفيديو من صفحة المقال إن وجد
    """
    if not is_valid_url(article_url):
        return None
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # البحث عن وسوم الفيديو
        video_tag = soup.find('video')
        if video_tag and video_tag.get('src'):
            video_url = video_tag.get('src')
            if not video_url.startswith(('http://', 'https://')):
                video_url = urljoin(article_url, video_url)
            return video_url
            
        # البحث عن وسوم iframe (يوتيوب، فيسبوك، إلخ)
        iframe = soup.find('iframe', src=re.compile(r'(youtube|facebook|twitter|vimeo)'))
        if iframe and iframe.get('src'):
            return iframe.get('src')
            
        # البحث عن روابط الفيديو في الصفحة
        video_links = soup.find_all('a', href=re.compile(r'\.(mp4|avi|mov|wmv)$'))
        if video_links:
            video_url = video_links[0].get('href')
            if not video_url.startswith(('http://', 'https://')):
                video_url = urljoin(article_url, video_url)
            return video_url
            
        # البحث عن روابط يوتيوب
        youtube_links = soup.find_all('a', href=re.compile(r'youtube\.com/watch|youtu\.be/'))
        if youtube_links:
            return youtube_links[0].get('href')
            
        return None
    except Exception as e:
        logger.error(f"Error extracting video URL from {article_url}: {e}")
        return None

def is_youtube_url(url):
    """
    التحقق مما إذا كان الرابط هو رابط يوتيوب
    """
    if not url:
        return False
        
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+'
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def extract_youtube_id(url):
    """
    استخراج معرف فيديو يوتيوب من الرابط
    """
    if not url:
        return None
        
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([\w-]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([\w-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([\w-]+)'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
            
    return None

def get_video_thumbnail(video_url):
    """
    الحصول على صورة مصغرة للفيديو
    """
    if not video_url:
        return None
        
    # إذا كان الفيديو من يوتيوب
    youtube_id = extract_youtube_id(video_url)
    if youtube_id:
        return f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"
        
    # للفيديوهات الأخرى، نعيد رابط الفيديو نفسه
    return video_url