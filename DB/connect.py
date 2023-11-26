'''Nibble-DB Commands'''

# Libraries
import sqlite3


#$ ================================ Tables ================================
#* --------------------------- Teacher - Table ---------------------------
def teacher_table(conexion):
    '''Creates a table named 'profesor' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS profesor(
            cedula TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            f_nacimiento TEXT NOT NULL,
            telefono1 TEXT NOT NULL,
            telefono2 TEXT,
            direccion TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE
        );""")
    conexion.commit()


#* --------------------------- Subject - Table ---------------------------
def subject_table(conexion):
    '''Creates a table named 'materia' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS materia(
            id_m INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        );""")
    conexion.commit()


#* --------------------------- Subject_Teacher - Table ---------------------------
def subject_teacher_table(conexion):
    '''Creates a table named "profesor_materias" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS profesor_materias(
            profesor_ci TEXT,
            materia_id INTEGER,
            PRIMARY KEY(profesor_ci, materia_id),
            CONSTRAINT fk_prof_ci FOREIGN KEY(profesor_ci) REFERENCES profesor(cedula_p),
            CONSTRAINT fk_mat_id FOREIGN KEY(materia_id) REFERENCES materia(id_m)
        );""")
    conexion.commit()


#* --------------------------- Student - Table ---------------------------
def student_table(conexion):
    '''Creates a table named "estudiante" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS estudiante(
            cedula TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            f_nacimiento TEXT NOT NULL,
            direccion TEXT NOT NULL,
            correo TEXT UNIQUE,
            etapa_id INTEGER NOT NULL,
            CONSTRAINT fk_etapa FOREIGN KEY(etapa_id) REFERENCES etapa(id_e)
        );""")
    conexion.commit()


#* --------------------------- Parent - Table ---------------------------
def phase_table(conexion):
    '''Creates a table named "etapa" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS etapa(
            id_e INTEGER PRIMARY KEY AUTOINCREMENT,
            grado_anio TEXT,
            seccion TEXT
        );""")
    conexion.commit()


#* --------------------------- Parent - Table ---------------------------
def parent_table(conexion):
    '''Creates a table named "representante" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS representante(
            cedula TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            telefono1 TEXT NOT NULL,
            telefono2 TEXT
        );""")
    conexion.commit()


#* --------------------------- Parent_Student - Table ---------------------------
def parent_student_table(conexion):
    '''Creates a table named "repre_estudiante" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS repre_estudiante(
            representante_ci TEXT,
            estudiante_ci TEXT,
            PRIMARY KEY(representante_ci, estudiante_ci)
            CONSTRAINT fk_repre_ci FOREIGN KEY(representante_ci) REFERENCES representante(cedula_r),
            CONSTRAINT fk_estudiante_ci FOREIGN KEY(estudiante_ci) REFERENCES estudiante(cedula_e)
        );""")
    conexion.commit()


#* --------------------------- Grade - Table ---------------------------
def grade_table(conexion):
    '''Creates a table named 'nota' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS nota(
            id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_ci TEXT NOT NULL,
            materia_id INTEGER NOT NULL,
            momento INTEGER NOT NULL,
            nro_actividad INTEGER NOT NULL,
            descrip_actividad TEXT,
            calificacion DECIMAL(4,2) NOT NULL,
            fecha TEXT NOT NULL
        );""")
    conexion.commit()

#* --------------------------- Calendar - Table ---------------------------
def calendar_table(conexion):
    '''Creates a table named 'calendario' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS calendario(
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha TEXT NOT NULL
        );""")
    conexion.commit()

#* --------------------------- User - Table ---------------------------
def user_table(conexion):
    '''Creates a table named 'usuario' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS usuario(
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            respuesta_seguridad_1 TEXT NOT NULL,
            respuesta_seguridad_2 TEXT NOT NULL,
            respuesta_seguridad_3 TEXT NOT NULL
        );""")
    conexion.commit()

#$ ================================ functions for insert records in the tables ================================

#$ ================================ functions for delete records of the tables ================================




#* --------------------------- Create The Tables ---------------------------
def create_tables():
    '''Creates all the tables in a SQLite database'''

    try:
        conexion = sqlite3.connect('DB/escuela.db')
        
        # Create the main tables
        teacher_table(conexion)
        subject_table(conexion)
        subject_teacher_table(conexion)
        phase_table(conexion)
        student_table(conexion)
        parent_table(conexion)
        parent_student_table(conexion)
        grade_table(conexion)

        # Create the secondary tables
        calendar_table(conexion)
        user_table(conexion)

        # Close the connection
        conexion.close()

    except Exception as ex:
        print(ex) #TODO - Delete this line / Write a log file

# Run the function
create_tables()
