# NAME: Blake Lemarr
# DATE: 04.16.26
# DESCRIPTION: Houses the list of dynamic MagicMock factories for pytest fixtures

# ========== IMPORTS ========== #
import json
import math
import secrets
import subprocess
import hashlib
import base64

from app.controllers import *
from app.models import *
from app.repositories import *
from app.utils import *
from datetime import datetime
from faker import Faker
from pathlib import Path
from pydantic import TypeAdapter
from unittest.mock import MagicMock
from uuid import uuid4

# ========== INIT ========== #
fake = Faker()

# =================================================================================== #
# ===================================== STORAGE ===================================== #
# =================================================================================== #

class MockStorageFactory:
    def __init__(self, mock_directory: str, mock_filename: str):
        self.mock = MagicMock(spec=StorageService, autospec=True)
        self.mock.filename = mock_filename

        self.mock_path = MagicMock(spec=Path, autospec=True)
        self.mock.file_path = self.mock_path(f'C:/{mock_directory}/{mock_filename}')
        self.mock.file_path.exists.return_value = True

        self.mock.load_data.return_value = []
        self.mock.delete_storage.return_value = True

        self.security = MockSecurityFactory()
        self.mock_accounts = MockAccountFactory()

    def load_single_account(self):
        '''Generates a single account with random data.'''

        account = self.mock_accounts.create_account()
        self.mock.load_data.return_value.append(account)

    def load_multi_mixed_accounts(self, total_accounts: int = 10):
        '''Generates a diverse list of accounts to return at varying permission levels. Minimum of 10'''

        if total_accounts < 10:
            raise ValueError('Must be a minimum of 10 accounts')

        number_of_admins: int = math.floor(total_accounts / 5)
        number_of_on_hold: int = math.floor(total_accounts / 10)
        number_of_banned: int = math.floor(total_accounts / 10)
        number_of_users: int = total_accounts - number_of_admins - number_of_on_hold - number_of_banned

        for _ in range(number_of_admins):
            admin = self.mock_accounts.create_account(status=AccountStatus.ADMIN)
            self.mock.load_data.return_value.append(admin)

        for _ in range(number_of_on_hold):
            on_hold = self.mock_accounts.create_account(status=AccountStatus.ON_HOLD)
            self.mock.load_data.return_value.append(on_hold)

        for _ in range(number_of_banned):
            banned = self.mock_accounts.create_account(status=AccountStatus.BANNED)
            self.mock.load_data.return_value.append(banned)

        for _ in range(number_of_users):
            user = self.mock_accounts.create_account()
            self.mock.load_data.return_value.append(user)

    def save_accounts(self, accounts: list):
        for account in accounts:
            self.mock.load_data.return_value.append(account)

    def load_data(self):
        return self.mock.load_data

    def query_seeded_data(self, key, value):
        data = self.mock.load_data()
        results = []

        for item in data:
            if isinstance(item, dict):
                # adapter = TypeAdapter(AccountInternal)
                # acc = adapter.validate_python(item)
                acc = AccountInternal.model_validate(item, strict=False)
            else:
                acc = item

            if getattr(acc, key.lower()) == value.lower():
                results.append(acc)

        return results

    def delete_storage_failed(self):
        self.mock.delete_storage.return_value = False

    def path_construction_failed(self):
        self.mock.file_path.exists.return_value = False

    def enable_auto_sync(self):
        def sync_save(data):
            self.mock.load_data.return_value = data
            return True
        self.mock.save_data.side_effect = sync_save

    def build(self):
        return self.mock

# ==================================================================================== #
# ===================================== ACCOUNTS ===================================== #
# ==================================================================================== #

class MockAccountFactory:
    def __init__(self):
        self.mock = MagicMock(spec=AccountRepository, autospec=True)
        self.security = MockSecurityFactory()


    def create_account(self, username: str | None = None, password: str | None = None, status: AccountStatus | None = None):
        user_id = str(fake.uuid4())
        username = username if username else fake.user_name()
        pii_email = fake.email(True, 'passvault.com')
        status = status if status else AccountStatus.ADMIN

        # HASHED PASSWORD #
        hashed_password = self.security.hashed_password(password if password else fake.password(), False)

        return AccountInternal(
            id=user_id,
            username=username,
            pii_email=pii_email,
            status=status,
            hashed_password=hashed_password
        )
    
    def create_sign_up(self, username: str | None = None, password: str | None = None):
        return CreateAccount(
            username=username if username else fake.user_name(),
            email=fake.email(True, 'passvault.com'),
            password=password if password else fake.password()
        )

# ==================================================================================== #
# ===================================== SECURITY ===================================== #
# ==================================================================================== #

class MockSecurityFactory:
    def __init__(self):
        pass

    def generate_pepper(self):
        return secrets.token_hex(32)

    def generate_salt(self):
        return secrets.token_bytes(16)

    def debugging_salt_pepper(self):
        return {
            "salt": b'Z]O\xb3\xd9\xcf\xce\xb1\x19:u#\x8e\x87\xc9\x83',
            "pepper": 'bb74a3bc759a30c74db45ff1849902ae99fcdfe0d2a8eb3866214f37044c3998'
        }

    def hashed_password(self, raw_password: str, debug_mode: bool = False):
        if debug_mode:
            debug = self.debugging_salt_pepper()
            pepper = debug['pepper']
            salt = debug['salt']
        else:
            salt = self.generate_salt()
            pepper = self.generate_pepper()

        combined_pass_pepper: str = raw_password + pepper
        encoded_combination_pass: bytes = combined_pass_pepper.encode('utf-8')

        hashed_password_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            encoded_combination_pass,
            salt,
            600000
        )

        return AccountPassword(
            salt=base64.b64encode(salt).decode('utf-8'),
            hash=base64.b64encode(hashed_password_bytes).decode('utf-8'),
        )

# ================================================================================= #
# ===================================== VAULT ===================================== #
# ================================================================================= #

