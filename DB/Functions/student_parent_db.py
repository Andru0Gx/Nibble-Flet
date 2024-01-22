'''Nibble DB - Student Parent Table's Functions'''

# Libraries
import sqlite3

#^ ------------------ Validate CI ------------------ *#
def validate_ci(ci, representante = True):
    '''Validate the CI'''
    # Check if the ci is already in any table of the database
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    if representante:
        cursor.execute(
            """SELECT cedula FROM estudiante WHERE cedula = ?;""", (ci,))
        ci_estudiante = cursor.fetchone()

        cursor.execute(
            """SELECT cedula FROM representante WHERE cedula = ?;""", (ci,))
        ci_representante = cursor.fetchone()

        cursor.execute(
            """SELECT cedula FROM profesor WHERE cedula = ?;""", (ci,))
        ci_profesor = cursor.fetchone()
    else:
        cursor.execute(
            """SELECT representante_id FROM repre_estudiante WHERE representante_id = ?;""", (ci,))
        ci_estudiante = cursor.fetchone()

        ci_representante = None
        ci_profesor = None

    conexion.close()
    if ci_estudiante or ci_representante or ci_profesor:
        return False
    else:
        return True

def validate_student(student_id, student_ci):
    '''Validate the student'''
    # Check if the ci is already in any table of the database
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()


    # Verificar si la cedula del estudiante coincide con la de otro estudiante (Omite el estudiante que se esta editando ID)
    cursor.execute(
        """SELECT cedula FROM estudiante WHERE cedula = ? AND id_s != ?;""", (student_ci, student_id))
    ci_estudiante = cursor.fetchone()

    # Verificar si la cedula del estudiante coincide con la de un representante
    cursor.execute(
        """SELECT cedula FROM representante WHERE cedula = ?;""", (student_ci,))
    ci_representante = cursor.fetchone()

    # Verificar si la cedula del estudiante coincide con la de un profesor
    cursor.execute(
        """SELECT cedula FROM profesor WHERE cedula = ?;""", (student_ci,))
    ci_profesor = cursor.fetchone()

    conexion.close()
    if ci_estudiante or ci_representante or ci_profesor:
        return False
    else:
        return True


#^ ------------------ Add ------------------ *#
#*1 - Add Student

def student_add(ci, name, lastname, birth_date, address, phase_id, admission_date, status):
    '''Add a student to the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()


    cursor.execute(
        """INSERT INTO estudiante (
            cedula,
            nombres,
            apellidos,
            f_nacimiento,
            direccion,
            etapa_id,
            f_ingreso,
            status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", (ci, name, lastname, birth_date, address, phase_id, admission_date, status))
    conexion.commit()
    conexion.close()

    return student_search(ci)['ID']

#*2 - Add Parent
def parent_add(ci, name, lastname, phone1, phone2):
    '''Add a parent to the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    # If the parent is already in the database, it will not be added
    if parent_search(ci):
        return parent_search(ci)['ID']
    else:
        cursor.execute(
            """INSERT INTO representante(
                cedula,
                nombres,
                apellidos,
                telefono1,
                telefono2
            ) VALUES (?, ?, ?, ?, ?);""", (ci, name, lastname, phone1, phone2))
        conexion.commit()
        conexion.close()

        return parent_search(ci)['ID']

#*3 - Add Parent Student
def parent_student_add(parent_ci, student_ci):
    '''Add a parent to a student'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """INSERT INTO repre_estudiante VALUES(
            ?, ?
        );""", (parent_ci, student_ci))
    conexion.commit()
    conexion.close()



#^ ------------------ Search ------------------ *#
#*1 - Search Student
def student_search(ci):
    '''Search a student in the database and return its info in a dictionary'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """SELECT * FROM estudiante WHERE id_s = ? or cedula = ?;""", (ci, ci))
    student = cursor.fetchone()

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

    # print(student)

    if student:
        student_info['ID'],student_info['ci'], student_info['name'], student_info['lastname'], student_info['birth_date'], student_info['address'], student_info['phase_id'], student_info['admission_date'], student_info['status'] = student
    else:
        return False

    conexion.close()
    return student_info

# student_search('v1234')

