# Name: Blake Lemarr
# Updated: 04.13.2026
# Description: Manages interactions between user and account operations

# ===== IMPORTS =====
import getpass
from input_with_timeout import input_with_timeout
from ..models import CreateAccount, AccountPublic, AccountInternal, AccountLogIn
from ..utils import AccountUtil, AuthUtil
from ..repositories import StorageService

# ===== INIT =====
account_storage: StorageService = StorageService('data', 'accounts.json')

# ===== CONTROLLER =====
class AccountsController:
    def __init__(self):
        self.account_utils = AccountUtil(storage=account_storage)
        self.auth_utils = AuthUtil(storage=account_storage)

    def log_in(self) -> bool | AccountInternal:
        print('''Welcome back! Please log into your account.
        To return to the main menu, enter EXIT instead of a username.''')

        # collect username
        username: str = input_with_timeout('Enter your username: ', timeout=10)

        # check for exit command
        if username.lower() == 'exit':
            return False

        # collect raw password
        raw_password: str = getpass.getpass(input_with_timeout('Enter your password: ', timeout=10))

        # create account data
        data: AccountLogIn = AccountLogIn(username=username, password=raw_password)

        # check user authorization
        user_id: str = self.auth_utils.authorize_log_in(data)

        # ensure user id is present
        if user_id is None:
            return False

        # get user information
        user: AccountInternal | None = self.account_utils.internal_fetch_user(user_id)

        # check that a user was found
        if user is None:
            return False

        print(f'\nWelcome back, {user.username}!\n')

        return user

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