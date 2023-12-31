'''Nibble DB - Subjects Functions'''

# Libraries
import sqlite3

#* ------------------ ADD SUBJECT ------------------ *#
def subject_add(subject_name):
    '''Add a new subject to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # search if the subject already exists
    if cursor.execute(
        """SELECT nombre FROM materia WHERE nombre = ?;""", (subject_name,)).fetchone() is not None:
        pass
    else:
        cursor.execute(
            """INSERT INTO materia (
                nombre
            ) VALUES (?);""", (subject_name,))
        conexion.commit()

    conexion.close()


#* ------------------ GET SUBJECTS ------------------ *#
def get_subjects():
    '''Get all the subjects from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_m,nombre FROM materia;""")
    search = cursor.fetchall()
    conexion.close()

    subject = {
        'ID': None,
        'Nombre': None
    }

    subjects_list = []

    for i in search:
        subject['ID'] = i[0]
        subject['Nombre'] = i[1]
        subjects_list.append(subject.copy())

    # Ordenar la lista de materias en orden alfabetico por nombre
    subjects_list.sort(key=lambda x: x['Nombre'])

    return subjects_list

#* ------------------ DELETE SUBJECT ------------------ *#
def delete_subject(subject_id):
    '''Delete a subject from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM materia WHERE id_m = ?;""", (subject_id,))
    conexion.commit()
    conexion.close()

#* ------------------ UPDATE SUBJECT ------------------ *#
def update_subject(subject_id, subject_name):
    '''Update a subject from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE materia SET nombre = ? WHERE id_m = ?;""", (subject_name, subject_id))
    conexion.commit()
    conexion.close()
