from datetime import datetime, timedelta
from decimal import Decimal
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.exceptions import AppException
from app.services.ledger_service import LedgerService


class InvoiceService:
    def __init__(self, subscription_repo: SubscriptionRepository, invoice_repo: InvoiceRepository, ledger_service: LedgerService):
        self.subscription_repo = subscription_repo
        self.invoice_repo = invoice_repo
        self.ledger_service = ledger_service

    def generate_invoice(self, subscription_id: int, billing_period_start: datetime | None = None):
        subscription = self.subscription_repo.get(subscription_id)
        if not subscription:
            raise AppException(404, "Subscription not found")
        if subscription.status != "active":
            raise AppException(400, "Only active subscriptions can generate invoices")

        period_start = billing_period_start or datetime.utcnow()
        period_end = period_start + (timedelta(days=30) if subscription.plan.interval == "monthly" else timedelta(days=365))
        due_date = period_start + timedelta(days=7)
        amount_due = Decimal(str(subscription.plan.price))

        invoice = self.invoice_repo.create(
            subscription_id=subscription.id,
            customer_id=subscription.customer_id,
            amount_due=amount_due,
            amount_paid=Decimal("0.00"),
            currency=subscription.plan.currency,
            status="issued",
            period_start=period_start,
            period_end=period_end,
            due_date=due_date,
        )
        self.ledger_service.create_entry(
            customer_id=subscription.customer_id,
            invoice_id=invoice.id,
            entry_type="invoice_created",
            amount=amount_due,
            currency=subscription.plan.currency,
            reference_id=f"invoice:{invoice.id}",
            description="Invoice generated from active subscription",
        )
        return invoice

    def list_invoices(self):
        return self.invoice_repo.list()
