from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Payment


class PaymentRepository:
    """
    Репозиторий для работы с платежами
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        client_id: int,
        subscription_id: int,
        payment_id: str,
        amount: int,
    ) -> Payment:
        """Создать платёж"""
        payment = Payment(
            client_id=client_id,
            subscription_id=subscription_id,
            payment_id=payment_id,
            amount=amount,
            status="pending",
        )
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def mark_succeeded(self, payment_id: str) -> Payment | None:
        """Пометить платёж успешным"""
        result = await self.session.execute(
            select(Payment).where(Payment.payment_id == payment_id)
        )
        payment = result.scalar_one_or_none()

        if not payment:
            return None

        payment.status = "succeeded"
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_by_payment_id(self, payment_id: str) -> Payment | None:
        """Получить платёж по ID платёжки"""
        result = await self.session.execute(
            select(Payment).where(Payment.payment_id == payment_id)
        )
        return result.scalar_one_or_none()
