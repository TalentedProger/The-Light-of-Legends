import asyncio
import datetime
from aiogram import Bot

from learn_words.user_storage import load_users
from learn_words.broadcast import load_random_post
from learn_words.formatting import format_word_post


async def scheduled_loop(bot: Bot):
    while True:
        now = datetime.datetime.now()
        users = load_users()
        for uid, info in users.items():
            if info.get("study_mode"):
                # Сравниваем день недели и время
                if (
                    info["day"] == now.strftime("%A").lower() and
                    info["time"] == now.strftime("%H:%M")
                ):
                    word = load_random_post()
                    await bot.send_message(
                        chat_id=int(uid),
                        text=format_word_post(word),
                        parse_mode="HTML"
                    )
        await asyncio.sleep(60)  # Проверка каждую минуту
