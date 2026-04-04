'''
Name: Blake Lemarr
Updated: 04.04.2026
Description: Fixtures and other configurations for unit and integration tests.
'''

# ===== IMPORTS =====

import base64
import hashlib
import pytest
import secrets
import subprocess
from app.models import *
from app.services import *
from app.utils import *
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

# ============================

# ===== SERVICE FIXTURES =====

@pytest.fixture
def account_service(storage):
    return AccountService(storage=storage)

@pytest.fixture
def account_util(account_service):
    utils = AccountUtil()
    utils.service = account_service

# ============================

# ===== MODEL FIXTURES =====

# ==========================

# ===== FACTORIES =====

@pytest.fixture
def service_account_factory():
    '''Generates fake accounts compatible with service use cases'''
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

@pytest.fixture
def util_account_factory():
    '''Generates fake accounts more compatible with util use cases.'''
    fake = Faker()

    def _new_user(username: str | None = None, password: str | None = None):
        return CreateAccount(
            username=username or fake.user_name(),
            email=fake.ascii_free_email(),
            password=password or fake.password()
        )

    return _new_user

@pytest.fixture
def hashed_password_factory(pepper_factory, salt_factory):
    '''Creates a cryptographically sound password hash'''
    fake = Faker()

    def _hashed_password(password: str | None = None):
        raw_password: str = password if password is not None else fake.password()
        pepper = pepper_factory()
        salt_bytes = salt_factory()

        peppered = raw_password + pepper
        password_bytes = peppered.encode('utf-8')

        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )

        hashed_password: str = base64.b64encode(hash_bytes).decode('utf-8')
        salt: str = base64.b64encode(salt_bytes).decode('utf-8')

        return AccountPassword(
            hash=hashed_password,
            salt=salt,
            iterations=600000,
            algorithm='PBKDF2-SHA256'
        )

    return _hashed_password

@pytest.fixture
def pepper_factory():
    '''Generates authentic peppers for the testing suite'''
    def _generate_pepper():
        try:
            result = subprocess.run(
                ['openssl', 'rand', '-hex', '32'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            # be sure to keep this in case openssl isn't installed
            import secrets
            return secrets.token_hex(32)

    return _generate_pepper

@pytest.fixture
def salt_factory():
    '''Generates salts for password, and is different from utility salts
    which are less secure and only for debugging'''
    def _generate_salt():
        return secrets.token_bytes(16)

    return _generate_salt

@pytest.fixture
def debugging_salt_factory():
    '''This is specifically for debugging purposes only and is NOT
    a secure option to use. DO NOT implement this anywhere as an actual salt.'''
    def _debugging_salt(seed: str):
        return hashlib.sha256(seed.encode()).hexdigest()[:32]

    return _debugging_salt

# =====================