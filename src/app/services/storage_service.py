# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages JSON file manipulation.

# ===== IMPORTS =====

import json
from pathlib import Path

# ===== SERVICES =====

class StorageService:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename if filename.endswith('.json') else f'{filename}.json'

    def construct_path(self) -> Path:
        '''
        Creates the path for the file being accessed.

        :param folder:
        :param filename:
        :return:
        '''

        this_file: Path = Path(__file__).resolve() # resolve location of this file
        src_dir: Path = this_file.parent.parent.parent # move up 3 levels to src
        storage_dir: Path = src_dir / self.directory # ensure chosen folder is used
        full_path: Path = storage_dir / self.filename # ensure chose file is used.

        return full_path

    def create_if_missing(self) -> bool:
        '''
        Checks if a data folder or JSON file if they are missing.

        Only supports JSON files.

        :param folder:
        :param filename:
        :return:
        '''

        file_path = self.construct_path()
        file_path.parent.mkdir(parents=True, exist_ok=True)  # creates the folder if missing

        if not file_path.exists():
            with open(file_path, 'w') as file:  # creates the file if missing
                json.dump([], file, indent=4)

        return file_path.exists()

    def read_file(self, file_path: Path):
        '''
        Loads the file and returns list of AccountInternal objects.

        :param file_path:
        :return:
        '''
        if not file_path.exists():
            self.create_if_missing()

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = []

        return data

    def save_file(self, file_path: Path, data: list) -> None:
        '''
        Saves data passed to the method in the correct file.

        :param file_path:
        :param data:
        :return:
        '''
        if not file_path.exists():
            self.create_if_missing()

        with open(file_path, 'w') as file:
            save_data: list = [item.model_dump(mode='json') for item in data]
            json.dump(save_data, file, indent=4)

        return None

    def destroy_file(self) -> bool:
        '''
        Deletes a file.

        :return:
        '''

        file_path = self.construct_path()

        file_path.unlink(missing_ok=True)  # Remove file

        return not file_path.exists()