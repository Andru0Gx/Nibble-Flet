'''Top-Level Event'''

import datetime
import flet as ft


class Event:
    '''
    Initializes the attributes and components of the event page.

    Inputs:
    - page (ft.Page): The page object on which the event components will be displayed.

    Outputs:
    - None
    '''
    def __init__(self, page: ft.Page):
        self.page = page

        # header
        tittle = ft.Text('Agregar Eventos', size= 25, width=800, text_align='center', color='#4B4669', height=50)

        date_picker = ft.DatePicker(
            first_date= datetime.datetime(1800,1,1),
            last_date= datetime.datetime(3000,1,1),
            on_change= lambda e: self.change(date_picker.value.strftime("%d / %m / %Y")),
        )

        self.page.overlay.append(date_picker)

        # body
        self.event_name = ft.TextField(
            width=450,
            height=35,
            label='Nombre del evento',
            hint_text='Ingresa el Nombre del Evento',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            multiline=True
        )

        self.event_description = ft.TextField(
            width=450,
            height=35,
            label='Descripcion',
            hint_text='Ingresa la descripcion del Evento',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            multiline=True
        )

        self.event_date = ft.Row([
            ft.TextField(
                width=155,
                height=35,
                label='Fecha',
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
                on_click= lambda e: date_picker.pick_date(),
                border_radius=15,
                content=ft.Icon(ft.icons.CALENDAR_TODAY, color='#f3f4fa', size=20),
            )
        ])

        self.manage_button = ft.Container(
            ft.Text('Agregar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=200,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.save_event(),
            border_radius=15,
        )

        # Search bar

        self.search_bar = ft.TextField(
            width=600,
            height=35,
            label='Buscar Evento',
            hint_text='Ingresa el titulo o fecha del Evento',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
            multiline=True
        )

        search_button = ft.Container(
            ft.Text('Buscar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=100,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.search(),
            border_radius=15,
        )

        # Search List
        self.data_list = ft.DataTable(
            width=725,
            border_radius=10,
            data_row_min_height=50,
            data_row_max_height=100,
            column_spacing=0,
            horizontal_margin=0,
            checkbox_horizontal_margin=0,

            vertical_lines=ft.BorderSide(1, '#6D62A1'),
            horizontal_lines= ft.BorderSide(1, '#6D62A1'),

            border=ft.border.all(1, '#6D62A1'),

            columns=[
                ft.DataColumn(ft.Container(ft.Text('Nombre', color='#4B4669',text_align='center'), width=180)),
                ft.DataColumn(ft.Container(ft.Text('Descripcion', color='#4B4669',text_align='center'), width=180)),
                ft.DataColumn(ft.Container(ft.Text('Fecha', color='#4B4669',text_align='center'), width=180)),
                ft.DataColumn(ft.Container(ft.Text('Acciones', color='#4B4669',text_align='center'), width=180)),
            ],
        )

        search_list = ft.Container(self.data_list, alignment=ft.alignment.center, margin=0)

        self.layout = ft.Column([
            tittle,
            ft.Row([
                self.event_name,
                self.event_date
            ], spacing= 20, alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                self.event_description,
                self.manage_button,
            ], spacing= 20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(color='#4B4669'),

            ft.Row([
                self.search_bar,
                search_button,
            ], spacing= 20, alignment=ft.MainAxisAlignment.CENTER),
            search_list
        ], scroll=ft.ScrollMode.ALWAYS)

        container = ft.Container(self.layout, bgcolor='#e9ebf6', expand=True, padding=ft.padding.only(20,10,20,20))

        up_button = ft.FloatingActionButton(icon=ft.icons.ARROW_UPWARD, bgcolor='#6D62A1', on_click= lambda e: self.layout.scroll_to(offset=0,duration=100), width=50, height=50)

        page.add(container, up_button)

    def change(self, e):
        '''
        Updates the value of the event date when the date picker is changed.

        :param e: The new date value selected from the date picker.
        :return: None
        '''
        self.event_date.controls[0].read_only = False
        self.page.update()

        self.event_date.controls[0].value = e
        self.event_date.controls[0].read_only = True
        self.page.update()

    def search(self):
        pass

    def save_event(self):
        pass



def maintwo(page: ft.Page):
    '''
    Sets various properties of a page/window, such as its size, title, theme mode, and focus.

    Example Usage:
    maintwo()

    Inputs:
    None

    Outputs:
    Events page/window with the specified properties.
    '''

    page.window_center()
    page.window_width = 800
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.theme_mode = 'Light'

    page.title = 'Nibble'
    page.padding = 0

    page.window_focused = True

    page.update()

    page.window_always_on_top = True

    Event(page)

# ft.app(target=maintwo)
