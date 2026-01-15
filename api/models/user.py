from datetime import date
from typing import Literal, Union

from pydantic import BaseModel, Field


class UserStartRequest(BaseModel):
    telegram_id: int = Field(..., gt=0, description="Telegram ID пользователя")

class RequestPhoneResponse(BaseModel):
    action: Literal["REQUEST_PHONE"]

class ClientInfo(BaseModel):
    id: int
    telegram_id: int
    full_name: str
    phone_number: str
    status: str

class SubscriptionInfo(BaseModel):
    id: int | None
    amount: int | None
    due_date: date | None
    status: str | None

class ShowCabinetResponse(BaseModel):
    action: Literal["SHOW_CABINET"]
    client: ClientInfo
    subscription: SubscriptionInfo

UserStartResponse = Union[
    RequestPhoneResponse,
    ShowCabinetResponse,
]

class SavePhoneRequest(BaseModel):
    telegram_id: int = Field(..., gt=0)
    phone_number: str = Field(..., min_length=5, max_length=20)

class SavePhoneResponse(BaseModel):
    success: bool
