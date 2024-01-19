'''Nibble Export DB Module'''

# Libraries
import os
import sqlite3
import csv
from tkinter import Tk, filedialog
from datetime import datetime

#* ------------------ Export DB ------------------ *#
def export_data(path, table_name):
    """
    Export data from a specified SQLite table to a CSV file.

    Parameters:
    - path (str): The path to the directory where the CSV file will be saved.
    - table_name (str): The name of the SQLite table to export.

    Returns:
    None

    This function connects to the 'DB/Nibble.db' SQLite database, executes a query to
    retrieve all data from the specified table, disconnects from the database, and then
    exports the data to a CSV file in the provided directory.

    If the table_name is equal to 'sqlite_sequence', the function prints a message and
    does not attempt to export the table.

    Example:
    export_data('/path/to/export', 'my_table')
    """
    try:
        # Connect to the database
        conexion = sqlite3.connect('DB/Nibble.db')
        cursor = conexion.cursor()

        # Execute a query to get data from the specified table
        cursor.execute(f'SELECT * FROM {table_name}')
        datos = cursor.fetchall()

        # Disconnect the database
        conexion.close()

        # Export the data to a CSV file in the selected location
        ruta_archivo = os.path.join(path, f'{table_name}.csv')
        with open(ruta_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            # Escribir el encabezado
            encabezado = [descripcion[0] for descripcion in cursor.description]
            escritor_csv.writerow(encabezado)

            # Escribir los datos
            escritor_csv.writerows(datos)
    except:
        pass

def path_selector_export():
    """
    Prompt the user to select a folder for exporting database tables.

    This function opens a window to allow the user to choose a directory for exporting database tables.
    It creates a backup folder with the current date and iterates through the tables in the database,
    exporting each table to a CSV file in the backup folder.

    Parameters:
    None

    Returns:
    None
    """
    try:
        # Create a window to select the folder
        path_window = Tk()
        path_window.withdraw()  # Hide the window

        # show the window infront of all other windows
        path_window.attributes('-topmost', True)

        # Get the path to save the backup
        initial_path = filedialog.askdirectory(title="Seleccionar carpeta para guardar", initialdir='C:/')

        if initial_path == '':
            path_window.destroy()
            return

        #* Create the backup folder with the current date *#
        actual_date = datetime.now().strftime('%Y-%m-%d')
        backup_folder = f'Respaldo ({actual_date})'

        # Check if the folder already exists and add an incremental number if necessary
        aditional_number = 1
        while os.path.exists(os.path.join(initial_path, backup_folder)):
            backup_folder = f'Respaldo ({actual_date} - {aditional_number})'
            aditional_number += 1

        # Create the backup folder
        path = os.path.join(initial_path, backup_folder)
        os.makedirs(path)

        # Get the list of tables in the database
        conexion = sqlite3.connect('DB/Nibble.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conexion.close()

        # Export each table in the backup folder
        for table in tables:
            export_data(path, table[0])

        # Cerrar la ventana de la interfaz gráfica
        path_window.destroy()

    except Exception as e:
        print(e)



#* ------------------ Import DB ------------------ *#
def import_data(path, table_name):
    """
    Import data from a CSV file into an SQLite table.

    Parameters:
    - path (str): The path to the CSV file.
    - table_name (str): The name of the SQLite table.

    Returns:
    None
    """
    try:
        # Check if the table name is 'sqlite_sequence' (this table is used internally by SQLite)
        if table_name == 'sqlite_sequence':
            return
        # Read the data from the CSV file and get the header
        with open(path) as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            encabezado = next(lector_csv)

        # Connect to the database
        conexion = sqlite3.connect('DB/Nibble.db')
        cursor = conexion.cursor()

        # Create the table if it doesn't exist
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {", ".join([f"{columna} TEXT" for columna in encabezado])})')

        # Delete existing data in the table
        cursor.execute(f'DELETE FROM {table_name}')

        # Read the data from the CSV file (again) to skip the header row
        with open(path, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv)  # Skip the header row

            # Insert the data into the table
            for fila in lector_csv:
                cursor.execute(f'INSERT INTO {table_name} ({", ".join(encabezado)}) VALUES ({", ".join("?" * len(encabezado))})', fila)

        # Confirm the changes and close the connection
        conexion.commit()
        conexion.close()
    except:
        pass


def path_selector_import():
    """
    Allow the user to select a folder with CSV files and import them into the database.

    Parameters:
    None

    Returns:
    None
    """
    try:
        # Create a window to select the folder
        path_window = Tk()
        path_window.withdraw()

        # show the window infront of all other windows
        path_window.attributes('-topmost', True)

        # Ask the user to select the folder with the CSV files
        ruta_carpeta = filedialog.askdirectory(title="Seleccionar carpeta con archivos CSV", initialdir='C:/')

        if ruta_carpeta == '':
            path_window.destroy()
            return

        # Get the list of CSV files in the folder
        archivos_csv = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.csv')]

        # Import each CSV file to the database
        for archivo_csv in archivos_csv:
            table_name = os.path.splitext(archivo_csv)[0]  # Use the name of the CSV file as the name of the table
            path = os.path.join(ruta_carpeta, archivo_csv)
            import_data(path, table_name)

        # Close the window
        path_window.destroy()
    except:
        pass
