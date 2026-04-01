# Name: Blake Lemarr
# Updated: 04.01.2026
# Description: Manages interactions between user and account operations

# ===== IMPORTS =====

import sys
from enum import Enum
from input_with_timeout import input_with_timeout
from ..models import CreateAccount
from ..utilities import AccountsUtilities
from ..utilities import introduction, main_menu, exit_program
from ..utilities import account_menu, welcome_authenticated_user, back_to_main_menu


# ===== CONTROLLER =====

class AppController:
    def __init__(self):
        pass

    @staticmethod
    def main_menu() -> int:
        print(main_menu)

        options: list[int] = [1, 2, 3, 4]
        user_selection: int = int(input_with_timeout(
            '''Your selection must be in the form of a number (e.g., 3).
            All other inputs will be considered invalid.
            
            Enter your selection: ''',
            timeout=10
        ))

        if user_selection in options:
            return user_selection
        else:
            return 0

    @staticmethod
    def exit_program(self) -> None:
        print(exit_program)
        sys.exit()