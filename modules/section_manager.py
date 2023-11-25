'''Body Sections Manager'''

# Libraries
import flet as ft

# Disable the pylint warnings
# pylint: disable=C0415

#* ------------------ Home Page ------------------ *#
def def_home(page: ft.Page):
    '''
    Create the home page

    Args:
    - page: An instance of the ft.Page class.

    Returns:
    - An instance of the Home class.
    '''
    from Pages.App_Layout.Body_Sections.home import Home
    return Home(page)

#* ------------------ Events Page ------------------ *#
def def_events(page: ft.Page):
    '''
    Returns the result of calling the 'maintwo' function from the 'events' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.events import maintwo
    return maintwo(page)

#* ------------------ Students Page ------------------ *#
def def_students(page: ft.Page, section: str):
    '''
    Returns the result of calling the 'maintwo' function from the 'students' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.students import Students
    return Students(page, section)
