from app.models import *

def test_create_new_account(account_service, account_factory):
    for _ in range(5):
        user = account_factory()
        created = account_service.create(user)
        assert created and created is not None

def test_query_user(account_service, account_factory):
    for _ in range(5):
        user = account_factory()

        created = account_service.create(user)
        assert created and created is not None

        query_username = account_service.query_user('username', user.username)
        assert query_username == user

        query_email = account_service.query_user('pii_email', user.pii_email)
        assert query_email == user