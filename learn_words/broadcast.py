import json
import random
from aiogram import Bot

from learn_words.user_storage import load_users
from learn_words.formatting import format_word_post
from aiogram.types import InputFile

POSTS_FILE = "learn_words/posts.json"


def load_random_post():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)
    return random.choice(posts)


async def send_scheduled_words(bot: Bot):
    users = load_users()
    post = load_random_post()
    text = format_word_post(post)
    image = InputFile("assets/images/word_template.jpg")

    for user_id, settings in users.items():
        if settings.get("study_mode"):
            await bot.send_photo(
                chat_id=int(user_id),
                photo=image,
                caption=text,
                parse_mode="HTML"
            )