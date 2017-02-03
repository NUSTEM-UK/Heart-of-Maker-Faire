import serial
import time
import random
import re

ser = serial.Serial('/dev/ttyUSB0', 9600)
heartCells = [0] * 10

emptyCells = []

codeNum = 0
for i in range(0,10):
    emptyCells.append(i)
    
while True:
    if not emptyCells:      #if there are no empty spaces left, end the programme
        break
    status = True
    newQRcode = ser.readline()  #read the current heart rate from the serial    
    codeNum = [int(s) for s in re.findall(r'\d+', newQRcode)] #strip the integers from the string
    print(codeNum[0])
    for i in heartCells:        #check if we already have this code logged
        if codeNum[0] == i:
            print("We've already had this code")
            status = False
            
    if status == True:          #if we've not had this code before randomly assign it to  cell and remove the cell from the empties list
        position = random.choice(emptyCells)
        print("Enter into cell %s:" % position)
        print(codeNum[0])
        emptyCells.remove(position)
        heartCells[position] = codeNum[0]

print("All cells are filled")

print(heartCells)
        
            
            
