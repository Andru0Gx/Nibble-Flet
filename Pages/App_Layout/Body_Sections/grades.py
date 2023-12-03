'''Grades Page'''

# Libraries
import flet as ft

class Grades(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        #* ------------------ Header ------------------ *#
        # Create the Title
        self.title = ft.Text(
            'Notas',
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
                on_click= lambda e: self.search_student(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the Student Name Label
        self.student_name = ft.Text(
            'Nombre del Estudiante',
            color='#4B4669',
            font_family='Arial',
            width = 300,
            text_align='center',
            size=15,
        )

        # Create the Student ID Label
        self.student_id = ft.Text(
            'Cedula del Estudiante',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='center',
            weight='bold',
            size=20,
        )

        #* ------------------ Body ------------------ *#
        # Create the Table
        self.table = ft.DataTable(
            vertical_lines=ft.BorderSide(1, '#6D62A1'),

            columns=[
                ft.DataColumn(ft.Container(ft.Text('Materia', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Momento 1', size=15, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Momento 2', size=15, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Momento 3', size=15, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Nota Final', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
            ],
        )

        # Scroll the table
        scrol = ft.Column([
            self.table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1000, height=500)

        # Create the Table Container
        self.table_container = ft.Container(
            content=scrol,
            width=1000,
            height=500,
            bgcolor='#f3f4fa',
            border_radius=10,
            padding=ft.padding.only(top=10),
            border=ft.border.all(color='#6D62A1', width=2),
        )

        #* ------------------ Layout ------------------ *#
        layout = ft.Column([
                self.title,
                ft.Row([
                    self.search_bar,
                    self.student_name,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                self.table_container,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment='center'
        )

        # Add the layout to the page
        self.content = layout

    def build(self):
        return self.content

    #* ------------------ Class Functions ------------------ *#
    def search_student(self):
        '''Search a student'''
