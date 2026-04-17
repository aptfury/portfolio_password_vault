# # NAME: Blake Lemarr
# # DATE: 04.16.26
# # DESCRIPTION: Configs and fixtures for pytest test suites

# ========== IMPORTS ========== #
import pytest
from faker import Faker

from app.models import *
from app.repositories import *
from app.utils import *
from app.controllers import *

# ========== STORAGE ========== #
@pytest.fixture
def storage(tmp_path):
    def _storage(directory: str, filename: str) -> StorageService:
        test_dir = tmp_path / directory
        test_path = test_dir / filename

        service: StorageService = StorageService(directory, filename)
        service.file_path = test_path
        return service
    return _storage