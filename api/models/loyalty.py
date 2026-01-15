from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Sequence


class BurnedPointsResponse(BaseModel):
    burn_date: Optional[datetime] | None
    points: int | None

class BalanceResponse(BaseModel):
    balance: int

class HistoryItem(BaseModel):
    amount: int
    created_at: Optional[datetime]
    type: str

    model_config = ConfigDict(from_attributes=True)

class HistoryResponse(BaseModel):
    history: Sequence[HistoryItem] | None

class SpendIntentResponse(BaseModel):
    token: str
    expires_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


