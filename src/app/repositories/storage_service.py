# NAME: Blake Lemarr
# DATE: 04.14.26
# DESCRIPTION: Manages JSON file manipulation.

# ========== IMPORTS ========== #
import json
from pathlib import Path
from typing import Any

# ========== SERVICE ========== #
class StorageService:
    def __init__(self, directory: str, filename: str):
        self.filename = filename if filename.endswith('.json') else f'{filename}.json'
        self.file_path = self._construct_path(directory)

    def _construct_path(self, directory: str) -> Path:
        '''
        Moves to the root directory and builds directory.

        :param directory:
        :return:
        '''

        src_dir: Path = Path(__file__).resolve().parent.parent.parent
        storage_dir: Path = src_dir / directory
        return storage_dir / self.filename

    def create_storage(self) -> None:
        '''
        Checks the path to make sure it exists.

        :return:
        '''

        self.file_path.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=4)

    def load_data(self) -> list[dict[str, Any]]:
        '''
        Loads any data from the file.

        :return:
        '''

        if not self.file_path.exists():
            self.create_storage()

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_data(self, data: list[dict[str, Any]]) -> None:
        '''
        Saves any data to the file.

        :param data:
        :return:
        '''

        if not self.file_path.exists():
            self.create_storage()

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def delete_storage(self) -> bool:
        '''
        Deletes a storage file from the system.

        :return:
        '''

        self.file_path.unlink(missing_ok=True)
        return not self.file_path.exists()