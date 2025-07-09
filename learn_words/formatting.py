def format_word_post(word_data: dict) -> str:
    return (
        f"📚 <b>Слово недели:</b> {word_data['word']} — {word_data['translation']}\n\n"
        f"💬 <i>{word_data['example']}</i>\n"
        f"🔍 {word_data['example_translation']}"
    )


def format_study_mode_status(day: str, time: str) -> str:
    return (
        f"📚 <b>Режим изучения уже включён!</b>\n\n"
        f"🗓 Вы выбрали: <b>{day}</b>\n"
        f"⏰ Время получения слов: <b>{time}</b>"
    )
