from aiogram import F,Router
from aiogram.types import Message,CallbackQuery,InputFile
from aiogram.types.input_file import FSInputFile
from aiogram.filters import CommandStart,Command
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto,InputMediaDocument
import app.keyboards as kb
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from pathlib import Path
from quizes.quiz_kb import *
from quizes.quiz_logic import *
from library.library_kb import *
from library.library_list import FAIRY_DATA
from proverbs.proverbs_service import *
from proverbs.proverbs_state import ProverbStates
from legends.legends_service import *
from legends.legends_state import LegendState
from songs import songs_logic as logic

import galery.logic as gal_logic
import myths.logic as myths_logic


from learn_words.study_mode_kb import *
from learn_words.user_storage import get_user, update_user, delete_user
from learn_words.formatting import format_study_mode_status



router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    photo = FSInputFile("assets/images/welcome2.jpg")
    # путь к локальному файлу с начальным фото
    await message.answer_photo(
        photo=photo,
        caption=(
            f"<b>{message.from_user.first_name}, добро пожаловать в виртуальный музей культурного наследия «Свет легенд» 💚</b>\n\n"
            "Здесь ты найдёшь удивительные сказки, мифы, легенды, пословицы и народные песни адыгского народа. Мы собрали для тебя частицы богатой культуры Адыгеи, чтобы ты мог узнать больше о её традициях и ценностях ✨\n\n"
            "Погрузись в мир сказок и легенд прямо сейчас 💫"
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=kb.main
    )


# реализация квиза
class QuizStates(StatesGroup):
    selecting_difficulty = State()
    in_quiz = State()
    finished = State()

@router.message(F.text == "Квест 🏆")
async def start_quiz_entry(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(
        "🧠 Проверьте свою интуицию, логику и знания в коротком, но увлекательном квизе!\n\n"
        "🌟 <b>Готовы начать ?</b>",
        reply_markup=start_quiz_kb(),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "quiz_yes")
async def select_difficulty(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Перед началом выберите тему :</b>\n\n"
        # "Перед началом выберите тему:\n\n"
        "⭐ <b>Мир Адыгов</b>\n"
        "⭐ <b>Культура Адыгов</b>\n",
        reply_markup=difficulty_kb(),
        parse_mode="HTML"
    )
    await callback.answer("Режим запускается ⚙️", show_alert=False)
    await state.set_state(QuizStates.selecting_difficulty)
     


@router.callback_query(F.data == "quiz_no")
async def cancel_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer("Выход из квиза 🛑", show_alert=False)


@router.callback_query(F.data.startswith("diff_"))
async def difficulty_chosen(callback: CallbackQuery, state: FSMContext):
    difficulty = callback.data.split("_")[1]
    # await state.update_data(difficulty=difficulty, current_q=0, score=0)
    await state.update_data(difficulty=difficulty, current_q=0, score=0, answers=[])


    await callback.message.edit_text(
        f"<b>📜 Викторина охватывает основные аспекты адыгской культуры, включая мифологию, легенды и традиции.</b>\n\n"
        "❔ Вы будете получать вопросы с вариантами ответа.\n\n"
        "⏩️ Нажмите на верный — и сразу переходите дальше.\n\n"
        "⏳ Не торопитесь! Количество времени не ограниченно!\n",
        reply_markup=start_or_exit_kb(),
        parse_mode="HTML"
    )
    await callback.answer(f"Выбран режим: {difficulty.upper()} 🎮", show_alert=False)



@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    difficulty = data["difficulty"]
    question, keyboard = get_question(difficulty, 0)
    await callback.message.edit_text(question, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("Вперёд! Первый вопрос 🧠", show_alert=False)
    await state.set_state(QuizStates.in_quiz)

# @router.callback_query(F.data.startswith("ans_"))
# async def process_answer(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     difficulty = data["difficulty"]
#     q_index = data["current_q"]
#     correct = check_answer(difficulty, q_index, callback.data.split("_")[1])
    
#     if correct:
#         data["score"] += 1
#         await callback.answer("✅ Верно!", show_alert=False)
#     else:
#         await callback.answer("❌ Неверно!", show_alert=False)

#     data["current_q"] += 1

#     if data["current_q"] >= get_total_questions(difficulty):
#         result_text, final_kb = get_result_summary(difficulty, data["score"])
#         await callback.message.edit_text(result_text, reply_markup=final_kb, parse_mode="HTML")
#         await state.set_state(QuizStates.finished)
#     else:
#         await state.update_data(current_q=data["current_q"], score=data["score"])
#         question, keyboard = get_question(difficulty, data["current_q"])
#         await callback.message.edit_text(question, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("ans_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    difficulty = data["difficulty"]
    q_index = data["current_q"]
    selected = callback.data.split("_")[1]

    is_correct = check_answer(difficulty, q_index, selected)

    # Сохраняем ответ
    answers = data.get("answers", [])
    answers.append(is_correct)

    if is_correct:
        data["score"] += 1
        await callback.answer("✅ Верно!", show_alert=False)
    else:
        await callback.answer("❌ Неверно!", show_alert=False)

    data["current_q"] += 1

    if data["current_q"] >= get_total_questions(difficulty):
        result_text, final_kb = get_result_summary(difficulty, answers)
        await callback.message.edit_text(result_text, reply_markup=final_kb, parse_mode="HTML")
        await state.set_state(QuizStates.finished)
    else:
        await state.update_data(current_q=data["current_q"], score=data["score"], answers=answers)
        question, keyboard = get_question(difficulty, data["current_q"])
        await callback.message.edit_text(question, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "change_mode")
async def change_mode(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>🔄 Сменим тему: </b>\n\n"
        "Выберите новый режим:",
        reply_markup=difficulty_kb(),
        parse_mode="HTML"
    )
    await callback.answer("Выберите новый уровень 🎚", show_alert=False)
    await state.set_state(QuizStates.selecting_difficulty)

@router.callback_query(F.data == "restart_quiz")
async def restart_quiz(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # await state.update_data(current_q=0, score=0)
    await state.update_data(current_q=0, score=0, answers=[])

    question, keyboard = get_question(data["difficulty"], 0)
    await callback.message.edit_text(question, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("Начнём заново 🔄", show_alert=False)
    await state.set_state(QuizStates.in_quiz)

@router.callback_query(F.data == "exit")
async def exit_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer("Выход из квиза 👋", show_alert=False)
    await state.clear()

# Обработчик входа в библиотеку
@router.message(F.text == "Библиотека 📚")
async def open_library_menu(message: Message):
    await message.delete()
    await message.answer(
        "<b>📚 Выберите интересующую вас сказку!</b>",
        reply_markup=get_library_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("fairy_"))
async def open_format_menu(callback: CallbackQuery):
    fairy_id = callback.data.split("_")[1]
    await callback.message.edit_text(
        "<b>📥 Выберите удобный формат:</b>",
        reply_markup=get_format_keyboard(fairy_id),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_library")
async def back_to_library(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📚 Выберите интересующую вас сказку!</b>",
        reply_markup=get_library_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "close_library")
async def close_library(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Меню закрыто", show_alert=False)

@router.callback_query(F.data.startswith("mp3_"))
async def send_mp3(callback: CallbackQuery):
    fairy_id = callback.data.split("_")[1]
    fairy = FAIRY_DATA.get(fairy_id)

    if not fairy:
        return await callback.answer("Неизвестная сказка ❌", show_alert=True)

    file_path = f"assets/mp3/{fairy['mp3']}"
    try:
        await callback.answer("📤 Загружаем аудио...", show_alert=False)
        audio = FSInputFile(file_path)
        await callback.answer()
        await callback.message.answer_audio(
            audio=audio,
            caption=f"\n\n🎧 <b>{fairy['title']}</b>\n\nПриятного вам прослушивания 💚",
            parse_mode="HTML"
        )
        await callback.answer("Записываем аудио...", show_alert=False)
    except FileNotFoundError:
        await callback.answer("Файл MP3 не найден ❌", show_alert=True)


@router.callback_query(F.data.startswith("pdf_"))
async def send_pdf(callback: CallbackQuery):
    fairy_id = callback.data.split("_")[1]
    fairy = FAIRY_DATA.get(fairy_id)

    if not fairy:
        return await callback.answer("Неизвестная сказка ❌", show_alert=True)

    file_path = f"assets/pdf/{fairy['pdf']}"
    try:
        await callback.answer("📤 Загружаем документ...", show_alert=False)
        pdf = FSInputFile(file_path)
        await callback.answer()
        await callback.message.answer_document(
            document=pdf,
            caption=f"\n\n📄 <b>{fairy['title']}</b>\n\nПриятного вам чтения 💚",
            parse_mode="HTML"
        )
    except FileNotFoundError:
        await callback.answer("Файл PDF не найден ❌", show_alert=True)


@router.message(F.text == "Пословицы 📝")
async def send_random_proverb(message: Message, state: FSMContext):
    await state.set_state(ProverbStates.viewing)
    sent_ids = set()
    await state.update_data(sent_ids=sent_ids)

    img_id = get_random_image_id(exclude_list=sent_ids)
    sent_ids.add(img_id)
    await state.update_data(sent_ids=sent_ids)

    img_path = get_image_path(img_id)
    caption = f"<b>💚 Адыгские пословицы</b>"
    await message.delete()
    await message.answer_photo(
        photo=FSInputFile(img_path),
        caption=caption,
        reply_markup=kb.get_proverbs_keyboard(img_id),parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "next_proverb")
async def next_proverb(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sent_ids = data.get("sent_ids", set())

    current_img_id = callback.message.reply_markup.inline_keyboard[1][0].callback_data.split(":")[1]
    sent_ids.add(current_img_id)

    available_ids = set(get_all_image_ids()) - sent_ids
    if not available_ids:
        await callback.answer("Вы просмотрели все пословицы 🙌", show_alert=True)
        return

    new_img_id = random.choice(list(available_ids))
    sent_ids.add(new_img_id)
    await state.update_data(sent_ids=sent_ids)

    img_path = get_image_path(new_img_id)
    caption = "<b>Адыгские пословицы 💚</b>"

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(img_path),
            caption=caption,
            parse_mode=ParseMode.HTML  # ✅ Работает только внутри InputMediaPhoto
        ),
        reply_markup=kb.get_proverbs_keyboard(new_img_id)
    )
    await callback.answer("Вот новая пословица ✨")

@router.callback_query(F.data.startswith("copy_proverb:"))
async def copy_proverb_text(callback: CallbackQuery):
    img_id = callback.data.split(":")[1]
    text = get_text_for_image(img_id)

    await callback.message.edit_caption(
        caption=f"<b>Скопируй пословицу 👇</b>\n\n<code><b>{text}</b></code>",
        parse_mode="HTML",
        reply_markup=kb.get_proverbs_keyboard(img_id)
    )
    await callback.answer("Теперь можно легко скопировать ✂️")




@router.callback_query(F.data == "exit_proverb_mode")
async def exit_proverb(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.answer("Режим пословиц закрыт ✅")

#Легенды
@router.message(F.text == "Легенды ⚜️")
async def show_first_legend(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(LegendState.viewing)
    shown = set()
    legend_id = get_random_legend_id()
    shown.add(legend_id)
    await state.update_data(shown=shown, current=legend_id)

    title = get_title(legend_id)
    caption = f"<b>{title}</b> ✨"
    await message.answer_document(
        document=FSInputFile(get_pdf_path(legend_id)),
        caption=caption,
        reply_markup=kb.get_legend_keyboard(legend_id),parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "legend_next")
async def next_legend(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    shown = data.get("shown", set())

    try:
        legend_id = get_random_legend_id(exclude=shown)
    except ValueError:
        await callback.answer("Вы посмотрели все легенды ✨", show_alert=True)
        return

    shown.add(legend_id)
    await state.update_data(shown=shown, current=legend_id)

    caption = f"<b>{get_title(legend_id)} ✨</b>"

    await callback.answer("Выбираем новую легенду ✨")
    await callback.message.edit_media(
        media=InputMediaDocument(
            media=FSInputFile(get_pdf_path(legend_id)),
            caption=caption,
            parse_mode=ParseMode.HTML  # ✅ Правильное место
        ),
        reply_markup=kb.get_legend_keyboard(legend_id)
    )
    


@router.callback_query(F.data.startswith("legend_info:"))
async def show_legend_description(callback: CallbackQuery, state: FSMContext):
    legend_id = callback.data.split(":")[1]
    text = f"<b>{get_title(legend_id)}</b>\n\n{get_description(legend_id)}"
    await callback.message.edit_caption(caption=text, reply_markup=kb.get_legend_keyboard(legend_id),parse_mode=ParseMode.HTML)
    await callback.answer("Описание добавлено 📖")

@router.callback_query(F.data == "legend_exit")
async def exit_legend(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.answer("Режим легенд завершён ✅")


#отправка аудио
@router.message(F.text == "Песни 🎶")
async def start_songs(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(sent_songs=set())
    await send_new_song(message, state)

@router.callback_query(F.data == "next_song")
async def next_song(callback: CallbackQuery, state: FSMContext):
    await send_new_song(callback.message, state)
    await callback.answer("Вот новая песня 🎶")

@router.callback_query(F.data == "exit_song_mode")
async def exit_song_mode(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы покинули режим песен 👋", show_alert=False)

# 🔁 Общая функция для отправки песни
async def send_new_song(message_or_cbmsg, state: FSMContext):
    data = await state.get_data()
    sent = set(data.get("sent_songs", []))

    try:
        song = logic.get_random_song(sent)
    except ValueError:
        await message_or_cbmsg.answer("Вы прослушали все песни 🙌")
        return

    audio = FSInputFile(logic.get_song_path(song))
    description = logic.get_song_description(song)

    await message_or_cbmsg.answer_audio(
        audio=audio,
        caption=f"\n\n\n<b>Погрузитесь в мир адыгской музыки и проникнитесь каждой нотой 💚</b>",
        # caption=f"\n\n<b>{description} 💚</b>",
        parse_mode="HTML",
        reply_markup=kb.get_song_keyboard()
    )

    sent.add(song)
    await state.update_data(sent_songs=sent)

# router.include_router(galery_router)

#ГАЛЕРЕЯ 
@router.message(F.text == "Галерея 📸")
async def start_gallery(message: Message, state: FSMContext):
    index = 0
    item = gal_logic.get_gallery_item(index)
    if not item:
        await message.answer("Галерея пуста 😢")
        return
    
    await message.delete()
    await state.update_data(gallery_index=index)

    await message.answer_photo(
        photo=FSInputFile(gal_logic.get_image_path(item['filename'])),
        caption=(
            "Галерея иллюстраций художественного творчества 💚\n\n"
            f"<b>Название:</b> {item['title']}\n"
            f"<b>Автор:</b> {item['author']}"
        ),
        reply_markup=kb.get_gallery_keyboard(index),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("gallery_next"))
async def next_picture(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("gallery_index", 0) + 1

    if index >= gal_logic.total_items():
        await callback.answer("Вы просмотрели все картины 🖼", show_alert=True)
        return

    item = gal_logic.get_gallery_item(index)
    await state.update_data(gallery_index=index)

    await callback.message.edit_media(
        media={
            "type": "photo",
            "media": FSInputFile(gal_logic.get_image_path(item["filename"])),
            "caption": (
                "Галерея иллюстраций художественного творчества 💚\n\n"
                f"<b>Название:</b> {item['title']}\n"
                f"<b>Автор:</b> {item['author']}"
            )
        },
        reply_markup=kb.get_gallery_keyboard(index),
        parse_mode="HTML"
    )
    await callback.answer("Новая картина загружена 🎨")


@router.callback_query(F.data == "gallery_exit")
async def exit_gallery(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.answer("Вы покинули галерею 🌙")


#МИФЫЫЫЫЫЫЫЫ
@router.message(F.text == "Мифы 🔮")
async def start_myths(message: Message, state: FSMContext):
    index = 0
    item = myths_logic.get_myths_item(index)
    if not item:
        await message.answer("Галерея пуста 😢")
        return
    await message.delete()
    await state.update_data(myths_index=index)

    await message.answer_photo(
        photo=FSInputFile(myths_logic.get_image_path(item['filename'])),
        caption=(
            "Галерея иллюстраций адыгских мифов 💚\n\n"
            f"<b>Название:</b> {item['title']}\n"
        ),
        reply_markup=kb.get_myths_keyboard(index),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("myths_next"))
async def next_picture(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("myths_index", 0) + 1

    if index >= myths_logic.total_items():
        await callback.answer("Вы просмотрели все картины 🖼", show_alert=True)
        return

    item = myths_logic.get_myths_item(index)
    await state.update_data(myths_index=index)

    await callback.message.edit_media(
        media={
            "type": "photo",
            "media": FSInputFile(myths_logic.get_image_path(item["filename"])),
            "caption": (
                "Галерея иллюстраций художественного творчества 💚\n\n"
                f"<b>Название:</b> {item['title']}\n"
            )
        },
        reply_markup=kb.get_myths_keyboard(index),
        parse_mode="HTML"
    )
    await callback.answer("Новая картина загружена 🎨")


@router.callback_query(F.data == "myths_exit")
async def exit_myths(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.answer("Вы покинули раздел мифов 🌙")



    #изучение новых слов 

@router.message(F.text == "Изучить новые слова 📖")
async def start_study_mode(msg: Message):
    user = get_user(msg.from_user.id)
    if user.get("study_mode"):
        await msg.answer(
            format_study_mode_status(user['day'], user['time']),
            reply_markup=mode_already_enabled_kb(),
            parse_mode=ParseMode.HTML
        )
    else:
        await msg.answer(
            "<b>📖 Режим изучения слов</b>\n\n"
            "Хотите включить 📚 <b>режим изучения новых слов</b>?\n\n"
            "Если готовы — давайте выберем удобное время и день для получения слов 🕒.",
            reply_markup=stage_one_kb(),
            parse_mode=ParseMode.HTML
        )


@router.callback_query(F.data == "to_stage_2")
async def choose_day(call: CallbackQuery):
    await call.message.edit_text(
        "📆 <b>Выберите удобный день недели</b> для получения слов:",
        reply_markup=day_selection_kb(),
        parse_mode=ParseMode.HTML
    )
    await call.answer("Вы на шаг ближе к изучению новых слов! 📘")


@router.callback_query(F.data.startswith("day_"))
async def save_day(call: CallbackQuery):
    day = call.data.split("_")[1]
    update_user(call.from_user.id, {"day": day})
    await call.message.edit_reply_markup(reply_markup=day_selection_kb(selected_day=day))
    await call.answer("День недели выбран! ✅")


@router.callback_query(F.data == "to_stage_3")
async def choose_time(call: CallbackQuery):
    await call.message.edit_text(
        "🕒 <b>Выберите удобное время</b> для получения новых слов:",
        reply_markup=time_selection_kb(),
        parse_mode=ParseMode.HTML
    )
    await call.answer("Почти готово ⏳")


@router.callback_query(F.data.startswith("time_"))
async def save_time(call: CallbackQuery):
    time = call.data.split("_")[1]
    update_user(call.from_user.id, {"time": time})
    await call.message.edit_reply_markup(reply_markup=time_selection_kb(selected_time=time))
    await call.answer("Время установлено! ⏰")


@router.callback_query(F.data == "to_stage_4")
async def confirm_setup(call: CallbackQuery):
    update_user(call.from_user.id, {"study_mode": True})
    user = get_user(call.from_user.id)
    await call.message.edit_text(
        f"✅ <b>Режим успешно включён!</b>\n\n"
        f"Вы будете получать новое слово <b>каждый {user['day']} в {user['time']}</b>. 📬",
        reply_markup=final_stage_kb(),
        parse_mode=ParseMode.HTML
    )
    await call.answer("Готово! Начнём изучать 💡")


@router.callback_query(F.data == "restart_setup")
async def restart(call: CallbackQuery):
    await call.message.edit_text(
        "<b>📖 Режим изучения слов</b>\n\n"
        "Хотите включить 📚 <b>режим изучения новых слов</b>?\n\n"
        "Если готовы — давайте выберем удобное время и день для получения слов 🕒.",
        reply_markup=stage_one_kb(),
        parse_mode=ParseMode.HTML
    )
    await call.answer("Начнём заново 🔄")


@router.callback_query(F.data == "disable_mode")
async def disable(call: CallbackQuery):
    update_user(call.from_user.id, {"study_mode": False})
    await call.answer("Режим отключён ❌", show_alert=True)
    await call.message.delete()


@router.callback_query(F.data == "exit_mode")
async def just_exit(call: CallbackQuery):
    await call.message.delete()
    await call.answer("Закрыто 👌", show_alert=False)

#о нас 

EMAIL = "svet-legend@yandex.ru"  # замените на ваш email

@router.message(F.text == "О нас ℹ️")
async def about_us(message: Message):
    await message.delete()
    photo = FSInputFile("assets/images/word_template.jpg")
    text = (
        "<b>Университет:</b> ФГБОУ ВО «Майкопский Государственный Технологический университет»\n"
        "<b>Автор идеи:</b> Мешвез Изабелла Рашидовна"
    )

    await message.answer_photo(photo=photo, caption=text, reply_markup=kb.about_inline_kb,parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "contact")
async def contact_callback(callback: CallbackQuery):
    await callback.answer(text=f"Наша почта: {EMAIL}", show_alert=True)

@router.callback_query(F.data == "close")
async def close_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

#оценить проект 

@router.message(F.text == "Оценить проект ⭐")
async def review_project(message: Message):
    await message.delete()
    photo = FSInputFile("assets/images/welcome.jpg")  # замените на актуальное изображение
    text = (
        "<b>Оцените наш проект!</b>\n"
        "Ваше мнение — наша мотивация 💚"
        "Поделитесь своими впечатлениями о проекте <b>«Свет легенд»</b>\n\nВы можете оставить отзыв и помочь нам стать лучше!"
    )

    await message.answer_photo(photo=photo, caption=text, reply_markup=kb.review_inline_kb, parse_mode="HTML")

@router.callback_query(F.data == "exit_review")
async def exit_review(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()