import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = '7542483069:AAEsn9mt8aNXZcvnGoKn8salwdjC3galfL8'
CHANNEL_USERNAME = '@colour_trading_1win'  # Replace with your channel username or ID
IMAGE_PATH = "pramotion1.jpeg"  # Path to the image file
bot = Bot(token=BOT_TOKEN)

async def send_promotion():
    """
    Sends the promotional message with an image.
    """
    message = """
🎮✨ **Get Ready to Play & Win Big!** ✨🎮  
Looking for the ultimate gaming and lottery experience? Dive into the world of thrilling games, massive rewards, and endless excitement! 🤑🎉  

🏆 **Why Join?**  
✅ Big Cash Prizes 💰  
✅ Secure & Fast Withdrawals 🏦  
✅ Tons of Exciting Games 🎲🎰  

🎉 **Your Gateway to Fun & Fortune!** 🎉  
Check out these amazing platforms and start winning today:  

🔹 **1Win**: [Play Now](https://yourpromotionlink.com/1win)  
🔹 **Lottery7**: [Try Your Luck](https://yourpromotionlink.com/lottery7)  
🔹 **Tiranga**: [Join & Win](https://yourpromotionlink.com/tiranga)  

💥 Don’t wait! Opportunities like these don’t last long. Click on the links and join the fun NOW! 💥  
"""

    try:
        # Send the image
        with open(IMAGE_PATH, 'rb') as img:
            await bot.send_photo(chat_id=CHANNEL_USERNAME, photo=img)

        # Send the message
        await bot.send_message(chat_id=CHANNEL_USERNAME, text=message, parse_mode="Markdown")

        logger.info("Promotional content sent successfully!")
    except TelegramError as e:
        logger.error(f"Error sending promotional content: {e}")

async def main():
    """
    Main loop to send promotional messages at regular intervals.
    """
    logger.info("Bot started. Sending promotional content every 5 seconds...")
    while True:
        await send_promotion()
        await asyncio.sleep(5)  # Wait for 5 seconds

if __name__ == "__main__":
    asyncio.run(main())
