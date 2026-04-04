# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages account access and data maintenance.

# ===== IMPORTS =====

import json
from ..models import AccountInternal, AccountPublic, AccountStatus
from ..services import StorageService


# ===== SERVICES =====

class AccountService:
    def __init__(self, storage: StorageService):
        self.service = storage
        self.file_path = self.service.construct_path()
        self.valid_path = self.service.create_if_missing()
        self.__load = self.service.read_file
        self.__save = self.service.save_file

    def __fetch_accounts(self) -> list[AccountInternal]:
        data = self.service.read_file(self.file_path)
        accounts: list[AccountInternal] = [AccountInternal.model_validate(account) for account in data]

        return accounts

    def create(self, new_user: AccountInternal) -> list | bool | None:
        '''
        Creates a new account and adds it to the accounts JSON file.

        :param new_user:
        :return:
        '''

        if self.valid_path:
            # load data
            accounts: list[AccountInternal] = self.__fetch_accounts()

            # make user the admin if they are the first account
            if len(accounts) == 0:
                new_user.status = AccountStatus.ADMIN

            # add user to data
            # accounts.append(new_user.model_dump(mode='json'))
            accounts.append(new_user)

            # write data
            self.__save(self.file_path, accounts)

            return True
        else:
            return None

    def query_user(self, field: str, search: str) -> AccountInternal | None:
        '''
        Find an account based on provided query

        :param field:
        :param search:
        :return:
        '''

        # check for valid path
        if not self.valid_path:
            return None

        # fetch accounts
        accounts: list[AccountInternal] = self.__fetch_accounts()

        if len(accounts) == 0:
            return None

        # loop accounts to find user
        for account in accounts:
            if search.lower() == getattr(account, field).lower():
                return account

        return None # no user found

    def query_users(self, field: str, search: str, limit: int | None = None) -> list[AccountInternal] | None:
        '''
        Finds a list of accounts based on query

        :param field:
        :param search:
        :param limit:
        :return:
        '''

        if not self.valid_path:
            return None

        accounts: list[AccountInternal] = self.__fetch_accounts()

        if len(accounts) == 0:
            return None

        users: list[AccountInternal] = []

        for account in accounts:
            if search.lower() == getattr(account, field).lower():
                users.append(account)

                if limit is not None and len(users) >= limit:
                    break

        return users

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

            data.remove(user_account.model_dump(mode='json')) # remove user from data

            # save data
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)