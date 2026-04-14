# Name: Blake Lemarr
# Updated: 03.31.2026
# Description: Defines user auth objects.

# ===== IMPORTS =====
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

# ===== ACCOUNT PASSWORD =====
class AccountPassword(BaseModel):
    model_config = ConfigDict(strict=True)

    hash: str
    salt: str
    iterations: int = Field(default=600000)
    algorithm: str = Field(default='PBKDF2-SHA256')