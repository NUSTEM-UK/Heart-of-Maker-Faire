import sqlite3
from sqlite3 import Error

import MySQLdb

import random
import time
import sys

host = "localhost"
user = "testuser"
password = "userpassword"
database = "databasename"



# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)
#     return None

def create_new_table(conn, populate):
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
        if populate == True:
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
    tablename = "heart_store" + time.strftime("%M%S")
    # create an empty table
    try:
        c = conn.cursor()

        c.execute(""" CREATE TABLE IF NOT EXISTS """ + tablename + """ (
                                            cell_id integer,
                                            qr_code integer,
                                            heart_rate integer
                                            ); """)
    # insert the old data into the new table
        c.execute(""" INSERT INTO """ + tablename + """ SELECT * FROM heart_store""")
    # drop the old table
        c.execute(""" DROP TABLE heart_store""")
    # create a new table
        create_new_table(conn, True)
        conn.commit()
    except Error as e:
        print(e)

def QR_usage_checker(conn, qrcode):
    try:
        c = conn.cursor()
        print("THIS BIT IS HAPPENING")
        c.execute("SELECT * FROM heart_store WHERE qr_code=?", (qrcode,))
        row = c.fetchall()
        print(row)
        if not row:
            print("UNIQUE")
            return(True)
        else:
            print("NOT UNIQUE")
            return(False)
    except:
        pass

def unique_cell_picker(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM heart_store WHERE qr_code=0")
    rows = c.fetchall()
    randomcell = random.randint(0,len(rows)-1)
    chosen_row = rows[randomcell]
    return(chosen_row[0])

try:
    conn = MySQLdb.connect(host,user,password,database)
except:
    conn = sqlite3.connect(database)

loadNew = sys.argv[1]     # check command line arguments
try:
    if loadNew == "y":
        print("Storing old data")
        store_old_data(conn)
except:
    pass
