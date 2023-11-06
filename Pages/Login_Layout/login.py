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
        body = ft.Row([
                ft.Column(controls=[
                    # Welcome text
                    ft.Text('¡Bienvenido!',size=24, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center', width=450),

                    self.username_entry, # username entry
                    self.password_entry, # password entry
                    # forget credentials text button
                    ft.Row(controls=[
                        ft.Container(height=20, width=200,padding=ft.padding.only(left=0), content=fg_credentials, on_click= lambda e: self.recover_credentials()),
                        ft.Container(height=20, width=200,padding=ft.padding.only(left=0), content=register, on_click= lambda e: self.register()),
                    ], spacing=70, alignment=ft.MainAxisAlignment.CENTER),

                    self.button, # login button

                ],alignment=ft.MainAxisAlignment.CENTER)
        ],alignment=ft.MainAxisAlignment.CENTER)

        # Create the container for the layout
        self.layout = ft.Container(content=body,width=720, height=300, border_radius=20, animate_opacity=300, opacity=0)

        #['#22c1c3','#6c2dfd']


        #* ------------------ Background ------------------ *#
        background = ft.Stack(expand=True, controls=[
                ft.Container(expand=True, bgcolor='#D7D9EE', gradient=ft.LinearGradient(colors=['#ae13ff','#5a40fc'], begin=ft.alignment.bottom_left, end=ft.alignment.bottom_right)),
                ft.Row(controls=[
                    ft.Column([
                        # Add the Layout to the background
                        ft.Container(content=self.layout,bgcolor='#F2F4FA', width=550, height=300, border_radius=25),
                    ],alignment=ft.MainAxisAlignment.CENTER)
                ],alignment=ft.MainAxisAlignment.CENTER)
            ])

        # Add the background to the page
        self.page.add(background)

        # animacion de opacidad al entrar
        self.animate()


    #* ------------------ Class Functions ------------------ *#
    def validate(self):
        '''Validate the credentials'''
        if self.username_entry.value == 'admin' and self.password_entry.value == 'admin': # Validate the credentials
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
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()

        time.sleep(0.25)

        self.page.remove(self.page.controls[0])
        FgCredentials(self.page) # Create the layout to recover the credentials

    def register(self):
        '''Register a new user'''
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()

        time.sleep(0.25)

        self.page.remove(self.page.controls[0])
        Register(self.page)

    def log(self):
        '''Log in to the system'''
        self.button.text = 'Cargando...'
        self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
        self.button.disabled = True
        self.page.update()
        time.sleep(0.5)
        self.button.text = 'Iniciar Sesion'
        self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
        self.button.disabled = False
        self.page.update()
        self.page.remove(self.page.controls[0])
        AppLayout(self.page) # Create the layout to recover the credentials

    def animate(self):
        '''Animate the layout'''
        time.sleep(0.1)
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()
