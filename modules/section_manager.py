'''Body Sections Manager'''

# Libraries
import flet as ft

def def_home(page: ft.Page):
    '''Create the home page'''
    from Pages.App_Layout.Body_Sections.home import Home
    return Home(page)

def def_events(page: ft.Page):
    '''Create the events page'''
    from Pages.App_Layout.Body_Sections.events import maintwo
    return maintwo(page)
