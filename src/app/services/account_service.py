# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages account access and data maintenance.

# ===== IMPORTS =====

import json
from ..models import AccountInternal, AccountPublic
from ..services import StorageService


# ===== SERVICES =====

class AccountService:
    def __init__(self, storage: StorageService):
        self.service = storage
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

            # add user to data
            data.append(new_user.model_dump())

            # write data
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)

            return True
        else:
            return None

    def find_account_by_username(self, username: str) -> AccountPublic | None:
        '''
        Finds a account by its username.

        :param username:
        :return:
        '''

        if self.valid_path:
            # load data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            if len(data) == 0:
                return None

            # find user
            user_account: AccountPublic | None = None
            accounts: list[AccountPublic] = [AccountPublic.model_validate(account) for account in data]

            for account in accounts:
                if account.username.lower() == username.lower():
                    user_account = account
                    break

            return user_account
        else:
            return None

    def internal_find_all_users(self) -> list[AccountInternal] | None:
        '''
        Returns a list of all registered users.

        :return:
        '''

        if self.valid_path:
            # load data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            if len(data) == 0:
                return None

            return [AccountInternal.model_validate(account) for account in data]
        else:
            return None

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

            for account in accounts:
                if account.username.lower() == username.lower():
                    user_account = account

            data.remove(user_account.model_dump()) # remove user from data

            # save data
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)