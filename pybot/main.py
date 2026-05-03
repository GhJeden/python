import telebot
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("Token not found.")
    exit()

bot = telebot.TeleBot(TOKEN)

reg_kb = types.ReplyKeyboardMarkup()
reg_btn = types.KeyboardButton('Регистрация👌')
reg_kb.add(reg_btn)

cancel_kb = types.ReplyKeyboardMarkup()
cancel_btn = types.KeyboardButton('Отмена❌')
cancel_kb.add(cancel_btn)

remove_kb = types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми кнопку ниже, чтобы получить спам на почту.", 
        reply_markup=reg_kb
    )

@bot.message_handler(func=lambda message: message.text == 'Регистрация👌')
def registration_handler(message):
    temp_msg = bot.send_message(
        message.chat.id, 
        "Отлично! Сейчас я удалю это сообщение, чтобы не засорять чат. Пожалуйста, подожди...", 
        reply_markup=remove_kb
    )
    
    bot.delete_message(message.chat.id, temp_msg.id)
    
    bot.send_message(
        message.chat.id, 
        "Отлично! Скинь мне чью-то почту, и я буду нещадно мучать её спамом!", 
        reply_markup=cancel_kb
    )

@bot.message_handler(func=lambda message: message.text == 'Отмена❌')
def cancel_handler(message):
    bot.send_message(
        message.chat.id, 
        "Регистрация отменена. Если передумаешь, нажми кнопку 'Регистрация👌'.", 
        reply_markup=reg_kb
    )

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()