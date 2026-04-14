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
from typing import Optional

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

    def read_self(self, req: AccountInternal, field: str, value: str) -> Optional[AccountPublic]:
        '''
        Lets user view their own profile.

        :param req:
        :param field:
        :param value:
        :return:
        '''

        self._check_access_forbidden(req)

        account = self.repo.read(field, value, req_id=req.id)

        if not account[0]:
            raise ValueError('Account could not be found.')

        return AccountPublic.model_construct(account[0].model_dump(mode='json'))

    def admin_search(
            self,
            req: AccountInternal, # the user querying
            field: AcceptedFields, # the field they are querying
            value: str | AccountStatus, # the value they are searching for in that field
    ) -> Optional[list[AccountInternal]]:
        '''
        Queries for a specific user based on input.

        PERMISSIONS:
        - ADMIN are able to query any user and can query request lists of users matching queries.
        - ON_HOLD and USERS are allowed to query themselves and view their own accounts.
        - BANNED are not allowed to query themselves or anyone else.

        :param req:
        :param field:
        :param value:
        :return:
        '''

        self._check_access_forbidden(req)

        if not self._is_admin(req):
            raise PermissionError('You cannot perform this operation unless you are an administrator.')

        return self.repo.read(field, value, req_id=req.id)

    def update(self, req: AccountInternal, update: AccountInternal) -> bool | None:
        '''
        Updates a user's account with new information without replacing their IDs.

        # todo - Make specific models for updating data to simplify process.

        :param req:
        :param update:
        :return:
        '''

        self._check_access_forbidden(req)

        # guarantee users cannot change their own status, even as admin
        if req.id == update.id:
            update.status = req.status

        if not self._is_admin(req):
            if not req.id == update.id:
                raise PermissionError('You do not have permissions to edit this account.')

            return self.repo.update(req.id, update, req_id=req.id)

        return self.repo.update(update.id, update, req_id=req.id)

    def get_all(self, req: AccountInternal) -> list[AccountInternal] | None:
        '''
        Retrieves all user accounts.

        :param req:
        :return:
        '''

        self._check_access_forbidden(req)

        if not self._is_admin(req):
            raise PermissionError('You do not have permissions for this operation.')

        return self.repo.get_all()

    def remove(self, req: AccountInternal, reason: str, target: AccountInternal) -> bool | None:
        '''
        Removes a user account.

        :param req:
        :param reason:
        :param target:
        :return:
        '''

        self._check_access_forbidden(req)

        if not self._is_admin(req):
            if not req.id == target.id:
                raise PermissionError('You do not have permissions for this operation.')

            return self.repo.delete(req.id, 'User deleting their account.', req_id=req.id)

        return self.repo.delete(target.id, reason, req_id=req.id)