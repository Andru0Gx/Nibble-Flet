'''Home Sections Layout'''

# Libraries
import flet as ft

# Modules
from modules.cal import FletCalendar


#^ ------------------ HOME ------------------ ^#
class Home(ft.UserControl):
    '''Home Page Layout'''
    def __init__(self, page):
        super().__init__()
        self.page = page

        #* ------------------ Layout ------------------ *#
        text_event = ft.Text(
            'INFORMACION EVENTOS',
            color='#4B4669',
            font_family='Helvetica',
            width = 200,
            text_align='center',
            weight='bold'
        )
        events_title = ft.Container(
            content=text_event,
            bgcolor='#e9ebf6',
            border_radius=50,
            border=ft.border.all(2, '#6D62A1'),
            height=30,
            left= 145
        )
        self.events_container = ft.Container(
            height=125,
            width=500,
            border_radius=20,
            padding=ft.padding.all(20),
            border=ft.border.all(2, '#6D62A1'),
            top=10,
        )

        info_events = ft.Stack([
            self.events_container,
            events_title,
        ], width=500, height=150)

        # Create the layout
        layout = ft.Row([
            ft.Column(controls=[
                    FletCalendar(self.page, self.events_container),
                    info_events,
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center'),
        ], alignment=ft.MainAxisAlignment.CENTER)

        self.content = layout
        self.update()

    def build(self):
        return self.content
