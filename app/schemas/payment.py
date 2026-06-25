from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase


class PaymentRecordRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=10)
    status: str = Field(pattern="^(succeeded|failed)$")
    provider_reference: str = Field(min_length=2, max_length=100)
    failure_reason: str | None = None


class PaymentAttemptResponse(ORMBase):
    id: int
    invoice_id: int
    amount: Decimal
    currency: str
    status: str
    provider_reference: str
    failure_reason: str | None
    created_at: datetime


class PaymentRecordResponse(BaseModel):
    payment_attempt: PaymentAttemptResponse
    invoice: dict
