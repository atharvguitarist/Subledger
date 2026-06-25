from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import ORMBase


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class CustomerResponse(ORMBase):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
