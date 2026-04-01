'''
Name: Blake Lemarr
Project: Password Vault
Description: The user access point for the application.
Documentation: docs/main

TODO - create documentation
'''

# ===============================
# IMPORTS
# ===============================

from sys import exit
from .controllers import AppController
from .controllers import AccountsController
from .models import AccountPublic, AccountInternal
from .utilities import introduction

def main():
    program: AppController = AppController()
    accounts: AccountsController = AccountsController()

    # ===============================
    # MAIN MENU
    # ===============================

    # start up sequence
    print(introduction)

    # main menu and user selection
    option: int = program.main_menu()

    if option == 0:
        print('Invalid input. Exiting...')
        exit()

    elif option == 1:
        exit() # todo - create log in

    elif option == 2:
        user = accounts.register_new_account()

        print(f'''
        Your account has been created with the following details.
        
        {user}
        
        See you next time!
        ''')
        exit()

    # ===============================
    # USER LOGIN
    # ===============================



    # ===============================
    # RETRIEVE PASSWORD(S)
    # ===============================



    # ===============================
    # EXPORT ALL USER DATA
    # ===============================



    # ===============================
    # HELP
    # ===============================



    # ===============================
    # EXIT
    # ===============================


main()