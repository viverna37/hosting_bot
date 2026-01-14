from sqlalchemy.ext.asyncio import AsyncSession

from database.repository.clients_repository import ClientRepository
from database.repository.payments_repository import PaymentRepository
from database.repository.subscription_repository import SubscriptionRepository


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.clients_repo = ClientRepository(session)
        self.payments_repo = PaymentRepository(session)
        self.subscriptions_repo = SubscriptionRepository(session)