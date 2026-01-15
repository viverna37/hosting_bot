from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..models import Subscription


class SubscriptionRepository:
    """
    Репозиторий для работы с подписками
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        client_id: int,
        amount: int,
        due_date: datetime,
    ) -> Subscription:
        """Создать подписку"""
        subscription = Subscription(
            client_id=client_id,
            amount=amount,
            due_date=due_date,
            status="pending",
        )
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def get_active_by_client(
        self,
        client_id: int
    ) -> Subscription | None:
        """Активная подписка клиента"""
        result = await self.session.execute(
            select(Subscription).where(
                Subscription.client_id == client_id,
                Subscription.status != "paid",
            )
        )
        return result.scalar_one_or_none()

    async def mark_paid(self, subscription_id: int) -> Subscription | None:
        """Пометить как оплаченную"""
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        subscription = result.scalar_one_or_none()

        if not subscription:
            return None

        subscription.status = "paid"
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def update_notification_time(
        self,
        subscription_id: int,
        notify_time: datetime,
    ) -> None:
        """Обновить время последнего уведомления"""
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        subscription = result.scalar_one_or_none()

        if not subscription:
            return

        subscription.last_notification_at = notify_time
        await self.session.commit()

    async def get_pending(self):
        """Получить все неоплаченные подписки"""
        result = await self.session.execute(
            select(Subscription).where(Subscription.status == "pending")
        )
        return result.scalars()

    async def get_by_id(self, subscription_id: int) -> Subscription | None:
        """Найти подписку по ID"""
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        return result.scalar_one_or_none()