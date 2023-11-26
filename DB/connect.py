
import sqlite3

#$ ========== functions for create the tables ==========
def teacher_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE profesor(
            cedula_p TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            f_nacimiento TEXT NOT NULL,
            tlf TEXT NOT NULL,
            tlfb TEXT,
            direccion TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE
        );""")
    conexion.commit()
    conexion.close()

def matter_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE materia(
            id_m INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        );""")
    conexion.commit()
    conexion.close()

def matter_teacher_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE prof_mat(
            profesor_ci TEXT,
            materia_id INTEGER,
            PRIMARY KEY(profesor_ci, materia_id),
            CONSTRAINT fk_prof_ci FOREIGN KEY(profesor_ci) REFERENCES profesor(cedula_p),
            CONSTRAINT fk_mat_id FOREIGN KEY(materia_id) REFERENCES materia(id_m)
        );""")
    conexion.commit()
    conexion.close()

def student_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE estudiante(
            cedula_e TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            f_nacimiento TEXT NOT NULL,
            tlf TEXT NOT NULL,
            tlfb TEXT,
            direccion TEXT NOT NULL,
            correo TEXT UNIQUE,
            etapa_id INTEGER NOT NULL,
            CONSTRAINT fk_etapa FOREIGN KEY(etapa_id) REFERENCES etapa(id_e)
        );""")
    conexion.commit()
    conexion.close()

def stage_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE etapa(
            id_e INTEGER PRIMARY KEY AUTOINCREMENT,
            grado_anio TEXT,
            seccion TEXT
        );""")
    conexion.commit()
    conexion.close()

def representative_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE representante(
            cedula_r TEXT PRIMARY KEY,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            tlf TEXT NOT NULL,
            tlfb TEXT
        );""")
    conexion.commit()
    conexion.close()

def repre_student_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE repre_estudiante(
            representante_ci TEXT,
            estudiante_ci TEXT,
            PRIMARY KEY(representante_ci, estudiante_ci)
            CONSTRAINT fk_repre_ci FOREIGN KEY(representante_ci) REFERENCES representante(cedula_r),
            CONSTRAINT fk_estudiante_ci FOREIGN KEY(estudiante_ci) REFERENCES estudiante(cedula_e)
        );""")
    conexion.commit()
    conexion.close()

def grade_table():
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE nota(
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
    conexion.close()

#$ ========== functions for insert records in the tables ==========

#$ ========== functions for delete records of the tables ==========

# Ejecutar
try:
    conexion = sqlite3.connect("database/escuela.db")
    #todo: orden de creación de las tablas
    #teacher_table()
    #matter_table()
    #matter_teacher_table()
    #stage_table()
    #student_table()
    #representative_table()
    #repre_student_table()
    #grade_table()
    
    #todo: llamar funciones para probar

except Exception as ex:
    print(ex)