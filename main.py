import os
import time
import asyncio
import threading
from pyrogram import Client, filters
from flask import Flask

# API Credentials
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Dictionary to store last reply time for each user
last_reply_time = {}

# Delay time in seconds (10 minutes = 600 seconds)
REPLY_DELAY = 600

# --- FEATURE 1: AUTO REPLY WITH 10 MIN DELAY ---
@app.on_message(filters.private & ~filters.me)
async def auto_reply(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    # Check if we replied to this user recently
    if user_id in last_reply_time:
        if current_time - last_reply_time[user_id] < REPLY_DELAY:
            return  # 10 min nahi hue, isliye reply nahi jayega

    reply_text = (
        "Hello! 👋\n\n"
        "I am currently busy or away from my phone. "
        "I will get back to you as soon as I am online.\n\n"
        "*This is an automated response (sent once every 10 min).*"
    )
    
    await message.reply_text(reply_text)
    # Update the last reply time for this user
    last_reply_time[user_id] = current_time

# --- FEATURE 2: QUICK REPLIES ---
QUICK_REPLIES = {
    ".hi": "Hello! How can I help you today?",
    ".busy": "I'm in a meeting right now, will talk to you later.",
    ".price": "I can build a professional website for you starting at just ₹100!",
    ".ok": "Understood. I will get back to you on this shortly."
}

@app.on_message(filters.me & filters.text)
async def quick_reply_handler(client, message):
    cmd = message.text.lower()
    if cmd in QUICK_REPLIES:
        await message.edit(QUICK_REPLIES[cmd])

# --- WEB SERVER FOR RENDER ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running with 10-min Delay Feature!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    try:
        print("Bot starting with Delay Logic...")
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        
