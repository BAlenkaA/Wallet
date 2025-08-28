from datetime import datetime

from pydantic import BaseModel


class AccountCreateDB(BaseModel):
    user_id: int
    balance: float


class AccountUpdate(BaseModel):
    balance: float


class AccountResponse(AccountUpdate):
    id: int
    created_at: datetime
