from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.repositories.ledger_repository import LedgerRepository
from app.schemas.ledger import LedgerEntryResponse

router = APIRouter(prefix="/ledger", tags=["Ledger"])


@router.get("", response_model=list[LedgerEntryResponse])
def list_ledger_entries(db: Session = Depends(get_db)):
    return LedgerRepository(db).list()
