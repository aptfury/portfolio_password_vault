# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages account access and data maintenance.

# ========== IMPORTS ========== #

from datetime import datetime
from ..models import AccountInternal, AccountPublic, AccountStatus
from .storage_service import StorageService
from .interface import IRepository
from typing import Optional, Any

# ========== REPO ========== #

class AccountRepository(IRepository[AccountInternal]):
    def __init__(self, storage: StorageService):
        self.storage = storage

    def _save(self, data: list[AccountInternal]) -> None:
        raw_data = [d.model_dump(mode='json') for d in data]
        self.storage.save_data(raw_data)
        return

    def get_all(self, req_id: str = 'INTERNAL') -> list[AccountInternal]:
        raw_data = self.storage.load_data()
        return [AccountInternal.model_validate(data) for data in raw_data]

    def create(self, data: AccountInternal, req_id: str = 'INTERNAL') -> bool:
        accounts = self.get_all(req_id)
        accounts.append(data)

        self._save(accounts)

        return True

    def read(self, field: str, value: str, req_id: str = 'INTERNAL') -> Optional[list[AccountInternal]]:
        accounts = self.get_all(req_id)
        res: list[AccountInternal] = []

        for acc in accounts:
            if getattr(acc, field).lower() == value.lower():
                res.append(acc)

        return res

    def update(self, target_id: str, update_data: AccountInternal, req_id: str = 'INTERNAL') -> bool:
        accounts = self.get_all(req_id)

        for i, acc in enumerate(accounts):
            if acc.id == target_id:
                update_data.updated_on = str(datetime.now())
                accounts[i] = update_data
                self._save(accounts)
                return True

        return False

    def delete(self, target_id: str, reason: str, req_id: str = 'INTERNAL') -> bool:
        accounts = self.get_all(req_id)
        target_account = None

        # todo - add security log that updates w/ reason

        for acc in accounts:
            if acc.id == target_id:
                target_account = acc

        accounts.remove(target_account)

        self._save(accounts)
        return True