from flask import Flask, request, send_file, jsonify
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# .env fayldan o'zgaruvchilarni yuklash
load_dotenv()

app = Flask(__name__)

# .env orqali token va chat_id o'qish
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(message: str):
    """Telegramga xabar yuboradi."""
    if not BOT_TOKEN or not CHAT_ID:
        print("❗ BOT_TOKEN yoki CHAT_ID aniqlanmadi.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("❗ Telegramga yuborishda xatolik:", response.text)
    except Exception as e:
        print("❗ Telegramga yuborishda xatolik:", e)

@app.route('/track.png')
def tracker():
    """PDF ochilganda ishga tushadigan tracker."""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        "📥 *PDF ochildi!*\n"
        f"🕓 Sana: {now}\n"
        f"🌍 IP: `{ip}`\n"
        f"🧭 User-Agent: `{user_agent}`"
    )

    print(message)

    # Log faylga yozish
    try:
        with open("logs.txt", "a", encoding="utf-8") as log:
            log.write(f"{now} | {ip} | {user_agent}\n")
    except Exception as e:
        print("❗ Log faylga yozishda xatolik:", e)

    # Telegramga yuborish
    send_to_telegram(message)

    # Tracker rasm yuborish
    return send_file("pixel.png", mimetype="image/png")

@app.route('/track_data', methods=['POST'])
def track_data():
    """Frontenddan kelgan qurilma ma'lumotlarini qabul qiladi."""
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ma'lumotlarni formatlash
    message = (
        "📊 *Qurilma ma'lumotlari keldi!*\n"
        f"🕓 Sana: {now}\n"
        f"🌍 IP: `{ip}`\n"
        f"🆔 Visitor ID: `{data.get('visitorId', 'unknown')}`\n"
        f"🖥️ Ekran: `{data.get('screen', 'unknown')}`\n"
        f"🎨 Rang chuqurligi: `{data.get('colorDepth', 'unknown')}`\n"
        f"🌐 Til: `{data.get('language', 'unknown')}`\n"
        f"💻 Platforma: `{data.get('platform', 'unknown')}`\n"
        f"🧭 User-Agent: `{data.get('userAgent', 'unknown')}`\n"
        f"⚙️ CPU: `{data.get('cpu', 'unknown')}`\n"
        f"🧠 RAM: `{data.get('ram', 'unknown')}`\n"
        f"⏰ Vaqt zonasi: `{data.get('timezone', 'unknown')}`\n"
        f"🕒 Mahalliy vaqt: `{data.get('localTime', 'unknown')}`\n"
        f"🚫 Do Not Track: `{data.get('doNotTrack', 'unknown')}`\n"
        f"🔋 Batareya: `{data.get('battery', 'unknown')}`\n"
        f"📹 Media: `{data.get('media', 'unknown')}`\n"
        f"🌐 Tarmoq turi: `{data.get('networkType', 'unknown')}`\n"
        f"📱 Qurilma turi: `{data.get('deviceType', 'unknown')}`\n"
        f"🏭 Ishlab chiqaruvchi: `{data.get('manufacturer', 'unknown')}`\n"
        f"🖥️ OS versiyasi: `{data.get('osVersion', 'unknown')}`\n"
        f"🧠 Umumiy xotira: `{data.get('memoryTotal', 'unknown')}`\n"
        f"🧠 Ishlatilgan xotira: `{data.get('memoryUsed', 'unknown')}`\n"
        f"⚙️ CPU yuki: `{data.get('cpuLoad', 'unknown')}`\n"
        f"📱 Qurilma modeli: `{data.get('deviceModel', 'unknown')}`"
    )

    print(message)

    # Log faylga yozish
    try:
        with open("logs.txt", "a", encoding="utf-8") as log:
            log.write(
                f"{now} | {ip} | Visitor ID: {data.get('visitorId', 'unknown')} | "
                f"Screen: {data.get('screen', 'unknown')} | "
                f"Color Depth: {data.get('colorDepth', 'unknown')} | "
                f"Language: {data.get('language', 'unknown')} | "
                f"Platform: {data.get('platform', 'unknown')} | "
                f"User-Agent: {data.get('userAgent', 'unknown')} | "
                f"CPU: {data.get('cpu', 'unknown')} | "
                f"RAM: {data.get('ram', 'unknown')} | "
                f"Timezone: {data.get('timezone', 'unknown')} | "
                f"Local Time: {data.get('localTime', 'unknown')} | "
                f"Do Not Track: {data.get('doNotTrack', 'unknown')} | "
                f"Battery: {data.get('battery', 'unknown')} | "
                f"Media: {data.get('media', 'unknown')} | "
                f"Network Type: {data.get('networkType', 'unknown')} | "
                f"Device Type: {data.get('deviceType', 'unknown')} | "
                f"Manufacturer: {data.get('manufacturer', 'unknown')} | "
                f"OS Version: {data.get('osVersion', 'unknown')} | "
                f"Memory Total: {data.get('memoryTotal', 'unknown')} | "
                f"Memory Used: {data.get('memoryUsed', 'unknown')} | "
                f"CPU Load: {data.get('cpuLoad', 'unknown')} | "
                f"Device Model: {data.get('deviceModel', 'unknown')}\n"
            )
    except Exception as e:
        print("❗ Log faylga yozishda xatolik:", e)

    # Telegramga yuborish
    send_to_telegram(message)

    return jsonify({"status": "success"})

@app.route('/')
def home():
    return "✅ PDF Tracker Flask server ishlayapti."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render uchun moslashuv
    app.run(host="0.0.0.0", port=port)
