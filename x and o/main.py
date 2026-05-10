import os
from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = TeleBot(TOKEN)

games = {}


def keyboard_board(board):
    keyboard = types.InlineKeyboardMarkup()

    for i in range(3):
        buttons = []

        for j in range(3):
            index = i * 3 + j

            text = board[index]

            if text == " ":
                text = "."

            button = types.InlineKeyboardButton(
                text,
                callback_data=f"move_{index}"
            )

            buttons.append(button)

        keyboard.row(*buttons)

    return keyboard


def check_winner(board, symbol):
    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],

        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],

        [0, 4, 8],
        [2, 4, 6]
    ]

    for combo in wins:
        if all(board[i] == symbol for i in combo):
            return True

    return False


def bot_turn(board, symbol):
    for i in range(9):
        if board[i] == " ":
            board[i] = symbol
            break


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()

    x_button = types.InlineKeyboardButton(
        "X",
        callback_data="symbol_X"
    )

    o_button = types.InlineKeyboardButton(
        "O",
        callback_data="symbol_O"
    )

    keyboard.row(x_button, o_button)

    bot.send_message(
        message.chat.id,
        "Which symbol do you want to play with?",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("symbol_"))
def choose_symbol(call):
    user_symbol = call.data.split("_")[1]

    if user_symbol == "X":
        bot_symbol = "O"
    else:
        bot_symbol = "X"

    board = [" "] * 9

    games[call.message.chat.id] = {
        "board": board,
        "user": user_symbol,
        "bot": bot_symbol
    }

    if bot_symbol == "X":
        bot_turn(board, bot_symbol)

    bot.edit_message_text(
        "Let the game begin!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard_board(board)
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("move_"))
def move(call):
    chat_id = call.message.chat.id

    if chat_id not in games:
        return

    game = games[chat_id]

    board = game["board"]

    index = int(call.data.split("_")[1])

    if board[index] != " ":
        return

    board[index] = game["user"]

    if check_winner(board, game["user"]):
        bot.edit_message_text(
            "You won!",
            chat_id,
            call.message.message_id,
            reply_markup=keyboard_board(board)
        )

        del games[chat_id]
        return

    if " " not in board:
        bot.edit_message_text(
            "Draw!",
            chat_id,
            call.message.message_id,
            reply_markup=keyboard_board(board)
        )

        del games[chat_id]
        return

    bot_turn(board, game["bot"])

    if check_winner(board, game["bot"]):
        bot.edit_message_text(
            "I won!",
            chat_id,
            call.message.message_id,
            reply_markup=keyboard_board(board)
        )

        del games[chat_id]
        return

    if " " not in board:
        bot.edit_message_text(
            "Draw!",
            chat_id,
            call.message.message_id,
            reply_markup=keyboard_board(board)
        )

        del games[chat_id]
        return

    bot.edit_message_reply_markup(
        chat_id,
        call.message.message_id,
        reply_markup=keyboard_board(board)
    )


bot.infinity_polling()