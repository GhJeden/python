import telebot
import os
from dotenv import load_dotenv
import random

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "H3ll0, I am a simple yes/no bot! Ask me any question, and I'll answer with yes or no.")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "I am a simple yes/no bot. Just ask me any question, and I'll answer with yes or no.")

@bot.message_handler(func=lambda message: True)
def answer_yes_no(message):
    response = random.choice(['Yes', 'No'])
    bot.reply_to(message, response)

if __name__ == '__main__':
    print('Bot is running...')
    bot.infinity_polling()

