# Name: Blake Lemarr
# Updated: 04.13.2026
# Description: Manages logic for authorization.

# ===== IMPORTS =====
from ..models import (
    AccountInternal,
    AccountLogIn,
    AccountPassword
)
from .crypto_util import CryptoUtil
from ..repositories import AccountRepository


# ===== UTILITIES =====
class AuthUtil:
    def __init__(self, storage):
        self.crypto_util: CryptoUtil = CryptoUtil()
        self.account_repo: AccountRepository = AccountRepository(storage=storage)

    def create_user_password(self, raw_password: str) -> AccountPassword:
        '''
        Gets propper password data from crypto util.

        :param raw_password:
        :return:
        '''
        return self.crypto_util.create_hash(raw_password)

    def authorize_log_in(self, login: AccountLogIn) -> str | None:
        '''
        Authorizes user login and returns user id if valid.

        :param login:
        :return:
        '''
        user: list[AccountInternal] = self.account_repo.read('username', login.username, 'INTERNAL_ADMIN')

        if user[0] is None:
            return None

        valid_password: bool = self.crypto_util.validate_hash(login.password, user[0].hashed_password)

        if not valid_password:
            return None

        return user[0].id