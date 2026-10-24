import os
import time
import random
import threading
from datetime import datetime, timedelta, timezone
from flask import Flask
from instagrapi import Client
import instagrapi.config
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

IG_USERNAME = "sujeetmishra9336"
IG_PASSWORD = "selected_reel.in"

# 🛠️ ब्रह्मास्त्र हैक: instagrapi के अंदर के पुराने वर्ज़न को जड़ से बदलना
LATEST_DEVICE = {
    "app_version": "345.0.0.34.109",
    "android_version": 34,
    "android_release": "14",
    "dpi": "480dpi",
    "resolution": "1080x2400",
    "manufacturer": "Google",
    "device": "husky",
    "model": "Pixel 8 Pro",
    "cpu": "tensor",
    "version_code": "621552483",
}
LATEST_UA = "Instagram 345.0.0.34.109 Android (34/14; 480dpi; 1080x2400; Google/google; Pixel 8 Pro; husky; husky; en_US; 621552483)"

# लाइब्रेरी की मेन मेमोरी को ओवरराइट करना ताकि वो रीसेट न कर सके
for k in instagrapi.config.DEVICES:
    instagrapi.config.DEVICES[k] = LATEST_DEVICE

cl = Client()
session_file = "/tmp/session.json"
is_logged_in = False
last_login_error = "Abhi login try nahi hua"

def init_client():
    global is_logged_in, last_login_error, cl
    try:
        if os.path.exists(session_file):
            os.remove(session_file)
            
        cl = Client(settings={
            "device_settings": LATEST_DEVICE,
            "user_agent": LATEST_UA
        })
        cl.set_device(LATEST_DEVICE)
        cl.set_user_agent(LATEST_UA)
        
        # relogin=False रखने से यह हमारी डिवाइस सेटिंग को कभी रीसेट नहीं करेगा!
        cl.login(IG_USERNAME, IG_PASSWORD, relogin=False)
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
        if not is_logged_in:
            success = init_client()
            if not success:
                return f"❌ LOGIN FAIL HUA BHAI: {last_login_error}"

        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_timezone)
        current_hour_str = now_ist.strftime("%-I %p") 
        
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
        
        cl.photo_upload_to_story(photo_path, caption="Night grind! 🔥")
        
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
        return f"✅ SUCCESS: Photo Story Posted with time: {current_hour_str}! 🚀🔥"
    
    except Exception as e:
        return f"❌ UPLOAD ERROR aaya bhai: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
