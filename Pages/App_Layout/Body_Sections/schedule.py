'''Schedule Page'''

# Libraries

import datetime
import time
import random
import string
import threading
import flet as ft

# Database
from DB.Functions.phases_db import get_phases
from DB.Functions.subjects_db import filter_subjects, search_subject_by_id
from DB.Functions.teacher_db import filter_teachers_by_subject, teacher_search
from DB.Functions.schedule_db import verify_search, schedule_add, schedule_id_search, verify_search_edit, schedule_edit as schedule_edit_db, schedule_delete as schedule_delete_db, check_amount as check, get_schedules, filter_schedules
from DB.Functions.temp_data_db import delete_tempdata_db, get_tempdata_db, save_tempdata_db, check_tempdata_db

class State:
    """
    A class that represents the state of an object.
    
    Attributes:
        i (int): The value of the state.
    """
    i = 0

s = State()
sem = threading.Semaphore()


class Schedule(ft.UserControl):
    '''Schedule with drag and drop functionality'''
    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.section = section

        #* ------------------ Variables ------------------ *#
        self.schedule_info_dict = {
            'ID': None,
            'Subject ID': None,
            'Teacher ID': None,
            'Block_time': None,
            'Block_day': None,
            'Date': None,
            'Phase': None
        }

        self.schedule_info_list = []




        #* ------------------ SideBar ------------------ *#
        # Create the Title
        title = ft.Text(
            'Materias',
            color='#4B4669',
            font_family='Arial',
            width = 200,
            text_align='center',
            weight='bold',
            size=20,
        )

        self.scroll = ft.Column([
            title,
            ft.Divider(),
        ],scroll=True, horizontal_alignment='center')

        self.sidebar = ft.Container(
            self.scroll,
            width=200,
            height=460,
            border=ft.border.all(color='#6D62A1', width=2),
            padding=ft.padding.all(5),
            border_radius=20,
            )


        #* ------------------ Body ------------------ *#
        # Create the Title
        title = ft.Text(
            'Horario',
            color='#4B4669',
            font_family='Arial',
            width = 200,
            text_align='center',
            weight='bold',
            size=20,
            height=39,
        )

        # Create the label for the schedule ID
        self.schedule_id = ft.Text(
            'ID: ',
            color='#4B4669',
            font_family='Arial',
            width = 110,
            text_align='left',
            weight='bold',
            size=13,
        )

        # Create the label for the schedule Grade | Section
        self.schedule_grade = ft.Text(
            color='#4B4669',
            font_family='Arial',
            width = 110,
            text_align='right',
            weight='bold',
            size=13,
        )

        # Create the container for the schedule ID and Type
        self.schedule_info = ft.Container(
            ft.Row([
                self.schedule_id,
                self.schedule_grade,
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            width=300,
            height=39,
            border_radius=5,
        )

        # Create the input for the Guide Teacher
        self.guide_teacher = ft.TextField(
            width=200,
            height=35,
            label='Profesor Guia',
            hint_text='Ingrese el nombre del profesor guia',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
        )




        # Create the schedule layout
        self.schedule = ft.DataTable(
            vertical_lines=ft.BorderSide(color='#6D62A1', width=1),
            width=900,
            height=380,
            data_row_max_height=55,
            columns=[
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text('Hora', color='#4B4669', size=15),alignment=ft.alignment.center, width=50
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text('Lunes', color='#4B4669', size=15), alignment=ft.alignment.center, width=100
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text('Martes', color='#4B4669', size=15),alignment=ft.alignment.center, width=100
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text('Miercoles', color='#4B4669', size=15),alignment=ft.alignment.center, width=100
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text('Jueves', color='#4B4669', size=15),alignment=ft.alignment.center, width=100
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text('Viernes', color='#4B4669', size=15),alignment=ft.alignment.center, width=100
                    )
                ),
            ],

            rows=[
                #* ------------------ 7:00 - 7:45 ------------------ *#
                self.rows('7:00', '7:45', '1'),

                #* ------------------ 7:45 - 8:30 ------------------ *#
                self.rows('7:45', '8:30', '2'),

                #* ------------------ 8:30 - 9:00 ------------------ *#
                self.rows('8:30', '9:00', '3'),

                #* ------------------ 9:00 - 9:30 ------------------ *#
                self.rows('9:00', '9:30', '4'),

                #* ------------------ 9:30 - 10:15 ------------------ *#
                self.rows('9:30', '10:15', '5'),

                #* ------------------ 10:15 - 11:00 ------------------ *#
                self.rows('10:15', '11:00', '6'),
            ]
        )

        # Create the body
        body_content = ft.Column([
            ft.Row([
                self.schedule_info,
                title,
                self.guide_teacher,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
            ft.Divider(),
            self.schedule,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=0)



        self.body = ft.Container(
            body_content,
            width=900,
            height=460,
            padding=ft.padding.all(5),
            border=ft.border.all(color='#6D62A1', width=2),
            border_radius=20,
        )

        #* ------------------ Footer ------------------ *#
        # Create the Search Bar
        self.search_bar = ft.Row([
            ft.TextField(
            width=450,
            height=35,
            label='Buscar Horario',
            hint_text='Ingrese el ID del horario',
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
                on_click= lambda e: self.search_schedule(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

        # Create the schedule Buttons (Create, Eliminate, Edit, Change View, Print, change School/Grade)
        self.schedule_buttons = ft.Row([
            ft.Container(
                ft.Text('Crear',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.create_schedule(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Eliminar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.confirm_delete_schedule(),
                border_radius=15,
            ),

            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.save_schedule(),
                border_radius=15,
                visible=False,
            ),

            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.confirm_edit_schedule(),
                border_radius=15,
                visible=False,
            ),

            ft.Container(
                ft.Text('Cancelar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.cancel_schedule(),
                border_radius=15,
                visible=False,
            ),

            ft.Container(
                ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.edit_schedule(),
                border_radius=15,
            ),

            ft.Container(
                ft.Icon(ft.icons.PRINT, color='#f3f4fa', size=20),
                width=50,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                # on_click= lambda e: self.print_teacher(), #TODO - Add the function to print a teacher
                border_radius=15,
                tooltip='Imprimir Profesor',
            ),

            ft.Container(
                ft.Icon(ft.icons.TABLE_ROWS_OUTLINED, color='#f3f4fa', size=20),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.view(),
                border_radius=15,
            ),

        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        footer = ft.Container(
            content=ft.Row([
            self.search_bar,
            self.schedule_buttons
        ],alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=1110,
        height=100,
        border_radius=20,
        border=ft.border.all(2, '#6D62A1'),
        )


        #* ------------------ Layout ------------------ *#
        self.layout = ft.Column([
            ft.Row([
                self.sidebar,
                self.body,
            ], alignment='center', vertical_alignment='start', disabled=True),
            footer,
        ], alignment=ft.MainAxisAlignment.START,horizontal_alignment='center' , spacing=20)
        self.content = self.layout

        self.check_temp()

    def build(self):
        return self.content

    #* ------------------ Functions ------------------ *#

    def check_temp(self):
        """
        Check the temporary data in the database and populate the fields with the retrieved data.

        This method checks if there is temporary data stored in the database. If there is, it retrieves the data and populates the corresponding fields in the Teachers page with the retrieved values. The temporary data includes information such as the teacher's name, last name, CI (Cedula), contact information, email, address, and birth date.

        Returns:
            None
        """
        if check_tempdata_db():
            data = get_tempdata_db()

            self.search_bar.controls[0].value = data
            self.update()
            self.search_schedule()

            delete_tempdata_db()


    #* ------------------ DRAG Functions ------------------ *#
    def create_drag(self, subject, grade, teacher:str, subject_id = None, teacher_id = None):
        '''Creates a subject in the schedule'''

        subject = subject.upper()
        grade = grade.upper()
        teacher = teacher.upper()

        data = {
            'Subject ID': subject_id,
            'Teacher ID': teacher_id,
            'Subject': subject,
            'Teacher': teacher,
            'Grade': grade,
        }

        string = f'{subject}\n{grade}\n{teacher}'

        subject = ft.Draggable(
            group='subjects',
            content=ft.Container(
                width=180,
                height=50,
                bgcolor=ft.colors.BLUE_300,
                border_radius=5,
                content=ft.Text(
                    string,
                    color= '#4B4669',
                    font_family='Arial',
                    text_align='center',
                    size=12,
                ),
            ),
            content_feedback=ft.Container(
                width=50,
                height=25,
                bgcolor=ft.colors.BLUE_300,
                border_radius=3,
            ),
            data=data,
        )
        self.scroll.controls.append(subject)
        self.scroll.update()

    def create_target(self,data):
        """
        Creates a drag target for subjects in the schedule.

        Returns:
            DragTarget: The created DragTarget object.

        Example Usage:
            schedule = Schedule(page, section)
            target = schedule.create_target()
        """
        target = ft.DragTarget(
            group='subjects',
            content=ft.Container(
                width=100,
                height=40,
                bgcolor='#bec0e3',
                border_radius=5,
            ),
            on_will_accept=self.drag_will_accept,
            on_accept=self.drag_accept,
            on_leave=self.drag_leave,
            data=data,
        )
        return target

    def drag_will_accept(self, e):
        """
        Updates the border color of a draggable control based on whether it will accept the dragged data or not.

        Args:
            e (event): The event object that contains information about the drag operation.

        Returns:
            None. The method only updates the border color of the draggable control.
        """
        e.control.content.border = ft.border.all(
            2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
        )
        e.control.update()

    def drag_accept(self, e: ft.DragTargetAcceptEvent):
        """
        Handles the acceptance of a dragged item onto a drop target.

        Args:
            e (ft.DragTargetAcceptEvent): The event object containing information about the drag and drop operation.

        Returns:
            None
        """
        src = self.page.get_control(e.src_id)

        if verify_search(src.data['Teacher ID'],e.control.data['Block'], self.schedule_grade.value, e.control.data['Day']):
            string = f"{src.data['Subject']}\n{src.data['Grade']}\n{src.data['Teacher']}"
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None
            e.control.content.content = ft.Text(
                string,
                color='#4B4669',
                font_family='Arial',
                text_align='center',
                size=10,
                data= {'ID': random.randint(1, 10000000)}
            )
            e.control.content.tooltip = string

            e.control.data['ID'] = e.control.content.content.data['ID']
            self.schedule_info_dict['ID'] = e.control.content.content.data['ID']
            self.schedule_info_dict['Subject ID'] = src.data['Subject ID']
            self.schedule_info_dict['Teacher ID'] = src.data['Teacher ID']
            self.schedule_info_dict['Block_time'] = e.control.data['Block']
            self.schedule_info_dict['Block_day'] = e.control.data['Day']
            self.schedule_info_dict['Date'] = datetime.datetime.now().strftime('%B %Y')
            self.schedule_info_dict['Phase'] = self.schedule_grade.value

            self.schedule_info_list.append(self.schedule_info_dict.copy())
            e.control.update()
        else:
            dlg = ft.AlertDialog(
                content=ft.Text("No se puede agregar esta materia", color='#4B4669', font_family='Arial', text_align='center', size=15),
                actions=[
                    ft.TextButton(
                        text='Aceptar',
                        on_click=lambda e: self.close(dlg)
                    )
                ]
            )
            self.open_dlg(dlg)
            e.control.content.border = None
            e.control.update()

    def drag_leave(self, e):
        """
        Remove the border from a draggable control when the mouse leaves its area.

        Args:
            e (event): The event object that contains information about the mouse leaving the draggable control.

        Returns:
            None
        """
        e.control.content.border = None
        e.control.update()

    def delete(self, e):
        """
        Deletes the content of a draggable control in the schedule.

        Args:
            e (event): The event object that contains information about the control being deleted.

        Returns:
            None

        """

        e.control.content.content.bgcolor = '#bec0e3'
        e.control.content.content.border = None
        if e.control.content.content.content is None:
            pass
        else:
            e.control.content.content.content.value = ''

            for info in self.schedule_info_list:
                if info['ID'] == e.control.content.data['ID']:
                    self.schedule_info_list.remove(info)
                    break

        e.control.update()

    def rows(self, start, end, block):
        """
        Create a row of data for the schedule table.

        Args:
            start (str): The start time of the schedule row.
            end (str): The end time of the schedule row.

        Returns:
            ft.DataRow: A DataRow object representing a row of data for the schedule table.
        """
        return ft.DataRow([
                    ft.DataCell(
                        ft.Container(
                            ft.Text(f'{start} - {end}', color='#4B4669', size=15), width=50, alignment=ft.alignment.center
                        )
                    ),
                    ft.DataCell(
                        self.create_target({'Block': block, 'Day': '1', 'ID': None}),
                        on_tap=self.delete,
                        data={
                            'Block': block,
                            'Day': '1',
                            'ID': None,
                        }
                    ),
                    ft.DataCell(
                        self.create_target({'Block': block, 'Day': '2', 'ID': None}),
                        on_tap=self.delete,
                        data={
                            'Block': block,
                            'Day': '2',
                            'ID': None,
                        }
                    ),
                    ft.DataCell(
                        self.create_target({'Block': block, 'Day': '3', 'ID': None}),
                        on_tap=self.delete,
                        data={
                            'Block': block,
                            'Day': '3',
                            'ID': None,
                        }
                    ),
                    ft.DataCell(
                        self.create_target({'Block': block, 'Day': '4', 'ID': None}),
                        on_tap=self.delete,
                        data={
                            'Block': block,
                            'Day': '4',
                            'ID': None,
                        }
                    ),
                    ft.DataCell(
                        self.create_target({'Block': block, 'Day': '5', 'ID': None}),
                        on_tap=self.delete,
                        data={
                            'Block': block,
                            'Day': '5',
                            'ID': None,
                        }
                    ),
                ])

    def show_drags(self, phase_info = None):
        '''Shows the drags in the sidebar'''

        phase = phase_info.split(' ')[0] + ' ' + phase_info.split(' ')[1].split(' ')[0]

        phase_type = phase.split(' ')[1]

        if phase_type == 'Grado':
            phase_type = 'Colegio'
        else:
            phase_type = 'Liceo'


        subject_list = filter_subjects(phase, phase_type)

        for subject in subject_list:
            teachers = filter_teachers_by_subject(subject['ID'])
            for teacher in teachers:
                teacher_info = teacher_search(teacher)
                self.create_drag(subject['Nombre'], subject['Etapa'], f"{teacher_info['Name']} {teacher_info['Last_Name']}", subject['ID'], teacher_info['ID'])




    #* ------------------ Schedule Buttons ------------------ *#
    #* DLG CREATE SCHEDULE *#
    def create_schedule(self):
        """
        Creates a new schedule by opening a dialog box to get the section and grade inputs from the user and validating the inputs.

        Inputs:
        - self: The instance of the Schedule class.

        Outputs:
        - None
        """
        self.layout.controls[0].disabled = False

        # Create a dlg to get the section and the grade
        dlg = ft.AlertDialog(
                content=ft.Column([
                    ft.Text('Configuracion del Horario', color='#4B4669', font_family='Arial', size=20),
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
                        on_change= lambda e: self.change_type(e.control.value),
                    ),
                ], width=300, height=60, alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment='center', spacing=10),
                actions=[
                    ft.Container(
                        ft.Container(
                            ft.Text('Continuar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                            width=80,
                            height=35,
                            bgcolor='#6D62A1',
                            alignment=ft.alignment.center,
                            on_click= lambda e: self.validate_dlg(dlg),
                            border_radius=15,
                        ), expand=True, height=35, alignment=ft.alignment.center
                    )
                ]
            )
        self.open_dlg(dlg)
        self.drop_dlg_options(dlg)

    def drop_dlg_options(self, dlg):
        """
        Populates dropdown options in a dialog with phases data.

        Parameters:
        - self: The instance of the class.
        - dlg: The dialog to be updated with dropdown options.

        Returns:
        None
        """
        phases_list = get_phases()
        for phase in phases_list:
            dlg.content.controls[1].options.append(ft.dropdown.Option(f"{phase['Grado/Año']} {phase['Seccion']}"))
        dlg.update()

    def change_type(self, mode = 'Colegio'):
        '''Changes the schedule type'''
        if mode != 'Colegio':
            mode = mode.split(' ')[1]
            if mode == 'Grado':
                mode = 'Colegio'
            else:
                mode = 'Liceo'

        # Delete the rows
        del self.schedule.rows[:]

        # Add the rows
        self.schedule.rows.append(self.rows('7:00', '7:45', '1'))
        self.schedule.rows.append(self.rows('7:45', '8:30', '2'))
        self.schedule.rows.append(self.rows('8:30', '9:00', '3'))
        self.schedule.rows.append(self.rows('9:00', '9:30', '4'))
        self.schedule.rows.append(self.rows('9:30', '10:15', '5'))
        self.schedule.rows.append(self.rows('10:15', '11:00', '6'))

        if mode == 'Liceo':
            # Delete the rows
            del self.schedule.rows[:]

            # Add the rows
            self.schedule.rows.append(self.rows('12:30', '1:50', '1'))
            self.schedule.rows.append(self.rows('1:50', '3:05', '2'))
            self.schedule.rows.append(self.rows('3:05', '4:20', '3'))
            self.schedule.rows.append(self.rows('4:20', '5:45', '4'))
        else:

            # Delete the rows
            del self.schedule.rows[:]

            # Add the rows
            self.schedule.rows.append(self.rows('7:00', '7:45', '1'))
            self.schedule.rows.append(self.rows('7:45', '8:30', '2'))
            self.schedule.rows.append(self.rows('8:30', '9:00', '3'))
            self.schedule.rows.append(self.rows('9:00', '9:30', '4'))
            self.schedule.rows.append(self.rows('9:30', '10:15', '5'))
            self.schedule.rows.append(self.rows('10:15', '11:00', '6'))

        self.body.update()

    def validate_dlg(self, dlg):
        '''Validate the dlg to create the schedule'''

        if dlg.content.controls[1].value is None:
            # Show the error in the button for a few seconds
            dlg.actions[0].content.bgcolor = '#FF0000'
            dlg.actions[0].content.content.value = 'Rellene todos los campos'
            dlg.actions[0].content.width = 200
            dlg.actions[0].content.update()
            time.sleep(1.5)
            dlg.actions[0].content.bgcolor = '#6D62A1'
            dlg.actions[0].content.content.value = 'Continuar'
            dlg.actions[0].content.width = 80
            dlg.actions[0].content.update()
        else:
            phase = dlg.content.controls[1].value
            self.show_drags(phase)

            # Hide all the footer but the cancel and save buttons
            self.search_bar.visible = False
            self.schedule_buttons.controls[0].visible = False
            self.schedule_buttons.controls[1].visible = False
            self.schedule_buttons.controls[2].visible = True
            self.schedule_buttons.controls[3].visible = False
            self.schedule_buttons.controls[4].visible = True
            self.schedule_buttons.controls[5].visible = False
            self.schedule_buttons.controls[6].visible = False
            self.schedule_buttons.controls[7].visible = False

            self.guide_teacher.value = ''
            self.schedule_grade.value = f'{dlg.content.controls[1].value}'

            self.update()

            self.close(dlg)




    #* EDIT SCHEDULE *#
    def edit_schedule(self):
        '''Edit the schedule'''
        if self.schedule_id.value == 'ID: ':
            dlg = ft.AlertDialog(
                content=ft.Text('Primero debe buscar un horario', color='#4B4669', font_family='Arial', size=15),
                actions=[
                    ft.TextButton(
                        text='Aceptar',
                        on_click=lambda e: self.close(dlg)
                    )
                ]
            )
            self.open_dlg(dlg)
        else:
            # hide all the footer but the cancel and save buttons
            self.search_bar.visible = False
            self.schedule_buttons.controls[0].visible = False
            self.schedule_buttons.controls[1].visible = False
            self.schedule_buttons.controls[2].visible = False
            self.schedule_buttons.controls[3].visible = True
            self.schedule_buttons.controls[4].visible = True
            self.schedule_buttons.controls[5].visible = False
            self.schedule_buttons.controls[6].visible = False
            self.schedule_buttons.controls[7].visible = False

            # Enable the sidebar and the body
            self.layout.controls[0].disabled = False

            # Add the DELETE action to the cells
            for row in self.schedule.rows:
                for cell in row.cells:
                    if isinstance(cell.content, ft.DragTarget):
                        cell.on_tap = self.delete_on_edit

            phase = self.schedule_grade.value
            self.show_drags(phase)

            self.update()



    def cancel_schedule(self):
        '''Cancel the schedule creation'''
        # Show all the footer buttons
        self.search_bar.visible = True
        self.schedule_buttons.controls[0].visible = True
        self.schedule_buttons.controls[1].visible = True
        self.schedule_buttons.controls[2].visible = False
        self.schedule_buttons.controls[3].visible = False
        self.schedule_buttons.controls[4].visible = False
        self.schedule_buttons.controls[5].visible = True
        self.schedule_buttons.controls[6].visible = True
        self.schedule_buttons.controls[7].visible = True

        # Clear the inputs
        self.guide_teacher.value = ''

        self.schedule_id.value = 'ID: '
        self.schedule_grade.value = ''

        self.schedule_info_list.clear()

        # Disable the sidebar and the body
        self.layout.controls[0].disabled = True

        # Delete the draggables from the sidebar
        del self.scroll.controls[2:]

        # Change the schedule type
        self.change_type()

        self.update()

    def save_schedule(self):
        '''Save the schedule in the database'''

        if self.guide_teacher.value == '':
            guide_teacher = 'Por Asignar'
        else:
            guide_teacher = self.guide_teacher.value

        # Generate the schedule code
        caracteres = string.ascii_letters + string.digits
        codigo_horario = ''.join(random.choice(caracteres) for _ in range(10))

        for row in self.schedule.rows:
            for cell in row.cells:
                if cell.content.content is not None:
                    if cell.content.data is None:
                        pass
                    elif cell.content.data['ID'] is None:
                        schedule_add(None, None, cell.content.data['Block'], self.schedule_grade.value, cell.content.data['Day'], guide_teacher, codigo_horario)

        # save the schedule in the database
        for data in self.schedule_info_list:
            schedule_add(data['Teacher ID'], data['Subject ID'], data['Block_time'], data['Phase'], data['Block_day'], guide_teacher, codigo_horario)

        self.show_schedule_code(codigo_horario)
        # Show all the footer buttons
        self.search_bar.visible = True
        self.schedule_buttons.controls[0].visible = True
        self.schedule_buttons.controls[1].visible = True
        self.schedule_buttons.controls[2].visible = False
        self.schedule_buttons.controls[3].visible = False
        self.schedule_buttons.controls[4].visible = False
        self.schedule_buttons.controls[5].visible = True
        self.schedule_buttons.controls[6].visible = True
        self.schedule_buttons.controls[7].visible = True

        # Clear the inputs
        self.guide_teacher.value = ''

        self.schedule_id.value = 'ID: '
        self.schedule_grade.value = ''

        self.schedule_info_list.clear()

        # Disable the sidebar and the body
        self.layout.controls[0].disabled = True

        # Delete the draggables from the sidebar
        del self.scroll.controls[2:]

        # Change the schedule type
        self.change_type()

        self.update()

    #* ------------------ Search Functions ------------------ *#
    def search_schedule(self):
        '''Search the schedule'''
        if self.search_bar.controls[0].value == '':
            self.guide_teacher.value = ''
            self.change_type()
            self.update()
        else:
            search = self.search_bar.controls[0].value
            schedule = schedule_id_search(search)
            if schedule is False:
                dlg = ft.AlertDialog(
                    content=ft.Text("No se encontro el horario", color='#4B4669', font_family='Arial', text_align='center', size=15),
                    actions=[
                        ft.TextButton(
                            text='Aceptar',
                            on_click=lambda e: self.close(dlg)
                        )
                    ]
                )
                self.open_dlg(dlg)
            else:
                del self.schedule.rows[:]
                if schedule[0]['Formato'] == 'Colegio':
                    loop = 6
                    time_list = [
                        {'start': '7:00', 'end': '7:45', 'block': '1'},
                        {'start': '7:45', 'end': '8:30', 'block': '2'},
                        {'start': '8:30', 'end': '9:00', 'block': '3'},
                        {'start': '9:00', 'end': '9:30', 'block': '4'},
                        {'start': '9:30', 'end': '10:15', 'block': '5'},
                        {'start': '10:15', 'end': '11:00', 'block': '6'}
                    ]
                else:
                    loop = 4
                    time_list = [
                        {'start': '12:30', 'end': '1:50', 'block': '1'},
                        {'start': '1:50', 'end': '3:05', 'block': '2'},
                        {'start': '3:05', 'end': '4:20', 'block': '3'},
                        {'start': '4:20', 'end': '5:45', 'block': '4'},
                    ]

                list_row = {
                    'start': None,
                    'end': None,
                    'string_1': None,
                    'string_2': None,
                    'string_3': None,
                    'string_4': None,
                    'string_5': None,
                    'data_id_1': None,
                    'data_id_2': None,
                    'data_id_3': None,
                    'data_id_4': None,
                    'data_id_5': None,
                    'bloque_hora_1': None,
                    'bloque_hora_2': None,
                    'bloque_hora_3': None,
                    'bloque_hora_4': None,
                    'bloque_hora_5': None,
                    'ID_1': None,
                    'ID_2': None,
                    'ID_3': None,
                    'ID_4': None,
                    'ID_5': None,
                }

                string_list = []
                self.guide_teacher.value = schedule[0]['Guide Teacher']
                for i in range(loop):
                    schedule = schedule_id_search(search, time_list[i]['block'])
                    for info in schedule:
                        string_txt = None
                        if info['Materia ID'] is not None and info['Profesor ID'] is not None:
                            subject = search_subject_by_id(info['Materia ID'])
                            teacher = teacher_search(info['Profesor ID'])

                            string_txt = f"{subject['Nombre']}\n{info['Etapa']}\n{teacher['Name']} {teacher['Last_Name']}"

                        list_row[f"string_{info['Bloque Dia']}"] = string_txt
                        list_row[f"data_id_{info['Bloque Dia']}"] = info['Materia ID']
                        list_row[f"bloque_hora_{info['Bloque Dia']}"] = info['Bloque Hora']
                        list_row['start'] = time_list[i]['start']
                        list_row['end'] = time_list[i]['end']
                        list_row[f"ID_{info['Bloque Dia']}"] = info['ID']

                        self.schedule_info_dict['ID'] = info['ID']
                        self.schedule_info_dict['Subject ID'] = info['Materia ID']
                        self.schedule_info_dict['Teacher ID'] = info['Profesor ID']
                        self.schedule_info_dict['Block_time'] = info['Bloque Hora']
                        self.schedule_info_dict['Block_day'] = info['Bloque Dia']
                        self.schedule_info_dict['Date'] = info['Fecha']
                        self.schedule_info_dict['Phase'] = info['Etapa']

                        self.schedule_info_list.append(self.schedule_info_dict.copy())

                    string_list.append(list_row.copy())

                for i in string_list:
                    self.schedule.rows.append(self.show_rows_schedule(i['start'], i['end'], i['string_1'], i['string_2'], i['string_3'], i['string_4'], i['string_5'], i['data_id_1'], i['data_id_2'], i['data_id_3'], i['data_id_4'], i['data_id_5'], i['bloque_hora_1'], i['bloque_hora_2'], i['bloque_hora_3'], i['bloque_hora_4'], i['bloque_hora_5'], i['ID_1'], i['ID_2'], i['ID_3'], i['ID_4'], i['ID_5']))


                self.schedule_grade.value = f"{schedule[0]['Etapa']}"
                self.schedule_id.value = f"ID: {schedule[0]['ID Horario']}"

                self.update()


    def show_rows_schedule(self,start, end, string_a, string_b, string_c, string_d, string_e, data_id_a, data_id_b, data_id_c, data_id_d, data_id_e, bloque_hora_a, bloque_hora_b, bloque_hora_c, bloque_hora_d, bloque_hora_e, id_a, id_b, id_c, id_d, id_e):
        '''Show the rows of the schedule'''
        return ft.DataRow([
                    ft.DataCell(
                        ft.Container(
                            ft.Text(f"{start} - {end}", color='#4B4669', size=15), width=50, alignment=ft.alignment.center
                        )
                    ),
                    ft.DataCell(
                        self.create_search_target(string_a, data_id_a, {'Block': bloque_hora_e, 'Day': 1, 'ID': id_a}),
                        data={
                            'Block': bloque_hora_a,
                            'Day': 'Lunes',
                            'ID': id_a
                        }
                    ),
                    ft.DataCell(
                        self.create_search_target(string_b, data_id_b, {'Block': bloque_hora_e, 'Day': 2, 'ID': id_b}),
                        data={
                            'Block': bloque_hora_b,
                            'Day': 'Martes',
                            'ID': id_b
                        }
                    ),
                    ft.DataCell(
                        self.create_search_target(string_c, data_id_c, {'Block': bloque_hora_e, 'Day': 3, 'ID': id_c}),
                        data={
                            'Block': bloque_hora_c,
                            'Day': 'Miercoles',
                            'ID': id_c
                        }
                    ),
                    ft.DataCell(
                        self.create_search_target(string_d, data_id_d, {'Block': bloque_hora_e, 'Day': 4, 'ID': id_d}),
                        data={
                            'Block': bloque_hora_d,
                            'Day': 'Jueves',
                            'ID': id_d
                        }
                    ),
                    ft.DataCell(
                        self.create_search_target(string_e, data_id_e, {'Block': bloque_hora_e, 'Day': 5, 'ID': id_e}),
                        data={
                            'Block': bloque_hora_e,
                            'Day': 'Viernes',
                            'ID': id_e
                        }
                    )
                ])

    def create_search_target(self,string, data_id, data_dict):
        '''Creates a search target for subjects in the schedule'''
        if data_id is None:
            color = '#bec0e3'
        else:
            color = ft.colors.BLUE_300
        target = ft.DragTarget(
            group='subjects',
            content=ft.Container(
                ft.Text(string, color='#4B4669',font_family='Arial',text_align='center',size=10),
                width=100,
                height=40,
                bgcolor=color,
                border_radius=5,
                tooltip=string,
            ),
            on_will_accept=self.drag_will_accept,
            on_accept=self.drag_edit_accept,
            on_leave=self.drag_leave,
            data=data_dict,
        )
        return target

    def drag_edit_accept(self, e: ft.DragTargetAcceptEvent):
        """
        Handles the acceptance of a dragged item onto a drop target.

        Args:
            e (ft.DragTargetAcceptEvent): The event object containing information about the drag and drop operation.

        Returns:
            None
        """
        src = self.page.get_control(e.src_id)

        if verify_search_edit(src.data['Teacher ID'],e.control.data['Block'], self.schedule_grade.value, e.control.data['Day'], self.schedule_id.value.split(' ')[1]):
            string = f"{src.data['Subject']}\n{src.data['Grade']}\n{src.data['Teacher']}"
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None
            e.control.content.content = ft.Text(
                string,
                color='#4B4669',
                font_family='Arial',
                text_align='center',
                size=10,
                data= {'ID': e.control.data['ID']}
            )

            e.control.data['ID'] = e.control.content.content.data['ID']
            self.schedule_info_dict['ID'] = e.control.content.content.data['ID']
            self.schedule_info_dict['Subject ID'] = src.data['Subject ID']
            self.schedule_info_dict['Teacher ID'] = src.data['Teacher ID']
            self.schedule_info_dict['Block_time'] = e.control.data['Block']
            self.schedule_info_dict['Block_day'] = e.control.data['Day']
            self.schedule_info_dict['Date'] = datetime.datetime.now().strftime('%B %Y')
            self.schedule_info_dict['Phase'] = self.schedule_grade.value

            self.schedule_info_list.append(self.schedule_info_dict.copy())
            e.control.update()
        else:
            dlg = ft.AlertDialog(
                content=ft.Text("No se puede agregar esta materia", color='#4B4669', font_family='Arial', text_align='center', size=15),
                actions=[
                    ft.TextButton(
                        text='Aceptar',
                        on_click=lambda e: self.close(dlg)
                    )
                ]
            )
            self.open_dlg(dlg)
            e.control.content.border = None
            e.control.update()


    def confirm_edit_schedule(self):
        """
        Displays a confirmation dialog for editing a schedule.

        Returns:
        None
        """
        dlg = ft.AlertDialog(
                content=ft.Text('¿Esta seguro que desea guardar los cambios?', color='#4B4669', font_family='Arial', size=15),
                actions=[
                    ft.ElevatedButton(
                        text='Aceptar',
                        on_click=lambda e: self.edit_confirmed(dlg)
                    ),
                    ft.ElevatedButton(
                        text='Cancelar',
                        on_click=lambda e: self.close(dlg)
                    )
                ]
            )
        self.open_dlg(dlg)

    def edit_confirmed(self, dlg):
        """
        Handles the confirmation of editing a schedule.

        Parameters:
        - self: The instance of the class.
        - dlg: The confirmation dialog to be closed after editing.

        Returns:
        None
        """
        if self.guide_teacher.value == '':
            guide_teacher = 'Por Asignar'
        else:
            guide_teacher = self.guide_teacher.value

        schedule_id = self.schedule_id.value.split(' ')[1]

        # save the schedule in the database
        for data in self.schedule_info_list:
            schedule_edit_db(schedule_id, data['Block_time'], data['Teacher ID'], data['Subject ID'], guide_teacher, data['ID'])

        self.close(dlg)


        # Show all the footer buttons
        self.search_bar.visible = True
        self.schedule_buttons.controls[0].visible = True
        self.schedule_buttons.controls[1].visible = True
        self.schedule_buttons.controls[2].visible = False
        self.schedule_buttons.controls[3].visible = False
        self.schedule_buttons.controls[4].visible = False
        self.schedule_buttons.controls[5].visible = True
        self.schedule_buttons.controls[6].visible = True
        self.schedule_buttons.controls[7].visible = True

        # Clear the inputs
        self.guide_teacher.value = ''

        self.schedule_id.value = 'ID: '
        self.schedule_grade.value = ''

        self.schedule_info_list.clear()

        # Disable the sidebar and the body
        self.layout.controls[0].disabled = True

        # Delete the draggables from the sidebar
        del self.scroll.controls[2:]

        # Change the schedule type
        self.change_type()

        self.update()

    def show_schedule_code(self, code):
        '''
        Displays the code of a schedule in an alert dialog.

        Parameters:
        - code (str): The code of the schedule to be displayed.

        Returns:
        None
        '''
        dlg = ft.AlertDialog(
                content=ft.Text(f'Codigo del Horario: {code}', color='#4B4669', font_family='Arial', size=15, selectable=True),
                actions=[
                    ft.TextButton(
                        text='Aceptar',
                        on_click=lambda e: self.close(dlg)
                    )
                ]
            )
        self.open_dlg(dlg)

    def delete_on_edit(self, e):
        """
        Deletes the content of a draggable control in the schedule.

        Args:
            e (event): The event object that contains information about the control being deleted.

        Returns:
            None

        """

        erased_id = e.control.content.data['ID']

        e.control.content.content.bgcolor = '#bec0e3'
        e.control.content.content.border = None
        if e.control.content.content.content is None:
            pass
        else:
            e.control.content.content.content.value = ''

            for row in self.schedule.rows:
                for cell in row.cells:
                    if isinstance(cell.content, ft.DragTarget):
                        if cell.content.data['ID'] == erased_id:
                            self.schedule_info_dict['ID'] = cell.content.data['ID']
                            self.schedule_info_dict['Subject ID'] = None
                            self.schedule_info_dict['Teacher ID'] = None
                            self.schedule_info_dict['Block_time'] = cell.content.data['Block']
                            self.schedule_info_dict['Block_day'] = cell.content.data['Day']
                            self.schedule_info_dict['Date'] = None
                            self.schedule_info_dict['Phase'] = None

                            self.schedule_info_list.append(self.schedule_info_dict.copy())
                            break



        e.control.update()

    #* ------------------ Delete Functions ------------------ *#
    def confirm_delete_schedule(self):
        """
        Displays a confirmation dialog for deleting a schedule.

        Returns:
        None
        """
        if self.schedule_id.value == 'ID: ':
            dlg = ft.AlertDialog(
                content=ft.Text('Primero debe buscar un horario', color='#4B4669', font_family='Arial', size=15),
                actions=[
                    ft.TextButton(
                        text='Aceptar',
                        on_click=lambda e: self.close(dlg)
                    )
                ]
            )
            self.open_dlg(dlg)
        else:
            dlg = ft.AlertDialog(
                    content=ft.Text('¿Esta seguro que desea eliminar el horario?', color='#4B4669', font_family='Arial', size=15),
                    actions=[
                        ft.ElevatedButton(
                            text='Cancelar',
                            on_click=lambda e: self.close(dlg)
                        ),
                        ft.ElevatedButton(
                            text='Aceptar',
                            on_click=lambda e: self.delete_second_confirm(dlg)
                        )
                    ]
                )
            self.open_dlg(dlg)

    def delete_second_confirm(self, dlg):
        """
        Displays a confirmation dialog box with a countdown timer. After the countdown, the dialog box is updated to allow the user to confirm the deletion.

        :param dlg: The dialog box object that is displayed to the user.
        :type dlg: dialog box
        :return: None
        """
        try:
            dlg.actions[1].on_click = None
            for i in range(5, -1, -1):
                dlg.actions[1].text = f'Espere {i} segundos...'
                dlg.update()
                time.sleep(1)

            dlg.actions[1].text = 'Confirmar Eliminacion'
            dlg.actions[1].bgcolor = '#f83c86'
            dlg.actions[1].on_click = lambda e: self.delete_schedule(dlg)
            dlg.update()
        except:
            pass

    def delete_schedule(self, dlg):
        """
        Deletes a schedule from the database.

        :param dlg: The dialog box object that is displayed to the user.
        :type dlg: dialog box
        :return: None
        """
        schedule_id = self.schedule_id.value.split(' ')[1]
        schedule_delete_db(schedule_id)
        self.close(dlg)

        # Show all the footer buttons
        self.search_bar.visible = True
        self.schedule_buttons.controls[0].visible = True
        self.schedule_buttons.controls[1].visible = True
        self.schedule_buttons.controls[2].visible = False
        self.schedule_buttons.controls[3].visible = False
        self.schedule_buttons.controls[4].visible = False
        self.schedule_buttons.controls[5].visible = True
        self.schedule_buttons.controls[6].visible = True
        self.schedule_buttons.controls[7].visible = True

        # Clear the inputs
        self.guide_teacher.value = ''

        self.schedule_id.value = 'ID: '
        self.schedule_grade.value = ''

        self.schedule_info_list.clear()

        # Disable the sidebar and the body
        self.layout.controls[0].disabled = True

        # Delete the draggables from the sidebar
        del self.scroll.controls[2:]

        # Change the schedule type
        self.change_type()

        self.update()


    #* ------------------ View Functions ------------------ *#
    def view(self):
        """
        Updates the content of the section attribute with a new instance of the ScheduleList class and reflects the changes in the user interface.

        Inputs:
        - None

        Outputs:
        - None
        """
        self.section.content = ScheduleList(self.page, self.section)
        self.section.update()

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








#^ ------------------ Schedule List ------------------ ^#

class ScheduleList(ft.UserControl):
    """
    Initializes the ScheduleList class object by creating the layout for a schedule list page.

    Args:
        page (ft.Page): The page object where the schedule list will be displayed.
        section (str): The section where the schedule list will be placed.

    Returns:
        None
    """
    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.body = section

        self.scrol_pos = 10

        #* ------------------ Layout ------------------ *#
        # Create the Title
        self.title = ft.Text(
            'Lista de Horarios',
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
            label='Buscar Horario',
            hint_text='Ingresa un dato del Horario',
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
                on_click= lambda e: self.search_schedule(),
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
                ft.DataColumn(ft.Container(ft.Text('ID', size=15, color='#4B4669', text_align='center'), width=165, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Etapa', size=15, color='#4B4669', text_align='center'), width=165, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Profesor Guia', size=15, color='#4B4669', text_align='center'), width=165, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Fecha', size=15, color='#4B4669', text_align='center'), width=165, alignment=ft.alignment.center)),
            ],
        )

        self.scrol = ft.Column([
            self.data_table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1100, height=490, on_scroll= lambda e: self.on_scroll(e))

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

        self.clear_filter_button = ft.Container(
            ft.Icon(ft.icons.FILTER_ALT_OFF, color='#f3f4fa', size=20),
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
                    self.change_view,
                    up_button
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            self.data_container,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout
        self.show_schedules()

    def build(self):
        return self.content

    #^ ------------------ Functions ------------------ *#
    def show_schedules(self):
        '''Show the schedules in the data table'''
        if check() < 10:
            list_schedules = get_schedules(0, check())
            last = check()
        else:
            list_schedules = get_schedules(0, 9)
            last = 9
        for i in range(0, last):
            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(list_schedules[i]['ID Horario'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_schedules[i]['Etapa'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_schedules[i]['Guide Teacher'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(list_schedules[i]['Fecha'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
            ], data=list_schedules[i]['ID Horario'], on_select_changed= lambda e: self.schedule_selected(e))
            self.data_table.rows.append(row)
        self.update()

    def on_scroll(self, e):
        """
        Called when the user scrolls to the bottom of the data table.
    
        Args:
            self (object): The instance of the teacherslist class.
            e (object): The event object that contains information about the scroll event.
        
        Returns:
            None
    
        """
        if e.pixels >= e.max_scroll_extent - 100:
            if sem.acquire(blocking=False):
                try:
                    # Obten horarios desde la posición actual hasta la posición + 9
                    list_schedule = get_schedules(self.scrol_pos, self.scrol_pos + 9)
                    #Verificar si la lista esta vacia
                    if list_schedule:
                        for schedule in list_schedule:
                            row = ft.DataRow([
                                ft.DataCell(ft.Container(ft.Text(schedule['ID Horario'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(schedule['Etapa'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(schedule['Guide Teacher'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(schedule['Fecha'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                            ], data=schedule['ID Horario'], on_select_changed= lambda e: self.schedule_selected(e))
                            self.data_table.rows.append(row)
                        self.update()
                        self.scrol_pos += 10
                finally:
                    sem.release()

    def search_schedule(self):
        '''Search a schedule in the database'''
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
            self.data_table.rows.clear()
            list_schedule = filter_schedules(search)

            for schedule in list_schedule:
                row = ft.DataRow([
                    ft.DataCell(ft.Container(ft.Text(schedule['ID Horario'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(schedule['Etapa'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(schedule['Guide Teacher'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(schedule['Fecha'], size=12, color='#4B4669', text_align='center'), width=160, alignment=ft.alignment.center)),
                ], data=schedule['ID Horario'], on_select_changed= lambda e: self.schedule_selected(e))
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
        self.update()
        self.show_schedules()

    def schedule_selected(self, e):
        '''Select a teacher from the data table'''
        save_tempdata_db(str(e.control.data))
        self.view(True)


    def view(self, op=False):
        '''Change the view of the data table to the Schedule page'''
        if op:
            self.body.content = Schedule(self.page, self.body)
            self.body.update()
        else:
            delete_tempdata_db()
            self.body.content = Schedule(self.page, self.body)
            self.body.update()

