'''Nibble DB - Grades Functions'''

# Libraries
import sqlite3
import datetime
import locale

# Database
from DB.Functions.subjects_db import filter_subjects

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

# Tables Structure
# Calificaciones
# id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
# estudiante_id TEXT NOT NULL,
# materia_id INTEGER NOT NULL,
# momento_1 DECIMAL(4,2),
# momento_2 DECIMAL(4,2),
# momento_3 DECIMAL(4,2),
# nota_final DECIMAL(4,2),
# periodo TEXT NOT NULL,
# CONSTRAINT fk_est_id_grade FOREIGN KEY(estudiante_id) REFERENCES estudiante(id_s) ON DELETE CASCADE ON UPDATE CASCADE,
# CONSTRAINT fk_mat_id_grade FOREIGN KEY(materia_id) REFERENCES materia(id_m) ON DELETE CASCADE ON UPDATE CASCADE


#* ------------------ ADD GRADE ------------------ *#
def grade_add(student_ci, subject_id, grade1 = None, grade2= None, grade3= None, final_grade= None, new_period = False):
    '''Add a new grade to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    student_phase_id = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_ci,)).fetchone()[0]

    phase_name = cursor.execute(
        """SELECT grado_anio, seccion FROM etapa WHERE id_e = ?;""", (student_phase_id,)).fetchone()
    phase_name = str(phase_name[0] + ' ' + phase_name[1])

    period = datetime.datetime.now().strftime('%d %B %Y')
    period = str(period + ' - ' + phase_name)

    if new_period:
        cursor.execute(
            """INSERT INTO calificaciones (
                estudiante_id,
                materia_id,
                momento_1,
                momento_2,
                momento_3,
                nota_final,
                periodo
            ) VALUES (?, ?, ?, ?, ?, ?, ?);""", (student_ci, subject_id, grade1, grade2, grade3, final_grade, period))
    else:
        # # search if the grade already exists if TRUE update the grade
        if cursor.execute(
            """SELECT estudiante_id, materia_id, periodo FROM calificaciones WHERE estudiante_id = ? AND materia_id = ?;""", (student_ci, subject_id)).fetchone() is not None:
            cursor.execute(
                """UPDATE calificaciones SET momento_1 = ?, momento_2 = ?, momento_3 = ?, nota_final = ? WHERE estudiante_id = ? AND materia_id = ?;""", (grade1, grade2, grade3, final_grade, student_ci, subject_id))
        else:
            cursor.execute(
                """INSERT INTO calificaciones (
                    estudiante_id,
                    materia_id,
                    momento_1,
                    momento_2,
                    momento_3,
                    nota_final,
                    periodo
                ) VALUES (?, ?, ?, ?, ?, ?, ?);""", (student_ci, subject_id, grade1, grade2, grade3, final_grade, period))
    conexion.commit()
    conexion.close()

#* ------------------ APPROVE STUDENT ------------------ *#
def approve_student(student_id,new_status, new_phase=None):
    '''Approve a student'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    student_info = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()

    phase_type = cursor.execute(
        """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (student_info[0],)).fetchone()[0]

    if phase_type.split(' ')[1] == 'Año':
        phase_type = 'Liceo'
    elif phase_type.split(' ')[1] == 'Grado':
        phase_type = 'Colegio'

    if new_status != 'Graduado':
        cursor.execute(
            """UPDATE estudiante SET etapa_id = ?, status = ? WHERE id_s = ?;""", (new_phase, new_status, student_id))
        conexion.commit()

        phase_data = cursor.execute(
            """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (new_phase,)).fetchone()[0]

        subjects_list = filter_subjects(phase_data, phase_type)
        for i in subjects_list:
            grade_add(student_id, i['ID'], new_period=True)

    else:
        cursor.execute(
            """UPDATE estudiante SET status = ? WHERE id_s = ?;""", (new_status, student_id))
        conexion.commit()
        conexion.close()

#* ------------------ DISAPPROVE STUDENT ------------------ *#
def disapprove_student(student_id, new_status):
    '''Disapprove a student'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()


    student_info = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()

    phase_type = cursor.execute(
        """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (student_info[0],)).fetchone()[0]

    if phase_type.split(' ')[1] == 'Año':
        phase_type = 'Liceo'
    elif phase_type.split(' ')[1] == 'Grado':
        phase_type = 'Colegio'

    cursor.execute(
        """UPDATE estudiante SET status = ? WHERE id_s = ?;""", (new_status, student_id))
    conexion.commit()

    phase_data = cursor.execute(
        """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (student_info[0],)).fetchone()[0]

    subjects_list = filter_subjects(phase_data, phase_type)
    for i in subjects_list:
        grade_add(student_id, i['ID'], new_period=True)

    conexion.close()



#* ------------------ FILTER GRADES BY PERIOD ------------------ *#
def filter_grades_by_period(period, student_id):
    '''Filter the grades by period'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_nota, estudiante_id, materia_id, momento_1, momento_2, momento_3, nota_final, periodo FROM calificaciones WHERE periodo = ? AND estudiante_id = ?;""", (period, student_id))
    search = cursor.fetchall()
    conexion.close()

    grade = {
        'ID': None,
        'Estudiante': None,
        'Materia': None,
        'Momento 1': None,
        'Momento 2': None,
        'Momento 3': None,
        'Nota Final': None,
        'Periodo': None
    }

    grades_list = []

    for i in search:
        grade['ID'] = i[0]
        grade['Estudiante'] = i[1]
        grade['Materia'] = i[2]
        grade['Momento 1'] = i[3]
        grade['Momento 2'] = i[4]
        grade['Momento 3'] = i[5]
        grade['Nota Final'] = i[6]
        grade['Periodo'] = i[7]
        grades_list.append(grade.copy())

    return grades_list

#* ------------------ GET ALL THE PERIODS OF AN ESTUDENT ------------------ *#
def get_periods(student_id):
    '''Get all the periods of an student'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT DISTINCT periodo FROM calificaciones WHERE estudiante_id = ?;""", (student_id,))
    search = cursor.fetchall()
    conexion.close()

    periods = []

    for i in search:
        periods.append(i[0])

    return periods

#* ------------------ FILTER GRADES BY STUDENT ------------------ *#
def filter_grades_by_student(student_id):
    '''Filter the grades by student'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT id_nota, estudiante_id, materia_id, momento_1, momento_2, momento_3, nota_final, periodo FROM calificaciones WHERE estudiante_id = ?;""", (student_id,))
    search = cursor.fetchall()
    conexion.close()

    grade = {
        'ID': None,
        'Estudiante': None,
        'Materia': None,
        'Momento 1': None,
        'Momento 2': None,
        'Momento 3': None,
        'Nota Final': None,
        'Periodo': None
    }

    grades_list = []

    for i in search:
        grade['ID'] = i[0]
        grade['Estudiante'] = i[1]
        grade['Materia'] = i[2]
        grade['Momento 1'] = i[3]
        grade['Momento 2'] = i[4]
        grade['Momento 3'] = i[5]
        grade['Nota Final'] = i[6]
        grade['Periodo'] = i[7]
        grades_list.append(grade.copy())

    return grades_list
