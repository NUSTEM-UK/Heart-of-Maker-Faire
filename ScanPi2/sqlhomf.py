"""Dependencies
apt-get install python3-dev ???
pip3 install mysqlclient
"""
import MySQLdb

import random
import time
import sys

host = "192.168.1.1"
user = "root"
password = "plokij"
database = "Heart"

def create_new_table(conn, populate):
    try:
        c = conn.cursor()
        c.execute("""DROP TABLE IF EXISTS heart_store""")
        c.execute(""" CREATE TABLE IF NOT EXISTS heart_store (
                                            cell_id integer,
                                            qr_code integer,
                                            heart_rate integer
                                        )""")
        if populate == True:
            for i in range(512):
                sql = """ INSERT INTO heart_store\
                        (cell_id,qr_code,heart_rate) \
                        VALUES ('%d', '%d', '%d')""" % \
                        (i, 0, 0)

                c.execute(sql)
        conn.commit()

    except Error as e:
        print(e)

def update_heart(conn, cell, qr, hr):
    sql = """ UPDATE heart_store
              SET qr_code = %d ,
                  heart_rate = %d
              WHERE  cell_id = %d """ % (qr, hr, cell)
    c = conn.cursor()
    c.execute(sql)
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
        c.execute("SELECT * FROM heart_store WHERE qr_code=%d" % qrcode)
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
    print(conn)
except:
    print("Error")



try:
    loadNew = sys.argv[1]     # check command line arguments
    if loadNew == "y":
        print("Storing old data")
        store_old_data(conn)
except:
    pass

if __name__ == "__main__":
    create_new_table(conn, True)
