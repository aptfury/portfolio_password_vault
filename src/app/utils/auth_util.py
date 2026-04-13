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
    AccountInternal,
    AccountPassword
)

# ===== UTILITIES =====

load_dotenv()

class AuthUtilities:
    def __init__(self):
        self.account_pepper = os.getenv("ACCOUNT_PEPPER")
        self.vault_pepper = os.getenv("VAULT_PEPPER")

    def new_account_password(self, raw_password: str) -> AccountPassword:
        '''
        Creates a secure password hash for the user.

        :param raw_password:
        :return:
        '''

        # todo - update docs to gen pepper w/ python -c "import secrets; print(secrets.token_urlsafe(32))"
        # todo - walkthrough adding to environmental variables

        if not self.account_pepper: # check for valid pepper
            raise ValueError('ACCOUNT_PEPPER not set in environment')

        salt_bytes: bytes = secrets.token_bytes(32) # create password salt in bytes

        combination: str = raw_password + self.account_pepper # combine raw_password and pepper
        password_bytes: bytes = combination.encode('utf-8') # encode combination

        # hash password and turn into string.
        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )
        hashed_password: str = base64.b64encode(hash_bytes).decode('utf-8')

        account_password: AccountPassword = AccountPassword(
            salt=base64.b64encode(salt_bytes).decode('utf-8'),
            hash=hashed_password
        )

        return account_password

    def validate_account_password(self, raw_password: str, account: AccountInternal) -> bool:
        '''
        Validates that the user's account password is correct.

        :param raw_password:
        :param account:
        :return:
        '''

        if not self.account_pepper: # check for pepper
            raise ValueError('ACCOUNT_PEPPER not set in environment')

        account_password: AccountPassword = account.hashed_password # get stored hash

        # hash submitted password using pepper and stored salt
        combination: str = raw_password + self.account_pepper
        password_bytes: bytes = combination.encode('utf-8')
        salt_bytes: bytes = account_password.salt.encode('utf-8')
        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )
        hashed_password: str = base64.b64encode(hash_bytes).decode('utf-8')

        return hashed_password == account_password.hash