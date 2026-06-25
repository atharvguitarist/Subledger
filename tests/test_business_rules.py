def create_plan(client, **overrides):
    payload = {
        "name": "Starter",
        "code": "starter",
        "price": "99.00",
        "currency": "USD",
        "interval": "monthly",
        "is_active": True,
    }
    payload.update(overrides)
    return client.post("/api/v1/plans", json=payload)


def create_customer(client, **overrides):
    payload = {"name": "Alice", "email": "alice@example.com"}
    payload.update(overrides)
    return client.post("/api/v1/customers", json=payload)


def create_subscription(client, customer_id, plan_id, **overrides):
    payload = {"customer_id": customer_id, "plan_id": plan_id, "status": "active"}
    payload.update(overrides)
    return client.post("/api/v1/subscriptions", json=payload)


def test_plan_price_must_be_gt_zero(client):
    response = create_plan(client, price="0")
    assert response.status_code == 422


def test_customer_email_must_be_unique(client):
    assert create_customer(client).status_code == 201
    response = create_customer(client)
    assert response.status_code == 409
    assert "unique" in response.json()["detail"].lower()


def test_cannot_create_subscription_for_inactive_plan(client):
    plan_id = create_plan(client, code="inactive-plan", is_active=False).json()["id"]
    customer_id = create_customer(client).json()["id"]
    response = create_subscription(client, customer_id, plan_id)
    assert response.status_code == 400
    assert "inactive plan" in response.json()["detail"].lower()


def test_customer_cannot_have_two_active_subscriptions_to_same_plan(client):
    plan_id = create_plan(client).json()["id"]
    customer_id = create_customer(client).json()["id"]
    assert create_subscription(client, customer_id, plan_id).status_code == 201
    response = create_subscription(client, customer_id, plan_id)
    assert response.status_code == 409


def test_invoice_amount_due_uses_plan_price_snapshot_at_generation_time(client):
    plan_id = create_plan(client, price="149.00").json()["id"]
    customer_id = create_customer(client).json()["id"]
    subscription_id = create_subscription(client, customer_id, plan_id).json()["id"]
    response = client.post(f"/api/v1/invoices/generate/{subscription_id}", json={})
    assert response.status_code == 201
    assert response.json()["amount_due"] == "149.00"


def test_success_payment_cannot_exceed_remaining_amount(client):
    plan_id = create_plan(client, price="100.00").json()["id"]
    customer_id = create_customer(client).json()["id"]
    subscription_id = create_subscription(client, customer_id, plan_id).json()["id"]
    invoice_id = client.post(f"/api/v1/invoices/generate/{subscription_id}", json={}).json()["id"]
    response = client.post(f"/api/v1/payments/record/{invoice_id}", json={
        "amount": "120.00",
        "currency": "USD",
        "status": "succeeded",
        "provider_reference": "pay_001"
    })
    assert response.status_code == 400


def test_partial_and_full_payment_update_invoice_status(client):
    plan_id = create_plan(client, price="100.00").json()["id"]
    customer_id = create_customer(client).json()["id"]
    subscription_id = create_subscription(client, customer_id, plan_id).json()["id"]
    invoice_id = client.post(f"/api/v1/invoices/generate/{subscription_id}", json={}).json()["id"]

    partial = client.post(f"/api/v1/payments/record/{invoice_id}", json={
        "amount": "40.00",
        "currency": "USD",
        "status": "succeeded",
        "provider_reference": "pay_002"
    })
    assert partial.status_code == 201
    assert partial.json()["invoice"]["status"] == "partially_paid"
    assert partial.json()["invoice"]["amount_paid"] == "40.00"

    full = client.post(f"/api/v1/payments/record/{invoice_id}", json={
        "amount": "60.00",
        "currency": "USD",
        "status": "succeeded",
        "provider_reference": "pay_003"
    })
    assert full.status_code == 201
    assert full.json()["invoice"]["status"] == "paid"
    assert full.json()["invoice"]["amount_paid"] == "100.00"


def test_failed_payment_does_not_increase_amount_paid_and_creates_ledger(client):
    plan_id = create_plan(client, price="100.00").json()["id"]
    customer_id = create_customer(client).json()["id"]
    subscription_id = create_subscription(client, customer_id, plan_id).json()["id"]
    invoice_id = client.post(f"/api/v1/invoices/generate/{subscription_id}", json={}).json()["id"]

    failed = client.post(f"/api/v1/payments/record/{invoice_id}", json={
        "amount": "25.00",
        "currency": "USD",
        "status": "failed",
        "provider_reference": "pay_004",
        "failure_reason": "declined"
    })
    assert failed.status_code == 201
    assert failed.json()["invoice"]["amount_paid"] == "0.00"

    ledger = client.get("/api/v1/ledger")
    assert ledger.status_code == 200
    entry_types = [entry["entry_type"] for entry in ledger.json()]
    assert "invoice_created" in entry_types
    assert "payment_failure" in entry_types
    assert all(entry["reference_id"] for entry in ledger.json())
