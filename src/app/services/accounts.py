# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages account access and data maintenance.

# ===== IMPORTS =====
from ..models import AccountInternal
from ..models import AccountPublic
from ..models import AccountStatus
from ..services import FileManagementService
# ===================

class AccountServices:
    def __init__(self):
        self.service = FileManagementService('data', 'accounts')
        self.file_path = self.service.construct_path()
        self.valid_path = self.service.create_if_missing()
        self.__load = self.service.read_file
        self.__save = self.service.save_file

    def __fetch_accounts(self) -> list[AccountInternal] | None:
        data = self.__load(self.file_path)
        return [AccountInternal.model_validate(acc) for acc in data]

    def create(self, new_user: AccountInternal) -> bool | None:
        '''
        Creates user account.

        :param new_user:
        :return:
        '''

        if self.valid_path:
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if any(new_user.username.lower() == user.username.lower() for user in accounts):
                print('This username is already in use. Please register again with a different username.')
                return False

            if len(accounts) == 0:
                new_user.status = AccountStatus.ADMIN
                print('As the first user, you have been made the admin of this instance.')

            # add user to data
            accounts.append(new_user)

            # write data
            self.__save(self.file_path, accounts)

            return True
        else:
            return None

    def update(self, field: str, search: str, data: AccountInternal) -> bool | None:
        '''
        Updates user accounts

        :param field:
        :param search:
        :param data:
        :return:
        '''

        if self.valid_path:
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None

            for i, user in enumerate(accounts):
                if getattr(user, field).lower() == search.lower():
                    accounts[i] = data

            self.__save(self.file_path, accounts)

            return True
        else:
            print('----- INVALID PATH -----')
            return False # todo - create invalid path error

    def query_user(self, field: str, search: str, is_public: bool) -> AccountInternal | AccountPublic | None:
        '''
        Returns first user account found based on query

        :param field:
        :param search:
        :param is_public:
        :return:
        '''

        if self.valid_path:
            # load data
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None

            for user in accounts:
                if search.lower() == getattr(user, field).lower():
                    if is_public:
                        return AccountPublic.model_construct(**user.model_dump())
                    else:
                        return user

            return None
        else:
            return None

    def query_users(self, field: str, search: str) -> list[AccountInternal] | None:
        '''
        Returns a list of users based on query

        :param field:
        :param search:
        :return:
        '''

        if self.valid_path:
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None

            users: list[AccountInternal] = []

            for user in accounts:
                if search.lower() == getattr(user, field):
                    users.append(user)

            return users
        else:
            return None

    def list(self) -> list[AccountInternal] | None:
        '''
        Returns all users

        :return:
        '''
        if self.valid_path:
            return self.__fetch_accounts()
        else:
            return None # todo - replace with path error

    # todo - expand based on email and id
    def remove(self, account: AccountInternal) -> bool | None:
        '''
        Removes an account.

        :param account:
        :return:
        '''

        if self.valid_path:
            # load data
            accounts: list[AccountInternal] = self.__fetch_accounts()

            if len(accounts) == 0:
                return None # todo - return an error for no user

            accounts.remove(account)

            # save data
            self.__save(self.file_path, accounts)

            return True
        else:
            return False