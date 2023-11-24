'''App Layout'''

# Libraries
import time
import flet as ft

# Pages
from modules.page_manager import def_login as Login

# Body Sections
from modules.section_manager import def_home as Home


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
                ft.PopupMenuItem(icon=ft.icons.IMPORT_EXPORT_OUTLINED, text='Importar/Exportar Base de Datos'),
                ft.PopupMenuItem(icon= ft.icons.SETTINGS_OUTLINED,text='Configuracion', on_click= lambda e:self.change_page(5)),
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
            icon_content=ft.Icon(ft.icons.BOOK, color='#4B4669', size=30),
            selected_icon_content=ft.Icon(ft.icons.BOOK, size=40),
            label_content=ft.Text('Calificaciones', color='#4B4669'),
        )

        sidebar = ft.NavigationRail(
            selected_index=0,
            destinations=[home, students, teachers, schedules, grades],
            bgcolor='#e9ebf6',
            min_width=100,
            width=200,
            label_type=ft.NavigationRailLabelType.SELECTED,
            extended=True,
            on_change= lambda e: self.change_page(e.control.selected_index),
        )

        #* ------------------ Body ------------------ *#
        self.body = ft.Container(expand=True, bgcolor='#F2F4FA', border=ft.Border(top=ft.BorderSide(color='#c2c9db', width=2), left=ft.BorderSide(color='#c2c9db', width=1)), padding=ft.padding.only(0,25,0,0))

        #* ------------------ Layout ------------------ *#
        # header
        layout = ft.Row(controls=[
            sidebar,
            self.body,
        ],expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START)

        # Add the layout to the page
        self.page.add(header, layout)

        # Change the page
        self.change_page(0)

    #* ------------------ Class Functions ------------------ *#
    def animate(self):
        '''Animate the layout'''
        time.sleep(0.1)
        self.body.opacity = 0 if self.body.opacity == 1 else 1
        self.body.update()

    def change_page(self, e): #TODO - ADD THE MODULE TO CHANGE THE PAGE (CLASS)
        '''Change the page'''
        self.animate()

        if e == 0:
            self.body.content = Home(self.page)
        elif e == 1:
            self.body.content = ft.Container(content=ft.Text('Students', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 2:
            self.body.content = ft.Container(content=ft.Text('Teachers', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 3:
            self.body.content = ft.Container(content=ft.Text('Schedules', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 4:
            self.body.content = ft.Container(content=ft.Text('Grades', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')
        elif e == 5:
            self.body.content = ft.Container(content=ft.Text('Settings', size=40, color='#4B4669', font_family='Arial',weight='bold', text_align='center'), expand=True, bgcolor='#F2F4FA')

        self.animate()

    def logout(self):
        '''Logout from the system'''
        self.page.remove(self.page.controls[0], self.page.controls[1])
        Login(self.page)
