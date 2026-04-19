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

from .conftest_factories import *

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

@pytest.fixture
def mock_storage():
    def _mock_storage(directory: str, filename: str):
        return MockStorageFactory(directory, filename)
    return _mock_storage

# ========== ACCOUNTS ========== #
@pytest.fixture
def mock_accounts():
    def _mock_accounts():
        return MockAccountFactory()
    return _mock_accounts

# ========== SECURITY ========== #
@pytest.fixture
def mock_security():
    def _mock_security():
        return MockSecurityFactory()
    return _mock_security