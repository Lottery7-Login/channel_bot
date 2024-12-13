import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
BOT_TOKEN = '7542483069:AAEsn9mt8aNXZcvnGoKn8salwdjC3galfL8'
CHANNEL_USERNAME = '@gameannouncement'
stored_content = []  # Store messages, photos, and videos

# Handler to store incoming messages
async def store_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1].file_id
        stored_content.append({"type": "photo", "content": photo})
        logger.info("Photo stored successfully.")
        await update.message.reply_text("Photo stored successfully!")
    elif update.message.video:
        video = update.message.video.file_id
        stored_content.append({"type": "video", "content": video})
        logger.info("Video stored successfully.")
        await update.message.reply_text("Video stored successfully!")
    elif update.message.text:
        text = update.message.text
        stored_content.append({"type": "text", "content": text})
        logger.info("Text message stored successfully.")
        await update.message.reply_text("Message stored successfully!")
    else:
        await update.message.reply_text("Unsupported content type.")

# Function to send all messages to the channel
async def send_to_channel(context: ContextTypes.DEFAULT_TYPE):
    if not stored_content:
        logger.warning("No content to send.")
        return

    for item in stored_content:
        try:
            if item["type"] == "photo":
                await context.bot.send_photo(chat_id=CHANNEL_USERNAME, photo=item["content"])
            elif item["type"] == "video":
                await context.bot.send_video(chat_id=CHANNEL_USERNAME, video=item["content"])
            elif item["type"] == "text":
                await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=item["content"])
            logger.info(f"Sent {item['type']} to the channel.")
        except Exception as e:
            logger.error(f"Error sending content: {e}")

    # Clear the content after sending
    stored_content.clear()
    logger.info("All stored content has been sent and cleared.")

# Scheduler setup
def schedule_jobs(scheduler, application):
    scheduler.add_job(
        send_to_channel,
        trigger='cron',
        hour=20,
        minute=0,
        args=[application]
    )
    scheduler.add_job(
        send_to_channel,
        trigger='cron',
        hour=12,
        minute=0,
        args=[application]
    )
    scheduler.add_job(
        send_to_channel,
        trigger='cron',
        hour=16,
        minute=0,
        args=[application]
    )
    scheduler.add_job(
        send_to_channel,
        trigger='cron',
        hour=18,
        minute=0,
        args=[application]
    )
    logger.info("Jobs scheduled successfully.")

# Main function
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(MessageHandler(filters.ALL, store_message))

    # Initialize scheduler
    scheduler = AsyncIOScheduler()
    schedule_jobs(scheduler, application)
    scheduler.start()

    # Run the bot
    logger.info("Bot is running.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
