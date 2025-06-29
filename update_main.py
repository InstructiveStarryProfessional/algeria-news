# سكريبت إضافة كود self-ping إلى main.py
with open("main.py", "a", encoding="utf-8") as f:
    f.write("""

# --- Self-ping keep_alive thread ---
import threading
import time
import requests
import os

def keep_alive():
    url = os.getenv('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
    interval = 30
    while True:
        try:
            res = requests.get(url)
            print(f"Pinged at {time.strftime('%Y-%m-%d %H:%M:%S')}, status: {res.status_code}")
        except Exception as e:
            print(f"Error pinging: {e}")
        time.sleep(interval)

threading.Thread(target=keep_alive, daemon=True).start()
""")
print("تمت إضافة كود self-ping إلى main.py") 