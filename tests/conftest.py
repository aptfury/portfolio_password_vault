""" conftest.py

AUTHOR: Blake Lemarr
CREATED: 05.26.26
UPDATED: 05.26.26

DESCRIPTION: Configuration file for pytest

UPDATES:
    - [mm.dd.yy] Update info
    
DEPENDENCIES:
    - pytest
    - Mock

"""

# -------------------- IMPORTS -------------------- #
import pytest
from unittest.mock import Mock

# -------------------- CONFIGS -------------------- #
@pytest.fixture
def fake_user():
    user: Mock = Mock()
    user.id = '1'
    user.username = 'lola'
    user.email = 'lol@doggo.com'
    
    return user

@pytest.fixture
def fake_password():
    pw: Mock = Mock()
    pw.id = 'PW_1'
    pw.website = 'www.doggos.com'
    pw.username = 'lola'
    pw.password = 'supersecret'
    
    return pw