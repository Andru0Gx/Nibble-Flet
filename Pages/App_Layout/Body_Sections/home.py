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
        events = ft.TextButton(text='Eventos', width=100, height=30, style=ft.ButtonStyle(bgcolor='#4B4669', color='#FFFFFF'), on_click= lambda e: self.events(), top=55, left=500)

        # Create the layout
        layout = ft.Row(controls=[
            ft.Column(controls=[
                ft.Stack(controls=[
                FletCalendar(self.page),
                events

                ]),
                ft.Container(height=100, width=1100, bgcolor='red', border_radius=20, padding=ft.padding.all(20), content=ft.Text('EVENTOS', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center')),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment='center')
        ], alignment=ft.MainAxisAlignment.CENTER)



        self.content = layout
        self.update()

    def build(self):
        return self.content
