'''Settings Page'''

# Libraries
import flet as ft

class Settings(ft.UserControl):
    '''
    
    Settings Page

    Sections:
    - User Change
    - Password Change
    - Database Import/Export
    - Database Reset (Delete all the data)
    - Database Storage (Show the storage of the database in a pie chart or something like that)
    
    '''
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        #TODO - Revisar el Layout de la pagina (no se ve bien y no esta bien hecho :C)

        #* ------------------ Layout ------------------ *#
        # Create the Title
        title = ft.Text(
            'Configuracion',
            color='#4B4669',
            font_family='Arial',
            width = 1100,
            text_align='center',
            weight='bold',
            size=25,
        )

        #* ------------------ Credentials - Layout ------------------ *#

        # Create the title for the user section
        user_title = ft.Text(
            'Credenciales',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='left',
            weight='bold',
            size=16,
        )

        self.credentials = ft.Container(ft.Row([

            # Create the TextField for the username
            ft.TextField(
                width=250,
                height=35,
                label='Cambiar Usuario',
                hint_text='Ingresa el nuevo nombre de usuario',
                value='admin', #TODO - get the username from the database and set it as the value
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                disabled=True,
            ),

            # Create the TextField for the password
            ft.TextField(
                width=250,
                height=35,
                label='Cambiar Contraseña',
                hint_text='Ingresa la nueva contraseña',
                value='admin', #TODO - get the password from the database and set it as the value
                bgcolor='#f3f4fa',
                hint_style=ft.TextStyle(color='#C0C1E3'),
                label_style=ft.TextStyle(color='#4B4669'),
                text_style=ft.TextStyle(color='#2c293d', font_family='Arial', size=14),
                border_color='#6D62A1',
                content_padding=ft.padding.only(left=10,top=0,right=10,bottom=0),
                disabled=True,
                password=True,
            ),

            # Create the button to save the username / password
            ft.Container(
                ft.Text('Guardar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.save_credentials(),
                border_radius=15,
                visible=False,
            ),

            # Create the button to cancel the username / password change
            ft.Container(
                ft.Text('Cancelar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=80,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.cancel_credentials(),
                border_radius=15,
                visible=False,
            ),

            # Create the button to edit the username / password change
            ft.Container(
                    ft.Text('Editar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                    width=80,
                    height=35,
                    bgcolor='#6D62A1',
                    alignment=ft.alignment.center,
                    on_click= lambda e: self.edit_credentials(),
                    border_radius=15,
                ),

        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20))

        credentials_layout = ft.Column([
            user_title,
            self.credentials,
        ])

        #* ------------------ Database - Layout ------------------ *#

        # Create the title for the database section
        database_title = ft.Text(
            'Base de Datos',
            color='#4B4669',
            font_family='Arial',
            width = 600,
            text_align='left',
            weight='bold',
            size=16,
        )

        self.buttons = ft.Row([
        # Create the button to import the database
            ft.Container(
                ft.Text('Restaurar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=100,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.import_db(),
                border_radius=15,
            ),

        # Create the button to export the database
            ft.Container(
                ft.Text('Respaldar',size=15, color='#f3f4fa', font_family='Arial', text_align='center'),
                width=100,
                height=35,
                bgcolor='#6D62A1',
                alignment=ft.alignment.center,
                on_click= lambda e: self.export_db(),
                border_radius=15,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=20)


        # Create the Color Legend
        color_legend = ft.Column([
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.BLUE),
                        ft.Text('Calendario', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.YELLOW),
                        ft.Text('Profesores', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.PINK),
                        ft.Text('Estudiantes', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.GREEN),
                        ft.Text('Horarios', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.INDIGO),
                        ft.Text('Notas', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.AMBER),
                        ft.Text('Representantes', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                    ft.Row([
                        ft.Container(width=20, height=20, bgcolor=ft.colors.CYAN),
                        ft.Text('Etapas', color='#4B4669', font_family='Arial', size=14),
                    ], spacing=10),
                ], spacing=10),
                border=ft.border.only(right=ft.BorderSide(color='#6D62A1', width=2)),
                padding=ft.padding.only(right=10, left=50),
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=20)


        # Create a Graph to show the storage of the database
        self.storage_graph = ft.PieChart(
        sections=[
            ft.PieChartSection( # Calendario
                20,
                color=ft.colors.BLUE,
                radius=120,
            ),
            ft.PieChartSection( # Profesores
                20,
                color=ft.colors.YELLOW,
                radius=120,
            ),
            ft.PieChartSection( # Estudiantes
                20,
                color=ft.colors.PINK,
                radius=120,
            ),
            ft.PieChartSection( # Horarios
                20,
                color=ft.colors.GREEN,
                radius=120,
            ),
            ft.PieChartSection( # Notas
                20,
                color=ft.colors.INDIGO,
                radius=120,
            ),
            ft.PieChartSection( # Representantes
                20,
                color=ft.colors.AMBER,
                radius=120,
            ),
            ft.PieChartSection( # Etapas
                20,
                color=ft.colors.CYAN,
                radius=120,
            ),
        ],
        sections_space=1,
        center_space_radius=0,
        width=200,
        height=200,
    )

        database_layout = ft.Column([
            database_title,
            self.buttons,
            ft.Row([
                color_legend,
                ft.VerticalDivider(width=200),
                self.storage_graph,
            ],spacing=20, alignment=ft.MainAxisAlignment.START ),
        ], spacing=20)

        #* ------------------ Layout ------------------ *#
        layout = ft.Column([
            title,
            ft.Divider(),
            credentials_layout,
            ft.Divider(),
            database_layout,
        ])

        layout_container = ft.Row([
            ft.Container(
            layout,
            width=1100,
            height=600,
            border_radius=20,
            padding=ft.padding.all(20),
            border=ft.border.all(2, '#6D62A1')
        )
        ], alignment=ft.MainAxisAlignment.CENTER)

        # add the layout to the page
        self.content = layout_container

    def build(self):
        return self.content

    #* ------------------ Functions ------------------ *#
    def edit_credentials(self):
        '''Function to edit the username and password'''

        # Change the buttons
        self.credentials.content.controls[2].visible = True
        self.credentials.content.controls[3].visible = True
        self.credentials.content.controls[4].visible = False


        # Enable the textfields
        self.credentials.content.controls[0].disabled = False
        self.credentials.content.controls[1].disabled = False

        # Show the password
        self.credentials.content.controls[1].password = False

        self.update()

    def cancel_credentials(self):
        '''Function to cancel the username and password change'''

        # Change the buttons
        self.credentials.content.controls[2].visible = False
        self.credentials.content.controls[3].visible = False
        self.credentials.content.controls[4].visible = True

        # Disable the textfields
        self.credentials.content.controls[0].disabled = True
        self.credentials.content.controls[1].disabled = True

        # Hide the password
        self.credentials.content.controls[1].password = True

        #TODO - Get the username and password from the database and set it as the value

        self.update()

    def save_credentials(self):
        '''Function to save the username and password change'''

        # Change the buttons
        self.credentials.content.controls[2].visible = False
        self.credentials.content.controls[3].visible = False
        self.credentials.content.controls[4].visible = True

        # Disable the textfields
        self.credentials.content.controls[0].disabled = True
        self.credentials.content.controls[1].disabled = True

        # Hide the password
        self.credentials.content.controls[1].password = True

        #TODO - Save the username and password in the database

        self.update()

    def import_db(self):
        '''Function to import the database'''
        pass

    def export_db(self):
        '''Function to export the database'''
        pass

    #TODO - Create a function to get the storage of the database and set it to the graph
