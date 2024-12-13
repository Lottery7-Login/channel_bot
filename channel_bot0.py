import logging
from telegram import Bot, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
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
BOT_TOKEN = 'your_bot_token_here'
CHANNEL_USERNAME = '@your_channel_username'
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
def schedule_jobs(application):
    scheduler = AsyncIOScheduler()

    # Wrapper to pass the application context
    async def send_to_channel_job():
        # Get the bot's context
        context = application.bot
        await send_to_channel(context)

    scheduler.add_job(
        send_to_channel_job,
        trigger='cron',
        hour=9,
        minute=0
    )
    scheduler.add_job(
        send_to_channel_job,
        trigger='cron',
        hour=12,
        minute=0
    )
    scheduler.add_job(
        send_to_channel_job,
        trigger='cron',
        hour=16,
        minute=0
    )
    scheduler.add_job(
        send_to_channel_job,
        trigger='cron',
        hour=18,
        minute=0
    )
    scheduler.start()
    logger.info("Jobs scheduled successfully.")

# Main function
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(MessageHandler(filters.ALL, store_message))

    # Schedule jobs
    schedule_jobs(application)

    # Run the bot
    logger.info("Bot is running.")
    await application.run_polling()

# Entry point
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Use the existing event loop
            logger.info("Using the existing event loop.")
            loop.create_task(main())
        else:
            # Start a new event loop
            logger.info("Starting a new event loop.")
            loop.run_until_complete(main())
    except RuntimeError as e:
        logger.error(f"Event loop error: {e}")
