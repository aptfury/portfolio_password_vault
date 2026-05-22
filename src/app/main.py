'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: The main file for the program that interacts
             with the user and helps them navigate the application.
'''

# ------------ IMPORTS ------------ #
import sys

from app.utilities.nav_utils import NavUtils
from app.utilities.hash_utils import HashUtils
from app.utilities.ident_utils import IdentUtils
from app.utilities.encrypt_utils import EncryptUtils

from app.services.auth_service import AuthService
from app.services.vault_service import VaultService
from app.services.account_service import AccountService

# ------------ MAIN ------------ #
def main():
    hash_utils: HashUtils = HashUtils()
    ident_utils: IdentUtils = IdentUtils()
    encrypt_utils: EncryptUtils = EncryptUtils()
    nav: NavUtils = NavUtils()
    auth_service: AuthService = AuthService(
        encrypt_utils=encrypt_utils,
        hash_utils=hash_utils,
        ident_utils=ident_utils,
    )
    vaults: VaultService = VaultService(
        encrypt_utils=encrypt_utils,
        hash_utils=hash_utils,
        ident_utils=ident_utils,
        auth_service=auth_service,
        nav_utils=nav
    )
    accounts: AccountService = AccountService(
        vault_service=vaults,
        encrypt_utils=encrypt_utils,
        hash_utils=hash_utils,
        ident_utils=ident_utils,
        auth_service=auth_service,
        nav_utils=nav
    )
    nav: NavUtils = NavUtils(vault=vaults, account=accounts)
    
    welcome_message = '''
------------------------------------------
        WELCOME TO PASSWORD VAULT!    
------------------------------------------
Select an option to get started:

(1) Create Account
(2) Log In
(3) Exit
'''
    print(welcome_message)
    
    selection: str = input('Enter a number: ')
    
    if selection == '1':
        accounts.create_account()
        return main()
    
    elif selection == '2':
        res: bool | None = accounts.login()
        
        if res:
            acc_menu: str | None = accounts.account_menu()
            
            if acc_menu == 'log out':
                acc_menu = None
                return main()
    
    elif selection == '3':
        print('\nThanks for stopping by!')
        sys.exit()
        return
    
    else:
        print(f'INVALID OPTION: {selection}')
        
        back_to_main: str = input('Return to main menu [y/n]?: ')
        
        if back_to_main == 'y':
            return main()
        else:
            print('\nSession aborted.')
            return sys.exit()

if __name__ == '__main__':
    main()