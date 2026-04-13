# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages interactions between user and account operations

# ===== IMPORTS =====

import getpass
from input_with_timeout import input_with_timeout
from ..models import CreateAccount, AccountPublic, AccountInternal
from ..utils import AccountUtil
from ..services import StorageService

# ===== CONTROLLER =====

account_storage: StorageService = StorageService('data', 'accounts.json')

class AccountsController:
    def __init__(self):
        self.account_utils = AccountUtil(storage=account_storage)

    # todo - make nav to parse data and call methods

    def log_in(self):
        pass

    def register_new_account(self):
        username: str = input_with_timeout('Enter a username: ', timeout=10)
        password: str = getpass.getpass(input_with_timeout('Enter a password: ', timeout=10))
        add_email: str = input_with_timeout('Would you like to enter an email [y/n]? ', timeout=10)
        email: str = ''

        if add_email == 'y':
            email = input_with_timeout('Enter an email: ', timeout=10)

        new_account: CreateAccount = CreateAccount(
            username=username,
            email=email,
            password=password
        )

        return self.account_utils.create(new_account)