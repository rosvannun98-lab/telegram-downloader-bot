import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("សួស្តី! 🤖 សូមផ្ញើ link YouTube ឬ TikTok មក ខ្ញុំនឹងជួយ download 😄")

def download_video(url: str) -> str:
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "format": "best[height<=360]/best",
        "noplaylist": True,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "http" not in text:
        await update.message.reply_text("សូមផ្ញើ link YouTube ឬ TikTok មក 🙏")
        return

    await update.message.reply_text("កំពុង download ⏳ សូមរង់ចាំបន្តិច...")

    loop = asyncio.get_running_loop()
    try:
        file_path = await loop.run_in_executor(None, download_video, text)
        await update.message.reply_video(video=open(file_path, "rb"))
    except Exception as e:
        await update.message.reply_text(f"មានបញ្ហា ❌ : {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
