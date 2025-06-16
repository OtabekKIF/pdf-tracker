from flask import Flask, request, send_file
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

@app.route('/')
def home():
    return "✅ PDF Tracker Flask server ishlayapti."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render uchun moslashuv
    app.run(host="0.0.0.0", port=port)
