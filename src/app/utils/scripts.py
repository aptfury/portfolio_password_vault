""" scripts.py

AUTHOR: Blake Lemarr
CREATED: 05.22.26
UPDATED: 05.22.26

DESCRIPTION: The different scripts used throughout the program

UPDATES:
    - [05.22.26] Created first few scripts
    
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
        script: list[str] = []
        return script
    
    def password_template(self, password):
        script: list[str] = []
        return script