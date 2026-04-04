# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages account access and data maintenance.

# ===== IMPORTS =====
import json
from ..models import AccountInternal, AccountPublic, AccountStatus, CreateAccount
from ..services import FileManagementService
# ===================

class AccountsService:
    def __init__(self):
        self.service = FileManagementService('vault', 'accounts')
        self.file_path = self.service.construct_path()
        self.valid_path = self.service.create_if_missing()

    def create_new_account(self, new_user: AccountInternal) -> bool | None:
        '''
        Creates a new account and adds it to the database.

        :param new_user:
        :return:
        '''

        if self.valid_path:
            # load data
            with open(self.file_path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = [] # catch no data

            if len(data) == 0:
                new_user.status = AccountStatus.ADMIN

            # add user to data
            data.append(new_user.model_dump())

            # write data
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)

            return True
        else:
            return None

    def update_account(self, status: AccountStatus, username: str, update: CreateAccount | AccountInternal) -> bool | None:
        '''
        Allows updating of user accounts. Admins can update various accounts, while users can
        only update their own accounts.

        :param status:
        :param username:
        :param update:
        :return:
        '''

        if status == AccountStatus.BANNED or status == AccountStatus.ON_HOLD:
            print('----- PERMISSION DENIED -----\n'
                  f'You cannot change your account because it is {status}.\n'
                  'If you believe this was an error, please reach out to the administrator.')
            return False # todo - add an access denied response that tells the application to exit

        if self.valid_path:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            if len(data) == 0:
                return None

            user: AccountInternal | None = None
            accounts: dict = {acc.username.lower(): acc for acc in data}

            if username.lower() in accounts:
                user = AccountInternal.model_validate(accounts[username.lower()])
            else:
                return None

            if status == AccountStatus.ADMIN:
                user = update

            elif status == AccountStatus.USER:
                if username != user.username:
                    return False # Users can only edit their own accounts.

                if update.email:
                    user.pii_email = update.email

                if update.username:
                    user.username = update.username

            else:
                return False

            with open(self.file_path, 'w') as file:
                updates: list = [acc.model_dump() for acc in accounts.values()]
                json.dump(updates, file, indent=4)

            return True
        else:
            print('----- INVALID PATH -----')
            return False # todo - create invalid path error

    def find_account_by_username(self, username: str, status: AccountStatus) -> AccountPublic | AccountInternal | None:
        '''
        Finds an account by its username and returns an internal view for admins
        and a public view for users.

        :param username:
        :param status:
        :return:
        '''

        # ensure accounts with restricted access permissions are automatically denied
        if status == AccountStatus.BANNED or status == AccountStatus.ON_HOLD:
            return None # todo - Create access rejection error msg

        if self.valid_path:
            # load data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            if len(data) == 0:
                return None

            user_account: AccountPublic | AccountInternal | None = None
            user_accounts: list[AccountPublic | AccountInternal] = []

            # todo - test user_account.append() implementation
            if status == AccountStatus.ADMIN:
                user_accounts.append(*[AccountInternal.model_validate(user) for user in data])
            else:
                # if user is not admin, return public view of account
                # utility logic should be created to ensure that users can only
                # query their own accounts.
                user_accounts.append(*[AccountPublic.model_validate(user) for user in data])

            for acc in user_accounts:
                if username.lower() == acc.username.lower():
                    user_account = acc
                    break

            return user_account
        else:
            return None

    def internal_find_all_users(self, status: AccountStatus) -> list[AccountInternal] | None:
        '''
        Returns a list of all registered users.

        :param status:
        :return:
        '''

        if status != AccountStatus.ADMIN:
            return None # todo - replace with access error

        if self.valid_path:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            if len(data) == 0:
                return None

            return [AccountInternal.model_validate(account) for account in data]
        else:
            return None # todo - replace with path error

    # todo - expand based on email and id
    def remove_account_by_username(self, username: str) -> None:
        '''
        Removes an account by its username.

        :param username:
        :return:
        '''

        if self.valid_path:
            # load data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            user_account: AccountInternal | None = None
            accounts: list[AccountInternal] = [AccountInternal.model_validate(account) for account in data]

            for acc in accounts:
                if acc.username.lower() == username.lower():
                    user_account = acc

            data.remove(user_account.model_dump()) # remove user from data

            # save data
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)