# cache_manager.py

import os
import hashlib
import time
import logging
import requests
from pathlib import Path
from config import CACHE_ENABLED, CACHE_DURATION, CACHE_DIR, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self.cache_dir = Path(CACHE_DIR)
        self.cache_enabled = CACHE_ENABLED
        self.cache_duration = CACHE_DURATION
        
        # إنشاء مجلد التخزين المؤقت إذا لم يكن موجوداً
        if self.cache_enabled:
            self.cache_dir.mkdir(exist_ok=True)
            logger.info(f"Cache manager initialized. Cache dir: {self.cache_dir}")
    
    def _get_cache_key(self, url: str) -> str:
        """إنشاء مفتاح فريد للرابط"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str, extension: str = '') -> Path:
        """الحصول على مسار ملف التخزين المؤقت"""
        filename = f"{cache_key}{extension}"
        return self.cache_dir / filename
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """التحقق من صحة ملف التخزين المؤقت"""
        if not cache_path.exists():
            return False
        
        # التحقق من عمر الملف
        file_age = time.time() - cache_path.stat().st_mtime
        return file_age < self.cache_duration
    
    def get_cached_image(self, url: str) -> str:
        """الحصول على الصورة من التخزين المؤقت أو تحميلها"""
        if not self.cache_enabled or not url:
            return url
        
        try:
            cache_key = self._get_cache_key(url)
            
            # البحث عن الملف في التخزين المؤقت
            for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                cache_path = self._get_cache_path(cache_key, ext)
                if self._is_cache_valid(cache_path):
                    logger.info(f"Cache hit for image: {url}")
                    return str(cache_path.absolute())
            
            # تحميل الصورة إذا لم تكن موجودة في التخزين المؤقت
            return self._download_and_cache_image(url, cache_key)
            
        except Exception as e:
            logger.error(f"Error in cache manager for {url}: {e}")
            return url
    
    def _download_and_cache_image(self, url: str, cache_key: str) -> str:
        """تحميل الصورة وحفظها في التخزين المؤقت"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
            response.raise_for_status()
            
            # تحديد امتداد الملف من نوع المحتوى
            content_type = response.headers.get('content-type', '').lower()
            if 'jpeg' in content_type or 'jpg' in content_type:
                extension = '.jpg'
            elif 'png' in content_type:
                extension = '.png'
            elif 'gif' in content_type:
                extension = '.gif'
            elif 'webp' in content_type:
                extension = '.webp'
            else:
                # محاولة استخراج الامتداد من الرابط
                extension = Path(url).suffix.lower()
                if extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    extension = '.jpg'  # افتراضي
            
            cache_path = self._get_cache_path(cache_key, extension)
            
            # حفظ الصورة
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Image cached: {url} -> {cache_path}")
            return str(cache_path.absolute())
            
        except Exception as e:
            logger.error(f"Failed to download and cache image {url}: {e}")
            return url
    
    def clear_old_cache(self):
        """حذف الملفات القديمة من التخزين المؤقت"""
        if not self.cache_enabled or not self.cache_dir.exists():
            return
        
        try:
            current_time = time.time()
            deleted_count = 0
            
            for file_path in self.cache_dir.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > self.cache_duration:
                        file_path.unlink()
                        deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Cleared {deleted_count} old cached files")
                
        except Exception as e:
            logger.error(f"Error clearing old cache: {e}")
    
    def get_cache_stats(self) -> dict:
        """الحصول على إحصائيات التخزين المؤقت"""
        if not self.cache_enabled or not self.cache_dir.exists():
            return {'enabled': False}
        
        try:
            files = list(self.cache_dir.iterdir())
            total_files = len([f for f in files if f.is_file()])
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            
            return {
                'enabled': True,
                'total_files': total_files,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'cache_dir': str(self.cache_dir),
                'cache_duration_hours': self.cache_duration / 3600
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {'enabled': True, 'error': str(e)}

# إنشاء مثيل عام لمدير التخزين المؤقت
cache_manager = CacheManager()