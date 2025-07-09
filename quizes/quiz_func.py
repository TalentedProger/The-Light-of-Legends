from aiogram import F,Router
from aiogram.types import Message,CallbackQuery,InputFile
from aiogram.types.input_file import FSInputFile
from aiogram.filters import CommandStart,Command
from aiogram.enums import ParseMode
import app.keyboards as kb
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from quizes.quiz_logic import questions
from aiogram.enums.parse_mode import ParseMode 

from app.handlers import router

class QuizState(StatesGroup):
    question = State()



# Генерация кнопок ответов
def get_answer_buttons(q_index: int, selected: int = None):
    buttons = []
    for i, text in enumerate(questions[q_index]["answers"]):
        prefix = "✅ " if selected == i else ""
        buttons.append(
            [InlineKeyboardButton(text=prefix + text, callback_data=f"select_{i}")]
        )
    if selected is not None:
        buttons.append([InlineKeyboardButton(text="📨 Отправить", callback_data="submit_answer")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "start_rules")
async def show_rules(callback: CallbackQuery):
    await callback.message.edit_text(
        "📜 <b>Правила:</b>\nОтвечай на вопросы, выбирай ответ, а потом жми <b>Отправить</b>.\n\nВ конце покажем твой результат!",
        reply_markup=kb.rules_kb,parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "begin_quiz")
async def begin_quiz(callback: CallbackQuery, state: FSMContext):
    await state.update_data(current_q=0, answers=[])
    await send_question(callback.message, state)

# Показываем вопрос (редактируем сообщение)
async def send_question(message: Message, state: FSMContext):
    data = await state.get_data()
    q_index = data["current_q"]
    question = questions[q_index]
    await message.edit_text(
        question["text"],
        reply_markup=get_answer_buttons(q_index)
    )
    await state.set_state(QuizState.question)

# Выбор ответа
@router.callback_query(F.data.startswith("select_"))
async def select_answer(callback: CallbackQuery, state: FSMContext):
    selected = int(callback.data.split("_")[1])
    data = await state.get_data()
    q_index = data["current_q"]
    await state.update_data(selected=selected)
    await callback.message.edit_reply_markup(
        reply_markup=get_answer_buttons(q_index, selected)
    )

# Отправка ответа и переход к следующему
@router.callback_query(F.data == "submit_answer")
async def submit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected")
    current_q = data["current_q"]
    all_answers = data.get("answers", [])
    all_answers.append(selected)
    
    await state.update_data(answers=all_answers)
    await state.update_data(selected=None)

    next_q = current_q + 1
    if next_q < len(questions):
        await state.update_data(current_q=next_q)
        await callback.message.edit_text("✅ Ответ засчитан. Переходим к следующему вопросу...")
        await asyncio.sleep(1)
        await send_question(callback.message, state)
    else:
        await state.clear()
        await show_results(callback.message, all_answers)

# Итоги
async def show_results(message: Message, user_answers: list):
    results = []
    correct_count = 0

    for i, user_answer in enumerate(user_answers):
        correct_index = questions[i]["correct"]
        is_correct = user_answer == correct_index
        icon = "✅" if is_correct else "❌"
        correct_text = questions[i]["answers"][correct_index]
        results.append(f"{icon} Вопрос {i+1}:\nПравильный ответ — <b>{correct_text}</b>\n")
        if is_correct:
            correct_count += 1

    results.append(f"🎯 <b>Решено верно: {correct_count} / {len(questions)}</b>")
    restart_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пройти ещё раз 🔁", callback_data="begin_quiz")]
    ])
    await message.edit_text("\n".join(results),reply_markup=restart_kb,parse_mode=ParseMode.HTML)
    # await message.edit_text("\n".join(results),parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Вы отменили квиз. Напишите <b>Пройти квест 🏆</b>, чтобы начать заново.",parse_mode=ParseMode.HTML)
    await state.clear()