'''Students Page'''

# Libraries
import flet as ft
import datetime

class Students(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page


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
            on_click= lambda e: self.eliminate_parent(),
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
            hint_text='Ingresa el Nombre del Estudiante',
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
                on_click= lambda e: self.add_parent(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Eliminar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.eliminate_parent(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.eliminate_parent(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Imprimir',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.eliminate_parent(),
                border_radius=15,
            ),
            
            ft.Container(
                ft.Icon(ft.icons.TABLE_VIEW_OUTLINED, color='#f3f4fa', size=20),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.eliminate_parent(),
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
        self.student_birthdate.controls[0].read_only = False
        self.update()
        self.student_birthdate.controls[0].value = date
        self.student_birthdate.controls[0].read_only = True
        self.update()

    def change_date_inscription(self, date):
        self.student_date_inscription.controls[0].read_only = False
        self.update()
        self.student_date_inscription.controls[0].value = date
        self.student_date_inscription.controls[0].read_only = True
        self.update()

    def change_phase(self):
        pass

    def search_parent(self):
        pass

    def add_parent(self):
        pass

    def eliminate_parent(self):
        pass
        