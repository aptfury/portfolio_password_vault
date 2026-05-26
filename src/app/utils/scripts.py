""" scripts.py

AUTHOR: Blake Lemarr
CREATED: 05.22.26
UPDATED: 05.26.26

DESCRIPTION: The different scripts used throughout the program

UPDATES:
    - [05.22.26] Created first few scripts
    - [05.26.26] Updating template scripts
    
DEPENDENCIES:
    - Name

"""

# -------------------- SCRIPTS -------------------- #
class ScriptsUtil:
    def main_menu(self):
        script: list[str] = [
            '\n-------------------------------',
            '           MAIN MENU           ',
            '-------------------------------',
            '(1) Log In                     ',
            '(2) Create Account             ',
            '(3) Exit                       ',
            '-------------------------------'
        ]
        return script
    
    def account_menu(self):
        script: list[str] = [
            '\n----------------------------------',
            '           ACCOUNT MENU           ',
            '----------------------------------',
            '(1) Access Vault                  ',
            '(2) View Account                  ',
            '(3) Update Account                ',
            '(4) Delete Account                ',
            '(5) Log Out to Main Menu          ',
            '(6) Log Out and Exit              ',
            '----------------------------------'
        ]
        return script
    
    def vault_menu(self):
        script: list[str] = [
            '\n--------------------------------',
            '           VAULT MENU           ',
            '--------------------------------',
            '(1) Add Password                ',
            '(2) Find Password               ',
            '(3) View Passwords              ',
            '(4) Back to Account Menu        ',
            '(5) Log Out to Main Menu        ',
            '(6) Log Out and Exit            ',
            '--------------------------------'
        ]
        return script
    
    def password_menu(self):
        script: list[str] = [
            '\n-----------------------------------',
            '           PASSWORD MENU           ',
            '-----------------------------------',
            '(1) Update Password                ',
            '(2) Delete Password                ',
            '(3) Back to Vault                  ',
            '(5) Log Out to Main Menu           ',
            '(6) Log Out and Exit               ',
            '-----------------------------------'
        ]
        return script
    
    def passwords_menu(self):
        script: list[str] = [
            '\n-----------------------------------',
            '           PASSWORD MENU           ',
            '-----------------------------------',
            '(1) Update Password                ',
            '(2) Delete Password                ',
            '(3) Next Password                  ',
            '(4) Previous Password              ',
            '(5) Back to Vault                  ',
            '(6) Log Out to Main Menu           ',
            '(7) Log Out and Exit               ',
            '-----------------------------------'
        ]
        return script
    
    def menu_selection(self):
        script: list[str] = [
            '\nEnter the number of the option you would like to select.',
            'ENTER SELECTION: '
        ]
        return script
    
    def account_template(self, account):
        script: list[str] = [
            '\n-----------------------------------',
            '           ACCOUNT  INFO           ',
            '-----------------------------------',
            f'USERNAME: {account.username}       ',
            f'EMAIL: {account.email}             ',
            '-----------------------------------',
            '              OPTIONS              ',
            '-----------------------------------',
            '(1) Edit                           ',
            '(2) Delete (Permanent)             ',
            '(3) Back                           ',
            '-----------------------------------'
        ]
        return script
    
    def password_template(self, password, reveal: bool = False):
        user_pass: str = password.password if reveal else ('*' * len(password.password))
        script: list[str] = [
            
            '\n-----------------------------------',
            '           PASSWORD INFO           ',
            '-----------------------------------',
            f'ID: {password.id}                  ',
            f'WEBSITE: {password.website}        ',
            f'USERNAME: {password.username}      ',
            f'PASSWORD: {user_pass}              ',
            '-----------------------------------',
            '              OPTIONS              ',
            '-----------------------------------',
            '(1) Edit                           ',
            '(2) Delete                         ',
            '(3) Back                           ',
            '-----------------------------------'
        ]
        return script