from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_payment_service
from app.db.deps import get_db
from app.schemas.invoice import InvoiceResponse
from app.schemas.payment import PaymentAttemptResponse, PaymentRecordRequest, PaymentRecordResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/record/{invoice_id}", response_model=PaymentRecordResponse, status_code=status.HTTP_201_CREATED)
def record_payment(invoice_id: int, payload: PaymentRecordRequest, service: PaymentService = Depends(get_payment_service), db: Session = Depends(get_db)):
    attempt, invoice = service.record_payment(
        invoice_id=invoice_id,
        amount=payload.amount,
        currency=payload.currency,
        status=payload.status,
        provider_reference=payload.provider_reference,
        failure_reason=payload.failure_reason,
    )
    db.commit()
    return {
        "payment_attempt": PaymentAttemptResponse.model_validate(attempt),
        "invoice": InvoiceResponse.model_validate(invoice).model_dump(mode="json"),
    }
