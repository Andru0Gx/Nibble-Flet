'''Flet Calendar'''

# Libraries
import datetime
import calendar
import locale
from calendar import HTMLCalendar
from dateutil import relativedelta
import flet as ft

# Database
from DB.Functions.calendar_db import filter_event_db

# Don't show the defined outside of class warning.
# pylint: disable=W0201
# Pylint: disable=

# Set the locale for the calendar.
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

class FletCalendar(ft.UserControl):
    '''Flet Calendar'''
    def __init__(self, page, events):
        super().__init__()

        self.page = page
        self.get_current_date()
        self.set_theme()
        self.events = events

        # Init the container control.
        self.calendar_container = ft.Container(
            width=1000,
            height=600,
            padding=ft.padding.all(2),
            border=ft.border.all(2, self.border_color),
            border_radius=ft.border_radius.all(10),
            alignment=ft.alignment.bottom_center,
            bgcolor='#f8f8fa'
        )

        self.build() # Build the calendar.
        self.output = ft.Text() # Add output control.


    def filter_event(self, date, all = False):
        '''Filter the events'''
        date = datetime.datetime.strptime(date, '%d / %m / %Y').strftime('%d / %m / %Y')
        if filter_event_db(date, True):
            event_info = filter_event_db(date, True)
            list_event = ''

            if all:
                return event_info

            for event in event_info:
                # only save up to 3 events
                if event_info.index(event) < 3:
                    list_event += f'{event_info.index(event) + 1} - {event["title"]}\n'
                else:
                    list_event += '....'
                    break
            list_event = list_event[:-1]
            return list_event
        else:
            return False

    def get_current_date(self):
        '''Get the initial current date'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day   = today.day
        self.current_year  = today.year

    def selected_date(self, e):
        '''User selected date'''
        # Format the date example: January 1, 2021
        str_date = f'{e.control.data[0]} / {e.control.data[1]} / {e.control.data[2]}'


        event_list = self.filter_event(str_date, True)

        if event_list:
            new_event_list = ''

            for event in event_list:
                new_event_list += f'{event_list.index(event) + 1} - {event["title"]}\n'

            # Create the dlg
            dlg = ft.AlertDialog(
                content=ft.Column([
                    ft.Text(f'Eventos del Dia {str_date}', size=20, color='#4B4669', font_family='Arial', text_align='center', width=300, height=30),
                    ft.Divider(height=1, thickness=2.0, color=self.border_color),

                    ft.Column([
                        ft.Text(new_event_list, size=16, color='#4B4669', font_family='Arial', text_align='left'),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, scroll=True, width=300, height=80),
                ], alignment=ft.MainAxisAlignment.START, spacing=10, width=300, height=120),
                actions=[
                    ft.Container(content=
                        ft.ElevatedButton(text='Aceptar', on_click= lambda e: self.close(dlg)), alignment=ft.alignment.center, width=300, height=30
                    ),
                ]
            )

            # Open the dlg
            self.open_dlg(dlg)


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


    def set_current_date(self):
        '''Set the calendar to the current date.'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day   = today.day
        self.current_year  = today.year
        self.build()
        self.calendar_container.update()

    def get_next(self, e):
        '''Move to the next month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month

        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_prev(self, e):
        '''Move to the previous month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_calendar(self):
        '''Get the calendar from the calendar module.'''
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)

    def set_theme(self, border_color='#6D62A1',
                text_color='#4B4669',
                current_day_color='#9a96bc', hover_color='#817aa7', event_color=ft.colors.CYAN_600):
        '''Set the theme for the calendar.'''
        self.border_color = border_color
        self.text_color = text_color
        self.current_day_color = current_day_color
        self.hover_color = hover_color
        self.event_color = event_color

    def hover(self, e, header=False):
        '''Hover over a day.'''

        # if iscurrent day
        if header:
            if e.control.bgcolor == self.current_day_color:
                return
            else:
                e.control.bgcolor = '#e9ebf6' if e.data == "true" else '#f8f8fa'
                e.control.update()
        else:
            e.control.bgcolor = self.hover_color if e.data == "true" else e.control.data[3]
            e.control.update()

    def event(self):
        '''Show the events'''
        import modules.section_manager as pm
        ft.app(target=pm.def_events)
        self.build()
        self.calendar_container.update()


    def build(self):
        '''Build the calendar for flet.'''
        current_calendar = self.get_calendar()
        actual_month = datetime.datetime.today().month
        # print(actual_month)

        # Format the date example: January 1, 2021
        str_date = f'{self.current_day}, {calendar.month_name[self.current_month]} {self.current_year}'

        date_display = ft.Text(str_date, text_align='center', size=25, color=self.text_color)
        next_button = ft.Container( ft.Text('>', text_align='center', size=25, color=self.text_color), on_click=self.get_next, on_hover=lambda e: self.hover(e, True), border_radius=ft.border_radius.all(10), width=40, height=40 )
        prev_button = ft.Container( ft.Text('<', text_align='center', size=25, color=self.text_color), on_click=self.get_prev, on_hover=lambda e: self.hover(e, True), border_radius=ft.border_radius.all(10), width=40, height=40 )
        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)

        # create the week format (Lu, Ma, Mi, Ju, Vi, Sa, Do)
        week_format = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=80)

        for day in calendar.day_name:
            day = day[0:3]
            container_week = ft.Container(content=ft.Text(day, size=20, color=self.text_color, text_align='center'),width=60, height=40, border_radius=ft.border_radius.all(10))
            week_format.controls.append(container_week)

        events = ft.ElevatedButton(text='Eventos', width=100, height=30, style=ft.ButtonStyle(bgcolor='#b6b9da', color='#454167',shape=ft.RoundedRectangleBorder(radius=10), side=ft.BorderSide(1,'#625a9b')), on_click= lambda e: self.event(), top=7.5, left= 30)


        calendar_column = ft.Column([ft.Stack([
            events,
            ft.Row([prev_button,date_display,next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=40, expand= False)
        ]), div, week_format],spacing=10, width=1100, height=600, alignment=ft.MainAxisAlignment.SPACE_EVENLY, expand=False)

        # Loop weeks and add row.
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=80)
            # Loop days and add days to row.
            for day in week:
                if day > 0:
                    display_day = str(day)
                    if self.filter_event(f'{day} / {self.current_month} / {self.current_year}'):
                        event_info = self.filter_event(f'{day} / {self.current_month} / {self.current_year}')
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.event_color
                    else:
                        event_info = 'No hay eventos'
                        is_current_day_font = ft.FontWeight.W_300
                        is_current_day_bg = ft.colors.TRANSPARENT

                    if len(str(display_day)) == 1:
                        display_day = str(display_day).zfill(2)
                    if day == self.current_day and self.current_month == actual_month:
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color

                        if self.filter_event(f'{day} / {self.current_month} / {self.current_year}'):
                            event_info = self.filter_event(f'{day} / {self.current_month} / {self.current_year}')[1]
                            is_current_day_font = ft.FontWeight.BOLD
                            is_current_day_bg = '#8ea4c6'

                    day_button = ft.Container(
                        content=ft.Text(
                            str(display_day),
                            weight=is_current_day_font,
                            color=self.text_color,
                            size=20,
                            text_align='center'
                        ),
                        on_click=self.selected_date,
                        data=(day,self.current_month, self.current_year, is_current_day_bg),
                        width=60,
                        height=60,
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(50),
                        bgcolor=is_current_day_bg,
                        on_hover=lambda e: self.hover(e),
                        tooltip=event_info
                    )


                else:
                    day_button = ft.Container(width=60, height=60, border_radius=ft.border_radius.all(10))

                week_row.controls.append(day_button)
            # Add the weeks to the main column.
            calendar_column.controls.append(week_row)
        # Add column to our page container.
        self.calendar_container.content = calendar_column
        return self.calendar_container
