# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages JSON file manipulation.

# ===== IMPORTS =====

import json
from pathlib import Path

# ===== SERVICES =====

class FileManagementService:
    def __init__(self, folder: str, filename: str):
        self.folder = folder
        self.filename = filename

    def construct_path(self) -> Path:
        '''
        Creates the path for the file being accessed.

        :param folder:
        :param filename:
        :return:
        '''

        if not self.filename.endswith('.json'):
            self.filename += '.json'

        return Path(f'../../{self.folder}/{self.filename}')  # define and return the appropriate path

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

    def destroy_file(self) -> bool:
        '''
        Deletes a file.

        :return:
        '''

        file_path = self.construct_path()

        file_path.unlink(missing_ok=True)  # Remove file

        return not file_path.exists()