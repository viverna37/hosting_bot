import aiohttp


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

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
