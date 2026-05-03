import telebot
import os
import re
from dotenv import load_dotenv
from telebot import types
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Token not found!')
    exit()

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

bot.add_custom_filter(custom_filters.StateFilter(bot))


class RegistrationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_phone = State()


reg_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
reg_btn = types.KeyboardButton('Регистрация')
reg_kb.add(reg_btn)

phone_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
phone_btn = types.KeyboardButton('Отправить номер', request_contact=True)
phone_kb.add(phone_btn)

cancel_kb = types.InlineKeyboardMarkup()
cancel_btn = types.InlineKeyboardButton('Отмена', callback_data='cancel')
cancel_kb.add(cancel_btn)

remove_kb = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        'Привет! Нажми "Регистрация" чтобы начать.',
        reply_markup=reg_kb
    )


@bot.message_handler(func=lambda message: message.text.startswith('Регистрация'))
def start_registration(message):
    bot.set_state(
        message.from_user.id,
        RegistrationStates.waiting_for_email,
        message.chat.id
    )

    bot.send_message(
        message.chat.id,
        'Введи свою email:',
        reply_markup=cancel_kb
    )


@bot.message_handler(state=RegistrationStates.waiting_for_email)
def process_email(message):
    email = message.text
    email_pattern = r"^[\w\.-_]+@[\w\.-_]+\.\w+$"

    if re.match(email_pattern, email):
        with open('emails.txt', 'a') as f:
            f.write(email + '\n')

        bot.set_state(
            message.from_user.id,
            RegistrationStates.waiting_for_phone,
            message.chat.id
        )

        bot.send_message(
            message.chat.id,
            "Теперь отправь номер телефона или нажми кнопку:",
            reply_markup=phone_kb
        )
    else:
        bot.send_message(message.chat.id, "Неверный email, попробуй ещё раз")


@bot.message_handler(state=RegistrationStates.waiting_for_phone, content_types=['contact', 'text'])
def process_phone(message):
    phone = None

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    phone_pattern = r"^\+?\d{10,15}$"

    if phone and re.match(phone_pattern, phone):
        with open('phones.txt', 'a') as f:
            f.write(phone + '\n')

        bot.delete_state(message.from_user.id, message.chat.id)

        bot.send_message(
            message.chat.id,
            "Регистрация завершена!",
            reply_markup=reg_kb
        )
    else:
        bot.send_message(
            message.chat.id,
            "Неверный номер, попробуй ещё раз"
        )


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def cancel_handler(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)

    bot.send_message(
        call.message.chat.id,
        'Регистрация отменена',
        reply_markup=reg_kb
    )

    bot.answer_callback_query(call.id)


if __name__ == "__main__":
    print('Bot is running...')
    bot.infinity_polling()