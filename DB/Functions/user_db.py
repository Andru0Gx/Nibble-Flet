'''Nibble DB - User's table functions'''

# Libraries
import sqlite3


#* --------------------------- Save User ---------------------------

def save_user(user, password, email, security_question1, security_question2, security_question3):
    '''Saves a user in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """INSERT INTO usuario(
            usuario,
            correo,
            contrasena,
            respuesta_seguridad_1,
            respuesta_seguridad_2,
            respuesta_seguridad_3
        ) VALUES (?, ?, ?, ?, ?, ?);""",
        (user, email, password, security_question1, security_question2, security_question3)
    )

    conexion.commit()
    conexion.close()

#* --------------------------- Get the User info ---------------------------
def get_user():
    '''Get User, Password, Email, Security Questions from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT usuario, contrasena, correo, respuesta_seguridad_1, respuesta_seguridad_2, respuesta_seguridad_3 FROM usuario;"""
    )

    user = cursor.fetchall()

    # Format the data to a dictionary
    user = {
        'user': user[0][0],
        'password': user[0][1],
        'email': user[0][2],
        'question1': user[0][3],
        'question2': user[0][4],
        'question3': user[0][5]
    }

    conexion.commit()
    conexion.close()

    return user


#* --------------------------- Update User ---------------------------
def update_user(user, password, email, security_question1, security_question2, security_question3):
    '''Updates the user's info in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE usuario SET
            usuario = ?,
            correo = ?,
            contrasena = ?,
            respuesta_seguridad_1 = ?,
            respuesta_seguridad_2 = ?,
            respuesta_seguridad_3 = ?;""",
        (user, email, password, security_question1, security_question2, security_question3)
    )

    conexion.commit()
    conexion.close()



#* --------------------------- Block user's table ---------------------------
def block_user():
    '''Verifies if the user's table has 1 record'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT * FROM usuario;"""
    )

    user = cursor.fetchall()

    if len(user) == 1:
        return True
    else:
        return False
