# NAME: Blake Lemarr
# DATE: 04.16.26
# DESCRIPTION: Storage test suite

# ========== TEST CASES ========== #
def test_create_storage(tmp_path, storage):
    db = storage('db', 'test.json')

    target_dir = tmp_path / 'db'
    target_path = target_dir / 'test.json'

    db.create_storage()

    assert db.file_path == target_path
    assert target_path.exists()
    assert db.file_path.exists()

def test_load_data(tmp_path, storage):
    db = storage('db', 'test.json')

    target_dir = tmp_path / 'db'
    target_path = target_dir / 'test.json'

    db.create_storage()

    assert db.file_path == target_path
    assert target_path.exists()
    assert db.file_path.exists()

    data = db.load_data()

    assert data is not None
    assert data == '[]'

# Tests dynamic creation of paths and files for data storage.
# def test_create_if_missing(tmp_path):
#     # create path
#     target_dir = tmp_path / 'storage'
#     target_file = 'accounts.json'
#
#     # start storage service with correct path
#     storage = StorageService(f'{target_dir}', target_file)
#
#     # create the directory and/or file if missing
#     created = storage.create_if_missing()
#
#     # test expectations
#     expected_file_path = target_dir / target_file
#     expected_content = '[]'
#
#     assert created
#     assert target_dir.is_dir()
#     assert expected_file_path.exists()
#     assert expected_file_path.is_file()
#     assert expected_file_path.read_text() == expected_content
#
# def test_read_file(tmp_path):
#     # create path
#     target_dir = tmp_path / 'data'
#     target_file = 'accounts.json'
#
#     # init service
#     service = StorageService(f'{target_dir}', target_file)
#
#     # create dir + file and get path
#     created = service.create_if_missing()
#     file_path = service.construct_path()
#
#     # read contents of file
#     contents = service.read_file(file_path)
#
#     # expectations
#     expected_file_path = target_dir / target_file
#     expected_contents = []
#
#     assert created
#     assert target_dir.is_dir()
#     assert expected_file_path.exists()
#     assert contents == expected_contents
#
# def test_save_file(tmp_path):
#     target_dir = tmp_path / 'data'
#     target_file = 'accounts.json'
#
#     service = StorageService(f'{target_dir}', target_file)
#
#     created = service.create_if_missing()
#     file_path = service.construct_path()
#
#     user_accounts: list = []
#     user = CreateAccount(
#         username='bugs bunny',
#         email='lola@princess.com',
#         password='alphabetsoup'
#     )
#     user_accounts.append(user)
#
#     service.save_file(file_path, user_accounts)
#
#     contents = service.read_file(file_path)
#
#     expected_contents = [acc.model_dump() for acc in user_accounts]
#
#     assert created
#     assert contents == expected_contents
#
# def test_destroy_file(tmp_path):
#     target_dir = tmp_path / 'data'
#     target_file = 'accounts.json'
#
#     service = StorageService(f'{target_dir}', target_file)
#
#     created = service.create_if_missing()
#     file_path = service.construct_path()
#
#     assert created
#     assert file_path.exists()
#
#     destroyed = service.destroy_file()
#
#     assert created
#     assert destroyed
#     assert not file_path.exists()