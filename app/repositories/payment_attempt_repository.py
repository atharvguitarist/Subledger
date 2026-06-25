from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.payment_attempt import PaymentAttempt


class PaymentAttemptRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> PaymentAttempt:
        obj = PaymentAttempt(**kwargs)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def list(self) -> list[PaymentAttempt]:
        return list(self.db.execute(select(PaymentAttempt).order_by(PaymentAttempt.id)).scalars().all())
