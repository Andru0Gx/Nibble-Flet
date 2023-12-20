'''Body Sections Manager'''

# Libraries
import flet as ft

# Disable the pylint warnings
# pylint: disable=C0415

#* ------------------ Home Page ------------------ *#
def def_home(page: ft.Page):
    """
    Returns an instance of the Home class initialized with the page object.

    Args:
        page (ft.Page): An object of the ft.Page class.

    Returns:
        Home: An instance of the Home class initialized with the page object.
    """
    from Pages.App_Layout.Body_Sections.home import Home
    return Home(page)

#* ------------------ Events Page ------------------ *#
def def_events(page: ft.Page):
    """
    Returns an instance of the `maintwo` class initialized with the `page` object.

    Args:
    - page (ft.Page): An object of the `ft.Page` class.

    Returns:
    - maintwo: An instance of the `maintwo` class initialized with the `page` object.
    """
    from Pages.App_Layout.Body_Sections.events import maintwo
    return maintwo(page)

#* ------------------ Students Page ------------------ *#
def def_students(page: ft.Page, section: str):
    """
    Returns an instance of the Students class initialized with the page and section objects.

    Args:
        page (ft.Page): An object of the ft.Page class.
        section (str): A string representing the section of the students.

    Returns:
        Students: An instance of the Students class initialized with the page and section objects.
    """
    from Pages.App_Layout.Body_Sections.students import Students
    return Students(page, section)

#* ------------------ Teachers Page ------------------ *#
def def_teachers(page: ft.Page, section: str):
    """
    Returns an instance of the Teachers class initialized with the page and section objects.

    Args:
        page (ft.Page): An object of the ft.Page class.
        section (str): A string representing the section of the teachers.

    Returns:
        Teachers: An instance of the Teachers class initialized with the page and section objects.
    """
    from Pages.App_Layout.Body_Sections.teachers import Teachers
    return Teachers(page, section)

#* ------------------ Settings Page ------------------ *#
def def_settings(page: ft.Page):
    """
    Returns an instance of the Settings class initialized with the page object.

    Args:
        page (ft.Page): An object of the ft.Page class representing the current page.

    Returns:
        settings: An instance of the Settings class initialized with the page object.
    """
    from Pages.App_Layout.Body_Sections.settings import Settings
    return Settings(page)

#* ------------------ Grades Page ------------------ *#
def def_grades(page: ft.Page):
    """
    Returns an instance of the Grades class initialized with the page object.

    Args:
    - page (ft.Page): An object of the ft.Page class representing the current page.

    Returns:
    - grades: An instance of the Grades class initialized with the page object.
    """
    from Pages.App_Layout.Body_Sections.grades import Grades
    return Grades(page)

#* ------------------ Schedule Page ------------------ *#
def def_schedule(page: ft.Page, section: str):
    """
    Returns an instance of the Schedule class initialized with the page and section objects.

    Args:
        page (ft.Page): An object of the ft.Page class representing the current page.
        section (str): A string representing the section of the schedule.

    Returns:
        schedule: An instance of the Schedule class initialized with the page and section objects.
    """
    from Pages.App_Layout.Body_Sections.schedule import Schedule
    return Schedule(page, section)

#* ------------------ Phase Page ------------------ *#
def def_phase(page: ft.Page):
    """
    Returns an instance of the Phases class initialized with the page object.

    Args:
        page (ft.Page): An object of the ft.Page class representing the current page.

    Returns:
        Phases: An instance of the Phases class initialized with the page object.
    """
    from Pages.App_Layout.Body_Sections.phase import Phases
    return Phases(page)
