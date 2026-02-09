from datetime import datetime, date

import aiohttp


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")


    async def admin_new_user(self, name: str, telegram_id: int, amount:int, due_date: date) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/admin/new_client",
                json={
                    "telegram_id": telegram_id,
                    "full_name": name,
                    "amount": amount,
                    "due_date": due_date
                      },
            ) as resp:
                if resp.status == 400:
                    return {"message": "INVALID_DUE_DATE"}
                if resp.status == 409:
                    return {"message": "CLIENT_ALREADY_EXIST"}
                if resp.status == 400:
                    return {"message": "INVAlID_AMOUNT"}
                return await resp.json()

    async def user_start(self, telegram_id: int) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/user/start",
                json={"telegram_id": telegram_id},
            ) as resp:
                if resp.status == 403:
                    return {"action": "NO_ACCESS"}
                return await resp.json()

    async def save_phone(self, telegram_id: int, phone_number: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/user/phone",
                json={
                    "telegram_id": telegram_id,
                    "phone_number": phone_number,
                },
            ) as resp:
                if resp.status != 200:
                    raise RuntimeError("Failed to save phone")
