from aiogram import BaseMiddleware
from typing import Callable, Dict, Any


class ApiMiddleware(BaseMiddleware):
    def __init__(self, api_client):
        self.api_client = api_client

    async def __call__(
        self,
        handler: Callable,
        event,
        data: Dict[str, Any]
    ):
        data["api"] = self.api_client
        return await handler(event, data)
