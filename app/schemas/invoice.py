from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.schemas.common import ORMBase


class InvoiceGenerateRequest(BaseModel):
    billing_period_start: datetime | None = None


class InvoiceResponse(ORMBase):
    id: int
    subscription_id: int
    customer_id: int
    amount_due: Decimal
    amount_paid: Decimal
    currency: str
    status: str
    period_start: datetime
    period_end: datetime
    due_date: datetime
    created_at: datetime
