'''Nibble DB - Grades Functions'''

# Libraries
import sqlite3
import datetime
import locale


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
def grade_add(student_id, subject_id, grade1 = None, grade2= None, grade3= None, final_grade= None, new_period = False, disapprove=False, actual_period = None):
    '''Add a new grade to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    period = None

    student_phase_id = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()[0]

    phase_name = cursor.execute(
        """SELECT grado_anio, seccion FROM etapa WHERE id_e = ?;""", (student_phase_id,)).fetchone()
    phase_name = str(phase_name[0] + ' ' + phase_name[1])

    if disapprove:
        period = datetime.datetime.now() + datetime.timedelta(days=1)
        period = period.strftime('%d %B %Y')
        period = str(period + ' - ' + phase_name)
    else:
        period = datetime.datetime.now().strftime('%d %B %Y')
        period = str(period + ' - ' + phase_name)

    if new_period:
        cursor.execute(
            """INSERT INTO calificaciones (
                estudiante_id,
                materia_id,
                etapa_id,
                momento_1,
                momento_2,
                momento_3,
                nota_final,
                periodo,
                estado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", (student_id, subject_id, student_phase_id,grade1, grade2, grade3, final_grade, period, 'En curso'))
    else:
        # # search if the grade already exists if TRUE update the grade
        if cursor.execute(
            """SELECT estudiante_id, materia_id, periodo FROM calificaciones WHERE estudiante_id = ? AND materia_id = ? AND periodo = ?;""", (student_id, subject_id, actual_period)).fetchone() is not None:
            cursor.execute(
                """UPDATE calificaciones SET momento_1 = ?, momento_2 = ?, momento_3 = ?, nota_final = ? WHERE estudiante_id = ? AND materia_id = ? AND periodo = ?;""", (grade1, grade2, grade3, final_grade, student_id, subject_id, actual_period))
        else:
            cursor.execute(
                """INSERT INTO calificaciones (
                    estudiante_id,
                    materia_id,
                    etapa_id,
                    momento_1,
                    momento_2,
                    momento_3,
                    nota_final,
                    periodo,
                    estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", (student_id, subject_id, student_phase_id,grade1, grade2, grade3, final_grade, period, 'En curso'))
    conexion.commit()
    conexion.close()

#* ------------------ APPROVE STUDENT ------------------ *#
def approve_student(student_id, actual_phase):
    '''Promote a student'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # Buscar la fase actual del estudiante y modificar el campo estado a 'Aprovado' En la tabla calificaciones
    cursor.execute(
        """UPDATE calificaciones SET estado = 'Aprobado' WHERE estudiante_id = ? AND periodo = ?;""", (student_id, actual_phase))

    conexion.commit()
    conexion.close()

