'''Nibble Module - PDF Printer'''

# Libraries
import os
from tkinter import Tk, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def create_pdf(data, file_name, student = None):
    """
    Create a PDF with a table using the provided data.

    Parameters:
    - data (list of lists): The data to be included in the table.
    - file_name (str): The name of the PDF file to be generated (without extension).

    Example:
    ```
    data_example = [
        ["ID", "Name", "Age"],
        [1, "John", 25],
        [2, "Alice", 30]
    ]
    
    create_pdf(data_example, "example_table")
    ```
    """
    # Create a PDF (if the file already exists, add a number to the name)
    if os.path.exists(file_name + '.pdf'):
        i = 1
        while os.path.exists(file_name + str(i) + '.pdf'):
            i += 1
        pdf = SimpleDocTemplate(file_name + str(i) + '.pdf', pagesize=letter)
    else:
        pdf = SimpleDocTemplate(file_name + '.pdf', pagesize=letter)

    # Create table
    data_table = Table(data)

    # Add style to table
    table_styles = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.transparent),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

    data_table.setStyle(table_styles)

    if student:
        # Create table
        student_table = Table(student)

        # Add style to table
        student_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.transparent),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.transparent),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
        student_table.setStyle(student_table_style)
        pdf.build([student_table, data_table])
    else:
        # Build PDF
        pdf.build([data_table])


def path_selector(file_name, data, student = None):
    """
    Opens a window to allow the user to select a folder and saves a PDF file with the provided data in that folder.

    Parameters:
    - file_name (str): The name of the PDF file to be generated (without extension).
    - data (list of lists): The data to be included in the PDF.

    Example:
    ```
    data_example = [
        ["ID", "Name", "Age"],
        [1, "John", 25],
        [2, "Alice", 30]
    ]
    path_selector("example_table", data_example)
    ```
    """
    try:
        # Create a window to select the folder
        path_window = Tk()
        path_window.withdraw()

        # show the window infront of all other windows
        path_window.attributes('-topmost', True)

        # Ask the user to select the folder to save the PDF
        ruta_carpeta = filedialog.askdirectory(title="Seleccionar carpeta para guardar el PDF", initialdir='C:/')

        if ruta_carpeta == '':
            path_window.destroy()
            return
        path_window.destroy()
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        if student:
            # create the PDF
            create_pdf(data, os.path.join(ruta_carpeta, file_name), student)
        else:
            # create the PDF
            create_pdf(data, os.path.join(ruta_carpeta, file_name))
    except:
        pass
