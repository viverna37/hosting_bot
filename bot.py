import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from database.db import db
from handlers import routers
from middlewares.config import ConfigMiddleware
from middlewares.database import DatabaseMiddleware

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.getLogger("aiogram").setLevel(logging.INFO)

async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await db.init(config.db.url)
    await db.create_tables()

    dp = Dispatcher()
    dp.include_routers(*routers)

    dp.update.middleware(ConfigMiddleware(config))
    dp.update.middleware(DatabaseMiddleware())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
