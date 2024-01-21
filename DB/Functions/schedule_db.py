'''Nibble DB - Schedule Functions'''

# Libraries
import sqlite3
import datetime

# Tables Structure
# id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
# profesor_id TEXT NOT NULL,
# materia_id INTEGER NOT NULL,
# bloque_hora TEXT NOT NULL,
# fecha TEXT NOT NULL,
# periodo TEXT NOT NULL,
# CONSTRAINT fk_prof__id_schedule FOREIGN KEY(profesor_id) REFERENCES profesor(id_p) ON DELETE CASCADE ON UPDATE CASCADE,
# CONSTRAINT fk_mat__id_schedule FOREIGN KEY(materia_id) REFERENCES materia(id_m) ON DELETE CASCADE ON UPDATE CASCADE

#* ------------------ SEARCH AVAILABLE SCHEDULE ------------------ *#
def verify_search(profesor_id, bloque_hora, phase, bloque_dia):
    '''Verify if the schedule is available'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    date = datetime.datetime.now().strftime('%B %Y')
    phase = phase.split(' ')[1]
    if phase == 'Año':
        phase = 'Liceo'
    elif phase == 'Grado':
        phase = 'Colegio'

    cursor.execute(
        """SELECT * FROM horario WHERE profesor_id = ? AND bloque_hora = ? AND fecha = ? AND formato = ? AND bloque_dia = ?;""", (profesor_id, bloque_hora, date, phase, bloque_dia))
    search = cursor.fetchone()

    conexion.close()

    if search:
        return False
    else:
        return True

def verify_search_edit(profesor_id, bloque_hora, phase, bloque_dia, schedule_id):
    '''Verify if the schedule is available'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    date = datetime.datetime.now().strftime('%B %Y')
    phase = phase.split(' ')[1]
    if phase == 'Año':
        phase = 'Liceo'
    elif phase == 'Grado':
        phase = 'Colegio'

    cursor.execute(
        """SELECT * FROM horario WHERE profesor_id = ? AND bloque_hora = ? AND fecha = ? AND formato = ? AND bloque_dia = ? AND id_horario != ?;""", (profesor_id, bloque_hora, date, phase, bloque_dia, schedule_id))
    search = cursor.fetchone()

    conexion.close()

    if search:
        return False
    else:
        return True


#* ------------------ ADD ------------------ *#
def schedule_add(profesor_id, materia_id, bloque_hora, phase, bloque_dia, guide_teacher, codigo_horario):
    '''Add a new schedule to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    date = datetime.datetime.now().strftime('%B %Y')

    phase_format = phase.split(' ')[1]
    if phase_format == 'Año':
        phase_format = 'Liceo'
    elif phase_format == 'Grado':
        phase_format = 'Colegio'


    cursor.execute(
        """INSERT INTO horario (
            id_horario,
            profesor_id,
            materia_id,
            bloque_hora,
            bloque_dia,
            fecha,
            etapa,
            formato,
            guide_teacher
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", (codigo_horario, profesor_id, materia_id, bloque_hora, bloque_dia, date, phase, phase_format, guide_teacher))
    conexion.commit()

    conexion.close()


#* ------------------ SEARCH ------------------ *#
def schedule_id_search(schedule_id, bloque_hora = None):
    '''Search a schedule by ID'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    if bloque_hora is None:
        cursor.execute(
            """SELECT * FROM horario WHERE id_horario = ?;""", (schedule_id,))
        schedule = cursor.fetchall()
    else:
        cursor.execute(
            """SELECT * FROM horario WHERE id_horario = ? AND bloque_hora = ?;""", (schedule_id, bloque_hora))
        schedule = cursor.fetchall()

    schedule_format = {
        'ID': None,
        'ID Horario': None,
        'Profesor ID': None,
        'Materia ID': None,
        'Bloque Hora': None,
        'Bloque Dia': None,
        'Fecha': None,
        'Etapa': None,
        'Formato': None,
        'Guide Teacher': None
    }

    schedule_list = []

    if schedule:
        for schedule in schedule:
            schedule_format['ID'], schedule_format['ID Horario'], schedule_format['Profesor ID'], schedule_format['Materia ID'], schedule_format['Bloque Hora'], schedule_format['Bloque Dia'], schedule_format['Fecha'], schedule_format['Etapa'], schedule_format['Formato'], schedule_format['Guide Teacher'] = schedule
            schedule_list.append(schedule_format.copy())
    else:
        return False

    conexion.close()

    return schedule_list



#* ------------------ Edit ------------------ *#
def schedule_edit(schedule_id, bloque_hora, profesor_id, materia_id, guide_teacher, id):
    '''Edit a schedule from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE horario SET profesor_id = ?, materia_id = ?, bloque_hora = ?, guide_teacher = ? WHERE id_horario = ? and id = ?;""", (profesor_id, materia_id, bloque_hora, guide_teacher, schedule_id, id))
    conexion.commit()

    conexion.close()

#* ------------------ Delete ------------------ *#
def schedule_delete(schedule_id):
    '''Delete a schedule from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM horario WHERE id_horario = ?;""", (schedule_id,))
    conexion.commit()

    conexion.close()


#^ ------------------ GET ------------------ ^#
#* 1 - Get the first X schedules (don't repeat the Schedule ID)
def get_schedules(start_index, end_index):
    '''Get the first X schedules from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(f"""SELECT DISTINCT id_horario FROM horario LIMIT {start_index - 1}, {end_index - start_index + 1};""")
    schedules_id = cursor.fetchall()

    schedule_info = {
        'ID Horario': None,
        'Fecha': None,
        'Etapa': None,
        'Guide Teacher': None
    }

    schedules_list = []

    for info in schedules_id:
        cursor.execute("""SELECT id_horario, fecha, etapa, guide_teacher FROM horario WHERE id_horario = ?;""", (info[0],))
        schedule = cursor.fetchone()
        schedule_info['ID Horario'], schedule_info['Fecha'], schedule_info['Etapa'], schedule_info['Guide Teacher'] = schedule
        schedules_list.append(schedule_info.copy())

    conexion.close()

    return schedules_list

#* 2 - Check Amount of Schedules
def check_amount():
    '''Check the amount of schedule in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute("""SELECT COUNT(DISTINCT id_horario) FROM horario;""")
    amount = cursor.fetchone()[0]

    conexion.close()
    return amount

#^ ------------------ FILTER ------------------ ^#
#* 1 - Filter Schedules (ID HORARIO, DATE, PHASE, GUIDE TEACHER)
def filter_schedules(filter):
    '''Filter schedules in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # Get the schedules
    cursor.execute(f"""SELECT DISTINCT id_horario FROM horario WHERE id_horario LIKE '%{filter}%' OR fecha LIKE '%{filter}%' OR etapa LIKE '%{filter}%' OR guide_teacher LIKE '%{filter}%';""")
    schedules_id = cursor.fetchall()

    schedule_info = {
        'ID Horario': None,
        'Fecha': None,
        'Etapa': None,
        'Guide Teacher': None
    }

    schedules_list = []

    for info in schedules_id:
        cursor.execute("""SELECT id_horario, fecha, etapa, guide_teacher FROM horario WHERE id_horario = ?;""", (info[0],))
        schedule = cursor.fetchone()
        schedule_info['ID Horario'], schedule_info['Fecha'], schedule_info['Etapa'], schedule_info['Guide Teacher'] = schedule
        schedules_list.append(schedule_info.copy())

    conexion.close()

    return schedules_list