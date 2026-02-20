import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.environ.get("TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "សួស្តី! 🤖\nផ្ញើ link YouTube ឬ TikTok មក ខ្ញុំនឹងជួយទាញយកឲ្យ 📥"
    )

def download_video(url: str) -> str:
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title).50s.%(ext)s",
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
        await update.message.reply_text("សូមផ្ញើ link YouTube ឬ TikTok មក 📎")
        return

    await update.message.reply_text("កំពុងទាញយក... សូមរង់ចាំបន្តិច ⏳")

    loop = asyncio.get_running_loop()
    try:
        file_path = await loop.run_in_executor(None, download_video, text)

        if os.path.exists(file_path):
            await update.message.reply_video(video=open(file_path, "rb"))
            os.remove(file_path)
        else:
            await update.message.reply_text("សុំទោស! មិនអាចទាញយកបានទេ ❌")
    except Exception as e:
        await update.message.reply_text(f"មានបញ្ហា: {e}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("គ្រាន់តែផ្ញើ link YouTube/TikTok មក bot នឹងទាញយកឲ្យ 📥")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
