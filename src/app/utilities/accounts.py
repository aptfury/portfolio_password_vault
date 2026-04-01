# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages logic for account handling.

# ===== IMPORTS =====
import os
import base64
import hashlib
import secrets
from . import AuthUtilities
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
        self.auth = AuthUtilities()
        self.pepper = os.getenv("ACCOUNT_PEPPER")

    def create_new_account(self, data: CreateAccount) -> bool:
        '''
        Creates a new account for the user.

        :param data:
        :return:
        '''

        # hash user password
        hashed_password: AccountPassword = self.auth.new_account_password(data.password)

        # create account model
        new_account: AccountInternal = AccountInternal(
            username=data.username,
            pii_email=data.email,
            hashed_password=hashed_password
        )

        # create new account
        return self.service.create_new_account(new_account)