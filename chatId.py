from telegram import Bot

# Replace this with your bot's token
BOT_TOKEN = '7542483069:AAEsn9mt8aNXZcvnGoKn8salwdjC3galfL8'

bot = Bot(token=BOT_TOKEN)

def get_chat_id():
    updates = bot.get_updates()
    for update in updates:
        print(update)

if __name__ == "__main__":
    print("Send a message to the channel, then run this script.")
    get_chat_id()
