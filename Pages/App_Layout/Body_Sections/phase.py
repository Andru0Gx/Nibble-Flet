'''Phase Layout'''

# Libraries
import time
import threading
import flet as ft

# Database
from DB.Functions.phases_db import get_phases, get_x_phases, check_amount as check, filter_phases_db
from DB.Functions.grades_db import verify_promote_student


class State:
    """
    A class that represents the state of an object.
    
    Attributes:
        i (int): The value of the state.
    """
    i = 0

s = State()
sem = threading.Semaphore()


class Phases(ft.UserControl):
    '''Phases'''
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.scrol_pos = 7

        #* ------------------ Layout ------------------ *#
        # Create the Title
        self.title = ft.Text(
            'Lista de Etapas',
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
            label='Buscar Etapa',
            hint_text='Ingresa un dato del Etapa',
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
                on_click= lambda e: self.search_phase(),
                border_radius=15,
                content=ft.Icon(ft.icons.SEARCH, color='#f3f4fa', size=20),
            )
        ])

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

        # Create the Data Table
        self.data_table = ft.DataTable(
            width=1100,
            border_radius=10,
            data_row_min_height=50,
            data_row_max_height=80,
            column_spacing=10,
            horizontal_margin=0,
            horizontal_lines= ft.BorderSide(1, '#6D62A1'),
            show_bottom_border=True,


            columns=[
                ft.DataColumn(ft.Container(ft.Text('ID', size=18, color='#4B4669', text_align='center'), width=135, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Etapa', size=18, color='#4B4669', text_align='center'), width=135, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Seccion', size=18, color='#4B4669', text_align='center'), width=135, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Acciones', size=18, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ],
        )

        self.scrol = ft.Column([
            self.data_table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1100, height=490, on_scroll= lambda e: self.on_scroll(e))

        self.data_container = ft.Container(self.scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#6D62A1'), border_radius=10, width=1100, height=500)

        up_button = ft.FloatingActionButton(content=ft.Icon(ft.icons.ARROW_UPWARD, color='#f3f4fa', size=20), bgcolor='#6D62A1', on_click= lambda e: self.scrol.scroll_to(offset=0,duration=100), width=50, height=35)

        # Create the Layout
        layout = ft.Column([
            self.title,
            ft.Row([
                    self.search_bar,
                    self.clear_filter_button,
                    up_button
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            self.data_container,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

        # Show the phases
        self.show_phases()

    def build(self):
        return self.content

    #^ ------------------ Functions ------------------ *#
    def show_phases(self):
        """
        Show Phases

        This method displays a list of phases based on the current check status. If the check is less than 7,
        it fetches the phases from index 0 to the current check value. Otherwise, it grabs phases from 0 to 6.
        The 'last' variable is set accordingly.

        Parameters:
            - self: The instance of the class.
            
        Returns:
            None

        Usage Example:
            instance.show_phases()
        """
        if check() < 7:
            phases_list = get_x_phases(0, check())
            last = check()
        else:
            phases_list = get_x_phases(0, 6)
            last = 6
        for i in range(0, last):
            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(phases_list[i]['ID'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(phases_list[i]['Grado/Año'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(ft.Text(phases_list[i]['Seccion'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                ft.DataCell(ft.Container(self.edit_set(phases_list[i]), width=200, alignment=ft.alignment.center)),
            ], data=phases_list[i]['ID'])
            self.data_table.rows.append(row)
        self.update()

    def edit_set(self, data):
        """
        Edit Set

        This method creates an ElevatedButton with specific properties for promoting a set of data.

        Parameters:
            - self: The instance of the class.
            - data: The data associated with the button.

        Returns:
            ft.ElevatedButton: The configured button.

        Usage Example:
            button = instance.edit_set(some_data)
        """
        return ft.ElevatedButton(
            text='Promover',
            width=120,
            height=35,
            bgcolor='#d7d9ee',
            color='#4a4669',
            on_click= lambda e: self.promote_all_confirm(data),
        )



    #* ------------------ Search Fuctions ------------------ *#
    def search_phase(self):
        '''Search a phase in the database'''
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

            phases_list = filter_phases_db(search)

            for phase in phases_list:
                row = ft.DataRow([
                    ft.DataCell(ft.Container(ft.Text(phase['ID'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(phase['Grado/Año'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(phase['Seccion'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(self.edit_set(phase), width=200, alignment=ft.alignment.center)),
                ], data=phase['ID'])
                self.data_table.rows.append(row)
            self.clear_filter_button.visible = True
            self.update()
            self.scrol.scroll_to(offset=0,duration=100)
            self.scrol_pos = check() + 1 # To avoid the scroll event

    def clear_filter(self):
        '''Clear the filter of the data table'''
        self.scrol.scroll_to(offset=0,duration=100)
        self.scrol_pos = 7
        self.search_bar.controls[0].value = ''
        del self.data_table.rows[:]
        self.clear_filter_button.visible = False
        self.update()
        self.show_phases()



    #* ------------------ Pass Fuctions ------------------ *#
    def promote_all_confirm(self, data):
        '''Pass all the students to the next phase'''

        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text('Promover Estudiantes', color='#4B4669', font_family='Arial', size=20),
                ft.Text(f"Etapa Seleccionada: {data['Grado/Año']} {data['Seccion']}", color='#4B4669', font_family='Arial', size=15),
                ft.Dropdown(
                    width=300,
                    height=35,
                    label='Siguiente Etapa (Grado/Año)',
                    hint_text='Selecciona la Siguiente Etapa',
                    filled=True,
                    bgcolor='#f3f4fa',
                    hint_style=ft.TextStyle(color='#C0C1E3'),
                    label_style=ft.TextStyle(color='#4B4669'),
                    text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                    border_color='#6D62A1',
                    content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                ),
                ft.Switch(
                    height=35,
                    label='Graduado (Ultimo año Liceo)',
                    value=False,
                    on_change= lambda e: self.switch_phase(e, dlg),
                ),
            ], spacing=10, width=300, height=150, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg), bgcolor='#6D62A1', color='#f3f4fa'),
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.validate_dlg(dlg, data), bgcolor='#6D62A1', color='#f3f4fa')
            ]
        )
        self.drop_options(dlg)
        self.open_dlg(dlg)

    def switch_phase(self, e, dlg):
        """
        Switch Phase

        This function toggles the state of a phase based on the provided event and dialog.

        Parameters:
            - self: The instance of the class.
            - e: The event triggering the switch.
            - dlg: The dialog associated with the switch.

        Returns:
            None

        Usage Example:
            instance.switch_phase(event, dialog)
        """
        if e.control.value:
            dlg.content.controls[2].disabled = True
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
            dlg.content.controls[2].options.append(ft.dropdown.Option(text= f"{phase['Grado/Año']} {phase['Seccion']}", key=phase))

        self.update()

    def validate_dlg(self, dlg, data):
        """
        Validate Dialog

        This method performs validation checks on the provided dialog and data. It handles different scenarios,
        such as promoting all with a second confirmation if a specific control value is true, or displaying error
        messages and updating the dialog accordingly.

        Parameters:
            - self: The instance of the class.
            - dlg: The dialog to be validated.
            - data: The data used for validation.

        Returns:
            None

        Usage Example:
            instance.validate_dlg(dialog_instance, some_data)
        """
        if dlg.content.controls[3].value:
            self.promote_all_second_confirm(dlg, 'Graduado', data = data)
        else:
            if dlg.content.controls[2].value is None:
                dlg.actions[1].bgcolor = '#ff0000'
                dlg.actions[1].text = 'Campo Vacio'
                dlg.update()
                time.sleep(1)
                dlg.actions[1].bgcolor = '#6D62A1'
                dlg.actions[1].text = 'Aceptar'
                dlg.update()
            elif eval(dlg.content.controls[2].value)['Grado/Año'] == f"{data['Grado/Año']}":
                dlg.actions[1].bgcolor = '#ff0000'
                dlg.actions[1].text = 'La Etapa es la misma'
                dlg.update()
                time.sleep(1)
                dlg.actions[1].bgcolor = '#6D62A1'
                dlg.actions[1].text = 'Aceptar'
                dlg.update()
            else:
                self.promote_all_second_confirm(dlg, data = data)


    def promote_all_second_confirm(self, dlg, op = False, data = None):
        """
        Promote All Second Confirm

        This method handles the second confirmation step for promoting all. It updates the dialog actions dynamically,
        providing a countdown and then changing the confirmation button to trigger the promotion.

        Parameters:
            - self: The instance of the class.
            - dlg: The dialog to be updated.
            - op: The operation flag (default is False).
            - data: The data associated with the promotion (default is None).

        Returns:
            None

        Usage Example:
            instance.promote_all_second_confirm(dialog_instance, some_operation, some_data)
        """
        try:
            dlg.actions[1].on_click = None
            for i in range(5, -1, -1):
                dlg.actions[1].text = f'Espere {i} segundos...'
                dlg.update()
                time.sleep(1)

            dlg.actions[1].text = 'Confirmar Promover'
            dlg.actions[1].bgcolor = '#70f83a'
            dlg.actions[1].color = '#2d2d2d'
            dlg.actions[1].on_click = lambda e: self.promote_all(dlg, op, data)
            dlg.update()
        except:
            pass


    def promote_all(self, dlg, op, data):
        '''Pass all the students to the next phase'''
        if op != 'Graduado':
            new_phase = eval(dlg.content.controls[2].value)
            if isinstance(verify_promote_student(data,new_phase), dict):
                self.close(dlg)
                student = verify_promote_student(data,new_phase)
                self.student_without_notes(student)
            else:
                dlg.actions[1].bgcolor = '#70f83a'
                dlg.actions[1].color = '#2d2d2d'
                dlg.actions[1].text = 'Estudiantes Promovidos'
                dlg.update()
                time.sleep(1.5)
                self.close(dlg)
        else:
            if isinstance(verify_promote_student(data, graduate=True), dict):
                self.close(dlg)
                student = verify_promote_student(data, graduate=True)
                self.student_without_notes(student)
            else:
                dlg.actions[1].bgcolor = '#70f83a'
                dlg.actions[1].color = '#2d2d2d'
                dlg.actions[1].text = 'Estudiantes Graduados'
                dlg.update()
                time.sleep(1.5)
                self.close(dlg)



    def student_without_notes(self, data):
        """
        Student Without Notes

        This method creates an AlertDialog to inform about a student without approved or rejected status.
        It displays the student's name, ID, and a message indicating the absence of approval or rejection.

        Parameters:
            - self: The instance of the class.
            - data: The data associated with the student.

        Returns:
            None

        Usage Example:
            instance.student_without_notes(some_data)
        """
        fullname = f"{data['name']} {data['lastname']}"
        fullname = fullname.title()
        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text(f"El estudiante {fullname}", color='#4B4669', font_family='Arial', size=15),
                ft.Text(f"Cedula {data['CI']}", color='#4B4669', font_family='Arial', size=15),
                ft.Text("Aun no ha sido aprobado o reprobado", color='#4B4669', font_family='Arial', size=15, italic=True),
            ], spacing=10, width=300, height=100, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
            actions=[
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg), bgcolor='#6D62A1', color='#f3f4fa')
            ],
        )
        self.open_dlg(dlg)

    def phase_without_students(self):
        """
        Phase Without Students

        This method creates an AlertDialog to inform that there are no students in the current phase.
        It displays a message indicating the absence of students in the phase.

        Parameters:
            - self: The instance of the class.

        Returns:
            None

        Usage Example:
            instance.phase_without_students()
        """
        dlg = ft.AlertDialog(
            content=ft.Column([
                ft.Text("No hay estudiantes en esta etapa", color='#4B4669', font_family='Arial', size=15),
            ], spacing=10, width=250, height=30, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
            actions=[
                ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg), bgcolor='#6D62A1', color='#f3f4fa')
            ],
        )
        self.open_dlg(dlg)


    #* ------------------ SCROLL Fuctions ------------------ *#
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
                    # Obten fases desde la posición actual hasta la posición + 6
                    phase_list = get_x_phases(self.scrol_pos, self.scrol_pos + 6)
                    #Verificar si la lista esta vacia
                    if phase_list:
                        for phase in phase_list:
                            row = ft.DataRow([
                                ft.DataCell(ft.Container(ft.Text(phase['ID'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(phase['Grado/Año'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(ft.Text(phase['Seccion'], color='#4B4669', font_family='Arial', size=15), width=135, alignment=ft.alignment.center)),
                                ft.DataCell(ft.Container(self.edit_set(phase), width=200, alignment=ft.alignment.center)),
                            ], data=phase['ID'])
                            self.data_table.rows.append(row)
                        self.update()
                        self.scrol_pos += 7
                finally:
                    sem.release()

    #* ------------------ DLG Fuctions ------------------ *#
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
