'''Nibble DB - Phases's functions'''

# Libraries
import sqlite3

#* ------------------ ADD PHASE ------------------ *#
def phase_add(phase_name, phase_section):
    '''Add a new phase to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # search if the phase already exists
    if cursor.execute(
        """SELECT grado_anio, seccion FROM etapa WHERE grado_anio = ? AND seccion = ?;""", (phase_name, phase_section)).fetchone() is not None:
        pass
    else:
        cursor.execute(
            """INSERT INTO etapa (
                grado_anio,
                seccion
            ) VALUES (?, ?);""", (phase_name, phase_section))
        conexion.commit()

    conexion.close()


#* ------------------ GET PHASES ------------------ *#
def get_phases():
    '''Get all the phases from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_e,grado_anio, seccion FROM etapa;""")
    search = cursor.fetchall()
    conexion.close()

    phase = {
        'ID': None,
        'Grado/Año': None,
        'Seccion': None
    }

    phases_list = []

    for i in search:
        phase['ID'] = i[0]
        phase['Grado/Año'] = i[1]
        phase['Seccion'] = i[2]
        phases_list.append(phase.copy())

    # Ordenar la lista de fases en orden alfabetico por seccion
    phases_list.sort(key=lambda x: x['Seccion'])

    return phases_list

#* ------------------ DELETE PHASES ------------------ *#
def delete_phase(phase_id):
    '''Delete a phase from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM etapa WHERE id_e = ?;""", (phase_id,))
    conexion.commit()
    conexion.close()

#* ------------------ UPDATE PHASES ------------------ *#
def update_phase(phase_id, phase_name, phase_section):
    '''Update a phase from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE etapa SET grado_anio = ?, seccion = ? WHERE id_e = ?;""", (phase_name, phase_section, phase_id))
    conexion.commit()
    conexion.close()

#* ------------------ SEARCH PHASES ------------------ *#
def search_phase(phase_name = None, phase_section = None, id = False):
    '''Search a phase from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    if id:
        cursor.execute(
            """SELECT id_e, grado_anio, seccion FROM etapa WHERE id_e = ?;""", (id,))
    else:
        cursor.execute(
            """SELECT id_e, grado_anio, seccion FROM etapa WHERE grado_anio = ? AND seccion = ?;""", (phase_name, phase_section))

    search = cursor.fetchone()
    conexion.close()

    phase = {
        'ID': None,
        'Grado/Año': None,
        'Seccion': None
    }

    if search is not None:
        phase['ID'] = search[0]
        phase['Grado/Año'] = search[1]
        phase['Seccion'] = search[2]

    return phase
