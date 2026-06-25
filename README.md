# SubLedger - SaaS Subscription & Billing System

SubLedger is a clean FastAPI backend for managing plans, customers, subscriptions, invoices, payment attempts, and append-only ledger entries.

## Stack
- FastAPI
- SQLAlchemy 2.0 ORM
- SQLite by default for easy local setup
- Pytest for business-rule tests
- Docker + docker-compose

## Features
- Clear separation of routes, services, repositories, models, schemas, config, and DB session logic.
- Business-rule validation in services.
- Invoice generation and payment recording flows.
- Append-only ledger entries with traceable `reference_id`.
- Swagger docs at `/docs`.

## Project structure
```text
app/
  api/
    routes/
    dependencies.py
    error_handlers.py
  core/
    config.py
  db/
    base.py
    deps.py
    init_db.py
    session.py
  models/
  repositories/
  schemas/
  services/
tests/
```

## Quick start
### Option 1: Local
```bash
bash run.sh
```
The app starts at `http://127.0.0.1:8000`.

### Option 2: Docker
```bash
docker compose up --build
```
The app starts at `http://127.0.0.1:8000`.

## Manual local setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## API list
- `POST /api/v1/plans`
- `GET /api/v1/plans`
- `POST /api/v1/customers`
- `GET /api/v1/customers`
- `POST /api/v1/subscriptions`
- `GET /api/v1/subscriptions`
- `POST /api/v1/invoices/generate/{subscription_id}`
- `GET /api/v1/invoices`
- `POST /api/v1/payments/record/{invoice_id}`
- `GET /api/v1/ledger`

## Sample flow
1. Create a plan.
2. Create a customer.
3. Create a subscription.
4. Generate an invoice for the subscription.
5. Record a payment for the invoice.
6. Inspect ledger entries.

## Assumptions
- Billing interval is monthly or yearly.
- Invoice generation uses the plan price at the time of invoice creation.
- Due date is seven days from invoice issue in the base version.
- SQLite is used by default for portability; the design is repository-based and can be moved to Postgres later.

## Limitations
- No authentication/authorization.
- No background jobs or recurring scheduler.
- No webhook-based provider integration.
- No proration, taxes, coupons, or refunds in this base version.

## Tests
```bash
pytest -q
```

## GitHub upload
After extracting the zip, initialize git and push:
```bash
git init
git add .
git commit -m "Initial SubLedger submission"
```
