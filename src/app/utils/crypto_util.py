# Name: Blake Lemarr
# Updated: 04.13.2026
# Description: Manages cryptography logic

# ===== IMPORTS =====
import os
import base64
import hashlib
import secrets
from dotenv import load_dotenv
from ..models import AccountPassword, AccountSalt

# ===== INITS =====
load_dotenv()

# ===== UTILITY =====
class CryptoUtil:
    def __init__(self):
        self.__ACCOUNT_PEPPER = os.getenv('ACCOUNT_PEPPER')
        self.__VAULT_PEPPER = os.getenv('VAULT_PEPPER')

    def __verify_peppers(self):
        if not self.__ACCOUNT_PEPPER:
            raise ValueError('ACCOUNT_PEPPER is missing or has not been set.')

        if not self.__VAULT_PEPPER:
            raise ValueError('VAULT_PEPPER is missing or has not been set.')

    def __generate_salt(self) -> AccountSalt:
        new_salt_bytes: bytes = secrets.token_bytes(32)
        new_salt: str = base64.b64encode(new_salt_bytes).decode('utf-8')

        return AccountSalt(salt_bytes=new_salt_bytes, salt=new_salt)

    def create_hash(self, raw_password: str) -> AccountPassword:
        '''
        Generates a hash for the vault key.

        :param raw_password:
        :return:
        '''
        self.__verify_peppers() # verify active peppers

        # generate salts
        salts: AccountSalt = self.__generate_salt()

        # attach pepper
        peppered: str = raw_password + self.__ACCOUNT_PEPPER

        # encode
        password_bytes: bytes = peppered.encode('utf-8')

        # generate password hash
        hashed_password_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salts.salt_bytes,
            600000
        )

        # convert hash to str
        hashed_password: str = base64.b64encode(hashed_password_bytes).decode('utf-8')

        # return account password
        return AccountPassword(
            salt=salts.salt,
            hash=hashed_password
        )

    def validate_hash(self, raw_password: str, stored_password: AccountPassword) -> bool | None:
        '''
        Validate matching passwords.

        :param raw_password:
        :param stored_password:
        :return:
        '''
        self.__verify_peppers()

        # generate hash from raw password
        peppered: str = raw_password + self.__ACCOUNT_PEPPER
        password_bytes: bytes = peppered.encode('utf-8')
        salt_bytes: bytes = stored_password.salt.encode('utf-8')
        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )
        hash_string: str = base64.b64encode(hash_bytes).decode('utf-8')

        return hash_string == stored_password.hash