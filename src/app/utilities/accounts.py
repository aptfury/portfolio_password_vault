# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages logic for account handling.

# ===== IMPORTS =====
import os
import base64
import hashlib
import secrets
from dotenv import load_dotenv
from ..models import (
    AccountPublic,
    AccountInternal,
    CreateAccount,
    AccountPassword
)
from ..services import AccountsService

# ===== UTILITIES =====

load_dotenv()

class AccountsUtilities:
    def __init__(self):
        self.service = AccountsService()
        self.pepper = os.getenv("ACCOUNT_PEPPER")

    def create_new_account(self, data: CreateAccount):
        # todo - turn salt into its own function
        # todo - move password creation to authorization.py
        random_bytes: bytes = secrets.token_bytes(32)
        salt: str = base64.b64encode(random_bytes).decode('utf-8')

        # todo - update docs to gen pepper w/ python -c "import secrets; print(secrets.token_urlsafe(32))"
        # todo - walkthrough adding to environmental variables

        if not self.pepper:
            raise ValueError('ACCOUNT_PEPPER not set in environment')

        peppered_password: str = data.password + self.pepper
        password_bytes: bytes = peppered_password.encode('utf-8')
        salt_bytes: bytes = salt.encode('utf-8')

        hashed_password_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )
        hashed_password: str = base64.b64encode(hashed_password_bytes).decode('utf-8')

        account_password: AccountPassword = AccountPassword(
            salt=salt,
            hash=hashed_password
        )

        new_account: AccountInternal = AccountInternal(
            username=data.username,
            pii_email=data.email,
            hashed_password=account_password
        )

        public_account: AccountPublic = AccountPublic(
            username=new_account.username,
            pii_email = new_account.email,
            created_on = new_account.created_on
        )

        return public_account