#*2 - Search Parent
def parent_search(ci):
    '''Search a parent in the database and return its info in a dictionary'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """SELECT * FROM representante WHERE id_r = ? or cedula = ?;""", (ci, ci))
    parent = cursor.fetchone()

    parent_info = { # parent info
        'ID': None,
        'name': None,
        'lastname': None,
        'ci': None,
        'phone1': None,
        'phone2': None
    }

    if parent:
        parent_info['ID'],parent_info['ci'], parent_info['name'], parent_info['lastname'], parent_info['phone1'], parent_info['phone2'] = parent
    else:
        return False

    conexion.close()
    return parent_info


#*3 - Search all the children of a parent
def parent_student_search(parent_ci = None, student_ci = None):
    '''Search all the children of a parent'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    # If the parent_ci is not None, it will search all the children of the parent
    if parent_ci:
        cursor.execute(
            """SELECT * FROM repre_estudiante WHERE representante_id = ?;""", (parent_ci,))
        children = cursor.fetchall()
        list_children = []
        children_info = { # children info
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

        for child in children:
            search = student_search(child[1])

            if search:
                children_info['ID'],children_info['name'], children_info['lastname'], children_info['ci'], children_info['birth_date'], children_info['address'], children_info['phase_id'], children_info['admission_date'], children_info['status'] = search.values()
                list_children.append(children_info.copy())
            else:
                return False

        conexion.close()
        return list_children

    # If the student_ci is not None, it will search the parent of the student and return his ci
    elif student_ci:
        cursor.execute(
            """SELECT representante_id FROM repre_estudiante WHERE estudiante_id = ?;""", (student_ci,))
        parent = cursor.fetchone()

        conexion.close()
        if parent:
            return parent[0]
        else:
            return False

    # If both are None, it will return False
    else:
        return False


#^ ------------------ Delete ------------------ *#
#*1 - Delete Student
def student_delete(ci):
    '''Delete a student from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """DELETE FROM estudiante WHERE cedula = ?;""", (ci,))
    conexion.commit()
    conexion.close()

#*2 - Delete Parent
def parent_delete(ci):
    '''Delete a parent from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """DELETE FROM representante WHERE cedula = ?;""", (ci,))
    conexion.commit()
    conexion.close()

#*3 - Delete Parent Student
def parent_student_delete(student_ci, parent_ci):
    '''Delete a parent from a student'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """DELETE FROM repre_estudiante WHERE representante_id = ? AND estudiante_id = ?;""", (parent_ci, student_ci))
    conexion.commit()
    conexion.close()


#^ ------------------ Update ------------------ *#
#*1 - Update Student
def student_update(ci, name, lastname, birth_date, address, phase_id, admission_date, id, status):
    '''Update a student in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """UPDATE estudiante SET cedula = ?, nombres = ?, apellidos = ?, f_nacimiento = ?, direccion = ?, etapa_id = ?, f_ingreso = ?, status = ? WHERE id_s = ?;""", (ci, name, lastname, birth_date, address, phase_id, admission_date, status, id))

    conexion.commit()
    conexion.close()

#*2 - Update Parent
def parent_update(ci, name, lastname, phone1, phone2, id):
    '''Update a parent in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """UPDATE representante SET cedula = ?, nombres = ?, apellidos = ?, telefono1 = ?, telefono2 = ? WHERE id_r = ?;""", (ci, name, lastname, phone1, phone2, id))
    conexion.commit()
    conexion.close()

#*3 - Update Parent Student
def parent_student_update(student_ci, parent_ci):
    '''Update a parent from a student'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()
    cursor.execute(
        """UPDATE repre_estudiante SET representante_id = ? WHERE estudiante_id = ?;""", (parent_ci, student_ci))
    conexion.commit()
    conexion.close()


#^ ------------------ Get ------------------ *#
#*1 - Get the first X students
def get_students(start_index, end_index):
    '''Get students from start_index to end_index from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        f"""SELECT * FROM estudiante LIMIT {start_index - 1}, {end_index - start_index + 1};"""
    )

    students = cursor.fetchall()
    list_students = []
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

    for student in students:
        student_info['ID'],student_info['ci'], student_info['name'], student_info['lastname'], student_info['birth_date'], student_info['address'], student_info['phase_id'], student_info['admission_date'], student_info['status'] = student
        list_students.append(student_info.copy())

    conexion.commit()
    conexion.close()

    return list_students


#*2 - check the amount of students
def check_amount():
    '''Get the amount of students from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT COUNT(*) FROM estudiante;"""
    )

    amount = cursor.fetchall()[0][0]

    conexion.commit()
    conexion.close()

    return amount


#^ ------------------ Filter ------------------ *#
#*1 - Filter Students (Name, Lastname, CI, phase, admission date, status)
def filter_students_db(filter):
    '''Filter students from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    phase_id = cursor.execute(f"""SELECT id_e FROM etapa WHERE grado_anio LIKE '%{filter}%'""").fetchone()

    if phase_id:
        cursor.execute(
            f"""SELECT * FROM estudiante WHERE etapa_id LIKE '%{phase_id[0]}%';"""
        )
    else:
        cursor.execute(
            f"""SELECT * FROM estudiante WHERE nombres LIKE '%{filter}%' OR apellidos LIKE '%{filter}%' OR cedula LIKE '%{filter}%' OR etapa_id LIKE '%{filter}%' OR f_ingreso LIKE '%{filter}%' OR status LIKE '%{filter}%';"""
        )
    students = cursor.fetchall()
    list_students = []
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

    for student in students:
        student_info['ID'],student_info['ci'], student_info['name'], student_info['lastname'], student_info['birth_date'], student_info['address'], student_info['phase_id'], student_info['admission_date'], student_info['status'] = student
        list_students.append(student_info.copy())

    conexion.commit()
    conexion.close()

    return list_students
