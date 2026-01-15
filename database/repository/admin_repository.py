from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Admin


class AdminRepository:
    """
    Репозиторий для работы с админами
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_admin(
            self,
            telegram_id: int,
    ) -> Admin | None:
        result = await self.session.execute(
            select(Admin).where(
                Admin.telegram_id == telegram_id
            )
        )
        return result.scalar_one_or_none()
