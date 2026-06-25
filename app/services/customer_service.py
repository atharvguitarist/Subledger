from app.repositories.customer_repository import CustomerRepository
from app.services.exceptions import AppException


class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def create_customer(self, data):
        if self.customer_repo.get_by_email(data.email):
            raise AppException(409, "Customer email must be unique")
        return self.customer_repo.create(**data.model_dump())

    def list_customers(self):
        return self.customer_repo.list()
