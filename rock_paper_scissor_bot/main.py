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
reg_btn = types.KeyboardButton('Play')
reg_kb.add(reg_btn)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Welcome to Rock-Paper-Scissors Bot🤖! Click 'Play' to start the game.",
        reply_markup=reg_kb
    )

reg_btn1 = types.KeyboardButton('Rock🪨')
reg_btn2 = types.KeyboardButton('Paper📄')
reg_btn3 = types.KeyboardButton('Scissors✂️')
game_kb = types.ReplyKeyboardMarkup()
game_kb.add(reg_btn1, reg_btn2, reg_btn3)

def get_computer_choice():
    import random
    return random.choice(['Rock🪨', 'Paper📄', 'Scissors✂️'])

@bot.message_handler(func=lambda message: message.text == 'Play')
def play(message):
    bot.send_message(
        message.chat.id, 
        "Choose Rock, Paper, or Scissors:",
        reply_markup=game_kb
    )

@bot.message_handler(func=lambda message: message.text in ['Rock🪨', 'Paper📄', 'Scissors✂️'])
def handle_choice(message):
    user_choice = message.text
    computer_choice = get_computer_choice()
    
    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (user_choice == 'Rock🪨' and computer_choice == 'Scissors✂️') or \
         (user_choice == 'Paper📄' and computer_choice == 'Rock🪨') or \
         (user_choice == 'Scissors✂️' and computer_choice == 'Paper📄'):
        result = "You win!"
    else:
        result = "You lose!"
    bot.send_message(
        message.chat.id,
        f"You chose {user_choice}, computer chose {computer_choice}. {result}",
        reply_markup=reg_kb
    )

exit_btn = types.KeyboardButton('Exit')
exit_kb = types.ReplyKeyboardMarkup()
exit_kb.add(exit_btn)
@bot.message_handler(func=lambda message: message.text == 'Exit')
def exit_game(message):
    bot.send_message(
        message.chat.id,
        "Thanks for playing! Click 'Play' to start again.",
        reply_markup=reg_kb
    )

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()