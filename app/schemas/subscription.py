from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase


class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_id: int
    status: str = Field(default="active", pattern="^(active|cancelled|paused)$")


class SubscriptionResponse(ORMBase):
    id: int
    customer_id: int
    plan_id: int
    status: str
    start_date: datetime
    end_date: datetime | None
    created_at: datetime
