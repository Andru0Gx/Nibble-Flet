'''Forget Credentials Layout'''

# Disable the pylint warnings
# pylint: disable=W0201

# Libraries
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
import socket

import time
import flet as ft


# Modules
from modules.back_button import back_container

# pages
from modules.page_manager import def_login as Login

# Database
from DB.Functions.user_db import get_user as get_credentials
from DB.Functions.user_db import update_user as update_credentials

#^ ------------------ FG CREDENTIALS ------------------ ^#

class FgCredentials(ft.UserControl):
    ''' Forgotten Credentials Layout

    Sections:
    - Button to recover the username
    - Button to recover the password
    '''
    def __init__(self, page:ft.Page, parent):
        super().__init__()
        self.page = page
        self.page.update()
        self.parent = parent

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

        # add the layout to the page
        self.content = body

    def build(self):
        return self.content

    #* ------------------ Class Functions ------------------ *#
    def user(self):
        '''Recover the username'''
        self.parent.content = Forget(self.page, password=False, parent=self.parent)
        self.parent.update()

    def password(self):
        '''Recover the password'''
        self.parent.content = Forget(self.page, password=True, parent=self.parent)
        self.parent.update()



#^ ------------------ FORGET ------------------ ^#
class Forget(ft.UserControl):
    '''Forget Layout

    Sections:
    - Validation Code Entry
    - Change layout to Security Questions
    - Change layout to Email
    - Security Questions Entry
    - Password Entry
    - Button to change the password
    '''
    def __init__(self, page: ft.Page, password: bool, parent):
        super().__init__()
        self.page = page
        self.parent = parent

        self.credentials = get_credentials()

        #* ------------------ Variables Layout1 ------------------ *#
        text = 'Se ha enviado un codigo a tu cuenta de correo electronico\npor favor ingresa el codigo de verificacion para continuar, \nrecuerda revisar tu bandeja de spam.'

        # Create the text content
        self.text = ft.Text(text, size=15, color='#4B4669', font_family='Arial', text_align='center')

        # Create the text content to change the layout
        self.change_method = ft.Container(height=20, width=225,padding=ft.padding.only(left=0), content=ft.Text('Preguntas de Seguridad', size=15, color='#4B4669', font_family='Arial', text_align='start'), on_click= lambda e: self.change_layout(password))

        self.resend = ft.Container(height=20, width=225,padding=ft.padding.only(left=0), content=ft.Text('Reenviar codigo', size=15, color='#4B4669', font_family='Arial', text_align='start'), on_click= lambda e: self.send_mail())

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
                            back_container(self.page, FgCredentials, self.parent),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Codigo De Verificacion', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        self.text,
                        self.code,
                        ft.Row(controls=[
                            self.change_method,
                            self.resend,
                        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
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
                            back_container(self.page, FgCredentials, self.parent),
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
        self.layout = ft.Container(content=self.body_layout1,width=720, height=300, border_radius=20)

        self.send_mail()

        # add the layout to the page
        self.content = self.layout

    def build(self):
        return self.content

    #* ------------------ Class Functions ------------------ *#

    def change_layout(self, password):
        '''Change the layout to Email'''

        if self.layout.content == self.body_layout1:
            self.layout.content = self.body_layout2
            self.change_method.content = ft.Text('Enviar codigo de verificacion', size=15, color='#4B4669', font_family='Arial', text_align='start')
            self.change_method.width = 450
            self.button.on_click = lambda e: self.validate_questions(password)
        elif self.layout.content == self.body_layout2:
            self.layout.content = self.body_layout1
            self.change_method.content = ft.Text('Preguntas de Seguridad', size=15, color='#4B4669', font_family='Arial', text_align='start')
            self.change_method.width = 225
            self.button.on_click = lambda e: self.validate_code(password)

        self.layout.update()
        self.parent.update()

    def wifi_verification(self):
        '''Check if the user is connected to the internet.'''
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except:
            pass
        return False

    def send_mail(self):
        '''Send mail with code to verify the user's email address.'''
        codigo = random.randint(100000, 999999)
        self.send_code = codigo

        correo = self.credentials['email']

        if self.wifi_verification():
            message = MIMEMultipart('plain')
            message['From'] = 'SC.Nibble@outlook.com'
            message['To'] = correo
            message['Subject'] = 'Código de verificación para Nibble'

            text = f" Estimado/a {correo},\n\nEspero que este correo te encuentre bien. En relación a tu solicitud de verificación en Nibble, nos complace proporcionarte el código de verificación necesario para completar el proceso de autenticación.\n\nCódigo de verificación: {codigo}\n\nPor favor, ten en cuenta que este código es confidencial y solo debe ser utilizado para el propósito de verificación en Nibble. No compartas este código con nadie, ya que podría comprometer la seguridad de tu cuenta.\n\nSi no has solicitado este código de verificación o tienes alguna pregunta o inquietud adicional, te recomendamos ponerse en contacto con nuestro equipo de soporte lo antes posible. Estaremos encantados de ayudarte en lo que necesites.\n\nGracias por confiar en Nibble. Esperamos brindarte una excelente experiencia.\n\nAtentamente,\n\nEl equipo de Nibble"

            message.attach(MIMEText(text, 'plain'))
            smtp = SMTP('smtp.office365.com', 587)
            smtp.starttls()
            smtp.login('SC.Nibble@outlook.com', 'Nibble.1234')
            smtp.sendmail('SC.Nibble@outlook.com', correo, message.as_string())
            smtp.quit()
            return True
        else:
            self.dlg = ft.AlertDialog(
                content=ft.Text('No tienes conexion a internet o se encuentra inestable.\nNota: Puedes usar las preguntas de seguridad.', size=15, color='#4B4669', font_family='Arial', text_align='left'),
                actions=[
                    ft.Row([
                        ft.ElevatedButton(text='Cancelar', style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.close(self.dlg)),
                        ft.ElevatedButton(text='Reintentar', style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.again())
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]
            )
            self.open_dlg(self.dlg)
            return False

    def again(self):
        """
        Retry sending the email with the verification code.

        This method updates the text and state of a dialog box to indicate the status of the email sending process.

        Inputs:
        - None

        Outputs:
        - None
        """

        self.dlg.actions[0].controls[1].text = 'Enviando...'
        self.dlg.actions[0].controls[1].disabled = True
        self.dlg.actions[0].controls[1].update()

        if self.send_mail():
            self.close(self.dlg)
        else:
            self.dlg.actions[0].controls[1].text = 'Envio Fallido'
            self.dlg.actions[0].controls[1].disabled = True
            self.dlg.actions[0].controls[1].update()

            time.sleep(1)

            self.dlg.actions[0].controls[1].text = 'Reintentar'
            self.dlg.actions[0].controls[1].disabled = False
            self.dlg.actions[0].controls[1].update()

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


    def validate_questions(self, next_page):
        '''Validate the questions'''
        if self.question1.value != '' and self.question2.value != '' and self.question3.value != '':
            if self.question1.value == self.credentials['question1'] and self.question2.value == self.credentials['question2'] and self.question3.value == self.credentials['question3']:
                self.button.text = 'Cargando...'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.layout.update()

                # Change the layout
                if next_page:
                    self.change_password()
                else:
                    self.show_username()
            else:
                self.button.text = 'Respuestas Incorrectas'
                self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.layout.update()
                time.sleep(2)
                self.button.text = 'Verificar'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.layout.update()
        else:
            self.button.text = 'Rellene todos los campos'
            self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            self.layout.update()
            time.sleep(2)
            self.button.text = 'Verificar'
            self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            self.layout.update()

    def validate_code(self, next_page):
        '''Validate the code'''

        code = self.code.value
        valid = True
        for letter in code: # Validate if the code is a number
            if letter.isalpha(): # Validate if the code is a number
                self.button.text = 'Codigo Invalido'
                self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.layout.update()
                time.sleep(2)
                self.button.text = 'Verificar'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.layout.update()
                valid = False
                break
        if valid: # Validate if the code is correct
            if self.code.value != '': # Validate if the field is empty
                received_code = self.code.value
                received_code = int(received_code)
                if received_code == self.send_code: # Validate if the code is correct
                    self.button.text = 'Cargando...'
                    self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                    self.layout.update()

                    # Change the layout
                    if next_page:
                        self.change_password()
                    else:
                        self.show_username()

                else: # Validate if the code is incorrect
                    self.button.text = 'Codigo Incorrecto'
                    self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                    self.layout.update()
                    time.sleep(2)
                    self.button.text = 'Verificar'
                    self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                    self.layout.update()
            else: # Validate if the field is empty
                self.button.text = 'Campo Vacio'
                self.button.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                self.layout.update()
                time.sleep(2)
                self.button.text = 'Verificar'
                self.button.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                self.layout.update()

    def change_password(self):
        '''Change the password'''
        parent = self.page
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

        self.button2 = ft.TextButton(text='Cambiar Contraseña', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.validate_password(password_entry, password_entry2, parent))

        #* ------------------ Layout ------------------ *#
        body = ft.Column(controls=[
                        ft.Row(controls=[
                            back_container(self.page, FgCredentials, self.parent),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Cambiar Contraseña', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        password_entry,
                        password_entry2,
                        self.button2,
                    ],horizontal_alignment='center', alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        self.parent.content = body
        self.parent.update()

    def validate_password(self, password_entry, password_entry2, parent):
        '''Validate the password'''

        if password_entry.value != '' and password_entry2.value != '':
            if password_entry.value == password_entry2.value:
                update_credentials(self.credentials['user'], password_entry.value, self.credentials['email'], self.credentials['question1'], self.credentials['question2'], self.credentials['question3'])
                self.button2.text = 'Cargando...'
                self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                parent.update()
                time.sleep(1)
                self.button2.text = 'Cambiar Contraseña'
                self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                parent.update()
                parent.remove(parent.controls[0])
                Login(parent)
            else:
                self.button2.text = 'Las contraseñas no coinciden'
                self.button2.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
                parent.update()
                time.sleep(2)
                self.button2.text = 'Cambiar Contraseña'
                self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
                parent.update()
        else:
            self.button2.text = 'Rellene todos los campos'
            self.button2.style = ft.ButtonStyle(bgcolor='#ff6600', color='#FFFFFF')
            parent.update()
            time.sleep(2)
            self.button2.text = 'Cambiar Contraseña'
            self.button2.style = ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF')
            parent.update()

    def show_username(self):
        '''Show the username'''
        username = self.credentials['user']
        parent = self.page

        def home(page):
            '''Return to the Login page'''
            page.remove(page.controls[0])
            Login(page)

        # boton continuar
        button = ft.TextButton(text='Continuar', width=450, height=50, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: home(parent))

        #* ------------------ Layout ------------------ *#
        body = ft.Column(controls=[
                        ft.Row(controls=[
                            back_container(self.page, FgCredentials, self.parent),
                            ft.Container(height=35,width=400, content=
                                ft.Text('Mostrar Usuario', size=25, weight=ft.FontWeight.BOLD, color='#4B4669', font_family='Arial', text_align='center')),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text('Tu Usuario es: ' + username, size=15, color='#4B4669', font_family='Arial', text_align='center'),
                        button,
                    ],horizontal_alignment='center', alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        self.parent.content = body
        self.parent.update()
