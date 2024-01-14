'''Grades Page'''

# Libraries
import time
import flet as ft

# Database
from DB.Functions.student_parent_db import student_search
from DB.Functions.subjects_db import filter_subjects, search_subject_by_id
from DB.Functions.phases_db import search_phase, get_phases
from DB.Functions.grades_db import grade_add, filter_grades_by_period, filter_grades_by_student, get_periods, approve_student


class Grades(ft.UserControl):
    '''
    Clase para gestionar y mostrar las calificaciones de los estudiantes.

    Args:
    - page (ft.Page): Página a la que se vincula la instancia.

    Attributes:
    - page (ft.Page): Página vinculada a la instancia.
    - actual_student: ID del estudiante actual.
    - actual_ci: CI (Cédula de Identidad) del estudiante actual.
    - title (ft.Container): Contenedor del título.
    - student_name (ft.Container): Contenedor para el nombre del estudiante.
    - student_period (ft.Container): Contenedor para el periodo y filtro.
    - table (ft.DataTable): Tabla para mostrar las calificaciones.
    - body_container (ft.Container): Contenedor principal del cuerpo.
    - search_bar (ft.Row): Barra de búsqueda para estudiantes.
    - grades_buttons (ft.Row): Botones para editar y aprobar/desaprobar.
    
    Methods:
    - show_subjects_by_periods(period): Muestra las materias por periodo.
    - show_subjects_by_search(phase): Muestra las materias por búsqueda.
    - search_student(): Busca un estudiante por CI.
    - show_periods(): Muestra los periodos en el dropdown.
    - activate_fields(): Activa la edición de campos.
    - cancel(): Cancela la edición del estudiante.
    - add_edit_student_confirm(): Confirma la adición o edición del estudiante.
    - add_edit_student(dlg): Añade o edita un estudiante.
    - activate_approve_buttons(): Activa los botones de aprobar/desaprobar.
    - approve_student_confirm(): Confirma la aprobación del estudiante.
    - change(dlg, e): Cambia las opciones del dropdown.
    - drop_options(dlg): Agrega opciones al dropdown.
    - validate_dlg(dlg): Valida y procesa la información del diálogo.
    - approve_student(dlg, op): Aprueba al estudiante según la opción seleccionada.
    - open_dlg(dlg): Abre el diálogo.
    - close(dlg): Cierra el diálogo.

    '''
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.actual_student = None
        self.actual_ci = None

        #* ------------------ Header ------------------ *#
        # Create the Title
        self.title = ft.Container(
            content=ft.Text('Calificaciones',
            color='#4B4669',
            text_align='right',
            font_family='Arial',
            weight='bold',
            size=20,
            ),
            width=300,
            height=30,
            alignment=ft.alignment.center,
        )

        # Create the Student Name Label
        self.student_name = ft.Container(
            content=ft.Text(
                'Nombre del Estudiante',
                color='#4B4669',
                font_family='Arial',
                text_align='center',
                size=15,
            ),
            width=300,
            height=30,
            alignment=ft.alignment.center,
        )

        # Create the student date Dropdown
        self.student_period = ft.Container(content=ft.Row([
            ft.Dropdown(
                width=250,
                height=30,
                label='Periodo',
                hint_text='Selecciona el periodo',
                filled=True,
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=12),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            ),
            ft.Container(
                ft.Icon(ft.icons.FILTER_ALT, color='#f3f4fa', size=20),
                width=30,
                height=30,
                bgcolor='#6D62A1',
                on_click=lambda e: self.show_subjects_by_periods(self.student_period.content.controls[0].value),
                tooltip='Filtrar',
                border_radius=15,
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=300,
        height=30,
        alignment=ft.alignment.center_left,
        padding=ft.padding.only(left=20),
        )

        #* ------------------ Body ------------------ *#
        # Create the Table
        self.table = ft.DataTable(
            vertical_lines=ft.BorderSide(1, '#6D62A1'),

            columns=[
                ft.DataColumn(ft.Container(ft.Text('Materia', size=15, color='#4B4669', text_align='center'), width=145, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Momento 1', size=15, color='#4B4669', text_align='center'), width=145, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Momento 2', size=15, color='#4B4669', text_align='center'), width=145, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Momento 3', size=15, color='#4B4669', text_align='center'), width=145, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Nota Final', size=15, color='#4B4669', text_align='center'), width=145, alignment=ft.alignment.center)),
            ],
        )

        # Scroll the table
        scrol = ft.Column([
            self.table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1000, height=500)

        # Create the Table Container
        table_container = ft.Container(
            content=scrol,
            width=1000,
            height=420,
            bgcolor='#f3f4fa',
            border_radius=10,
            padding=ft.padding.only(top=10),
            border=ft.border.all(2, '#bec0e3'),
        )

        self.body_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.student_period,
                    self.title,
                    self.student_name,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                table_container
            ], alignment=ft.MainAxisAlignment.START, spacing=10, horizontal_alignment='center'),
            width=1020,
            height=480,
            bgcolor='#f3f4fa',
            border_radius=10,
            padding=ft.padding.only(top=10),
            border=ft.border.all(color='#6D62A1', width=2),
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
                on_click= lambda e: self.search_student(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the Grades Buttons (Add, Eliminate, Edit, Change View, Print)
        self.grades_buttons = ft.Row([
            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.activate_fields(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
                on_click= lambda e: self.add_edit_student_confirm(),
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
                ft.Text('Aprobar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#C0C1E3', # Color when the button is disabled
                alignment=ft.alignment.center,
                on_click= lambda e: self.approve_student_confirm(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Desaprobar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=100,
                height=35,
                bgcolor='#C0C1E3', # Color when the button is disabled
                alignment=ft.alignment.center,
                # on_click=, #TODO - Add the function to disapprove the student
                border_radius=15,
                disabled=True,
            ),

            ft.Container(
                ft.Icon(ft.icons.PRINT, color='#f3f4fa', size=20),
                width=50,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                # on_click= lambda e: self.print_student(), #TODO - Add the function to print the student
                border_radius=15,
                tooltip='Imprimir Notas',
            ),
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        footer = ft.Container(
            content=ft.Row([
            self.search_bar,
            self.grades_buttons
        ],alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=1025,
        height=100,
        border_radius=20,
        border=ft.border.all(2, '#6D62A1'),
        )


        #* ------------------ Layout ------------------ *#
        layout = ft.Row([
                ft.Column([
                    self.body_container,
                    footer
                ], spacing=20, alignment=ft.MainAxisAlignment.START, horizontal_alignment='center'),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # Add the layout to the page
        self.content = layout

    def build(self):
        return self.content

    #* ------------------ Class Functions ------------------ *#
    def show_subjects_by_periods(self, period):
        '''Show the subjects in the table'''
        del self.table.rows[:]

        list_grades = filter_grades_by_period(period, self.actual_student)

        for grade in list_grades:

            materia = search_subject_by_id(grade['Materia'])

            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(materia['Nombre'], size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
            ], data=grade['Materia'])
            if list_grades:
                row.cells[1].content.content.value = list_grades[list_grades.index(grade)]['Momento 1']
                row.cells[2].content.content.value = list_grades[list_grades.index(grade)]['Momento 2']
                row.cells[3].content.content.value = list_grades[list_grades.index(grade)]['Momento 3']
                row.cells[4].content.content.value = list_grades[list_grades.index(grade)]['Nota Final']
            self.table.rows.append(row)
        self.update()

    def show_subjects_by_search(self, phase):
        '''Show the subjects in the table'''

        del self.table.rows[:]
        list_grades = filter_grades_by_student(self.actual_student)
        phase_type = phase.split(' ')[1]

        if phase_type == 'Año':
            phase_type = 'Liceo'
        elif phase_type == 'Grado':
            phase_type = 'Colegio'

        list_subjects = filter_subjects(phase, phase_type)


        for subject in list_subjects:
            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(subject['Nombre'], size=12, color='#4B4669', text_align='center'), width=150, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
                ft.DataCell(ft.Container(
                    ft.TextField(
                        width=150,
                        height=45,
                        label='Nota',
                        hint_text='Ingresa la nota',
                        bgcolor='#f3f4fa',
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                        text_align=ft.TextAlign.CENTER,
                        input_filter=ft.InputFilter(regex_string='[0-9.]|[A-Z]'),
                        max_length=4,
                        dense=False,
                        counter_style=ft.TextStyle(color='red', size=0),
                    ),width=145, alignment=ft.alignment.center, padding=ft.padding.only(top=5))),
            ], data=subject['ID'])
            if list_grades:
                row.cells[1].content.content.value = list_grades[list_subjects.index(subject)]['Momento 1']
                row.cells[2].content.content.value = list_grades[list_subjects.index(subject)]['Momento 2']
                row.cells[3].content.content.value = list_grades[list_subjects.index(subject)]['Momento 3']
                row.cells[4].content.content.value = list_grades[list_subjects.index(subject)]['Nota Final']
            self.table.rows.append(row)

        self.update()


    #* ------------------ Search Functions ------------------ *#
    def search_student(self):
        '''Search a student'''
        if self.search_bar.controls[0].value == '':
            self.student_name.content.value = 'Nombre del Estudiante'
            del self.table.rows[:]
            self.update()
        else:
            # formatear el value poniendo una 'v' al inicio
            if self.search_bar.controls[0].value[0] != 'v':
                ci = 'v' + self.search_bar.controls[0].value
            else:
                ci = self.search_bar.controls[0].value

            student = student_search(ci)

            if student:
                phase = search_phase(id = student['phase_id'])
                self.student_name.content.value = student['name'] + ' ' + student['lastname']
                self.update()
                self.actual_student = student['ID']
                self.actual_ci = student['ci']
                self.show_periods()

                if self.student_period.content.controls[0].options != []:
                    self.show_subjects_by_periods(self.student_period.content.controls[0].value)
                else:
                    self.show_subjects_by_search(phase['Grado/Año'])

                self.grades_buttons.controls[3].disabled = False
                self.grades_buttons.controls[3].bgcolor = '#6D62A1'
                self.grades_buttons.controls[4].disabled = False
                self.grades_buttons.controls[4].bgcolor = '#6D62A1'
                self.activate_approve_buttons()
                self.update()
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('El estudiante no se encuentra registrado'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
                )
                self.open_dlg(dlg)

    def show_periods(self):
        '''Show the periods in the dropdown'''
        self.student_period.content.controls[0].options = []
        periods = get_periods(self.actual_student)
        if periods:
            for period in periods:
                self.student_period.content.controls[0].options.append(ft.dropdown.Option(f'{period}'))

            # Mostrar el periodo actual
            self.student_period.content.controls[0].value = periods[-1]
        else:
            self.student_period.content.controls[0].value = None

        self.update()



    #* ------------------ Edit Functions ------------------ *#

    def activate_fields(self):
        '''Activate the fields to edit the student'''

        if self.student_name.content.value != 'Nombre del Estudiante':
            self.body_container.disabled = False
            self.search_bar.visible = False
            self.grades_buttons.controls[0].visible = False
            self.grades_buttons.controls[1].visible = True
            self.grades_buttons.controls[2].visible = True
            self.grades_buttons.controls[3].visible = False
            self.grades_buttons.controls[4].visible = False
            self.grades_buttons.controls[5].visible = False

            self.update()
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Debe buscar un estudiante primero'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
            )
            self.open_dlg(dlg)

    def cancel(self):
        '''Cancel the edit of the student'''
        self.body_container.disabled = True
        self.search_bar.visible = True
        self.grades_buttons.controls[0].visible = True
        self.grades_buttons.controls[1].visible = False
        self.grades_buttons.controls[2].visible = False
        self.grades_buttons.controls[3].visible = True
        self.grades_buttons.controls[4].visible = True
        self.grades_buttons.controls[5].visible = True

        self.search_bar.controls[0].value = self.actual_ci
        self.search_student()

        self.update()

    def add_edit_student_confirm(self):
        '''Add or edit a student Confirm'''
        dlg = ft.AlertDialog(
            content=ft.Text('¿Estas seguro de guardar los cambios?'),
            actions=[
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.add_edit_student(dlg)),
                ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg))
            ]
        )
        self.open_dlg(dlg)

    def add_edit_student(self, dlg):
        '''Add or edit a student'''
        subject_grades = {
            'Student ID': None,
            'Subject ID': None,
            'Momento 1': None,
            'Momento 2': None,
            'Momento 3': None,
            'Nota Final': None,
        }

        for row in self.table.rows:
            subject_grades['Student ID'] = self.actual_student
            subject_grades['Subject ID'] = row.data
            subject_grades['Momento 1'] = row.cells[1].content.content.value
            subject_grades['Momento 2'] = row.cells[2].content.content.value
            subject_grades['Momento 3'] = row.cells[3].content.content.value
            subject_grades['Nota Final'] = row.cells[4].content.content.value

            grade_add(
                subject_grades['Student ID'],
                subject_grades['Subject ID'],
                subject_grades['Momento 1'],
                subject_grades['Momento 2'],
                subject_grades['Momento 3'],
                subject_grades['Nota Final'],
            )

        self.close(dlg)
        self.cancel()


    #* ------------------ Approve / Disapprove Functions ------------------ *#
    def activate_approve_buttons(self):
        '''Activate the approve and disapprove buttons if the student grades are complete'''
        content = self.table.rows
        for row in content:
            for cells in row.cells:
                if cells.content.content.value == '':
                    self.grades_buttons.controls[3].disabled = True
                    self.grades_buttons.controls[3].bgcolor = '#C0C1E3'
                    self.grades_buttons.controls[4].disabled = True
                    self.grades_buttons.controls[4].bgcolor = '#C0C1E3'
                    return


    def approve_student_confirm(self):
        '''Approve the student'''

        student_info = student_search(self.actual_ci)
        phase_info = search_phase(id = student_info['phase_id'])

        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Aprobar Estudiante', color='#4B4669', font_family='Arial', size=20),
                ft.Text(f"Etapa actual del estudiante: {phase_info['Grado/Año']} {phase_info['Seccion']}", color='#4B4669', font_family='Arial', size=15),
                ft.Dropdown(
                    width=300,
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
                ),

                ft.Dropdown(
                    width=300,
                    height=35,
                    label='Estado',
                    hint_text='Selecciona el estado',
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
                        ft.dropdown.Option('Graduado'),
                    ],
                    on_change= lambda e: self.change(dlg, e),
                ),

            ], spacing=10, width=300, height=150, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg), bgcolor='#6D62A1', color='#f3f4fa'),
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.validate_dlg(dlg), bgcolor='#6D62A1', color='#f3f4fa')
            ]
        )
        self.drop_options(dlg)
        self.open_dlg(dlg)

    def change(self, dlg, e):
        '''Change the dropdown options'''
        if e.control.value == 'Graduado':
            dlg.content.controls[2].disabled = True
            dlg.content.controls[2].value = None
        else:
            dlg.content.controls[2].disabled = False
        dlg.update()

    def drop_options(self, dlg):
        """
        Populates dropdown options in the dialog based on unique Grado/Año values from phases.

        Parameters:
            - self: The instance of the class containing this method.
            - dlg: The dialog instance to populate with dropdown options.

        Description:
            This function retrieves a list of phases, removes duplicate Grado/Año values with different Seccion,
            sorts the list by Grado/Año in descending order, and populates the dropdown options in the dialog with
            the formatted Grado/Año values.

        Usage:
            - Call this function to dynamically update dropdown options in the dialog.

        Example:
            drop_options(self, dialog_instance)
        """
        phases_list = get_phases()


        for phase in phases_list:
            dlg.content.controls[2].options.append(ft.dropdown.Option(f"{phase['Grado/Año']} {phase['Seccion']}"))

        self.update()


    def validate_dlg(self, dlg):
        """
        Validates the dialog's dropdown values and calls the approve_student() method if the values are valid.

        Parameters:
            - self: The instance of the class containing this method.
            - dlg: The dialog instance to validate.

        Description:
            This function checks if the dropdown values in the dialog are valid. If the values are valid, the
            approve_student() method is called. If the values are invalid, an error message is displayed.

        Usage:
            - Call this function to validate the dialog's dropdown values.

        Example:
            validate_dlg(self, dialog_instance)
        """
        if dlg.content.controls[3].value == 'Graduado':
            self.approve_student(dlg, dlg.content.controls[3].value)
        else:
            if dlg.content.controls[2].value is None:
                dlg.actions[1].text = 'Selecciona una Etapa'
                dlg.actions[1].bgcolor = '#ff0000'
                dlg.update()
                time.sleep(1)
                dlg.actions[1].text = 'Aceptar'
                dlg.actions[1].bgcolor = '#6D62A1'
                dlg.update()
            else:
                if dlg.content.controls[3].value == 'Activo' or dlg.content.controls[3].value == 'Retirado':
                    self.approve_student(dlg, dlg.content.controls[3].value)
                else:
                    dlg.actions[1].text = 'Selecciona un Estado'
                    dlg.actions[1].bgcolor = '#ff0000'
                    dlg.update()
                    time.sleep(1)
                    dlg.actions[1].text = 'Aceptar'
                    dlg.actions[1].bgcolor = '#6D62A1'
                    dlg.update()


    def approve_student(self, dlg, op):
        '''Approve the student'''
        if op == 'Graduado':
            approve_student(self.actual_student, op)
        else:
            phase_name = dlg.content.controls[2].value.split(' ')[0] + ' ' + dlg.content.controls[2].value.split(' ')[1]
            phase_section = dlg.content.controls[2].value.split(' ')[2]
            phase_id = search_phase(phase_name, phase_section)['ID']
            approve_student(self.actual_student, op, phase_id)
            self.search_bar.controls[0].value = self.actual_ci
            self.update()

        self.close(dlg)
        self.cancel()




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
