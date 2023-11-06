'''Module to create a back button'''

# libraries
import flet as ft

#* ---------------------------------------------------- Functions

# return to the previous page
def back(page: ft.Page, new_page: ft.Page):
    '''Return to the previous page'''
    page.remove(page.controls[0])
    new_page(page)

def back_container(container: ft.Container, new_page: ft.Page):
    '''Create a container with a back button'''
    button = container

    def hover(e):
        '''Change the color of the button when the mouse is over it'''
        e.control.bgcolor = '#817aa7' if e.data == "true" else '#F2F4FA'
        e.control.update()

    button = ft.Container(
        content=ft.Image('assets/back.png', width=50, height=50, scale=0.5,color='#2c293d'),
        width=35,
        height=35,
        bgcolor='#F2F4FA',
        border_radius=25,
        on_click= lambda e: back(container, new_page), on_hover= hover)

    return button