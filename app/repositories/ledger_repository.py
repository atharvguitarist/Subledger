from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.ledger_entry import LedgerEntry


class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> LedgerEntry:
        obj = LedgerEntry(**kwargs)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def list(self) -> list[LedgerEntry]:
        return list(self.db.execute(select(LedgerEntry).order_by(LedgerEntry.id)).scalars().all())
