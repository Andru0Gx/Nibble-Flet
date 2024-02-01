'''Students Page'''

# Libraries
import time
import datetime
import threading
import flet as ft

# Modules
from modules.pdf_printer import path_selector

# Database
from DB.Functions.student_parent_db import student_add, parent_add, parent_student_add
from DB.Functions.student_parent_db import student_search, parent_search, parent_student_search, filter_students_db
from DB.Functions.student_parent_db import validate_ci, validate_student
from DB.Functions.student_parent_db import student_delete, parent_delete, parent_student_delete
from DB.Functions.student_parent_db import student_update, parent_update, parent_student_update
from DB.Functions.student_parent_db import get_students, check_amount as check
from DB.Functions.temp_data_db import save_tempdata_db, get_tempdata_db, delete_tempdata_db, check_tempdata_db
from DB.Functions.phases_db import get_phases, search_phase
from DB.Functions.grades_db import grade_add, sync_students, delete_grades_student
from DB.Functions.subjects_db import filter_subjects


class State:
    """
    A class that represents the state of an object.
    
    Attributes:
        i (int): The value of the state.
    """
    i = 0

s = State()
sem = threading.Semaphore()


class Students(ft.UserControl):
    '''
    The `Students` class is a user control class that represents a form for registering students and their parents.
    It provides fields for entering student information such as name, last name, CI, birthdate, address, date of 
    inscription, and grade. It also provides fields for entering parent information such as name, last name, CI, 
    and contact details.

    The class includes methods for:
    - Changing the birthdate and date of inscription
    - Searching for parents
    - Adding parents and students to the database
    - Deleting parents and students from the database
    - Editing student information
    - Printing student information
    - Changing the view to display a list of students.

    Methods:
        - change_birthdate(date): Updates the value of the birthdate field in the student form.
        - change_date_inscription(date): Updates the value of the date of inscription for a student.
        - search_parent(): Searches for a parent in the database.
        - add_parent(): Adds a parent to the database.
        - change_phase(): Changes the phase of the student.
        - delete_parent(): Deletes a parent from the database.
        - add_student(): Adds a student to the database.
        - delete_student(): Deletes a student from the database.
        - edit_student(): Edits a student in the database.
        - print_student(): Prints a student from the database.
        - view(): Changes the view to display the list of students.
    '''

    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.body = section

        self.actual_student = None
        self.actual_parent = None


        #* ------------------ DatePicker ------------------ *#
        self.date_picker_birthdate = ft.DatePicker(
            first_date= datetime.datetime(1800,1,1),
            last_date= datetime.datetime(3000,1,1),
            on_change= lambda e: self.change_birthdate(self.date_picker_birthdate.value.strftime("%d / %m / %Y")),
        )

        self.date_picker_inscription = ft.DatePicker(
            first_date= datetime.datetime(1800,1,1),
            last_date= datetime.datetime(3000,1,1),
            on_change= lambda e: self.change_date_inscription(self.date_picker_inscription.value.strftime("%d / %m / %Y")),
        )

        self.page.add(self.date_picker_birthdate)
        self.page.add(self.date_picker_inscription)



        #* ------------------ Layout - Student ------------------ *#
        # Create the Title
        self.student_title = ft.Text(
            'Registrar Estudiante',
            color='#4B4669',
            font_family='Arial',
            width = 500,
            text_align='center',
            weight='bold',
            size=20,
        )

        # Create the student name text field
        self.student_name = ft.TextField(
            width=500,
            height=35,
            label='Nombre del Estudiante',
            hint_text='Ingresa el Nombre del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the student lastname text field
        self.student_lastname = ft.TextField(
            width=500,
            height=35,
            label='Apellido del Estudiante',
            hint_text='Ingresa el Apellido del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the student ci text field
        self.student_ci = ft.TextField(
            width=500,
            height=35,
            label='Cedula del Estudiante',
            hint_text='Ingresa la Cedula del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            input_filter=ft.InputFilter(regex_string='[0-9]'),
        )

        # Create the student birthdate text field
        self.student_birthdate = ft.Row([
            ft.TextField(
                width=170,
                height=35,
                label='Fecha de Nacimiento',
                hint_text='Selecciona la fecha',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669', size=15),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                read_only=True,
            ),

            ft.Container(
                width=35,
                height=35,
                bgcolor= '#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.date_picker_birthdate.pick_date(),
                border_radius=15,
                content=ft.Icon(ft.icons.CALENDAR_TODAY, color='#f3f4fa', size=20),
            )
        ])

        # Create the student address text field
        self.student_address = ft.TextField(
            width=500,
            height=35,
            label='Direccion',
            hint_text='Ingresa la Direccion del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the student date inscription text field
        self.student_date_inscription = ft.Row([
            ft.TextField(
                width=170,
                height=35,
                label='Fecha de Inscripcion',
                hint_text='Selecciona la fecha',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669', size=15),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                read_only=True,
            ),

            ft.Container(
                width=35,
                height=35,
                bgcolor= '#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.date_picker_inscription.pick_date(),
                border_radius=15,
                content=ft.Icon(ft.icons.CALENDAR_TODAY, color='#f3f4fa', size=20),
            )
        ])

        # Create the student grade Dropdown
        self.student_grade = ft.Dropdown(
            width=220,
            height=35,
            label='Etapa (Grado/Año)',
            hint_text='Selecciona la Etapa',
            filled=True,
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the student status Dropdown
        self.student_status = ft.Dropdown(
            width=220,
            height=35,
            label='Estado',
            hint_text='Selecciona el Estado',
            filled=True,
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            options=[
                ft.dropdown.Option('Activo'),
                ft.dropdown.Option('Retirado'),
                ft.dropdown.Option('Graduado', disabled=True), #TODO - If state TRUE, disable the dropdown and the phase dropdown
            ]
        )

        # Create the layout
        self.layout_student = ft.Container(
            ft.Column([
            self.student_title,
            self.student_name,
            self.student_lastname,
            self.student_ci,
            ft.Row([
                self.student_birthdate,
                self.student_date_inscription,
            ], spacing=20),
            self.student_address,
            ft.Row([
                self.student_grade,
                self.student_status,
            ], spacing=20),
        ], alignment=ft.MainAxisAlignment.START, spacing=20),
        width=500,
        height=480,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        disabled=True,
        )


        #* ------------------ Layout - Parent ------------------ *#
        # Create the Title
        self.parent_title = ft.Text(
            'Registrar Representante',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='center',
            weight='bold',
            size=20,
        )

        # Create the parent name text field
        self.parent_name = ft.TextField(
            width=500,
            height=35,
            label='Nombre del Representante',
            hint_text='Ingresa el Nombre del Representante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
        )

        # Create the parent lastname text field
        self.parent_lastname = ft.TextField(
            width=500,
            height=35,
            label='Apellido del Representante',
            hint_text='Ingresa el Apellido del Representante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
        )

        # Create the parent ci text field and a searh button
        self.parent_ci = ft.Row([
            ft.TextField(
            width=415,
            height=35,
            label='Cedula del Representante',
            hint_text='Ingresa la Cedula del Representante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            input_filter=ft.InputFilter(regex_string='[0-9]'),
            on_change= lambda e: self.refresh_children(),
        ),
            ft.Container(
                width=35,
                height=35,
                bgcolor= '#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.search_parent(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the parent contact text field
        self.parent_contact = ft.Row([
            ft.TextField(
                width=220,
                height=35,
                label='Contacto 1',
                hint_text='Ingresa el contacto',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                input_filter=ft.InputFilter(regex_string='[0-9]'),
            ),

            ft.TextField(
                width=220,
                height=35,
                label='Contacto 2 (Opcional)',
                hint_text='Ingresa el contacto',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                input_filter=ft.InputFilter(regex_string='[0-9]'),
            )
        ], spacing=20)

        # Create a list of the children of the parent
        self.parent_children = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(ft.Text('Nombre', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Cedula', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Grado', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
            ],
            width=500,
            data_row_max_height=40,
            heading_row_height=40

        )

        scroll = ft.Column([
            self.parent_children,
        ], width=500, height=125, scroll=ft.ScrollMode.ALWAYS)

        child_content = ft.Container(scroll, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#bec0e3'), border_radius=10, width=500, height=125)



        # Create the Layout
        self.layout_parent = ft.Container(
            content=ft.Column([
            self.parent_title,
            self.parent_name,
            self.parent_lastname,
            self.parent_ci,
            self.parent_contact,
            ft.Column([
                ft.Text('Hijos', size=16, color='#4B4669', text_align='center', weight='bold'),
                child_content
            ], alignment=ft.MainAxisAlignment.START, spacing=10, horizontal_alignment='center'),
        ],alignment=ft.MainAxisAlignment.START, spacing=20),
        width=500,
        height=480,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        disabled=True,
        )

        #* ------------------ Footer ------------------ *#
        # Create the Search Bar
        self.search_bar = ft.Row([
            ft.TextField(
            width=450,
            height=35,
            label='Buscar Estudiante',
            hint_text='Ingresa la cedula del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            input_filter=ft.InputFilter(regex_string='[0-9]'),
        ),
            ft.Container(
                width=35,
                height=35,
                bgcolor= '#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.search(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the Students Buttons (Add, Eliminate, Edit, Change View, Print)
        self.students_buttons = ft.Row([
            ft.Container(
                ft.Text('Agregar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.activate_fields(1),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Eliminar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.delete_confirm(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.activate_fields(2),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
                on_click= lambda e: self.add_student(),
                visible=False,
            ),

            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
                on_click= lambda e: self.edit_student(),
                visible=False,
            ),

            ft.Container(
                ft.Text('Cancelar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.cancel(),
                border_radius=15,
                visible=False,
            ),

            ft.Container(
                ft.Icon(ft.icons.PRINT, color='#f3f4fa', size=20),
                width=50,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.print_student(),
                border_radius=15,
                tooltip='Imprimir Estudiante',
            ),

            ft.Container(
                ft.Icon(ft.icons.TABLE_ROWS_OUTLINED, color='#f3f4fa', size=20),
                width=50,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.view(),
                border_radius=15,
            )
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        footer = ft.Container(
            content=ft.Row([
            self.search_bar,
            self.students_buttons
        ],alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=1025,
        height=100,
        border_radius=20,
        border=ft.border.all(2, '#6D62A1'),
        )



        #* ------------------ Layout ------------------ *#
        # Create the layout
        layout = ft.Column([
            ft.Row([
                self.layout_student,
                self.layout_parent
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            footer
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

        self.drop_options()
        self.check_temp()

    def build(self):
        return self.content


    #^ ------------------ Functions ------------------ *#

    def check_temp(self):
        """
        Retrieves temporary data from the database and populates the form fields with the retrieved data.

        Inputs:
        - None

        Flow:
        1. Checks if there is temporary data in the database.
        2. If there is temporary data, retrieves the data and assigns it to the `data` variable.
        3. Evaluates the `data` variable using the `eval()` function to convert it from a string to a dictionary.
        4. Searches for the parent ID using the student's CI (identification number) from the retrieved data.
        5. Searches for the parent information using the parent ID.
        6. Assigns the parent ID and student ID from the retrieved data to the `actual_parent` and `actual_student` variables respectively.
        7. Populates the student form fields with the corresponding data from the retrieved data.
        8. Populates the parent form fields with the corresponding data from the retrieved parent information.
        9. Deletes the temporary data from the database.

        Outputs:
        - None
        """
        if check_tempdata_db():
            data = get_tempdata_db()

            data = eval(data)

            phase = search_phase(id=data['phase_id'])

            phase = f"{phase['Grado/Año']} {phase['Seccion']}"

            parent_id = parent_student_search(student_ci=data['ID'])

            parent_info = parent_search(parent_id)

            self.actual_parent = parent_info['ID']
            self.actual_student = data['ID']


            self.student_name.value = data['name']
            self.student_lastname.value = data['lastname']
            self.student_ci.value = data['ci']
            self.student_birthdate.controls[0].value = data['birth_date']
            self.student_address.value = data['address']
            self.student_date_inscription.controls[0].value = data['admission_date']
            self.student_grade.value = phase
            self.student_status.value = data['status']

            self.parent_name.value = parent_info['name']
            self.parent_lastname.value = parent_info['lastname']
            self.parent_ci.controls[0].value = parent_info['ci']
            self.parent_contact.controls[0].value = parent_info['phone1']
            self.parent_contact.controls[1].value = parent_info['phone2']

            self.parent_rows(parent_student_search(parent_id))

            delete_tempdata_db()

    def change_birthdate(self, date):
        '''
        Updates the value of the birthdate field in the student form.

        Args:
            date (str): The new birthdate value to be set.

        Returns:
            None
        '''
        self.student_birthdate.controls[0].read_only = False
        self.update()
        self.student_birthdate.controls[0].value = date
        self.student_birthdate.controls[0].read_only = True
        self.update()

    def change_date_inscription(self, date):
        '''
        Updates the value of the date of inscription for a student.

        Args:
            date (str): The new date of inscription for the student.

        Returns:
            None
        '''
        self.student_date_inscription.controls[0].read_only = False
        self.update()
        self.student_date_inscription.controls[0].value = date
        self.student_date_inscription.controls[0].read_only = True
        self.update()

    def refresh_children(self):
        """
        Refreshes the list of children associated with the parent.

        This method clears the existing rows in the parent_children container and updates the view to reflect the changes. It is called when the parent's CI field is changed.

        Parameters:
            None

        Returns:
            None
        """
        del self.parent_children.rows[:]
        self.update()

    def drop_options(self):
        """
        Sets the dropdown options for the student grade.

        This method retrieves the list of phases from the database using the 'get_phases' function. It then iterates over each phase and creates a dropdown option for the student grade using the phase's 'Grado/Año' and 'Seccion' values. The created option is appended to the 'options' attribute of the 'student_grade' dropdown.

        This method should be called whenever the dropdown options need to be updated, such as when a new phase is added to the database.

        Parameters:
            None

        Returns:
            None
        """
        phases_list = get_phases()
        for phase in phases_list:
            self.student_grade.options.append(ft.dropdown.Option(f"{phase['Grado/Año']} {phase['Seccion']}"))
        self.update()

    def activate_fields(self, op):
        '''Activates all the fields in the student and parent forms'''
        if op == 1:
            self.layout_student.disabled = False
            self.layout_parent.disabled = False


            self.student_name.value = ''
            self.student_lastname.value = ''
            self.student_ci.value = ''
            self.student_birthdate.controls[0].value = ''
            self.student_address.value = ''
            self.student_date_inscription.controls[0].value = ''
            self.student_grade.value = ''
            self.student_status.value = ''

            self.parent_name.value = ''
            self.parent_lastname.value = ''
            self.parent_ci.controls[0].value = ''
            self.parent_contact.controls[0].value = ''
            self.parent_contact.controls[1].value = ''

            self.search_bar.controls[0].value = ''

            del self.parent_children.rows[:]

            self.search_bar.visible = False
            self.students_buttons.controls[0].visible = False
            self.students_buttons.controls[1].visible = False
            self.students_buttons.controls[2].visible = False
            self.students_buttons.controls[3].visible = True
            self.students_buttons.controls[4].visible = False
            self.students_buttons.controls[5].visible = True
            self.students_buttons.controls[6].visible = False
            self.students_buttons.controls[7].visible = False
        elif op == 2:
            if self.validate():
                self.layout_student.disabled = False
                self.layout_parent.disabled = False

                self.search_bar.visible = False
                self.students_buttons.controls[0].visible = False
                self.students_buttons.controls[1].visible = False
                self.students_buttons.controls[2].visible = False
                self.students_buttons.controls[3].visible = False
                self.students_buttons.controls[4].visible = True
                self.students_buttons.controls[5].visible = True
                self.students_buttons.controls[6].visible = False
                self.students_buttons.controls[7].visible = False
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('Debe buscar un estudiante primero'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
                )
                self.open_dlg(dlg)
        self.update()

    def cancel(self):
        '''Cancels the registration of a student'''
        self.layout_student.disabled = True
        self.layout_parent.disabled = True

        self.student_name.value = ''
        self.student_lastname.value = ''
        self.student_ci.value = ''
        self.student_birthdate.controls[0].value = ''
        self.student_address.value = ''
        self.student_date_inscription.controls[0].value = ''
        self.student_grade.value = ''
        self.student_status.value = ''

        self.parent_name.value = ''
        self.parent_lastname.value = ''
        self.parent_ci.controls[0].value = ''
        self.parent_contact.controls[0].value = ''
        self.parent_contact.controls[1].value = ''

        self.search_bar.controls[0].value = ''

        self.students_buttons.controls[0].visible = True
        self.students_buttons.controls[1].visible = True
        self.students_buttons.controls[2].visible = True
        self.students_buttons.controls[3].visible = False
        self.students_buttons.controls[4].visible = False
        self.students_buttons.controls[5].visible = False
        self.students_buttons.controls[6].visible = True
        self.students_buttons.controls[7].visible = True

        self.search_bar.visible = True

        self.actual_parent = None
        self.actual_student = None

        del self.parent_children.rows[:]

        self.update()


    def validate(self):
        '''Validates the information entered in the student and parent forms'''

        # Validate the student information
        if self.student_name.value == '' or self.student_lastname.value == '' or self.student_ci.value == '' or self.student_birthdate.controls[0].value == '' or self.student_address.value == '' or self.student_date_inscription.controls[0].value == '' or self.student_grade.value == '' or self.student_status.value == '':
            return False

        # Validate the parent information
        if self.parent_name.value == '' or self.parent_lastname.value == '' or self.parent_ci.controls[0].value == '' or self.parent_contact.controls[0].value == '':
            return False

        return True

    def parent_rows(self, data):
        """
        Populates the table with data about parents.

        Args:
            data (list): A list of dictionaries containing parent data. Each dictionary should have keys 'name', 'ci', and 'phase_id' representing the parent's name, CI (identification number), and phase ID.

        Returns:
            None. The method updates the table with the parent data.
        """
        for child in data:

            phase = search_phase(id=child['phase_id'])
            phase = f"{phase['Grado/Año']} {phase['Seccion']}"


            row = ft.DataRow([
                        ft.DataCell(ft.Container(ft.Text(child['name'], size=12, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(ft.Text(child['ci'], size=12, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(ft.Text(phase, size=12, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                    ])
            self.parent_children.rows.append(row)
        self.update()

    # Parents Functions
    def search_parent(self):
        '''Search a parent in the database'''
        if self.parent_ci.controls[0].value == '':
            dlg = ft.AlertDialog(
                content=ft.Text('Ingrese la cedula del representante'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
            )
            self.open_dlg(dlg)
        else:
            if self.parent_ci.controls[0].value[0] != 'v':
                ci = 'v' + self.parent_ci.controls[0].value
            else:
                ci = self.parent_ci.controls[0].value

            parent_info = parent_search(ci)
            if parent_info:
                self.parent_name.value = parent_info['name']
                self.parent_lastname.value = parent_info['lastname']
                self.parent_contact.controls[0].value = parent_info['phone1']
                self.parent_contact.controls[1].value = parent_info['phone2']
                self.update()

                parent_children = parent_student_search(parent_ci = parent_info['ID'])

                self.actual_parent = parent_info['ID']

                del self.parent_children.rows[:]

                if parent_children:
                    self.parent_rows(parent_children)

            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('El representante no se encuentra registrado'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
                )
                self.open_dlg(dlg)

    def search(self):
        '''Search a student in the database'''
        if self.search_bar.controls[0].value == '':
            self.cancel()
        else:
            # formatear el value poniendo una 'v' al inicio

            if self.search_bar.controls[0].value[0] != 'v':
                ci = 'v' + self.search_bar.controls[0].value
            else:
                ci = self.search_bar.controls[0].value

            student_info = student_search(ci)

            if student_info:
                parent_student = parent_student_search(student_ci = student_info['ID'])
                parent_info = parent_search(parent_student)

            if student_info and parent_info:
                phase = search_phase(id=student_info['phase_id'])

                phase = f"{phase['Grado/Año']} {phase['Seccion']}"


                self.student_ci.value = student_info['ci']
                self.student_name.value = student_info['name']
                self.student_lastname.value = student_info['lastname']
                self.student_birthdate.controls[0].value = student_info['birth_date']
                self.student_address.value = student_info['address']
                self.student_grade.value = phase
                self.student_date_inscription.controls[0].value = student_info['admission_date']
                self.student_status.value = student_info['status']

                self.parent_ci.controls[0].value = parent_info['ci']
                self.parent_name.value = parent_info['name']
                self.parent_lastname.value = parent_info['lastname']
                self.parent_contact.controls[0].value = parent_info['phone1']
                self.parent_contact.controls[1].value = parent_info['phone2']

                self.actual_parent = parent_info['ID']
                self.actual_student = student_info['ID']

                del self.parent_children.rows[:]

                parent_children = parent_student_search(parent_ci = parent_info['ID'])

                if parent_children:
                    self.parent_rows(parent_children)

                self.update()
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('El estudiante no se encuentra registrado'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
                )
                self.open_dlg(dlg)

    def add_student(self):
        '''Add a student to the database'''
        if self.validate():
            if self.student_ci.value[0] != 'v':
                ci = 'v' + self.student_ci.value
            else:
                ci = self.student_ci.value

            if self.parent_ci.controls[0].value[0] != 'v':
                ci_r = 'v' + self.parent_ci.controls[0].value
            else:
                ci_r = self.parent_ci.controls[0].value

            if validate_ci(ci):
                if ci_r != ci:
                    grado = self.student_grade.value.split(' ')[0] + ' ' + self.student_grade.value.split(' ')[1]
                    seccion = self.student_grade.value.split(' ')[2]
                    grade_id = search_phase(grado, seccion)['ID']

                    student_id = student_add(ci, self.student_name.value, self.student_lastname.value, self.student_birthdate.controls[0].value, self.student_address.value, grade_id,self.student_date_inscription.controls[0].value, self.student_status.value)

                    if self.parent_ci.controls[0].value[0] != 'v':
                        ci = 'v' + self.parent_ci.controls[0].value
                    else:
                        ci = self.parent_ci.controls[0].value

                    parent_id = parent_add(ci, self.parent_name.value, self.parent_lastname.value, self.parent_contact.controls[0].value, self.parent_contact.controls[1].value)
                    parent_student_add(parent_id, student_id)

                    phase = self.student_grade.value
                    phase_type = phase.split(' ')[1].split(' ')[0]

                    if phase_type == 'Año':
                        phase_type = 'Liceo'
                    elif phase_type == 'Grado':
                        phase_type = 'Colegio'
                    phase = phase.split(' ')[0] + ' ' + phase.split(' ')[1]

                    subjects_list = filter_subjects(phase, phase_type)

                    for subject in subjects_list:
                        grade_add(student_id, subject['ID'])
                    self.cancel()
                else:
                    dlg = ft.AlertDialog(
                        content=ft.Text('La cedula del representante no puede ser igual a la del estudiante'),
                        actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
                    )
                    self.open_dlg(dlg)
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('La cedula del estudiante ya se encuentra registrada'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
                )
                self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Faltan campos por llenar'),
                actions=[
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))
                ]
            )
            self.open_dlg(dlg)

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


    def delete_confirm(self):
        '''Delete a student from the database'''
        if self.validate():
            self.dlg = ft.AlertDialog(
                content=ft.Text('¿Esta seguro que desea eliminar al estudiante?'),
                actions=[
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.delete_student()),
                    ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(self.dlg))
                ]
            )
            self.open_dlg(self.dlg)
        else:
            self.dlg = ft.AlertDialog(
                content=ft.Text('Debe buscar un estudiante primero'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(self.dlg))]
            )
            self.open_dlg(self.dlg)

    def delete_student(self):
        '''Delete a student from the database'''
        if self.student_ci.value[0] != 'v':
            ci_e = 'v' + self.student_ci.value
        else:
            ci_e = self.student_ci.value

        if self.parent_ci.controls[0].value[0] != 'v':
            ci_r = 'v' + self.parent_ci.controls[0].value
        else:
            ci_r = self.parent_ci.controls[0].value

        id_p = parent_search(ci_r)['ID']
        id_s = student_search(ci_e)['ID']

        student_delete(ci_e)
        parent_student_delete(id_s, id_p)
        delete_grades_student(id_s)

        if validate_ci(id_p, False):
            parent_delete(ci_r)
        else:
            pass

        self.cancel()
        self.close(self.dlg)

    def edit_student(self):
        '''Edit a student from the database'''
        if self.validate():
            if self.student_ci.value[0] != 'v':
                ci = 'v' + self.student_ci.value
            else:
                ci = self.student_ci.value

            if self.parent_ci.controls[0].value[0] != 'v':
                ci_r = 'v' + self.parent_ci.controls[0].value
            else:
                ci_r = self.parent_ci.controls[0].value

            if validate_student(self.actual_student, ci):
                if ci_r != ci:
                    grado = self.student_grade.value.split(' ')[0] + ' ' + self.student_grade.value.split(' ')[1]
                    seccion = self.student_grade.value.split(' ')[2]
                    grade_id = search_phase(grado, seccion)['ID']

                    student_update(ci, self.student_name.value, self.student_lastname.value, self.student_birthdate.controls[0].value, self.student_address.value, grade_id,self.student_date_inscription.controls[0].value, self.actual_student, self.student_status.value)

                    if self.parent_ci.controls[0].value[0] != 'v':
                        ci = 'v' + self.parent_ci.controls[0].value
                    else:
                        ci = self.parent_ci.controls[0].value

                    parent_update(ci, self.parent_name.value, self.parent_lastname.value, self.parent_contact.controls[0].value, self.parent_contact.controls[1].value, self.actual_parent)
                    parent_student_update(self.student_ci.value,self.parent_ci.controls[0].value)
                    self.cancel()
                else:
                    dlg = ft.AlertDialog(
                        content=ft.Text('La cedula del representante no puede ser igual a la del estudiante'),
                        actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
                    )
                    self.open_dlg(dlg)
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('La cedula del estudiante ya se encuentra registrada'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
                )
                self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Faltan campos por llenar'),
                actions=[
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))
                ]
            )
            self.open_dlg(dlg)

    def print_student(self):
        '''Print a student from the database'''
        if self.validate():
            student_name = self.student_name.value
            student_lastname = self.student_lastname.value
            student_ci = self.student_ci.value
            student_phase = self.student_grade.value
            student_status = self.student_status.value

            parent_name = self.parent_name.value
            parent_lastname = self.parent_lastname.value
            parent_ci = self.parent_ci.controls[0].value
            parent_contact1 = self.parent_contact.controls[0].value

            data = [
                ["Estudiante", "Cedula", "Grado", "Status", "Representante", "Cedula", "Contacto"],
                [f"{student_name} {student_lastname}", student_ci, student_phase, student_status, f"{parent_name} {parent_lastname}", parent_ci, parent_contact1]
            ]

            dlg = ft.AlertDialog(
                content=ft.TextField(
                    width=200,
                    height=35,
                    label='Nombre del archivo',
                    hint_text='Ingresa el nombre del archivo',
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                ),
                actions=[
                    ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg), bgcolor='#6D62A1', color='#f3f4fa'),
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.print_confirmed(dlg, data), bgcolor='#6D62A1', color='#f3f4fa')
                ]
            )
            self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Debe buscar un estudiante primero'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
            )
            self.open_dlg(dlg)

    def print_confirmed(self, dlg, data):
        """
        Prints the student information.

        This method is called when the user confirms the printing of the student information. It retrieves the name of the file from the dialog box and calls the 'print_student' function from the 'print' module to print the student information.

        Args:
            dlg (Dialog): The dialog box that needs to be closed.
            data (list): A list of lists containing the student information to be printed.

        Returns:
            None
        """

        if dlg.content.value == '':
            dlg.actions[1].text = 'Rellene todos los campos'
            dlg.actions[1].bgcolor = '#ff0000'
            dlg.update()

            time.sleep(1)

            dlg.actions[1].text = 'Agregar'
            dlg.actions[1].bgcolor = '#6D62A1'
            dlg.update()
            return False

        file_name = dlg.content.value
        self.close(dlg)
        path_selector(file_name, data)


    def view(self):
        '''
        Change the view of the data table to display the list of students.

        Example Usage:
        students = Students(page, section)
        students.view()

        Inputs: None

        Flow:
        1. The view method is called.
        2. The body.content attribute of the Students class object is updated 
        to display the list of students using the Students_list class.
        3. The body.update() method is called to update the view.

        Outputs: None
        '''
        self.body.content = Studentslist(self.page, self.body)
        self.body.update()




class Studentslist(ft.UserControl):
    '''
    The `Studentslist` class is a user control class that represents a list of students.
    It provides a search bar and a data table with the list of students.

    The class includes methods for:
    - Searching for a student in the database.
    - Changing the view to display the student form.
    
    '''
    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.body = section

        self.scrol_pos = 10

        self.search_filter = None

        #* ------------------ Layout ------------------ *#
        # Create the Title
        self.title = ft.Text(
            'Lista de Estudiantes',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='center',
            weight='bold',
            size=20,
        )

        # Create the Clear Filter Button
        self.clear_filter_button = ft.Container(
            ft.Icon(ft.icons.FILTER_ALT_OFF, color='#f3f4fa', size=20),
            width=35,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.clear_filter(),
            border_radius=15,
            tooltip='Limpiar Filtro',
            visible=False,
        )

        self.print_list_button = ft.Container(
            ft.Icon(ft.icons.PRINT, color='#f3f4fa', size=20),
            width=50,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.print_list(),
            border_radius=15,
            tooltip='Imprimir Lista',
        )

        # Create the Search Bar
        self.search_bar = ft.Row([
            ft.TextField(
            width=500,
            height=35,
            label='Buscar Estudiante',
            hint_text='Ingresa un dato del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
        ),
            ft.Container(
                width=35,
                height=35,
                bgcolor= '#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.search_student(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the Data Table
        self.data_table = ft.DataTable(
            width=1100,
            border_radius=10,
            data_row_min_height=50,
            data_row_max_height=100,
            column_spacing=10,
            horizontal_margin=0,
            horizontal_lines= ft.BorderSide(1, '#6D62A1'),
            show_bottom_border=True,


            columns=[
                ft.DataColumn(ft.Container(ft.Text('Nombre', size=15, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Apellido', size=15, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Cedula', size=15, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Grado', size=15, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Fecha de Inscripcion', size=15, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Status', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
            ],
        )

        self.scrol = ft.Column([
            self.data_table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1100, height=490, on_scroll=lambda e: self.on_scroll(e))

        self.data_container = ft.Container(self.scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#6D62A1'), border_radius=10, width=1100, height=500)

        up_button = ft.FloatingActionButton(content=ft.Icon(ft.icons.ARROW_UPWARD, color='#f3f4fa', size=20), bgcolor='#6D62A1', on_click= lambda e: self.scrol.scroll_to(offset=0,duration=100), width=50, height=35)


        # Create the Button Change View
        self.change_view = ft.Container(
            ft.Icon(ft.icons.TABLE_ROWS_OUTLINED, color='#f3f4fa', size=20),
            width=50,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.view(),
            border_radius=15,
        )

        # Create the Layout
        layout = ft.Column([
            self.title,
            ft.Row([
                    self.search_bar,
                    self.clear_filter_button,
                    self.print_list_button,
                    self.change_view,
                    up_button
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            self.data_container,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

        self.show_students()

    def build(self):
        return self.content

    #^ ------------------ Functions ------------------ *#
    def search_student(self):
        '''Search a student in the database'''
        search = self.search_bar.controls[0].value

        if search == '':
            self.search_bar.controls[1].bgcolor = '#ff0000'
            self.search_bar.controls[1].content = ft.Text('Campo Vacio',size=15, color='#f3f4fa', font_family='Arial', text_align='center')
            self.search_bar.controls[1].width = 100
            self.update()
            time.sleep(1)
            self.search_bar.controls[1].bgcolor = '#6D62A1'
            self.search_bar.controls[1].content = ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20)
            self.search_bar.controls[1].width = 35
            self.update()
        else:
            self.search_filter = search
            self.data_table.rows.clear()

            list_students = filter_students_db(search)

            for student in list_students:
                phase = search_phase(id=student['phase_id'])
                phase = f"{phase['Grado/Año']} {phase['Seccion']}"
                row = ft.DataRow([
                    ft.DataCell(ft.Container(ft.Text(student['name'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(student['lastname'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(student['ci'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(phase, size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(student['admission_date'], size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(student['status'], size=12, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ], data=student['ID'], on_select_changed= lambda e: self.student_selected(e))
                self.data_table.rows.append(row)
            self.clear_filter_button.visible = True
            self.update()
            self.scrol.scroll_to(offset=0,duration=100)
            self.scrol_pos = check() + 1 # To avoid the scroll event

    def clear_filter(self):
        '''Clear the filter of the data table'''
        self.scrol.scroll_to(offset=0,duration=100)
        self.scrol_pos = 10
        self.search_bar.controls[0].value = ''
        del self.data_table.rows[:]
        self.clear_filter_button.visible = False
        self.search_filter = None
        self.update()
        self.show_students()

    def view(self, op=False):
        '''Change the view of the data table to the Students'''

        if op:
            self.body.content = Students(self.page, self.body)
            self.body.update()
        else:
            delete_tempdata_db()
            self.body.content = Students(self.page, self.body)
            self.body.update()

    def show_students(self):
        """
        Displays a list of students in a data table.

        Retrieves the student data from the database and creates a row for each student in the data table.

        Inputs:
        - None

        Outputs:
        - None
        """
        if check() < 10:
            list_students = get_students(0, check())
            last = check()
        else:
            list_students = get_students(0, 9)
            last = 9
        for i in range(0, last):
            phase = search_phase(id=list_students[i]['phase_id'])
            phase = f"{phase['Grado/Año']} {phase['Seccion']}"
            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(list_students[i]['name'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_students[i]['lastname'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_students[i]['ci'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(phase, size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_students[i]['admission_date'], size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_students[i]['status'], size=12, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center))
            ], data=list_students[i]['ID'], on_select_changed= lambda e: self.student_selected(e))
            self.data_table.rows.append(row)
        self.update()
    def on_scroll(self, e):
        """
        Called when the user scrolls to the bottom of the data table.
    
        Args:
            self (object): The instance of the Studentslist class.
            e (object): The event object that contains information about the scroll event.
        
        Returns:
            None
    
        """
        if e.pixels >= e.max_scroll_extent - 100:
            if sem.acquire(blocking=False):
                try:
                    # Obten estudiantes desde la posición actual hasta la posición + 9
                    list_students = get_students(self.scrol_pos, self.scrol_pos + 9)
                    #Verificar si la lista esta vacia
                    if list_students:
                        for student in list_students:
                            phase = search_phase(id=student['phase_id'])
                            phase = f"{phase['Grado/Año']} {phase['Seccion']}"

                            row = ft.DataRow([
                                ft.DataCell(ft.Container(ft.Text(student['name'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(student['lastname'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(student['ci'], size=12, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(phase, size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(student['admission_date'], size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(student['status'], size=12, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                            ], data=student['ID'], on_select_changed= lambda e: self.student_selected(e))
                            self.data_table.rows.append(row)
                        self.update()
                        self.scrol_pos += 10
                finally:
                    sem.release()
    def student_selected(self, e):
        """
        Perform actions when a student is selected from the data table.

        Args:
            e (object): The event object that contains information about the selected student.

        Returns:
            None

        Raises:
            None
        """
        search = student_search(e.control.data)

        if search:
            save_tempdata_db(str(search))
            self.view(True)
        else:
            pass

    def print_list(self):
        '''Print the list of students'''
        if self.search_filter:
            list_students = filter_students_db(self.search_filter)
        else:
            list_students = get_students(0, check())


        if not list_students:
            dlg = ft.AlertDialog(
                content=ft.Text('No hay estudiantes para generar la lista'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
            )
            self.open_dlg(dlg)
            return False

        data = [
            ["Nombre", "Apellido", "Cedula", "Grado", "Fecha de Inscripcion", "Status"],
        ]

        for student in list_students:
            phase = search_phase(id=student['phase_id'])
            phase = f"{phase['Grado/Año']} {phase['Seccion']}"
            data.append([student['name'], student['lastname'], student['ci'], phase, student['admission_date'], student['status']])

        dlg = ft.AlertDialog(
            content=ft.TextField(
                width=200,
                height=35,
                label='Nombre del archivo',
                hint_text='Ingresa el nombre del archivo',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            ),
            actions=[
                ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg), bgcolor='#6D62A1', color='#f3f4fa'),
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.print_confirmed(dlg, data), bgcolor='#6D62A1', color='#f3f4fa')
            ]
        )
        self.open_dlg(dlg)

    def print_confirmed(self, dlg, data):
        """
        Prints the list of students.

        This method is called when the user confirms the printing of the list of students. It retrieves the name of the file from the dialog box and calls the 'print_list' function from the 'print' module to print the list of students.

        Args:
            dlg (Dialog): The dialog box that needs to be closed.
            data (list): A list of lists containing the student information to be printed.

        Returns:
            None
        """
        if dlg.content.value == '':
            dlg.actions[1].text = 'Rellene todos los campos'
            dlg.actions[1].bgcolor = '#ff0000'
            dlg.update()

            time.sleep(1)

            dlg.actions[1].text = 'Agregar'
            dlg.actions[1].bgcolor = '#6D62A1'
            dlg.update()
            return False
        file_name = dlg.content.value
        self.close(dlg)
        path_selector(file_name, data)


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
