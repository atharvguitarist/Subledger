from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_invoice_service
from app.db.deps import get_db
from app.schemas.invoice import InvoiceGenerateRequest, InvoiceResponse
from app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/generate/{subscription_id}", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def generate_invoice(subscription_id: int, payload: InvoiceGenerateRequest | None = None, service: InvoiceService = Depends(get_invoice_service), db: Session = Depends(get_db)):
    invoice = service.generate_invoice(subscription_id, payload.billing_period_start if payload else None)
    db.commit()
    return invoice


@router.get("", response_model=list[InvoiceResponse])
def list_invoices(service: InvoiceService = Depends(get_invoice_service)):
    return service.list_invoices()
