from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Customer:
        obj = Customer(**kwargs)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def get(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        return self.db.execute(select(Customer).where(Customer.email == email)).scalar_one_or_none()

    def list(self) -> list[Customer]:
        return list(self.db.execute(select(Customer).order_by(Customer.id)).scalars().all())
