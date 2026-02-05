import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading

# API Credentials from Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- FEATURE 1: AUTO REPLY ---
@app.on_message(filters.private & ~filters.me)
async def auto_reply(client, message):
    reply_text = (
        "Hello! 👋\n\n"
        "I am currently busy or away from my phone. "
        "I will get back to you as soon as I am online.\n\n"
        "*This is an automated response.*"
    )
    await message.reply_text(reply_text)

# --- FEATURE 2: QUICK REPLIES (Premium Style) ---
# In keywords ko chat mein likhte hi bot inhe full message mein badal dega
QUICK_REPLIES = {
    ".hi": "Hello! How can I help you today?",
    ".busy": "I'm in a meeting right now, will talk to you later.",
    ".price": "I can build a professional website for you starting at just ₹100!",
    ".ok": "Understood. I will get back to you on this shortly.",
    ".id": "My Telegram ID is currently managed by an automated assistant."
}

@app.on_message(filters.me & filters.text)
async def quick_reply_handler(client, message):
    cmd = message.text.lower()
    if cmd in QUICK_REPLIES:
        await message.edit(QUICK_REPLIES[cmd])

# --- WEB SERVER FOR RENDER (To prevent Port Errors) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is alive and running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start Web Server in a separate thread
    threading.Thread(target=run_web_server, daemon=True).start()
    # Run the Telegram Bot
    app.run()
  
