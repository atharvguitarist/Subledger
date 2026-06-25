from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.subscription import Subscription


class SubscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Subscription:
        obj = Subscription(**kwargs)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def get(self, subscription_id: int) -> Subscription | None:
        return self.db.get(Subscription, subscription_id)

    def list(self) -> list[Subscription]:
        return list(self.db.execute(select(Subscription).order_by(Subscription.id)).scalars().all())

    def find_active_by_customer_and_plan(self, customer_id: int, plan_id: int) -> Subscription | None:
        stmt = select(Subscription).where(
            Subscription.customer_id == customer_id,
            Subscription.plan_id == plan_id,
            Subscription.status == "active",
        )
        return self.db.execute(stmt).scalar_one_or_none()
