# NAME: Blake Lemarr
# DATE: 04.14.26
# DESCRIPTION: Configs and fixtures for pytest test suites

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
        service: StorageService = StorageService(f'{tmp_path}/{directory}', filename, True)
        return service
    return _storage