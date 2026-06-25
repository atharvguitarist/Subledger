from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_subscription_service
from app.db.deps import get_db
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(payload: SubscriptionCreate, service: SubscriptionService = Depends(get_subscription_service), db: Session = Depends(get_db)):
    subscription = service.create_subscription(payload)
    db.commit()
    return subscription


@router.get("", response_model=list[SubscriptionResponse])
def list_subscriptions(service: SubscriptionService = Depends(get_subscription_service)):
    return service.list_subscriptions()
