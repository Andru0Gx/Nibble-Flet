'''App Layout'''

# Libraries
import flet as ft

# Pages
from modules.page_manager import def_login as Login

# Body Sections
from modules.section_manager import def_home as Home
from modules.section_manager import def_students as Students
from modules.section_manager import def_teachers as Teachers
from modules.section_manager import def_settings as Settings
from modules.section_manager import def_grades as Grades
from modules.section_manager import def_schedule as Schedule
from modules.section_manager import def_phase as Phase


class AppLayout:
    ''' AppLayout
    
    Sections:
    - Header
    - Sidebar
    - Body

    Header:
    - Logo
    - Name
    - Button to logout
    
    Sidebar:
    - Button to show the home
    - Button to show the students
    - Button to show the teachers
    - Button to show the subjects
    - Button to show the schedules
    - Button to show the grades
    - Button to show the settings

    Body:
    - Container to show the content
    '''

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.update()

        #* ------------------ Variables ------------------ *#

        #* ------------------ Header ------------------ *#

        # Create the logo
        logo = ft.Container(height=80, width=150, content=ft.Image('assets/Nibble-Logo-2.png'), padding=ft.padding.all(20))

        # Create the name
        name = ft.Text('Unidad Educativa "Salvador Garmendia Grateron"', size=40, color='#4B4669', font_family='Helvetica', text_align='center', italic=True)

        # Create the buru
        burger_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(icon= ft.icons.SETTINGS_OUTLINED,text='Configuracion', on_click= lambda e:self.change_page(6)),
                ft.PopupMenuItem(icon=ft.icons.LOGOUT_OUTLINED, text='Cerrar Sesion', on_click=lambda e: self.logout())
            ],
            content=ft.Container(ft.Icon(ft.icons.MENU, color='#000000'), padding=ft.padding.all(10))
            )

        header = ft.AppBar(
            title=name,
            center_title=True,
            leading=logo,
            leading_width=150,
            actions=[burger_menu],
            bgcolor='#e9ebf6',
            toolbar_height=80,
        )

        #* ------------------ Sidebar ------------------ *#
        # Create the sidebar

        home = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.HOME_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.HOME_ROUNDED, size=40),
            label_content=ft.Text('Inicio', color='#4B4669'),
        )

        students = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.PERSON_OUTLINE, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.PERSON, size=40),
            label_content=ft.Text('Estudiantes', color='#4B4669'),
        )

        teachers = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.PERSON_4_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.PERSON_4, size=40),
            label_content=ft.Text('Profesores', color='#4B4669'),
        )

        schedules = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.SCHEDULE_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.SCHEDULE, size=40),
            label_content=ft.Text('Horarios', color='#4B4669'),
        )

        grades = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.BOOK_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.BOOK, size=40),
            label_content=ft.Text('Calificaciones', color='#4B4669'),
        )

        phases = ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.ROOM_PREFERENCES_OUTLINED, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.ROOM_PREFERENCES, size=40),
            label_content=ft.Text('Etapas', color='#4B4669'),
        )

        sidebar = ft.NavigationRail(
            selected_index=0,
            destinations=[home, students, teachers, schedules, grades, phases],
            bgcolor='#e9ebf6',
            min_width=100,
            width=200,
            label_type=ft.NavigationRailLabelType.SELECTED,
            extended=True,
            on_change= lambda e: self.change_page(e.control.selected_index),
        )

        #* ------------------ Body ------------------ *#
        self.body = ft.Container(width=1150, height=688, bgcolor='#F2F4FA', border=ft.Border(top=ft.BorderSide(color='#c2c9db', width=2), left=ft.BorderSide(color='#c2c9db', width=2)), padding=ft.padding.only(0,25,0,0))

        #* ------------------ Layout ------------------ *#
        # header
        layout = ft.Row(controls=[
            sidebar,
            self.body,
        ],height=820 ,spacing=0, vertical_alignment=ft.CrossAxisAlignment.START)

        # Add the layout to the page
        self.page.add(header, layout)

        # Change the page
        self.change_page(0)

    #* ------------------ Class Functions ------------------ *#
    def change_page(self, e):
        '''Change the page'''

        if e == 0:
            self.body.content = Home(self.page)
        elif e == 1:
            self.body.content = Students(self.page, self.body)
        elif e == 2:
            self.body.content = Teachers(self.page, self.body)
        elif e == 3:
            self.body.content = Schedule(self.page, self.body)
        elif e == 4:
            self.body.content = Grades(self.page)
        elif e == 5:
            self.body.content = Phase(self.page)
        elif e == 6:
            self.body.content = Settings(self.page)

        self.body.update()

    def logout(self):
        '''Logout from the system'''
        self.page.clean()
        Login(self.page)
