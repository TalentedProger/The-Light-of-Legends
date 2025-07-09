from aiogram import Dispatcher
from app.handlers import *
from learn_words import broadcast


def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(study_mode.router)
    return dp
