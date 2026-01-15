from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class  NewClientRequest(BaseModel):
    telegram_id: int = Field(..., gt=0, description="Telegram ID клиента")
    full_name: str = Field(..., min_length=1, max_length=255, description="Имя клиента")
    amount: int = Field(..., gt=0, description="Сумма ежемесячного платежа в рублях")
    due_date: date = Field(..., description="Первая дата оплаты (YYYY-MM-DD)")


class NewClientResponse(BaseModel):
    client_id: int
    subscription_id: int
    telegram_id: int
    full_name: str
    amount: int
    due_date: date
