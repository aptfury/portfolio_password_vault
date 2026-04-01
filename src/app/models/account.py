# Name: Blake Lemarr
# Updated: 03.31.2026
# Description: Defines user data objects.

# ===== IMPORTS =====
from .auth import AccountPassword
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, computed_field
from pydantic.config import ConfigDict
from typing import Optional
from uuid import uuid4

# ===== DATA CONFIG =====
class AccountStatus(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    ON_HOLD = 'on_hold'
    BANNED = 'banned'

# ===== ACCOUNT =====
class AccountBase(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    pii_email: Optional[EmailStr] = Field(default=None, exclude=True)

    @computed_field
    @property
    def email(self) -> Optional[str]:
        if not self.pii_email:
            return None

        name, domain = self.pii_email.split('@')
        return f'{name[0]}{'*' * (len(name) - 1)}@{domain}'

class AccountInternal(AccountBase):
    model_config = ConfigDict(strict=True)

    id: str = Field(default_factory=lambda: uuid4().hex)
    status: AccountStatus = Field(default=AccountStatus.USER)
    hashed_password: AccountPassword = Field(exclude=True)
    created_on: datetime = Field(default_factory=datetime.now)
    updated_on: datetime = Field(default_factory=datetime.now)

class AccountPublic(AccountBase):
    model_config = ConfigDict(strict=True)

    created_on: datetime

class CreateAccount(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str