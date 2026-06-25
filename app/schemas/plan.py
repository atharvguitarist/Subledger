from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase


class PlanCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=50)
    price: Decimal = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=10)
    interval: str = Field(default="monthly", pattern="^(monthly|yearly)$")
    is_active: bool = True


class PlanResponse(ORMBase):
    id: int
    name: str
    code: str
    price: Decimal
    currency: str
    interval: str
    is_active: bool
    created_at: datetime
