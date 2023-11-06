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


#^ ------------------ RUN APP ------------------ ^#

def main(page: ft.Page):
    '''Main function to run the app'''
    page.title = 'Nibble'
    page.window_maximized = True
    page.padding = 0
    page.window_resizable = False
    page.window_maximizable = False

    page.update()
    # Login(page)
    pm.def_app_layout(page)

ft.app(target=main)
