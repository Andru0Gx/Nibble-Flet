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
        self.events_container = ft.Container(
            height=75,
            width=500,
            border_radius=20,
            padding=ft.padding.all(20),
            border=ft.border.all(2, '#6D62A1'),
            top=10,
        )

        # Create the layout
        layout = ft.Row([
            ft.Column(controls=[
                    FletCalendar(self.page, self.events_container),
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment='center'),
        ], alignment=ft.MainAxisAlignment.CENTER)

        self.content = layout
        self.update()

    def build(self):
        return self.content
