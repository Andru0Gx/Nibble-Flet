
# Libraries
import sqlite3

#$ ================================ Functions ================================
#* -------------------------------- Insert --------------------------------

def insertar(cedula, nombres, apellidos, f_nacimiento, telefono1, telefono2, direccion, correo):

    conexion = sqlite3.connect('DB/Nibble.db')

    cursor = conexion.cursor()
 
    cursor.execute(
        """INSERT INTO profesor (cedula, nombres, apellidos, f_nacimiento, telefono1, telefono2, direccion, correo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
            (cedula, nombres, apellidos, f_nacimiento, telefono1, telefono2, direccion, correo)
            )
    conexion.commit()
    conexion.close()



#* -------------------------------- Delete --------------------------------
def eliminar(cedula):

    conexion = sqlite3.connect('DB/Nibble.db')

    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM profesor WHERE cedula = ?;""",
        (cedula)
    )
    conexion.commit()
    conexion.close()


#* -------------------------------- Modify --------------------------------
def modificar(cedula, nombres, apellidos, f_nacimiento, telefono1, telefono2, direccion, correo):
   
    conexion = sqlite3.connect('DB/Nibble.db')

    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE profesor SET cedula = ?, nombres = ?, apellidos = ?, f_nacimiento = ?, telefono1 = ?, telefono2 = ?, direccion = ?, correo = ?
        WHERE cedula = ?;""",
        (cedula, nombres, apellidos, f_nacimiento, telefono1, telefono2, direccion, correo, cedula)
    )
    conexion.commit()
    conexion.close()