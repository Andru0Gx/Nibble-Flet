'''Nibble-DB - Tables'''

# Libraries
import sqlite3

#$ ================================ Tables ================================
#* --------------------------- Teacher - Table ---------------------------
def teacher_table(conexion):
    '''Creates a table named 'profesor' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS profesor(
            id_p INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL UNIQUE,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            f_nacimiento TEXT NOT NULL,
            telefono1 TEXT NOT NULL,
            telefono2 TEXT,
            direccion TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE
        );""")
    conexion.commit()


#* --------------------------- Subject_Matter - Table ---------------------------
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
            CONSTRAINT fk_prof_ci FOREIGN KEY(profesor_ci) REFERENCES profesor(cedula_p) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_mat_id FOREIGN KEY(materia_id) REFERENCES materia(id_m) ON DELETE CASCADE ON UPDATE CASCADE
        );""")
    conexion.commit()


#* --------------------------- Student - Table ---------------------------
def student_table(conexion):
    '''Creates a table named "estudiante" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS estudiante(
            id_s INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL UNIQUE,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            f_nacimiento TEXT NOT NULL,
            direccion TEXT NOT NULL,
            etapa_id INTEGER NOT NULL,
            f_ingreso TEXT NOT NULL,
            status TEXT NOT NULL,
            CONSTRAINT fk_etapa FOREIGN KEY(etapa_id) REFERENCES etapa(id_e) ON DELETE CASCADE ON UPDATE CASCADE
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
            id_r INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL UNIQUE,
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
            representante_id INTEGER,
            estudiante_id INTEGER,
            PRIMARY KEY(representante_id, estudiante_id),
            CONSTRAINT fk_rep_id FOREIGN KEY(representante_id) REFERENCES representante(id_r) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_est_id FOREIGN KEY(estudiante_id) REFERENCES estudiante(id_s) ON DELETE CASCADE ON UPDATE CASCADE
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

#* --------------------------- schedule - Table ---------------------------
def schedule_table(conexion):
    '''Creates a table named 'horario' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS horario(
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            anio_en_curso TEXT NOT NULL,
            dia TEXT NOT NULL,
            profesor_ci TEXT NOT NULL,
            materia_id INTEGER NOT NULL,
            bloque_hora,
            CONSTRAINT fk_prof_ci_schedule FOREIGN KEY(profesor_ci) REFERENCES profesor(cedula_p) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_mat__id_schedule FOREIGN KEY(materia_id) REFERENCES materia(id_m) ON DELETE CASCADE ON UPDATE CASCADE
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


#* --------------------------- TEMP DATA - Table ---------------------------
def temp_data_table(conexion):
    '''Creates a table named 'temp_data' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS temp_data(
            data TEXT PRIMARY KEY
        );""")
    conexion.commit()



#* --------------------------- Create The Tables ---------------------------
def create_tables():
    '''Creates all the tables in a SQLite database'''

    try:
        conexion = sqlite3.connect('DB/Nibble.db')

        #Create the main tables
        teacher_table(conexion)
        subject_table(conexion)
        subject_teacher_table(conexion)
        phase_table(conexion)
        student_table(conexion)
        parent_table(conexion)
        parent_student_table(conexion)
        grade_table(conexion)
        schedule_table(conexion)

        temp_data_table(conexion)

        #Create the secondary tables
        calendar_table(conexion)
        user_table(conexion)

        # Close the connection
        conexion.close()

    except Exception as ex:
        print(ex) #TODO - Delete this line / Write a log file
