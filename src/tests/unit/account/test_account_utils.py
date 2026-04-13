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

def test_get_user_id(account_util, util_registered_user_factory):
    admin = util_registered_user_factory(status=AccountStatus.ADMIN)
    user = util_registered_user_factory(status=AccountStatus.USER)

    assert isinstance(admin, AccountInternal)
    assert isinstance(user, AccountInternal)

    fetch_id_as_admin = account_util.get_user_id(admin, 'username', user.username)
    fetch_id_as_user = account_util.get_user_id(user, 'username', user.username)

    expected_fetch_id_as_admin = user.id
    expected_fetch_id_as_user = None

    assert isinstance(fetch_id_as_admin, str)
    assert fetch_id_as_admin == expected_fetch_id_as_admin
    assert fetch_id_as_user == expected_fetch_id_as_user

def test_update(account_util, util_registered_user_factory):
    admin: AccountInternal = util_registered_user_factory(username='main_admin', status=AccountStatus.ADMIN)
    user: AccountInternal = util_registered_user_factory(username='main_user', status=AccountStatus.USER)
    on_hold: AccountInternal = util_registered_user_factory(username='user_hold', status=AccountStatus.ON_HOLD)
    banned: AccountInternal = util_registered_user_factory(username='user_banned', status=AccountStatus.BANNED)

    assert [isinstance(account, AccountInternal) for account in [admin, user, on_hold, banned]]

    ### TEST CASE UPDATE ACCOUNTS ###

    admin_update_legal: AccountInternal = util_registered_user_factory(username='admin_name_change', status=AccountStatus.ADMIN)
    admin_update_illegal: AccountInternal = util_registered_user_factory(status=AccountStatus.USER)
    admin_update_legal.id = admin.id
    admin_update_illegal.id = admin.id

    user_update_legal: AccountInternal = util_registered_user_factory(username='user_name_change', status=AccountStatus.USER)
    user_update_illegal: AccountInternal = util_registered_user_factory(status=AccountStatus.ADMIN)
    user_update_legal.id = user.id
    user_update_illegal.id = user.id

    on_hold_update_illegal_name: AccountInternal = util_registered_user_factory(username='on_hold_name_change', status=AccountStatus.ON_HOLD)
    on_hold_update_illegal_status: AccountInternal = util_registered_user_factory(status=AccountStatus.USER)
    on_hold_update_illegal_name.id = on_hold.id
    on_hold_update_illegal_status.id = on_hold.id

    banned_update_illegal_name: AccountInternal = util_registered_user_factory(username='banned_name_change', status=AccountStatus.BANNED)
    banned_update_illegal_status: AccountInternal = util_registered_user_factory(status=AccountStatus.ADMIN)
    banned_update_illegal_name.id = banned.id
    banned_update_illegal_status.id = banned.id

    ### TEST CASE UPDATE ACCOUNTS ###

    ### ON_HOLD ###
    on_hold_can_update_on_hold: bool = account_util.update(on_hold, 'id', on_hold.id, on_hold_update_illegal_name)
    assert on_hold_can_update_on_hold is None

    on_hold_can_promote_on_hold: bool = account_util.update(on_hold, 'id', on_hold.id, on_hold_update_illegal_status)
    assert on_hold_can_promote_on_hold is None

    on_hold_can_update_user: bool = account_util.update(on_hold, 'id', user.id, user_update_legal)
    assert on_hold_can_update_user is None

    on_hold_can_update_admin: bool = account_util.update(on_hold, 'id', admin.id, admin_update_illegal)
    assert on_hold_can_update_admin is None
    ### ON_HOLD ###

    ### BANNED ###
    banned_can_update_banned: bool = account_util.update(banned, 'id', banned.id, banned_update_illegal_name)
    assert banned_can_update_banned is None

    banned_can_promote_banned: bool = account_util.update(banned, 'id', banned.id, banned_update_illegal_status)
    assert banned_can_promote_banned is None

    banned_can_update_user: bool = account_util.update(banned, 'id', user.id, user_update_illegal)
    assert banned_can_update_user is None

    banned_can_update_admin: bool = account_util.update(banned, 'id', admin.id, admin_update_illegal)
    assert banned_can_update_admin is None
    ### BANNED ###

    ### USER ###
    user_can_update_user_info: bool = account_util.update(user, 'id', user.id, user_update_legal)
    assert user_can_update_user_info is True

    user_can_promote_user: bool = account_util.update(user, 'id', user.id, user_update_illegal)
    assert user_can_promote_user is False

    user_can_update_admin: bool = account_util.update(user, 'id', admin.id, admin_update_illegal)
    assert user_can_update_admin is None

    user_can_update_on_hold: bool = account_util.update(user, 'id', on_hold.id, on_hold_update_illegal_name)
    assert user_can_update_on_hold is None

    user_can_update_banned: bool = account_util.update(user, 'id', banned.id, banned_update_illegal_name)
    assert user_can_update_banned is None
    ### USER ###

    ### ADMIN ###
    admin_can_update_admin: bool = account_util.update(admin, 'id', admin.id, admin_update_legal)
    assert admin_can_update_admin is True

    admin_can_demote_admin: bool = account_util.update(admin, 'id', admin.id, admin_update_illegal)
    assert admin_can_demote_admin is False

    admin_can_promote_user: bool = account_util.update(admin, 'id', user.id, user_update_illegal)
    assert admin_can_promote_user is True

    admin_can_update_on_hold: bool = account_util.update(admin, 'id', on_hold.id, on_hold_update_illegal_status)
    assert admin_can_update_on_hold is True

    admin_can_update_banned: bool = account_util.update(admin, 'id', banned.id, banned_update_illegal_status)
    assert admin_can_update_banned is True
    ### ADMIN ###

