import os
import time
import random
import threading
from datetime import datetime, timedelta, timezone
from flask import Flask
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# ✅ तेरा असली यूजरनेम और पासवर्ड 
IG_USERNAME = "sujeetmishra9336"
IG_PASSWORD = "selected_reel.in"

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

# 🔥 24/7 ALWAYS ONLINE (हरा डॉट हमेशा चालू)
def always_online_loop():
    init_client()
    while True:
        try:
            cl.get_timeline_feed()
            print("Online Ping Sent! 🟢")
        except Exception as e:
            print(f"Loop Error: {e}")
            init_client()
        # हर 3-4 मिनट में ऑनलाइन का सिग्नल भेजेगा
        time.sleep(random.randint(180, 240))

threading.Thread(target=always_online_loop, daemon=True).start()

@app.route("/")
def home():
    return "Sujeet Bhai ka 24/7 Online + Auto Text Story Bot Live Hai! 🟢💻🔥"

@app.route("/post-night-story")
def post_story():
    try:
        # 1. टाइम निकालना (IST)
        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_timezone)
        current_hour_str = now_ist.strftime("%-I %p") 
        
        # 2. खुद से एक तगड़ी फोटो बनाना (ताकि वीडियो/FFmpeg का कोई लफड़ा ही न रहे!)
        img = Image.new('RGB', (1080, 1920), color=(15, 15, 15)) # ब्लैक बैकग्राउंड
        d = ImageDraw.Draw(img)
        
        # फॉन्ट सेट करना (बड़ा साइज़)
        try:
            font = ImageFont.load_default(size=70)
        except:
            font = ImageFont.load_default()
        
        # 3. जो टेक्स्ट लिखना है (टाइम के साथ)
        text = f"Time update: It's {current_hour_str}\n\nBut I can't sleep...\nLearning computer coding 💻🔥"
        
        # सेंटर में टेक्स्ट लिखने का लॉजिक
        bbox = d.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (1080 - w) / 2
        y = (1920 - h) / 2
        
        # हैकर वाले हरे रंग (Neon Green) में टेक्स्ट लिखना
        d.multiline_text((x, y), text, fill=(0, 255, 0), font=font, align="center")
        
        photo_path = "/tmp/night_story.jpg"
        img.save(photo_path)
        
        # 🚨 5 सेकंड का इंतज़ार (सिक्योरिटी के लिए)
        time.sleep(5)
        
        # 4. फोटो को स्टोरी पर अपलोड मारना (इसमें कोई बैन नहीं लगता!)
        cl.photo_upload_to_story(photo_path, caption="Night grind! 🔥")
        
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
        return f"✅ SUCCESS: Photo Story Posted with time: {current_hour_str}! 🚀🔥"
    
    except Exception as e:
        return f"❌ ERROR aaya bhai: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
        
