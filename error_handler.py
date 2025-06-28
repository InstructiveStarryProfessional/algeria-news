# error_handler.py

import time
import logging
import requests
from functools import wraps
from typing import Callable, Any, Optional
from config import MAX_RETRIES, RETRY_DELAY, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class NetworkError(Exception):
    """استثناء مخصص لأخطاء الشبكة"""
    pass

class RateLimitError(Exception):
    """استثناء مخصص لتجاوز حد الطلبات"""
    pass

def retry_on_failure(max_retries: int = None, delay: int = None, exceptions: tuple = None):
    """ديكوريتر لإعادة المحاولة عند الفشل"""
    if max_retries is None:
        max_retries = MAX_RETRIES
    if delay is None:
        delay = RETRY_DELAY
    if exceptions is None:
        exceptions = (requests.RequestException, NetworkError, ConnectionError, TimeoutError)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = delay * (2 ** attempt)  # تأخير متزايد
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {wait_time} seconds..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {e}"
                        )
                except Exception as e:
                    # أخطاء غير قابلة للإعادة
                    logger.error(f"Non-retryable error in {func.__name__}: {e}")
                    raise
            
            raise last_exception
        return wrapper
    return decorator

def safe_request(url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
    """طلب HTTP آمن مع معالجة الأخطاء"""
    try:
        # إعداد المهلة الزمنية والرؤوس الافتراضية
        kwargs.setdefault('timeout', REQUEST_TIMEOUT)
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('User-Agent', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # تنفيذ الطلب
        response = requests.request(method, url, **kwargs)
        
        # التحقق من رمز الاستجابة
        if response.status_code == 429:
            raise RateLimitError(f"Rate limit exceeded for {url}")
        elif response.status_code >= 500:
            raise NetworkError(f"Server error {response.status_code} for {url}")
        elif response.status_code >= 400:
            logger.warning(f"Client error {response.status_code} for {url}")
            return None
        
        response.raise_for_status()
        return response
        
    except requests.exceptions.Timeout:
        raise NetworkError(f"Timeout error for {url}")
    except requests.exceptions.ConnectionError:
        raise NetworkError(f"Connection error for {url}")
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Request error for {url}: {e}")

@retry_on_failure()
def safe_get(url: str, **kwargs) -> Optional[requests.Response]:
    """GET request آمن مع إعادة المحاولة"""
    return safe_request(url, 'GET', **kwargs)

@retry_on_failure()
def safe_post(url: str, **kwargs) -> Optional[requests.Response]:
    """POST request آمن مع إعادة المحاولة"""
    return safe_request(url, 'POST', **kwargs)

def handle_telegram_error(func: Callable) -> Callable:
    """ديكوريتر لمعالجة أخطاء التليجرام"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e).lower()
            
            if 'chat not found' in error_msg:
                logger.error("Telegram chat not found. Check channel ID.")
            elif 'bot was blocked' in error_msg:
                logger.error("Bot was blocked by user.")
            elif 'message is too long' in error_msg:
                logger.error("Message too long for Telegram.")
            elif 'file too large' in error_msg:
                logger.error("File too large for Telegram.")
            elif 'flood control' in error_msg or 'too many requests' in error_msg:
                logger.error("Telegram rate limit exceeded. Waiting...")
                time.sleep(60)  # انتظار دقيقة
            else:
                logger.error(f"Telegram error in {func.__name__}: {e}")
            
            # إعادة رفع الاستثناء للمعالجة في مستوى أعلى
            raise
    return wrapper

def log_error(error: Exception, context: str = ""):
    """تسجيل الأخطاء بتفاصيل مفيدة"""
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        logger.error(f"[{context}] {error_type}: {error_msg}")
    else:
        logger.error(f"{error_type}: {error_msg}")
    
    # تسجيل تفاصيل إضافية للأخطاء المهمة
    if isinstance(error, (NetworkError, RateLimitError)):
        logger.error(f"Network issue detected. Consider checking connectivity.")
    elif isinstance(error, FileNotFoundError):
        logger.error(f"File not found. Check file paths and permissions.")
    elif isinstance(error, PermissionError):
        logger.error(f"Permission denied. Check file/directory permissions.")

def setup_error_logging():
    """إعداد نظام تسجيل الأخطاء"""
    # إعداد تنسيق الرسائل
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # إعداد معالج الملف
    file_handler = logging.FileHandler('bot_errors.log', encoding='utf-8')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    
    # إعداد معالج وحدة التحكم
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # إعداد المسجل الجذر
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger.info("Error logging system initialized")

class ErrorStats:
    """إحصائيات الأخطاء"""
    def __init__(self):
        self.error_counts = {}
        self.last_errors = []
        self.max_last_errors = 50
    
    def record_error(self, error: Exception, context: str = ""):
        """تسجيل خطأ في الإحصائيات"""
        error_type = type(error).__name__
        
        # عد الأخطاء حسب النوع
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # حفظ آخر الأخطاء
        error_info = {
            'timestamp': time.time(),
            'type': error_type,
            'message': str(error),
            'context': context
        }
        
        self.last_errors.append(error_info)
        if len(self.last_errors) > self.max_last_errors:
            self.last_errors.pop(0)
    
    def get_stats(self) -> dict:
        """الحصول على إحصائيات الأخطاء"""
        return {
            'error_counts': self.error_counts,
            'total_errors': sum(self.error_counts.values()),
            'recent_errors': len(self.last_errors),
            'last_errors': self.last_errors[-10:]  # آخر 10 أخطاء
        }

# إنشاء مثيل عام لإحصائيات الأخطاء
error_stats = ErrorStats()