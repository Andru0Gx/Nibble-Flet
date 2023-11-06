'''Manager Windows'''

import flet as ft

def def_login(page: ft.Page):
    '''Create the login page'''
    from Pages.Login_Layout.login import Login
    Login(page)

def def_register(page: ft.Page):
    '''Create the register page'''
    from Pages.Login_Layout.register import Register
    Register(page)

def def_forget_credentials(page: ft.Page):
    '''Create the forget credentials page'''
    from Pages.Login_Layout.fg_credentials import FgCredentials
    FgCredentials(page)

def def_app_layout(page: ft.Page):
    '''Create the app layout page'''
    from Pages.App_Layout.app_layout import AppLayout
    AppLayout(page)
