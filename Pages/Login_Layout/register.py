'''Register Layout'''

# Disable the pylint warnings
# pylint: disable=W0201

# libraries
import time
import flet as ft

# Modules
from modules.back_button import back_container

# Pages
from modules.page_manager import def_login as Login

# Database
from DB.Functions.user_db import save_user as save

#^ ------------------ REGISTER ------------------ ^#

class Register(ft.UserControl):
    '''Register Layout

    Sections:
    - Entry for the username
    - Entry for the password
    - Entry for the email
    - Entry for the security question1
    - Entry for the security question2
    - Entry for the security question3
    - Button to register
    - Button to return to Login
    '''
    def __init__(self, page: ft.Page, parent):
        super().__init__()
        self.page = page
        self.page.update()
        self.parent = parent
        self.parent.height = 550

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

        # Create the Entry for the email
        self.email_entry = ft.TextField(
                    width=450,
                    height=50,
                    label='Correo Electronico',
                    hint_text='Ingresa tu Correo Electronico',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )

        # Create the Entry for the security question1
        self.question1 = ft.TextField(
                    width=450,
                    height=50,
                    label='Cual es tu color favorito',
                    hint_text='Ingresa tu respuesta',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )

        # Create the Entry for the security question2
        self.question2 = ft.TextField(
                    width=450,
                    height=50,
                    label='Cual es tu comida favorita',
                    hint_text='Ingresa tu respuesta',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )

        # Create the Entry for the security question3
        self.question3 = ft.TextField(
                    width=450,
                    height=50,
                    label='Cual es tu animal favorito',
                    hint_text='Ingresa tu respuesta',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )

        # Create the button to register
        self.button = ft.TextButton(text='Registrarse', width=450, height=41, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.validate())

        #* ------------------ Layout ------------------ *#
        self.body = ft.Row([
                ft.Column(controls=[
                    ft.Row(controls=[
                        back_container(self.page, Login),
                        ft.Container(height=35,width=400, content= ft.Text('Registrarse',size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center', width=450))
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    self.username_entry, # username entry
                    self.password_entry, # password entry
                    self.email_entry, # email entry
                    self.question1, # question1 entry
                    self.question2, # question2 entry
                    self.question3, # question3 entry
                    self.button, # register button
                ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment='center')
        ],alignment=ft.MainAxisAlignment.CENTER)

        # add the layout to the page
        self.content = self.body

    def build(self):
        return self.content

    #* ------------------ Class Functions ------------------ *#
    def validate(self):
        '''Validate the credentials'''
        page = self.page
        if self.username_entry.value != '' and self.password_entry.value != '' and self.email_entry.value != '' and self.question1.value != '' and self.question2.value != '' and self.question3.value != '': # Validate the credentials
            self.save_data()
            self.button.text = 'Cargando...'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.body.update()
            time.sleep(0.5)
            self.button.text = 'Registrarse'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.body.update()
            page.remove(page.controls[0])
            Login(page)
        else:   # Validate if the fields are empty
            self.button.text = 'Rellene todos los campos'
            self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            self.body.update()
            time.sleep(2)
            self.button.text = 'Registrarse'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.body.update()

    def save_data(self):    #TODO - ADD THE MODULE TO SAVE THE DATA IN THE DATABASE
        '''Save the data to the database'''
        save(
            self.username_entry.value,
            self.password_entry.value,
            self.email_entry.value,
            self.question1.value,
            self.question2.value,
            self.question3.value
            )
