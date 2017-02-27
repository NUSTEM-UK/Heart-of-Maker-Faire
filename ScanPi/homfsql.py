import sqlite3
from sqlite3 import Error
import random
import time

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_new_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS heart_store (
                                            cell_id integer,
                                            qr_code integer,
                                            heart_rate integer
                                        ); """)
        for i in range(512):
            sql = ''' INSERT INTO heart_store(cell_id,qr_code,heart_rate)
                          VALUES(?,?,?) '''
            c.execute(sql, (i, 0, 0))
            conn.commit()

    except Error as e:
        print(e)

def update_heart(conn, cell, qr, hr):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE heart_store
              SET qr_code = ? ,
                  heart_rate = ?
              WHERE  cell_id = ?'''
    c = conn.cursor()
    new_data = (qr,hr,cell)
    c.execute(sql, new_data)
    conn.commit()

def store_old_data(conn):
    tablename = "heart_store" + time.strftime("%m%d-%H%M%S")
    # create an empty table
    try:
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS ? (
                                            cell_id integer,
                                            qr_code integer,
                                            heart_rate integer
                                            ); """, tablename)
    # insert the old data into the new table
        c.execute(""" INSERT INTO ? SELECT * FROM heart_store""", tablename)
    # drop the old table
        c.execute(""" DROP TABLE heart_store""")
    # create a new table
        create_new_table(conn)
        conn.commit()
    except:
        pass

def QR_usage_checker(conn, qrcode):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM heart_store WHERE qr_code=?", (qrcode))
        row = c.fetchall()
        return(True,row[0])
    except:
        pass

def unique_cell_picker(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM heart_store WHERE qr_code=0")
    rows = cur.fetchall()
    randomcell = random.randint(0,len(rows))
    chosen_row = rows[randomcell]
    print(chosen_row[0])
    return(chosen_row[0])
