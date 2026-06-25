from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.error_handlers import register_exception_handlers
from app.api.routes import customers, invoices, ledger, payments, plans, subscriptions
from app.core.config import settings
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
register_exception_handlers(app)

app.include_router(plans.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(subscriptions.router, prefix="/api/v1")
app.include_router(invoices.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(ledger.router, prefix="/api/v1")


@app.get("/")
def healthcheck():
    return {"message": "SubLedger API is running"}
