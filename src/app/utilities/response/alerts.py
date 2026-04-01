# Name: Blake Lemarr
# Updated: 03.31.2026
# Description: Defines alert objects.

# ===== IMPORTS =====
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from pydantic.config import ConfigDict
from typing import Annotated, Optional


# ===== DATA CONFIG =====
class AlertType(str, Enum):
    MAXIMUM_LOGIN_ATTEMPTS = 'maximum_login_attempts'
    ACCOUNT_ON_HOLD = 'account_on_hold'
    ACCOUNT_BANNED = 'account_banned'
    PASSWORD_CHANGED = 'password_changed'