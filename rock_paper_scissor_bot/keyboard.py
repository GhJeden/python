from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Play Rock, Paper, Scissors"),
        KeyboardButton(text="View Rules")
        ]
    ],
    resize_keyboard=True
)

rock_paper_scissors_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Rock", callback_data="rock"),
            InlineKeyboardButton(text="Paper", callback_data="paper"),
            InlineKeyboardButton(text="Scissors", callback_data="scissors")
        ]
    ]
)
