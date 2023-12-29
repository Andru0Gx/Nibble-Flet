'''Nibble DB - Temp Data table's functions'''

import sqlite3

#* --------------------------- Save Data ---------------------------
def save_tempdata_db(data):
    '''Saves data in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """INSERT INTO temp_data(
            data
        ) VALUES (?);""",
        (data,)
    )

    conexion.commit()
    conexion.close()

#* --------------------------- Get Data ---------------------------
def get_tempdata_db():
    '''Get data from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT data FROM temp_data;"""
    )

    data = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return data[0][0]

#* --------------------------- Delete Data ---------------------------
def delete_tempdata_db():
    '''Delete data from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM temp_data;"""
    )

    conexion.commit()
    conexion.close()


#* --------------------------- Check if there is data ---------------------------
def check_tempdata_db():
    '''Check if there is data in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT COUNT(*) FROM temp_data;"""
    )

    data = cursor.fetchall()

    conexion.commit()
    conexion.close()

    if data[0][0] == 0:
        return False
    else:
        return True
