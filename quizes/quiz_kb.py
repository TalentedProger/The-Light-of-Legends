from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_quiz_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Конечно ✅", callback_data="quiz_yes")],
        [InlineKeyboardButton(text="Нет, выйти с режима ❌", callback_data="quiz_no")]
    ])

def difficulty_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мир Адыгов", callback_data="diff_easy")],
        [InlineKeyboardButton(text="Культура Адыгов", callback_data="diff_medium")]
        # [InlineKeyboardButton(text="Тяжелый 🥉", callback_data="diff_hard")]
    ])

def start_or_exit_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать ▶️", callback_data="start_quiz")],
        [InlineKeyboardButton(text="Выйти ❌", callback_data="exit")]
    ])

def answer_kb(options: list):
    buttons = [[InlineKeyboardButton(text=opt, callback_data=f"ans_{opt}")] for opt in options]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def final_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти еще раз 🔁", callback_data="restart_quiz")],
        [InlineKeyboardButton(text="Перейти к темам ⚙️", callback_data="change_mode")],
        [InlineKeyboardButton(text="Выйти ❌", callback_data="exit")]
    ])
