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

    # Theme for the scrollbar
    page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                thickness=10,
                thumb_visibility=True,
                thumb_color={
                    ft.MaterialState.DEFAULT: '#9a96bc',
                    ft.MaterialState.HOVERED: '#817aa7',
                },
            ),
        )

    # page.window_min_height = 768
    # page.window_min_width = 1366

    db()
    page.update()
    # pm.def_app_layout(page)
    pm.def_login(page)


ft.app(target=main)
