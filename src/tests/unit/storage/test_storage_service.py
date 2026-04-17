# NAME: Blake Lemarr
# DATE: 04.16.26
# DESCRIPTION: Storage test suite

# ========== IMPORTS ========== #
import json

# ========== TEST CASES ========== #
def test_create_storage(tmp_path, storage):
    db = storage('db', 'test.json')

    target_dir = tmp_path / 'db'
    target_path = target_dir / 'test.json'

    db.create_storage()

    assert db.file_path == target_path
    assert target_dir.is_dir()
    assert target_path.exists()
    assert target_path.is_file()
    assert target_path.read_text() == '[]'

def test_load_data(tmp_path, storage):
    db = storage('db', 'test.json')

    target_dir = tmp_path / 'db'
    target_path = target_dir / 'test.json'

    db.create_storage()

    assert db.file_path == target_path
    assert target_dir.is_dir()
    assert target_path.exists()
    assert target_path.is_file()

    sample_data: list = [{'id': '1', 'name': 'Fruits Basket'}]

    target_path.write_text(json.dumps(sample_data))

    assert target_path.read_text() == json.dumps(sample_data)

    data = db.load_data()

    assert data == sample_data

def test_save_data(tmp_path, storage):
    db = storage('db', 'test.json')

    target_dir = tmp_path / 'db'
    target_path = target_dir / 'test.json'

    db.create_storage()

    assert db.file_path == target_path

    sample_data: list = [{'id': '1', 'name': 'Fruits Basket'}]

    db.save_data(sample_data)

    data = db.load_data()

    assert data == sample_data

def test_delete_storage(tmp_path, storage):
    db = storage('db', 'test.json')

    target_dir = tmp_path / 'db'
    target_path = target_dir / 'test.json'

    db.create_storage()

    assert db.file_path == target_path
    assert target_path.exists()
    assert target_dir.is_dir()
    assert target_path.is_file()

    db.delete_storage()

    assert target_dir.is_dir()
    assert not target_path.exists()
    assert not target_path.is_file()