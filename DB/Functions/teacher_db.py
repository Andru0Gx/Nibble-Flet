'''Nibble DB - Teacher's Functions'''

# Table Structure

# Table Name: profesor
    # id_p INTEGER PRIMARY KEY AUTOINCREMENT,
    # cedula TEXT NOT NULL UNIQUE,
    # nombres TEXT NOT NULL,
    # apellidos TEXT NOT NULL,
    # f_nacimiento TEXT NOT NULL,
    # telefono1 TEXT NOT NULL,
    # telefono2 TEXT,
    # direccion TEXT NOT NULL,
    # correo TEXT NOT NULL UNIQUE

# Table Name: materia
    # id_m INTEGER PRIMARY KEY AUTOINCREMENT,
    # nombre TEXT NOT NULL

# Table Name: profesor_materias
    # profesor_id INTEGER,
    # materia_id INTEGER,
    # PRIMARY KEY(profesor_id, materia_id),
    # CONSTRAINT fk_prof_ci FOREIGN KEY(profesor_id) REFERENCES profesor(id_p) ON DELETE CASCADE ON UPDATE CASCADE,
    # CONSTRAINT fk_mat_id FOREIGN KEY(materia_id) REFERENCES materia(id_m) ON DELETE CASCADE ON UPDATE CASCADE


# Libraries
import sqlite3

#^ ------------------ VALIDATE ------------------ ^#
def validate_ci(ci):
    '''Validate the CI'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # Search if the CI is already in the database (Student / Teacher)
    cursor.execute(
        """SELECT cedula FROM estudiante WHERE cedula = ?;""", (ci,))
    ci_estudiante = cursor.fetchone()

    cursor.execute(
        """SELECT cedula FROM profesor WHERE cedula = ?;""", (ci,))
    ci_profesor = cursor.fetchone()

    if ci_estudiante or ci_profesor:
        return False
    else:
        return True



#^ ------------------ ADD ------------------ ^#
#* 1 - Add Teacher
def teacher_add(ci, name, last_name, birth_date, phone1, phone2, address, email):
    '''Add a new teacher to the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """INSERT INTO profesor (
            cedula,
            nombres,
            apellidos,
            f_nacimiento,
            telefono1,
            telefono2,
            direccion,
            correo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", (ci, name, last_name, birth_date, phone1, phone2, address, email))
    conexion.commit()
    conexion.close()

    return teacher_search(ci)['ID']

#* 2 - Add Subject to a Teacher
def subject_add_to_teacher(teacher_id, subject_id):
    '''Add a subject to a teacher'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    if cursor.execute(
        """SELECT profesor_id FROM profesor_materias WHERE profesor_id = ? AND materia_id = ?;""", (teacher_id, subject_id)).fetchone() is not None:
        return False
    else:
        cursor.execute(
            """INSERT INTO profesor_materias (
                profesor_id,
                materia_id
            ) VALUES (?, ?);""", (teacher_id, subject_id))
        conexion.commit()
        conexion.close()
        return True

#^ ------------------ SEARCH ------------------ ^#
#* 1 - Search Teacher
def teacher_search(ci):
    '''Search a teacher in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT * FROM profesor WHERE cedula = ? or id_p = ?;""", (ci, ci))
    teacher = cursor.fetchone()

    teacher_info = {
        'ID': None,
        'Name': None,
        'Last_Name': None,
        'CI': None,
        'Birth_Date': None,
        'Phone1': None,
        'Phone2': None,
        'Address': None,
        'Email': None,
    }

    if teacher:
        teacher_info['ID'], teacher_info['CI'], teacher_info['Name'], teacher_info['Last_Name'], teacher_info['Birth_Date'], teacher_info['Phone1'], teacher_info['Phone2'], teacher_info['Address'], teacher_info['Email'] = teacher
    else:
        return False

    conexion.close()
    return teacher_info

