import os
import time
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid, FloodWait
from flask import Flask

# API Credentials from Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Dictionary to store last reply time for each user
last_reply_time = {}
REPLY_DELAY = 600  # 10 minutes delay (Logic piche kaam karega, message mein nahi dikhega)

# --- FEATURE: AUTO REPLY (CLEAN VERSION) ---
@app.on_message(filters.private & ~filters.me)
async def auto_reply(client, message):
    try:
        user_id = message.from_user.id
        current_time = time.time()

        # Check for 10-minute cooldown (Quietly)
        if user_id in last_reply_time:
            if current_time - last_reply_time[user_id] < REPLY_DELAY:
                return 

        # --- AAPKA UPDATED MESSAGE ---
        reply_text = (
            "Hello! 👋\n\n"
            "I am currently busy or away from my phone. "
            "I will get back to you as soon as I am online. 🙃"
        )
        
        await message.reply_text(reply_text)
        
        # Update last reply time
        last_reply_time[user_id] = current_time

    except (PeerIdInvalid, ValueError):
        pass
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print(f"Auto-reply error: {e}")

# --- FEATURE: QUICK REPLIES (.command) ---
QUICK_REPLIES = {
    ".hi": "Hello! How can I help you?",
    ".busy": "I'm busy right now, will talk later.",
    ".price": "Websites start at just ₹100 for lifetime!",
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
    return "Bot is running with Clean Auto-Reply!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    try:
        print("Bot started with Clean Message...")
        app.run()
    except Exception as e:
        print(f"Main Error: {e}")
