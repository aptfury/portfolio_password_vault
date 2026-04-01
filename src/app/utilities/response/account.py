def welcome_authenticated_user(username):
    return f'Welcome back, {username}!'

account_menu: str = '''
What would you like to do?
    (1) Retrieve Password
    (2) Add Password
    (3) Edit Password
    (4) Delete Password
    (5) Update Account
    (6) Back to Main Menu
    (7) Help
    (8) Exit
'''

back_to_main_menu: str = 'Returning to main menu...\n'