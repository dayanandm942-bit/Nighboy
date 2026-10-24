import os
import time
import random
import threading
from datetime import datetime, timedelta, timezone
from flask import Flask
from instagrapi import Client

app = Flask(__name__)

# ✅ तेरी डिटेल्स यहाँ फिट कर दी हैं भाई:
IG_USERNAME = "sujeetmishra9336"
IG_PASSWORD = "selected_reel.in"

# जिस पेज से रील उठानी है
TARGET_PAGE = "kh200.__"

cl = Client()
session_file = "/tmp/session.json"

def init_client():
    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(session_file)
        print("Logged in successfully bhai! ✅")
    except Exception as e:
        print(f"Login Error: {e}")

# 🔥 24/7 ALWAYS ONLINE + STORY WATCHER (Background Engine)
def always_online_loop():
    init_client()
    while True:
        try:
            # 1. टाइमलाइन रिफ्रेश करेगा ताकि 'Active Now' (हरा डॉट) हमेशा चालू रहे
            cl.get_timeline_feed()
            
            # 2. लोगों की स्टोरीज़ अपने आप 'Seen' करेगा
            reels_tray = cl.get_reels_tray_feed()
            for tray in reels_tray[:3]: # हर बार में 3 लोगों की स्टोरी देखेगा
                items = tray.get("items", [])
                if items:
                    media_ids = [item["pk"] for item in items]
                    cl.story_seen(media_ids)
            
            print("Online Ping Sent & Stories Watched! 🟢")
        except Exception as e:
            print(f"Loop Error: {e}")
            init_client()
            
        # हर 3 से 4 मिनट (180-240 सेकंड) में अपने आप चलेगा
        time.sleep(random.randint(180, 240))

# सर्वर स्टार्ट होते ही बैकग्राउंड में 24/7 लूप चालू कर देगा
threading.Thread(target=always_online_loop, daemon=True).start()

@app.route("/")
def home():
    return "Sujeet Bhai ka 24/7 Always Online + Night Owl Bot Live Hai! 🟢💻🔥"

# 🌙 रात को 2 AM, 3 AM, 4 AM पर अपने आप टाइम बदलकर स्टोरी डालने वाला लिंक
@app.route("/post-night-story")
def post_story():
    try:
        # 1. इंडिया का असली टाइम (IST) निकालना
        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_timezone)
        
        # यह अपने आप '2 AM', '3 AM', '4 AM' जैसा फॉर्मेट निकाल लेगा
        current_hour_str = now_ist.strftime("%-I %p") 
        
        # 2. @kh200.__ पेज से रैंडम रील उठाना
        user_id = cl.user_id_from_username(TARGET_PAGE)
        medias = cl.user_clips(user_id, amount=20)
        
        if not medias:
            return "भाई उस पेज से रील नहीं मिल पाई!"
            
        selected_reel = random.choice(medias)
        video_path = cl.clip_download(selected_reel.pk, folder="/tmp")
        
        # 3. टाइम के हिसाब से ऑटोमैटिक कैप्शन बदलना
        caption = f"Time update: It's {current_hour_str} but I can't sleep, learning computer coding... 💻🔥"
        
        cl.video_upload_to_story(video_path, caption=caption)
        
        if os.path.exists(video_path):
            os.remove(video_path)
            
        return f"Story Posted Successfully with time: {current_hour_str}! 🚀🔥"
    except Exception as e:
        return f"Story dalne me error aaya: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
