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

    def create(self, new_user: AccountInternal) -> bool | None:
        '''
        Creates a new account and adds it to the accounts JSON file.

        :param new_user:
        :return:
        '''

        if not self.valid_path:
            return None

        # load data
        accounts: list[AccountInternal] = self.__fetch_accounts()

        # make user the admin if they are the first account
        if len(accounts) == 0:
            new_user.status = AccountStatus.ADMIN

        for user in accounts:
            if new_user.username == user.username:
                print('Username taken, please register again to pick a new one.')
                return False

        # add user to data
        # accounts.append(new_user.model_dump(mode='json'))
        accounts.append(new_user)

        # write data
        self.__save(self.file_path, accounts)

        return True

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

    def query_users(self, field: str, search: str) -> list[AccountInternal] | None:
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

        return users

    def get_user_id(self, field: str, search: str) -> str | None:
        if not self.valid_path:
            return None

        user: AccountInternal = self.query_user(field, search)

        return user.id

    def update(self, field: str, search: str, update: AccountInternal) -> bool:
        '''
        Updates an account using a query.

        :param field:
        :param search:
        :param update:
        :return:
        '''

        if not self.valid_path:
            return False

        accounts: list[AccountInternal] = self.__fetch_accounts()

        if len(accounts) == 0:
            return False

        for i, account in enumerate(accounts):
            if search.lower() == getattr(account, field).lower():
                accounts[i] = update
                break

        self.__save(self.file_path, accounts)

        return True

    def get_all(self) -> list[AccountInternal] | None:
        if not self.valid_path:
            return None

        return self.__fetch_accounts()


    def remove(self, account: AccountInternal) -> bool | None:
        '''
        Removes an account by a query.

        :param account:
        :return:
        '''

        if not self.valid_path:
            return None

        accounts: list[AccountInternal] = self.__fetch_accounts()

        accounts.remove(account)

        self.__save(self.file_path, accounts)

        return True