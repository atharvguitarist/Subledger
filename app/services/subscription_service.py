from app.repositories.customer_repository import CustomerRepository
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.exceptions import AppException


class SubscriptionService:
    def __init__(self, subscription_repo: SubscriptionRepository, customer_repo: CustomerRepository, plan_repo: PlanRepository):
        self.subscription_repo = subscription_repo
        self.customer_repo = customer_repo
        self.plan_repo = plan_repo

    def create_subscription(self, data):
        customer = self.customer_repo.get(data.customer_id)
        if not customer:
            raise AppException(404, "Customer not found")
        plan = self.plan_repo.get(data.plan_id)
        if not plan:
            raise AppException(404, "Plan not found")
        if not plan.is_active:
            raise AppException(400, "A subscription cannot be created for an inactive plan")
        existing = self.subscription_repo.find_active_by_customer_and_plan(data.customer_id, data.plan_id)
        if existing and data.status == "active":
            raise AppException(409, "Customer already has an active subscription to this plan")
        return self.subscription_repo.create(**data.model_dump())

    def list_subscriptions(self):
        return self.subscription_repo.list()
