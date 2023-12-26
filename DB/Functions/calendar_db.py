'''Nibble DB - Calendar's table functions'''

import sqlite3

#* --------------------------- Save Event ---------------------------
def save_event_db(title, description, date):
    '''Saves an event in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """INSERT INTO calendario(
            titulo,
            descripcion,
            fecha
        ) VALUES (?, ?, ?);""",
        (title, description, date)
    )

    conexion.commit()
    conexion.close()


#* --------------------------- Get the first X Events ---------------------------
def get_events(start_index, end_index):
    '''Get events from start_index to end_index from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        f"""SELECT titulo, descripcion, fecha, id_evento FROM calendario LIMIT {start_index - 1}, {end_index - start_index + 1};"""
    )

    events = cursor.fetchall()

    # Format the data to a list of dictionaries
    event_list = []
    for event in events:
        event_dict = {
            'title': event[0],
            'description': event[1],
            'date': event[2],
            'id': event[3]
        }
        event_list.append(event_dict)

    conexion.commit()
    conexion.close()

    return event_list

#* --------------------------- Check the amount of events ---------------------------

def check_amount():
    '''Get the amount of events from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT COUNT(*) FROM calendario;"""
    )

    amount = cursor.fetchall()[0][0]

    conexion.commit()
    conexion.close()

    return amount

#* --------------------------- Edit an event ---------------------------
def edit_event_db(title, description, date, id_event):
    '''Edit an event in the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """UPDATE calendario SET titulo = ?, descripcion = ?, fecha = ? WHERE id_evento = ?;""",
        (title, description, date, id_event)
    )

    conexion.commit()
    conexion.close()

#* --------------------------- get last event added ---------------------------
def get_last_event():
    '''Get the last event added from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """SELECT titulo, descripcion, fecha, id_evento FROM calendario ORDER BY id_evento DESC LIMIT 1;"""
    )

    event = cursor.fetchall()[0]


    conexion.commit()
    conexion.close()

    return event[3]


#* --------------------------- Delete an event ---------------------------
def delete_event_db(id_event):
    '''Delete an event from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    cursor.execute(
        """DELETE FROM calendario WHERE id_evento = ?;""",
        (id_event,)
    )

    conexion.commit()
    conexion.close()


#* --------------------------- filter list by any event info ---------------------------
def filter_event_db(filter, date = False):
    '''Filter the events from the database'''
    conexion = sqlite3.connect('DB/nibble.db')
    cursor = conexion.cursor()

    if date:
        cursor.execute(
            f"""SELECT titulo, descripcion, fecha, id_evento FROM calendario WHERE fecha = '{filter}';"""
        )
    else:
        cursor.execute(
            f"""SELECT titulo, descripcion, fecha, id_evento FROM calendario WHERE titulo LIKE '%{filter}%' OR descripcion LIKE '%{filter}%' OR fecha LIKE '%{filter}%';"""
        )

    events = cursor.fetchall()

    # Format the data to a list of dictionaries
    event_list = []
    for event in events:
        event_dict = {
            'title': event[0],
            'description': event[1],
            'date': event[2],
            'id': event[3]
        }
        event_list.append(event_dict)

    conexion.commit()
    conexion.close()

    return event_list
