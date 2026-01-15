from datetime import date
from exceptions import (
    ClientAlreadyExistsError,
    InvalidDueDateError,
    InvalidAmountError,
)


class AdminService:
    def __init__(
        self,
        client_repo,
        sub_repo,
            admin_repo
    ):
        self.client_repo = client_repo
        self.sub_repo = sub_repo
        self.admin_repo = admin_repo

    async def check_access(self, telegram_id: int) -> bool:
        row = await self.admin_repo.get_admin(telegram_id)
        return True if row else False

    async def create_client(
        self,
        telegram_id: int,
        full_name: str,
        amount: int,
        due_date: date,
    ):
        # Проверка на дубль
        client = await self.client_repo.get_by_telegram_id(telegram_id)
        if client:
            raise ClientAlreadyExistsError()

        # Проверка даты
        today = date.today()
        if due_date < today:
            raise InvalidDueDateError()

        # Проверка суммы
        if amount <= 0:
            raise InvalidAmountError()

        # Создание клиента
        client = await self.client_repo.create(
            telegram_id=telegram_id,
            full_name=full_name,
        )

        # Создание подписки
        subscription = await self.sub_repo.create(
            client_id=client.id,
            amount=amount,
            due_date=due_date,
        )

        return {
            "client_id": client.id,
            "subscription_id": subscription.id,
            "telegram_id": client.telegram_id,
            "full_name": client.full_name,
            "amount": subscription.amount,
            "due_date": subscription.due_date,
        }
