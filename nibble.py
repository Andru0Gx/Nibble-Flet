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
import time
import flet as ft

# Modules
from modules.cal import FletCalendar

#* ---------------------------------------------------- Functions

# return to the previous page
def back(page: ft.Page, new_page: ft.Page):
    '''Return to the previous page'''
    page.remove(page.controls[0])
    new_page(page)

def back_container(container: ft.Container, new_page: ft.Page):
    '''Create a container with a back button'''
    button = container

    def hover(e):
        '''Change the color of the button when the mouse is over it'''
        e.control.bgcolor = '#817aa7' if e.data == "true" else '#F2F4FA'
        e.control.update()

    button = ft.Container(
        content=ft.Image('assets/back.png', width=50, height=50, scale=0.5,color='#2c293d'),
        width=35,
        height=35,
        bgcolor='#F2F4FA',
        border_radius=25,
        on_click= lambda e: back(container, new_page), on_hover= hover)

    return button

#* ---------------------------------------------------- Classes
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


#^ ------------------ REGISTER ------------------ ^#

class Register:
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
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.update()

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
        body = ft.Row([
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

        # Create the container for the layout
        self.layout = ft.Container(content=body,width=720, height=300, border_radius=20, animate_opacity=300, opacity=0)

        #* ------------------ Background ------------------ *#
        background = ft.Stack(expand=True, controls=[
                ft.Container(expand=True, bgcolor='#D7D9EE', gradient=ft.LinearGradient(colors=['#ae13ff','#5a40fc'], begin=ft.alignment.bottom_left, end=ft.alignment.bottom_right)),
                ft.Row(controls=[
                    ft.Column([
                        ft.Container(content=self.layout,bgcolor='#F2F4FA', width=550, height=550, border_radius=25),
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
        if self.username_entry.value != '' and self.password_entry.value != '' and self.email_entry.value != '' and self.question1.value != '' and self.question2.value != '' and self.question3.value != '': # Validate the credentials
            self.save_data()
            self.button.text = 'Cargando...'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()
            time.sleep(1)
            self.button.text = 'Registrarse'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()
            self.page.remove(self.page.controls[0])
            Login(self.page)
        else:   # Validate if the fields are empty
            self.button.text = 'Rellene todos los campos'
            self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            self.page.update()
            time.sleep(2)
            self.button.text = 'Registrarse'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.page.update()

    def animate(self):
        '''Animate the layout'''
        time.sleep(0.1)
        self.layout.opacity = 0 if self.layout.opacity == 1 else 1
        self.layout.update()

    def save_data(self):    #TODO - ADD THE MODULE TO SAVE THE DATA IN THE DATABASE
        '''Save the data to the database'''


class AppLayout:
    ''' AppLayout
    
    Sections:
    - Header
    - Sidebar
    - Body

    Header:
    - Logo
    - Name
    - Button to logout
    
    Sidebar:
    - Button to show the home
    - Button to show the students
    - Button to show the teachers
    - Button to show the subjects
    - Button to show the schedules
    - Button to show the grades
    - Button to show the settings

    Body:
    - Container to show the content
    '''

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.update()

        #* ------------------ Variables ------------------ *#

        #* ------------------ Header ------------------ *#

        # Create the logo
        logo = ft.Container(height=80, width=150, content=ft.Image('assets/Nibble-Logo-2.png'), padding=ft.padding.all(20))

        # Create the name
        name = ft.Text('Unidad Educativa "Salvador Garmendia Grateron"', size=40, color='#4B4669', font_family='Helvetica', text_align='center', italic=True)

        # Create the button to logout
        logout = ft.Container(height=80, width=150, content=ft.Icon(ft.icons.LOGOUT, color='#4B4669', size=30), padding=ft.padding.all(20), on_click= lambda e: self.logout())

        header = ft.AppBar(
            title=name,
            center_title=True,
            leading=logo,
            leading_width=150,
            actions=[logout],
            bgcolor='#e9ebf6',
            toolbar_height=80,
        )

        #* ------------------ Sidebar ------------------ *#
        # Create the sidebar

        home = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.HOME_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.HOME_ROUNDED, size=40),
            label_content=ft.Text('Inicio', color='#4B4669'),
        )

        students = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.PERSON_OUTLINE, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.PERSON, size=40),
            label_content=ft.Text('Estudiantes', color='#4B4669'),
        )

        teachers = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.PERSON_4_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.PERSON_4, size=40),
            label_content=ft.Text('Profesores', color='#4B4669'),
        )

        schedules = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.SCHEDULE_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.SCHEDULE, size=40),
            label_content=ft.Text('Horarios', color='#4B4669'),
        )

        grades = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.BOOK, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.BOOK, size=40),
            label_content=ft.Text('Calificaciones', color='#4B4669'),
        )

        settings = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.SETTINGS, size=40),
            label_content=ft.Text('Configuracion', color='#4B4669'),
        )

        sidebar = ft.NavigationRail(
            selected_index=0,
            destinations=[home, students, teachers, schedules, grades, settings],
            bgcolor='#e9ebf6',
            min_width=100,
            width=200,
            label_type=ft.NavigationRailLabelType.SELECTED,
            extended=True,
            on_change= lambda e: self.change_page(e.control.selected_index),
        )

        #* ------------------ Body ------------------ *#
        self.body = ft.Container(expand=True, bgcolor='#F2F4FA', border=ft.Border(top=ft.BorderSide(color='#c2c9db', width=2), left=ft.BorderSide(color='#c2c9db', width=1)))

        #* ------------------ Layout ------------------ *#
        # header
        layout = ft.Row(controls=[
            sidebar,
            self.body,
        ],expand=True, spacing=0)

        # Add the layout to the page
        self.page.add(header, layout)

        # Change the page
        self.change_page(0)

    #* ------------------ Class Functions ------------------ *#
    def animate(self):
        '''Animate the layout'''
        time.sleep(0.1)
        self.body.opacity = 0 if self.body.opacity == 1 else 1
        self.body.update()

    def change_page(self, e): #TODO - ADD THE MODULE TO CHANGE THE PAGE (CLASS)
        '''Change the page'''
        self.animate()

        if e == 0:
            self.body.content = Home(self.page)
        elif e == 1:
            self.body.content = ft.Container(content=ft.Text('Students', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 2:
            self.body.content = ft.Container(content=ft.Text('Teachers', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 3:
            self.body.content = ft.Container(content=ft.Text('Schedules', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 4:
            self.body.content = ft.Container(content=ft.Text('Grades', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 5:
            self.body.content = ft.Container(content=ft.Text('Settings', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')

        self.animate()

    def logout(self):
        '''Logout from the system'''
        self.page.remove(self.page.controls[0], self.page.controls[1])
        Login(self.page)

class Home(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        #* ------------------ Layout ------------------ *#
        events = ft.TextButton(text='Eventos', width=100, height=30, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.events(), top=55, left=500)

        # Create the layout
        layout = ft.Row(controls=[
            ft.Column(controls=[
                ft.Stack(controls=[
                FletCalendar(self.page),
                events

                ]),
                ft.Container(height=100, width=1100, bgcolor='red', border_radius=20, padding=ft.padding.all(20), content=ft.Text('EVENTOS', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center')),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment='center')
        ], alignment=ft.MainAxisAlignment.CENTER)



        self.content = layout
        self.update()

    def build(self):
        return self.content













#TODO - Create Modules for the windows

#^ ------------------ RUN APP ------------------ ^#
def main(page: ft.Page):
    '''Main function to run the app'''
    page.title = 'Nibble'
    page.window_maximized = True
    page.padding = 0
    page.window_resizable = False
    page.window_maximizable = False

    page.update()
    Login(page)
    # AppLayout(page)

ft.app(target=main)