def test_get_all(account_util, util_registered_user_factory):
    admin = util_registered_user_factory(status=AccountStatus.ADMIN)
    user = util_registered_user_factory(status=AccountStatus.USER)
    on_hold = util_registered_user_factory(status=AccountStatus.ON_HOLD)
    banned = util_registered_user_factory(status=AccountStatus.BANNED)

    banned_can_get_all: list[AccountInternal] = account_util.get_all(banned)
    assert banned_can_get_all is None

    on_hold_can_get_all: list[AccountInternal] = account_util.get_all(on_hold)
    assert on_hold_can_get_all is None

    user_can_get_all: list[AccountInternal] = account_util.get_all(user)
    assert user_can_get_all is None

    admin_can_get_all: list[AccountInternal] = account_util.get_all(admin)
    assert admin_can_get_all is not None
    assert [isinstance(user, AccountInternal) for user in admin_can_get_all]

def test_remove(account_util, util_registered_user_factory):
    admin: AccountInternal = util_registered_user_factory(status=AccountStatus.ADMIN)
    user: AccountInternal = util_registered_user_factory(status=AccountStatus.USER)
    on_hold: AccountInternal = util_registered_user_factory(status=AccountStatus.ON_HOLD)
    banned: AccountInternal = util_registered_user_factory(status=AccountStatus.BANNED)

    banned_can_remove_user: bool = account_util.remove(banned, user)
    assert banned_can_remove_user is False

    banned_can_remove_self: bool = account_util.remove(banned, banned)
    assert banned_can_remove_self is False

    on_hold_can_remove_user: bool = account_util.remove(on_hold, user)
    assert on_hold_can_remove_user is False

    on_hold_can_remove_self: bool = account_util.remove(on_hold, on_hold)
    assert on_hold_can_remove_self is False

    user_can_remove_user: bool = account_util.remove(user, on_hold)
    assert user_can_remove_user is None

    user_can_remove_self: bool = account_util.remove(user, user)
    assert user_can_remove_self is True

    admin_can_remove_user: bool = account_util.remove(admin, banned)
    assert admin_can_remove_user is True

    admin_can_remove_self: bool = account_util.remove(admin, admin)
    assert admin_can_remove_self is True