#* 2 - Search Teacher's Subjects
def teacher_subjects_search(teacher_id):
    '''Search a teacher's subjects in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT materia_id FROM profesor_materias WHERE profesor_id = ?;""", (teacher_id,))
    subject_list = cursor.fetchall()

    subject = {
        'ID': None,
        'Name': None,
        'Grade': None,
    }

    for subject_id in subject_list:
        cursor.execute(
            """SELECT id_m, nombre, etapa FROM materia WHERE id_m = ?;""", (subject_id[0],))
        subject['ID'], subject['Name'], subject['Grade'] = cursor.fetchone()
        subject_list[subject_list.index(subject_id)] = subject.copy()

    conexion.close()
    return subject_list

#^ ------------------ DELETE ------------------ ^#
#* 1 - Delete Teacher
def teacher_delete(ci):
    '''Delete a teacher from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM profesor WHERE cedula = ?;""", (ci,))
    conexion.commit()
    conexion.close()

#* 2 - Delete Teacher and Subjects
def teacher_and_subjects_delete(teacher_id):
    '''Delete a teacher's subjects from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM profesor_materias WHERE profesor_id = ?;""", (teacher_id,))
    conexion.commit()
    conexion.close()

#* 3 - Delete Teacher's Subject
def teacher_subject_delete(teacher_id, subject_id):
    '''Delete a teacher's subject from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM profesor_materias WHERE profesor_id = ? AND materia_id = ?;""", (teacher_id, subject_id))
    conexion.commit()
    conexion.close()

#^ ------------------ UPDATE ------------------ ^#
#* 1 - Update Teacher
def teacher_update(ci, name, last_name, birth_date, phone1, phone2, address, email, id):
    '''Update a teacher in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute("""UPDATE profesor SET
        cedula = ?,
        nombres = ?,
        apellidos = ?,
        f_nacimiento = ?,
        telefono1 = ?,
        telefono2 = ?,
        direccion = ?,
        correo = ?
        WHERE id_p = ?;""", (ci, name, last_name, birth_date, phone1, phone2, address, email, id))
    conexion.commit()
    conexion.close()

#^ ------------------ GET ------------------ ^#
#* 1 - Get the first X teachers
def get_teachers(start_index, end_index):
    '''Get the first X teachers from the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(f"""SELECT * FROM profesor LIMIT {start_index - 1}, {end_index - start_index + 1};""")
    teachers = cursor.fetchall()

    teachers_list = []
    teacher_info = {
        'ID': None,
        'CI': None,
        'Name': None,
        'Last_Name': None,
        'Birth_Date': None,
        'Phone1': None,
        'Phone2': None,
        'Address': None,
        'Email': None,
    }

    for teacher in teachers:
        teacher_info['ID'], teacher_info['CI'], teacher_info['Name'], teacher_info['Last_Name'], teacher_info['Birth_Date'], teacher_info['Phone1'], teacher_info['Phone2'], teacher_info['Address'], teacher_info['Email'] = teacher
        teachers_list.append(teacher_info.copy())

    conexion.close()
    return teachers_list

#* 2 - Check the amount of teachers
def check_amount():
    '''Check the amount of teachers in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(f"""SELECT COUNT(*) FROM profesor;""")
    amount = cursor.fetchone()[0]

    conexion.close()
    return amount

#^ ------------------ FILTER ------------------ ^#
#* 1 - Filter Teachers (NAME, LAST_NAME, CI, PHONE1)
def filter_teachers_db(filter):
    '''Filter teachers in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # Get the teachers
    cursor.execute(f"""SELECT * FROM profesor WHERE nombres LIKE '%{filter}%' OR apellidos LIKE '%{filter}%' OR cedula LIKE '%{filter}%' OR telefono1 LIKE '%{filter}%';""")
    teachers = cursor.fetchall()

    teachers_list = []
    teacher_info = {
        'ID': None,
        'CI': None,
        'Name': None,
        'Last_Name': None,
        'Birth_Date': None,
        'Phone1': None,
        'Phone2': None,
        'Address': None,
        'Email': None,
    }

    for teacher in teachers:
        teacher_info['ID'], teacher_info['CI'], teacher_info['Name'], teacher_info['Last_Name'], teacher_info['Birth_Date'], teacher_info['Phone1'], teacher_info['Phone2'], teacher_info['Address'], teacher_info['Email'] = teacher
        teachers_list.append(teacher_info.copy())

    conexion.close()
    return teachers_list


#^ ------------------ SCHEDULE TEACHERS ------------------ ^#
#* 1 - Filter teachers by subject
def filter_teachers_by_subject(subject_id):
    '''Filter teachers by subject'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    # Get the teachers
    cursor.execute(f"""SELECT profesor_id FROM profesor_materias WHERE materia_id = {subject_id};""")
    teachers = cursor.fetchall()

    teachers_list = []

    for teacher in teachers:
        teachers_list.append(teacher[0])

    conexion.close()
    return teachers_list