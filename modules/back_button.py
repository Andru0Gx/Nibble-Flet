'''Module to create a back button'''

# libraries
import flet as ft

#* ---------------------------------------------------- Functions

# return to the previous page
def back(page: ft.Page, new_page: ft.Page, parent = None):
    '''Return to the previous page'''
    if parent != None:
        parent.content = new_page(page, parent)
        parent.update()
    else:
        page.remove(page.controls[0])
        new_page(page)

def back_container(container: ft.Container, new_page: ft.Page, parent = None):
    '''Create a container with a back button'''
    button = container

    def hover(e):
        '''Change the color of the button when the mouse is over it'''
        e.control.bgcolor = '#817aa7' if e.data == "true" else '#F2F4FA'
        e.control.update()

    button = ft.Container(
        content=ft.Icon(ft.icons.ARROW_BACK, color='#4B4669', size=30),
        width=35,
        height=35,
        bgcolor='#F2F4FA',
        border_radius=25,
        on_click= lambda e: back(container, new_page, parent), on_hover= hover)

    return button