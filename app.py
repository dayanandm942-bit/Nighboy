import os
import time
import random
import threading
from datetime import datetime, timedelta, timezone
from flask import Flask
from instagrapi import Client

app = Flask(__name__)

# ✅ यूज़रनेम और पासवर्ड (Render/GitHub के लिए)
IG_USERNAME = "sujeetmishra9336"
IG_PASSWORD = "selected_reel.in"

TARGET_PAGE = "kh200.__"

cl = Client()
session_file = "/tmp/session.json"

def init_client():
    try:
        # डिवाइस को थोड़ा नॉर्मल फोन जैसा दिखाना 
        cl.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "Xiaomi",
            "device": "chiron",
            "model": "Mi MIX 2",
            "cpu": "qcom",
            "version_code": "314665256"
        })
        
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(session_file)
        print("Logged in successfully bhai! ✅")
    except Exception as e:
        print(f"Login Error: {e}")

# 🔥 24/7 ALWAYS ONLINE (हरा डॉट)
def always_online_loop():
    init_client()
    while True:
        try:
            cl.get_timeline_feed()
            print("Online Ping Sent! 🟢")
        except Exception as e:
            print(f"Loop Error: {e}")
            init_client()
        # बैन से बचने के लिए 20 से 35 मिनट का रैंडम गैप
        time.sleep(random.randint(1200, 2100)) 

threading.Thread(target=always_online_loop, daemon=True).start()

# 🌐 मेन होमपेज
@app.route("/")
def home():
    return "Sujeet Bhai ka 24/7 Always Online + Night Owl Bot Live Hai! 🟢💻🔥"

# 🤖 24/7 जगाए रखने के लिए UptimeRobot का स्पेशल रूट
@app.route("/ping")
def ping():
    return "Bot is awake and running! 🟢", 200

@app.route("/post-night-story")
def post_story():
    try:
        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_timezone)
        current_hour_str = now_ist.strftime("%-I %p") 
        
        user_id = cl.user_id_from_username(TARGET_PAGE)
        medias = cl.user_clips(user_id, amount=5) 
        
        if not medias:
            return "भाई उस पेज से रील नहीं मिल पाई!"
            
        selected_reel = random.choice(medias)
        video_path = cl.clip_download(selected_reel.pk, folder="/tmp")
        
        time.sleep(random.randint(15, 25))
        
        caption = f"Time update: It's {current_hour_str} but I can't sleep, learning computer coding... 💻🔥"
        
        cl.video_upload_to_story(video_path, caption=caption)
        
        if os.path.exists(video_path):
            os.remove(video_path)
            
        return f"✅ SUCCESS: Story Posted Successfully with time: {current_hour_str}! 🚀🔥"
    
    except Exception as e:
        return f"❌ ERROR aaya bhai: {str(e)} <br><br> (Full detail: {repr(e)})"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
