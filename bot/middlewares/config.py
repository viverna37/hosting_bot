from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message

class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config):
        super().__init__()
        self.config = config

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ):
        data['config'] = self.config
        return await handler(event, data)