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

import getpass
from sys import exit
from .controllers import MainController
from .controllers import AccountsController
from .models import AccountPublic, AccountInternal

def main():
    program: MainController = MainController()
    accounts: AccountsController = AccountsController()

    # ===============================
    # MAIN MENU
    # ===============================

    # start up sequence

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