# import asyncio
# import logging

# from aiogram import Bot,Dispatcher
# from config import TOKEN
# from app.handlers import router
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from learn_words.db import init_db

# bot = Bot(token=TOKEN)
# dp = Dispatcher()

# async def main():
# 	dp.include_router(router)
# 	init_db()
# 	await dp.start_polling(bot)

# if __name__ == '__main__':
# 	try:
# 		asyncio.run(main())
# 	except KeyboardInterrupt: print('exit')

import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from aiogram.client.default import DefaultBotProperties
# from learn_words.db import init_db
# from learn_words.setup import setup_scheduler  # ← добавим запуск планировщика
from aiogram.enums import ParseMode

from learn_words.dispatcher import setup_dispatcher
from learn_words.scheduler import scheduled_loop



# bot = Bot(
#     token=TOKEN,
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )
dp = Dispatcher()

async def main():
    # await init_db()                # ← теперь это async
    # await setup_scheduler(bot)     # ← запускаем планировщик
    bot = Bot(token=TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
