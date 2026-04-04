'''
Name: Blake Lemarr
Updated: 04.04.2026
Description: Fixtures and other configurations for unit and integration tests.
'''

# ===== IMPORTS =====

import pytest
from app.models import *
from app.services import *
from app.utilities import *
from app.controllers import *
from faker import Faker

# ===================

# ===== STORAGE FIXTURES =====

@pytest.fixture
def storage(tmp_path):
    # create testing path
    test_dir = tmp_path / 'database'
    test_file = 'test.json'

    # init storage service
    service = StorageService(test_dir, test_file)

    # create the directory and json file
    service.create_if_missing()

    return service # return storage service instance

@pytest.fixture
def mock_storage(tmp_path):
    # directory
    mock_path = tmp_path / 'mock_storage.json'

    # create mock storage environment
    mock = MagicMock(spec=StorageService)
    mock_path.write_text('[]')

    # defaults
    mock.read_file.return_value = []
    mock.construct_path.return_value = mock_path
    mock.create_if_missing.return_value = True
    mock.full_path = mock_path

    return mock

# ============================

# ===== SERVICE FIXTURES =====

@pytest.fixture
def account_service(storage):
    return AccountService(storage=storage)

# ============================

# ===== MODEL FIXTURES =====

# @pytest.fixture
# def account_models():
#     create = CreateAccount(
#         username='test',
#         password='belligerent',
#         email='penelope@outmail.com',
#     )
#     password = AccountPassword(
#         hash='hashed_shit',
#         salt='salty-bitch',
#         iterations=600000,
#         algorithm='sha512',
#     )
#     internal = AccountInternal(
#         username='pickles and cheese',
#         pii_email='pickes@outmail.com',
#         hashed_password=password,
#     )
#     public = AccountPublic
#     status = AccountStatus
#
#     return internal

# ==========================

# ===== FACTORIES =====

@pytest.fixture
def account_factory():
    fake = Faker()

    def _create_user(username: str | None = None, password: str | None = None):
        user = username or fake.user_name()
        raw_password = password or fake.password()

        password_model = AccountPassword(
            salt=fake.sha256(),
            hash=fake.sha256(),
            iterations=600000,
            algorithm='sha256'
        )

        return AccountInternal(
            username=user,
            pii_email=fake.ascii_free_email(),
            hashed_password=password_model
        )

    return _create_user


# =====================