from app.models import *

def test_create(account_service, account_factory):
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

def test_query_users(account_service, account_factory):
    created_users: list[AccountInternal] = [account_factory(username='jonah') for _ in range(5)]
    assert [isinstance(user, AccountInternal) for user in created_users]
    assert len(created_users) == 5

    created: list[bool] = [account_service.create(new_user) for new_user in created_users]
    assert [created for user in created]
    assert len(created) == len(created_users)

    users: list[AccountInternal] = [account_service.query_users('username', user.username) for user in created_users]
    assert len(users) == len(created_users)

def test_update(account_service, account_factory):
    user: AccountInternal = account_factory(username='nonametester')

    created = account_service.create(user)
    assert created and created is not None

    changes: AccountInternal = account_factory()
    changes.id = user.id
    assert changes.username != user.username
    assert changes.pii_email != user.pii_email
    assert changes.hashed_password != user.hashed_password
    assert changes.id == user.id

    updated = account_service.update('username', 'nonametester', changes)
    assert updated and updated is not None

    updated_user = account_service.query_user('id', user.id)
    assert isinstance(updated_user, AccountInternal)
    assert updated_user == changes
    assert updated_user != user

    old_user_data = account_service.query_user('username', user.username)
    assert old_user_data is None

    duplicate_users = account_service.query_users('id', user.id)
    assert len(duplicate_users) == 1

def test_get_all(account_service, account_factory):
    for _ in range(15):
        user = account_factory()
        account_service.create(user)

    all_users: list[AccountInternal] = account_service.get_all()
    assert all_users is not None
    assert len(all_users) == 15