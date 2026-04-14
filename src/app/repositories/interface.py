# NAME: Blake Lemarr
# DATE: 04.14.26
# DESCRIPTION: A generic for the repositories
# NOTE: Still getting used to these changes, so implementation may need review.

# ========== IMPORTS ========== #
from abc import ABC, abstractmethod
from typing import Optional

# ========== INTERFACE ========== #
class IRepository[T](ABC):
    @abstractmethod
    def create(self, data: T, req_id: str) -> bool:
        ...

    @abstractmethod
    def read(self, field: str, value: str, req_id: str) -> Optional[list[T]]:
        ...

    @abstractmethod
    def get_all(self, req_id: str) -> list[T]:
        ...

    @abstractmethod
    def update(self, target_id: str, update_data: T, req_id: str) -> bool:
        ...

    @abstractmethod
    def delete(self, target_id: str, reason: str, req_id: str) -> bool:
        ...