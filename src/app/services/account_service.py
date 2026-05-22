'''
AUTHOR: Blake Lemarr
DATE: 05.13.26
DESCRIPTION: Manages all of the account operations for the application
'''

# ------------ IMPORTS ------------ #
import sys
import secrets

# from getpass import getpass
from datetime import datetime
from pydantic import EmailStr
# from input_with_timeout import input_with_timeout

from ..models import (
    AccountModel,
    AccountAuthModel,
    VaultEntryModel,
    VaultModel
)
from ..utilities import (
    EncryptUtils,
    HashUtils,
    IdentUtils,
    NavUtils
)
from .auth_service import AuthService
from .vault_service import VaultService
from ..repositories import AccountRepo

# ------------ ACCOUNT SERVICE ------------ #
class AccountService:
    def __init__(
        self,
        vault_service: VaultService,
        encrypt_utils: EncryptUtils,
        hash_utils: HashUtils,
        ident_utils: IdentUtils,
        auth_service: AuthService,
        nav_utils: NavUtils
    ):
        # ------ config ------ #
        self.repo: AccountRepo = AccountRepo()
        self.vault: VaultService = vault_service
        self.encrypt: EncryptUtils = encrypt_utils
        self.hash: HashUtils = hash_utils
        self.id: IdentUtils = ident_utils
        self.auth: AuthService = auth_service
        self.nav: NavUtils = nav_utils
        
        # ------ user session ------ #
        self.session_id: str = None
        self._id: str = None
        self.name: str = None
        
    def create_account(self) -> None:
        
        name: str = None
        raw_password: str = None
        email: EmailStr = None
        
        try:
            # TODO: Add in username exists check - account utils
            # TODO: Add in username valid check - account utils
            # USERNAME should be at least 2 chars and include only letters & digits
            name = input('Enter a username: ')
            
            if name is None or '':
                print('You must provide a name/username for the account.')
                name = input('Enter a username: ')
                
                if name is None or '':
                    print('Username was not accepted. Please try again later.')
                    sys.exit()
                    return
        except TimeoutError:
            print('Account creation timed out on username.')
            sys.exit()
            return
            
        try:
            # TODO: Add in password valid check - account utils - use strings module
            # PASSWORD should be at least 8 chars (1 upper, 1 lower, 1 digit, 1 punctuation)
            attempts: int = 1
            
            for attempts in range(3):
                # TODO: Hide password when typing it in
                raw_password: str = input('Enter a password: ')
                raw_password_again: str = input('Re-enter your password: ')
                
                is_match: bool = secrets.compare_digest(raw_password, raw_password_again)
                
                if not is_match:
                    print(f'\nPasswords did not match. Please try again. (Attempt: {attempts} of 3)\n')
                    attempts += 1
                    
                    if attempts >= 3:
                        print('No more password attempts available. Please try again later.')
                        sys.exit()
                        return
                else:
                    attempts = 1
                    break
        except TimeoutError:
            print('Account creation timed out on password.')
            sys.exit()
            return
            
        try:
            # TODO - Check valid email
            email: str = input('(OPTIONAL) Enter your email: ')
            
        except TimeoutError:
            print('Account creation timed out on email.')
            sys.exit()
            return
            
    
        created: bool = self.auth.create_account(name=name, raw_password=raw_password, email=email)
        
        if not created:
            print('Account creation failed. Please restart the program and try again.')
            sys.exit()
            return
        
        user: AccountModel = self.repo.get_one_where('name', name)
        
        if not user.name == name:
            # TODO: Eventually create a file to house error messages
            # TODO: Eventually create custom errors with codes based on file
            error_msg: str = f'''
            -------------------------------
                    ACCOUNT FAILURE
            -------------------------------
            
            Your account could not be created due to an internal system error.
            Please create an issue on the github to let the maintainer(s) know.
            
            Provide the following information:
            
                SYSTEM ERROR: ACCOUNT_CREATION_FAILURE
                WHERE: ACCOUNT_SERVICE
                WHY: CHECK_EXISTS_MISMATCH
                WHEN: {datetime.now()}
                
                DETAILS: {name} submitted, {user.name} saved
            '''
            
            raise SystemError(error_msg)
        
        self.vault.create_vault(user=user)
        return
        
    def login(self) -> bool:
        try:
            name = input('Enter your username: ')
            raw_password = input('Enter your password: ')
                
            logged_in: bool = self.auth.login(name=name, raw_password=raw_password)
            
            if logged_in:
                user: AccountModel = self.repo.get_one_where('name', name)
                session_id = self.encrypt._fernet
                
                self.session_id = session_id
                self.name = user.name
                self._id = user.id
                
                print(f'Welcome back, {self.name}!')
                print(f'user_id: {self._id} || session_id: {self.session_id}')
                
            return logged_in

        
        except TimeoutError:
            print('TimeoutError: User did not responde in time.')
            sys.exit()
            
            return
        
    def account_menu(self):
        menu_options: str = f'''
--------------------------
start menu > main menu
--------------------------
        MAIN MENU
--------------------------
Hello, {self.name}!
What would you like to do?

(1) Access Password Vault
(2) View Account Details
(3) Update Account Details *Password updates not yet supported
(4) Log Out
(5) Exit
'''
        print(menu_options)
        
        nav_choice: str = input('\nEnter the number: ')
        
        if nav_choice == '1':
            vault_nav = self.vault.vault_menu(self.name)
            
            if vault_nav == 'back':
                self.account_menu()
            elif vault_nav == 'log out':
                self.logout()
                return 'log out'
        elif nav_choice == '2':
            self.view_account()
        elif nav_choice == '3':
            self.update_account()
        elif nav_choice == '4' or nav_choice == '5':
            self.logout()
            return 'log out'
        else:
            print('Invalid selection.')
            self.account_menu()
        
    def view_account(self) -> None:
        user: AccountModel = self.repo.get_one_where('name', self.name)
        
        user_view: str = f'''
--------------------------------------
        USER ACCOUNT DETAILS        
--------------------------------------

NAME: {user.name}
EMAIL: {user.email}
CREATED: {user.created}
'''
        
        print(user_view)
        return
        
    def update_account(self) -> None:
        update_options: str = '''
Which field would you liked to update?

(1) Name
(2) Email
'''
        
        print(update_options)
        
        field: str = input('\nWhich would you like to update (1 or 2): ')
        
        if field == '1' or field == 'Name':
            name: str = input('Verify your current name: ')
            new_name: str = input('Enter your new name: ')
            
            user: AccountModel = self.repo.get_one_where('name', name)
            user = user.model_copy(deep=True)
            user.name = new_name

            updated = self.repo.update_one_where(data=user, key='name', value=name)
            
            if updated:
                self.name = new_name
                print('UPDATE SUCCESSFUL')
                return
            else:
                raise Exception('USERNAME COULD NOT BE UPDATED')
            
        elif field == '2' or field == 'Email':
            email: str = input('Verify your current email: ')
            new_email: str = input('Enter your new email: ')
            
            user: AccountModel = self.repo.get_one_where('email', email)
            user = user.model_copy(deep=True)
            user.email = new_email

            updated = self.repo.update_one_where(data=user, key='email', value=email)
            
            if updated:
                print('UPDATE SUCCESSFUL')
                return
            else:
                raise Exception('EMAIL COULD NOT BE UPDATED')
            
        else:
            print('invalid request')
            return
        
    def logout(self) -> None:
        confirm: str = input('Confirm logout (y/n): ')
        
        if confirm == 'y':
            self.auth.logout()
            self.vault.logout()
            self._id = None
            self.session_id = None
            self.name = None
            
            print('Goodbye!')
            sys.exit()