from app.repositories.plan_repository import PlanRepository
from app.services.exceptions import AppException


class PlanService:
    def __init__(self, plan_repo: PlanRepository):
        self.plan_repo = plan_repo

    def create_plan(self, data):
        if self.plan_repo.get_by_code(data.code):
            raise AppException(409, "Plan code already exists")
        if data.price <= 0:
            raise AppException(400, "Plan price must be greater than 0")
        return self.plan_repo.create(**data.model_dump())

    def list_plans(self):
        return self.plan_repo.list()
