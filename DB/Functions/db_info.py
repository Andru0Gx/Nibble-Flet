'''Nibble DB - Info'''

# Libraries
import sqlite3

#^ ------------------ GET ------------------ ^#
#*1 - Get amount of records in the database
def get_amount(table):
    '''Get amount of records in the database'''
    # Connect to the database
    conexion = sqlite3.connect('DB/Nibble.db')
    cursor = conexion.cursor()

    cursor.execute(f"""SELECT COUNT(*) FROM {table};""")
    amount = cursor.fetchone()[0]

    conexion.close()
    return amount