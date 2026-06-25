from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.invoice import Invoice


class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Invoice:
        obj = Invoice(**kwargs)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def get(self, invoice_id: int) -> Invoice | None:
        return self.db.get(Invoice, invoice_id)

    def list(self) -> list[Invoice]:
        return list(self.db.execute(select(Invoice).order_by(Invoice.id)).scalars().all())

    def update_payment(self, invoice: Invoice, amount_paid: Decimal, status: str) -> Invoice:
        invoice.amount_paid = amount_paid
        invoice.status = status
        self.db.add(invoice)
        self.db.flush()
        self.db.refresh(invoice)
        return invoice
