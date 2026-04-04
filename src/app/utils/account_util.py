# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages logic for account handling.

# ===== IMPORTS =====
import os
from .auth_util import AuthUtilities
from enum import Enum
from dotenv import load_dotenv
from ..models import (
    AccountPublic,
    AccountInternal,
    CreateAccount,
    AccountPassword,
    AccountStatus
)
from ..services import AccountService, StorageService

# ===== UTILITIES =====

load_dotenv()
account_storage: StorageService = StorageService('data', 'accounts.json')
class AcceptedFields(str, Enum):
    id = 'id'
    username = 'username',
    pii_email = 'pii_email',
    email = 'pii_email',
    created_on = 'created_on',
    status = 'status'

class AccountUtil:
    def __init__(self):
        self.service = AccountService(storage=account_storage)
        self.auth = AuthUtilities()
        self.pepper = os.getenv("ACCOUNT_PEPPER")
        self.fields = AcceptedFields

    def create(self, data: CreateAccount) -> bool:
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
        return self.service.create(new_account)

