'''Flet Calendar'''

import datetime
import calendar
import locale
from calendar import HTMLCalendar
from dateutil import relativedelta
import flet as ft

# Don't show the defined outside of class warning.
# pylint: disable=W0201
# Pylint: disable=

# Set the locale for the calendar.
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

class FletCalendar(ft.UserControl):
    '''Flet Calendar'''
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.get_current_date()
        self.set_theme()

        # Init the container control.
        self.calendar_container = ft.Container(width=1100, height=500,
                                          padding=ft.padding.all(2),
                                          border=ft.border.all(2, self.border_color),
                                          border_radius=ft.border_radius.all(10),
                                          alignment=ft.alignment.bottom_center, bgcolor='#e9ebf6')

        self.build() # Build the calendar.
        self.output = ft.Text() # Add output control.

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
        # self.output.value = str_date
        print(str_date)


        # self.output.value = e.control.data
        # self.output.update()
        #return e.control.data

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
                  current_day_color='#7e73b8', hover_color='#817aa7'):
        '''Set the theme for the calendar.'''
        self.border_color = border_color
        self.text_color = text_color
        self.current_day_color = current_day_color
        self.hover_color = hover_color

    def hover(self, e):
        '''Hover over a day.'''

        # if iscurrent day
        if e.control.bgcolor == self.current_day_color:
            return
        else:
            e.control.bgcolor = '#817aa7' if e.data == "true" else '#e9ebf6'
            e.control.update()

    def build(self):
        '''Build the calendar for flet.'''
        current_calendar = self.get_calendar()

        # Format the date example: January 1, 2021
        str_date = f'{self.current_day}, {calendar.month_name[self.current_month]} {self.current_year}'

        date_display = ft.Text(str_date, text_align='center', size=25, color=self.text_color)
        next_button = ft.Container( ft.Text('>', text_align='center', size=25, color=self.text_color), on_click=self.get_next, on_hover=lambda e: self.hover(e), border_radius=ft.border_radius.all(10), width=40, height=40 )
        prev_button = ft.Container( ft.Text('<', text_align='center', size=25, color=self.text_color), on_click=self.get_prev, on_hover=lambda e: self.hover(e), border_radius=ft.border_radius.all(10), width=40, height=40 )
        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)

        # create the week format (Lu, Ma, Mi, Ju, Vi, Sa, Do)
        week_format = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=90)

        for day in calendar.day_name:
            day = day[0:3]
            container_week = ft.Container(content=ft.Text(day, size=20, color=self.text_color, text_align='center'),width=60, height=40, border_radius=ft.border_radius.all(10))
            week_format.controls.append(container_week)



        calendar_column = ft.Column([ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER, height=40, expand=False), div, week_format],
                                    spacing=25, width=1100, height=700, alignment=ft.MainAxisAlignment.CENTER, expand=False)
        # Loop weeks and add row.
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=90)
            # Loop days and add days to row.
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day)
                    if len(str(display_day)) == 1:
                        display_day = str(display_day).zfill(2)
                    if day == self.current_day:
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color

                    day_button = ft.Container(content=ft.Text(str(display_day), weight=is_current_day_font, color=self.text_color, size=20, text_align='center'),
                                              on_click=self.selected_date, data=(day,self.current_month, self.current_year),
                                              width=60, height=60, alignment=ft.alignment.center,
                                              border_radius=ft.border_radius.all(50),
                                              bgcolor=is_current_day_bg, on_hover=lambda e: self.hover(e))
                else:
                    day_button = ft.Container(width=60, height=60, border_radius=ft.border_radius.all(10))

                week_row.controls.append(day_button)

            # Add the weeks to the main column.
            calendar_column.controls.append(week_row)
        # Add column to our page container.
        self.calendar_container.content = calendar_column
        return self.calendar_container
