from decimal import Decimal
from app.repositories.ledger_repository import LedgerRepository


class LedgerService:
    def __init__(self, ledger_repo: LedgerRepository):
        self.ledger_repo = ledger_repo

    def create_entry(
        self,
        *,
        customer_id: int,
        invoice_id: int | None,
        entry_type: str,
        amount: Decimal,
        currency: str,
        reference_id: str,
        description: str | None = None,
    ):
        return self.ledger_repo.create(
            customer_id=customer_id,
            invoice_id=invoice_id,
            entry_type=entry_type,
            amount=amount,
            currency=currency,
            reference_id=reference_id,
            description=description,
        )
