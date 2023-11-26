'''Students Page'''

# Libraries
import datetime
import flet as ft

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
            width = 600,
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
        )

        # Create the student birthdate text field
        self.student_birthdate = ft.Row([
            ft.TextField(
                width=195,
                height=35,
                label='Fecha de Nacimiento',
                hint_text='Selecciona la fecha',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
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
                width=195,
                height=35,
                label='Fecha de Inscripcion',
                hint_text='Selecciona la fecha',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
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

        # Create the student grade text field
        self.student_grade = ft.TextField(
            width=500,
            height=35,
            label='Etapa (Grado/Año)',
            hint_text='Ingresa el Grado del Estudiante',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the change student button
        self.change_student_button = ft.Container(
            ft.Text('Cambiar Etapa',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=150,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.change_phase(),
            border_radius=15,
        )

        # Create the layout
        layout_student = ft.Container(
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
            self.student_grade,
            self.change_student_button
        ], alignment=ft.MainAxisAlignment.START, spacing=20),
        width=550,
        height=500,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
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
            width=450,
            height=35,
            label='Cedula del Representante',
            hint_text='Ingresa la Cedula del Representante',
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
                on_click= lambda e: self.search_parent(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the parent contact text field
        self.parent_contact = ft.Row([
            ft.TextField(
                width=240,
                height=35,
                label='Contacto 1',
                hint_text='Ingresa el contacto',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
            ),

            ft.TextField(
                width=240,
                height=35,
                label='Contacto 2 (Opcional)',
                hint_text='Ingresa el contacto',
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
            )
        ], spacing=20)

        # Create the Add and eliminate button
        self.buttons = ft.Row([
        ft.Container(
            ft.Text('Agregar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=150,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.add_parent(),
            border_radius=15,
        ),

        # Create the Elimnate button
        ft.Container(
            ft.Text('Eliminar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=150,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.delete_parent(),
            border_radius=15,
        )
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        # Create the Layout
        layout_parent = ft.Container(
            content=ft.Column([
            self.parent_title,
            self.parent_name,
            self.parent_lastname,
            self.parent_ci,
            self.parent_contact,
            self.buttons
        ],alignment=ft.MainAxisAlignment.START, spacing=20),
        width=550,
        height=500,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        )

        #* ------------------ Footer ------------------ *#
        # Create the Search Bar
        self.search_bar = ft.Row([
            ft.TextField(
            width=500,
            height=35,
            label='Buscar Estudiante',
            hint_text='Ingresa la cedula del Estudiante',
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
                on_click= lambda e: self.search_parent(),
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
                on_click= lambda e: self.add_student(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Eliminar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.delete_student(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.edit_student(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Imprimir',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.print_student(),
                border_radius=15,
            ),

            ft.Container(
                ft.Icon(ft.icons.TABLE_ROWS_OUTLINED, color='#f3f4fa', size=20),
                width=80,
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
        width=1110,
        height=100,
        border_radius=20,
        border=ft.border.all(2, '#6D62A1'),
        )



        #* ------------------ Layout ------------------ *#
        # Create the layout
        layout = ft.Column([
            ft.Row([
                layout_student,
                layout_parent
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            footer
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

    def build(self):
        return self.content


    #^ ------------------ Functions ------------------ *#
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

    # Parents Functions
    def search_parent(self):
        '''Search a parent in the database'''

    def add_parent(self):
        '''Add a parent to the database'''


    # Students Functions
    def change_phase(self):
        '''Change the phase of the student'''

    def delete_parent(self):
        '''Delete a parent from the database'''

    def add_student(self):
        '''Add a student to the database'''
        #TODO - buscar al representante en la base de datos (Cedula)
        # En caso de que no este registrado, agregarlo y luego agregar al estudiante
        # En caso de que si este registrado, agregar al estudiante

    def delete_student(self):
        '''Delete a student from the database'''

    def edit_student(self):
        '''Edit a student from the database'''

    def print_student(self):
        '''Print a student from the database'''

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
                ft.DataColumn(ft.Container(ft.Text('Grado', size=15, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Fecha de Inscripcion', size=15, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
            ],
        )

        scrol = ft.Column([
            self.data_table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1100, height=490)

        self.data_container = ft.Container(scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#6D62A1'), border_radius=10, width=1100, height=500)

        up_button = ft.FloatingActionButton(icon=ft.icons.ARROW_UPWARD, bgcolor='#6D62A1', on_click= lambda e: scrol.scroll_to(offset=0,duration=100), width=50, height=35)


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
                    self.change_view,
                    up_button
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            self.data_container,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

    def build(self):
        return self.content

    #^ ------------------ Functions ------------------ *#
    def search_student(self):
        '''Search a student in the database'''

    def view(self):
        '''Change the view of the data table to the Students'''
        self.body.content = Students(self.page, self.body)
        self.body.update()
        