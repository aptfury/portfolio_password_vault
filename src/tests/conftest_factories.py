# NAME: Blake Lemarr
# DATE: 04.16.26
# DESCRIPTION: Houses the list of dynamic MagicMock factories for pytest fixtures

# ========== IMPORTS ========== #
import json
import secrets
import subprocess
import hashlib
import base64

from _pytest.tmpdir import tmp_path
from app.controllers import *
from app.models import *
from app.repositories import *
from app.utils import *
from datetime import datetime
from faker import Faker
from pathlib import Path
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

        self.mock.file_path = MagicMock(spec=Path, autospec=True)
        self.mock.file_path.return_value = Path(f'C:/{mock_directory}/{mock_filename}')
        self.mock.file_path.exists.return_values = True

        self.mock.load_data.return_values = []
        self.mock.delete_storage.return_values = True

        self.security = MockSecurityFactory()
        self.mock_accounts = MockAccountFactory()

    def load_single_account(self):
        '''Generates a single account with random data.'''

        account = self.mock_accounts.create_account()
        self.mock.load_data.return_values.append(account)

    def load_ten_mixed_accounts(self):
        '''Generates a diverse list of accounts to return at varying permission levels.'''

        for _ in range(2):
            admin = self.mock_accounts.create_account(status=AccountStatus.ADMIN)
            self.mock.load_data.return_values.append(admin)

        on_hold = self.mock_accounts.create_account(status=AccountStatus.ON_HOLD)
        self.mock.load_data.return_values.append(on_hold)

        banned = self.mock_accounts.create_account(status=AccountStatus.BANNED)
        self.mock.load_data.return_values.append(banned)

        for _ in range(6):
            user = self.mock_accounts.create_account()
            self.mock.load_data.return_values.append(user)

    def delete_storage_failed(self):
        self.mock.delete_storage.return_values = False

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
        mock_user = MagicMock(spec=AccountInternal, autospec=True)
        mock_user.id = str(fake.uuid4())
        mock_user.username = username if username else fake.user_name()
        mock_user.pii_email = fake.email(True, 'passvault.com')
        mock_user.status = status if status else AccountStatus.ADMIN
        mock_user.created_on = datetime.now()
        mock_user.updated_on = datetime.now()

        # CENSOR EMAIL #
        # todo - transfer to security
        name, domain = mock_user.pii_email.split('@')
        mock_user.email = f'{name[0]}{'*' * (len(name) - 1)}@{domain}'

        # HASHED PASSWORD #
        mock_user.hashed_password = self.security.hashed_password(password if password else fake.password(), False)

        return mock_user

# ==================================================================================== #
# ===================================== SECURITY ===================================== #
# ==================================================================================== #

class MockSecurityFactory:
    def __init__(self):
        pass

    def generate_pepper(self):
        try:
            result = subprocess.run(
                ['openssl', 'rand', '-hex', '32'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return secrets.token_hex(32)

    def generate_salt(self):
        return secrets.token_bytes(16)

    def debugging_salt_pepper(self):
        salt = secrets.token_bytes(16)

        try:
            pepper = subprocess.run(
                ['openssl', 'rand', '-hex', '32'],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "salt": salt,
                "pepper": pepper.stdout.strip()
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "salt": salt,
                "pepper": secrets.token_hex(32)
            }

    def hashed_password(self, raw_password: str, debug_mode: bool = False):
        mock_password = MagicMock(spec=AccountPassword, autospec=True)

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

        mock_password.iterations = 600000
        mock_password.algorithm = 'PBKDF2-SHA256'
        mock_password.salt = base64.b64encode(salt).decode('utf-8')
        mock_password.hash = base64.b64encode(hashed_password_bytes).decode('utf-8')

        return mock_password

# ================================================================================= #
# ===================================== VAULT ===================================== #
# ================================================================================= #

