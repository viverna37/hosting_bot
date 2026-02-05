import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from api_client.api_clent import ApiClient
from bot.middlewares.api_client import ApiMiddleware
from config.config import load_config
from bot.handlers import routers
from middlewares.config import ConfigMiddleware

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.getLogger("aiogram").setLevel(logging.INFO)

async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_routers(*routers)
    api_client = ApiClient(base_url=config.api.base_url)

    dp.message.middleware(ApiMiddleware(api_client))
    dp.callback_query.middleware(ApiMiddleware(api_client))
    dp.update.middleware(ConfigMiddleware(config))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
