from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.config import Config
from bot.keyboards.ikb import IKB

router = Router()

@router.message(Command('admin'))
async def open_admin_menu(message: Message, config: Config):
    if message.from_user.id in config.tg_bot.admin_ids:
        await message.answer("Твоя админ панель", reply_markup=IKB.Admin.get_main_menu())