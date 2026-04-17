# from app.models import *
#
# def test_create(account_service, service_account_factory):
#     for _ in range(5):
#         user = service_account_factory()
#         created = account_service.create(user)
#         assert created and created is not None
#
# def test_query_user(account_service, service_account_factory):
#     for _ in range(5):
#         user = service_account_factory()
#
#         created = account_service.create(user)
#         assert created and created is not None
#
#         query_username = account_service.read('username', user.username)
#         assert query_username == user
#
#         query_email = account_service.read('pii_email', user.pii_email)
#         assert query_email == user
#
# def test_get_user_id(account_service, service_account_factory):
#     user: AccountInternal = service_account_factory()
#     account_service.create(user)
#
#     user_id: str = account_service.get_user_id('username', user.username)
#
#     assert isinstance(user_id, str)
#     assert user_id == user.id
#
# def test_update(account_service, service_account_factory):
#     user: AccountInternal = service_account_factory(username='nonametester')
#
#     created = account_service.create(user)
#     assert created and created is not None
#
#     changes: AccountInternal = service_account_factory()
#     changes.id = user.id
#     assert changes.username != user.username
#     assert changes.pii_email != user.pii_email
#     assert changes.hashed_password != user.hashed_password
#     assert changes.id == user.id
#
#     updated = account_service.update('username', 'nonametester', changes)
#     assert updated and updated is not None
#
#     updated_user = account_service.read('id', user.id)
#     assert isinstance(updated_user, AccountInternal)
#     assert updated_user == changes
#     assert updated_user != user
#
#     old_user_data = account_service.read('username', user.username)
#     assert old_user_data is None
#
# def test_get_all(account_service, service_account_factory):
#     for _ in range(15):
#         user = service_account_factory()
#         account_service.create(user)
#
#     all_users: list[AccountInternal] = account_service.get_all()
#     assert all_users is not None
#     assert len(all_users) == 15
#
# def test_remove(account_service, service_account_factory):
#     users: list[str] = []
#
#     for _ in range(5):
#         user = service_account_factory()
#         account_service.create(user)
#         users.append(user.id)
#
#     user: AccountInternal = account_service.read('id', users[3])
#     assert user is not None
#
#     removed = account_service.remove(user)
#     assert removed and removed is not None
#
#     all_users = account_service.get_all()
#     assert len(all_users) == 4
#
#     verify_delete: AccountInternal = account_service.read('id', users[3])
#     assert not verify_delete or verify_delete is None