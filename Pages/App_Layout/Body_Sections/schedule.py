'''Schedule Page'''

# Libraries

import datetime
import time
import flet as ft

class Schedule(ft.UserControl):
    '''Schedule with drag and drop functionality'''
    def __init__(self, page: ft.Page, section: str):
        super().__init__()
        self.page = page
        self.section = section

        #* ------------------ Variables ------------------ *#
        #TODO - Add the Database functionality
        self.seccion = None
        self.grado = None
        self.tipo = None
        self.date = None



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
            'ID: 123456789',
            color='#4B4669',
            font_family='Arial',
            width = 100,
            text_align='left',
            weight='bold',
            size=13,
        )

        # Create the label for the schedule Type (School or Grade)
        self.schedule_type = ft.Text(
            'Colegio',
            color='#4B4669',
            font_family='Arial',
            width = 50,
            text_align='right',
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
                self.schedule_type,
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
                self.rows('7:00', '7:45'),

                #* ------------------ 7:45 - 8:30 ------------------ *#
                self.rows('7:45', '8:30'),

                #* ------------------ 8:30 - 9:00 ------------------ *#
                self.rows('8:30', '9:00'),

                #* ------------------ 9:00 - 9:30 ------------------ *#
                self.rows('9:00', '9:30'),

                #* ------------------ 9:30 - 10:15 ------------------ *#
                self.rows('9:30', '10:15'),

                #* ------------------ 10:15 - 11:00 ------------------ *#
                self.rows('10:15', '11:00'),
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
                on_click= lambda e: self.delete_schedule(),
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
                ft.Text('Imprimir',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.print_schedule(),
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

    def build(self):
        return self.content

    #* ------------------ Functions ------------------ *#
    def create_drag(self, subject, grade, teacher:str):
        '''Creates a subject in the schedule'''

        subject = subject.upper()
        grade = grade.upper()
        teacher = teacher.upper()

        string = f'{subject}\n{grade}\n{teacher}'

        subject = ft.Draggable(
            group='subjects',
            content=ft.Container(
                width=180,
                height=50,
                bgcolor=ft.colors.CYAN,
                border_radius=5,
                content=ft.Text(
                    string,
                    color='#4B4669',
                    font_family='Arial',
                    text_align='center',
                    size=12,
                ),
            ),
            content_feedback=ft.Container(
                width=50,
                height=25,
                bgcolor=ft.colors.CYAN,
                border_radius=3,
            ),
            data=(subject, grade, teacher),
        )
        self.scroll.controls.append(subject)
        self.scroll.update()

    def create_target(self):
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

        src_data = src.data[0]

        if src_data == 'MATEMATICA':  #TODO - Add the Database functionality
            string = f'{src.data[0]}\n{src.data[1]}\n{src.data[2]}'
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None
            e.control.content.content = ft.Text(
                string,
                color='#4B4669',
                font_family='Arial',
                text_align='center',
                size=10,
            )
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
        e.control.update()

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

    def rows(self, start, end):
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
                        self.create_target(),
                        on_tap=self.delete,
                    ),
                    ft.DataCell(
                        self.create_target(),
                        on_tap=self.delete,
                    ),
                    ft.DataCell(
                        self.create_target(),
                        on_tap=self.delete,
                    ),
                    ft.DataCell(
                        self.create_target(),
                        on_tap=self.delete,
                    ),
                    ft.DataCell(
                        self.create_target(),
                        on_tap=self.delete,
                    ),
                ])


    def show_drags(self): #TODO - Add the Database functionality
        '''Shows the drags in the sidebar'''
        for _ in range(5):
            self.create_drag('matematica', '1er Grado', 'andres ortiz')

    #* ------------------ Buttons Functions ------------------ *#
    def change_type(self, mode = 'Colegio'):
        '''Changes the schedule type'''

        self.schedule_type.value = 'Colegio'

        # Delete the rows
        del self.schedule.rows[:]

        # Add the rows
        self.schedule.rows.append(self.rows('7:00', '7:45'))
        self.schedule.rows.append(self.rows('7:45', '8:30'))
        self.schedule.rows.append(self.rows('8:30', '9:00'))
        self.schedule.rows.append(self.rows('9:00', '9:30'))
        self.schedule.rows.append(self.rows('9:30', '10:15'))
        self.schedule.rows.append(self.rows('10:15', '11:00'))



        if mode == 'Liceo':
            self.schedule_type.value = 'Liceo'

            # Delete the rows
            del self.schedule.rows[:]

            # Add the rows
            self.schedule.rows.append(self.rows('12:30', '1:50'))
            self.schedule.rows.append(self.rows('1:50', '3:05'))
            self.schedule.rows.append(self.rows('3:05', '4:20'))
            self.schedule.rows.append(self.rows('4:20', '5:45'))
        else:
            self.schedule_type.value = 'Colegio'

            # Delete the rows
            del self.schedule.rows[:]

            # Add the rows
            self.schedule.rows.append(self.rows('7:00', '7:45'))
            self.schedule.rows.append(self.rows('7:45', '8:30'))
            self.schedule.rows.append(self.rows('8:30', '9:00'))
            self.schedule.rows.append(self.rows('9:00', '9:30'))
            self.schedule.rows.append(self.rows('9:30', '10:15'))
            self.schedule.rows.append(self.rows('10:15', '11:00'))

        self.body.update()


    def search_schedule(self): #TODO - Add the Database functionality
        '''TO WRITE'''

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
        self.dlg = ft.AlertDialog(
                content=ft.Column([
                    ft.Dropdown(
                        width=200,
                        height=35,
                        label='Grado / Año',
                        hint_text='Ingrese el grado o año',
                        filled=True,
                        bgcolor='#f3f4fa',
                        options=[
                            ft.dropdown.Option('1ero'),
                            ft.dropdown.Option('2do'),
                            ft.dropdown.Option('3ero'),
                            ft.dropdown.Option('4to'),
                            ft.dropdown.Option('5to'),
                            ft.dropdown.Option('6to'),
                        ],
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0)
                    ),

                    ft.Dropdown(
                        width=200,
                        height=35,
                        label='Seccion',
                        hint_text='Ingrese la seccion',
                        filled=True,
                        bgcolor='#f3f4fa',
                        options=[
                            ft.dropdown.Option('A'),
                            ft.dropdown.Option('B'),
                            ft.dropdown.Option('C'),
                            ft.dropdown.Option('D'),
                            ft.dropdown.Option('E'),
                            ft.dropdown.Option('F'),
                        ],
                        hint_style=ft.TextStyle(color='#C0C1E3'),
                        label_style=ft.TextStyle(color='#4B4669'),
                        text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                        border_color='#6D62A1',
                        content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                    ),

                    ft.RadioGroup(content=ft.Container(
                        ft.Column([
                            ft.Radio(value='Liceo', label='Liceo'),
                            ft.Radio(value='Colegio', label='Colegio'),
                        ]), padding=ft.padding.only(left=10,top=0,right=10,bottom=0)),
                        on_change= lambda e: self.change_type(e.control.value),
                    ),

                ], width=200, height=150, alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment='center', spacing=10),
                actions=[
                    ft.Container(
                        ft.Container(
                            ft.Text('Continuar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                            width=80,
                            height=35,
                            bgcolor='#6D62A1',
                            alignment=ft.alignment.center,
                            on_click= lambda e: self.validate_dlg(),
                            border_radius=15,
                        ), expand=True, height=35, alignment=ft.alignment.center
                    )
                ]
            )
        self.open_dlg(self.dlg)

    def validate_dlg(self):
        '''Validate the dlg to create the schedule'''

        if self.dlg.content.controls[0].value is None or self.dlg.content.controls[1].value is None or self.dlg.content.controls[2].value is None:
            # Show the error in the button for a few seconds
            self.dlg.actions[0].content.bgcolor = '#FF0000'
            self.dlg.actions[0].content.content.value = 'Rellene todos los campos'
            self.dlg.actions[0].content.width = 200
            self.dlg.actions[0].content.update()
            time.sleep(1.5)
            self.dlg.actions[0].content.bgcolor = '#6D62A1'
            self.dlg.actions[0].content.content.value = 'Continuar'
            self.dlg.actions[0].content.width = 80
            self.dlg.actions[0].content.update()
        else:
            #TODO - Add the Database functionality to get the subjects
            self.show_drags()

            # Hide all the footer but the cancel and save buttons
            self.search_bar.visible = False
            self.schedule_buttons.controls[0].visible = False
            self.schedule_buttons.controls[1].visible = False
            self.schedule_buttons.controls[2].visible = True
            self.schedule_buttons.controls[3].visible = True
            self.schedule_buttons.controls[4].visible = False
            self.schedule_buttons.controls[5].visible = False
            self.schedule_buttons.controls[6].visible = False


            # Variables
            self.seccion = self.dlg.content.controls[1].value
            self.grado = self.dlg.content.controls[0].value
            self.tipo = self.dlg.content.controls[2].value
            self.date = datetime.datetime.now().date()

            self.schedule_grade.value = f'{self.grado} | Seccion {self.seccion}'

            self.layout.update()

            self.close(self.dlg)


    def edit_schedule(self):
        '''Edit the schedule'''
        # hide all the footer but the cancel and save buttons
        self.search_bar.visible = False
        self.schedule_buttons.controls[0].visible = False
        self.schedule_buttons.controls[1].visible = False
        self.schedule_buttons.controls[2].visible = True
        self.schedule_buttons.controls[3].visible = True
        self.schedule_buttons.controls[4].visible = False
        self.schedule_buttons.controls[5].visible = False
        self.schedule_buttons.controls[6].visible = False

        # Enable the sidebar and the body
        self.layout.controls[0].disabled = False

        #TODO - Add the Database functionality to get the subjects
        self.show_drags()

        # Change the schedule type
        self.change_type()

        self.layout.update()



    def cancel_schedule(self):
        '''Cancel the schedule creation'''
        # Show all the footer buttons
        self.search_bar.visible = True
        self.schedule_buttons.controls[0].visible = True
        self.schedule_buttons.controls[1].visible = True
        self.schedule_buttons.controls[2].visible = False
        self.schedule_buttons.controls[3].visible = False
        self.schedule_buttons.controls[4].visible = True
        self.schedule_buttons.controls[5].visible = True
        self.schedule_buttons.controls[6].visible = True

        # Clear the inputs
        self.guide_teacher.value = ''

        # Disable the sidebar and the body
        self.layout.controls[0].disabled = True

        # Delete the draggables from the sidebar
        del self.scroll.controls[2:]

        # Change the schedule type
        self.change_type()

        self.layout.update()


    def delete_schedule(self): #TODO - Add the Database functionality
        '''TO WRITE'''

    def save_schedule(self): #TODO - Add the Database functionality
        '''Save the schedule in the database'''
        dlg = ft.AlertDialog(
            content=ft.Text("Horario Guardado", color='#4B4669', font_family='Arial', text_align='center', size=15),
            actions=[
                ft.TextButton(
                    text='Aceptar',
                    on_click=lambda e: self.close(dlg)
                )
            ]
        )
        self.open_dlg(dlg)

        # Show all the footer buttons
        self.search_bar.visible = True
        self.schedule_buttons.controls[0].visible = True
        self.schedule_buttons.controls[1].visible = True
        self.schedule_buttons.controls[2].visible = False
        self.schedule_buttons.controls[3].visible = False
        self.schedule_buttons.controls[4].visible = True
        self.schedule_buttons.controls[5].visible = True
        self.schedule_buttons.controls[6].visible = True

        # Clear the inputs
        self.guide_teacher.value = ''

        # Disable the sidebar and the body
        self.layout.controls[0].disabled = True

        # Delete the draggables from the sidebar
        del self.scroll.controls[2:]

        # Change the schedule type
        self.change_type()

        self.layout.update()

        print(f'Seccion: {self.seccion}\nGrado: {self.grado}\nTipo: {self.tipo}\nFecha: {self.date}')


    def print_schedule(self): #TODO - Add the functionality to print the schedule
        '''TO WRITE'''

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
                ft.DataColumn(ft.Container(ft.Text('ID', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Modalidad', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Etapa', size=15, color='#4B4669', text_align='center'), width=50, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Seccion', size=15, color='#4B4669', text_align='center'), width=60, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Profesor Guia', size=15, color='#4B4669', text_align='center'), width=250, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Fecha', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
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
    def search_schedule(self):
        '''Search a schedule in the database'''

    def view(self):
        '''Change the view of the data table to the Schedule page'''
        self.body.content = Schedule(self.page, self.body)
        self.body.update()
