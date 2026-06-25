from decimal import Decimal
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.payment_attempt_repository import PaymentAttemptRepository
from app.services.exceptions import AppException
from app.services.ledger_service import LedgerService


class PaymentService:
    def __init__(self, invoice_repo: InvoiceRepository, payment_attempt_repo: PaymentAttemptRepository, ledger_service: LedgerService):
        self.invoice_repo = invoice_repo
        self.payment_attempt_repo = payment_attempt_repo
        self.ledger_service = ledger_service

    def record_payment(self, invoice_id: int, amount: Decimal, currency: str, status: str, provider_reference: str, failure_reason: str | None = None):
        invoice = self.invoice_repo.get(invoice_id)
        if not invoice:
            raise AppException(404, "Invoice not found")
        if currency != invoice.currency:
            raise AppException(400, "Payment currency must match invoice currency")

        remaining = Decimal(str(invoice.amount_due)) - Decimal(str(invoice.amount_paid))
        if status == "succeeded" and amount > remaining:
            raise AppException(400, "A successful payment cannot exceed the remaining unpaid amount on the invoice")

        payment_attempt = self.payment_attempt_repo.create(
            invoice_id=invoice_id,
            amount=amount,
            currency=currency,
            status=status,
            provider_reference=provider_reference,
            failure_reason=failure_reason,
        )

        if status == "failed":
            self.ledger_service.create_entry(
                customer_id=invoice.customer_id,
                invoice_id=invoice.id,
                entry_type="payment_failure",
                amount=amount,
                currency=currency,
                reference_id=f"payment_attempt:{payment_attempt.id}",
                description=failure_reason or "Payment failed",
            )
            return payment_attempt, invoice

        new_amount_paid = Decimal(str(invoice.amount_paid)) + amount
        new_status = "paid" if new_amount_paid == Decimal(str(invoice.amount_due)) else "partially_paid"
        invoice = self.invoice_repo.update_payment(invoice, new_amount_paid, new_status)
        self.ledger_service.create_entry(
            customer_id=invoice.customer_id,
            invoice_id=invoice.id,
            entry_type="payment_success",
            amount=amount,
            currency=currency,
            reference_id=f"payment_attempt:{payment_attempt.id}",
            description="Payment succeeded",
        )
        return payment_attempt, invoice
