from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.plan import Plan


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Plan:
        obj = Plan(**kwargs)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def get(self, plan_id: int) -> Plan | None:
        return self.db.get(Plan, plan_id)

    def get_by_code(self, code: str) -> Plan | None:
        return self.db.execute(select(Plan).where(Plan.code == code)).scalar_one_or_none()

    def list(self) -> list[Plan]:
        return list(self.db.execute(select(Plan).order_by(Plan.id)).scalars().all())
