'''Login Layout'''

# Disable the pylint warnings
# pylint: disable=W0201

# Libraries
import time
import flet as ft

# Pages
from modules.page_manager import def_register as Register
from modules.page_manager import def_forget_credentials as FgCredentials
from modules.page_manager import def_app_layout as AppLayout

# Database
from DB.Functions.user_db import block_user as block
from DB.Functions.user_db import get_user as get_credentials

#^ ------------------ LOGIN ------------------ ^#

class Login:
    '''Login Layout
    
    Sections:
    - Entry for the username
    - Entry for the password
    - Button to login
    - Button to recover password
    - Button to register
    '''

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.credentials = get_credentials()

        #* ------------------ Variables ------------------ *#

        # Create the Entry for the username
        self.username_entry = ft.TextField(
                    width=450,
                    height=50,
                    label='Usuario',
                    hint_text='Ingresa tu Usuario',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )
        # Create the Entry for the password
        self.password_entry = ft.TextField(
                    width=450,
                    height=50,
                    label='Contraseña',
                    hint_text='Ingresa tu Contraseña',
                    password=True,
                    can_reveal_password=True,
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )
        # Create the text content to recover password
        fg_credentials = ft.Text('¿Olvidaste tus credenciales?', size=15, color='#4B4669', font_family='Arial', text_align='center')

        # Create the text content to register
        register = ft.Text('¿No tienes cuenta?', size=15, color='#4B4669', font_family='Arial', text_align='center')

        # Create the button to login
        self.button = ft.TextButton(text='Iniciar Sesion', width=450, height=41, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.validate())

        #* ------------------ Layout ------------------ *#
        self.body = ft.Row([
                ft.Column(controls=[
                    # Welcome text
                    ft.Text('¡Bienvenido!',size=24, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center', width=450),
                    self.username_entry, # username entry
                    self.password_entry, # password entry
                    # forget credentials text button
                    ft.Row(controls=[
                        ft.Container(height=20, width=200,padding=ft.padding.only(left=0), content=fg_credentials),
                        ft.Container(height=20, width=200,padding=ft.padding.only(left=0), content=register),
                    ], spacing=70, alignment=ft.MainAxisAlignment.CENTER),

                    self.button, # login button

                ],alignment=ft.MainAxisAlignment.CENTER)
        ],alignment=ft.MainAxisAlignment.CENTER)

        #['#22c1c3','#6c2dfd']

        #* ------------------ Background ------------------ *#
        self.background = ft.Stack(expand=True, controls=[
                ft.Container(expand=True, bgcolor='#D7D9EE', gradient=ft.LinearGradient(colors=['#ae13ff','#5a40fc'], begin=ft.alignment.bottom_left, end=ft.alignment.bottom_right)),
                ft.Row(controls=[
                    ft.Column([
                        # Add the Layout to the background
                        ft.Container(content=self.body,bgcolor='#F2F4FA', width=550, height=300, border_radius=25),
                    ],alignment=ft.MainAxisAlignment.CENTER)
                ],alignment=ft.MainAxisAlignment.CENTER)
            ])

        self.layout = self.background.controls[1].controls[0].controls[0]
        # Add the background to the page
        self.page.add(self.background)

        self.restrict()


    #* ------------------ Class Functions ------------------ *#
    def validate(self):
        '''Validate the credentials'''

        if self.username_entry.value == self.credentials['user'] and self.password_entry.value == self.credentials['password']: # Validate the credentials
            self.log()
        elif self.username_entry.value == '' or self.password_entry.value == '': # Validate if the fields are empty
            self.button.text = 'Rellene todos los campos'
            self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            self.page.update()
            time.sleep(2)
            self.button.text = 'Iniciar Sesion'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()
        else:   # Validate if the credentials are incorrect
            self.button.text = 'Usuario o Contraseña Incorrectos'
            self.button.style = ft.ButtonStyle(bgcolor='#FF0000', color='#FFFFFF')
            self.page.update()
            time.sleep(2)
            self.button.text = 'Iniciar Sesion'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()

    def recover_credentials(self):
        '''Recover the credentials'''
        self.layout.content = FgCredentials(self.page, self.layout) # Create the layout to recover the credentials
        self.layout.update()

    def register(self):
        '''Register a new user'''
        self.layout.content = Register(self.page, self.layout)
        self.layout.update()

    def log(self):
        '''Log in to the system'''
        self.page.remove(self.page.controls[0])
        AppLayout(self.page) # Create the layout to recover the credentials


    def restrict(self):
        '''Restrict the access to the register layout'''

        if block():
            dlg = ft.AlertDialog(
                content=ft.Text('Ya existe un usuario registrado en el sistema'),
                actions=[
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))
                ]
            )
            self.button.on_click = lambda e: self.validate()
            self.body.controls[0].controls[3].controls[1].on_click = lambda e: self.open_dlg(dlg)
            self.body.controls[0].controls[3].controls[0].on_click = lambda e: self.recover_credentials()
            self.layout.update()
        else:

            dlg = ft.AlertDialog(
                content=ft.Text('No existe un usuario registrado en el sistema'),
                actions=[
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))
                ]
            )
            self.button.on_click = lambda e: self.open_dlg(dlg)
            self.body.controls[0].controls[3].controls[1].on_click = lambda e: self.register()
            self.body.controls[0].controls[3].controls[0].on_click = lambda e: self.open_dlg(dlg)
            self.layout.update()



    def open_dlg(self, dlg):
        """
        Open a dialog box in the user interface.

        :param dlg: The dialog box object that needs to be opened.
        :type dlg: object
        """
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close(self, dlg):
        """
        Closes the dialog box by setting its 'open' attribute to False and updating the page.

        Args:
            dlg (Dialog): The dialog box to be closed.

        Returns:
            None
        """
        dlg.open = False
        self.page.update()
