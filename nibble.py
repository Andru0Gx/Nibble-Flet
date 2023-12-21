'''
nibble.py
========================
Data management system for a school

Requires the installation of the following libraries:
- Flet
- Time

Author: Andru0Gx
Date: 26/10/2023
'''

# Disable the pylint warnings
# pylint: disable=W0201

# Libraries
import flet as ft

# Pages
# from modules.page_manager import def_login as Login
import modules.page_manager as pm

# Database
from DB.Functions.tables import create_tables as db


#^ ------------------ RUN APP ------------------ ^#

#TODO - Add Maximized window True
#TODO - cambiar los botones de editar por guardar
def main(page: ft.Page):
    '''Main function to run the app'''
    page.title = 'Nibble'
    # page.window_maximized = True
    page.padding = 0
    page.theme_mode = 'Light'
    page.window_resizable = False
    page.window_maximizable = False
    page.window_height = 768
    page.window_width = 1366

    page.update()
    pm.def_app_layout(page)
    # pm.def_login(page)

    db()

ft.app(target=main)
