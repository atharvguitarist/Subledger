from datetime import datetime
from decimal import Decimal
from app.schemas.common import ORMBase


class LedgerEntryResponse(ORMBase):
    id: int
    customer_id: int
    invoice_id: int | None
    entry_type: str
    amount: Decimal
    currency: str
    reference_id: str
    description: str | None
    created_at: datetime
