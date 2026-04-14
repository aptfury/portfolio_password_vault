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
    test_dir = tmp_path / 'db' / 'test.json'

    service = StorageService('db', 'test.json')
    service.file_path = test_dir

    return service