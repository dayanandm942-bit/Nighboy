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

def init_client():
    try:
        # 🚨 सबसे ज़रूरी: अगर पुरानी करप्ट फाइल पड़ी है, तो उसे डिलीट मारो
        if os.path.exists(session_file):
            os.remove(session_file)
            print("Old session deleted! Starting fresh... 🗑️")

        # 📱 2024 लेटेस्ट Samsung Galaxy S21 का प्रोफाइल (इंस्टाग्राम इसे कभी पुराना नहीं बोलेगा)
        cl.set_device({
            "app_version": "333.0.0.32.118",
            "android_version": 30,
            "android_release": "11",
            "dpi": "480dpi",
            "resolution": "1080x2280",
            "manufacturer": "Samsung",
            "device": "SM-G991B",
            "model": "SM-G991B",
            "cpu": "exynos2100",
            "version_code": "563600643"
        })
        
        # एकदम नया फ्रेश लॉग-इन
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
        time.sleep(random.randint(180, 240))

threading.Thread(target=always_online_loop, daemon=True).start()

@app.route("/")
def home():
    return "Sujeet Bhai ka 24/7 Online + Auto Text Story Bot Live Hai! 🟢💻🔥"

@app.route("/post-night-story")
def post_story():
    try:
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
        
        time.sleep(5)
        
        cl.photo_upload_to_story(photo_path, caption="Night grind! 🔥")
        
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
        return f"✅ SUCCESS: Photo Story Posted with time: {current_hour_str}! 🚀🔥"
    
    except Exception as e:
        return f"❌ ERROR aaya bhai: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
