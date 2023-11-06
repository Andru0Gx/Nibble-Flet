'''Forget Credentials Layout'''

# Disable the pylint warnings
# pylint: disable=W0201

# Libraries
import time
import flet as ft

# Modules
from modules.back_button import back_container

# pages
from modules.page_manager import def_login as Login

#^ ------------------ FG CREDENTIALS ------------------ ^#

class FgCredentials:
    ''' Forgotten Credentials Layout

    Sections:
    - Button to recover the username
    - Button to recover the password
    '''
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.page.update()

        #* ------------------ Layout ------------------ *#
        body = ft.Row([
            ft.Column( spacing=20,controls=[
                    ft.Row(controls=[
                        back_container(self.page, Login),
                        ft.Container(height=35,width=400, content=ft.Text('He Olvidado mi', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                    ]),

                    ft.TextButton(text='Usuario', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.user()),

                    ft.TextButton(text='Contraseña', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.password()),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment='center')
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Create the container for the layout
        self.layout = ft.Container(content=body,width=720, height=300, border_radius=20, animate_opacity=300, opacity=0)

        #* ------------------ Background ------------------ *#
        background = ft.Stack(expand=True, controls=[
                ft.Container(expand=True, bgcolor='#D7D9EE', gradient=ft.LinearGradient(colors=['#ae13ff','#5a40fc'], begin=ft.alignment.bottom_left, end=ft.alignment.bottom_right)),
                ft.Row(controls=[
                    ft.Column([
                        ft.Container(content=self.layout,bgcolor='#F2F4FA', width=550, height=300, border_radius=25),
                    ],alignment=ft.MainAxisAlignment.CENTER)
                ],alignment=ft.MainAxisAlignment.CENTER)
            ])
        self.page.add(background)


        # animacion de opacidad al entrar
        time.sleep(0.1)
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()



    #* ------------------ Class Functions ------------------ *#
    def user(self):
        '''Recover the username'''
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()

        self.page.remove(self.page.controls[0])
        Forget(self.page, password=False)

    def password(self):
        '''Recover the password'''
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()

        self.page.remove(self.page.controls[0])
        Forget(self.page, password=True)



#^ ------------------ FORGET ------------------ ^#
class Forget:
    '''Forget Layout

    Sections:
    - Validation Code Entry
    - Change layout to Security Questions
    - Change layout to Email
    - Security Questions Entry
    - Password Entry
    - Button to change the password
    '''
    def __init__(self, page: ft.Page, password: bool):
        super().__init__()
        self.page = page
        self.page.update()

        #* ------------------ Variables Layout1 ------------------ *#
        text = 'Se ha enviado un codigo a tu cuenta de correo electronico\npor favor ingresa el codigo de verificacion para continuar, \nrecuerda revisar tu bandeja de spam.'

        # Create the text content
        self.text = ft.Text(text, size=15, color='#4B4669', font_family='Arial', text_align='center')

        # Create the text content to change the layout
        self.change_method = ft.Container(height=20, width=450,padding=ft.padding.only(left=0), content=ft.Text('No puedes acceder a tu correo?', size=15, color='#4B4669', font_family='Arial', text_align='start'), on_click= lambda e: self.change_layout(password))

        # Create the Entry for the validation code
        self.code = ft.TextField(
                    width=450,
                    height=50,
                    label='Codigo de Verificacion',
                    hint_text='Ingresa tu Codigo',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                )

        # Create the button to login
        self.button = ft.TextButton(text='Verificar', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.validate_code(password))


        #* ------------------ Layout1 ------------------ *#
        # Create the layout
        self.body_layout1 =ft.Column(controls=[
                        ft.Row(controls=[
                            back_container(self.page, FgCredentials),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Codigo De Verificacion', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        self.text,
                        self.code,
                        self.change_method,
                        self.button,

                    ],horizontal_alignment='center', alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        #* ------------------ Variables Layout 2 ------------------ *#

        # Security Questions
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

        #* ------------------ Layout2 ------------------ *#

        self.body_layout2 = ft.Column(controls=[
                        ft.Row(controls=[
                            back_container(self.page, FgCredentials),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Preguntas de Seguridad', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        self.question1,
                        self.question2,
                        self.question3,
                        self.change_method,
                        self.button,
                    ],horizontal_alignment='center', alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        # Create the container for the layout
        self.layout = ft.Container(content=self.body_layout1,width=720, height=300, border_radius=20, animate_opacity=300, opacity=0)


        #* ------------------ Background ------------------ *#
        self.container = ft.Container(content=self.layout,bgcolor='#F2F4FA', width=550, height=300, border_radius=25, animate_size=300)

        # Create the background
        self.background = ft.Stack(expand=True, controls=[
                ft.Container(expand=True, bgcolor='#D7D9EE', gradient=ft.LinearGradient(colors=['#ae13ff','#5a40fc'], begin=ft.alignment.bottom_left, end=ft.alignment.bottom_right)),
                ft.Row(controls=[
                    ft.Column([
                        self.container,
                    ],alignment=ft.MainAxisAlignment.CENTER)
                ],alignment=ft.MainAxisAlignment.CENTER)
            ])
        self.page.add(self.background)

        # animacion de opacidad al entrar
        time.sleep(0.1)
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()


        #send code
        self.send_code = self.email_code()

    #* ------------------ Class Functions ------------------ *#

    def change_layout(self, password):
        '''Change the layout to Email'''

        if self.layout.content == self.body_layout1:
            self.layout.content = self.body_layout2
            self.change_method.content = ft.Text('Enviar codigo de verificacion', size=15, color='#4B4669', font_family='Arial', text_align='start')
            self.button.on_click = lambda e: self.validate_questions(password)
        elif self.layout.content == self.body_layout2:
            self.layout.content = self.body_layout1
            self.change_method.content = ft.Text('No puedes acceder a tu correo?', size=15, color='#4B4669', font_family='Arial', text_align='start')
            self.button.on_click = lambda e: self.validate_code(password)

        self.layout.update()

    def email_code(self): #TODO - ADD THE MODULE TO SEND THE CODE TO THE EMAIL
        '''Function to send the code to the email'''
        code = generate_code()
        correo = get_email()
        if send_mail(correo, code):
            print('Correo enviado con éxito')
        else:
            print('No conectado a internet')
        return code

    def validate_questions(self, next_page):
        '''Validate the questions'''
        if self.question1.value != '' and self.question2.value != '' and self.question3.value != '':
            if self.question1.value == 'rojo' and self.question2.value == 'pizza' and self.question3.value == 'perro':
                self.button.text = 'Cargando...'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()

                # Change the layout
                if next_page:
                    self.change_password()
                else:
                    self.show_username()
            else:
                self.button.text = 'Respuestas Incorrectas'
                self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.page.update()
                time.sleep(2)
                self.button.text = 'Verificar'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()
        else:
            self.button.text = 'Rellene todos los campos'
            self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            self.page.update()
            time.sleep(2)
            self.button.text = 'Verificar'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()

    def validate_code(self, next_page):
        '''Validate the code'''

        code = self.code.value
        valid = True
        for letter in code: # Validate if the code is a number
            if letter.isalpha(): # Validate if the code is a number
                self.button.text = 'Codigo Invalido'
                self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.page.update()
                time.sleep(2)
                self.button.text = 'Verificar'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()
                valid = False
                break
        if valid: # Validate if the code is correct
            if self.code.value != '': # Validate if the field is empty
                received_code = self.code.value
                received_code = int(received_code)
                if received_code == self.send_code: # Validate if the code is correct
                    self.button.text = 'Cargando...'
                    self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                    self.page.update()

                    # Change the layout
                    if next_page:
                        self.change_password()
                    else:
                        self.show_username()

                else: # Validate if the code is incorrect
                    self.button.text = 'Codigo Incorrecto'
                    self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                    self.page.update()
                    time.sleep(2)
                    self.button.text = 'Verificar'
                    self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                    self.page.update()
            else: # Validate if the field is empty
                self.button.text = 'Campo Vacio'
                self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.page.update()
                time.sleep(2)
                self.button.text = 'Verificar'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()

    def change_password(self):
        '''Change the password'''
        password_entry = ft.TextField(
                    width=450,
                    height=50,
                    label='Nueva Contraseña',
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

        password_entry2 = ft.TextField(
                    width=450,
                    height=50,
                    label='Confirmar Contraseña',
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

        self.button2 = ft.TextButton(text='Cambiar Contraseña', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.validate_password(password_entry, password_entry2))

        #* ------------------ Layout ------------------ *#
        body = ft.Column(controls=[
                        ft.Row(controls=[
                            back_container(self.page, FgCredentials),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Cambiar Contraseña', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        password_entry,
                        password_entry2,
                        self.button2,
                    ],horizontal_alignment='center', alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        self.layout.content = body
        self.layout.update()

    def validate_password(self, password_entry, password_entry2):
        '''Validate the password'''

        if password_entry.value != '' and password_entry2.value != '':
            if password_entry.value == password_entry2.value:
                self.button2.text = 'Cargando...'
                self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()
                time.sleep(1)
                self.button2.text = 'Cambiar Contraseña'
                self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()
                self.page.remove(self.page.controls[0])
                Login(self.page)
                #TODO - ADD THE MODULE TO CHANGE THE PASSWORD
            else:
                self.button2.text = 'Las contraseñas no coinciden'
                self.button2.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.page.update()
                time.sleep(2)
                self.button2.text = 'Cambiar Contraseña'
                self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.page.update()
        else:
            self.button2.text = 'Rellene todos los campos'
            self.button2.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            self.page.update()
            time.sleep(2)
            self.button2.text = 'Cambiar Contraseña'
            self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()

    def show_username(self):
        '''Show the username'''
        username = 'admin' #TODO - ADD THE MODULE TO GET THE USERNAME

        def home():
            '''Return to the Login page'''
            self.page.remove(self.page.controls[0])
            Login(self.page)

        # boton continuar
        button = ft.TextButton(text='Continuar', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: home())

        #* ------------------ Layout ------------------ *#
        body = ft.Column(controls=[
                        ft.Row(controls=[
                            back_container(self.page, FgCredentials),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Mostrar Usuario', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text('Tu Usuario es: ' + username, size=15, color='#4B4669', font_family='Arial', text_align='center'),
                        button,
                    ],horizontal_alignment='center', alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        self.layout.content = body
        self.layout.update()
