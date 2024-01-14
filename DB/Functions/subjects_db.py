'''Nibble DB - Subjects Functions'''

# Libraries
import sqlite3

#* ------------------ ADD SUBJECT ------------------ *#
def subject_add(subject_name, phase):
    '''Add a new subject to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # search if the subject already exists
    if cursor.execute(
        """SELECT nombre FROM materia WHERE nombre = ? AND etapa = ?;""", (subject_name, phase)).fetchone() is not None:
        pass
    else:
        cursor.execute(
            """INSERT INTO materia (
                nombre,
                etapa
            ) VALUES (?, ?);""", (subject_name, phase))
        conexion.commit()

    conexion.close()


#* ------------------ GET SUBJECTS ------------------ *#
def get_subjects():
    '''Get all the subjects from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia;""")
    search = cursor.fetchall()
    conexion.close()

    subject = {
        'ID': None,
        'Nombre': None,
        'Etapa': None
    }

    subjects_list = []

    for i in search:
        subject['ID'] = i[0]
        subject['Nombre'] = i[1]
        subject['Etapa'] = i[2]
        subjects_list.append(subject.copy())

    # Ordenar la lista de materias en orden ascendente
    subjects_list.sort(key=lambda x: x['ID'])

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
def update_subject(subject_id, subject_name, phase):
    '''Update a subject from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE materia SET nombre = ?, etapa = ? WHERE id_m = ?;""", (subject_name, phase,subject_id))
    conexion.commit()
    conexion.close()

#* ------------------ FILTER SUBJECTS BY PHASE ------------------ *#
def filter_subjects(phase, phase_type):
    '''Filter the subjects by phase'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia WHERE etapa = ?;""", (phase,))
    search = cursor.fetchall()

    subject = {
        'ID': None,
        'Nombre': None,
        'Etapa': None
    }

    subjects_list = []

    for i in search:
        subject['ID'] = i[0]
        subject['Nombre'] = i[1]
        subject['Etapa'] = i[2]
        subjects_list.append(subject.copy())

    # filtrar etapas por el nombre type (liceo, colegio)
    cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia WHERE etapa = ?;""", (phase_type,))
    search = cursor.fetchall()
    conexion.close()

    for i in search:
        subject['ID'] = i[0]
        subject['Nombre'] = i[1]
        subject['Etapa'] = i[2]
        subjects_list.append(subject.copy())

    # Ordenar la lista de materias en orden ascendente
    subjects_list.sort(key=lambda x: x['ID'])

    return subjects_list


#* ------------------ SEARCH SUBJECT BY ID ------------------ *#
def search_subject_by_id(subject_id):
    '''Search a subject by id'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia WHERE id_m = ?;""", (subject_id,))
    search = cursor.fetchone()
    conexion.close()

    subject = {
        'ID': None,
        'Nombre': None,
        'Etapa': None
    }

    subject['ID'] = search[0]
    subject['Nombre'] = search[1]
    subject['Etapa'] = search[2]

    return subject
