""" nav_utils.py

AUTHOR: Blake Lemarr
CREATED: 05.22.26
UPDATED:

DESCRIPTION: A utility to assist in navigating between services.

UPDATES: 
    - [mm.dd.yy] Update notice
    
IMPORTS:
    - None

"""

# ------------ nav utils ------------ #
class NavUtils:
    def __init__(
        self,
        account,
        vault
    ):
        self.account = account
        self.vault = vault

    def navigate_to_account(self):
        self.account.account_menu()
        
    def navigate_to_vault(self):
        self.vault.vault_menu()