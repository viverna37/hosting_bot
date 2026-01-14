from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Any, Awaitable
from database.db import db
from database.repository.main_repository import Repository


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with db.session() as session:
            data["repository"] = Repository(session)
            return await handler(event, data)