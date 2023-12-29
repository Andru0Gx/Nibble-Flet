'''Phase Layout'''

# Libraries
import flet as ft

class Phases(ft.UserControl):
    '''Phases'''
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

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

        # Create a button to pass all the students to the next phase
        self.pass_all_button = ft.Container(
            content=ft.Text('Aprobar a Todos', color='#f3f4fa', size=15, text_align='center'),
            width=150,
            height=35,
            bgcolor='#6D62A1',
            border_radius=10,
            on_click= lambda e: self.pass_all(),
            alignment=ft.alignment.center,
        )

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
                ft.DataColumn(ft.Container(ft.Text('Fecha', size=15, color='#4B4669', text_align='center'), width=100, alignment=ft.alignment.center)),
                ft.DataColumn(ft.Container(ft.Text('Acciones', size=15, color='#4B4669', text_align='center'), width=200, alignment=ft.alignment.center)),
                ],
        )

        scrol = ft.Column([
            self.data_table,
        ], alignment=ft.MainAxisAlignment.START, spacing=20, scroll=ft.ScrollMode.ALWAYS, width=1100, height=490)

        self.data_container = ft.Container(scrol, alignment=ft.alignment.top_center, margin=0, border=ft.border.all(2, '#6D62A1'), border_radius=10, width=1100, height=500)

        up_button = ft.FloatingActionButton(content=ft.Icon(ft.icons.ARROW_UPWARD, color='#f3f4fa', size=20), bgcolor='#6D62A1', on_click= lambda e: scrol.scroll_to(offset=0,duration=100), width=50, height=35)

        # Create the Layout
        layout = ft.Column([
            self.title,
            ft.Row([
                    self.search_bar,
                    self.pass_all_button,
                    up_button
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            self.data_container,
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center', spacing=20)

        # add the layout to the page
        self.content = layout

    def build(self):
        return self.content

    #^ ------------------ Functions ------------------ *#
    def search_phase(self):
        '''Search a phase in the database'''

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

    def pass_all(self):
        '''Pass all the students to the next phase'''

        # Create the DLG to confirm the action
        dlg = ft.AlertDialog(
            content=ft.Text('¿Estás seguro de que quieres aprobar a todos los estudiantes?'),
            actions=[ft.Row([
                ft.ElevatedButton(text='Cancelar', on_click= lambda e: self.close(dlg)),
                ft.ElevatedButton(text='Aprobar', on_click= lambda e: self.close(dlg)), #TODO - Add the function to pass all the students
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)],
        )

        # Open the DLG
        self.open_dlg(dlg)
