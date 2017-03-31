""" These functions allow the two scanning units to access an SQL database served on
a Pi ZERO W, this ensure that no duplications of cell locations can occur. """
import MySQLdb
import random
import time
import sys

# set access details for the SQL db
host = "192.168.1.1"
user = "root"
password = "plokij"
database = "Heart"

def create_heartwatch_table(conn):
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS heart_watch""")
    c.execute("""CREATE TABLE IF NOT EXISTS heart_watch
                (colour char(20), status int, heartNum int)""")
    colours = ["green", "yellow", 'magenta', 'cyan']
    for i in colours:
        c.execute(""" INSERT INTO heart_watch (colour, status, heartNum)
                    VALUES ('%s', '%d', '%d')""" % (i, 0, 0))
    conn.commit()

def watch_colour_picker(conn, cellNum):
    #First select a currently unused colour
    c = conn.cursor()
    c.execute("""SELECT * FROM heart_watch WHERE status = 0""")
    rows = c.fetchall()
    if not rows: # if all four colurs have been chosen return False
        conn.commit()
        return False
    randomChoice = random.randint(0, len(rows)-1)
    chosenRow = rows[randomChoice]
    chosenColour = str(chosenRow[0])
    print(chosenColour)

    # Lock in that colour choice
    sql = """ UPDATE heart_watch
              SET status = 1 
              WHERE  colour = '%s' """ % chosenColour
    c.execute(sql)
    conn.commit()
    c.execute("""UPDATE heart_watch SET heartNum = %d WHERE
                colour = '%s'""" % (cellNum, chosenColour))
    conn.commit()
    return chosenColour

def watch_colour_reset(conn, cellNum):
    c = conn.cursor()
    c.execute("""UPDATE heart_watch SET status = 0 WHERE
                heartNum = '%d'""" % cellNum)
    c.execute("""UPDATE heart_watch SET heartNum = 0 WHERE
                heartNum = '%d'""" % cellNum)
    conn.commit()

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
            for i in range(420):
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

def release(conn,location):
    sql = """ UPDATE heart_store
              SET qr_code = 0 ,
                  heart_rate = 0
              WHERE  cell_id = '%d' """ % location
    c = conn.cursor()
    c.execute(sql)
    c.execute("""UPDATE heart_watch SET heartNum = 0, status = 0 WHERE
                heartNum = '%d'""" % location)
    conn.commit()

def QR_usage_checker(conn, qrcode):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM heart_store WHERE qr_code=%d" % qrcode)
        row = c.fetchall()
        if not row:
            print("UNIQUE")
            return(True)
        else:
            print("NOT UNIQUE")            
            return(row[0][0])
    except:
        pass

def unique_cell_picker(conn, short):
    c = conn.cursor()
    if short:
        print('SHORT')
        c.execute("SELECT * FROM heart_store WHERE qr_code=0 AND cell_id < 210")
    else:
        print('TALL')
        c.execute("SELECT * FROM heart_store WHERE qr_code=0")
    rows = c.fetchall()
    randomcell = random.randint(0,len(rows)-1)
    chosen_row = rows[randomcell]
    return(chosen_row[0])
    
# try to connect to the SQL server and database
try:
    conn = MySQLdb.connect(host,user,password,database)
    print("SQL connection successful:")
    print(conn)
except:
    print("Error connecting to the SQL database, are you on the correct network?")

# did the user want to use a previous table or load a new on
try:
    loadNew = sys.argv[1]     # check command line arguments
    if loadNew == "y":
        print("Storing old data")
        store_old_data(conn)
except:
    pass

if __name__ == "__main__":
    try:
        create_heartwatch_table(conn)
    except KeyboardInterrupt:
        print('End Prog')
        conn.close()

