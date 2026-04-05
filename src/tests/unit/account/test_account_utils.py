from app.models import *

def test_create(account_util, account_service, util_account_factory):
    util = account_util
    service = account_service
    new_user: CreateAccount = util_account_factory()

    assert isinstance(new_user, CreateAccount)

    created: bool = util.create(new_user)
    assert created and created is not None

    account: AccountInternal = service.query_user(util.fields.username, new_user.username)
    assert isinstance(account, AccountInternal)
    assert account.username == new_user.username
    assert account.pii_email == new_user.email

def test_query_user(account_util, util_registered_user_factory):
    admin: AccountInternal = util_registered_user_factory(email='admin@email.com', status=AccountStatus.ADMIN)
    user: AccountInternal = util_registered_user_factory(email='admin@email.com', status=AccountStatus.USER)
    on_hold: AccountInternal = util_registered_user_factory(status=AccountStatus.ON_HOLD)
    banned: AccountInternal = util_registered_user_factory(status=AccountStatus.BANNED)

    # queries from banned users
    banned_response_self = account_util.query_user(banned, 'username', banned.username)
    banned_response_other = account_util.query_user(banned, 'username', admin.username)

    expected_banned_response_self = None
    expected_banned_response_other = None

    assert banned_response_self == expected_banned_response_self
    assert banned_response_other == expected_banned_response_other

    # queries from on_hold users
    on_hold_response_self = account_util.query_user(on_hold, 'username', on_hold.username)
    on_hold_response_other = account_util.query_user(on_hold, 'username', user.username)

    expected_on_hold_response_self = AccountPublic.model_construct(on_hold.model_dump(mode='json'))
    expected_on_hold_response_other = None

    assert isinstance(on_hold_response_self, AccountPublic)
    assert on_hold_response_self == expected_on_hold_response_self
    assert on_hold_response_other == expected_on_hold_response_other

    # queries from users
    user_response_self = account_util.query_user(user, 'username', user.username)
    user_response_other = account_util.query_user(user, 'username', banned.username)

    expected_user_response_self = AccountPublic.model_construct(user.model_dump(mode='json'))
    expected_user_response_other = None

    assert isinstance(user_response_self, AccountPublic)
    assert user_response_self == expected_user_response_self
    assert user_response_other == expected_user_response_other

    # queries from admin
    admin_response_self = account_util.query_user(admin, 'username', admin.username)
    admin_response_other = account_util.query_user(admin, 'username', user.username)
    admin_response_list = account_util.query_user(admin, 'pii_email', 'admin@email.com', True)

    expected_admin_response_self = admin
    expected_admin_response_other = user
    expected_admin_response_list = [admin, user]

    assert isinstance(admin_response_self, AccountInternal)
    assert isinstance(admin_response_other, AccountInternal)
    assert [isinstance(user, AccountInternal) for user in admin_response_list]

    assert admin_response_self == expected_admin_response_self
    assert admin_response_other == expected_admin_response_other
    assert admin_response_list == expected_admin_response_list