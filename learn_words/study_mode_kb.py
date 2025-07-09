from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def stage_one_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Выйти", callback_data="exit_mode")],
            [InlineKeyboardButton(text="▶️ Далее", callback_data="to_stage_2")]
        ]
    )

def day_selection_kb(selected_day: str = "") -> InlineKeyboardMarkup:
    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    keyboard = []
    for day in days:
        text = f"{day.capitalize()}{' ✅' if selected_day == day else ''}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"day_{day}")])
    keyboard.append([
        InlineKeyboardButton(text="▶️ Далее", callback_data="to_stage_3"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_stage_1")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def time_selection_kb(selected_time: str = "") -> InlineKeyboardMarkup:
    times = ["10:00", "14:00", "18:00", "21:00", "23:00"]
    keyboard = []
    for time in times:
        text = f"{time}{' ✅' if selected_time == time else ''}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"time_{time}")])
    keyboard.append([
        InlineKeyboardButton(text="▶️ Далее", callback_data="to_stage_4"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_stage_2")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def final_stage_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Изменить день/время", callback_data="restart_setup")],
            [InlineKeyboardButton(text="❌ Выйти", callback_data="exit_mode")]
        ]
    )

def mode_already_enabled_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Изменить время", callback_data="restart_setup")],
            [InlineKeyboardButton(text="🔕 Выключить режим", callback_data="disable_mode")],
            [InlineKeyboardButton(text="❌ Выйти", callback_data="exit_mode")]
        ]
    )
