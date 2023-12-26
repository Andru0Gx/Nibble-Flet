'''Top-Level Event'''

# Libraries
import time
import datetime
import threading
import flet as ft



# Database
from DB.Functions.calendar_db import save_event_db
from DB.Functions.calendar_db import get_events
from DB.Functions.calendar_db import check_amount as check
from DB.Functions.calendar_db import edit_event_db
from DB.Functions.calendar_db import get_last_event
from DB.Functions.calendar_db import delete_event_db
from DB.Functions.calendar_db import filter_event_db

#* --------------------------- Class for Infinity scroll ---------------------------
class State:
    """
    A class that represents the state of an object.
    
    Attributes:
        i (int): The value of the state.
    """
    i = 0

s = State()
sem = threading.Semaphore()


#* --------------------------- Event Page ---------------------------
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

        # Variables
        self.scrol_pos = 10

        self.page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                thickness=10,
                thumb_visibility=True,
                thumb_color='#817aa7',
            )
        )

        # header
        tittle = ft.Text('Agregar Eventos', size= 25, width=800, text_align='center', color='#4B4669', height=50)

        date_picker = ft.DatePicker(
            first_date= datetime.datetime(1800,1,1),
            last_date= datetime.datetime(3000,1,1),
            on_change= lambda e: self.change(date_picker.value.strftime("%d / %m / %Y")),
        )

        search_date_picker = ft.DatePicker(
            first_date= datetime.datetime(1800,1,1),
            last_date= datetime.datetime(3000,1,1),
            on_change= lambda e: self.search_date(search_date_picker.value.strftime("%d / %m / %Y")),
        )

        self.page.overlay.append(date_picker)
        self.page.overlay.append(search_date_picker)

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
            on_click= lambda e: self.add_event(),
            border_radius=15,
        )

        self.save_button = ft.Container(
            ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=90,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.edit_event(),
            border_radius=15,
            visible=False,
        )

        self.cancel_button = ft.Container(
            ft.Text('Cancelar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=90,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.cancel(),
            border_radius=15,
            visible=False,
        )

        # Search bar

        self.search_bar = ft.TextField(
            width=530,
            height=35,
            label='Buscar Evento',
            hint_text='Ingresa el titulo o fecha del Evento',
            bgcolor='#f3f4fa',
            hint_style=ft.TextStyle(color='#C0C1E3'),
            label_style=ft.TextStyle(color='#4B4669'),
            text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
            border_color='#6D62A1',
            content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
        )

        self.search_button = ft.Container(
            ft.Text('Buscar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
            width=100,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.search(),
            border_radius=15,
        )

        self.clear_filter_button = ft.Container(
            ft.Icon(ft.icons.FILTER_ALT_OFF, color='#f3f4fa', size=20),
            width=35,
            height=35,
            bgcolor='#6D62A1',
            alignment=ft.alignment.center,
            on_click= lambda e: self.clear_filter(),
            border_radius=15,
            tooltip='Limpiar Filtro'
        )

        self.search_date_button = ft.Container(
                width=35,
                height=35,
                bgcolor= '#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: search_date_picker.pick_date(),
                border_radius=15,
                content=ft.Icon(ft.icons.CALENDAR_TODAY, color='#f3f4fa', size=20),
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
            horizontal_lines= ft.BorderSide(1, '#6D62A1'),
            show_bottom_border=True,
            heading_row_height=0,

            columns=[
                ft.DataColumn(ft.Container( width=180)),
                ft.DataColumn(ft.Container( width=180)),
                ft.DataColumn(ft.Container( width=180)),
                ft.DataColumn(ft.Container( width=180)),
                ],
        )

        self.data_scroll = ft.Column([self.data_list],scroll=True, on_scroll_interval=0, on_scroll= lambda e: self.on_scroll(e))

        search_list = ft.Container(self.data_scroll, alignment=ft.alignment.top_center, margin=0, width=725,height=350, border=ft.border.all(1, '#6D62A1'), border_radius=10)

        self.layout = ft.Column([
            tittle,
            ft.Row([
                self.event_name,
                self.event_date
            ], spacing= 20, alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                self.event_description,
                self.manage_button,
                self.save_button,
                self.cancel_button
            ], spacing= 20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(color='#4B4669'),

            ft.Row([
                self.search_bar,
                self.search_date_button,
                self.search_button,
                self.clear_filter_button
            ], spacing= 10, alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                ft.Container(
                    ft.Text('Nombre', color='#4B4669',text_align='center', size=15, weight=ft.FontWeight.W_600),
                    width=180,
                    height=30,
                    alignment=ft.alignment.center
                    ),

                ft.Container(
                    ft.Text('Descripcion', color='#4B4669',text_align='center', size=15, weight=ft.FontWeight.W_600),width=180,
                    height=30,
                    alignment=ft.alignment.center
                    ),

                ft.Container(
                    ft.Text('Fecha', color='#4B4669',text_align='center', size=15, weight=ft.FontWeight.W_600),
                    width=180,
                    height=30,
                    alignment=ft.alignment.center
                    ),

                ft.Container(
                    ft.Text('Acciones', color='#4B4669',text_align='center', size=15, weight=ft.FontWeight.W_600), width=180,
                    height=30,
                    alignment=ft.alignment.center
                    ),
            ], width=725, spacing=0),

            search_list
        ], horizontal_alignment='center')

        container = ft.Container(self.layout, bgcolor='#e9ebf6', expand=True, padding=ft.padding.only(20,10,20,20))

        up_button = ft.FloatingActionButton(icon=ft.icons.ARROW_UPWARD, bgcolor='#6D62A1', on_click= lambda e: self.data_scroll.scroll_to(offset=0,duration=100), width=50, height=50)

        page.add(container, up_button)

        self.show_events()

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
        '''Searches for an event in the database.'''
        search = self.search_bar.value

        if search == '':
            self.search_button.bgcolor = '#ff0000'
            self.search_button.content.value = 'Campo vacio'
            self.page.update()
            time.sleep(1)
            self.search_button.bgcolor = '#6D62A1'
            self.search_button.content.value = 'Buscar'
            self.page.update()
        else:
            self.data_list.rows.clear()

            list_events = filter_event_db(search)

            for event in list_events:
                row = ft.DataRow([
                    ft.DataCell(ft.Container(ft.Text(event['title'], color='#4B4669',text_align='center', size=15), width=180)),
                    ft.DataCell(ft.Container(ft.Text(event['description'], color='#4B4669',text_align='center', size=15), width=180)),
                    ft.DataCell(ft.Container(ft.Text(event['date'], color='#4B4669',text_align='center', size=15), width=180)),
                    ft.DataCell(ft.Container(self.edit_set(event['date'], event['title'], event['description'], event['id']), width=180)),
                ], data=event['id'])
                self.data_list.rows.append(row)

            self.page.update()
            self.data_scroll.scroll_to(offset=0,duration=100)

    def search_date(self, date):
        """
        Search for events based on a specific date.

        Args:
            date (str): The date to search for events in the format 'YYYY-MM-DD'.

        Returns:
            None

        Example:
            event = Event(page)
            event.search_date('2022-12-31')
        """
        self.search_bar.value = ''
        self.page.update()

        self.search_bar.value = date
        self.page.update()


    def clear_filter(self):
        '''Clears the search bar and shows all the events in the database.'''
        self.search_bar.value = ''
        self.data_list.rows.clear()
        self.show_events()
        self.data_scroll.scroll_to(offset=0,duration=100)

    def add_event(self):
        '''Saves the event in the database.'''
        if self.event_name.value != '' and self.event_description.value != '' and self.event_date.controls[0].value != '':
            save_event_db(self.event_name.value, self.event_description.value, self.event_date.controls[0].value)

            id = get_last_event()

            self.manage_button.bgcolor = '#00ff00'
            self.manage_button.content.value = 'Evento agregado'
            self.manage_button.disabled = True

            # add the event to the table
            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(self.event_name.value, color='#4B4669',text_align='center', size=15), width=180)),
                ft.DataCell(ft.Container(ft.Text(self.event_description.value, color='#4B4669',text_align='center', size=15), width=180)),
                ft.DataCell(ft.Container(ft.Text(self.event_date.controls[0].value, color='#4B4669',text_align='center', size=15), width=180)),
                ft.DataCell(ft.Container(self.edit_set(self.event_date.controls[0].value, self.event_name.value, self.event_description.value, id), width=180)),
            ], data=id)
            self.data_list.rows.append(row)

            self.page.update()

            time.sleep(1)
            self.manage_button.bgcolor = '#6D62A1'
            self.manage_button.content.value = 'Agregar'
            self.manage_button.disabled = False

            self.event_name.value = ''
            self.event_description.value = ''
            self.event_date.controls[0].value = ''

            self.page.update()
        else:
            self.manage_button.bgcolor = '#ff0000'
            self.manage_button.content.value = 'Rellene todos los campos'
            self.page.update()
            time.sleep(1)
            self.manage_button.bgcolor = '#6D62A1'
            self.manage_button.content.value = 'Agregar'
            self.page.update()


    def show_events(self):
        '''Shows the events in the table'''

        if check() < 10:
            list_events = get_events(0, check())
            last = check()
        else:
            list_events = get_events(0, 9)
            last = 9




        for i in range(0, last):
            row = ft.DataRow([
                ft.DataCell(ft.Container(ft.Text(list_events[i]['title'], color='#4B4669',text_align='center', size=15), width=180)),
                ft.DataCell(ft.Container(ft.Text(list_events[i]['description'], color='#4B4669',text_align='center', size=15), width=180)),
                ft.DataCell(ft.Container(ft.Text(list_events[i]['date'], color='#4B4669',text_align='center', size=15), width=180)),
                ft.DataCell(ft.Container(self.edit_set(list_events[i]['date'], list_events[i]['title'], list_events[i]['description'], list_events[i]['id']), width=180)),
            ],data=list_events[i]['id'])
            self.data_list.rows.append(row)

        self.page.update()

    def edit_set(self, date, title, description, id):
        '''Sets the edit mode of the table'''
        return ft.Row([
                    ft.IconButton(icon=ft.icons.EDIT, on_click= lambda e: self.activate_edit(e), width=50, height=50, icon_color='#3741c8', data=[date, title, description, id]),
                    ft.IconButton(icon=ft.icons.DELETE, on_click= lambda e: self.delete(e), width=50, height=50, icon_color='#ff0000', data=[date, title, description, id]),
                ], alignment=ft.MainAxisAlignment.CENTER)


    def activate_edit(self, e):
        '''Edits the event in the database.'''
        self.event_name.value = e.control.data[1]
        self.event_description.value = e.control.data[2]
        self.event_date.controls[0].value = e.control.data[0]
        self.save_button.data = e.control.data

        self.manage_button.visible = False
        self.save_button.visible = True
        self.cancel_button.visible = True
        self.page.update()

    def cancel(self):
        '''Cancels the edit mode of the table'''
        self.event_name.value = ''
        self.event_description.value = ''
        self.event_date.controls[0].value = ''

        self.manage_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.page.update()


    def edit_event(self):
        '''Saves the edited event in the database.'''
        if self.event_name.value != '' and self.event_description.value != '' and self.event_date.controls[0].value != '':
            edit_event_db(self.event_name.value, self.event_description.value, self.event_date.controls[0].value, self.save_button.data[3])

            self.manage_button.bgcolor = '#00ff00'
            self.manage_button.content.value = 'Evento Editado'
            self.manage_button.disabled = True
            self.manage_button.visible = True
            self.save_button.visible = False
            self.cancel_button.visible = False

            # add the event to the table
            for row in self.data_list.rows:
                if row.data == self.save_button.data[3]:
                    row.cells[0].content.content.value = self.event_name.value
                    row.cells[1].content.content.value = self.event_description.value
                    row.cells[2].content.content.value = self.event_date.controls[0].value
                    row.cells[3].content.content = self.edit_set(self.event_date.controls[0].value, self.event_name.value, self.event_description.value, self.save_button.data[3])
                    break

            self.page.update()

            time.sleep(1)
            self.manage_button.bgcolor = '#6D62A1'
            self.manage_button.content.value = 'Agregar'
            self.manage_button.disabled = False

            self.event_name.value = ''
            self.event_description.value = ''
            self.event_date.controls[0].value = ''

            self.page.update()

        else:
            self.save_button.bgcolor = '#ff0000'
            self.save_button.width = 200
            self.save_button.content.value = 'Rellene todos los campos'
            self.cancel_button.visible = False
            self.page.update()
            time.sleep(1)
            self.save_button.bgcolor = '#6D62A1'
            self.save_button.width = 90
            self.save_button.content.value = 'Guardar'
            self.cancel_button.visible = True
            self.page.update()


    def open_dlg(self, dlg):
        """
        Open a dialog box in the user interface.

        :param dlg: The dialog box object that needs to be opened.
        :type dlg: object
        """
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def dlg_close(self, dlg, delete, id = None):
        """
        Closes the dialog box by setting its 'open' attribute to False and updating the page.

        Args:
            dlg (Dialog): The dialog box to be closed.

        Returns:
            None
        """
        if delete:
            delete_event_db(id)

            self.scrol_pos -= 1

            for row in self.data_list.rows:
                if row.data == id:
                    self.data_list.rows.remove(row)
                    self.page.update()
                    break

            # add another row to the table
            if len(self.data_list.rows) < 10:
                list_events = get_events(self.scrol_pos, self.scrol_pos + 9)

                # Verifica que hay eventos para agregar
                if list_events:
                    for event in list_events:
                        row = ft.DataRow([
                            ft.DataCell(ft.Container(ft.Text(event['title'], color='#4B4669', text_align='center', size=15), width=180)),
                            ft.DataCell(ft.Container(ft.Text(event['description'], color='#4B4669', text_align='center', size=15), width=180)),
                            ft.DataCell(ft.Container(ft.Text(event['date'], color='#4B4669', text_align='center', size=15), width=180)),
                            ft.DataCell(ft.Container(self.edit_set(event['date'], event['title'], event['description'], event['id']), width=180)),
                        ], data=event['id'])
                        self.data_list.rows.append(row)

                    self.page.update()
                    self.scrol_pos += 10

        dlg.open = False
        self.page.update()

    def delete(self, e):
        '''Deletes the event in the database.'''
        id = e.control.data[3]

        dlg = ft.AlertDialog(
            content=ft.Text('¿Estas seguro que quieres eliminar este evento?', color='#4B4669', size=15, text_align='center'),
            actions=[
                ft.ElevatedButton('Eliminar', on_click= lambda e: self.dlg_close(dlg,True, id)),
                ft.ElevatedButton('Cancelar', on_click= lambda e: self.dlg_close(dlg,False)),
            ]
        )

        self.open_dlg(dlg)


    def on_scroll(self, e: ft.OnScrollEvent):
        '''
        Adds events to the table when the user scrolls to the bottom of the table.

        :param e: The scroll event.
        :return: None
        '''
        if e.pixels >= e.max_scroll_extent - 100:
            if sem.acquire(blocking=False):
                try:
                    # Obten eventos desde la posición actual hasta la posición + 9
                    list_events = get_events(self.scrol_pos, self.scrol_pos + 9)

                    # Verifica que hay eventos para agregar
                    if list_events:
                        for event in list_events:
                            row = ft.DataRow([
                                ft.DataCell(ft.Container(ft.Text(event['title'], color='#4B4669', text_align='center', size=15), width=180)),
                                ft.DataCell(ft.Container(ft.Text(event['description'], color='#4B4669', text_align='center', size=15), width=180)),
                                ft.DataCell(ft.Container(ft.Text(event['date'], color='#4B4669', text_align='center', size=15), width=180)),
                                ft.DataCell(ft.Container(self.edit_set(event['date'], event['title'], event['description'], event['id']), width=180)),
                            ], data=event['id'])
                            self.data_list.rows.append(row)

                        self.page.update()
                        self.scrol_pos += 10
                finally:
                    sem.release()




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
