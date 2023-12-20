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

#* ------------------ Teachers Page ------------------ *#
def def_teachers(page: ft.Page, section: str):
    '''
    Returns the result of calling the 'maintwo' function from the 'teachers' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.teachers import Teachers
    return Teachers(page, section)

#* ------------------ Settings Page ------------------ *#
def def_settings(page: ft.Page):
    '''
    Returns the result of calling the 'maintwo' function from the 'settings' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.settings import Settings
    return Settings(page)

#* ------------------ Grades Page ------------------ *#
def def_grades(page: ft.Page):
    '''
    Returns the result of calling the 'maintwo' function from the 'grades' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.grades import Grades
    return Grades(page)

#* ------------------ Schedule Page ------------------ *#
def def_schedule(page: ft.Page, section: str):
    '''
    Returns the result of calling the 'maintwo' function from the 'schedule' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.schedule import Schedule
    return Schedule(page, section)

#* ------------------ Phase Page ------------------ *#
def def_phase(page: ft.Page):
    '''
    Returns the result of calling the 'maintwo' function from the 'phase' 
    module in the 'Pages.App_Layout.Body_Sections' package with the given 'page' 
    object as an argument.
    
    Args:
        page (ft.Page): A 'ft.Page' object representing a page.
    
    Returns:
        The result of calling the 'maintwo' function with the 'page' object as an argument.
    '''
    from Pages.App_Layout.Body_Sections.phase import Phases
    return Phases(page)
