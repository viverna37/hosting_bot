
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Clients


class ClientRepository:
    """
    Репозиторий для работы с клиентами
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        telegram_id: int,
        full_name: str,
        status: str = "active",
    ) -> Clients:
        """Создать клиента"""
        client = Clients(
            telegram_id=telegram_id,
            full_name=full_name,
            status=status,
        )
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def get_by_telegram_id(self, telegram_id: int) -> Clients | None:
        """Найти клиента по TG ID"""
        result = await self.session.execute(
            select(Clients).where(Clients.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, client_id: int) -> Clients | None:
        """Найти клиента по ID"""
        result = await self.session.execute(
            select(Clients).where(Clients.id == client_id)
        )
        return result.scalar_one_or_none()

    async def deactivate(self, client_id: int) -> Clients | None:
        """Деактивировать клиента"""
        client = await self.get_by_id(client_id)
        if not client:
            return None

        client.status = "inactive"
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def get_all(self):
        """Получить всех клиентов"""
        result = await self.session.execute(
            select(Clients)
        )
        return result.scalars()

    async def update_phone_number(self, telegram_id: int, phone_number: str) -> Clients | None:
        """Обновить номер телеона клиента"""
        result = await self.session.execute(
            select(Clients).where(Clients.telegram_id == telegram_id)
        )
        client = result.scalar_one_or_none()

        if not client:
            return None

        client.phone_number = phone_number
        await self.session.commit()
        await self.session.refresh(client)
        return client