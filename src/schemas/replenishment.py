from datetime import datetime

from pydantic import BaseModel


class ReplenishmentCreateDB(BaseModel):
    transaction_id: str
    user_id: int
    amount: float


class WebhookRequest(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: int
    signature: str


class PaymentResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
