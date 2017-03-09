from homfsql import *
from random import randint
from time import sleep

conn = create_connection("fourthtest.db")
# create_new_table(conn, True)

store_old_data(conn)

# while True:
#
#     newQR = randint(0,500)
#
#     isitnew = QR_usage_checker(conn, newQR)
#
#     if isitnew == True:
#         cell_num = unique_cell_picker(conn)
#         hr = randint(50, 160)
#         update_heart(conn, cell_num, newQR, hr)
#     else:
#         print("QR %s has already been used." % newQR)
#     sleep(1)