#* ------------------ DISAPPROVE STUDENT ------------------ *#
def disapprove_student(student_id, actual_phase):
    '''Disapprove a student'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # Buscar la fase actual del estudiante y modificar el campo estado a 'Reprobado' En la tabla calificaciones
    cursor.execute(
        """UPDATE calificaciones SET estado = 'Reprobado' WHERE estudiante_id = ? AND periodo = ?;""", (student_id, actual_phase))
    conexion.commit()
    conexion.close()


#* ------------------ PROMOTE / UNPROMOTE STUDENT ------------------ *#
def verify_promote_student(actual_phase, new_phase = None, graduate = False):
    '''Promote a student
    
    Search all the students (Table - Estudiantes) in the actual phase with the status 'Activo'

    Conditions:
    - If 1 student (Table Calificaciones) has the status 'En curso' then return the student ID
    - If graduate is True then change the status of the student to 'Graduado'
    - If 1 student (Table Calificaciones) has the status 'Reprobado' the dissaprove the student
    - If 1 student (Table Calificaciones) has the status 'Aprobado' then promote the student

    '''

    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    student_info = { # student info
        'ID': None,
        'CI': None,
        'name': None,
        'lastname': None,
    }

    students_list = []

    # Get all the students in the actual phase
    search = cursor.execute(
        """SELECT id_s,cedula,nombres,apellidos FROM estudiante WHERE etapa_id = ? AND status = 'Activo';""", (actual_phase['ID'],)).fetchall()

    for i in search:
        student_info['ID'] = i[0]
        student_info['CI'] = i[1]
        student_info['name'] = i[2]
        student_info['lastname'] = i[3]
        students_list.append(student_info.copy())

    if not students_list:
        return False
    else:
        try:
            for i in students_list:
                # 1st condition
                if cursor.execute(
                    """SELECT estado FROM calificaciones WHERE estudiante_id = ? AND etapa_id = ?;""", (i['ID'], actual_phase['ID'])).fetchone()[0] == 'En curso':
                    return i

            # 2th condition
            if graduate:
                for i in students_list:
                    # 3nd condition
                    if cursor.execute(
                        """SELECT estado FROM calificaciones WHERE estudiante_id = ? AND etapa_id = ?;""", (i['ID'], actual_phase['ID'])).fetchone()[0] == 'Reprobado':
                        unpromote_student(conexion, i['ID'])
                    # 4rd condition
                    elif cursor.execute(
                        """SELECT estado FROM calificaciones WHERE estudiante_id = ? AND etapa_id = ?;""", (i['ID'], actual_phase['ID'])).fetchone()[0] == 'Aprobado':
                        promote_student(conexion,i['ID'], 'Graduado')

            else:
                for i in students_list:
                    # 3nd condition
                    if cursor.execute(
                        """SELECT estado FROM calificaciones WHERE estudiante_id = ? AND etapa_id = ?;""", (i['ID'], actual_phase['ID'])).fetchone()[0] == 'Reprobado':
                        unpromote_student(conexion, i['ID'])

                    # 4rd condition
                    elif cursor.execute(
                        """SELECT estado FROM calificaciones WHERE estudiante_id = ? AND etapa_id = ?;""", (i['ID'], actual_phase['ID'])).fetchone()[0] == 'Aprobado':
                        promote_student(conexion,i['ID'], 'Aprobado', new_phase)

            conexion.commit()
            conexion.close()
            return True
        except:
            pass

#* ------------------ PROMOTE STUDENT ------------------ *#

def promote_student(conexion, student_id,new_status, new_phase=None):
    '''Approve a student'''
    # Connect to the database
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
            """UPDATE estudiante SET etapa_id = ? WHERE id_s = ?;""", (new_phase['ID'], student_id))
        conexion.commit()

        cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia WHERE etapa = ?;""", (new_phase['Grado/Año'],))
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

        for i in search:
            subject['ID'] = i[0]
            subject['Nombre'] = i[1]
            subject['Etapa'] = i[2]
            subjects_list.append(subject.copy())

        # Ordenar la lista de materias en orden ascendente
        subjects_list.sort(key=lambda x: x['ID'])

        for i in subjects_list:

            student_phase_id = cursor.execute(
            """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()[0]

            phase_name = cursor.execute(
            """SELECT grado_anio, seccion FROM etapa WHERE id_e = ?;""", (student_phase_id,)).fetchone()
            phase_name = str(phase_name[0] + ' ' + phase_name[1])

            period = datetime.datetime.now().strftime('%d %B %Y')
            period = str(period + ' - ' + phase_name)

            cursor.execute(
            """INSERT INTO calificaciones (
                estudiante_id,
                materia_id,
                etapa_id,
                periodo,
                estado
            ) VALUES (?, ?, ?, ?, ?);""", (student_id, i['ID'], student_phase_id, period, 'En curso'))
            conexion.commit()

    else:
        cursor.execute(
            """UPDATE estudiante SET status = ? WHERE id_s = ?;""", (new_status, student_id))
        conexion.commit()

#* ------------------ UNPROMOTE STUDENT ------------------ *#
def unpromote_student(conexion, student_id):
    '''Disapprove a student'''
    # Connect to the database
    cursor = conexion.cursor()


    student_info = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()

    phase_type = cursor.execute(
        """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (student_info[0],)).fetchone()[0]

    if phase_type.split(' ')[1] == 'Año':
        phase_type = 'Liceo'
    elif phase_type.split(' ')[1] == 'Grado':
        phase_type = 'Colegio'

    phase_data = cursor.execute(
        """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (student_info[0],)).fetchone()[0]

    cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia WHERE etapa = ?;""", (phase_data,))
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

    for i in search:
        subject['ID'] = i[0]
        subject['Nombre'] = i[1]
        subject['Etapa'] = i[2]
        subjects_list.append(subject.copy())

    # Ordenar la lista de materias en orden ascendente
    subjects_list.sort(key=lambda x: x['ID'])

    for i in subjects_list:
        student_phase_id = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()[0]

        phase_name = cursor.execute(
        """SELECT grado_anio, seccion FROM etapa WHERE id_e = ?;""", (student_phase_id,)).fetchone()
        phase_name = str(phase_name[0] + ' ' + phase_name[1])

        period = datetime.datetime.now() + datetime.timedelta(days=1)
        period = period.strftime('%d %B %Y')
        period = str(period + ' - ' + phase_name)

        cursor.execute(
        """INSERT INTO calificaciones (
            estudiante_id,
            materia_id,
            etapa_id,
            periodo,
            estado
        ) VALUES (?, ?, ?, ?, ?);""", (student_id, i['ID'], student_phase_id, period, 'En curso'))
        conexion.commit()


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
        """SELECT DISTINCT periodo, estado FROM calificaciones WHERE estudiante_id = ?;""", (student_id,))
    search = cursor.fetchall()
    conexion.close()

    periods = []

    periods_info = {
        'Periodo': None,
        'Estado': None
    }

    for i in search:
        periods_info['Periodo'] = i[0]
        periods_info['Estado'] = i[1]
        periods.append(periods_info.copy())

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

#* ------------------ SYNC STUDENT ------------------ *#
def sync_students(student_id):
    '''Verify if the student phase is the same as the student phase in the grades table'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    student = cursor.execute(
        """SELECT * FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()

    student_info = { # student info
        'ID': None,
        'name': None,
        'lastname': None,
        'ci': None,
        'birth_date': None,
        'address': None,
        'phase_id': None,
        'admission_date': None,
        'status': None
    }

    student_info['ID'],student_info['ci'], student_info['name'], student_info['lastname'], student_info['birth_date'], student_info['address'], student_info['phase_id'], student_info['admission_date'], student_info['status'] = student



    student_phase_grade = cursor.execute(
        """SELECT etapa_id FROM calificaciones WHERE estudiante_id = ?;""", (student_info['ID'],)).fetchone()

    if student_info['phase_id'] != student_phase_grade[0]:

        student_info = cursor.execute(
        """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()

        phase_data = cursor.execute(
            """SELECT grado_anio FROM etapa WHERE id_e = ?;""", (student_info[0],)).fetchone()[0]

        if phase_data.split(' ')[1] == 'Año':
            phase_type = 'Liceo'
        elif phase_data.split(' ')[1] == 'Grado':
            phase_type = 'Colegio'

        cursor.execute(
        """SELECT id_m,nombre, etapa FROM materia WHERE etapa = ?;""", (phase_data,))
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

        for i in search:
            subject['ID'] = i[0]
            subject['Nombre'] = i[1]
            subject['Etapa'] = i[2]
            subjects_list.append(subject.copy())

        # Ordenar la lista de materias en orden ascendente
        subjects_list.sort(key=lambda x: x['ID'])

        for i in subjects_list:

            student_phase_id = cursor.execute(
            """SELECT etapa_id FROM estudiante WHERE id_s = ?;""", (student_id,)).fetchone()[0]

            phase_name = cursor.execute(
            """SELECT grado_anio, seccion FROM etapa WHERE id_e = ?;""", (student_phase_id,)).fetchone()
            phase_name = str(phase_name[0] + ' ' + phase_name[1])

            period = datetime.datetime.now().strftime('%d %B %Y')
            period = str(period + ' - ' + phase_name)

            cursor.execute(
            """INSERT INTO calificaciones (
                estudiante_id,
                materia_id,
                etapa_id,
                periodo,
                estado
            ) VALUES (?, ?, ?, ?, ?);""", (student_id, i['ID'], student_phase_id, period, 'En curso'))
            conexion.commit()
        conexion.close()
        return True
    else:
        conexion.close()
        return False
