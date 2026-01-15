import json
from typing import Any, AsyncGenerator

from fastapi import Depends, Header, HTTPException, Request

from api.services.admin_service import AdminService
from api.services.user_service import UserService
from database.db import db
from database.repository.admin_repository import AdminRepository
from database.repository.clients_repository import ClientRepository
from database.repository.payments_repository import PaymentRepository
from database.repository.subscription_repository import SubscriptionRepository


# ---------- DB ----------
async def get_session() -> AsyncGenerator[Any, Any]:
    async with db.session() as session:
        yield session

# ---------- SERVICES ----------
def get_admin_service(
        session=Depends(get_session),
) -> AdminService:
    return AdminService(
        client_repo=ClientRepository(session),
        sub_repo=SubscriptionRepository(session),
        admin_repo=AdminRepository
    )

def get_user_service(
        session=Depends(get_session),
) -> UserService:
    return UserService(
        client_repo = ClientRepository(session),
    sub_repo =SubscriptionRepository(session),
    payments_repo = PaymentRepository(session),
    )
# ---------- AUTH ----------
async def verify_admin(
    request: Request,
    service: AdminService = Depends(get_admin_service),
):
    body = await request.json()

    telegram_id = body.get("telegram_id")
    if not telegram_id:
        raise HTTPException(status_code=400, detail="telegram_id is required")

    admin = await service.check_access(telegram_id)

    if not admin:
        raise HTTPException(status_code=403, detail="Access denied")







