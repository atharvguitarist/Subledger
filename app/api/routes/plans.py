from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_plan_service
from app.db.deps import get_db
from app.schemas.plan import PlanCreate, PlanResponse
from app.services.plan_service import PlanService

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(payload: PlanCreate, service: PlanService = Depends(get_plan_service), db: Session = Depends(get_db)):
    plan = service.create_plan(payload)
    db.commit()
    return plan


@router.get("", response_model=list[PlanResponse])
def list_plans(service: PlanService = Depends(get_plan_service)):
    return service.list_plans()
