from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_customer_service
from app.db.deps import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, service: CustomerService = Depends(get_customer_service), db: Session = Depends(get_db)):
    customer = service.create_customer(payload)
    db.commit()
    return customer


@router.get("", response_model=list[CustomerResponse])
def list_customers(service: CustomerService = Depends(get_customer_service)):
    return service.list_customers()
