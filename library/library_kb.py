from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# def get_library_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🟢 Аслануко - сын львицы", callback_data='fairy_1')],
#         [InlineKeyboardButton(text="🟢 Бык-великан", callback_data='fairy_2')],
#         [InlineKeyboardButton(text="🟢Гадальщица Бабочка", callback_data='fairy_3')],
#         [InlineKeyboardButton(text="🟢 Девочка,которая несла золото", callback_data='fairy_4')],
#         [InlineKeyboardButton(text="🟢 Делёж по-божески", callback_data='fairy_5')],
#         [InlineKeyboardButton(text="🟢 Кадир", callback_data='fairy_6')],
#         [InlineKeyboardButton(text="🟢 Муж и жена", callback_data='fairy_7')],
#         [InlineKeyboardButton(text="🟢 Нормэрышхо - большой Нормэр", callback_data='fairy_8')],
#         [InlineKeyboardButton(text="🟢 Трудовые деньги", callback_data='fairy_9')],
#         [InlineKeyboardButton(text="🟢 Чудесная гармошка", callback_data='fairy_10')],
#         [InlineKeyboardButton(text="Закрыть меню ❌", callback_data='close_library')]
#     ])

def get_library_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кадир", callback_data='fairy_6'),InlineKeyboardButton(text="Муж и жена", callback_data='fairy_7')],
        [InlineKeyboardButton(text="Бык-великан", callback_data='fairy_2'),InlineKeyboardButton(text="Трудовые деньги", callback_data='fairy_9')],
        [InlineKeyboardButton(text="Трудовые деньги", callback_data='fairy_9'),InlineKeyboardButton(text="Делёж по-божески", callback_data='fairy_5')],
        [InlineKeyboardButton(text="Делёж по-божески", callback_data='fairy_5')],
        [InlineKeyboardButton(text="Чудесная гармошка", callback_data='fairy_10')],
        [InlineKeyboardButton(text="Гадальщица Бабочка", callback_data='fairy_3')],
        [InlineKeyboardButton(text="Аслануко - сын львицы", callback_data='fairy_1')],
        [InlineKeyboardButton(text="Нормэрышхо - большой Нормэр", callback_data='fairy_8')],
        [InlineKeyboardButton(text="Девочка,которая несла золото", callback_data='fairy_4')],
        [InlineKeyboardButton(text="Закрыть меню ❌", callback_data='close_library')]
    ])
















def get_format_keyboard(fairy_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Прослушать в MP3 🎧", callback_data=f"mp3_{fairy_id}")],
        [InlineKeyboardButton(text="Прочитать в PDF 📄", callback_data=f"pdf_{fairy_id}")],
        [InlineKeyboardButton(text="Вернуться к библиотеке 🔙", callback_data="back_to_library")],
        [InlineKeyboardButton(text="Закрыть меню ❌", callback_data="close_library")]
    ])