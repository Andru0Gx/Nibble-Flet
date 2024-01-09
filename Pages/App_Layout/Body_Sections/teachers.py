'''Teachers Page'''

# Libraries
import datetime
import flet as ft

# Database
from DB.Functions.teacher_db import validate_ci
from DB.Functions.teacher_db import teacher_add, subject_add_to_teacher
from DB.Functions.teacher_db import teacher_search, teacher_subjects_search
from DB.Functions.teacher_db import teacher_delete, teacher_subject_delete, teacher_and_subjects_delete
from DB.Functions.teacher_db import teacher_update



from DB.Functions.subjects_db import get_subjects


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

    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.body = section

        self.actual_teacher = None

        self.del_log = []
        self.add_log = []

        self.subject_teacher_info = {
            'ID': None,
            'Name': None,
            'Teacher ID': None,
        }

        self.subject_log = None

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
            width = 500,
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
            input_filter=ft.InputFilter(regex_string='[0-9]'),
        )

        # Create the text field for the phone
        self.teacher_contact = ft.Row([
            ft.TextField(
                width=218,
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
                width=218,
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
        width=500,
        height=480,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        disabled=True,
        )

        #* ------------------ Layout - Subject ------------------ *#

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
        ft.Dropdown(
            width=350,
            height=35,
            label='Materia',
            hint_text='Selecciona la materia',
            filled=True,
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            on_change= lambda e: self.change_log(e),
        ),
        ft.Container(
                ft.Text('Asignar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
                on_click= lambda e: self.subject_confirm(),
            )
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        # Subject Datalist
        self.subject_list = ft.DataTable(
            width= 500,
            border_radius=10,
            data_row_min_height=25,
            data_row_max_height=50,
            column_spacing=0,
            horizontal_margin=0,
            horizontal_lines= ft.BorderSide(1, '#6D62A1'),
            show_bottom_border=True,

            columns=[
                ft.DataColumn(ft.Container(ft.Text('Materias Asignadas', size=15, color='#4B4669', text_align='left'), width=300, alignment=ft.alignment.center_left, padding=ft.padding.only(left=30))),
                ft.DataColumn(ft.Container(ft.Text('Eliminar', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
            ],
        )

        scrol = ft.Column([
            self.subject_list,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=500, height=300)

        self.data_container = ft.Container(scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#bec0e3'), border_radius=10, width=500, height=310)


        # Layout for the documents / subject
        self.layout_subject = ft.Container(
            content=ft.Column([
            title_subject,
            self.teacher_subject,
            self.data_container
        ],alignment=ft.MainAxisAlignment.START, spacing=20),
        width=500,
        height=480,
        border_radius=20,
        padding=ft.padding.all(20),
        border=ft.border.all(2, '#6D62A1'),
        disabled=True,
        )




        #* ------------------ Layout - Footer ------------------ *#

        # Create the Search Bar
        self.search_bar = ft.Row([
            ft.TextField(
            width=450,
            height=35,
            label='Buscar Profesor',
            hint_text='Ingresa la cedula del profesor',
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
                on_click= lambda e: self.search_teacher(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the Teachers Buttons (Add, Eliminate, Edit, Change View, Print)
        self.teachers_buttons = ft.Row([
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
                on_click= lambda e: self.add_teacher(),
                visible=False,
            ),

            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                border_radius=15,
                on_click= lambda e: self.confirm_edit(),
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
                on_click= lambda e: self.print_teacher(),
                border_radius=15,
                tooltip='Imprimir Profesor',
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
            self.teachers_buttons
        ],alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=1025,
        height=100,
        border_radius=20,
        border=ft.border.all(2, '#6D62A1'),
        )

        #* ------------------ Layout ------------------ *#
        # Create the layout for the page
        layout = ft.Column([
            ft.Row([
                self.teacher_layout,
                self.layout_subject
            ], alignment=ft.MainAxisAlignment.CENTER,spacing=20),
            footer
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

        # self.drop_options()

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

    def drop_options(self, data = None):
        '''Add the options to the dropdown'''
        del self.teacher_subject.controls[0].options[:]
        subjects_list = get_subjects()

        if data:
            for subject in subjects_list:
                for subject_t in data:
                    if subject['ID'] == subject_t['ID']:
                        subjects_list.remove(subject)
                        subjects_list.insert(0, {'ID': None, 'Nombre': None})

            for subject in subjects_list:
                if subject['ID'] != None:
                    self.teacher_subject.controls[0].options.append(ft.dropdown.Option(f"{subject['ID']} {subject['Nombre']}"))
        else:
            for subject in subjects_list:
                self.teacher_subject.controls[0].options.append(ft.dropdown.Option(f"{subject['ID']} {subject['Nombre']}"))
        self.update()

    def activate_fields(self, op):
        '''Activates all the fields in the teacher forms'''
        if op == 1:
            self.teacher_layout.disabled = False

            self.teacher_name.value = ''
            self.teacher_last_name.value = ''
            self.teacher_ci.value = ''
            self.teacher_contact.controls[0].value = ''
            self.teacher_contact.controls[1].value = ''
            self.teacher_email.value = ''
            self.teacher_address.value = ''
            self.teacher_birthday.controls[0].value = ''

            self.search_bar.controls[0].value = ''

            del self.subject_list.rows[:]

            self.search_bar.visible = False
            self.teachers_buttons.controls[0].visible = False
            self.teachers_buttons.controls[1].visible = False
            self.teachers_buttons.controls[2].visible = False
            self.teachers_buttons.controls[3].visible = True
            self.teachers_buttons.controls[4].visible = False
            self.teachers_buttons.controls[5].visible = True
            self.teachers_buttons.controls[6].visible = False
            self.teachers_buttons.controls[7].visible = False

        elif op == 2:
            if self.validate():
                self.teacher_layout.disabled = False
                self.layout_subject.disabled = False

                self.search_bar.visible = False
                self.teachers_buttons.controls[0].visible = False
                self.teachers_buttons.controls[1].visible = False
                self.teachers_buttons.controls[2].visible = False
                self.teachers_buttons.controls[3].visible = False
                self.teachers_buttons.controls[4].visible = True
                self.teachers_buttons.controls[5].visible = True
                self.teachers_buttons.controls[6].visible = False
                self.teachers_buttons.controls[7].visible = False

                data = teacher_subjects_search(self.actual_teacher)
                self.drop_options(data)

            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('Debe buscar un profesor primero'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
                )
                self.open_dlg(dlg)
        self.update()

    def validate(self):
        '''Validate if the teacher exists'''
        if self.teacher_name.value == '' or self.teacher_last_name.value == '' or self.teacher_ci.value == '' or self.teacher_contact.controls[0].value == '' or self.teacher_email.value == '' or self.teacher_address.value == '' or self.teacher_birthday.controls[0].value == '':
            return False
        else:
            return True

    def cancel(self):
        '''Cancels the registration of a teacher'''
        self.teacher_layout.disabled = True
        self.layout_subject.disabled = True

        self.teacher_name.value = ''
        self.teacher_last_name.value = ''
        self.teacher_ci.value = ''
        self.teacher_contact.controls[0].value = ''
        self.teacher_contact.controls[1].value = ''
        self.teacher_email.value = ''
        self.teacher_address.value = ''
        self.teacher_birthday.controls[0].value = ''

        self.teacher_subject.controls[0].value = ''

        self.search_bar.controls[0].value = ''

        self.teachers_buttons.controls[0].visible = True
        self.teachers_buttons.controls[1].visible = True
        self.teachers_buttons.controls[2].visible = True
        self.teachers_buttons.controls[3].visible = False
        self.teachers_buttons.controls[4].visible = False
        self.teachers_buttons.controls[5].visible = False
        self.teachers_buttons.controls[6].visible = True
        self.teachers_buttons.controls[7].visible = True

        self.search_bar.visible = True

        self.actual_teacher = None

        del self.subject_list.rows[:]

        self.update()

        self.del_log = []
        self.add_log = []
        self.subject_log = None



    def search_teacher(self):
        '''Search a teacher'''
        if self.search_bar.controls[0].value == '':
            self.cancel()
        else:
            if self.search_bar.controls[0].value[0] != 'v':
                ci = 'v' + self.search_bar.controls[0].value
            else:
                ci = self.search_bar.controls[0].value

            teacher_info = teacher_search(ci)

            if teacher_info:
                teacher_subjects = teacher_subjects_search(teacher_info['ID'])
            
                self.teacher_name.value = teacher_info['Name']
                self.teacher_last_name.value = teacher_info['Last_Name']
                self.teacher_ci.value = teacher_info['CI']
                self.teacher_contact.controls[0].value = teacher_info['Phone1']
                self.teacher_contact.controls[1].value = teacher_info['Phone2']
                self.teacher_email.value = teacher_info['Email']
                self.teacher_address.value = teacher_info['Address']
                self.teacher_birthday.controls[0].value = teacher_info['Birth_Date']

                self.actual_teacher = teacher_info['ID']

                del self.subject_list.rows[:]

                if teacher_subjects:
                    self.subjects_row(teacher_subjects)

                self.update()
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('El profesor no se encuentra registrado'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
                )
                self.open_dlg(dlg)



    def add_teacher(self):
        '''Add a new teacher'''
        if self.validate():
            if self.teacher_ci.value[0] != 'v':
                ci = self.teacher_ci.value = 'v' + self.teacher_ci.value

            if validate_ci(ci):
                self.actual_teacher = teacher_add(ci, self.teacher_name.value, self.teacher_last_name.value, self.teacher_birthday.controls[0].value, self.teacher_contact.controls[0].value, self.teacher_contact.controls[1].value, self.teacher_address.value, self.teacher_email.value)
                self.cancel()
            else:
                dlg = ft.AlertDialog(
                    content=ft.Text('La cedula del profesor ya esta registrada'),
                    actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
                )
                self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Debe llenar todos los campos'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
            )
            self.open_dlg(dlg)


    def delete_confirm(self):
        '''Delete a teacher from the database'''
        if self.validate():
            dlg = ft.AlertDialog(
                content=ft.Text('¿Esta seguro que desea eliminar al profesor?'),
                actions=[
                    ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.delete_teacher(dlg)),
                    ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg))
                ]
            )
            self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Debe buscar un profesor primero'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
            )
            self.open_dlg(dlg)

    def delete_teacher(self, dlg):
        '''Delete a teacher'''
        if self.teacher_ci.value[0] != 'v':
            ci = self.teacher_ci.value = 'v' + self.teacher_ci.value
        else:
            ci = self.teacher_ci.value
        teacher_delete(ci)
        teacher_and_subjects_delete(self.actual_teacher)
        self.close(dlg)
        self.cancel()

    def confirm_edit(self):
        '''Confirm the changes in the teacher'''
        if self.validate():
            dlg = ft.AlertDialog(
                    content=ft.Text('Pulse aceptar para confirmar los cambios'),
                    actions=[
                        ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.edit_teacher(dlg)),
                        ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg))
                    ]
                )
            self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Debe llenar todos los campos'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))],
            )
            self.open_dlg(dlg)

    def edit_teacher(self, dlg):
        '''Edit a teacher'''
        if self.del_log:
            for subject in self.del_log:
                teacher_subject_delete(self.actual_teacher, subject['ID'])

        if self.add_log:
            for subject in self.add_log:
                subject_add_to_teacher(self.actual_teacher, subject['ID'])


        if self.teacher_ci.value[0] != 'v':
            ci = self.teacher_ci.value = 'v' + self.teacher_ci.value
        else:
            ci = self.teacher_ci.value

        teacher_update(ci, self.teacher_name.value, self.teacher_last_name.value, self.teacher_birthday.controls[0].value, self.teacher_contact.controls[0].value, self.teacher_contact.controls[1].value, self.teacher_address.value, self.teacher_email.value, self.actual_teacher)
        self.close(dlg)
        self.cancel()


    def print_teacher(self):
        '''Print a teacher'''
        print('Print Teacher')


    #* ------------------ Subject Functions ------------------ *#
    def change_log(self, e):
        '''Change the log'''
        self.subject_log = e

    def subject_edit_set(self, id, name):
        return ft.Row([
            # Create the button to delete the subject
            ft.IconButton(icon=ft.icons.DELETE, icon_color='#ff0000', width=35, height=35, icon_size=20, on_click= lambda e: self.subject_confirm_delete(e), data=[id, name]),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    def subjects_row(self, data):
        for subject in data:
            row = ft.DataRow([
                        ft.DataCell(ft.Container(ft.Text(subject['Name'], size=12, color='#4B4669', text_align='center'), width=300, alignment=ft.alignment.center_left, padding=ft.padding.only(left=30))),
                        ft.DataCell(ft.Container(self.subject_edit_set(subject['ID'], subject['Name']), width=100, alignment=ft.alignment.center))
                    ])
            self.subject_list.rows.append(row)
        self.update()

    def subject_confirm(self):
        if self.teacher_subject.controls[0].value is not None:
            self.add_subject()
        else:
            dlg = ft.AlertDialog(
                content=ft.Text('Debe seleccionar una materia'),
                actions=[ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg))]
            )
            self.open_dlg(dlg)

    def add_subject(self):
        '''Add a subject to the teacher'''
        subject_id = self.teacher_subject.controls[0].value.split(' ')[0]

        # delete the option from the dropdown
        for option in self.teacher_subject.controls[0].options:
            if option.key == self.subject_log.control.value:
                self.teacher_subject.controls[0].options.remove(option)

        self.subject_teacher_info['ID'] = subject_id
        self.subject_teacher_info['Name'] = self.teacher_subject.controls[0].value.split(' ', 1)[1]
        self.subject_teacher_info['Teacher ID'] = self.actual_teacher

        self.add_log.append(self.subject_teacher_info.copy())

        del self.subject_list.rows[:]
        teacher_subjects = teacher_subjects_search(self.actual_teacher)

        for subject in self.del_log:
            if subject['ID'] == subject_id:
                self.del_log.remove(subject)

        for subject in self.add_log:
            teacher_subjects.append(subject)
        
        for subject in self.del_log:
            subject_t = {
                'ID': subject['ID'],
                'Name': subject['Name'],
            }

            if subject_t in teacher_subjects:
                teacher_subjects.remove(subject_t)

        self.subjects_row(teacher_subjects)
        self.teacher_subject.controls[0].value = ''

        self.update()

    def subject_confirm_delete(self, e):
        '''Delete a subject from the teacher'''
        data = e.control.data
        dlg = ft.AlertDialog(
            content=ft.Text('¿Esta seguro que desea eliminar la materia?'),
            actions=[
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.delete_subject(data, dlg)),
                ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg))
            ]
        )
        self.open_dlg(dlg)

    def delete_subject(self, data, dlg):
        '''Delete a subject from the teacher'''

        drop = f'{data[0]} {data[1]}'

        # add the option to the dropdown
        self.teacher_subject.controls[0].options.append(ft.dropdown.Option(drop))

        self.subject_teacher_info['ID'] = data[0]
        self.subject_teacher_info['Name'] = data[1]
        self.subject_teacher_info['Teacher ID'] = self.actual_teacher

        self.del_log.append(self.subject_teacher_info.copy())

        for subject in self.add_log:
            if subject['ID'] == data[0]:
                self.add_log.remove(subject)

        del self.subject_list.rows[:]
        teacher_subjects = teacher_subjects_search(self.actual_teacher)

        for subject in self.del_log:
            subject_t = {
                'ID': subject['ID'],
                'Name': subject['Name'],
            }

            if subject_t in teacher_subjects:
                teacher_subjects.remove(subject_t)

        for subject in self.add_log:
            teacher_subjects.append(subject)

        self.subjects_row(teacher_subjects)
        self.update()

        self.close(dlg)


    #* ------------------ DGL Functions ------------------ *#
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



    #* ------------------ Functions ------------------ *#
    def view(self):
        '''
        Updates the content of the body section of the Teachers page with a new instance of the Teacherslist class.

        Inputs:
        - self: The instance of the Teachers class.

        Outputs:
        - None
        '''
        self.body.content = Teacherslist(self.page, self.body)
        self.body.update()



class Teacherslist(ft.UserControl):

    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.body = section

        #* ------------------ Layout ------------------ *#
        # Create the Title
        self.title = ft.Text(
            'Lista de Profesores',
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
            label='Buscar Profesor',
            hint_text='Ingresa un dato del Profesor',
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
                ft.DataColumn(ft.Container(ft.Text('Nombre', size=15, color='#4B4669', text_align='center'), width=250, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Apellido', size=15, color='#4B4669', text_align='center'), width=250, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Cedula', size=15, color='#4B4669', text_align='center'), width=250, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Contacto 1', size=15, color='#4B4669', text_align='center'), width=250, alignment=ft.alignment.center)),
            ],
        )

        scrol = ft.Column([
            self.data_table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1100, height=490)

        self.data_container = ft.Container(scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#6D62A1'), border_radius=10, width=1100, height=500)

        up_button = ft.FloatingActionButton(content=ft.Icon(ft.icons.ARROW_UPWARD, color='#f3f4fa', size=20), bgcolor='#6D62A1', on_click= lambda e: scrol.scroll_to(offset=0,duration=100), width=50, height=35)


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

        self.print_teacher_button = ft.Container(
                ft.Icon(ft.icons.PRINT, color='#f3f4fa', size=20),
                width=50,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.print_teacher_list(),
                border_radius=15,
                tooltip='Imprimir Lista',
            )

        self.clear_filter_button = ft.Container(
                ft.Icon(ft.icons.CLEAR_ALL, color='#f3f4fa', size=20),
                width=50,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.clear_filter(),
                border_radius=15,
                tooltip='Limpiar Filtro',
                visible=False,
            )

        # Create the Layout
        layout = ft.Column([
            self.title,
            ft.Row([
                    self.search_bar,
                    self.clear_filter_button,
                    self.print_teacher_button,
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
    def search_teacher(self):
        '''Search a teacher in the database'''

    def view(self):
        '''Change the view of the data table to the Teacher form'''
        self.body.content = Teachers(self.page, self.body)
        self.body.update()

    def print_teacher_list(self):
        '''Print the list of teachers'''


    def clear_filter(self):
        '''Clear the filter of the data table'''
