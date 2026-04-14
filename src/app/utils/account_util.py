# Name: Blake Lemarr
# Updated: 04.13.2026
# Description: Manages logic for account handling.

# ========== IMPORTS ========== #
import os
from .auth_util import AuthUtil
from enum import Enum
from dotenv import load_dotenv
from ..models import (
    AccountPublic,
    AccountInternal,
    CreateAccount,
    AccountPassword,
    AccountStatus
)
from ..repositories import AccountRepository

# ========== INIT ========== #
load_dotenv()

class AcceptedFields(str, Enum):
    id = 'id'
    username = 'username'
    pii_email = 'pii_email'
    email = 'pii_email'
    created_on = 'created_on'
    status = 'status'

# ========== UTILITIES ========== #
class AccountUtil:
    def __init__(self, storage):
        self.__auth = AuthUtil(storage=storage)
        self.repo = AccountRepository(storage=storage)
        self.fields = AcceptedFields

    def _check_access_forbidden(self, user: AccountInternal) -> None:
        '''
        Used to detect accounts that are on hold or banned.

        :param status:
        :return:
        '''

        if user.status == AccountStatus.BANNED or user.status == AccountStatus.ON_HOLD:
            raise PermissionError(f'You cannot complete this operation while your account is {user.status}.')

    def _is_admin(self, user: AccountInternal) -> bool:
        '''
        Shorthand for whether the user is an administrator.

        :param status:
        :return:
        '''
        return user.status == AccountStatus.ADMIN

    def create(self, data: CreateAccount) -> bool:
        '''
        Creates a new account for the user.

        :param data:
        :return:
        '''

        # hash user password
        hashed_password: AccountPassword = self.__auth.create_user_password(data.password)

        # create account model
        new_account: AccountInternal = AccountInternal(
            username=data.username,
            pii_email=data.email,
            hashed_password=hashed_password
        )

        # create new account
        return self.repo.create(new_account, req_id='INTERNAL_ADMINISTRATOR')

    def internal_read(self, user_id: str) -> AccountInternal | None:
        '''
        Internally grabs a user by their user_id as part of internal processes.

        :param user_id:
        :return:
        '''

        # get the account
        account: list[AccountInternal] = self.repo.read('id', user_id, 'INTERNAL')

        if account is None:
            return None

        # transform account to public view and return it
        return account[0]

    def read(
            self,
            user: AccountInternal, # the user querying
            field: AcceptedFields, # the field they are querying
            value: str | AccountStatus, # the value they are searching for in that field
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
        :param value:
        :param all_matches:
        :return:
        '''

        is_admin: bool = self._is_admin(user.status)
        is_forbidden: bool = self._check_access_forbidden(user.status)

        if is_forbidden:
            if user.status == AccountStatus.BANNED:
                # todo - throw error
                # todo - security log attempt
                # todo - exit program without further responses
                return None

        if not is_admin:
            if getattr(user, field).lower() == value.lower() and not all_matches:
                account: list[AccountInternal] = self.repo.read(field, value, user.id)

                # double check that it's their account
                if user.id != account.id:
                    # todo - throw error
                    # todo - security log attempt
                    # todo - exit program with alert
                    return None

                # convert to secure view
                public_access: AccountPublic = AccountPublic.model_construct(account[0].model_dump(mode='json'))
                return public_access

        # double check request is coming from admin
        if is_admin:
            # check if they are requesting a list
            accounts: list[AccountInternal] = self.repo.read(field, value, user.id)

            if all_matches:
                return accounts
            else:
                return accounts[0]
        else:
            # todo - throw error
            # todo - log error
            # todo - exit with alert to user that they should report this/open an issue
            return None

    def update(self, user: AccountInternal, update: AccountInternal) -> bool | None:
        '''
        Updates a user's account with new information without replacing their IDs.

        # todo - Make specific models for updating data to simplify process.

        :param user:
        :param field:
        :param search:
        :param update:
        :return:
        '''

        if self._check_access_forbidden(user.status):
            # todo - manage error
            return None

        if not self._is_admin(user.status):
            if user.id == update.id:
                if user.status != update.status:
                    return False

                response = self.repo.update(update.id, update, user.id)
                return response
            else:
                return None

        if self._is_admin(user.status):
            # ensure admin cannot change their own status
            if user.id == update.id and user.status != update.status:
                return False

            response = self.repo.update(update.id, update, user.id)
            return response
        else:
            return None

    def get_all(self, user: AccountInternal) -> list[AccountInternal] | None:
        '''
        Retrieves all user accounts.

        :param user:
        :return:
        '''
        if not self._is_admin(user.status):
            return None

        return self.repo.get_all()

    def remove(self, user: AccountInternal, reason: str, target: AccountInternal) -> bool | None:
        '''
        Removes a user account.

        :param user:
        :param reason:
        :param target:
        :return:
        '''
        if not self._is_admin(user.status):
            if self._check_access_forbidden(user.status):
                return False

            if user.id == target.id:
                return self.repo.delete(target.id, reason, user.id)

            return None

        return self.repo.delete(target.id, reason, user.id)