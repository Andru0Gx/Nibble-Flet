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
            nombre TEXT NOT NULL,
            etapa TEXT NOT NULL
        );""")
    conexion.commit()


#* --------------------------- Subject_Teacher - Table ---------------------------
def subject_teacher_table(conexion):
    '''Creates a table named "profesor_materias" in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS profesor_materias(
            profesor_id INTEGER,
            materia_id INTEGER,
            PRIMARY KEY(profesor_id, materia_id),
            CONSTRAINT fk_prof_ci FOREIGN KEY(profesor_id) REFERENCES profesor(id_p) ON DELETE CASCADE ON UPDATE CASCADE,
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
            seccion TEXT,
            last_added TEXT
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
        """CREATE TABLE IF NOT EXISTS calificaciones(
            id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id TEXT NOT NULL,
            materia_id INTEGER NOT NULL,
            etapa_id INTEGER NOT NULL,
            momento_1 DECIMAL(4,2),
            momento_2 DECIMAL(4,2),
            momento_3 DECIMAL(4,2),
            nota_final DECIMAL(4,2),
            periodo TEXT NOT NULL,
            estado TEXT,
            CONSTRAINT fk_est_id_grade FOREIGN KEY(estudiante_id) REFERENCES estudiante(id_s) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_mat_id_grade FOREIGN KEY(materia_id) REFERENCES materia(id_m) ON DELETE CASCADE ON UPDATE CASCADE
            CONSTRAINT fk_etapa_id_grade FOREIGN KEY(etapa_id) REFERENCES etapa(id_e) ON DELETE CASCADE ON UPDATE CASCADE
        );""")
    conexion.commit()

#* --------------------------- schedule - Table ---------------------------
def schedule_table(conexion):
    '''Creates a table named 'horario' in a SQLite database'''

    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS horario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_horario INTEGER,
            profesor_id TEXT,
            materia_id INTEGER,
            bloque_hora TEXT,
            bloque_dia TEXT,
            fecha TEXT,
            etapa  TEXT,
            formato TEXT,
            guide_teacher TEXT,
            CONSTRAINT fk_prof__id_schedule FOREIGN KEY(profesor_id) REFERENCES profesor(id_p) ON DELETE CASCADE ON UPDATE CASCADE,
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
