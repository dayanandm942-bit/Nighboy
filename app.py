import os
import time
import random
import threading
from datetime import datetime, timedelta, timezone
from flask import Flask
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

IG_USERNAME = "sujeetmishra9336"
IG_PASSWORD = "selected_reel.in"

cl = Client()
session_file = "/tmp/session.json"
is_logged_in = False
last_login_error = "Abhi login try nahi hua"

def setup_latest_device():
    # 📱 2026 का एकदम लेटेस्ट Android 14 (Samsung S24 Ultra) सेटअप
    cl.set_device({
        "app_version": "410.0.0.0.96",
        "android_version": 34,
        "android_release": "14.0",
        "dpi": "480dpi",
        "resolution": "1080x2340",
        "manufacturer": "Samsung",
        "device": "SM-S928B",
        "model": "SM-S928B",
        "cpu": "qcom",
        "version_code": "654321987"
    })
    # 🚨 सबसे ज़रूरी: User-Agent बदलना ताकि "Out of date" एरर कभी न आए!
    cl.set_user_agent("Instagram 410.0.0.0.96 Android (34/14.0; 480dpi; 1080x2340; Samsung; SM-S928B; SM-S928B; qcom; en_US; 654321987)")

def init_client():
    global is_logged_in, last_login_error
    try:
        if os.path.exists(session_file):
            os.remove(session_file)
            
        setup_latest_device()
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings(session_file)
        is_logged_in = True
        last_login_error = "None"
        print("Logged in successfully bhai! ✅")
        return True
    except Exception as e:
        is_logged_in = False
        last_login_error = str(e)
        print(f"Login Error: {e}")
        return False

# 🔥 24/7 ALWAYS ONLINE (हरा डॉट)
def always_online_loop():
    init_client()
    while True:
        try:
            if not is_logged_in:
                init_client()
            if is_logged_in:
                cl.get_timeline_feed()
                print("Online Ping Sent! 🟢")
        except Exception as e:
            print(f"Loop Error: {e}")
            init_client()
        time.sleep(random.randint(180, 240))

threading.Thread(target=always_online_loop, daemon=True).start()

@app.route("/")
def home():
    status = "LOGGED IN ✅" if is_logged_in else f"NOT LOGGED IN ❌ (Error: {last_login_error})"
    return f"Sujeet Bhai ka Bot Live Hai! <br><br> <b>Instagram Status:</b> {status}"

@app.route("/post-night-story")
def post_story():
    global is_logged_in
    try:
        # 1. अगर लॉग-इन नहीं है, तो अभी तुरंत लॉग-इन ट्राई करो
        if not is_logged_in:
            success = init_client()
            if not success:
                return f"❌ LOGIN FAIL HUA BHAI: {last_login_error}"

        # 2. टाइम निकालना (IST)
        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_timezone)
        current_hour_str = now_ist.strftime("%-I %p") 
        
        # 3. ब्लैक स्क्रीन फोटो बनाना
        img = Image.new('RGB', (1080, 1920), color=(15, 15, 15)) 
        d = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.load_default(size=70)
        except:
            font = ImageFont.load_default()
        
        text = f"Time update: It's {current_hour_str}\n\nBut I can't sleep...\nLearning computer coding 💻🔥"
        
        bbox = d.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (1080 - w) / 2
        y = (1920 - h) / 2
        
        d.multiline_text((x, y), text, fill=(0, 255, 0), font=font, align="center")
        
        photo_path = "/tmp/night_story.jpg"
        img.save(photo_path)
        
        time.sleep(3)
        
        # 4. स्टोरी अपलोड
        cl.photo_upload_to_story(photo_path, caption="Night grind! 🔥")
        
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
        return f"✅ SUCCESS: Photo Story Posted with time: {current_hour_str}! 🚀🔥"
    
    except Exception as e:
        return f"❌ UPLOAD ERROR aaya bhai: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
