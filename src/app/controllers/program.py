# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages interactions between user and account operations

# ===== IMPORTS =====

from . import AccountsController
from input_with_timeout import input_with_timeout

# ===== CONTROLLER =====

class AppController:
    def __init__(self):
        self.accounts: AccountsController = AccountsController()
        self.app_name: str = 'Indie Password Vault' # working title because no creative juices
        self.version: str = 'v.0.0.1'
        self.menu_options: dict = {
            1: 'log in',
            2: 'register account',
            3: 'help',
            4: 'exit',
            "invalid_input": "invalid"
        }

    def introduction(self) -> None:
        print(f'''====== {self.app_name} {self.version} ======

Hello! Welcome to {self.app_name}!
''')

    def main_menu(self, first_time: bool) -> str:
        if first_time:
            self.introduction()

        print('''Choose an option from the menu below:
    (1) Log In
    (2) Register Account
    (3) Help
    (4) Exit
''')

        user_selection: int = int(input_with_timeout('''
        Your selection must be in the form of a number (e.g., 3).
        All other inputs will be considered invalid.
        
        Enter your selection:
        ''',
            timeout=10
        ))

        if user_selection in self.menu_options.keys():
            return self.menu_options[user_selection]
        else:
            return self.menu_options['invalid_input']

    def account_handler(self, data):
        pass

    def vault_handler(self, option: str):
        pass