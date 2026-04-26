import telebot
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("Error: TOKEN is not set")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Password Generator Bot! Use /generate to create a new password.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Use /generate to create a new password.")
    
@bot.message_handler(func=lambda message: message.text == '/generate')
def generate_password(message):
    import random
    import string
    
    length = message.text.split()[1] if len(message.text.split()) > 1 else 12
    try:
        length = int(length)
    except ValueError:
        bot.reply_to(message, "Please provide a valid number for password length.")
        return
    else:
        length = max(12, min(length, 64))  # Ensure length is between 4 and 64
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    
    bot.reply_to(message, f"Your generated password is: {password}")

if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()