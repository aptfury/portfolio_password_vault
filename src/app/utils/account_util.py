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
        self.fields = AcceptedFields
        self.__auth = AuthUtilities()
        self.__pepper = os.getenv("ACCOUNT_PEPPER")

    def __access_forbidden(self, status: str) -> bool:
        '''
        Used to detect accounts that are on hold or banned.

        :param status:
        :return:
        '''
        return status == AccountStatus.ON_HOLD or status == AccountStatus.BANNED

    def __is_admin(self, status: str) -> bool:
        '''
        Shorthand for whether the user is an administrator.

        :param status:
        :return:
        '''
        return status == AccountStatus.ADMIN

    def create(self, data: CreateAccount) -> bool:
        '''
        Creates a new account for the user.

        :param data:
        :return:
        '''

        # hash user password
        hashed_password: AccountPassword = self.__auth.new_account_password(data.password)

        # create account model
        new_account: AccountInternal = AccountInternal(
            username=data.username,
            pii_email=data.email,
            hashed_password=hashed_password
        )

        # create new account
        return self.service.create(new_account)

    def query_user(
            self,
            user: AccountInternal, # the user querying
            field: AcceptedFields, # the field they are querying
            search: str | AccountStatus, # the value they are searching for in that field
            all_matches: bool = False # returns a list of all responses - ADMIN ONLY
    ) -> AccountInternal | AccountPublic | list[AccountInternal | AccountPublic] | None:
        '''
        Queries for a specific user based on input.

        PERMISSIONS:
        - ADMIN are able to query any user and can query request lists of users matching queries.
        - ON_HOLD and USERS are allowed to query themselves and view their own accounts.
        - BANNED are not allowed to query themselves or anyone else.

        :param user:
        :param field:
        :param search:
        :param all_matches:
        :return:
        '''

        is_admin: bool = self.__is_admin(user.status)
        is_forbidden: bool = self.__access_forbidden(user.status)

        if is_forbidden:
            if user.status == AccountStatus.BANNED:
                # todo - throw error
                # todo - security log attempt
                # todo - exit program without further responses
                return None

        if not is_admin:
            if getattr(user, field).lower() == search.lower() and not all_matches:
                account: AccountInternal = self.service.query_user(field, search)

                # double check that it's their account
                if user.id != account.id:
                    # todo - throw error
                    # todo - security log attempt
                    # todo - exit program with alert
                    return None

                # convert to secure view
                public_access: AccountPublic = AccountPublic.model_construct(account.model_dump(mode='json'))
                return public_access

        # double check request is coming from admin
        if is_admin:
            # check if they are requesting a list
            if all_matches:
                accounts: list[AccountInternal] = self.service.get_all()
                matches: list[AccountInternal] = list()

                for account in accounts:
                    if getattr(account, field).lower() == search.lower():
                        matches.append(account)

                return matches
            else:
                return self.service.query_user(field, search)
        else:
            # todo - throw error
            # todo - log error
            # todo - exit with alert to user that they should report this/open an issue
            return None

    def get_user_id(self, user: AccountInternal, field: str, search: str) -> str | None:
        '''
        ADMIN & INTERNAL USE ONLY.

        Allows admins and internal systems to retrieve a user's ID without returning the whole user account.

        :param user:
        :param field:
        :param search:
        :return:
        '''

        if not self.__is_admin(user.status):
            # todo - access denied/forbidden access
            # todo - add to security log
            # todo - exit with message to create bug report if user has admin permissions
            return None

        account: AccountInternal = self.service.query_user(field, search)

        return account.id

    def update(self, user: AccountInternal, field: str, search: str, update: AccountInternal) -> bool | None:
        '''
        Updates a user's account with new information without replacing their IDs.

        # todo - Make specific models for updating data to simplify process.

        :param user:
        :param field:
        :param search:
        :param update:
        :return:
        '''

        if self.__access_forbidden(user.status):
            # todo - manage error
            return None

        if not self.__is_admin(user.status):
            if user.id == update.id:
                if user.status != update.status:
                    return False

                response = self.service.update(field, search, update)
                return response
            else:
                return None

        if self.__is_admin(user.status):
            # ensure admin cannot change their own status
            if user.id == update.id and user.status != update.status:
                return False

            response = self.service.update(field, search, update)
            return response
        else:
            return None

    def get_all(self, user: AccountInternal) -> list[AccountInternal] | None:
        if not self.__is_admin(user.status):
            return None

        return self.service.get_all()

    def remove(self, user: AccountInternal, target: AccountInternal) -> bool | None:
        if not self.__is_admin(user.status):
            if self.__access_forbidden(user.status):
                return False

            if user.id == target.id:
                return self.service.remove(target)

            return None

        return self.service.remove(target)