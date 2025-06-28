import requests
import feedparser
from sources import NEWS_SOURCES

print("فحص مصادر الأخبار...")

for source in NEWS_SOURCES:
    name = source['name']
    url = source['url']
    try:
        resp = requests.get(url, timeout=10)
        status = resp.status_code
        if status == 200:
            feed = feedparser.parse(resp.content)
            entries = len(feed.entries)
            print(f"✅ {name}: يعمل ({entries} خبر)")
        else:
            print(f"❌ {name}: HTTP {status}")
    except Exception as e:
        print(f"❌ {name}: خطأ - {e}")
