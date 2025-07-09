from quizes.quiz_kb import answer_kb, final_kb
from quizes.quiz_questions import QUESTIONS

def get_rules_text(difficulty: str) -> str:
    return f"Вы выбрали {difficulty.upper()} уровень. Правила просты: выбери правильный ответ. Готовы?"

def get_question(difficulty: str, index: int):
    q = QUESTIONS[difficulty][index]
    text = f"❓ <b>Вопрос {index + 1}/{get_total_questions(difficulty)}:</b>\n\n{q['question']}"
    return text, answer_kb(q["options"])


def check_answer(difficulty: str, index: int, selected: str) -> bool:
    return QUESTIONS[difficulty][index]["correct"] == selected

def get_total_questions(difficulty: str) -> int:
    return len(QUESTIONS[difficulty])

# def get_result_summary(difficulty: str, score: int):
#     total = len(QUESTIONS[difficulty])
#     results = [
#         f"<b>🏁 Результаты:</b>\n"
#     ]
#     for i, q in enumerate(QUESTIONS[difficulty]):
#         emoji = "✅" if score > i else "❌"
#         results.append(f"{i + 1}. <b>{q['correct']}</b> — {emoji}")
    
#     stats = f"\n\n<b>📊 Статистика:</b>\n\n Решено верно:{score}/{total}"
#     return "\n".join(results) + stats, final_kb()

# def get_result_summary(difficulty: str, score: int):
#     total = len(QUESTIONS[difficulty])
#     percent = round((score / total) * 100)

#     # Итоговый текст в зависимости от процента
#     if percent > 85:
#         comment = "👏 <b>Так держать, мы гордимся вами!</b>"
#     elif percent > 60:
#         comment = "👍 <b>Очень неплохой результат, но вы можете лучше, попробуйте пройти материал еще раз!</b>"
#     else:
#         comment = "📘 <b>Довольно неожиданно, но не стоит расстраиваться — стоит еще раз подробно разобрать пройденный материал!</b>"

#     # Собираем итоговую таблицу
#     results = ["<b>🏁 Результаты:</b>\n"]
#     for i, q in enumerate(QUESTIONS[difficulty]):
#         emoji = "✅" if score > i else "❌"
#         results.append(f"{i + 1}. <b>{q['correct']}</b> — {emoji}")

#     stats = (
#         f"\n\n<b>📊 Статистика:</b>\n⚡️ Решено верно:<b>{score}/{total}</b>\n"
#         f"📈 Знание раздела: <b>{percent}%.</b>\n\n"
#         f"{comment}"
#     )

#     return "\n".join(results) + stats, final_kb()

def get_result_summary(difficulty: str, answers: list[bool]):
    total = len(QUESTIONS[difficulty])
    score = sum(answers)
    percent = round((score / total) * 100)

    if percent > 85:
        comment = "👏 <b>Так держать, мы гордимся вами!</b>"
    elif percent > 60:
        comment = "👍 <b>Очень неплохой результат, но вы можете лучше!</b>"
    else:
        comment = "📘 <b>Не расстраивайтесь — повторение поможет вам стать лучше!</b>"

    results = ["<b>🏁 Результаты:</b>\n"]
    for i, q in enumerate(QUESTIONS[difficulty]):
        correct_answer = q["correct"]
        result_emoji = "✅" if answers[i] else "❌"
        results.append(f"{i + 1}. <b>{correct_answer}</b> — {result_emoji}")

    stats = (
        f"\n\n<b>📊 Статистика:</b>\n"
        f"⚡️ Верных ответов: <b>{score}/{total}</b>\n"
        f"📈 Знание раздела: <b>{percent}%</b>\n\n"
        f"{comment}"
    )

    return "\n".join(results) + stats, final_kb()
