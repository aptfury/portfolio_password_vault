'''
AUTHOR: Blake Lemarr
DATE: 05.14.26
DESCRIPTION: Manages all of the vault operations for the application.
'''

# ------------ IMPORTS ------------ #
import sys
import json
import secrets

# from getpass import getpass
from datetime import datetime
# from input_with_timeout import input_with_timeout

from ..models import AccountModel, AccountAuthModel, VaultModel, VaultEntryModel, VaultLoginDataModel

from ..repositories.vault_repo import VaultRepo
from ..repositories.account_repo import AccountRepo

from .auth_service import AuthService
from ..utilities import EncryptUtils, HashUtils, IdentUtils, NavUtils

# ------------ VAULT SERVICE ------------ #
class VaultService:
    def __init__(
        self,
        encrypt_utils: EncryptUtils,
        hash_utils: HashUtils,
        ident_utils: IdentUtils,
        auth_service: AuthService,
        nav_utils: NavUtils
    ):
    # ------ config ------ #
        self.repo: VaultRepo = VaultRepo()
        self.account_repo: AccountRepo = AccountRepo()
        self.encrypt: EncryptUtils = encrypt_utils
        self.hash: HashUtils = hash_utils
        self.id: IdentUtils = ident_utils
        self.auth: AuthService = auth_service
        self.nav: NavUtils = nav_utils
        
        # ------ user session ------ #
        self.name: str = None
        self.vault_id: str = None
        
    def create_vault(self, user: AccountModel) -> None:
        vault = VaultModel(
            _id=user.password.vault_id,
            user_id=user.id,
            created=str(datetime.now()),
            vault=[]
        )
        
        try:
            created = self.repo.create(vault)
            if created:
                return
            else:
                raise SystemError(f'An error occured and the vault could not be created at this time. (USER_ID: {user.id} | VAULT_ID: {user.password.vault_id})')
        except Exception as e:
            print(e)
            
    # todo - create a login method
    def vault_menu(self, name: str) -> str | None:
        if self.auth.access_granted:
            if self.vault_id is None:
                user: AccountModel = self.account_repo.get_one_where('name', name)
                self.vault_id = user.password.vault_id
                self.name = name
        else:
            raise PermissionError('ACCESS_FORBIDDEN: If this is an error, please close the application and log in again.')
        
        menu_options: str = f'''
--------------------------
main menu > vault menu
--------------------------
        VAULT MENU
--------------------------
(1) Add Password
(2) Find Password
(3) View Passwords
(4) Manage Passwords
(5) Back
(6) Log Out
'''
        
        print(menu_options)
        nav_choice: int = int(input('\nWhat would you like to do? Enter the number: '))
        
        if nav_choice == 1:
            self.add_password()
        elif nav_choice == 2:
            self.find_password()
        elif nav_choice == 3:
            self.view_passwords()
        elif nav_choice == 4:
            pass_nav = self.manage_passwords()
            
            if pass_nav == 'back':
                self.nav.navigate_to_account()
            elif pass_nav == 'log out':
                return 'log out'
        elif nav_choice == 5:
            return 'back'
        elif nav_choice == 6:
            return 'log out'
        else:
            print('Invalid selection')
            self.vault_menu(name)
        
    def add_password(self) -> bool:
        entry: VaultEntryModel = VaultEntryModel(
            _id=self.id.generate_nano_id(),
            name='',
            website='',
            login=VaultLoginDataModel(
                username='',
                password=''
            ),
            created=str(datetime.now())
        )
        
        entry.name = input('(Optional - Enter to skip)\nPassword Name: ') or None
        
        entry.website = input('(Optional - Enter to skip)\nWebsite: ') or None
        
        entry.login.username = input('(Optional = Enter to skip)\nUsername: ') or None
        
        entry.login.password = input('Password: ') or None

        if entry.login.password is None:
            print('[ALERT!] You must enter a password.')
            
            entry.login.password = input('Password: ') or None
            
            if entry.login.password is None:
                raise ValueError('No password entered; Action aborted.')
                
        if (
            entry.name is None and
            entry.website is None and
            entry.login.username is None
        ):
            print('WARNING: You did not add a name, website, or username for your password entry.')
            option: str = input('Would you liked to add one? [y/n]: ')
            
            if option == 'y':
                option: str = input('Which would you liked to add? [Name, Website, Username]: ')
                
                if option.lower() == 'name':
                    entry.name = input('Password Name: ') or None
                    
                    if entry.name is None:
                        raise ValueError('Name was not entered.')
                
                if option.lower() == 'website':
                    entry.website = input('Website: ') or None
                    
                    if entry.website is None:
                        raise ValueError('Website was not entered.')
                    
                if option.lower() == 'username':
                    entry.login.username = input('Username: ') or None

                    if entry.login.username is None:
                        raise ValueError('Username was not entered.')
                    
        print('You can edit the password any time. Here is the entry ID - it can be used to find the password later, so be sure to save it somewhere safe.')
        print(f'\n#### PASSWORD ID: {entry.id} ####\n')
        
        vault: VaultModel = self.repo.get_by_id(self.vault_id)
        vault.vault.append(entry)
        
        saved: bool = self.repo.update_one_where(vault, '_id', self.vault_id)
        
        if saved:
            print('Password added to vault!')
            self.vault_menu(self.name)
        else:
            raise SystemError('Password could not be saved. Please try again later.')
        
    def find_password(self) -> None:
        user_vault: VaultModel = self.repo.get_by_id(self.vault_id)
        look_up_options: list = ['id', 'name', 'website', 'username', 'password']        
        
        if len(user_vault.vault) <= 0:
            print('Could not find any passwords.')
            self.vault_menu(self.name)
        
        print('You can look up your password using its ID, Name, Website, Username, or the Password itself.')
        look_up: str = input('Look up by: ')
        
        if look_up.lower() not in look_up_options:
            print('You must select one of the following: ID, Name, Website, Username, Password.')
            look_up: str = input('Look up by: ')
            
            if look_up.lower() not in look_up_options:
                raise KeyError('User did not submit one of the available look_up keys.')
            
        value: str = input(f'Enter the {look_up}: ')
        
        search_results: list[VaultEntryModel] = []
        
        for entry in user_vault.vault:
            if look_up.lower() == '_id':
                if entry.id == value:
                    search_results.append(entry)
                    
            elif look_up.lower() == 'name':
                if entry.name == value:
                    search_results.append(entry)
                    
            elif look_up.lower() == 'website':
                if entry.website == value:
                    search_results.append(entry)
                    
            elif look_up.lower() == 'username':
                if entry.login.username == value:
                    search_results.append(entry)
                    
            elif look_up.lower() == 'password':
                if entry.login.password == value:
                    search_results.append(entry)
            
        if len(search_results) == 0:
            print('No entries found.')
            return
        
        reveal_pass: str = input('Would you like the results to show your password [y/n]?: ')
        
        for result in search_results:
            template: str = f''''
===============================
        RESULTS: {search_results.index(result) + 1} of {len(search_results)}
-------------------------------
id: {result.id}
name: {result.name}
-------------------------------
website: {result.website}
username: {result.login.username}
password: {('*' * len(result.login.password)) if reveal_pass == 'n' else result.login.password}
===============================
'''
            print(template)
            self.vault_menu(self.name)
            
            
    def view_passwords(self) -> None:
        user_vault: VaultModel = self.repo.get_by_id(self.vault_id)
        
        if len(user_vault.vault) <= 0:
            print('You do not have any stored passwords')
            self.vault_menu(self.name)
        
        reveal_pass: str = input('Reveal password [y/n]?: ')
        
        for result in user_vault.vault:
            template: str = f''''
===============================
        RESULTS: {user_vault.vault.index(result) + 1} of {len(user_vault.vault)}
-------------------------------
id: {result.id}
name: {result.name}
-------------------------------
website: {result.website}
username: {result.login.username}
password: {('*' * len(result.login.password)) if reveal_pass == 'n' else result.login.password}
===============================
'''
            print(template)
            
            self.vault_menu(self.name)
    
    def manage_passwords(self) -> None | str:
        menu_options: str = f'''
--------------------------------
vault menu > password manager
--------------------------------
        PASSWORD MANAGER
--------------------------------
(1) Edit Password
(2) Delete Password
(3) Delete Vault
(4) Back
(5) Log Out
'''
        
        print(menu_options)
        option: str = input('Make a selection: ')
        
        if option == '1':
            self.edit_password()
        elif option == '2':
            self.delete_password()
        elif option == '3':
            self.delete_vault()
        elif option == '4':
            self.vault_menu(self.name)
        elif option == '5':
            return 'log out'
        else:
            print('Invalid selection.')
            self.manage_passwords()
    
    # todo - create bulk edit
    def edit_password(self) -> None:
        user_vault: VaultModel = self.repo.get_by_id(self.vault_id)
        
        if len(user_vault.vault) <= 0:
            print('No passwords available.')
            self.manage_passwords()
        
        pass_id: str = input('Enter the ID of the password: ')
        
        target: VaultEntryModel = None

        for entry in user_vault.vault:
            if entry.id == pass_id:
                target = entry
        
        if target is None:
            raise LookupError('Password not found.')
        
        template: str = f'''
===============================
            CURRENT
-------------------------------
id: {target.id}
name: {target.name}
-------------------------------
website: {target.website}
username: {target.login.username}
password: {target.login.password}
===============================
'''
        print(template)
        
        target_copy: VaultEntryModel = target.model_copy(deep=True)
        
        print(f'\nCURRENT NAME: {target.name}')
        target_copy.name = input('(press enter to skip)\nCHANGE NAME: ')
        
        print(f'\nCURRENT WEBSITE: {target.website}')
        target_copy.website = input('(press enter to skip)\nCHANGE WEBSITE: ')
        
        print(f'\nCURRENT USERNAME: {target.login.username}')
        target_copy.login.username = input('(press enter to skip)\nCHANGE USERNAME: ')
        
        print(f'\nCURRENT PASSWORD: {target.login.password}')
        target_copy.login.password = input('(press enter to skip)\nCHANGE PASSWORD: ')
        
        if target_copy.name == '':
            target_copy.name = target.name
        if target_copy.website == '':
            target_copy.website = target.website
        if target_copy.login.username == '':
            target_copy.login.username = target.login.username
        if target_copy.login.password == '':
            target_copy.login.password = target.login.password
            
        changes: str = f'''
===============================
            CHANGES
-------------------------------
id: {target_copy.id}
name: {target_copy.name}
-------------------------------
website: {target_copy.website}
username: {target_copy.login.username}
password: {target_copy.login.password}
===============================
'''
        print(changes)
        confirm: str = input('Confirm changes [y/n]: ')
        
        if confirm == 'y':
            user_vault.vault.remove(target)
            user_vault.vault.append(target_copy)
            updated: bool = self.repo.update_one_where(user_vault, '_id', self.vault_id)
            
            if not updated:
                raise SystemError('Update failed; Please try again later.')
            
        self.manage_passwords()
        
    # todo - create bulk delete
    def delete_password(self) -> None:
        user_vault: VaultModel = self.repo.get_by_id(self.vault_id)
        
        if len(user_vault.vault) <= 0:
            print('No passwords available to delete.')
            self.manage_passwords()
        
        delete_id: str = input('Password ID: ')
        
        if delete_id == '':
            raise ValueError('User did not enter an id.')
        
        for entry in user_vault.vault:
            if entry.id == delete_id:
                user_vault.vault.remove(entry)
            
        self.repo.update_one_where(user_vault, '_id', self.vault_id)
        
        self.manage_passwords()
        
    # todo - create test case
    def delete_vault(self) -> None:
        confirm: str = input('Please confirm that you would like to delete the entire vault and all passwords within the vault [CONFIRM/DENY]: ')
        
        if confirm.upper() == 'CONFIRM':
            deleted = self.repo.delete_one_where('_id', self.vault_id)
            
            if not deleted:
                raise SystemError('Ran into an error deleting the vault.')
            
        
    def logout(self) -> None:
        self.vault_id = None