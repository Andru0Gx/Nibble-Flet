'''Teachers Page'''

# Libraries
import datetime
import flet as ft

class Teachers(ft.UserControl):
    '''Teachers Page

    Sections:
    - Header
    - Body

    Header:
    - Title
    - Button to add a new teacher
    - Button to show the teachers
    - Button to show the teachers

    Body:
    - Container to show the content
    '''

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        #* ------------------ DatePicker ------------------ *#
        self.date_picker_birthdate = ft.DatePicker(
            first_date= datetime.datetime(1800,1,1),
            last_date= datetime.datetime(3000,1,1),
            on_change= lambda e: self.change_birthdate(self.date_picker_birthdate.value.strftime("%d / %m / %Y")),
        )

        self.page.add(self.date_picker_birthdate)

        #* ------------------ Layout - Profesor ------------------ *#

        # Create the title
        title = ft.Text(
            'Registrar Profesor',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='center',
            weight='bold',
            size=20,
        )

        # Create the text field for the name
        self.teacher_name = ft.TextField(
            width=500,
            height=35,
            label='Nombre del Profesor',
            hint_text='Ingresa el Nombre del Profesor',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the text field for the last name
        self.teacher_last_name = ft.TextField(
            width=500,
            height=35,
            label='Apellido del Profesor',
            hint_text='Ingresa el Apellido del Profesor',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the text field for the ci
        self.teacher_ci = ft.TextField(
            width=500,
            height=35,
            label='Cedula del Profesor',
            hint_text='Ingresa la Cedula del Profesor',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the text field for the phone
        self.teacher_contact = ft.Row([
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

        # Create the text field for the email
        self.teacher_email = ft.TextField(
            width=500,
            height=35,
            label='Correo Electronico',
            hint_text='Ingresa el Correo Electronico',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the text field for the address
        self.teacher_address = ft.TextField(
            width=500,
            height=35,
            label='Direccion',
            hint_text='Ingresa la Direccion',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        # Create the text field for the birthday
        self.teacher_birthday = ft.Row([
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

        # Layout for the teacher
        self.teacher_layout = ft.Container(
            content=ft.Column([
                title,
                self.teacher_name,
                self.teacher_last_name,
                self.teacher_ci,
                self.teacher_birthday,
                self.teacher_contact,
                self.teacher_email,
                self.teacher_address,
        ],alignment=ft.MainAxisAlignment.START, spacing=20),
        width=550,
        height=500,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        )

        #* ------------------ Layout - Documents / Subject ------------------ *#
        # Create the title
        title_documents = ft.Text(
            'Copia Del Titulo',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='center',
            weight='bold',
            size=20,
        )

        # Create the Buttons (ADD, DELETE, VIEW)
        self.documents_buttons = ft.Row([
            ft.Container(
                ft.Icon(ft.icons.ADD, color='#f3f4fa', size=20),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
            ),

            ft.Container(
                ft.Icon(ft.icons.DELETE, color='#f3f4fa', size=20),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
            ),

            ft.Container(
                ft.Icon(ft.icons.VISIBILITY_OUTLINED, color='#f3f4fa', size=20),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
            )
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        # Create the title
        title_subject = ft.Text(
            'Asignar Materia',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='center',
            weight='bold',
            size=20,
        )

        # Create the text field for the subject
        self.teacher_subject = ft.Row([
        ft.TextField(
            width=400,
            height=35,
            label='Materia',
            hint_text='Ingresa la Materia',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        ),
        ft.Container(
                ft.Text('Asignar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
            )
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        # Subject Datalist
        self.subject_list = ft.DataTable(
            width= 500,
            border_radius=10,
            data_row_min_height=25,
            data_row_max_height=50,
            column_spacing=10,
            horizontal_margin=0,
            horizontal_lines= ft.BorderSide(1, '#6D62A1'),
            show_bottom_border=True,


            columns=[
                ft.DataColumn(ft.Container(ft.Text('Materias Asignadas', size=15, color='#4B4669', text_align='center'), width=500, alignment=ft.alignment.center)),
            ],
        )

        scrol = ft.Column([
            self.subject_list,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=500, height=190)

        self.data_container = ft.Container(scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#bec0e3'), border_radius=10, width=500, height=200)


        # Layout for the documents / subject
        layout_documents_subject = ft.Container(
            content=ft.Column([
            title_documents,
            self.documents_buttons,
            ft.Divider(),
            title_subject,
            self.teacher_subject,
            self.data_container
        ],alignment=ft.MainAxisAlignment.START, spacing=20),
        width=550,
        height=500,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        )




        #* ------------------ Layout - Footer ------------------ *#

        # Create the Search Bar
        self.search_bar = ft.Row([
            ft.TextField(
            width=500,
            height=35,
            label='Buscar Profesor',
            hint_text='Ingresa la cedula del profesor',
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
                on_click= lambda e: self.search_teacher(),
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
                on_click= lambda e: self.add_teacher(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Eliminar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.delete_teacher(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.edit_teacher(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Imprimir',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.print_teacher(),
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
        # Create the layout for the page
        layout = ft.Column([
            ft.Row([
                self.teacher_layout,
                layout_documents_subject
            ], alignment=ft.MainAxisAlignment.CENTER,spacing=20),
            footer
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

    def build(self):
        return self.content



    #* ------------------ Teacher Functions ------------------ *#
    def change_birthdate(self, date):
        '''Change the birthdate'''
        self.teacher_birthday.controls[0].read_only = False
        self.update()
        self.teacher_birthday.controls[0].value = date
        self.teacher_birthday.controls[0].read_only = True
        self.update()

    def search_teacher(self):
        '''Search a teacher'''
        print('Search Teacher')

    def add_teacher(self):
        '''Add a new teacher'''
        print('Add Teacher')

    def delete_teacher(self):
        '''Delete a teacher'''
        print('Delete Teacher')

    def edit_teacher(self):
        '''Edit a teacher'''
        print('Edit Teacher')

    def print_teacher(self):
        '''Print a teacher'''
        print('Print Teacher')

    def view(self):
        '''View the teachers'''
        print('View Teachers')
