from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Библиотека 📚')],
	[KeyboardButton(text='Пословицы 📝'),KeyboardButton(text='Песни 🎶')],
	[KeyboardButton(text='Легенды ⚜️'),KeyboardButton(text='Мифы 🔮')],
    [KeyboardButton(text='Галерея 📸'),KeyboardButton(text='Квест 🏆')],
    [KeyboardButton(text='О нас ℹ️'),KeyboardButton(text='Оценить проект ⭐')],
    [KeyboardButton(text='Изучить новые слова 📖')],
	
],resize_keyboard=True,input_field_placeholder="Выберите пункт меню")

start_quiz_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да, давайте начинать ✅", callback_data="start_rules")],
    [InlineKeyboardButton(text="Нет, вернуться назад ❌", callback_data="cancel")]
])

rules_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать ▶️", callback_data="begin_quiz")]
])


def get_proverbs_keyboard(img_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая ⏩️", callback_data="next_proverb")],
        [InlineKeyboardButton(text="Скопировать 📝", callback_data=f"copy_proverb:{img_id}")],
        [InlineKeyboardButton(text="Выйти из режима ❌", callback_data="exit_proverb_mode")]
    ])


def get_legend_keyboard(legend_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Краткое описание 📝", callback_data=f"legend_info:{legend_id}")],
        [InlineKeyboardButton(text="Следующая ⏩️", callback_data="legend_next")],
        [InlineKeyboardButton(text="Выйти ❌", callback_data="legend_exit")]
    ])

def get_song_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Следующая песня ▶️", callback_data="next_song")],
        [InlineKeyboardButton(text="Удалить ❌", callback_data="exit_song_mode")]
    ])


# клавиатура для изучения слов
def get_main_word_keyboard(is_active: bool):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Изменить время" if is_active else "🔔 Включить режим",
                callback_data="word_toggle"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Закрыть меню",
                callback_data="word_close_menu"
            )
        ]
    ])
    return keyboard

def get_time_picker_keyboard():
    times = ["09:00", "12:00", "15:00", "18:00", "21:00"]
    rows = [[InlineKeyboardButton(text=t, callback_data=f"word_set_time:{t}")] for t in times]
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="word_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_gallery_keyboard(index: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❌ Выйти", callback_data="gallery_exit"),
        InlineKeyboardButton(text="🖼 Следующая", callback_data=f"gallery_next:{index}")
    )
    return builder.as_markup()

def get_myths_keyboard(index: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❌ Выйти", callback_data="myths_exit"),
        InlineKeyboardButton(text="🖼 Следующая", callback_data=f"myths_next:{index}")
    )
    return builder.as_markup()

about_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📩 Связаться", callback_data="contact"),
        InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    ]
])


review_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💬 Оставить отзыв", url="https://forms.yandex.ru/u/687a058ae010db0735e8f675")],
    [InlineKeyboardButton(text="❌ Выйти", callback_data="exit_review")]
])