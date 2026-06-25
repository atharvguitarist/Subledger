# SubLedger Low-Level Design

## ERD
- **Customer** 1..* **Subscription**
- **Plan** 1..* **Subscription**
- **Subscription** 1..* **Invoice**
- **Invoice** 1..* **PaymentAttempt**
- **Customer** 1..* **LedgerEntry**
- **Invoice** 1..* **LedgerEntry**

## Entity summary
### Plan
Fields: id, name, code, price, currency, interval, is_active, created_at.

### Customer
Fields: id, name, email, created_at.

### Subscription
Fields: id, customer_id, plan_id, status, start_date, end_date, created_at.

### Invoice
Fields: id, subscription_id, customer_id, amount_due, amount_paid, currency, status, period_start, period_end, due_date, created_at.

### PaymentAttempt
Fields: id, invoice_id, amount, currency, status, provider_reference, failure_reason, created_at.

### LedgerEntry
Fields: id, customer_id, invoice_id, entry_type, amount, currency, reference_id, description, created_at.

## Service responsibilities
| Service | Responsibilities |
|---|---|
| PlanService | Validate price and uniqueness of code, create and list plans. |
| CustomerService | Enforce unique email, create and list customers. |
| SubscriptionService | Validate customer/plan existence, block inactive plans, prevent duplicate active subscriptions. |
| InvoiceService | Validate active subscription, compute billing period, snapshot plan price into invoice, create invoice ledger event. |
| PaymentService | Validate invoice, currency, and remaining amount; create payment attempt; update invoice only on success; create payment ledger event. |
| LedgerService | Central append-only creator for ledger records. |

## Repository responsibilities
| Repository | Responsibilities |
|---|---|
| PlanRepository | Plan persistence and lookup by id/code. |
| CustomerRepository | Customer persistence and lookup by id/email. |
| SubscriptionRepository | Subscription persistence and active-subscription lookup. |
| InvoiceRepository | Invoice persistence, lookup, listing, and amount/status updates. |
| PaymentAttemptRepository | Payment attempt persistence. |
| LedgerRepository | Append-only ledger persistence and listing. |

## Business rule ownership
| Rule | Owner |
|---|---|
| Plan price must be greater than 0 | Pydantic schema + PlanService |
| Customer email must be unique | CustomerService |
| Subscription cannot be created for inactive plan | SubscriptionService |
| Customer cannot have two active subscriptions to same plan | SubscriptionService |
| Invoice amount_due comes from current plan price | InvoiceService |
| Successful payment cannot exceed remaining invoice amount | PaymentService |
| Full payment -> paid, partial payment -> partially_paid | PaymentService |
| Failed payment does not increase amount_paid | PaymentService |
| Ledger entries are append-only with reference_id | LedgerService + LedgerRepository |

## Design pattern explanation
The backend follows a layered architecture:
- **Routes** handle HTTP concerns.
- **Services** own business rules and orchestration.
- **Repositories** isolate persistence.
- **Models** define DB structure and relationships.
- **Schemas** validate request/response payloads.
- **DB layer** manages engine/session creation and dependency injection.

This makes the code easier to test, extend, and swap to another database.

## Invoice generation flow
1. Route receives `subscription_id` and optional billing period start.
2. `InvoiceService` fetches subscription through `SubscriptionRepository`.
3. Service validates that the subscription exists and is active.
4. Service reads plan interval and price from the subscription relationship.
5. Service computes billing period and due date.
6. `InvoiceRepository` creates invoice in `issued` status.
7. `LedgerService` adds `invoice_created` entry.
8. Route commits and returns invoice response.

## Payment recording flow
1. Route receives `invoice_id`, amount, currency, status, provider reference, and optional failure reason.
2. `PaymentService` fetches invoice through `InvoiceRepository`.
3. Service validates invoice existence, currency match, and remaining unpaid amount.
4. `PaymentAttemptRepository` creates the payment attempt.
5. If payment failed, invoice totals stay unchanged.
6. If payment succeeded, invoice `amount_paid` and `status` are updated.
7. `LedgerService` creates `payment_success` or `payment_failure` entry.
8. Route commits and returns payment attempt with updated invoice snapshot.
