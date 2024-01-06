'''Settings Page'''

# Libraries
import time
import flet as ft

# Database
from DB.Functions.user_db import get_user,update_user
from DB.Functions.phases_db import phase_add, get_phases, delete_phase, update_phase
from DB.Functions.subjects_db import subject_add, get_subjects, delete_subject, update_subject

class Settings(ft.UserControl):
    '''
    
    Settings Page

    Sections:
    - User Change
    - Password Change
    - Database Import/Export
    - Database Reset (Delete all the data)
    - Database Storage (Show the storage of the database in a pie chart or something like that)
    
    '''
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        credentials = get_user()

        #* ------------------ Layout ------------------ *#
        # Create the Title
        title = ft.Text(
            'Configuracion',
            color='#4B4669',
            font_family='Arial',
            width = 1100,
            text_align='center',
            weight='bold',
            size=25,
        )

        #* ------------------ Credentials - Layout ------------------ *#

        # Create the title for the user section
        user_title = ft.Row([
            ft.Icon(ft.icons.SECURITY_SHARP, color='#6D62A1', size=25),

            ft.Text(
                'Credenciales',
                color='#4B4669',
                font_family='Arial',
                width = 110,
                text_align='left',
                weight='bold',
                size=16,
            ),

        ], spacing=10, alignment=ft.MainAxisAlignment.START)

        self.credentials = ft.Container(ft.Column([
            ft.Row([
                ft.Container( # Create the container for the user icon
                    ft.Icon(ft.icons.CIRCLE, color='#3564fc', size=15),
                    width=30,
                    height=30,
                    bgcolor='#f3f4fa',
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10),
                    border_radius=15,
                ),

                ft.TextField( # Create the TextField for the username
                    width=250,
                    height=35,
                    label='Cambiar Usuario',
                    hint_text='Ingresa el nuevo nombre de usuario',
                    value= credentials['user'],
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                ),

                ft.TextField( # Create the TextField for the email
                    width=250,
                    height=35,
                    label='Cambiar Correo',
                    hint_text='Ingresa el nuevo nombre de usuario',
                    value= credentials['email'],
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                ),

                ft.TextField( # Create the TextField for the password
                    width=250,
                    height=35,
                    label='Cambiar Contraseña',
                    hint_text='Ingresa la nueva contraseña',
                    value= credentials['password'],
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                    password=True,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

            ft.Row([
                ft.Container( # Create the container for the user icon
                    ft.Icon(ft.icons.CIRCLE, color='#3564fc', size=15),
                    width=30,
                    height=30,
                    bgcolor='#f3f4fa',
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10),
                    border_radius=15,
                ),

                ft.TextField( # Create the TextField for the security question 1
                    width=250,
                    height=35,
                    label='Cual es tu color favorito?',
                    hint_text='Ingresa la nueva respuesta de seguridad',
                    value= credentials['question1'],
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                    password=True,
                ),

                ft.TextField( # Create the TextField for the security question 2
                    width=250,
                    height=35,
                    label='Cual es tu comida favorita?',
                    hint_text='Ingresa la nueva respuesta de seguridad',
                    value= credentials['question2'],
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                    password=True,
                ),

                ft.TextField( # Create the TextField for the security question 3
                    width=250,
                    height=35,
                    label='Cual es tu animal favorito?',
                    hint_text='Ingresa la nueva respuesta de seguridad',
                    value= credentials['question3'],
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                    password=True,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20), disabled=True)


        self.credentials_buttons = ft.Row([
            # Create the button to save the username / password
            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.save_credentials(),
                border_radius=15,
                visible=False,
            ),

            # Create the button to cancel the username / password change
            ft.Container(
                ft.Text('Cancelar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.cancel_credentials(),
                border_radius=15,
                visible=False,
            ),

            # Create the button to edit the username / password change
            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.edit_credentials(),
                border_radius=15,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)


        credentials_layout = ft.Column([
            user_title,
            self.credentials,
            self.credentials_buttons,
        ])

        #* ------------------ Subjects | Phase - Layout ------------------ *#

        # Create the title for the subjects section
        subjects_title = ft.Row([
            ft.Icon(ft.icons.SUBJECT, color='#6D62A1', size=25),

            ft.Text(
                'Materias',
                color='#4B4669',
                font_family='Arial',
                width = 600,
                text_align='left',
                weight='bold',
                size=16,
            ),
        ], spacing=10, alignment=ft.MainAxisAlignment.START)


        self.subjects = ft.DataTable(
            width=400,
            column_spacing=0,
            show_bottom_border=True,
            heading_row_height=35,

            columns=[
                ft.DataColumn(ft.Container(ft.Text('Materia', color='#4B4669', font_family='Arial', size=15), width=250)),
                ft.DataColumn(ft.Container(ft.Text('Acciones', color='#4B4669', font_family='Arial', size=15), width=80)),
            ],
        )

        self.subject_scroll = ft.Column([
            self.subjects,
        ], alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, height=200)

        subject_container = ft.Container(
            self.subject_scroll,
            width=400,
            height=200,
            border_radius=ft.BorderRadius(top_left=10, top_right=0, bottom_left=10, bottom_right=10),
            padding=ft.padding.all(5),
            border=ft.border.all(2, '#bec0e3'),
        )

        self.add_subject_button = ft.Container(
                ft.Icon(ft.icons.ADD, color='#6e62a0', size=25),
                width=30,
                height=42,
                bgcolor='#bec0e3',
                alignment=ft.alignment.center_left,
                on_click= lambda e: self.subject_confirm_add(),
                border_radius=ft.BorderRadius(top_left=0, top_right=15, bottom_left=0, bottom_right=15),
            )

        subjects_layout = ft.Column([
            subjects_title,
            ft.Row([
                subject_container,
                self.add_subject_button,
            ], alignment=ft.MainAxisAlignment.START, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START),
        ], width=450)


        # Create the title for the phase section
        phase_title = ft.Row([
            ft.Icon(ft.icons.SUBJECT, color='#6D62A1', size=25),

            ft.Text(
                'Etapas',
                color='#4B4669',
                font_family='Arial',
                width = 600,
                text_align='left',
                weight='bold',
                size=16,
            ),
        ], spacing=10, alignment=ft.MainAxisAlignment.START)

        self.phase = ft.DataTable(
            width=400,
            column_spacing=0,
            show_bottom_border=True,
            heading_row_height=35,

            columns=[
                ft.DataColumn(ft.Container(ft.Text('Grado / Año', color='#4B4669', font_family='Arial', size=15), width=150)),
                ft.DataColumn(ft.Container(ft.Text('Seccion', color='#4B4669', font_family='Arial', size=15), width=80)),
                ft.DataColumn(ft.Container(ft.Text('Acciones', color='#4B4669', font_family='Arial', size=15), width=80)),
            ],
        )

        self.phase_scroll = ft.Column([
            self.phase,
        ], alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, height=200)

        phase_container = ft.Container(
            self.phase_scroll,
            width=400,
            height=200,
            border_radius=ft.BorderRadius(top_left=0, top_right=10, bottom_left=10, bottom_right=10),
            padding=ft.padding.all(5),
            border=ft.border.all(2, '#bec0e3'),
        )

        self.add_phase_button = ft.Container(
                ft.Icon(ft.icons.ADD, color='#6e62a0', size=25),
                width=30,
                height=42,
                bgcolor='#bec0e3',
                alignment=ft.alignment.center_right,
                on_click= lambda e: self.phase_confirm_add(),
                border_radius=ft.BorderRadius(top_left=15, top_right=0, bottom_left=15, bottom_right=0),
            )

        phase_layout = ft.Column([
            phase_title,
            ft.Row([
                self.add_phase_button,
                phase_container,
            ], alignment=ft.MainAxisAlignment.START, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START),
        ], width=450)

        subject_phase_layout = ft.Row([
            subjects_layout,
            phase_layout,
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=20)






        #* ------------------ Database - Layout ------------------ *#

        # Create the title for the database section
        database_title = ft.Row([
            ft.Icon(ft.icons.PIE_CHART_ROUNDED, color='#6D62A1', size=25),

            ft.Text(
                'Base de Datos',
                color='#4B4669',
                font_family='Arial',
                width = 600,
                text_align='left',
                weight='bold',
                size=16,
            ),
        ], spacing=10, alignment=ft.MainAxisAlignment.START)

        self.database_buttons = ft.Row([
        # Create the button to import the database
            ft.Container(
                ft.Text('Restaurar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=100,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                # on_click= lambda e: self.import_db(), #TODO - Create the function to import the database
                border_radius=15,
            ),

        # Create the button to export the database
            ft.Container(
                ft.Text('Respaldar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=100,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                # on_click= lambda e: self.export_db(), #TODO - Create the function to export the database
                border_radius=15,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=20)


        # Create the Color Legend
        color_legend = ft.Column([
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.BLUE),
                        ft.Text('Calendario', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.YELLOW),
                        ft.Text('Profesores', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.PINK),
                        ft.Text('Estudiantes', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.GREEN),
                        ft.Text('Horarios', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.INDIGO),
                        ft.Text('Notas', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.AMBER),
                        ft.Text('Representantes', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.CYAN),
                        ft.Text('Etapas', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                ], spacing=10),
                border=ft.border.only(right=ft.BorderSide(color='#6D62A1', width=2)),
                padding=ft.padding.only(right=10, left=50),
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=20)


        # Create a Graph to show the storage of the database
        self.storage_graph = ft.PieChart(
        sections=[
            ft.PieChartSection( # Calendario
                20,
                color=ft.colors.BLUE,
            ),
            ft.PieChartSection( # Profesores
                20,
                color=ft.colors.YELLOW,
            ),
            ft.PieChartSection( # Estudiantes
                20,
                color=ft.colors.PINK,
            ),
            ft.PieChartSection( # Horarios
                20,
                color=ft.colors.GREEN,
            ),
            ft.PieChartSection( # Notas
                20,
                color=ft.colors.INDIGO,
            ),
            ft.PieChartSection( # Representantes
                20,
                color=ft.colors.AMBER,
            ),
            ft.PieChartSection( # Etapas
                20,
                color=ft.colors.CYAN,
            ),
        ],
        sections_space=1,
        center_space_radius=0,
        width=200,
        height=200,
        scale=2.5,
    )

        database_layout = ft.Column([
            database_title,
            self.database_buttons,
            ft.Row([
                color_legend,
                ft.VerticalDivider(width=200),
                self.storage_graph,
            ],spacing=20, alignment=ft.MainAxisAlignment.START ),
        ], spacing=20)

        #* ------------------ Layout ------------------ *#
        self.scrol = ft.Column([
            title,
            ft.Divider(),
            credentials_layout,
            ft.Divider(),
            subject_phase_layout,
            ft.Divider(),
            database_layout,
        ], spacing=20, alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, height=590)

        layout_container = ft.Row([
            ft.Container(
                self.scrol,
                width=1100,
                height=600,
                border_radius=20,
                padding=ft.padding.all(20),
                border=ft.border.all(2, '#6D62A1')
            )
        ], alignment=ft.MainAxisAlignment.CENTER)

        # add the layout to the page
        self.content = layout_container

        self.show_subjects()
        self.show_phases()


    def build(self):
        return self.content


    #* ------------------ CREDENTIALS Functions ------------------ *#

    def credentials_validates(self):
        '''Function to validate the credentials'''
        validates = True

        content = self.credentials.content.controls

        for controls in content[0].controls:
            # si es igual a un textfield
            if isinstance(controls, ft.TextField):
                if controls.value != '':
                    content[0].controls[0].content.color = '#3564fc'
                else:
                    validates = False
                    content[0].controls[0].content.color = '#ff0000'
                    break

        for controls in content[1].controls:
            # si es igual a un textfield
            if isinstance(controls, ft.TextField):
                if controls.value != '':
                    content[1].controls[0].content.color = '#3564fc'
                else:
                    validates = False
                    content[1].controls[0].content.color = '#ff0000'
                    break

        self.credentials.update()

        if validates:
            return True
        else:

            self.credentials_buttons.controls[0].content.value = 'Rellene todos los campos'
            self.credentials_buttons.controls[0].bgcolor = '#ff0000'
            self.credentials_buttons.controls[0].width = 200
            self.credentials_buttons.controls[0].update()

            time.sleep(1)

            self.credentials_buttons.controls[0].content.value = 'Guardar'
            self.credentials_buttons.controls[0].bgcolor = '#6D62A1'
            self.credentials_buttons.controls[0].width = 80
            self.credentials_buttons.controls[0].update()

            return False

    def edit_credentials(self):
        '''Function to edit the username and password'''

        # Change the buttons
        self.credentials_buttons.controls[0].visible = True
        self.credentials_buttons.controls[1].visible = True
        self.credentials_buttons.controls[2].visible = False


        # Enable the textfields
        self.credentials.disabled = False

        # Show the password
        self.credentials.content.controls[0].controls[3].password = False

        # Show the Security Questions
        self.credentials.content.controls[1].controls[1].password = False
        self.credentials.content.controls[1].controls[2].password = False
        self.credentials.content.controls[1].controls[3].password = False

        self.update()

    def cancel_credentials(self):
        '''Function to cancel the username and password change'''

        # Change the buttons
        self.credentials_buttons.controls[0].visible = False
        self.credentials_buttons.controls[1].visible = False
        self.credentials_buttons.controls[2].visible = True

        # Disable the textfields
        self.credentials.disabled = True

        # hide the password
        self.credentials.content.controls[0].controls[3].password = True

        # hide the Security Questions
        self.credentials.content.controls[1].controls[1].password = True
        self.credentials.content.controls[1].controls[2].password = True
        self.credentials.content.controls[1].controls[3].password = True

        # Change the colors to the original
        self.credentials.content.controls[0].controls[0].content.color = '#3564fc'
        self.credentials.content.controls[1].controls[0].content.color = '#3564fc'


        # Set the values to the original

        credentials = get_user()

        self.credentials.content.controls[0].controls[1].value = credentials['user']
        self.credentials.content.controls[0].controls[2].value = credentials['email']
        self.credentials.content.controls[0].controls[3].value = credentials['password']
        self.credentials.content.controls[1].controls[1].value = credentials['question1']
        self.credentials.content.controls[1].controls[2].value = credentials['question2']
        self.credentials.content.controls[1].controls[3].value = credentials['question3']

        self.update()

    def save_credentials(self):
        '''Function to save the username and password change'''


        if self.credentials_validates():
            # save the new credentials
            user = self.credentials.content.controls[0].controls[1].value
            email = self.credentials.content.controls[0].controls[2].value
            password = self.credentials.content.controls[0].controls[3].value
            question1 = self.credentials.content.controls[1].controls[1].value
            question2 = self.credentials.content.controls[1].controls[2].value
            question3 = self.credentials.content.controls[1].controls[3].value

            update_user(user, password, email, question1, question2, question3)

            # Change the buttons
            self.credentials_buttons.controls[0].visible = False
            self.credentials_buttons.controls[1].visible = False
            self.credentials_buttons.controls[2].visible = True

            # Disable the textfields
            self.credentials.disabled = True

            # hide the password
            self.credentials.content.controls[0].controls[3].password = True

            # hide the Security Questions
            self.credentials.content.controls[1].controls[1].password = True
            self.credentials.content.controls[1].controls[2].password = True
            self.credentials.content.controls[1].controls[3].password = True

            # Change the colors to the original
            self.credentials.content.controls[0].controls[0].content.color = '#3564fc'
            self.credentials.content.controls[1].controls[0].content.color = '#3564fc'
        else:
            pass

        self.update()

    #* ------------------ SUBJECTS Functions ------------------ *#
    def show_subjects(self):
        """
        Display a list of subjects in a table format on the settings page.

        This method retrieves the list of subjects from the database and iterates over each subject to create a data row for each subject.
        Each data row contains two data cells: one for the subject name and one for the edit and delete buttons.
        The data rows are then appended to the table on the settings page.

        Inputs: None
        Outputs: None
        """

        subjects_list = get_subjects()

        for subject in subjects_list:
            row = ft.DataRow([
                    ft.DataCell(ft.Container(ft.Text(subject['Nombre'], color='#4B4669', font_family='Arial', size=12), width=250)),
                    ft.DataCell(ft.Container(self.subject_edit_set(subject['ID'], subject['Nombre']), width=80)),
                ], data=subject['ID'])
            self.subjects.rows.append(row)
        self.update()

    def subject_validate(self, dlg):
        '''Function to validate the subject'''
        if dlg.content.controls[1].value != '':
            return True
        else:
            dlg.actions[1].text = 'Rellene todos los campos'
            dlg.actions[1].bgcolor = '#ff0000'
            dlg.update()

            time.sleep(1)

            dlg.actions[1].text = 'Agregar'
            dlg.actions[1].bgcolor = '#6D62A1'
            dlg.update()
            return False

    def subject_edit_set(self, id, subject_name):
        '''Function to set the subject edit buttons'''
        return ft.Row([
            # Create the button to edit the subject
            ft.IconButton(icon=ft.icons.EDIT, icon_color='#3741c8', width=35, height=35, icon_size=20, on_click= lambda e: self.subject_confirm_edit(e), data=[id, subject_name]),
            # Create the button to delete the subject
            ft.IconButton(icon=ft.icons.DELETE, icon_color='#ff0000', width=35, height=35, icon_size=20, on_click= lambda e: self.subject_confirm_delete(e), data=[id, subject_name]),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def subject_confirm_add(self):
        """
        Display a dialog box for adding a new subject.

        This method prompts the user to enter the name of the subject and provides options to cancel or add the subject.

        Example Usage:
        ```python
        settings = Settings(page)
        settings.subject_confirm_add()
        ```

        Inputs: None

        Flow:
        1. Create an `AlertDialog` with a title and a `TextField` for entering the name of the subject.
        2. Display the dialog box with options to cancel or add the subject.
        3. If the user clicks on the "Cancelar" button, close the dialog box.
        4. If the user clicks on the "Agregar" button, call the `add_subject` method and pass the dialog box as a parameter.
        5. Close the dialog box.

        Outputs: None
        """
        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Agregar Materia', color='#4B4669', font_family='Arial', size=20),
                ft.TextField(
                    width=300,
                    height=35,
                    label='Nombre de la Materia',
                    hint_text='Ingresa el nombre de la materia',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                )
            ], spacing=10, width=300, height=70, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Agregar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.add_subject(dlg)),
            ])
        self.open_dlg(dlg)

    def add_subject(self, dlg):
        """
        Adds a new subject to the database and updates the subjects table on the settings page.

        :param dlg: The dialog box that contains the input fields for the new subject.
        :type dlg: Dialog
        """
        if self.subject_validate(dlg):
            subject_name = dlg.content.controls[1].value
            subject_add(subject_name)
            self.close(dlg)
            self.subjects.rows.clear()
            self.show_subjects()
        else:
            pass

    def subject_confirm_edit(self, e):
        """
        Displays a dialog box that allows the user to edit the name of a subject.

        Args:
            e (Event): The event object that triggered the method.

        Returns:
            None
        """
        name = e.control.data[1]
        id = e.control.data[0]

        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Editar Materia', color='#4B4669', font_family='Arial', size=20),
                ft.TextField(
                    width=300,
                    height=35,
                    label='Nombre de la Materia',
                    hint_text='Ingresa el nombre de la materia',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                    value=name
                )
            ], spacing=10, width=300, height=70, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Editar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.edit_subject(dlg, id)),
            ])
        self.open_dlg(dlg)

    def edit_subject(self, dlg, id):
        """
        Updates a subject in the database.

        Args:
            dlg (Dialog): A dialog object that contains the controls for editing the subject.
            id (int): The ID of the subject to be edited.

        Returns:
            None

        Raises:
            None

        Summary:
        The `edit_subject` method is responsible for updating a subject in the database. It takes a dialog object and the ID of the subject as inputs, and updates the subject name in the database if the input is valid.

        Example Usage:
        ```python
        settings = Settings(page)
        settings.edit_subject(dialog, subject_id)
        ```

        Code Analysis:
        - The method first validates the input dialog using the `subject_validate` method.
        - If the input is valid, it retrieves the new subject name from the dialog's controls.
        - It then calls the `update_subject` function with the subject ID and the new subject name to update the subject in the database.
        - The method closes the dialog and clears the rows in the subjects table.
        - Finally, it calls the `show_subjects` method to display the updated list of subjects.
        """
        if self.subject_validate(dlg):
            subject_name = dlg.content.controls[1].value
            update_subject(id, subject_name)
            self.close(dlg)
            self.subjects.rows.clear()
            self.show_subjects()
        else:
            pass


    def subject_confirm_delete(self, e):
        """
        Confirm the deletion of a subject in the Settings page.

        Args:
            e (event): The event object that triggered the method.

        Returns:
            None

        Example Usage:
            settings = Settings(page)
            settings.subject_confirm_delete(event)

        Code Analysis:
            This method is used to confirm the deletion of a subject in the Settings page. It displays a dialog box with a confirmation message and two buttons: "Cancelar" (Cancel) and "Eliminar" (Delete).

            Inputs:
            - e (event): The event object that triggered the method.

            Flow:
            1. Get the ID of the subject to be deleted from the event object.
            2. Create an `AlertDialog` with a confirmation message asking if the user is sure they want to delete the subject.
            3. Add two buttons to the dialog: "Cancelar" (Cancel) and "Eliminar" (Delete).
            4. When the "Cancelar" button is clicked, close the dialog.
            5. When the "Eliminar" button is clicked, call the `delete_subject` method with the dialog and subject ID as arguments.
            6. Open the dialog.

            Outputs:
            - None
        """
        id = e.control.data[0]

        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('¿Estas seguro que quieres eliminar esta materia?', color='#4B4669', font_family='Arial', size=15),
                ft.Text('Se recomienda borrar la materia solamente si la acaba de agregar, de lo contrario podria generar un error en el programa', color='#4B4669', font_family='Arial', size=15),
            ], spacing=10, width=300, height=100, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Eliminar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.subject_secundary_confirm_delete(dlg, id)),
            ])
        self.open_dlg(dlg)

    def subject_secundary_confirm_delete(self, dlg, id):
        """
        Confirms the deletion of a subject in the Settings page.

        Parameters:
            dlg (Dialog): The dialog box containing the confirmation message.
            id (int): The ID of the subject to be deleted.

        Description:
            This method is called when the user confirms the deletion of a subject in the Settings page.
            It updates the text and behavior of the confirmation button in the dialog box to give the user
            a countdown before the deletion is executed. The countdown is displayed in the button text, and
            the button color changes to indicate that it is the confirmation button. Once the countdown reaches
            zero, the button text changes to "Confirmar Eliminacion" and the button color changes to indicate
            that it is the final confirmation button. Clicking on this button triggers the deletion of the subject.

        Example:
            subject_secundary_confirm_delete(dlg, 1)
        """
        dlg.actions[1].on_click = None
        for i in range(5, -1, -1):
            dlg.actions[1].text = f'Espere {i} segundos...'
            dlg.update()
            time.sleep(1)

        dlg.actions[1].text = 'Confirmar Eliminacion'
        dlg.actions[1].bgcolor = '#f83c86'
        dlg.actions[1].on_click = lambda e: self.delete_subject(dlg, id)
        dlg.update()

    def delete_subject(self, dlg, id):
        """
        Delete a subject from the database.

        Args:
            dlg (Dialog): The dialog box that needs to be closed after deleting the subject.
            id (int): The ID of the subject that needs to be deleted.

        Returns:
            None

        """
        delete_subject(id)
        self.close(dlg)
        self.subjects.rows.clear()
        self.show_subjects()

    #* ------------------ PHASE Functions ------------------ *#
    def show_phases(self):
        """
        Retrieves a list of phases from the database and displays them in a table format on the settings page.

        Inputs:
        - None

        Flow:
        1. Retrieve the list of phases from the database using the `get_phases` function.
        2. Iterate over each phase in the list.
        3. Create a data row for each phase, consisting of three data cells: one for the grade/year, one for the section, and one for the edit button.
        4. Append the data row to the `phase` table.
        5. Update the settings page to reflect the changes.

        Outputs:
        - None
        """
        phases_list = get_phases()

        for phase in phases_list:
            row = ft.DataRow([
                    ft.DataCell(ft.Container(ft.Text(phase['Grado/Año'], color='#4B4669', font_family='Arial', size=12), width=150)),
                    ft.DataCell(ft.Container(ft.Text(phase['Seccion'], color='#4B4669', font_family='Arial', size=12), width=80)),
                    ft.DataCell(ft.Container(self.phase_edit_set(phase['ID'], phase['Grado/Año'], phase['Seccion']), width=80)),
                ], data=phase['ID'])
            self.phase.rows.append(row)

        self.update()

    def phase_validate(self, dlg):
        '''Function to validate the phase'''
        if dlg.content.controls[1].controls[0].value != '' and dlg.content.controls[1].controls[1].value != '' and dlg.content.controls[2].value is not None:
            return True
        else:
            dlg.actions[1].text = 'Rellene todos los campos'
            dlg.actions[1].bgcolor = '#ff0000'
            dlg.update()

            time.sleep(1)

            dlg.actions[1].text = 'Agregar'
            dlg.actions[1].bgcolor = '#6D62A1'
            dlg.update()
            return False

    def phase_edit_set(self, id, grade, section): #TODO - Add the function to edit the phase
        '''Function to set the subject edit buttons'''
        return ft.Row([
            # Create the button to edit the subject
            ft.IconButton(icon=ft.icons.EDIT, icon_color='#3741c8', width=35, height=35, icon_size=20, on_click= lambda e: self.phase_confirm_edit(e), data=[id, grade, section]),
            # Create the button to delete the subject
            ft.IconButton(icon=ft.icons.DELETE, icon_color='#ff0000', width=35, height=35, icon_size=20, on_click= lambda e: self.phase_confirm_delete(e), data=[id, grade, section]),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def phase_confirm_add(self):
        """
        Displays a dialog box for adding a phase.

        This method creates an AlertDialog object with a title and content. The content of the dialog includes a text field for entering the phase name, a text field for entering the section, and a radio group for selecting the type of phase. The dialog also includes two buttons: "Cancelar" to close the dialog and "Agregar" to add the phase.

        Example Usage:
        ```python
        settings = Settings(page)
        settings.phase_confirm_add()
        ```

        Inputs: None
        Outputs: None
        """
        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Agregar Fase', color='#4B4669', font_family='Arial', size=20),
                ft.Row([
                    ft.TextField(
                        width=150,
                        height=35,
                        label='Fase',
                        hint_text='Ingresa la fase',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        input_filter=ft.InputFilter(regex_string='[0-9]'),
                    ),
                    ft.TextField(
                        width=140,
                        height=35,
                        label='Seccion',
                        hint_text='Ingresa la seccion',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        input_filter=ft.InputFilter(regex_string='[A-Z]'),
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=300, height=35),

                ft.RadioGroup(content=ft.Container(
                    ft.Row([
                        ft.Radio(value='Grado', label='Grado'),
                        ft.Radio(value='Año', label='Año'),
                    ], alignment=ft.MainAxisAlignment.START), padding=ft.padding.only(left=10,top=0,right=10,bottom=0))
                ),

            ], spacing=10, width=300, height=125, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Agregar',bgcolor = '#6D62A1',color = '#f3f4fa',  on_click= lambda e: self.add_phase(dlg)),
            ])
        self.open_dlg(dlg)

    def add_phase(self, dlg):
        """
        Adds a new phase to the settings page.

        Args:
            dlg (dialog): A dialog object that contains the input values for the new phase.

        Returns:
            None

        Summary:
        This method is used to add a new phase to the settings page. It takes a dialog object as input and validates the input values. If the validation is successful, it adds the new phase to the database, updates the phase list, and closes the dialog. If the validation fails, it does nothing.

        Example Usage:
        ```python
        settings = Settings(page)
        settings.add_phase(dialog)
        ```

        Code Analysis:
        - The method first validates the input values using the `phase_validate` method.
        - If the validation is successful, it checks the value of the second control in the dialog to determine the type of phase (either "Grado" or "Año").
        - It constructs the phase name by concatenating the value of the first control in the dialog with the type of phase.
        - It adds the new phase to the database using the `phase_add` function.
        - It clears the existing phase rows and updates the settings page.
        - It shows the updated list of phases on the settings page.
        - It closes the dialog.
        - If the validation fails, it does nothing.
        """
        if self.phase_validate(dlg):
            if dlg.content.controls[2].value == 'Grado':
                phase_name = dlg.content.controls[1].controls[0].value + ' Grado'
            else:
                phase_name = dlg.content.controls[1].controls[0].value + ' Año'

            phase_add(phase_name, dlg.content.controls[1].controls[1].value)
            del self.phase.rows[:]
            self.update()
            self.show_phases()
            self.close(dlg)
        else:
            pass

    def phase_confirm_edit(self, e):
        """
        Displays a dialog box for editing a phase in a settings page.

        Args:
            e (Event): An event object that contains data about the control that triggered the event.

        Returns:
            None

        Example Usage:
            settings = Settings(page)
            settings.phase_confirm_edit(e)

        Code Analysis:
            - Extracts the id, section, and grade from the event data.
            - Splits the grade into the grade value and grade type.
            - Creates a dialog box with text fields for entering the new phase and section, and a radio group for selecting the grade type.
            - Sets the initial values of the text fields and radio group based on the extracted data.
            - Adds "Cancelar" and "Editar" buttons to the dialog box, with event handlers for canceling or saving the changes.
            - Displays the dialog box to the user.
        """
        id = e.control.data[0]
        section = e.control.data[2]
        grade = e.control.data[1]

        grade_type = grade.split(' ')[1]
        grade = grade.split(' ')[0]

        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Editar Fase', color='#4B4669', font_family='Arial', size=20),

                ft.Row([
                    ft.TextField(
                        width=150,
                        height=35,
                        label='Fase',
                        hint_text='Ingresa la fase',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        input_filter=ft.InputFilter(regex_string='[0-9]'),
                        value=grade,
                    ),
                    ft.TextField(
                        width=140,
                        height=35,
                        label='Seccion',
                        hint_text='Ingresa la seccion',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        input_filter=ft.InputFilter(regex_string='[A-Z]'),
                        value=section,
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=300, height=35),

                ft.RadioGroup(content=ft.Container(
                    ft.Row([
                        ft.Radio(value='Grado', label='Grado'),
                        ft.Radio(value='Año', label='Año'),
                    ], alignment=ft.MainAxisAlignment.START), padding=ft.padding.only(left=10,top=0,right=10,bottom=0)),
                    value=grade_type
                ),

            ], spacing=10, width=300, height=125, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Editar',bgcolor = '#6D62A1',color = '#f3f4fa',  on_click= lambda e: self.edit_phase(dlg, id)),
            ])
        self.open_dlg(dlg)

    def edit_phase(self, dlg, id):
        """
        Update a phase in the database based on user input from a dialog box.

        Args:
            dlg (DialogBox): The dialog box object that contains the user input.
            id (int): The ID of the phase to be updated in the database.

        Returns:
            None

        Example Usage:
            settings = Settings(page)
            settings.edit_phase(dlg, id)

        """
        if self.phase_validate(dlg):
            if dlg.content.controls[2].value == 'Grado':
                phase_name = dlg.content.controls[1].controls[0].value + ' Grado'
            else:
                phase_name = dlg.content.controls[1].controls[0].value + ' Año'

            update_phase(id, phase_name, dlg.content.controls[1].controls[1].value)
            del self.phase.rows[:]
            self.update()
            self.show_phases()
            self.close(dlg)
        else:
            pass

    def phase_confirm_delete(self, e):
        """
        Displays a confirmation dialog to the user when they want to delete a phase.

        Args:
            e (Event): The event object that triggered the method. It contains information about the phase to be deleted.

        Returns:
            None
        """
        id = e.control.data[0]

        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Esta seguro que desea eliminar la fase?', color='#4B4669', font_family='Arial', size=15, weight='bold'),
                ft.Text('Se recomienda borrar la fase solamente si la acaba de agregar, de lo contrario podria generar un error en el programa', color='#4B4669', font_family='Arial', size=15),
            ], spacing=10, width=300, height=100, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar',bgcolor = '#6D62A1',color = '#f3f4fa', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Eliminar',bgcolor = '#6D62A1',color = '#f3f4fa',  on_click= lambda e: self.phase_secundary_confirm_delete(id, dlg)),
            ])
        self.open_dlg(dlg)

    def phase_secundary_confirm_delete(self, id, dlg):
        """
        Displays a confirmation dialog box with a countdown timer. After the countdown, the dialog box is updated to allow the user to confirm the deletion.

        :param dlg: The dialog box object that is displayed to the user.
        :type dlg: dialog box
        :return: None
        """
        dlg.actions[1].on_click = None
        for i in range(5, -1, -1):
            dlg.actions[1].text = f'Espere {i} segundos...'
            dlg.update()
            time.sleep(1)

        dlg.actions[1].text = 'Confirmar Eliminacion'
        dlg.actions[1].bgcolor = '#f83c86'
        dlg.actions[1].on_click = lambda e: self.delete_phase(id, dlg)
        dlg.update()

    def delete_phase(self, id, dlg):
        """
        Delete a phase from the list of phases.

        Args:
            id (int): The ID of the phase to be deleted.
            dlg (Dialog): The dialog box to be closed after the phase is deleted.

        Returns:
            None

        """
        delete_phase(id)
        del self.phase.rows[:]
        self.update()
        self.show_phases()
        self.close(dlg)


    #* ------------------ Database Functions ------------------ *#
    #TODO - Create a function to get the storage of the database and set it to the graph





    #* ------------------ DLG Functions ------------------ *#

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
